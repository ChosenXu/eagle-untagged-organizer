# Eagle Untagged Organizer

[English](../README.md) | [简体中文](README.zh-CN.md) | [繁体中文](README.zh-Hant.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md) | Deutsch

Ein zum offenen [Agent Skills](https://agentskills.io)-Standard kompatibler Skill, der **nicht markierte** Design-Assets in [Eagle](https://eagle.cool/) über den MCP-Server `eagle-mcp` stapelweise organisiert — Umbenennen, Annotieren und Taggen von UI/UX-Referenzen und Grafikdesign-Werken in einem Durchgang. Funktioniert mit Claude Code, Codex CLI, Gemini CLI, GitHub Copilot, Cursor und WorkBuddy.

## Was es macht

Für jedes ausgewählte, nicht markierte Asset erzeugt es drei Ausgaben, die in Eagle mit einem einzigen `item_update`-Aufruf zurückgeschrieben werden:

1. **Name** — ein prägnanter, titelartiger Name (im Eagle-Raster durchsuchbar); hat ein Asset bereits einen guten Namen, wird er behalten oder zum Überschreiben vorgeschlagen, statt blind umbenannt zu werden.
2. **Annotation** — ein strukturierter Fünf-Felder-Block (Typ / Struktur / Visual / Verwendung / Referenzwert)
3. **Tags** — wörtlich aus einem kontrollierten, dreidimensionalen Vokabular ausgewählt (Designbereich / visueller Stil / Technik)

Die Ausgabesprache ist konfigurierbar (简体中文 / 繁體中文（港式）/ English / 日本語 / 한국어 / Русский / Español / Deutsch). Entspricht die Sprache der Benutzeranweisung einer unterstützten Sprache, wird diese übernommen, andernfalls wird Englisch als Rückfall verwendet.

## Highlights

1. **Liest jedes Asset wirklich, bevor es handelt** — es rät nie aus Dateinamen. Zuerst führt es eine multimodale Vorabprüfung durch, liest jedes Bild, um Motive, Farben und Layout zu verstehen, und erzeugt erst dann Namen und Annotationen — Qualität ist garantiert.
2. **Strukturiert, wiederverwendbar und auf Kurs** — Namen sind kurze Titel, keine Analyse-Sätze; Annotationen folgen einer festen Fünf-Felder-Vorlage; Tags stammen aus einem kontrollierten, dreidimensionalen Vokabular und werden wörtlich ausgewählt (keine erfundenen Begriffe). Das Ergebnis ist eine konsistente Bibliothek, deren Tag-Taxonomie nie außer Kontrolle gerät.
3. **Sicherheit zuerst: Vorschau vor dem Schreiben** — jede Änderung wird als Dry-Run-Manifest zur Prüfung angezeigt und nur nach deiner Freigabe stapelweise in Eagle geschrieben. Nach dem Schreiben liest es jedes Element erneut zur Verifikation — es verändert deine Bibliothek nie stillschweigend.
4. **Skaliert auf große Stapel** — bei Läufen mit 100+ Assets führt ein eingebautes Python-Skript die Stapelschreibvorgänge über stdio aus, sodass keine riesigen Nutzlasten in den Dialog gepresst werden müssen.
5. **Respektiert deine vorhandenen Namen** — Assets mit bereits gutem Namen behalten ihn standardmäßig und erhalten nur Annotation + Tags; nur sinnlose / zufällige Namen werden automatisch umbenannt, und ob überschrieben wird, entscheidest du immer im Dry-Run-Manifest.
6. **Wiederherstellbare Stapel** — vor jedem Schreiben sichert ein Befehl Namen / Tags / Annotation jedes Assets als Snapshot in einer JSON-Datei mit Zeitstempel; ein Begleitskript stellt daraus wieder her (nach «yes»-Bestätigung), falls ein Stapel fehlschlägt.

## Installieren

Dieser Skill folgt dem offenen [Agent Skills](https://agentskills.io)-Standard (`SKILL.md` + `scripts/` + `references/`) und funktioniert in jedem kompatiblen KI-Agenten. Klone dieses Repository in das Skills-Verzeichnis deines Agenten:

| Agent | Benutzerverzeichnis | Projektverzeichnis |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| GitHub Copilot CLI | `~/.copilot/skills/` | `.github/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | — |

Tipp: `~/.agents/skills/` ist das agentenübergreifende Verzeichnis — Codex CLI, Gemini CLI, GitHub Copilot und Cursor lesen es nativ, und Claude Code durchsucht es ebenfalls als Fallback. Einmal installiert, wird er von mehreren Agenten entdeckt.

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.agents/skills/eagle-untagged-organizer
```

Oder kopiere den Ordner manuell in eines der obigen Verzeichnisse.

## Voraussetzungen

- Die Eagle-Desktop-App muss laufen.
- `eagle-mcp` (der in Eagles offiziellem Plugin enthaltene MCP-Server) muss in der MCP-Konfiguration deines Agenten registriert sein:

| Agent | MCP-Konfiguration |
|---|---|
| Claude Code | `claude mcp add` oder Projekt-`.mcp.json` |
| Codex CLI | `~/.codex/config.toml` → `[mcp_servers.eagle-mcp]` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers` |
| GitHub Copilot | `.mcp.json` (Repo-Root) |
| Cursor | `~/.cursor/mcp.json` |
| WorkBuddy | `~/.workbuddy/mcp.json` → `mcpServers` |

## Nutzung

Erwähne Eagle / `eagle-mcp` / nicht markierte Assets mit dem Vorsatz einer Stapelorganisation, und der Skill steuert den Workflow. Siehe [`SKILL.md`](../SKILL.md) für den vollständigen Workflow (Vorabprüfungen → analysieren → Dry-Run-Vorschau → Autorisierungs-Gate → Stapelupdate → verifizieren).

> Musst du stattdessen ein chaotisches Tag-Vokabular bereinigen (Tags zusammenführen, umbenennen oder ausmustern)? Nutze [`eagle-tag-governance`](https://github.com/ChosenXu/eagle-tag-governance). Die beiden Skills sind unabhängig.

## Struktur

```
SKILL.md                     # Skill-Definition und Workflow
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

## Lizenz

[MIT](../LICENSE)
