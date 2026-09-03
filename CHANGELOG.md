# Changelog / 更新日志

All notable changes to this project are documented in this file.
本文件记录本项目所有重要变更。

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).
格式参考 Keep a Changelog，版本号遵循语义化版本（SemVer）。

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
