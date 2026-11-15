# Semantic roles

Ports do not reference palette colors directly. They reference **roles**, and
roles resolve to a palette color per variant. Change `keyword` from `orange`
to `pink` in `palette.toml` and all 13 targets follow in one regenerate.

## The map

<!-- BEGIN GENERATED: roles -->
| role                 | token        | dark brand | dark dim  | light brand | light dim | style         |
|----------------------|--------------|------------|-----------|-------------|-----------|---------------|
| `keyword`            | `orange`     | `#ff671d`  | `#e48a67` | `#f04205`   | `#c05f46` | -             |
| `keyword-ctrl`       | `orange`     | `#ff671d`  | `#e48a67` | `#f04205`   | `#c05f46` | -             |
| `keyword-op`         | `orange`     | `#ff671d`  | `#e48a67` | `#f04205`   | `#c05f46` | -             |
| `operator`           | `orange`     | `#ff671d`  | `#e48a67` | `#f04205`   | `#c05f46` | -             |
| `builtin`            | `amber`      | `#ffab29`  | `#dbaa6d` | `#d6760b`   | `#ad7548` | -             |
| `decorator`          | `amber`      | `#ffab29`  | `#dbaa6d` | `#d6760b`   | `#ad7548` | -             |
| `string`             | `green`      | `#04bc4c`  | `#6db979` | `#0c9065`   | `#4c856b` | -             |
| `string-doc`         | `green`      | `#04bc4c`  | `#6db979` | `#0c9065`   | `#4c856b` | italic        |
| `string-escape`      | `amber`      | `#ffab29`  | `#dbaa6d` | `#d6760b`   | `#ad7548` | -             |
| `regex`              | `pink`       | `#f35998`  | `#de82a2` | `#e14889`   | `#b65f7e` | -             |
| `number`             | `purple`     | `#d444f1`  | `#ca7cdb` | `#d444f1`   | `#ac5fbc` | -             |
| `boolean`            | `purple`     | `#d444f1`  | `#ca7cdb` | `#d444f1`   | `#ac5fbc` | -             |
| `constant`           | `purple`     | `#d444f1`  | `#ca7cdb` | `#d444f1`   | `#ac5fbc` | -             |
| `type`               | `yellow`     | `#ffed23`  | `#d3ca6e` | `#aa710e`   | `#947347` | -             |
| `class`              | `yellow`     | `#ffed23`  | `#d3ca6e` | `#aa710e`   | `#947347` | -             |
| `namespace`          | `yellow`     | `#ffed23`  | `#d3ca6e` | `#aa710e`   | `#947347` | -             |
| `interface`          | `yellow`     | `#ffed23`  | `#d3ca6e` | `#aa710e`   | `#947347` | -             |
| `function`           | `blue`       | `#2970ff`  | `#6794e8` | `#2970ff`   | `#4b76c7` | -             |
| `method`             | `blue`       | `#2970ff`  | `#6794e8` | `#2970ff`   | `#4b76c7` | -             |
| `variable`           | `fg`         | `#f4f4f4`  | `#cccccc` | `#171717`   | `#3a3a3a` | -             |
| `parameter`          | `fg`         | `#f4f4f4`  | `#cccccc` | `#171717`   | `#3a3a3a` | -             |
| `property`           | `light-blue` | `#3fc6eb`  | `#78bad0` | `#0a92b1`   | `#4c8597` | -             |
| `attribute`          | `amber`      | `#ffab29`  | `#dbaa6d` | `#d6760b`   | `#ad7548` | -             |
| `tag`                | `orange`     | `#ff671d`  | `#e48a67` | `#f04205`   | `#c05f46` | -             |
| `label`              | `amber`      | `#ffab29`  | `#dbaa6d` | `#d6760b`   | `#ad7548` | -             |
| `preprocessor`       | `indigo`     | `#7d64ff`  | `#928ce7` | `#7d64ff`   | `#756ec6` | -             |
| `punctuation`        | `subtext`    | `#afafaf`  | `#8f8f8f` | `#696969`   | `#6e6e6e` | -             |
| `comment`            | `subtext`    | `#afafaf`  | `#8f8f8f` | `#696969`   | `#6e6e6e` | italic        |
| `comment-doc`        | `subtext`    | `#afafaf`  | `#8f8f8f` | `#696969`   | `#6e6e6e` | italic        |
| `link`               | `light-blue` | `#3fc6eb`  | `#78bad0` | `#0a92b1`   | `#4c8597` | underline     |
| `heading`            | `orange`     | `#ff671d`  | `#e48a67` | `#f04205`   | `#c05f46` | bold          |
| `deprecated`         | `faint`      | `#696969`  | `#666666` | `#afafaf`   | `#a0a0a0` | strikethrough |
| `diagnostic.error`   | `pink`       | `#f35998`  | `#de82a2` | `#e14889`   | `#b65f7e` | -             |
| `diagnostic.warning` | `amber`      | `#ffab29`  | `#dbaa6d` | `#d6760b`   | `#ad7548` | -             |
| `diagnostic.info`    | `blue`       | `#2970ff`  | `#6794e8` | `#2970ff`   | `#4b76c7` | -             |
| `diagnostic.hint`    | `subtext`    | `#afafaf`  | `#8f8f8f` | `#696969`   | `#6e6e6e` | -             |
| `diagnostic.ok`      | `green`      | `#04bc4c`  | `#6db979` | `#0c9065`   | `#4c856b` | -             |
| `diff.added`         | `green`      | `#04bc4c`  | `#6db979` | `#0c9065`   | `#4c856b` | -             |
| `diff.removed`       | `pink`       | `#f35998`  | `#de82a2` | `#e14889`   | `#b65f7e` | -             |
| `diff.changed`       | `yellow`     | `#ffed23`  | `#d3ca6e` | `#aa710e`   | `#947347` | -             |
<!-- END GENERATED: roles -->

