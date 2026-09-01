#!/usr/bin/env python3
"""Bulk-apply Eagle item updates through the MCP stdio proxy.

Drives `node <mcp-proxy.js>` over JSON-RPC to call `item_update` (or any
tool) with a large `items` array, avoiding the need to paste a 100+ item
payload into the chat. This is the reliable path for bulk rename + tag +
annotate at scale — see SKILL.md Phase 4 and references/gotchas.md.

Usage:
    python3 apply_eagle_batch.py --tool item_update --payload /path/to/payload.json [--batch 20]

payload.json format:
    { "items": [ { "id": "...", "name": "...", "tags": [...], "annotation": "..." }, ... ] }

For other tools (e.g. item_get by ids), pass `--tool item_get` and a payload
shaped as that tool's arguments, e.g. { "ids": ["...", ...] }.

Notes:
    - Requires the Eagle desktop app to be running and `node` on PATH.
    - The proxy path is auto-detected; override with --proxy if needed.
    - Batch size default 20 (safe); the result text is printed for review,
      and success is judged per-batch by the tool's isError flag, NOT by
      string-matching. Always re-read items afterwards to confirm the
      returned count equals the requested count.
"""

import argparse
import json
import os
import queue
import subprocess
import sys
import threading
import time

# Keep these paths `~`-based and generic. Do NOT hardcode an absolute
# `/Users/<name>/...` path — that would break on other machines and leak the
# original author's macOS username when the skill is shared.
DEFAULT_PROXY_CANDIDATES = [
    os.path.expanduser("~/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"),
]


class MCPClient:
    def __init__(self, proxy):
        self.p = subprocess.Popen(
            ["node", proxy],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, bufsize=1,
        )
        self.q = queue.Queue()
        self.lock = threading.Lock()
        self.t = threading.Thread(target=self._reader, daemon=True)
        self.t.start()
        self._id = 0

    def _reader(self):
        for line in self.p.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except Exception:
                continue
            self.q.put(msg)

    def _send(self, obj):
        with self.lock:
            self.p.stdin.write(json.dumps(obj) + "\n")
            self.p.stdin.flush()

    def _wait(self, msg_id, timeout=60):
        end = time.time() + timeout
        while time.time() < end:
            try:
                m = self.q.get(timeout=2)
            except queue.Empty:
                continue
            if m.get("id") == msg_id:
                return m
        return None

    def initialize(self):
        self._id += 1
        rid = self._id
        self._send({
            "jsonrpc": "2.0", "id": rid, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "eagle-untagged-organizer", "version": "1.0"},
            },
        })
        init = self._wait(rid, 30)
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return init

    def call_tool(self, name, args, timeout=120):
        self._id += 1
        rid = self._id
        self._send({
            "jsonrpc": "2.0", "id": rid, "method": "tools/call",
            "params": {"name": name, "arguments": args},
        })
        return self._wait(rid, timeout)

    def close(self):
        for attr in ("stdin",):
            try:
                getattr(self.p, attr).close()
            except Exception:
                pass
        try:
            self.p.terminate()
        except Exception:
            pass


def resolve_proxy(explicit=None):
    if explicit:
        if os.path.isfile(explicit):
            return explicit
        sys.exit(f"error: --proxy path not found: {explicit}")
    for c in DEFAULT_PROXY_CANDIDATES:
        if os.path.isfile(c):
            return c
    sys.exit(
        "error: could not locate mcp-proxy.js. Pass --proxy <path> to the "
        "Eagle mcp-server modules/mcp-proxy.js file."
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tool", default="item_update", help="MCP tool name to call")
    ap.add_argument("--payload", required=True, help="JSON file holding the tool arguments")
    ap.add_argument("--batch", type=int, default=20, help="items per call (default 20)")
    ap.add_argument("--proxy", default=None, help="path to mcp-proxy.js (auto-detected)")
    args = ap.parse_args()

    if not os.path.isfile(args.payload):
        sys.exit(f"error: payload file not found: {args.payload}")
    with open(args.payload) as f:
        args_dict = json.load(f)

    # The bulk item_update payload is {"items": [...]}; chunk that array.
    items = args_dict.get("items")
    if not isinstance(items, list):
        sys.exit('error: payload must contain an "items" array')

    client = MCPClient(resolve_proxy(args.proxy))
    init = client.initialize()
    ok = init is not None
    info = (init or {}).get("result", {}).get("serverInfo")
    print("initialize:", "OK" if ok else "FAIL", info or "")
    if not ok:
        sys.exit("error: MCP initialize failed (is Eagle running?)")

    # Strip review-only fields (e.g. `oldName` from a dry-run manifest) before
    # sending, so the payload matches the tool's schema. The server rejects
    # unknown fields when the schema forbids additional properties, so feeding
    # the manifest verbatim would fail the whole batch.
    cleaned = []
    for it in items:
        if not isinstance(it, dict):
            cleaned.append(it)
            continue
        cleaned.append({k: v for k, v in it.items() if k != "oldName"})

    batches = [cleaned[i:i + args.batch] for i in range(0, len(cleaned), args.batch)]
    total_requested = len(cleaned)
    total_confirmed = 0
    for bi, batch in enumerate(batches, 1):
        res = client.call_tool(args.tool, {"items": batch})
        if res is None:
            print(f"batch {bi}/{len(batches)}: TIMEOUT (re-run needed for these {len(batch)} items)")
            continue
        is_err = res.get("result", {}).get("isError", False)
        content = res.get("result", {}).get("content", [])
        text = content[0].get("text", "") if content else ""
        print(f"batch {bi}/{len(batches)}: isError={is_err} | {text[:200]}")
        if not is_err:
            total_confirmed += len(batch)

    print(f"requested={total_requested} confirmed_ok={total_confirmed}")
    if total_confirmed != total_requested:
        print("WARNING: confirmed count != requested count — re-read the items "
              "afterwards to find any silently dropped entries.")
    client.close()


if __name__ == "__main__":
    main()
