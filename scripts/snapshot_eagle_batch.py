#!/usr/bin/env python3
"""Export a read-only pre-write snapshot of a batch of Eagle items.

Reads the id list from a dry-run manifest (produced by build_dryrun.py),
fetches each item's current name / tags / annotation via `item_get` with
`fullDetails`, and writes a timestamped JSON snapshot. This is purely
read-only — it never writes to Eagle — and gives you a rollback point before
apply_eagle_batch.py modifies the batch. See SKILL.md Phase 3, Step 3-pre.

Usage:
    python3 snapshot_eagle_batch.py --manifest dryrun_manifest.json [--out-dir <dir>]

The snapshot file is named `eagle-rollback-YYYYMMDD-HHMMSS.json` and written
to `--out-dir` (default: ~/.workbuddy/skill-backups/eagle-untagged-organizer-rollbacks/).
Roll back later with restore_eagle_snapshot.py --snapshot <file>.
"""

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_eagle_batch import MCPClient, resolve_proxy

DEFAULT_OUT_DIR = os.path.expanduser(
    "~/.workbuddy/skill-backups/eagle-untagged-organizer-rollbacks"
)
GET_BATCH = 500  # item_get ids limit is 1000; stay safely under it


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True,
                    help="dry-run manifest JSON (from build_dryrun.py) with an 'items' array")
    ap.add_argument("--out-dir", default=DEFAULT_OUT_DIR,
                    help="directory for the snapshot JSON (created if missing)")
    ap.add_argument("--proxy", default=None, help="path to mcp-proxy.js (auto-detected)")
    args = ap.parse_args()

    try:
        with open(args.manifest) as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit(f"error: manifest not found: {args.manifest}")
    except json.JSONDecodeError as e:
        sys.exit(f"error: manifest is not valid JSON: {e}")

    items = data.get("items") if isinstance(data, dict) else data
    if not isinstance(items, list):
        sys.exit('error: manifest must contain an "items" array')

    ids = [it["id"] for it in items if isinstance(it, dict) and it.get("id")]
    if not ids:
        sys.exit("error: no item ids found in manifest")

    os.makedirs(args.out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(args.out_dir, f"eagle-rollback-{ts}.json")

    client = MCPClient(resolve_proxy(args.proxy))
    client.initialize()

    # Fetch current state in safe batches (read-only).
    fetched = {}
    for i in range(0, len(ids), GET_BATCH):
        chunk = ids[i:i + GET_BATCH]
        res = client.call_tool("item_get", {"ids": chunk, "fullDetails": True})
        content = res.get("result", {}).get("content", [])
        text = content[0].get("text", "") if content else ""
        if res.get("result", {}).get("isError"):
            print(f"WARNING: item_get failed for chunk {i//GET_BATCH + 1}: {text[:200]}")
            continue
        try:
            d = json.loads(text)
        except Exception:
            print(f"WARNING: could not parse item_get response for chunk {i//GET_BATCH + 1}")
            continue
        for it in d.get("data", []):
            if it.get("id"):
                fetched[it["id"]] = it

    client.close()

    snap = {
        "generatedAt": datetime.now().isoformat(),
        "source": "eagle-untagged-organizer pre-write snapshot",
        "items": [],
    }
    missing = []
    for i in ids:
        it = fetched.get(i)
        if not it:
            missing.append(i)
            continue
        snap["items"].append({
            "id": i,
            "name": it.get("name", ""),
            "tags": it.get("tags", []),
            "annotation": it.get("annotation", ""),
        })

    try:
        with open(out_path, "w") as f:
            json.dump(snap, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # Snapshot is a safety net, not a required step — warn, don't abort.
        print(f"WARNING: could not write snapshot ({e}); batch proceeds without rollback point")
        return

    print(f"snapshot written: {out_path}")
    print(f"captured {len(snap['items'])}/{len(ids)} items")
    if missing:
        print(f"WARNING: {len(missing)} ids not returned by Eagle (skipped): {missing[:5]}")


if __name__ == "__main__":
    main()