## Why these assignments

### Primary and secondary colors carry the frequent roles

The Grafana brand guide ranks its colors: one primary (orange), four
chromatic secondaries (yellow, green, blue, purple), then five support
colors. The roles follow that ranking. The five kinds of token that fill
most of a source file each get a primary or secondary color, so a screen of
code looks like the brand rather than like its supporting cast.

- `orange` (primary) — keywords, control flow, operators, tags, headings.
  The brand's own color on the thing you scan for first.
- `blue` (secondary) — functions and methods. Call sites are the next most
  frequent thing after keywords, and blue is the calmest secondary to read
  at that density.
- `green` (secondary) — strings and insertions. The most common non-code
  content in a file, and green is restful at high frequency.
- `yellow` (secondary) — types, classes, namespaces, interfaces, and
  `diff.changed`. Types are frequent but not dense, which suits the
  brightest color in the palette. On light backgrounds yellow becomes the
  brand's 160% step, a dark gold.
- `purple` (secondary) — numbers, booleans, constants. Literal values that
  are not strings.

The support colors take the rarer roles:

- `amber` — builtins, decorators, attributes, labels, string escapes, and
  warnings. Warm like orange but quieter, for names the language gave you
  rather than ones you wrote.
- `light-blue` — properties, members, and links.
- `indigo` — preprocessor directives and imports.
- `pink` — errors, deletions, regexes. See below.
- `light-green` — no syntax role. It stays in the palette for targets that
  expose every accent: tmux's `@grafana_light_green` option and Herdr's
  `teal` slot.

### Variables are plain foreground

`variable` and `parameter` resolve to `fg`, not to an accent. In real code
identifiers are the majority of the characters on screen; coloring them
means coloring everything, which defeats the point. Reserving plain
foreground for them lets the accents actually mean something.

This is a change from the original site theme, which used pink for
variables.

### Punctuation is dimmed

`punctuation` resolves to `subtext` rather than `fg`. Brackets, commas and
semicolons are structural noise that the eye already parses from shape.
Dimming them slightly makes the identifiers and keywords between them read
more clearly.

### Comments are muted and italic

Comments use `subtext` (Neutral 2 on brand dark, Neutral 3 on brand light)
plus italic. Their softer tone keeps them behind the main code.

### There is no red

The Grafana brand palette contains no red. Rather than invent one, the
roles that conventionally want red map to `pink`:

| role | color | reasoning |
|---|---|---|
| `diagnostic.error` | `pink` | the most red-adjacent brand hue |
| `diff.removed` | `pink` | consistent with error |
| `regex` | `pink` | regexes are where syntax errors hide, so the association is useful |
| `diagnostic.warning` | `amber` | already the brand's caution color |

Pink is checked to be ΔE ≥ 8 from `orange` in every variant and flavor, so "something
is wrong" never reads as "this is a keyword".

The one place the absence leaks through is Herdr, whose theme token
vocabulary hard-codes the name `red`. That file sets `red` to our pink and
notes it inline.

## Adding a role

1. Add it to `[roles]` in `palette.toml`, pointing at a palette token.
2. Reference it from the emitters that can express it, via `v.rc("name")`.
3. Add it to `_ROLE_ORDER` in `tools/gcs/docs.py` so it appears in this
   table.
4. Run `python3 tools/generate.py`.

`--verify` will reject a role whose color does not resolve or whose style is
not one of `italic`, `bold`, `underline`, `strikethrough`.
