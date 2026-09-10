# Eagle Untagged Organizer

[English](../README.md) | [简体中文](README.zh-CN.md) | [繁体中文](README.zh-Hant.md) | [日本語](README.ja.md) | 한국어 | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md)

[Agent Skills](https://agentskills.io) 오픈 표준 호환 스킬. `eagle-mcp` MCP 서버를 통해 [Eagle](https://eagle.cool/)의 **태그 없는** 디자인 에셋을 일괄 정리합니다 — UI/UX 레퍼런스와 그래픽 디자인 작품의 이름 변경, 주석 추가, 태그 지정을 한 번에 수행합니다. Claude Code, Codex CLI, Gemini CLI, GitHub Copilot, Cursor, WorkBuddy에서 작동합니다.

## 기능

선택한 태그 없는 각 에셋에 대해 Eagle에 단일 `item_update` 호출로 기록되는 3가지 출력을 생성합니다:

1. **이름** — 간결한 타이틀 형식의 이름(Eagle 그리드에서 검색 가능). 에셋에 이미 좋은 이름이 있으면 무조건 바꾸지 않고 유지하거나 덮어쓰기로 제안합니다.
2. **주석** — 구조화된 5필드 블록(유형 / 구조 / 비주얼 / 용도 / 참고 가치)
3. **태그** — 통제된 3차원 어휘(디자인 영역 / 비주얼 스타일 / 기법)에서 그대로 선택

출력 언어는 설정 가능(简体中文 / 繁體中文（港式）/ English / 日本語 / 한국어 / Русский / Español / Deutsch). 사용자 지시 언어가 지원 언어면 그 언어를 상속하고, 그렇지 않으면 영어로 폴백합니다.

## 주요 특징

1. **실행 전 각 에셋을 실제로 "읽음"** — 파일명으로 추측하지 않습니다. 먼저 멀티모달 사전 점검을 실행해 각 이미지를 읽고 주제·색상·레이아웃을 파악한 뒤 이름과 주석을 생성합니다. 품질이 보장됩니다.
2. **체계적이고 재사용 가능하며 일관되게 유지됨** — 이름은 분석 문장이 아닌 짧은 타이틀. 주석은 고정된 5필드 템플릿을 따릅니다. 태그는 통제된 3차원 어휘에서 그대로 선택(조작된 용어 없음). 결과는 태그 분류가 통제 불능으로 무너지지 않는 일관된 라이브러리입니다.
3. **안전 제일: 쓰기 전 미리보기** — 모든 변경은 검토용 dry-run 매니페스트로 표시되며, 사용자가 승인한 후에만 Eagle에 일괄 기록됩니다. 쓰기 후에는 각 항목을 다시 읽어 검증 — 라이브러리를 조용히 변경하지 않습니다.
4. **대규모 배치도 가능** — 100개 이상 에셋 실행 시 내장 Python 스크립트가 stdio를 통해 일괄 기록하므로 거대한 페이로드를 대화에 밀어넣을 필요가 없습니다.
5. **기존 이름 존중** — 이미 좋은 이름이 있는 에셋은 기본적으로 유지되고 주석+태그만 추가됩니다. 무의미/임의의 이름만 자동으로 이름이 바뀌며, 덮어쓸지는 항상 dry-run 매니페스트에서 사용자가 결정합니다.
6. **복구 가능한 배치** — 쓰기 전 한 명령으로 각 에셋의 현재 이름/태그/주석을 타임스탬프 JSON으로 스냅샷합니다. 배치에 문제가 생기면 함께 제공되는 스크립트가(`yes` 확인 후) 해당 스냅샷에서 복원합니다.

## 설치

이 스킬은 [Agent Skills](https://agentskills.io) 오픈 표준(`SKILL.md` + `scripts/` + `references/`)을 따르며, 호환되는 모든 AI 에이전트에서 동작합니다. 저장소를 사용 중인 에이전트의 스킬 디렉터리에 클론하세요:

| 에이전트 | 사용자 수준 | 프로젝트 수준 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | — |

팁: `~/.agents/skills/`는 에이전트 공통 디렉터리입니다 — Codex CLI, Gemini CLI, GitHub Copilot, Cursor는 기본적으로 읽고, Claude Code도 폴백 경로로 스캔합니다. 한 번 설치로 여러 에이전트에서 발견됩니다.

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.agents/skills/eagle-untagged-organizer
```

또는 폴더를 위 디렉터리 중 하나에 수동으로 복사하세요.

## 사전 요구사항

- Eagle 데스크톱 앱이 실행 중이어야 합니다.
- `eagle-mcp`(Eagle 공식 플러그인에 포함된 stdio MCP 서버)를 사용 중인 에이전트의 MCP 설정에 등록해야 합니다:

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

| 에이전트 | MCP 설정 |
|---|---|
| Claude Code | `claude mcp add`(사용자 수준) 또는 프로젝트 `.mcp.json` |
| Codex CLI | `~/.codex/config.toml` → `[mcp_servers.eagle-mcp]` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers` |
| GitHub Copilot | `~/.copilot/mcp-config.json`(`"type": "local"`) 또는 저장소 루트의 `.mcp.json` |
| Cursor | `~/.cursor/mcp.json` |
| WorkBuddy | `~/.workbuddy/mcp.json` → `mcpServers` |

> Codex CLI는 TOML 형식을 사용합니다: `~/.codex/config.toml`에 `[mcp_servers.eagle-mcp]`를 추가하고 `command = "node"`, `args = ["<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"]`로 설정하세요.
>
> Gemini CLI는 위와 동일한 `mcpServers` JSON 구조를 `~/.gemini/settings.json`에 작성합니다(또는 `gemini mcp add -s user eagle-mcp node "<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"` 실행).
>
> GitHub Copilot: 동일한 서버를 `"type": "local"`과 함께 `~/.copilot/mcp-config.json`에 추가하세요(또는 `copilot mcp add eagle-mcp -- node "<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"` 실행).

## 사용법

Eagle / `eagle-mcp` / 태그 없는 에셋을 일괄 정리 의도와 함께 언급하면 스킬이 워크플로를 주도합니다. 전체 워크플로(사전 점검 → 분석 → dry-run 미리보기 → 승인 게이트 → 일괄 업데이트 → 검증)는 [`SKILL.md`](../SKILL.md)를 참조하세요.

> 반대로 엉망인 태그 어휘를 정리(태그 병합 / 이름 변경 / 폐기)하고 싶다면 [`eagle-tag-governance`](https://github.com/ChosenXu/eagle-tag-governance)를 사용하세요. 두 스킬은 서로 독립적입니다.

## 구조

```
SKILL.md                     # 스킬 정의와 워크플로
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

## 라이선스

[MIT](../LICENSE)
