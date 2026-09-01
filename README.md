# Eagle Untagged Organizer

A [WorkBuddy](https://www.workbuddy.cn/) skill that batch-organizes **untagged** design assets in [Eagle](https://eagle.cool/) via the `eagle-mcp` connector — renaming, annotating, and tagging UI/UX references and graphic-design works in one pass. It also provides a **tag-governance** workflow to merge/normalize an overgrown tag vocabulary.

## What it does

For every selected untagged asset it produces three outputs, written back to Eagle in a single `item_update` call:

1. **Name** — a concise, title-style name (searchable in the Eagle grid)
2. **Annotation** — a structured five-field block (设计类型 / 结构 / 视觉 / 用途 / 参考价值)
3. **Tags** — selected verbatim from a controlled three-dimension vocabulary (design domain / visual style / technique)

Output language is configurable: 简体中文 (default), 繁體中文（港式）, or English.

## Install

Clone this repository into your WorkBuddy skills directory:

```bash
git clone https://github.com/<your-user>/eagle-untagged-organizer.git \
  ~/.workbuddy/skills/eagle-untagged-organizer
```

Or copy the folder manually into `~/.workbuddy/skills/`.

## Prerequisites

- The Eagle desktop app must be running.
- `eagle-mcp` must be configured in `~/.workbuddy/mcp.json` and trusted in the connector panel.

## Usage

Mention Eagle / `eagle-mcp` / untagged assets with a batch-organize intent (or a tag-cleanup intent such as "合并标签" / "整理标签"), and the skill drives the workflow. See [`SKILL.md`](SKILL.md) for the full workflow (pre-flight checks → analyze → dry-run preview → authorization gate → batch update → verify).

## Structure

```
SKILL.md                     # skill definition & workflow
references/
  vocabulary.md              # 简体中文 tag taxonomy (canonical)
  vocabulary-zh-Hant.md      # 繁體中文（港式） tag taxonomy
  vocabulary-en.md           # English tag taxonomy
  templates.md               # naming formula & five-field annotation template
  gotchas.md                 # pitfalls & call-shape gotchas
  tag-governance.md          # merge/normalize tags workflow
scripts/
  apply_eagle_batch.py       # bulk-apply item updates via MCP stdio proxy
  build_dryrun.py            # build a reviewable dry-run manifest
```

## License

[MIT](LICENSE)
