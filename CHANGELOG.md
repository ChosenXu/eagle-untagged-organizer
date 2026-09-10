# Changelog / 更新日志

All notable changes to this project are documented in this file.
本文件记录本项目所有重要变更。

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).
格式参考 Keep a Changelog，版本号遵循语义化版本（SemVer）。

---

## [2.5.2] - 2026-09-10

### Changed / 变更
- README restructure: all non-English READMEs moved into a new `readme/` folder at the repository root; the English `README.md` stays in the root. Relative links inside every README (language switcher, `SKILL.md`, `LICENSE`) were updated to match the new locations.
  README 结构重组：全部非英语 README 移入仓库根目录新建的 `readme/` 文件夹，英文版 `README.md` 保留在根目录；各 README 内的相对链接（语言切换导航、`SKILL.md`、`LICENSE`）已同步修正至新位置。

### Fixed / 修复
- Language switcher: in the ja/ko/ru/es/de READMEs the current language itself is no longer hyperlinked (English, 简体中文, and 繁體中文 already behaved this way). The current language is now plain text in all 8 READMEs.
  语言导航：日/韩/俄/西/德 5 份 README 不再给当前语言自身加超链接（英文、简体中文、繁体中文此前已是纯文本）。现在 8 份 README 中当前语言均为纯文本。

### Notes / 说明
- Documentation-only release (patch). The organizer workflow, the three-dimension tag vocabularies, and all scripts are unchanged.
  纯文档发布（补丁级）。organizer 工作流、三维受控标签词表与全部脚本均无变化。

## [2.5.1] - 2026-09-07

### Added / 新增
- Reverse cross-link to the companion `eagle-tag-governance` skill: all 8 READMEs now carry a callout that points users with an already-tangled tag vocabulary to that skill, and states the two skills are independent. This completes the bidirectional link — `eagle-tag-governance` already linked here from its v1.0.0 README.
  新增指向配套技能 `eagle-tag-governance` 的反向互链：8 份 README 现均含一条提示框，将已有混乱标签词表的用户引导至该技能，并说明两者相互独立。至此双向互链完成——`eagle-tag-governance` 自 v1.0.0 起即已反向指向本技能。

### Notes / 说明
- Documentation-only release (patch). The organizer workflow, the three-dimension tag vocabularies, and all scripts are unchanged.
  纯文档发布（补丁级）。organizer 工作流、三维受控标签词表与全部脚本均无变化。

---

## [2.5.0] - 2026-09-05

### Added / 新增

- Multilingual output expansion: the organizer now supports 日本語, 한국어, Русский, Español, and Deutsch as output languages, in addition to the existing 简体中文 / 繁體中文（港式）/ English — aligning the skill with Eagle's eight official UI languages.
  多语言输出扩展：在原有 简体中文 / 繁體中文（港式）/ English 基础上，新增 日本語 / 한국어 / Русский / Español / Deutsch 五种输出语言，与 Eagle 官方 8 种界面语言对齐。
- Five new controlled tag vocabularies: `references/vocabulary-ja.md`, `vocabulary-ko.md`, `vocabulary-ru.md`, `vocabulary-es.md`, `vocabulary-de.md` — each mirrors the canonical Chinese taxonomy term-for-term using industry-standard terms.
  新增 5 份受控标签词表（ja/ko/ru/es/de），逐词镜像中文规范词表，采用行业通用术语。
- Five new five-field annotation label sets and five routing rows in the "Output Language" section, so names, annotations, and tags follow the target language across all eight languages.
  在「Output Language」节新增 5 套五段式标注标签与 5 行路由，使命名 / 标注 / 标签在全部 8 种语言下均跟随目标语言。
- Auto-inherit output language: when the user's instruction is written in a supported language, that language is used as the output language; otherwise (unsupported or ambiguous) it falls back to **English** instead of Simplified Chinese.
  产出语言自动继承：用户指令所用语言为受支持语言时，直接继承为产出语言；否则（不支持或无法判断）回退到**英语**而非简体中文。
- `description` now carries trigger phrases in Japanese / Korean / Russian / Spanish / German, so the skill also fires when users write their request in those languages.
  `description` 新增日 / 韩 / 俄 / 西 / 德 触发短语，用户用这些语言下指令时也能唤起技能。
- Five new README translations: `README.ja.md`, `README.ko.md`, `README.ru.md`, `README.es.md`, `README.de.md`; all eight READMEs now cross-link through a full language switcher.
  新增 5 份 README 译文；8 份 README 均通过完整语言切换器互链。
- `references/templates.md`: two more five-field annotation examples — 日本語 and Русский — so non-Latin output languages have a copyable reference instead of depending solely on the SKILL.md routing table.
  `references/templates.md`：新增 日本語 / Русский 两组五段式标注示例，非拉丁语系产出可直接参照，无需只依赖 SKILL.md 路由表。

