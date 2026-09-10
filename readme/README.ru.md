# Eagle Untagged Organizer

[English](../README.md) | [简体中文](README.zh-CN.md) | [繁体中文](README.zh-Hant.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | Русский | [Español](README.es.md) | [Deutsch](README.de.md)

Навык, совместимый с открытым стандартом [Agent Skills](https://agentskills.io), который пакетно упорядочивает **не размеченные тегами** дизайн-ассеты в [Eagle](https://eagle.cool/) через MCP-сервер `eagle-mcp` — переименование, аннотирование и тегирование UI/UX-референсов и графических работ за один проход. Работает в Claude Code, Codex CLI, Gemini CLI, GitHub Copilot, Cursor и WorkBuddy.

## Что он делает

Для каждого выбранного неразмеченного ассета генерирует три вывода, записываемые в Eagle одним вызовом `item_update`:

1. **Имя** — лаконичное название в виде заголовка (ищется в сетке Eagle); если у ассета уже есть хорошее имя, оно сохраняется или предлагается к перезаписи, а не слепо переименовывается.
2. **Аннотация** — структурированный блок из пяти полей (Тип / Структура / Визуал / Назначение / Справочная ценность)
3. **Теги** — выбираются дословно из контролируемой трёхмерной лексики (сфера дизайна / визуальный стиль / техника)

Язык вывода настраивается (简体中文 / 繁體中文（港式）/ English / 日本語 / 한국어 / Русский / Español / Deutsch). Если язык инструкции пользователя поддерживается — наследуется этот язык, иначе используется английский запасной вариант.

## Основные преимущества

1. **Действительно «читает» каждый ассет перед действием** — никогда не угадывает по именам файлов. Сначала запускает мультимодальную предварительную проверку, читая каждое изображение, чтобы понять объекты, цвета и компоновку, и лишь затем создаёт имена и аннотации — качество гарантировано.
2. **Структурировано, пригодно для повторного использования и последовательно** — имена — это короткие заголовки, а не аналитические предложения; аннотации следуют фиксированному шаблону из пяти полей; теги берутся из контролируемой трёхмерной лексики дословно (без выдуманных терминов). Результат — согласованная библиотека, чья таксономия тегов никогда не уходит вразнос.
3. **Безопасность прежде всего: предпросмотр перед записью** — каждое изменение показывается как manifest сухого прогона (dry-run) для вашей проверки, и пакетная запись в Eagle происходит только после вашего одобрения. После записи перечитывает каждый элемент для проверки — никогда не мутирует библиотеку молча.
4. **Масштабируется на большие пакеты** — для прогонов 100+ ассетов встроенный Python-скрипт выполняет пакетную запись через stdio, поэтому не нужно забивать огромные данные в диалог.
5. **Уважает ваши существующие имена** — ассеты с уже хорошим именем по умолчанию сохраняют его и получают только аннотацию + теги; автоматически переименовываются только бессмысленные / случайные имена, а перезаписывать ли — всегда ваше решение в manifest сухого прогона.
6. **Восстанавливаемые пакеты** — перед любой записью одна команда снимает снимок текущих имени / тегов / аннотации каждого ассета в JSON с отметкой времени; сопутствующий скрипт восстанавливает из него (после подтверждения «yes»), если пакет пошёл не так.

## Установка

Этот навык соответствует открытому стандарту [Agent Skills](https://agentskills.io) (`SKILL.md` + `scripts/` + `references/`) и работает в любом совместимом AI-агенте. Клонируйте репозиторий в каталог навыков вашего агента:

| Агент | Пользовательский каталог | Каталог проекта |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| GitHub Copilot CLI | `~/.copilot/skills/` | `.github/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | — |

Подсказка: `~/.agents/skills/` — межагентный общий каталог: Codex CLI, Gemini CLI, GitHub Copilot и Cursor читают его нативно, Claude Code также сканирует его как запасной путь. Одна установка — обнаружение во всех агентах.

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.agents/skills/eagle-untagged-organizer
```

Или скопируйте папку вручную в любой из перечисленных каталогов.

## Требования

- Приложение Eagle должно быть запущено.
- `eagle-mcp` (MCP-сервер, встроенный в официальный плагин Eagle) должен быть зарегистрирован в конфигурации MCP вашего агента:

| Агент | Конфигурация MCP |
|---|---|
| Claude Code | `claude mcp add` или `.mcp.json` проекта |
| Codex CLI | `~/.codex/config.toml` → `[mcp_servers.eagle-mcp]` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers` |
| GitHub Copilot | `.mcp.json` (корень репозитория) |
| Cursor | `~/.cursor/mcp.json` |
| WorkBuddy | `~/.workbuddy/mcp.json` → `mcpServers` |

## Использование

Упомяните Eagle / `eagle-mcp` / неразмеченные ассеты с намерением пакетной организации — навык ведёт рабочий процесс. Полный процесс (предварительные проверки → анализ → предпросмотр сухого прогона → шлюз авторизации → пакетное обновление → проверка) см. в [`SKILL.md`](../SKILL.md).

> Нужно, наоборот, привести в порядок запутанный словарь тегов (объединить, переименовать или вывести из употребления теги)? Используйте [`eagle-tag-governance`](https://github.com/ChosenXu/eagle-tag-governance). Оба навыка независимы.

## Структура

```
SKILL.md                     # определение навыка и рабочий процесс
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

## Лицензия

[MIT](../LICENSE)
