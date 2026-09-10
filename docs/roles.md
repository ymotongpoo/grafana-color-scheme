# Semantic roles

Ports do not reference palette colors directly. They reference **roles**, and
roles resolve to a palette color per variant. Change `keyword` from `orange`
to `pink` in `palette.toml` and all 11 targets follow in one regenerate.

## The map

<!-- BEGIN GENERATED: roles -->
| role                 | token         | dark      | light     | style         |
|----------------------|---------------|-----------|-----------|---------------|
| `keyword`            | `orange`      | `#c18c68` | `#ac795a` | -             |
| `keyword-ctrl`       | `orange`      | `#c18c68` | `#ac795a` | -             |
| `keyword-op`         | `orange`      | `#c18c68` | `#ac795a` | -             |
| `operator`           | `orange`      | `#c18c68` | `#ac795a` | -             |
| `builtin`            | `amber`       | `#b4a075` | `#a08a61` | -             |
| `decorator`          | `amber`       | `#b4a075` | `#a08a61` | -             |
| `string`             | `green`       | `#89a17e` | `#7d9068` | -             |
| `string-doc`         | `green`       | `#89a17e` | `#7d9068` | italic        |
| `string-escape`      | `amber`       | `#b4a075` | `#a08a61` | -             |
| `regex`              | `pink`        | `#b77f94` | `#ac7b8d` | -             |
| `number`             | `light-blue`  | `#789fa6` | `#719399` | -             |
| `boolean`            | `light-blue`  | `#789fa6` | `#719399` | -             |
| `constant`           | `light-blue`  | `#789fa6` | `#719399` | -             |
| `type`               | `blue`        | `#8198b5` | `#7b8da5` | -             |
| `class`              | `blue`        | `#8198b5` | `#7b8da5` | -             |
| `namespace`          | `blue`        | `#8198b5` | `#7b8da5` | -             |
| `interface`          | `blue`        | `#8198b5` | `#7b8da5` | -             |
| `function`           | `purple`      | `#ad8eaf` | `#a183a2` | -             |
| `method`             | `purple`      | `#ad8eaf` | `#a183a2` | -             |
| `variable`           | `fg`          | `#b9b1a9` | `#6b625b` | -             |
| `parameter`          | `fg`          | `#b9b1a9` | `#6b625b` | -             |
| `property`           | `light-green` | `#79a08a` | `#6f9381` | -             |
| `attribute`          | `amber`       | `#b4a075` | `#a08a61` | -             |
| `tag`                | `orange`      | `#c18c68` | `#ac795a` | -             |
| `label`              | `amber`       | `#b4a075` | `#a08a61` | -             |
| `preprocessor`       | `indigo`      | `#8d86b1` | `#8a80aa` | -             |
| `punctuation`        | `subtext`     | `#8d8279` | `#928579` | -             |
| `comment`            | `subtext`     | `#8d8279` | `#928579` | italic        |
| `comment-doc`        | `subtext`     | `#8d8279` | `#928579` | italic        |
| `link`               | `light-blue`  | `#789fa6` | `#719399` | underline     |
| `heading`            | `orange`      | `#c18c68` | `#ac795a` | bold          |
| `deprecated`         | `faint`       | `#786d63` | `#a89b8e` | strikethrough |
| `diagnostic.error`   | `pink`        | `#b77f94` | `#ac7b8d` | -             |
| `diagnostic.warning` | `amber`       | `#b4a075` | `#a08a61` | -             |
| `diagnostic.info`    | `blue`        | `#8198b5` | `#7b8da5` | -             |
| `diagnostic.hint`    | `subtext`     | `#8d8279` | `#928579` | -             |
| `diagnostic.ok`      | `green`       | `#89a17e` | `#7d9068` | -             |
| `diff.added`         | `green`       | `#89a17e` | `#7d9068` | -             |
| `diff.removed`       | `pink`        | `#b77f94` | `#ac7b8d` | -             |
| `diff.changed`       | `yellow`      | `#acaa70` | `#989363` | -             |
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

### Comments are muted and italic

Comments use `subtext` plus italic. Their softer tone keeps them behind the
main code. The palette is tuned visually, without a minimum contrast target.

### There is no red

The Grafana brand palette contains no red. Rather than invent one, the
roles that conventionally want red map to `pink`:

| role | color | reasoning |
|---|---|---|
| `diagnostic.error` | `pink` | the most red-adjacent brand hue |
| `diff.removed` | `pink` | consistent with error |
| `regex` | `pink` | regexes are where syntax errors hide, so the association is useful |
| `diagnostic.warning` | `amber` | already the brand's caution color |

Pink is checked to be ΔE ≥ 8 from `orange` in both variants, so "something
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
