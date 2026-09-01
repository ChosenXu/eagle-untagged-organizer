# Naming & Annotation Templates

## Naming Guidelines (title formula)

Format: `[视觉风格/调性][设计类型]搭配[最显著视觉特征]`

- Must read like a short title, **not** an analysis sentence. Avoid `这是一个…` / `图中展示了…`.
- Keep under ~20 characters when possible, scannable in the Eagle grid.
- Names are free text in the target language (see "Output Language" in SKILL.md) and are **independent** of the tag vocabulary — do not force names to match tag casing.

Examples:
- `极简品牌识别指南搭配网格系统` (graphic / branding)
- `复古活动海报搭配粗衬线字体` (graphic / poster)
- `等距图标组合柔和色调` (graphic / icon set)
- `暗色金融仪表盘搭配投资组合图表` (UI / dashboard)

## Annotation Template (library-management perspective)

Eagle's `annotation` is a single text field. Produce the annotation as a **labeled block with exactly five fields, in this exact order**. These five fields are mandatory — do not add, remove, or rename them. Use the field labels for the target language (see "Output Language" in SKILL.md).

**Field order (exact, in all three languages):**

| # | 简体中文 | 繁體中文（港式） | English | Meaning |
|---|---|---|---|---|
| 1 | `设计类型` | `設計類型` | `Type` | the design domain/type |
| 2 | `结构` | `結構` | `Structure` | layout/composition & hierarchy |
| 3 | `视觉` | `視覺` | `Visual` | style, color, typography |
| 4 | `用途` | `用途` | `Use` | what it serves as a reference for |
| 5 | `参考价值` | `參考價值` | `Reference Value` | the standout merit worth collecting |

**Formatting rules (hard):**

- Each field goes on its **own line**, separated by a newline. **Never** join multiple fields into one paragraph or one continuous line.
- Use the exact field label followed by `：` (full-width colon), then the value.
- No blank lines between fields; no bullet markers; no extra labels.

**Template (copy this structure verbatim, using the target language's labels):**

```
设计类型：<值>
结构：<值>
视觉：<值>
用途：<值>
参考价值：<值>
```

**Example (poster) — 简体中文:**

```
设计类型：活动海报
结构：居中对称构图，标题统领视觉，日期与地点下沉为次级信息
视觉：暖橙/深棕双色，主标题用大字号粗衬线，辅助信息用无衬线
用途：适合音乐、展览等线下活动的宣传主视觉参考
参考价值：示范复古双色印刷的克制表达与强标题张力
```

**Example (poster) — 繁體中文（港式）:**

```
設計類型：活動海報
結構：居中對稱構圖，標題統領視覺，日期與地點下沉為次級資訊
視覺：暖橙／深棕雙色，主標題用大號字粗襯線，輔助資訊用無襯線
用途：適合音樂、展覽等線下活動的宣傳主視覺參考
參考價值：示範復古雙色印刷的克制表達與強標題張力
```

**Example (poster) — English:**

```
Type: Event poster
Structure: Centered symmetrical layout; the headline leads the visual, with date and venue demoted to secondary information
Visual: Warm orange / deep brown duotone; large bold serif for the headline, sans-serif for supporting text
Use: A primary-visual reference for offline event promotion (music, exhibitions)
Reference Value: Demonstrates restrained duotone printing with strong headline tension
```

## Tagging Guidelines

- Tag across the three dimensions (设计领域 / 视觉风格 / 主要技法) using the vocabulary file matching the target language (see "Output Language" in SKILL.md).
- Select tags **verbatim** from that vocabulary — do not invent new terms, translate, or create synonyms.
- Keep only the most search-valuable tags — typically 2–4 from 设计领域, 1–2 from 视觉风格, 1–3 from 主要技法.
- Tags and names/annotations must share the **same** target language. Do not mix languages across the three outputs for a single asset.
