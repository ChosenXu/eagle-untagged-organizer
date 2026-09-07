# Eagle Untagged Organizer

[English](README.md) | [簡體中文](README.zh-CN.md) | 繁體中文 | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md)

一個 [WorkBuddy](https://www.workbuddy.cn/) skill，透過 `eagle-mcp` 連接器批量整理 [Eagle](https://eagle.cool/) 中**未打標籤**的設計素材——一次性完成 UI/UX 參考與平面設計作品的命名、標註和打標籤。

## 它能做什麼

針對每一張選中的未打標籤素材，它會產出三項結果，並透過一次 `item_update` 呼叫寫回 Eagle：

1. **命名** —— 簡潔的標題式名稱（便於在 Eagle 網格中檢索）；若素材已有妥當名稱，則保留或建議覆蓋，而非盲目重新命名。
2. **標註** —— 結構化的五段式區塊（設計類型 / 結構 / 視覺 / 用途 / 參考價值）
3. **標籤** —— 從三維受控詞表（設計領域 / 視覺風格 / 技法）中逐字原樣選取

輸出語言可配置：簡體中文、繁體中文（港式）、English、日本語、한국어、Русский、Español、Deutsch。若使用者指令所用語言屬於受支援語言，則繼承該語言；否則回退到英語。

## 核心優勢

1. **真正「看懂」素材再動手** —— 不是靠檔名瞎猜，而是先做多模態能力預檢，逐張讀圖理解畫面裡的物件、配色、版式，再產出命名和標註——品質有保證。
2. **結構化、可重用、不跑偏** —— 命名是短標題而非分析長句；標註是固定五段式；標籤是三維受控詞表、逐字原樣選取、禁止自造詞。整理出來的庫風格統一，標籤體系不會越滾越亂。
3. **安全第一，先預覽後寫入** —— 所有修改都先出 dry-run 變更清單給你審閱，確認無誤才批量落庫；改完還會逐條回讀校驗，不會悄無聲息地亂改你的庫。
4. **大量素材也能扛** —— 100+ 的大批量場景有內建 Python 腳本走 stdio 批量寫入，不用把巨量 payload 糊進對話裡。
5. **尊重你已有的命名** —— 已有妥當名稱的素材預設保留原名、只補註釋與標籤；只有無意義/隨機名才自動重新命名，且是否覆蓋始終由你在 dry-run 清單中決定。
6. **批次可回滾** —— 寫入前一條指令把本批每個素材的目前名稱 / 標籤 / 註釋匯出為帶時間戳的 JSON 快照；若批次出錯，配套腳本讀取快照還原（需輸入 `yes` 確認）。

## 安裝

將本倉庫克隆到你的 WorkBuddy skills 目錄：

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.workbuddy/skills/eagle-untagged-organizer
```

或者手動把整個資料夾拷貝到 `~/.workbuddy/skills/` 下。

## 前置條件

- Eagle 桌面端必須正在運行。
- `eagle-mcp` 需在 `~/.workbuddy/mcp.json` 中配置，並在連接器面板中信任。

## 使用方法

當提到 Eagle / `eagle-mcp` / 未打標籤素材並帶有批量整理意圖時，本 skill 會自動驅動工作流。完整工作流（預檢 → 分析 → dry-run 預覽 → 授權門檻 → 批量更新 → 校驗）見 [`SKILL.md`](SKILL.md)。

> 需要反過來清理混亂的標籤詞表（合併 / 重新命名 / 退役標籤）？請使用 [`eagle-tag-governance`](https://github.com/ChosenXu/eagle-tag-governance)。兩個技能相互獨立。

## 目錄結構

```
SKILL.md                     # skill 定義與工作流
references/
  vocabulary.md              # 簡體中文標籤詞表（規範版）
  vocabulary-zh-Hant.md      # 繁體中文（港式）標籤詞表
  vocabulary-en.md           # 英文標籤詞表
  vocabulary-ja.md           # 日本語標籤詞表
  vocabulary-ko.md           # 한국어標籤詞表
  vocabulary-ru.md           # Русский標籤詞表
  vocabulary-es.md           # Español 標籤詞表
  vocabulary-de.md           # Deutsch 標籤詞表
  templates.md               # 命名公式與五段式標註模板
  gotchas.md                 # 常見坑與呼叫形態注意事項
scripts/
  apply_eagle_batch.py       # 透過 MCP stdio 代理批量套用更新
  build_dryrun.py            # 生成可審閱的 dry-run 變更清單
  snapshot_eagle_batch.py    # 唯讀：匯出帶時間戳的寫入前快照（id+名稱+標籤+標註）
  restore_eagle_snapshot.py  # 從快照還原（item_update 寫回，寫入前需輸入 yes 確認）
```

## 授權

[MIT](LICENSE)
