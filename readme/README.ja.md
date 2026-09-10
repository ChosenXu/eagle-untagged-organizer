# Eagle Untagged Organizer

[English](../README.md) | [简体中文](README.zh-CN.md) | [繁体中文](README.zh-Hant.md) | 日本語 | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md)

[Agent Skills](https://agentskills.io) オープン標準に準拠したスキル。`eagle-mcp` MCP サーバー経由で [Eagle](https://eagle.cool/) 内の**未タグ付け**デザイン素材を一括整理します。UI/UX リファレンスやグラフィックデザイン作品に対し、リネーム・注釈・タグ付けを一度に実行します。Claude Code、Codex CLI、Gemini CLI、GitHub Copilot、Cursor、WorkBuddy で動作します。

## 概要

選択した未タグ付け素材ごとに、Eagle へ単一の `item_update` 呼び出しで書き戻される 3 つの出力を生成します：

1. **名前** — 簡潔なタイトル形式の名前（Eagle グリッドで検索可能）。素材に既に良い名前がある場合は、むやみにリネームせず、保持または上書き提案を行います。
2. **注釈** — 構造化された 5 フィールドブロック（タイプ / 構成 / ビジュアル / 用途 / 参考価値）
3. **タグ** — 制御された 3 次元語彙（デザイン領域 / ビジュアルスタイル / 技法）からそのまま選択

出力言語は設定可能（简体中文 / 繁體中文（港式）/ English / 日本語 / 한국어 / Русский / Español / Deutsch）。ユーザーの指示言語が対応言語ならそれを継承し、それ以外は英語にフォールバックします。

## ハイライト

1. **実行前に各素材を本当に「読む」** — ファイル名から推測しません。まずマルチモーダルな事前チェックを実行し、各画像を読んで被写体・色・レイアウトを理解してから名前と注釈を生成します。品質が保証されます。
2. **構造化され、再利用可能、軌道に乗る** — 名前は分析文ではなく短いタイトル。注釈は固定の 5 フィールドテンプレートに従う。タグは制御された 3 次元語彙からそのまま選択（造語なし）。結果は一貫したライブラリとなり、タグ体系が制御不能に崩れることはありません。
3. **安全最優先：書き込み前にプレビュー** — すべての変更はレビュー用の dry-run マニフェストとして提示され、あなたが承認して初めて Eagle へ一括書き込みされます。書き込み後は各アイテムを再読み取りして検証 — ライブラリを黙って変更することはありません。
4. **大規模バッチにも対応** — 100 以上の素材実行では、組み込みの Python スクリプトが stdio 経由で一括書き込みを行うため、巨大なペイロードを会話に詰め込む必要がありません。
5. **既存の名前を尊重** — 既に良い名前がある素材はデフォルトで保持され、注釈＋タグのみが付きます。無意味／ランダムな名前のみ自動リネームされ、上書きするかは常に dry-run マニフェストであなたが決めます。
6. **バッチは復元可能** — 書き込み前に 1 コマンドで各素材の現在の名前／タグ／注釈をタイムスタンプ付き JSON にスナップショット。バッチが失敗した場合、同伴スクリプトが（`yes` 確認後）そこから復元します。

## インストール

本スキルは [Agent Skills](https://agentskills.io) オープン標準（`SKILL.md` + `scripts/` + `references/`）に準拠しており、互換性のある任意の AI エージェントで動作します。リポジトリを利用中のエージェントのスキルディレクトリにクローンしてください：

| エージェント | ユーザーレベル | プロジェクトレベル |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | — |

ヒント：`~/.agents/skills/` はエージェント横断の共通ディレクトリです——Codex CLI、Gemini CLI、GitHub Copilot、Cursor はネイティブに読み込み、Claude Code もフォールバックとして走査します。1 回のインストールで複数エージェントから発見されます。

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.agents/skills/eagle-untagged-organizer
```

または、フォルダを上記の任意のディレクトリに手動でコピーします。

## 前提条件

- Eagle デスクトップアプリが起動していること。
- `eagle-mcp`（Eagle 公式プラグインに同梱の stdio MCP サーバー）を、利用中のエージェントの MCP 設定に登録します：

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

| エージェント | MCP 設定 |
|---|---|
| Claude Code | `claude mcp add`（ユーザー単位）またはプロジェクトの `.mcp.json` |
| Codex CLI | `~/.codex/config.toml` → `[mcp_servers.eagle-mcp]` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers` |
| GitHub Copilot | `~/.copilot/mcp-config.json`（`"type": "local"`）またはリポジトリルートの `.mcp.json` |
| Cursor | `~/.cursor/mcp.json` |
| WorkBuddy | `~/.workbuddy/mcp.json` → `mcpServers` |

> Codex CLI は TOML 形式です：`~/.codex/config.toml` に `[mcp_servers.eagle-mcp]` を追加し、`command = "node"`、`args = ["<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"]` を設定します。
>
> Gemini CLI は上記と同じ `mcpServers` JSON 構造を `~/.gemini/settings.json` に記述します（または `gemini mcp add -s user eagle-mcp node "<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"` を実行）。
>
> GitHub Copilot：同じサーバーを `"type": "local"` 付きで `~/.copilot/mcp-config.json` に追加します（または `copilot mcp add eagle-mcp -- node "<home>/Library/Application Support/Eagle/Plugins/mcp-server/modules/mcp-proxy.js"` を実行）。

## 使い方

Eagle / `eagle-mcp` / 未タグ付け素材に一括整理の意図を添えて言及すると、スキルがワークフローを駆動します。完全なワークフロー（事前チェック → 分析 → dry-run プレビュー → 承認ゲート → 一括更新 → 検証）は [`SKILL.md`](../SKILL.md) を参照。

> 逆に、乱雑なタグ語彙を整理（タグの統合 / リネーム / 廃止）したい場合は、[`eagle-tag-governance`](https://github.com/ChosenXu/eagle-tag-governance) をご利用ください。両スキルは独立しています。

## 構成

```
SKILL.md                     # スキル定義とワークフロー
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

## ライセンス

[MIT](../LICENSE)
