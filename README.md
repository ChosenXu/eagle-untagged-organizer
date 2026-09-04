# Eagle Untagged Organizer

[English](README.md) | [中文](README.zh-CN.md)

A [WorkBuddy](https://www.workbuddy.cn/) skill that batch-organizes **untagged** design assets in [Eagle](https://eagle.cool/) via the `eagle-mcp` connector — renaming, annotating, and tagging UI/UX references and graphic-design works in one pass.

## What it does

For every selected untagged asset it produces three outputs, written back to Eagle in a single `item_update` call:

1. **Name** — a concise, title-style name (searchable in the Eagle grid); if an asset already has a good name, it is kept or proposed for overwrite rather than blindly renamed.
2. **Annotation** — a structured five-field block (设计类型 / 结构 / 视觉 / 用途 / 参考价值)
3. **Tags** — selected verbatim from a controlled three-dimension vocabulary (design domain / visual style / technique)

Output language is configurable: 简体中文 (default), 繁體中文（港式）, or English.

## Highlights

1. **Truly "reads" each asset before acting** — it never guesses from filenames. It first runs a multimodal pre-flight check, reading each image to understand its subjects, colors, and layout, and only then produces names and annotations — quality is guaranteed.
2. **Structured, reusable, and on-track** — names are short titles, not analytical sentences; annotations follow a fixed five-field template; tags come from a controlled three-dimension vocabulary and are selected verbatim (no invented terms). The result is a consistent library whose tag taxonomy never drifts out of control.
3. **Safety first: preview before writing** — every change is surfaced as a dry-run manifest for your review, and it batch-writes to Eagle only after you approve. After writing, it re-reads each item to verify — it never silently mutates your library.
4. **Scales to large batches** — for 100+ asset runs, a built-in Python script performs batch writes over stdio, so you don't cram huge payloads into the conversation.
5. **Respects your existing names** — assets that already have a good name keep it by default and only get annotation + tags; only meaningless / random names are auto-renamed, and whether to overwrite is always your call in the dry-run manifest.
6. **Recoverable batches** — before any write, one command snapshots every asset's current name / tags / annotation to a timestamped JSON; a companion script restores from it (after a `yes` confirmation) if a batch goes wrong.

## Install

Clone this repository into your WorkBuddy skills directory:

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.workbuddy/skills/eagle-untagged-organizer
```

Or copy the folder manually into `~/.workbuddy/skills/`.

## Prerequisites

- The Eagle desktop app must be running.
- `eagle-mcp` must be configured in `~/.workbuddy/mcp.json` and trusted in the connector panel.

## Usage

Mention Eagle / `eagle-mcp` / untagged assets with a batch-organize intent, and the skill drives the workflow. See [`SKILL.md`](SKILL.md) for the full workflow (pre-flight checks → analyze → dry-run preview → authorization gate → batch update → verify).

## Structure

```
SKILL.md                     # skill definition & workflow
references/
  vocabulary.md              # 简体中文 tag taxonomy (canonical)
  vocabulary-zh-Hant.md      # 繁體中文（港式） tag taxonomy
  vocabulary-en.md           # English tag taxonomy
  templates.md               # naming formula & five-field annotation template
  gotchas.md                 # pitfalls & call-shape gotchas
scripts/
  apply_eagle_batch.py       # bulk-apply item updates via MCP stdio proxy
  build_dryrun.py            # build a reviewable dry-run manifest
```

## License

[MIT](LICENSE)
