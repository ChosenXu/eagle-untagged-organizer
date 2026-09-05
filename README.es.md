# Eagle Untagged Organizer

[English](README.md) | [简体中文](README.zh-CN.md) | [繁体中文](README.zh-Hant.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md)

Una habilidad de [WorkBuddy](https://www.workbuddy.cn/) que organiza por lotes los activos de diseño **sin etiquetar** en [Eagle](https://eagle.cool/) a través del conector `eagle-mcp` — renombrando, anotando y etiquetando referencias UI/UX y obras de diseño gráfico en una sola pasada.

## Qué hace

Para cada activo sin etiquetar seleccionado produce tres salidas, escritas de vuelta en Eagle en una sola llamada `item_update`:

1. **Nombre** — un nombre conciso estilo título (buscable en la cuadrícula de Eagle); si un activo ya tiene un buen nombre, se conserva o propone sobrescribir en lugar de renombrar a ciegas.
2. **Anotación** — un bloque estructurado de cinco campos (Tipo / Estructura / Visual / Uso / Valor de referencia)
3. **Etiquetas** — seleccionadas literalmente de un vocabulario controlado de tres dimensiones (ámbito del diseño / estilo visual / técnica)

El idioma de salida es configurable (简体中文 / 繁體中文（港式）/ English / 日本語 / 한국어 / Русский / Español / Deutsch). Si el idioma de la instrucción del usuario es compatible, se hereda ese idioma; de lo contrario se usa el inglés como respaldo.

## Destacados

1. **Realmente «lee» cada activo antes de actuar** — nunca adivina por el nombre de archivo. Primero ejecuta una comprobación previa multimodal, leyendo cada imagen para entender sus sujetos, colores y disposición, y solo entonces produce nombres y anotaciones — la calidad está garantizada.
2. **Estructurado, reutilizable y en buen camino** — los nombres son títulos cortos, no frases analíticas; las anotaciones siguen una plantilla fija de cinco campos; las etiquetas provienen de un vocabulario controlado de tres dimensiones y se seleccionan literalmente (sin términos inventados). El resultado es una biblioteca coherente cuya taxonomía de etiquetas nunca se descontrola.
3. **Seguridad primero: vista previa antes de escribir** — cada cambio se muestra como un manifiesto de dry-run para tu revisión, y solo se escribe en Eagle por lotes tras tu aprobación. Después de escribir, vuelve a leer cada elemento para verificar — nunca muta tu biblioteca en silencio.
4. **Escala a lotes grandes** — para ejecuciones de 100+ activos, un script Python integrado realiza escrituras por lotes sobre stdio, para que no haya que introducir cargas enormes en la conversación.
5. **Respeta tus nombres existentes** — los activos que ya tienen un buen nombre lo conservan por defecto y solo reciben anotación + etiquetas; solo se renombran automáticamente los nombres sin sentido / aleatorios, y si sobrescribir o no siempre es decisión tuya en el manifiesto de dry-run.
6. **Lotes recuperables** — antes de cualquier escritura, un comando captura el nombre / etiquetas / anotación actuales de cada activo en un JSON con marca de tiempo; un script complementario restaura desde él (tras confirmar «yes») si algo sale mal.

## Instalar

Clona este repositorio en tu directorio de habilidades de WorkBuddy:

```bash
git clone https://github.com/ChosenXu/eagle-untagged-organizer.git \
  ~/.workbuddy/skills/eagle-untagged-organizer
```

O copia la carpeta manualmente en `~/.workbuddy/skills/`.

## Requisitos previos

- La aplicación de escritorio Eagle debe estar en ejecución.
- `eagle-mcp` debe estar configurado en `~/.workbuddy/mcp.json` y ser confiable en el panel de conectores.

## Uso

Menciona Eagle / `eagle-mcp` / activos sin etiquetar con intención de organización por lotes, y la habilidad conduce el flujo de trabajo. Consulta [`SKILL.md`](SKILL.md) para el flujo completo (comprobaciones previas → analizar → vista previa de dry-run → puerta de autorización → actualización por lotes → verificar).

## Estructura

```
SKILL.md                     # definición del skill y flujo de trabajo
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

## Licencia

[MIT](LICENSE)
