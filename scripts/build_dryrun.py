#!/usr/bin/env python3
"""Build a dry-run change manifest for a batch of Eagle item updates.

The manifest is a JSON file the user can review and edit (delete/keep/alter
individual entries) before any write happens. After review, the SAME file is
fed to `apply_eagle_batch.py --payload <manifest>` to apply exactly the
entries that remain — so "review → prune → apply" is one clean, auditable
loop and nothing is written that was not explicitly left in the manifest.

Manifest format (matches apply_eagle_batch.py's payload; review-only fields are
stripped before send):
    {
      "items": [
        {
          "id": "...",
          "oldName": "...",        # review-only (ignored by apply script)
          "nameAction": "keep",    # "keep" preserves the existing name; "rename" sends proposedName
          "proposedName": "...",   # set only when nameAction is rename/propose
          "name": "...",           # carried for propose/rename entries; the script sends it only when nameAction=="rename"
          "tags": [...],
          "annotation": "..."
        }
      ]
    }

Notes:
    - `oldName` / `nameAction` / `proposedName` are review-only metadata;
      `apply_eagle_batch.py` strips them before sending and honors `nameAction`
      (sends `name` only when `nameAction == "rename"`, else omits it so Eagle
      keeps the existing name).
    - This script does NOT write to Eagle. It only writes the local manifest.
"""

import argparse
import json
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True,
                    help="JSON file produced during analysis, list of proposed items")
    ap.add_argument("--output", required=True,
                    help="path to write the review manifest (e.g. dryrun_manifest.json)")
    args = ap.parse_args()

    try:
        with open(args.input) as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit(f"error: input file not found: {args.input}")
    except json.JSONDecodeError as e:
        sys.exit(f"error: input is not valid JSON: {e}")

    items = data.get("items") if isinstance(data, dict) else data
    if not isinstance(items, list):
        sys.exit('error: input must be a list of items or {"items": [...]}')

    manifest = {"items": []}
    for it in items:
        if not isinstance(it, dict) or "id" not in it:
            print(f"warning: skipping malformed entry (no id): {it!r}")
            continue
        # Carry review-only fields through so the user sees what changes and
        # can choose per-asset whether to keep or overwrite the existing name.
        # `nameAction` defaults to "rename" for backward compatibility with
        # plain manifests that have no nameAction; the analysis step should set
        # it explicitly ("keep" | "rename").
        entry = {
            "id": it["id"],
            "oldName": it.get("oldName", it.get("name", "")),
            "nameAction": it.get("nameAction", "rename"),
            "proposedName": it.get("proposedName", it.get("name", "")),
            "name": it.get("name", ""),
            "tags": it.get("tags", []),
            "annotation": it.get("annotation", ""),
        }
        manifest["items"].append(entry)

    with open(args.output, "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"wrote {len(manifest['items'])} items to {args.output}")
    print("review this file, delete/alter any entries you want to skip, then run:")
    print(f"  python3 scripts/apply_eagle_batch.py --tool item_update --payload {args.output}")


if __name__ == "__main__":
    main()
