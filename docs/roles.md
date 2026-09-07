# Semantic roles

Ports do not reference palette colors directly. They reference **roles**, and
roles resolve to a palette color per variant. Change `keyword` from `orange`
to `pink` in `palette.toml` and all 11 targets follow in one regenerate.

## The map

<!-- BEGIN GENERATED: roles -->
| role                 | token         | dark      | light     | style         |
|----------------------|---------------|-----------|-----------|---------------|
| `keyword`            | `orange`      | `#e47534` | `#c72f07` | -             |
| `keyword-ctrl`       | `orange`      | `#e47534` | `#c72f07` | -             |
| `keyword-op`         | `orange`      | `#e47534` | `#c72f07` | -             |
| `operator`           | `orange`      | `#e47534` | `#c72f07` | -             |
| `builtin`            | `amber`       | `#d28f27` | `#915d14` | -             |
| `decorator`          | `amber`       | `#d28f27` | `#915d14` | -             |
| `string`             | `green`       | `#7ab03a` | `#0b7347` | -             |
| `string-doc`         | `green`       | `#7ab03a` | `#0b7347` | italic        |
| `string-escape`      | `amber`       | `#d28f27` | `#915d14` | -             |
| `regex`              | `pink`        | `#e2548e` | `#a93c68` | -             |
| `number`             | `light-blue`  | `#38a4c2` | `#25708a` | -             |
| `boolean`            | `light-blue`  | `#38a4c2` | `#25708a` | -             |
| `constant`           | `light-blue`  | `#38a4c2` | `#25708a` | -             |
| `type`               | `blue`        | `#77a0d2` | `#1540e0` | -             |
| `class`              | `blue`        | `#77a0d2` | `#1540e0` | -             |
| `namespace`          | `blue`        | `#77a0d2` | `#1540e0` | -             |
| `interface`          | `blue`        | `#77a0d2` | `#1540e0` | -             |
| `function`           | `purple`      | `#c48ed0` | `#9d1ab1` | -             |
| `method`             | `purple`      | `#c48ed0` | `#9d1ab1` | -             |
| `variable`           | `fg`          | `#c9c9c9` | `#3a3a3a` | -             |
| `parameter`          | `fg`          | `#c9c9c9` | `#3a3a3a` | -             |
| `property`           | `light-green` | `#48aa78` | `#084b31` | -             |
| `attribute`          | `amber`       | `#d28f27` | `#915d14` | -             |
| `tag`                | `orange`      | `#e47534` | `#c72f07` | -             |
| `label`              | `amber`       | `#d28f27` | `#915d14` | -             |
| `preprocessor`       | `indigo`      | `#9084d7` | `#5240b8` | -             |
| `punctuation`        | `subtext`     | `#9e9e9e` | `#5e5e5e` | -             |
| `comment`            | `subtext`     | `#9e9e9e` | `#5e5e5e` | italic        |
| `comment-doc`        | `subtext`     | `#9e9e9e` | `#5e5e5e` | italic        |
| `link`               | `light-blue`  | `#38a4c2` | `#25708a` | underline     |
| `heading`            | `orange`      | `#e47534` | `#c72f07` | bold          |
| `deprecated`         | `faint`       | `#8c8c8c` | `#6a6a6a` | strikethrough |
| `diagnostic.error`   | `pink`        | `#e2548e` | `#a93c68` | -             |
| `diagnostic.warning` | `amber`       | `#d28f27` | `#915d14` | -             |
| `diagnostic.info`    | `blue`        | `#77a0d2` | `#1540e0` | -             |
| `diagnostic.hint`    | `subtext`     | `#9e9e9e` | `#5e5e5e` | -             |
| `diagnostic.ok`      | `green`       | `#7ab03a` | `#0b7347` | -             |
| `diff.added`         | `green`       | `#7ab03a` | `#0b7347` | -             |
| `diff.removed`       | `pink`        | `#e2548e` | `#a93c68` | -             |
| `diff.changed`       | `yellow`      | `#bdaa2f` | `#6f681c` | -             |
<!-- END GENERATED: roles -->

## Why these assignments

### Warm for control, cool for structure

The broad split: warm accents mark what the code *does*, cool accents mark
what it *is*.

- `orange` — keywords, control flow, operators, tags. The brand's primary
  color on the thing you scan for first.
- `amber` — builtins, decorators, attributes, string escapes. Warm but
  quieter than orange, for names the language gave you rather than ones you
  wrote.
- `green` — strings and insertions. The most common non-code content in a
  file, and green is restful at high frequency.
- `light-blue` — numbers, booleans, constants. Literal values that are not
  strings.
- `blue` — types, classes, namespaces, interfaces. Everything structural.
- `purple` — functions and methods. Distinct from `blue` so a call site is
  never confused with a type reference.
- `light-green` — properties and members.
- `indigo` — preprocessor and imports. Rare enough to earn its own hue.
- `pink` — errors, deletions, regexes. See below.
- `yellow` — `diff.changed` only. Deliberately narrow: on light backgrounds
  yellow is the hardest hue to keep legible, so it carries the least work.

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

### Comments are italic and 6:1

Comments get `subtext` plus italic. The contrast is deliberately in the
middle of the range — around 6:1, clearing AA with margin but visibly
quieter than body text. A comment nobody can read is worse than no comment,
and a comment as loud as the code is noise.

### There is no red

The Grafana brand palette contains no red. Rather than invent one, the
roles that conventionally want red map to `pink`:

| role | color | reasoning |
|---|---|---|
| `diagnostic.error` | `pink` | the most red-adjacent brand hue |
| `diff.removed` | `pink` | consistent with error |
| `regex` | `pink` | regexes are where syntax errors hide, so the association is useful |
| `diagnostic.warning` | `amber` | already the brand's caution color |

Pink is checked to be ΔE ≥ 10 from `orange` in both variants, so "something
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
