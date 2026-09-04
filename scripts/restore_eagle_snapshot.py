#!/usr/bin/env python3
"""Restore Eagle items from a pre-write snapshot (rollback).

Reads a snapshot JSON produced by snapshot_eagle_batch.py and writes back each
item's original name / tags / annotation via `item_update`. This OVERWRITES the
current values, so it is a true rollback to the pre-write state.

For safety it prints a summary and asks for explicit confirmation (type "yes")
before writing anything. See SKILL.md Phase 3, Step 3-pre.

Usage:
    python3 restore_eagle_snapshot.py --snapshot eagle-rollback-YYYYMMDD-HHMMSS.json [--batch 20]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_eagle_batch import MCPClient, resolve_proxy


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshot", required=True,
                    help="snapshot JSON from snapshot_eagle_batch.py")
    ap.add_argument("--batch", type=int, default=20,
                    help="items per item_update call (default 20)")
    ap.add_argument("--proxy", default=None, help="path to mcp-proxy.js (auto-detected)")
    args = ap.parse_args()

    try:
        with open(args.snapshot) as f:
            snap = json.load(f)
    except FileNotFoundError:
        sys.exit(f"error: snapshot not found: {args.snapshot}")
    except json.JSONDecodeError as e:
        sys.exit(f"error: snapshot is not valid JSON: {e}")

    items = snap.get("items", [])
    if not isinstance(items, list) or not items:
        sys.exit("error: snapshot has no items to restore")

    print(f"Rollback will restore {len(items)} items to their pre-write state:")
    for it in items[:10]:
        print(f"  - {it.get('id')}: {it.get('name', '')[:40]}")
    if len(items) > 10:
        print(f"  ... and {len(items) - 10} more")

    ans = input("Type 'yes' to confirm rollback: ").strip().lower()
    if ans != "yes":
        sys.exit("rollback cancelled — no changes made")

    client = MCPClient(resolve_proxy(args.proxy))
    client.initialize()

    payload = [{
        "id": it.get("id"),
        "name": it.get("name", ""),
        "tags": it.get("tags", []),
        "annotation": it.get("annotation", ""),
    } for it in items if it.get("id")]

    batches = [payload[i:i + args.batch] for i in range(0, len(payload), args.batch)]
    total_confirmed = 0
    for bi, batch in enumerate(batches, 1):
        res = client.call_tool("item_update", {"items": batch})
        if res is None:
            print(f"batch {bi}/{len(batches)}: TIMEOUT (re-run restore for these {len(batch)} items)")
            continue
        is_err = res.get("result", {}).get("isError", False)
        text = res.get("result", {}).get("content", [{}])[0].get("text", "")
        print(f"batch {bi}/{len(batches)}: isError={is_err} | {text[:120]}")
        if not is_err:
            total_confirmed += len(batch)

    print(f"restored={total_confirmed}/{len(payload)}")
    if total_confirmed != len(payload):
        print("WARNING: restored count != item count — re-read the items to find any "
              "silently dropped entries, then re-run restore if needed.")
    client.close()


if __name__ == "__main__":
    main()