### Changed / 变更
- Terminology pass on the five v2.5.0 vocabularies (17 tag replacements across 5 files, counts and dimension split A/B/C = 14/13/12 unchanged, no duplicates introduced). Terminology choices follow the industry-standard term in each language rather than a literal rendering of the English pivot.
  对 v2.5.0 新增的 5 份词表做术语校准（5 个文件共 17 处替换；词数与维度分布 A/B/C = 14/13/12 不变，未引入重复标签）。选词依据各语言业界惯用说法，而非英文 pivot 的直译。
  - `vocabulary-ru.md`: `Сеточная система`→`Модульная сетка` (standard RU term for grid system), `Карточный макет`→`Карточная раскладка` (the former reads as "card layout file"), `Швейцарский`→`Швейцарский стиль` (bare adjective; the canonical ZH term is 瑞士风, not 瑞士).
    `vocabulary-ru.md`：Сеточная система→Модульная сетка（grid system 的俄文标准说法）、Карточный макет→Карточная раскладка（前者易读成"卡片版式文件"）、Швейцарский→Швейцарский стиль（裸形容词；中文规范词是「瑞士风」而非「瑞士」）。
  - `vocabulary-de.md`: `Verlauf`→`Farbverlauf` (Verlauf alone means "course/progression"), `Schweizer`→`Schweizer Stil` (Schweizer alone means "Swiss person").
    `vocabulary-de.md`：Verlauf→Farbverlauf（Verlauf 单独意为"过程／走向"）、Schweizer→Schweizer Stil（Schweizer 单独意为"瑞士人"）。
  - `vocabulary-ko.md`: `진행 막대`→`진행 표시줄` (standard KO UI term), `스위스`→`스위스 스타일` (bare country name collides with photos of Switzerland), `디스플레이 타입`→`디스플레이 서체` (서체 is the KO typography term), and localized the two untranslated platform tags `Web UI`→`웹 UI`, `Mobile UI`→`모바일 UI`.
    `vocabulary-ko.md`：진행 막대→진행 표시줄（韩文 UI 标准术语）、스위스→스위스 스타일（裸国名会与瑞士风景照撞车）、디스플레이 타입→디스플레이 서체（韩文排版术语为 서체），并本地化两条漏译的平台标签 Web UI→웹 UI、Mobile UI→모바일 UI。
  - `vocabulary-ja.md`: `スイス`→`スイススタイル`, `ディスプレイタイプ`→`ディスプレイ書体` (書体 is the JA typography term), and localized `Web UI`→`ウェブUI`, `Mobile UI`→`モバイルUI` — matching the file's existing convention of katakana-izing loanwords (グラスモーフィズム, デュオトーン).
    `vocabulary-ja.md`：スイス→スイススタイル、ディスプレイタイプ→ディスプレイ書体（日文排版术语为 書体），并本地化 Web UI→ウェブUI、Mobile UI→モバイルUI，与本文件既有的片假名化外来语惯例一致（グラスモーフィズム、デュオトーン）。
  - `vocabulary-es.md`: `Sistema de rejilla`→`Sistema de retícula` (retícula is the graphic-design term; rejilla belongs to CSS Grid docs), `Suizo`→`Estilo suizo`, `Tipo display`→`Tipografía display`.
    `vocabulary-es.md`：Sistema de rejilla→Sistema de retícula（平面设计标准术语为 retícula，rejilla 主要见于 CSS Grid 文档）、Suizo→Estilo suizo、Tipo display→Tipografía display。
  - Deliberately kept: `UI` is retained as an initialism in every language (matching the canonical ZH `网页UI` / `移动UI`), as are established loanwords (`Dashboard`, `Glassmorphism`, `Memphis`, `Branding`, `Packaging`). Tag vocabularies are search keys, not prose — forcing a translation there hurts retrievability.
    刻意保留：`UI` 作为首字母缩写在所有语言中均不翻译（与中文规范词「网页UI／移动UI」一致），已成业界通用的借词（Dashboard / Glassmorphism / Memphis / Branding / Packaging）同样保留。词表是检索键而非散文，硬译会损害可检索性。

### Fixed / 修正
- `references/templates.md`: corrected the outdated "in all three languages" wording to "all eight languages", and added a pointer to the field-label table in `SKILL.md`.
  `references/templates.md`：将过时的「in all three languages」修正为 eight languages，并补充指向 SKILL.md 字段标签表的说明。
- `scripts/apply_eagle_batch.py`: replaced the literal `/Users/<name>/...` example path inside a comment with a `<home>/Library/...` placeholder, so the "don't hardcode machine-specific paths" reminder no longer trips `validate`'s absolute-path check.
  `scripts/apply_eagle_batch.py`：注释中的示例路径由 `/Users/<name>/...` 改为 `<home>/Library/...` 占位写法，提醒语义保留，且不再触发 validate 的绝对路径误报。
