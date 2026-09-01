---
name: eagle-untagged-organizer
description: Use when the user wants to rename, tag, or annotate untagged design assets in Eagle (via the eagle-mcp connector), or to merge/normalize an overgrown Eagle tag vocabulary. Triggers on mentions of Eagle, eagle-mcp, or untagged/未打标签 items combined with a batch-organize intent, or on tag-cleanup intent (合并标签/整理标签/重命名标签). Produces a name, a structured annotation, and tags for each asset based on visual analysis, covering both UI/UX references and graphic design works.
agent_created: true
version: 2.1.0
---

# Eagle Untagged Organizer

## Overview

Batch-organize untagged Eagle library assets via the `eagle-mcp` connector. This skill handles **UI/UX references** (web pages, mobile apps, dashboards, settings) and **graphic design works** (brand guidelines, posters, packaging, editorial spreads, icon sets, infographics, typography specimens).

It has two workflows:
1. **Untagged organizer** (default) — for every selected asset, produce a name, annotation, and tags, written in one `item_update` call.
2. **Tag governance** — merge/normalize an overgrown tag vocabulary (`tag_merge`, `tag_update`). See `references/tag-governance.md`.

For the organizer workflow, every selected asset produces three outputs:
1. A concise **name** (title-style, for quick identification & search)
2. A structured **annotation** (library-management perspective analysis)
3. **Tags** across three controlled dimensions (design domain / visual style / technique)

## Output Language

The skill body (instructions, logic, workflow) stays in English regardless of target language. Only the **three outputs written to Eagle** — the name, the annotation, and the tags — follow the target language.

**Default target language: 简体中文 (Simplified Chinese).** Unless the user explicitly asks otherwise, produce Chinese names/annotations and select tags from `references/vocabulary.md`.

When the user asks for a specific output language, route to the matching files:

| Target language | Vocabulary file | Annotation field labels |
|---|---|---|
| 简体中文 (default) | `references/vocabulary.md` | `设计类型 / 结构 / 视觉 / 用途 / 参考价值` |
| 繁體中文（港式） | `references/vocabulary-zh-Hant.md` | `設計類型 / 結構 / 視覺 / 用途 / 參考價值` |
| English | `references/vocabulary-en.md` | `Type / Structure / Visual / Use / Reference Value` |

The five annotation fields stay in the same logical order and meaning across all languages — only the labels and the tag vocabulary change.

## When to Use

- The user mentions Eagle, eagle-mcp, or untagged items.
- The user wants to rename, tag, or annotate multiple Eagle assets automatically.
- The user asks for a richer, more consistent metadata pass on design references (UI screenshots or graphic design works).
- **Tag governance** triggers: the user wants to merge/consolidate/normalize existing tags (e.g. "合并标签", "整理标签", "标签太乱", "重命名标签") — route to `references/tag-governance.md`.

## Prerequisites

- Eagle desktop app must be running, because `eagle-mcp` is an SSE proxy that connects to Eagle itself.
- `eagle-mcp` must be configured in `~/.workbuddy/mcp.json` under `mcpServers` and trusted in the connector panel.
- The connector exposes a set of tools; the key ones used by this skill are `item_get`, `item_count`, `item_update` (organizer), and `tag_get`, `tag_merge`, `tag_update` (governance).

## Supporting Files

Load these `references/` files only when needed, not all at once:

| File | When to read |
|---|---|
| `references/vocabulary.md` | Before producing tags in 简体中文 (default) — the canonical tag list (select verbatim, no invented terms) |
| `references/vocabulary-zh-Hant.md` | Before producing tags in 繁體中文（港式） — Hong Kong-convention Traditional Chinese tag list |
| `references/vocabulary-en.md` | Before producing tags in English — industry-standard English tag list |
| `references/templates.md` | Before producing names/annotations — the naming formula and the five-field annotation template (also inlined in Phase 2) |
| `references/gotchas.md` | Before the first `item_update` of a session, and whenever a call behaves unexpectedly |
| `references/tag-governance.md` | When the user wants to merge/consolidate/normalize existing tags (tag governance workflow) |

`scripts/apply_eagle_batch.py` is a bundled Python MCP-stdio client for bulk (100+) writes; use it instead of pasting large payloads into the chat. `scripts/build_dryrun.py` turns the analysis output into a reviewable manifest (Phase 3a). See `references/gotchas.md` for usage.

## Workflow

### Phase 0 — Pre-flight checks (environment probes, must pass before any writes)

These three probes are decoupled from the batch and run before anything else. Step 0a is mandatory and non-bypassable; 0b and 0c run once per environment.

**Step 0a. Multimodal capability check (mandatory gate).**
- Take **one** image as input: grab any single record from Eagle (`item_get` one item → read its `url` or local file path), or any locally readable image file that contains real pixel information.
- Read the image directly and judge whether the current model can truly "see" pixels (describe objects, colors, layout, text that are only knowable from pixels).
- **Multimodal capable** → continue.
- **Not multimodal capable** → stop everything immediately; do not enter the batch. Tell the user to switch to a multimodal-capable model and retry, since naming/annotation/tagging all depend on visual understanding.

**Step 0b. Connection check.**
- Confirm `eagle-mcp` is nested under `mcpServers` in `~/.workbuddy/mcp.json`. Test the connection (spawn the MCP server and send an `initialize` JSON-RPC request over stdio) if needed.

