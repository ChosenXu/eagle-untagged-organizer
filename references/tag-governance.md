# Tag Governance (merge & consolidate tags)

This is a **separate workflow** from the untagged-asset organizer. Use it when the user wants to clean up an overgrown or inconsistent tag vocabulary — merge synonyms, normalize casing/spelling, or retire one-off tags. The writes here (`tag_merge`, `tag_update`) are **global, permanent, and irreversible**, so they are guarded by the same dry-run + authorization discipline as asset updates.

## When this workflow applies

- The user says tags are messy, too many, duplicated, or overlapping (e.g. "合并标签", "整理标签", "标签太乱了", "同义标签", "重命名标签").
- `tag_get` reveals many near-duplicate or near-synonym tags (e.g. `网页UI` vs `网页 UI` vs `网页界面`, or `海报` vs `宣传海报`).
- The user wants to normalize a tag set against the controlled vocabulary in `references/vocabulary.md`.

## Workflow

### Step 1 — Scan the current tag vocabulary

- Call `tag_get` with `coreFieldsOnly: true` to list all tags and their usage counts (use `tag_count` if you only need the total).
- Sort by count. Focus on: (a) tags with near-zero usage (likely junk), (b) pairs/groups that are obvious synonyms or spelling/casing variants, (c) tags that overlap the canonical terms in `references/vocabulary.md`.

### Step 2 — Propose merge/rename operations

Group the findings into concrete operations:

- **Merge** (source → target): two tags mean the same thing; pick the canonical one as target. Use `tag_merge` with `operations: [{source, target}]`.
- **Rename** (oldName → newName): a tag has a wrong/inconsistent name but no obvious duplicate; fix its spelling or casing. Use `tag_update` with `tags: [{oldName, newName}]`.

Decision rules:
- Prefer the canonical spelling from `references/vocabulary.md` as the target/newName.
- When neither form is in the vocabulary, prefer the most common existing form (highest count) as target, so fewer items change.
- Do **not** merge two tags that are merely related but distinct (e.g. `海报` vs `包装` are different domains, not synonyms).
- Flag any uncertain pair for the user instead of silently merging.

### Step 3 — Dry-run preview

- Present a table: each operation (`source → target` or `oldName → newName`), the affected item count (from `tag_get`), and the rationale.
- Also show the **consequences**: `tag_merge` removes the source tag everywhere and is irreversible; `tag_update` renames globally and is permanent.
- Write the operation list to a JSON file (e.g. `merge_plan.json`) shaped exactly like the tool args, so the user can edit/prune it — the same review pattern as the asset dry-run manifest.

### Step 4 — Authorization gate

- Require explicit confirmation before running any `tag_merge` / `tag_update`. List the operations, the affected counts, and the irreversibility.
- These are **global** operations: they touch every item using the tag, not just the current batch. State this explicitly.
- Do not run both `tag_merge` and `tag_update` in a way that races; prefer one tool call per distinct semantic change, verify, then continue.

### Step 5 — Apply & verify

- Apply the confirmed operations (small sets: one `tag_merge` / `tag_update` call with the operations array; large sets: drive via the MCP stdio client as in `references/gotchas.md`).
- Verify with `tag_get` (the source tags should be gone, target counts should have increased) and spot-check a few items with `item_get`.

## Key gotchas (tag-specific)

- `tag_merge` is **irreversible** — the source tag is deleted and cannot be recovered. There is no undo.
- `tag_update` is **global and permanent** — it renames the tag on every item, tag group, starred tag, and history entry.
- These tools operate on **tag names**, not tag IDs. Ensure names are exact (case-sensitive, no stray spaces) before running.
- The `operations`/`tags` args are plain JSON arrays — do not wrap in `{operations: [...]}` → already correct, but never nest further (see the array-param gotcha in `references/gotchas.md`).
