# Eagle Untagged Organizer

English | [简体中文](readme/README.zh-CN.md) | [繁体中文](readme/README.zh-Hant.md) | [日本語](readme/README.ja.md) | [한국어](readme/README.ko.md) | [Русский](readme/README.ru.md) | [Español](readme/README.es.md) | [Deutsch](readme/README.de.md)

An [Agent Skills](https://agentskills.io)-compatible skill that batch-organizes **untagged** design assets in [Eagle](https://eagle.cool/) via the `eagle-mcp` MCP server — renaming, annotating, and tagging UI/UX references and graphic-design works in one pass. Works with Claude Code, Codex CLI, Gemini CLI, GitHub Copilot, Cursor, and WorkBuddy.

## What it does

For every selected untagged asset it produces three outputs, written back to Eagle in a single `item_update` call:

1. **Name** — a concise, title-style name (searchable in the Eagle grid); if an asset already has a good name, it is kept or proposed for overwrite rather than blindly renamed.
2. **Annotation** — a structured five-field block (设计类型 / 结构 / 视觉 / 用途 / 参考价值)
3. **Tags** — selected verbatim from a controlled three-dimension vocabulary (design domain / visual style / technique)

Output language is configurable: 简体中文, 繁體中文（港式）, English, 日本語, 한국어, Русский, Español, Deutsch. When the user's instruction is written in a supported language, that language is inherited as the output language; otherwise (unsupported or ambiguous) it falls back to English.

## Highlights

1. **Truly "reads" each asset before acting** — it never guesses from filenames. It first runs a multimodal pre-flight check, reading each image to understand its subjects, colors, and layout, and only then produces names and annotations — quality is guaranteed.
2. **Structured, reusable, and on-track** — names are short titles, not analytical sentences; annotations follow a fixed five-field template; tags come from a controlled three-dimension vocabulary and are selected verbatim (no invented terms). The result is a consistent library whose tag taxonomy never drifts out of control.
3. **Safety first: preview before writing** — every change is surfaced as a dry-run manifest for your review, and it batch-writes to Eagle only after you approve. After writing, it re-reads each item to verify — it never silently mutates your library.
4. **Scales to large batches** — for 100+ asset runs, a built-in Python script performs batch writes over stdio, so you don't cram huge payloads into the conversation.
5. **Respects your existing names** — assets that already have a good name keep it by default and only get annotation + tags; only meaningless / random names are auto-renamed, and whether to overwrite is always your call in the dry-run manifest.
6. **Recoverable batches** — before any write, one command snapshots every asset's current name / tags / annotation to a timestamped JSON; a companion script restores from it (after a `yes` confirmation) if a batch goes wrong.

## Install

This skill follows the open [Agent Skills](https://agentskills.io) standard (`SKILL.md` + `scripts/` + `references/`) and works with any compatible AI agent. Clone this repository into your agent's skills directory:

| Agent | User-level directory | Project-level directory |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | — |

Tip: `~/.agents/skills/` is the cross-agent directory — Codex CLI, Gemini CLI, GitHub Copilot, and Cursor read it natively, and Claude Code scans it as a fallback too. One install, discovered by multiple agents.

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.agents/skills/eagle-untagged-organizer
```

Or copy the folder manually into any of the directories above.

## Prerequisites

- The Eagle desktop app must be running.
- `eagle-mcp` (the stdio MCP server bundled with Eagle's official plugin) must be registered in your agent's MCP configuration:

```json
{
  "mcpServers": {
    "eagle-mcp": {
      "command": "node",
      "args": ["<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"]
    }
  }
}
```

| Agent | MCP configuration |
|---|---|
| Claude Code | `claude mcp add` (user scope) or project `.mcp.json` |
| Codex CLI | `~/.codex/config.toml` → `[mcp_servers.eagle-mcp]` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers` |
| GitHub Copilot | `~/.copilot/mcp-config.json` (`"type": "local"`) or repo-root `.mcp.json` |
| Cursor | `~/.cursor/mcp.json` |
| WorkBuddy | `~/.workbuddy/mcp.json` → `mcpServers` |

> Codex CLI uses TOML instead: in `~/.codex/config.toml`, add `[mcp_servers.eagle-mcp]` with `command = "node"` and `args = ["<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"]`.
>
> Gemini CLI uses the same `mcpServers` JSON structure shown above in `~/.gemini/settings.json` (or run `gemini mcp add -s user eagle-mcp node "<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"`).
>
> GitHub Copilot: add the same server to `~/.copilot/mcp-config.json` with `"type": "local"` (or run `copilot mcp add eagle-mcp -- node "<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"`).

## Usage

Mention Eagle / `eagle-mcp` / untagged assets with a batch-organize intent, and the skill drives the workflow. See [`SKILL.md`](SKILL.md) for the full workflow (pre-flight checks → analyze → dry-run preview → authorization gate → batch update → verify).

> Need to clean up a messy tag vocabulary (merge, rename, or retire tags) instead? Use [`eagle-tag-governance`](https://github.com/ChosenXu/eagle-tag-governance). The two skills are independent.

## Structure

```
SKILL.md                     # skill definition & workflow
references/
  vocabulary.md              # 简体中文 tag taxonomy (canonical)
  vocabulary-zh-Hant.md      # 繁體中文（港式） tag taxonomy
  vocabulary-en.md           # English tag taxonomy
  vocabulary-ja.md           # 日本語 tag taxonomy
  vocabulary-ko.md           # 한국어 tag taxonomy
  vocabulary-ru.md           # Русский tag taxonomy
  vocabulary-es.md           # Español tag taxonomy
  vocabulary-de.md           # Deutsch tag taxonomy
  templates.md               # naming formula & five-field annotation template
  gotchas.md                 # pitfalls & call-shape gotchas
scripts/
  apply_eagle_batch.py       # bulk-apply item updates via MCP stdio proxy
  build_dryrun.py            # build a reviewable dry-run manifest
  snapshot_eagle_batch.py    # read-only: export a timestamped pre-write snapshot (id+name+tags+annotation)
  restore_eagle_snapshot.py  # restore assets from a snapshot via item_update (asks "yes" before writing)
```

## License

[MIT](LICENSE)
