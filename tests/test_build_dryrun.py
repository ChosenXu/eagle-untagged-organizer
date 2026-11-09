"""Offline tests for build_dryrun manifest building + atomic output."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "build_dryrun.py")


def _run(payload):
    d = tempfile.mkdtemp()
    inp = os.path.join(d, "in.json")
    out = os.path.join(d, "out.json")
    with open(inp, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    r = subprocess.run([sys.executable, SCRIPT, "--input", inp, "--output", out],
                       capture_output=True, text=True)
    data = None
    if os.path.exists(out):
        with open(out, encoding="utf-8") as f:
            data = json.load(f)
    return r, data, out


class BuildDryrunTests(unittest.TestCase):
    def test_builds_manifest(self):
        r, data, out = _run([{"id": "A", "name": "n", "tags": ["t"], "annotation": "a"}])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(data["items"][0]["id"], "A")
        self.assertFalse(os.path.exists(out + ".tmp"), "temp file left behind")

    def test_skips_malformed_entries(self):
        r, data, out = _run([{"id": "A"}, {"no": "id"}, "junk"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(data["items"]), 1)


if __name__ == "__main__":
    unittest.main()
