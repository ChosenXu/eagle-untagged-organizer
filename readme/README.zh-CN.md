# Eagle Untagged Organizer

[English](../README.md) | 简体中文 | [繁体中文](README.zh-Hant.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md)

一个兼容 [Agent Skills](https://agentskills.io) 开放标准的 skill，通过 `eagle-mcp` MCP 服务器批量整理 [Eagle](https://eagle.cool/) 中**未打标签**的设计素材——一次性完成 UI/UX 参考与平面设计作品的命名、标注和打标签。适用于 Claude Code、Codex CLI、Gemini CLI、GitHub Copilot、Cursor 与 WorkBuddy。

## 它能做什么

针对每一张选中的未打标签素材，它会产出三项结果，并通过一次 `item_update` 调用写回 Eagle：

1. **命名** —— 简洁的标题式名称（便于在 Eagle 网格中检索）；若素材已有妥当名称，则保留或建议覆盖，而非盲目重命名。
2. **标注** —— 结构化的五段式区块（设计类型 / 结构 / 视觉 / 用途 / 参考价值）
3. **标签** —— 从三维受控词表（设计领域 / 视觉风格 / 技法）中逐字原样选取

输出语言可配置：简体中文、繁體中文（港式）、English、日本語、한국어、Русский、Español、Deutsch。若用户指令所用语言属于受支持语言，则继承该语言；否则回退到英语。

## 核心优势

1. **真正"看懂"素材再动手** —— 不是靠文件名瞎猜，而是先做多模态能力预检，逐张读图理解画面里的对象、配色、版式，再产出命名和标注——质量有保证。
2. **结构化、可复用、不跑偏** —— 命名是短标题而非分析长句；标注是固定五段式；标签是三维受控词表、逐字原样选取、禁止自造词。整理出来的库风格统一，标签体系不会越滚越乱。
3. **安全第一，先预览后写入** —— 所有修改都先出 dry-run 变更清单给你审阅，确认无误才批量落库；改完还会逐条回读校验，不会悄无声息地乱改你的库。
4. **大量素材也能扛** —— 100+ 的大批量场景有内置 Python 脚本走 stdio 批量写入，不用把巨量 payload 糊进对话里。
5. **尊重你已有的命名** —— 已有妥当名称的素材默认保留原名、只补注释与标签；只有无意义/随机名才自动重命名，且是否覆盖始终由你在 dry-run 清单中决定。
6. **批次可回滚** —— 写入前一条命令把本批每个素材的当前名称 / 标签 / 注释导出为带时间戳的 JSON 快照；若批次出错，配套脚本读取快照还原（需输入 `yes` 确认）。

## 安装

本 skill 遵循 [Agent Skills](https://agentskills.io) 开放标准（`SKILL.md` + `scripts/` + `references/`），可在任意兼容的 AI Agent 中使用。将本仓库克隆到你所用 Agent 的 skills 目录：

| 平台 | 用户级目录 | 项目级目录 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| GitHub Copilot CLI | `~/.copilot/skills/` | `.github/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | — |

提示：`~/.agents/skills/` 是跨平台通用目录——Codex CLI、Gemini CLI、GitHub Copilot、Cursor 均原生读取，Claude Code 也会作为兜底路径扫描。一处安装，多平台发现。

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.agents/skills/eagle-untagged-organizer
```

或者手动把整个文件夹拷贝到上述任意目录下。

## 前置条件

- Eagle 桌面端必须正在运行。
- `eagle-mcp`（Eagle 官方插件内置的 MCP 服务器）需注册到你所用 Agent 的 MCP 配置中：

| 平台 | MCP 配置 |
|---|---|
| Claude Code | `claude mcp add` 或项目 `.mcp.json` |
| Codex CLI | `~/.codex/config.toml` → `[mcp_servers.eagle-mcp]` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers` |
| GitHub Copilot | `.mcp.json`（仓库根目录） |
| Cursor | `~/.cursor/mcp.json` |
| WorkBuddy | `~/.workbuddy/mcp.json` → `mcpServers` |

## 使用方法

当提到 Eagle / `eagle-mcp` / 未打标签素材并带有批量整理意图时，本 skill 会自动驱动工作流。完整工作流（预检 → 分析 → dry-run 预览 → 授权门槛 → 批量更新 → 校验）见 [`SKILL.md`](../SKILL.md)。

> 需要反过来清理混乱的标签词表（合并 / 重命名 / 退役标签）？请使用 [`eagle-tag-governance`](https://github.com/ChosenXu/eagle-tag-governance)。两个技能相互独立。

## 目录结构

```
SKILL.md                     # skill 定义与工作流
references/
  vocabulary.md              # 简体中文标签词表（规范版）
  vocabulary-zh-Hant.md      # 繁體中文（港式）标签词表
  vocabulary-en.md           # 英文标签词表
  vocabulary-ja.md           # 日本語标签词表
  vocabulary-ko.md           # 한국어标签词表
  vocabulary-ru.md           # Русский标签词表
  vocabulary-es.md           # Español 标签词表
  vocabulary-de.md           # Deutsch 标签词表
  templates.md               # 命名公式与五段式标注模板
  gotchas.md                 # 常见坑与调用形态注意事项
scripts/
  apply_eagle_batch.py       # 通过 MCP stdio 代理批量应用更新
  build_dryrun.py            # 生成可审阅的 dry-run 变更清单
  snapshot_eagle_batch.py    # 只读：导出带时间戳的写入前快照（id+名称+标签+标注）
  restore_eagle_snapshot.py  # 从快照还原（item_update 写回，写入前需输入 yes 确认）
```

## 许可证

[MIT](../LICENSE)
