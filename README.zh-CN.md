# Eagle Untagged Organizer

[English](README.md) | 中文

一个 [WorkBuddy](https://www.workbuddy.cn/) skill，通过 `eagle-mcp` 连接器批量整理 [Eagle](https://eagle.cool/) 中**未打标签**的设计素材——一次性完成 UI/UX 参考与平面设计作品的命名、标注和打标签。

## 它能做什么

针对每一张选中的未打标签素材，它会产出三项结果，并通过一次 `item_update` 调用写回 Eagle：

1. **命名** —— 简洁的标题式名称（便于在 Eagle 网格中检索）
2. **标注** —— 结构化的五段式区块（设计类型 / 结构 / 视觉 / 用途 / 参考价值）
3. **标签** —— 从三维受控词表（设计领域 / 视觉风格 / 技法）中逐字原样选取

输出语言可配置：简体中文（默认）、繁體中文（港式）、English。

## 核心优势

1. **真正"看懂"素材再动手** —— 不是靠文件名瞎猜，而是先做多模态能力预检，逐张读图理解画面里的对象、配色、版式，再产出命名和标注——质量有保证。
2. **结构化、可复用、不跑偏** —— 命名是短标题而非分析长句；标注是固定五段式；标签是三维受控词表、逐字原样选取、禁止自造词。整理出来的库风格统一，标签体系不会越滚越乱。
3. **安全第一，先预览后写入** —— 所有修改都先出 dry-run 变更清单给你审阅，确认无误才批量落库；改完还会逐条回读校验，不会悄无声息地乱改你的库。
4. **大量素材也能扛** —— 100+ 的大批量场景有内置 Python 脚本走 stdio 批量写入，不用把巨量 payload 糊进对话里。

## 安装

将本仓库克隆到你的 WorkBuddy skills 目录：

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.workbuddy/skills/eagle-untagged-organizer
```

或者手动把整个文件夹拷贝到 `~/.workbuddy/skills/` 下。

## 前置条件

- Eagle 桌面端必须正在运行。
- `eagle-mcp` 需在 `~/.workbuddy/mcp.json` 中配置，并在连接器面板中信任。

## 使用方法

当提到 Eagle / `eagle-mcp` / 未打标签素材并带有批量整理意图时，本 skill 会自动驱动工作流。完整工作流（预检 → 分析 → dry-run 预览 → 授权门槛 → 批量更新 → 校验）见 [`SKILL.md`](SKILL.md)。

## 目录结构

```
SKILL.md                     # skill 定义与工作流
references/
  vocabulary.md              # 简体中文标签词表（规范版）
  vocabulary-zh-Hant.md      # 繁體中文（港式）标签词表
  vocabulary-en.md           # 英文标签词表
  templates.md               # 命名公式与五段式标注模板
  gotchas.md                 # 常见坑与调用形态注意事项
scripts/
  apply_eagle_batch.py       # 通过 MCP stdio 代理批量应用更新
  build_dryrun.py            # 生成可审阅的 dry-run 变更清单
```

## 许可证

[MIT](LICENSE)
