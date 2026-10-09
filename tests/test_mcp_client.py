#!/usr/bin/env python3
"""Offline selftest for MCPClient in scripts/apply_eagle_batch.py.

MCPClient is where the three P2 bugs of v2.6.2 lived (P-1 stderr pipe
deadlock, P-2 wall-clock timeout math, P-3 unreaped child process), and
none of that was under test. These tests substitute a fake Popen so no
node process and no running Eagle are needed.

Run from the skill root:
    python3 -m unittest discover -s tests -v
"""

import contextlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import apply_eagle_batch as ab  # noqa: E402


class FakeWriter(io.StringIO):
    """stdin stand-in that records close() so close() paths can be asserted."""

    def __init__(self):
        super().__init__()
        self.is_closed = False

    def close(self):
        self.is_closed = True
        super().close()


class FakePopen:
    """Popen stand-in with pre-loaded stdout/stderr and call recording."""

    def __init__(self, stdout_lines=(), stderr_lines=()):
        self.stdout = io.StringIO("".join(line + "\n" for line in stdout_lines))
        self.stderr = io.StringIO("".join(line + "\n" for line in stderr_lines))
        self.stdin = FakeWriter()
        self.terminated = False
        self.waited = False
        self.closed_pipes = []

    def terminate(self):
        self.terminated = True

    def wait(self, timeout=None):
        self.waited = True
        return 0


def rpc(msg_id, result='{"ok": true}'):
    return '{"jsonrpc": "2.0", "id": %s, "result": %s}' % (msg_id, result)


class MCPClientTestCase(unittest.TestCase):
    def setUp(self):
        self.popen_calls = []

    def make_client(self, stdout_lines=(), stderr_lines=()):
        # Patch the subprocess module attribute as seen from the script so
        # MCPClient never spawns a real node process. restore afterwards.
        real_popen = ab.subprocess.Popen
        self.addCleanup(setattr, ab.subprocess, "Popen", real_popen)

        def fake_popen(argv, **kwargs):
            self.popen_calls.append(argv)
            return FakePopen(stdout_lines, stderr_lines)

        ab.subprocess.Popen = fake_popen
        client = ab.MCPClient("fake-proxy.js")
        self.addCleanup(client.close)
        return client

    def test_initialize_roundtrip(self):
        client = self.make_client(stdout_lines=[rpc(1, '{"serverInfo": {"name": "fake"}}')])
        init = client.initialize()
        self.assertIsNotNone(init)
        self.assertEqual(init["result"]["serverInfo"]["name"], "fake")
        # the initialize request went through stdin as one JSON line
        sent = client.p.stdin.getvalue()
        self.assertIn('"method": "initialize"', sent)

    def test_wait_discards_mismatched_ids(self):
        client = self.make_client(stdout_lines=[
            '{"jsonrpc": "2.0", "method": "noise"}',  # notification, no id
            rpc(99),                                   # late response for someone else
            rpc(1),                                    # the one we wait for
        ])
        got = client._wait(1, timeout=10)
        self.assertIsNotNone(got)
        self.assertEqual(got["id"], 1)
        # consumed messages are not re-delivered to a later waiter
        self.assertIsNone(client._wait(99, timeout=0))

    def test_wait_timeout_returns_none_without_matching_response(self):
        client = self.make_client(stdout_lines=[])
        self.assertIsNone(client._wait(7, timeout=0))
        self.assertIsNone(client.call_tool("item_update", {"items": []}, timeout=0))

    def test_stderr_drained_and_forwarded(self):
        noisy = ["Eagle MCP Proxy log line %d" % i for i in range(500)]
        # Redirect stderr BEFORE creating the client: the reader thread starts
        # in __init__ and may write within microseconds, so a later redirect
        # loses the first lines to the real stderr (observed: 498/500).
        captured = io.StringIO()
        with contextlib.redirect_stderr(captured):
            client = self.make_client(stdout_lines=[rpc(1)], stderr_lines=noisy)
            client.t_err.join(timeout=5)
        out = captured.getvalue()
        self.assertIn("[mcp-proxy] Eagle MCP Proxy log line 499", out)
        self.assertEqual(out.count("Eagle MCP Proxy log line"), 500)

    def test_close_reaps_child_and_closes_all_pipes(self):
        client = self.make_client(stdout_lines=[], stderr_lines=[])
        fake = client.p
        client.close()
        self.assertTrue(fake.terminated)
        self.assertTrue(fake.waited)
        self.assertTrue(fake.stdin.is_closed)
        self.assertTrue(fake.stdout.closed)
        self.assertTrue(fake.stderr.closed)


if __name__ == "__main__":
    unittest.main()
