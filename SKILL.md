---
name: eagle-untagged-organizer
description: Use when the user wants to rename, tag, or annotate untagged design assets in Eagle (via the eagle-mcp connector). Triggers on mentions of Eagle, eagle-mcp, or untagged/未打标签 items combined with a batch-organize intent. Produces a name, a structured annotation, and tags for each asset based on visual analysis, covering both UI/UX references and graphic design works.
agent_created: true
version: 2.4.0
---

# Eagle Untagged Organizer

## Overview

Batch-organize untagged Eagle library assets via the `eagle-mcp` connector. This skill handles **UI/UX references** (web pages, mobile apps, dashboards, settings) and **graphic design works** (brand guidelines, posters, packaging, editorial spreads, icon sets, infographics, typography specimens).

It has a single workflow — the **Untagged organizer**: for every selected asset, produce a name, annotation, and tags, written in one `item_update` call.

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

## Prerequisites

- Eagle desktop app must be running, because `eagle-mcp` is an SSE proxy that connects to Eagle itself.
- `eagle-mcp` must be configured in `~/.workbuddy/mcp.json` under `mcpServers` and trusted in the connector panel.
- The connector exposes a set of tools; the key ones used by this skill are `item_get`, `item_count`, and `item_update`.

## Supporting Files

Load these `references/` files only when needed, not all at once:

| File | When to read |
|---|---|
| `references/vocabulary.md` | Before producing tags in 简体中文 (default) — the canonical tag list (select verbatim, no invented terms) |
| `references/vocabulary-zh-Hant.md` | Before producing tags in 繁體中文（港式） — Hong Kong-convention Traditional Chinese tag list |
| `references/vocabulary-en.md` | Before producing tags in English — industry-standard English tag list |
| `references/templates.md` | Before producing names/annotations — the naming formula and the five-field annotation template (also inlined in Phase 2) |
| `references/gotchas.md` | Before the first `item_update` of a session, and whenever a call behaves unexpectedly |

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

**Step 0d. Naming mode (ask once before Phase 1).**
Decide how to treat assets that already have a name, so the batch does not blindly overwrite good user-chosen names:
- **Mode A (mixed, default)** — judge each asset individually per the Phase 2 name-disposition rules; the user reviews every decision in the dry-run manifest.
- **Mode B (trust existing names)** — the user states the names are already good; skip name generation for all assets, set `nameAction: "keep"` on every entry, and produce only annotation + tags. Saves analysis time and tokens.
- **Mode C (force regenerate)** — the user states to ignore existing names; set `nameAction: "rename"` on every entry and generate names for all, as the original v2.2.0 behavior.

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

**Name disposition — respect existing naming (judge this for every asset before producing a name).**
Inspect the asset's existing `name` (returned by Eagle) and classify it into one of three actions. Record the rationale so the user can review it in the dry-run manifest:

- **KEEP** — the existing name is semantically complete and good quality (real topical words, accurately describes the asset, reads like a title or an accurate phrase). Do **not** regenerate; only add annotation + tags.
- **PROPOSE** — the existing name is partially meaningful but vague / off-topic / awkward / over-long, or it looks clean but misses the asset's point. Keep the original by default, but also produce a `proposedName` so the user can choose to overwrite.
- **AUTO_RENAME** — the existing name is meaningless or random (UUID; `IMG_` / `screenshot_` / `微信图片_` / `QQ截图` / `捕获` / `未命名` / `Untitled`; pure date-digit stamps; or empty). Regenerate per the title formula in `references/templates.md`.

Score the existing name on two axes (0–2) to make the call reproducible:
- **Relevance**: off-topic (0) / partially relevant (1) / accurately describes the asset (2)
- **Form**: garbage / random (0) / readable but awkward (1) / clean title-style (2)

| Relevance | Form | Action |
|---|---|---|
| ≤1 | ≤1 | AUTO_RENAME |
| 2 | 2 | KEEP |
| 2 | ≤1 | PROPOSE (content good, tidy the form) |
| ≤1 | 2 | PROPOSE (form clean but off-topic) |
| =1 (either axis) | — | PROPOSE |

Conservative rule: only AUTO_RENAME when the name clearly matches a random-string pattern; otherwise prefer PROPOSE or KEEP so the user keeps control. In Mode B the disposition is moot — every asset is KEEP.

**Name** — use the title formula from `references/templates.md`. Names are free text in the target language and are **independent** of tag casing/vocabulary. For KEEP / PROPOSE assets this step is skipped; for AUTO_RENAME and Mode C it produces `proposedName`.

**Tags** — select verbatim from the vocabulary file matching the target language (see "Output Language"). See `references/templates.md` for the full template and an example.

### Phase 3a — Dry-run preview (required before any write)

Build a structured change manifest so the user can review and prune before anything is written. Do **not** write to Eagle in this phase.