- Multilingual review pass / 多语言校对（无母语者，机器自查 + 外部核验）：
  - `README.ja.md`: replaced two Chinese terms that had leaked into the Japanese text — `动作前`→`実行前`, `多模态`→`マルチモーダル`; aligned the five-field label list with `SKILL.md` (`設計タイプ`→`タイプ`).
    `README.ja.md`：修掉混入日文的两处中文词（动作前→実行前、多模态→マルチモーダル），并将五段式字段标签与 SKILL.md 对齐（設計タイプ→タイプ）。
  - `README.ko.md`: `행동하기 전`→`실행 전`, `설계 유형`→`유형` (align with `SKILL.md`), replaced the nonsensical literal rendering `궤도에 올림` (of "on track") with `일관되게 유지됨`, and translated the leftover English `companion 스크립트`→`함께 제공되는 스크립트`.
    `README.ko.md`：행동하기 전→실행 전、설계 유형→유형（与 SKILL.md 对齐）、误译「궤도에 올림」（"on track" 直译）→일관되게 유지됨，并补译残留英文 companion 스크립트。
  - `README.de.md`: replaced the non-German pseudo-verb `snapshotet` with `sichert ... als Snapshot`.
    `README.de.md`：非德语伪动词 snapshotet 改为 sichert ... als Snapshot。
  - `SKILL.md`: the colon rule now states `：` for CJK vs `: ` for non-CJK, instead of the outdated "(Chinese) or (English)".
    `SKILL.md`：冒号规则由过时的「(Chinese) 或 (English)」改为按 CJK / 非 CJK 区分。
  - `references/templates.md`: polished the 日本語 example (視覚を牽引→視線を引きつけ, added missing predicate 配置されている, セリフ→セリフ体) and the Русский example (место→место проведения, reordered the "без засечек" clause, дуотон-печать→печать в технике дуотон).
    `references/templates.md`：润色日文示例（补谓语、セリフ体）与俄文示例（место проведения、调整语序、改写生硬复合词）。

### Notes / 说明
- Backward compatible: existing 简体中文 / 繁體中文（港式）/ English behavior is unchanged. The prior "default 简体中文" is now "inherit invocation language, fall back to English".
  向后兼容：原有三语行为不变；原「默认简体中文」改为「继承唤起语言，回退英语」。
- Translations are model-generated drafts and have been through one machine review pass — 15 objective errors and 17 terminology choices corrected (see Fixed / Changed above). No native speaker was involved, so **long-sentence naturalness in Russian, Korean, and Japanese remains unverified**; a native-speaker read-through is still recommended before broad publication.
  翻译为模型生成初稿，并已完成一轮机器校对（见上文 Fixed / Changed）：修正 15 处客观错误、17 处术语选择。全程无母语者参与，因此**俄 / 韩 / 日 长句的自然度仍未经验证**，公开发布前仍建议请母语者通读一遍。

---

## [2.4.0] - 2026-09-04

### Added / 新增
- Pre-write rollback snapshot: before the Phase 4 write, `scripts/snapshot_eagle_batch.py --manifest dryrun_manifest.json` exports a timestamped, read-only JSON of every batch asset's current `name` / `tags` / `annotation` (via `item_get` fullDetails) to `~/.workbuddy/skill-backups/eagle-untagged-organizer-rollbacks/`. It is read-only and never writes to Eagle; a failure only warns.
  写入前回滚快照：在 Phase 4 写入前，`snapshot_eagle_batch.py --manifest dryrun_manifest.json` 将本批每个素材当前的 `name` / `tags` / `annotation`（经 `item_get` fullDetails）导出为带时间戳的只读 JSON，存放于项目外的回滚目录。该步骤只读、不写 Eagle，失败仅告警。
- One-click rollback: `scripts/restore_eagle_snapshot.py --snapshot <file>` reads a snapshot and restores each item's original name / tags / annotation via `item_update`. It prints a summary and asks you to type `yes` before overwriting, so a bad batch is recoverable.
  一键回滚：`restore_eagle_snapshot.py --snapshot <file>` 读取快照，经 `item_update` 还原每个素材的原文名 / 原标签 / 原注释。执行前打印摘要并要求输入 `yes` 确认，确保出错批次可恢复。

## [2.3.0] - 2026-09-04

