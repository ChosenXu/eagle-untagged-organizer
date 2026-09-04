# Changelog / 更新日志

All notable changes to this project are documented in this file.
本文件记录本项目所有重要变更。

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).
格式参考 Keep a Changelog，版本号遵循语义化版本（SemVer）。

---

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