**Step 0c. Rename capability probe (once per environment).**
- The published `item_update` schema lists only `tags`, `folders`, `annotation`, `star`, but `name` is also accepted in practice. Verify by renaming a single test item, reading it back via `item_get`, then reverting. If `name` does not stick, fall back to `references/gotchas.md` (REST cannot rename; MCP `item_update` is required).

### Phase 1 — Fetch untagged items

- Call `item_get` with `isUntagged: true` (or `item_query` to locate previously-touched assets by name).
- Use `limit`/`offset` to page. Filter to image types (`jpg`, `png`, etc.) if the user asked for images.

### Phase 2 — Visually analyze each image

- Read each image file path returned by Eagle using the image-reading capability.
- Identify the asset as a UI/UX reference or a graphic design work, then produce name + annotation + tags. Keep granularity consistent across the batch.

**Annotation — mandatory five-field block (follow this exactly).** Do NOT invent your own field names. The annotation MUST contain these five fields, in this exact order, each on its own line. Use the field labels for the target language (see "Output Language" above).

**简体中文 (default):**

```
设计类型：<值>
结构：<值>
视觉：<值>
用途：<值>
参考价值：<值>
```

**繁體中文（港式）:**

```
設計類型：<值>
結構：<值>
視覺：<值>
用途：<值>
參考價值：<值>
```

**English:**

```
Type: <value>
Structure: <value>
Visual: <value>
Use: <value>
Reference Value: <value>
```

- `设计类型` / `設計類型` / `Type` = the design domain/type (海报 / 品牌 / 包装 / 编辑 / 图标 / 版式 / 信息图表 / 网页UI / 移动UI / 仪表盘 …).
- `结构` / `結構` / `Structure` = layout/composition and information hierarchy.
- `视觉` / `視覺` / `Visual` = visual style, color scheme, typography.
- `用途` / `用途` / `Use` = what it serves as a reference for.
- `参考价值` / `參考價值` / `Reference Value` = the standout merit worth collecting.

Formatting rules (hard):
- **One field per line, each on its own newline.** Never join the fields into a single continuous line or paragraph.
- Use the exact label for the target language followed by `：` (Chinese) or `: ` (English), then the value. No bullet markers, no blank lines between fields.

**Name** — use the title formula from `references/templates.md`. Names are free text in the target language and are **independent** of tag casing/vocabulary.

**Tags** — select verbatim from the vocabulary file matching the target language (see "Output Language"). See `references/templates.md` for the full template and an example.

### Phase 3a — Dry-run preview (required before any write)

Build a structured change manifest so the user can review and prune before anything is written. Do **not** write to Eagle in this phase.

- For every analyzed asset, collect the proposed change: `id`, `oldName` → `name`, `tags`, `annotation` (one-line summary per item).
- Write the manifest to a JSON file using `scripts/build_dryrun.py --input <analysis.json> --output dryrun_manifest.json`, so the user gets an editable list. (For very small batches ≤ 5 items, an inline table in the reply may suffice, but a file is always safer.)
- Present a human-readable summary in the reply: total count, and a table of `id / old name → new name / tags / annotation summary`, so the user can spot bad renames or wrong tags at a glance.
- Invite the user to edit the manifest file directly: delete any entry to skip it, or change `name`/`tags`/`annotation` to correct it. Only the entries left in the manifest will be applied.

### Phase 3b — Authorization gate (required before any write)

Based on the reviewed manifest, require explicit confirmation:
- **Scope**: how many assets remain in the manifest, and their IDs/names.
- **Per-asset change**: old name → new name, old tags → new tags (tags are **replaced**, not merged), annotation summary — as they stand after the user's edits.
- **Side effects**: renaming also changes the underlying file path; tag replacement discards any pre-existing tags.
- **Confirmation**: small batches (≤ N items, default 10) may proceed with a single confirmation; large batches require an explicit "confirm all" that acknowledges tag overwrite.

Do not proceed to Phase 4 until the user confirms the final manifest.

### Phase 4 — Batch update

- For small batches, build one `item_update` call with an `items` array (each item: `id`, `name`, `tags`, `annotation`).
- For large batches, feed the **reviewed manifest file** from Phase 3a directly to `scripts/apply_eagle_batch.py --tool item_update --payload dryrun_manifest.json` — the manifest format matches the script's payload, so only the entries the user left in the file get applied.
- Omit the `folders` key entirely unless you intend to move the item (Eagle preserves existing folder membership when `folders` is absent).

### Phase 5 — Verify

- Call `item_get` with the updated IDs to confirm names and tags.
- Call `item_get` with `fullDetails: true` on at least one item to confirm the annotation was saved.
- Re-read the items and confirm the returned count equals the requested count (large batches can silently drop entries).

## Scope & Out of Scope

**In scope**:
- The untagged organizer: rename, tag, and annotate untagged Eagle assets (UI/UX references and graphic design works) based on visual analysis.
- Tag governance: merge/normalize/rename existing tags — **only** via `references/tag-governance.md`, with dry-run preview and explicit authorization (these writes are global and irreversible).

**Out of scope** (do not perform these unless the user separately asks and confirms):
- Folder reorganization or moving items into/out of folders.
- Deleting assets or moving them to trash.
- Deduplicating or detecting near-duplicate assets.
- Any write to Eagle without passing the Phase 3a dry-run preview and the Phase 3b authorization gate (or the equivalent gates in `references/tag-governance.md`).