### Added / 新增
- Respect existing naming: the organizer now judges each asset's current name and either keeps it, proposes an overwrite (user chooses), or auto-renames only meaningless/random names. A `nameAction` (`keep` | `rename`) + `proposedName` field is added to the dry-run manifest so the user keeps final control.
  尊重已有命名：整理器现在会判断每个素材的当前名称，保留、建议覆盖（由用户选择）或仅对无意义/随机名称自动重命名。dry-run manifest 新增 `nameAction`（`keep` | `rename`）与 `proposedName` 字段，最终决定权留在用户手中。
- Three naming modes (A mixed / B trust-existing / C force-rename) selected once per run, so a batch of already-good names skips generation entirely.
  三种命名模式（A 混合 / B 信任原名 / C 强制重命名）每次运行选一次，已妥善命名的整批可完全跳过命名生成。
- `scripts/apply_eagle_batch.py` honors `nameAction`: it sends `name` only when `nameAction=="rename"`, otherwise omits it so Eagle preserves the original name (verified empirically). `nameAction` / `proposedName` / `oldName` are stripped before send.
  `apply_eagle_batch.py` 遵循 `nameAction`：仅当 `rename` 时发送 `name`，否则省略以保留原名（已实测验证）。发送前剔除 `nameAction` / `proposedName` / `oldName`。
- `scripts/build_dryrun.py` emits `nameAction` + `proposedName` alongside `oldName`.
  `build_dryrun.py` 在 `oldName` 之外输出 `nameAction` 与 `proposedName`。

### Notes / 说明
- Backward compatible: manifests without `nameAction` still rename as before (default `rename`); the organizer workflow (pre-flight → analyze → dry-run → authorize → batch update → verify) is unchanged in shape.
  向后兼容：无 `nameAction` 的 manifest 仍按原行为重命名（默认 `rename`）；organizer 工作流形态不变。

---

## [2.2.0] - 2026-09-03

### Changed / 变更
- Scope the skill down to a single **Untagged organizer** workflow (rename, annotate, tag). Tag governance is split out into a separate future skill, `eagle-tag-governance`.
  将技能职责收窄为单一的「Untagged organizer」工作流（命名 / 标注 / 打标签）。标签治理（合并 / 规范化 / 重命名）拆分到未来的独立技能 `eagle-tag-governance`。
- Remove all tag-governance references from `SKILL.md` and both READMEs (`README.md`, `README.zh-CN.md`); renumber the Highlights list.
  从 `SKILL.md` 与两份 README 中移除全部标签治理相关说明，并重排 Highlights 编号。
- Bump `version` 2.1.0 → 2.2.0 in `SKILL.md` frontmatter.
  在 `SKILL.md` frontmatter 中将版本号由 2.1.0 提升至 2.2.0。

### Removed / 移除
- Delete `references/tag-governance.md` (the merge/normalize/rename-tags workflow).
  删除 `references/tag-governance.md`（合并 / 规范化 / 重命名标签的工作流文件）。

### Notes / 说明
- No behavior change to the organizer workflow itself (pre-flight → analyze → dry-run → authorize → batch update → verify).
  organizer 工作流本身行为不变（预检 → 分析 → dry-run → 授权 → 批量更新 → 校验）。

---

## [2.1.0] - 2026-09-02

### Added / 新增
- Initial published version of `eagle-untagged-organizer`.
  首个公开发布版本。
- Batch-organize **untagged** Eagle assets via the `eagle-mcp` connector: rename, annotate, and tag UI/UX references and graphic-design works in one pass.
  通过 `eagle-mcp` 连接器批量整理 Eagle 中未打标签的素材：一次性完成 UI/UX 参考与平面设计作品的命名、标注、打标签。
- Two workflows: the **Untagged organizer** (default) and **Tag governance** (merge/normalize/rename an overgrown tag vocabulary).
  两个工作流：Untagged organizer（默认）与 Tag governance（合并 / 规范化已膨胀的标签词表）。
- Controlled three-dimension tag vocabulary (`references/vocabulary*.md`) and a fixed five-field annotation template (`references/templates.md`) in zh-CN / zh-HK / en.
  三维受控标签词表与固定五段式标注模板，支持简体中文 / 港式繁体 / 英文。
- Safety-first flow: multimodal pre-flight check, dry-run manifest preview, and an explicit authorization gate before any Eagle write; re-read verification afterward.
  安全优先流程：多模态预检、dry-run 变更清单预览、写入前显式授权门槛、写入后回读校验。
- Bundled Python helpers for large batches: `scripts/apply_eagle_batch.py` (bulk stdio writes) and `scripts/build_dryrun.py` (reviewable manifest).
  内置 Python 辅助脚本：`apply_eagle_batch.py`（大批量 stdio 写入）与 `build_dryrun.py`（生成可审阅 manifest）。
- Bilingual documentation: `README.md` (English) and `README.zh-CN.md` (简体中文) with a language switcher.
  双语文档：英文 `README.md` 与简体中文 `README.zh-CN.md`，带语言切换。
