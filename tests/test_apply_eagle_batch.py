#!/usr/bin/env python3
"""Minimal selftest for scripts/apply_eagle_batch.py (stdlib unittest, offline).

Run from the skill root:
    python3 -m unittest discover -s tests -v

Covers the two historically buggy spots: clean_items payload hygiene
(v2.7.0 S-5: dirty entries dropped instead of poisoning the batch) and
count_item_successes (S-11: per-item success parsed instead of trusting
the batch-level isError flag).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import apply_eagle_batch as ab  # noqa: E402


class CleanItemsTests(unittest.TestCase):
    def test_rename_with_explicit_name(self):
        # rename entry carrying the final name: used as-is
        cleaned = ab.clean_items([{
            "id": "K1", "oldName": "IMG_0001", "nameAction": "rename",
            "name": "新标题", "tags": "设计", "annotation": "注释",
        }])
        self.assertEqual(len(cleaned), 1)
        entry = cleaned[0]
        self.assertEqual(entry["name"], "新标题")
        for gone in ("oldName", "nameAction", "proposedName"):
            self.assertNotIn(gone, entry)  # Eagle schema forbids them
        self.assertEqual(entry["tags"], "设计")

    def test_rename_falls_back_to_proposed_name(self):
        # rename entry without a final name: proposedName is applied
        cleaned = ab.clean_items([{
            "id": "K1b", "oldName": "IMG_0001", "nameAction": "rename",
            "proposedName": "兜底标题",
        }])
        self.assertEqual(cleaned[0]["name"], "兜底标题")
        self.assertNotIn("proposedName", cleaned[0])

    def test_keep_omits_name(self):
        # nameAction=keep → no `name` field at all, Eagle keeps existing name
        cleaned = ab.clean_items([{
            "id": "K2", "name": "旧标题", "nameAction": "keep",
        }])
        self.assertEqual(len(cleaned), 1)
        self.assertNotIn("name", cleaned[0])

    def test_dirty_entries_dropped(self):
        # 2.7.0 S-5: non-dict / id-less entries are dropped, not forwarded
        cleaned = ab.clean_items([
            "not-a-dict",
            {"title": "no id here"},
            {"id": "K3", "nameAction": "keep"},
        ])
        self.assertEqual([e["id"] for e in cleaned], ["K3"])

    def test_rename_without_any_name_warns_but_keeps_entry(self):
        cleaned = ab.clean_items([{"id": "K4", "nameAction": "rename"}])
        self.assertEqual(len(cleaned), 1)
        self.assertNotIn("name", cleaned[0])


class CountItemSuccessesTests(unittest.TestCase):
    def test_per_item_failure_not_counted(self):
        # S-11: batch says success while an item failed — count must reflect
        # the per-item verdicts, not the batch flag
        text = '{"success": true, "data": [{"id": "a", "success": true}, {"id": "b", "success": false}]}'
        self.assertEqual(ab.count_item_successes(text, fallback=2), 1)

    def test_all_items_success(self):
        text = '{"success": true, "data": [{"id": "a"}, {"id": "b"}]}'
        self.assertEqual(ab.count_item_successes(text, fallback=0), 2)

    def test_no_per_item_data_falls_back(self):
        self.assertEqual(ab.count_item_successes('{"success": true}', fallback=3), 3)
        self.assertEqual(ab.count_item_successes("not json", fallback=4), 4)

    def test_batch_failure_without_data_is_zero(self):
        text = '{"success": false, "message": "Item not found"}'
        self.assertEqual(ab.count_item_successes(text, fallback=1), 0)


if __name__ == "__main__":
    unittest.main()