- For every analyzed asset, collect the proposed change and emit it via `scripts/build_dryrun.py`: `id`, `oldName`, `nameAction` (`keep` | `rename`), `proposedName` (set only when `nameAction` is `rename` or `propose`), `tags`, `annotation` (one-line summary per item).
  - `nameAction: "keep"` → the bulk script OMITs `name` for this item, so Eagle preserves the existing name. (Verified: omitting `name` from `item_update` leaves the name unchanged — no path churn, no overwrite.)
  - `nameAction: "rename"` → the bulk script sends `name: proposedName`.
  - KEEP assets carry an empty `proposedName` and are never renamed. PROPOSE assets carry the suggestion in `proposedName` but default to `nameAction: "keep"` — the user flips it to `rename` to apply the overwrite. AUTO_RENAME / Mode C assets carry `nameAction: "rename"` with the generated `proposedName`.
- Write the manifest to a JSON file using `scripts/build_dryrun.py --input <analysis.json> --output dryrun_manifest.json`, so the user gets an editable list. (For very small batches ≤ 5 items, an inline table in the reply may suffice, but a file is always safer.)
- Present a human-readable summary in the reply: total count, and a table of `id / old name → (new name) / 命名处理 / tags / annotation summary`, where `命名处理` is one of `保留原名` / `建议覆盖（原名⇄建议名）` / `自动重命名`. This lets the user spot bad renames or wrong tags at a glance.
- Invite the user to edit the manifest file directly: delete any entry to skip it, change `name`/`tags`/`annotation` to correct it, or set an entry's `nameAction` to `keep` (preserve the original name) or `rename` (apply `proposedName`). Only the entries left in the manifest, with their final `nameAction`, will be applied.

### Phase 3b — Authorization gate (required before any write)

Based on the reviewed manifest, require explicit confirmation:
- **Scope**: how many assets remain in the manifest, and their IDs/names.
- **Per-asset change**: old name → new name, old tags → new tags (tags are **replaced**, not merged), annotation summary — as they stand after the user's edits.
- **Per-asset name handling**: for each entry, state whether the name is kept (`nameAction: keep`), proposed-overwrite (show both old name and `proposedName`), or auto-renamed — as they stand after the user's edits. No name is overwritten unless its `nameAction` is `rename`.
- **Side effects**: renaming also changes the underlying file path; tag replacement discards any pre-existing tags.
- **Confirmation**: small batches (≤ N items, default 10) may proceed with a single confirmation; large batches require an explicit "confirm all" that acknowledges tag overwrite.

Do not proceed to Phase 4 until the user confirms the final manifest.

**Step 3c. Pre-write rollback snapshot (recommended safety net).**
Before the Phase 4 write, capture the current state of every asset still in the manifest so a bad batch is recoverable:
- Run `scripts/snapshot_eagle_batch.py --manifest dryrun_manifest.json`. It reads the id list from the manifest, fetches each item's current `name` / `tags` / `annotation` through `item_get` (fullDetails), and writes a timestamped JSON snapshot to `~/.workbuddy/skill-backups/eagle-untagged-organizer-rollbacks/eagle-rollback-YYYYMMDD-HHMMSS.json`.
- This step is **read-only** and never writes to Eagle. If it fails (disk/permission), it only warns — the batch still proceeds.
- The snapshot covers exactly this batch's assets (not the whole library) and is the rollback point for this run.
- If a later batch goes wrong, restore with `scripts/restore_eagle_snapshot.py --snapshot <file>` — it prints a summary and asks you to type `yes` before overwriting anything.

### Phase 4 — Batch update

- For small batches, build one `item_update` call with an `items` array (each item: `id`, `name`, `tags`, `annotation`).
- For large batches, feed the **reviewed manifest file** from Phase 3a directly to `scripts/apply_eagle_batch.py --tool item_update --payload dryrun_manifest.json` — the manifest format matches the script's payload, so only the entries the user left in the file get applied.
- Omit the `folders` key entirely unless you intend to move the item (Eagle preserves existing folder membership when `folders` is absent).

### Phase 5 — Verify

- Call `item_get` with the updated IDs to confirm names and tags.
- Call `item_get` with `fullDetails: true` on at least one item to confirm the annotation was saved.
- Re-read the items and confirm the returned count equals the requested count (large batches can silently drop entries).
- If a verification check fails or the batch looks wrong, roll back with `scripts/restore_eagle_snapshot.py --snapshot <file>` using the Step 3c snapshot — it restores each item's original name / tags / annotation.

## Scope & Out of Scope

**In scope**:
- The untagged organizer: rename, tag, and annotate untagged Eagle assets (UI/UX references and graphic design works) based on visual analysis.

**Out of scope** (do not perform these unless the user separately asks and confirms):
- Folder reorganization or moving items into/out of folders.
- Deleting assets or moving them to trash.
- Deduplicating or detecting near-duplicate assets.
- Merging, renaming, normalizing, or retiring existing library tags — these are tag-governance operations handled by a separate skill, not this one.
- Any write to Eagle without passing the Phase 3a dry-run preview and the Phase 3b authorization gate.
