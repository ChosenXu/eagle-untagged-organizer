# Eagle Untagged Organizer

[English](../README.md) | [简体中文](README.zh-CN.md) | [繁体中文](README.zh-Hant.md) | 日本語 | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md)

[WorkBuddy](https://www.workbuddy.cn/) スキル。`eagle-mcp` コネクタ経由で [Eagle](https://eagle.cool/) 内の**未タグ付け**デザイン素材を一括整理します。UI/UX リファレンスやグラフィックデザイン作品に対し、リネーム・注釈・タグ付けを一度に実行します。

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

リポジトリを WorkBuddy のスキルディレクトリにクローン：

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.workbuddy/skills/eagle-untagged-organizer
```

またはフォルダを `~/.workbuddy/skills/` に手動でコピー。

## 前提条件

- Eagle デスクトップアプリが起動していること。
- `eagle-mcp` が `~/.workbuddy/mcp.json` に設定され、コネクタパネルで信頼されていること。

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
