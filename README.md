# Grafana color scheme

One palette, derived from the Grafana Labs brand colors, ported to 11 tools.
Dim rather than high contrast, and every syntax token clears WCAG AA.

![Grafana Dark palette](docs/palette-dark.svg)

![Grafana Light palette](docs/palette-light.svg)

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

> **Not an official Grafana Labs project.** "Grafana" is a trademark of
> Grafana Labs; this repository is an independent port of their brand palette
> and is not affiliated with or endorsed by them. See [NOTICE](NOTICE).

## About

Two variants, `grafana-dark` and `grafana-light`, generated from a single
source of truth ([`palette.toml`](palette.toml)) by one dependency-free
script. The generated files are committed, so you can download the one file
your tool needs and never run anything.

The scheme started life as the syntax highlighting for
[www.ymotongpoo.com](https://www.ymotongpoo.com) and was generalized from
there.

## Palette

### Base colors

Taken verbatim from the Grafana Labs brand guide. These are never edited to
fix a contrast problem; the variants are.

<!-- BEGIN GENERATED: brand -->
| brand color   | hex       | group     |
|---------------|-----------|-----------|
| `orange`      | `#ff671d` | primary   |
| `white`       | `#ffffff` | secondary |
| `black`       | `#000000` | secondary |
| `yellow`      | `#ffed23` | secondary |
| `green`       | `#04bc4c` | secondary |
| `blue`        | `#2970ff` | secondary |
| `purple`      | `#d444f1` | secondary |
| `amber`       | `#ffab29` | support   |
| `light-green` | `#91d441` | support   |
| `light-blue`  | `#3fc6eb` | support   |
| `indigo`      | `#7d64ff` | support   |
| `pink`        | `#f35998` | support   |
| `neutral-1`   | `#f4f4f4` | neutral   |
| `neutral-2`   | `#afafaf` | neutral   |
| `neutral-3`   | `#696969` | neutral   |
| `neutral-4`   | `#3a3a3a` | neutral   |
| `neutral-5`   | `#171717` | neutral   |
<!-- END GENERATED: brand -->

The brand also publishes tint and shade ladders for five hues. The light
variant draws most of its accents from the 140–180% steps.

<!-- BEGIN GENERATED: ladders -->
| hue      | 20%       | 40%       | 60%       | 80%       | 100%      | 120%      | 140%      | 160%      | 180%      |
|----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| `orange` | `#fee9d4` | `#ffd0a7` | `#ffad70` | `#ff8137` | `#ff671d` | `#f04205` | `#c72f07` | `#9d250e` | `#7f230f` |
| `yellow` | `#fcffd2` | `#fffea8` | `#fff86b` | `#feed55` | `#fbe136` | `#fdc809` | `#cf9304` | `#aa710e` | `#915d14` |
| `green`  | `#d7f9e3` | `#aaf0c7` | `#72e1a6` | `#54d192` | `#18b16a` | `#0c9065` | `#0b7347` | `#0a5b39` | `#084b31` |
| `blue`   | `#d9e7ff` | `#bbd8ff` | `#8dc0ff` | `#599bff` | `#2870ff` | `#1b55f5` | `#1540e0` | `#1734b6` | `#1a308f` |
| `purple` | `#f9e8fe` | `#f3ceff` | `#eeaafd` | `#e477fb` | `#d444f0` | `#bb23d5` | `#9d1ab1` | `#831790` | `#6e1976` |
<!-- END GENERATED: ladders -->

Two things worth knowing about the source data:

- **The 100% step of a ladder is not always the secondary color of the same
  name.** The guide lists green as `#04bc4c` but centers its ladder on
  `#18b16a`; yellow is `#ffed23` against a ladder center of `#fbe136`; blue
  and purple differ in the last digit. Both sets are reproduced faithfully in
  `palette.toml`, and the ladders are what the variants are built from.
- **There is no red.** See [below](#there-is-no-red).

### Derivation

The point of the scheme is that no single token shouts over the others, so
both variants aim their accents into a narrow contrast band instead of
maximizing contrast.

- **Dark** puts the background at `#1e1e1e` — brand `neutral-5` mixed 20%
  toward `neutral-4` — then mixes each brand hue 5–30% *toward that
  background*. Mixing toward the background lowers luminance and saturation
  together, which is what reads as "dim" rather than merely "dark".
- **Light** puts the background at `#f7f7f7` and starts from the brand's
  140–180% shades, deepening toward `neutral-5` only as far as needed.

Full reasoning, including the values that had to be nudged and why, is in
[docs/derivation.md](docs/derivation.md).

### Dark

<!-- BEGIN GENERATED: palette-dark -->
| token         | hex       | brand origin | contrast on `#1e1e1e` |
|---------------|-----------|--------------|-----------------------|
| `orange`      | `#e47534` | orange 80%   | 5.47:1                |
| `amber`       | `#d28f27` | amber        | 6.11:1                |
| `yellow`      | `#bdaa2f` | yellow 100%  | 7.11:1                |
| `green`       | `#7ab03a` | light green  | 6.43:1                |
| `light-green` | `#48aa78` | green 80%    | 5.79:1                |
| `light-blue`  | `#38a4c2` | light blue   | 5.76:1                |
| `blue`        | `#77a0d2` | blue 60%     | 6.15:1                |
| `indigo`      | `#9084d7` | indigo       | 5.13:1                |
| `purple`      | `#c48ed0` | purple 60%   | 6.45:1                |
| `pink`        | `#e2548e` | pink         | 4.68:1                |
<!-- END GENERATED: palette-dark -->

### Light

<!-- BEGIN GENERATED: palette-light -->
| token         | hex       | brand origin | contrast on `#f7f7f7` |
|---------------|-----------|--------------|-----------------------|
| `orange`      | `#c72f07` | orange 140%  | 5.11:1                |
| `amber`       | `#915d14` | yellow 180%  | 5.19:1                |
| `yellow`      | `#6f681c` | yellow       | 5.34:1                |
| `green`       | `#0b7347` | green 140%   | 5.51:1                |
| `light-green` | `#084b31` | green 180%   | 9.51:1                |
| `light-blue`  | `#25708a` | light blue   | 5.21:1                |
| `blue`        | `#1540e0` | blue 140%    | 6.90:1                |
| `indigo`      | `#5240b8` | indigo       | 7.04:1                |
| `purple`      | `#9d1ab1` | purple 140%  | 6.09:1                |
| `pink`        | `#a93c68` | pink         | 5.55:1                |
<!-- END GENERATED: palette-light -->

### Surfaces and text

Surfaces are **two ladders diverging from `base`**, not one chain:

- shadow: `base` → `mantle` → `crust`
- elevation: `base` → `surface0` → `surface1` → `surface2`

In the light variant this matters — `mantle` is lighter than `surface0`, and
`crust` sits between `surface0` and `surface1` — so treating the six as a
single ordering will give you the wrong answer.

<!-- BEGIN GENERATED: surfaces -->
| token      | dark                | light               |
|------------|---------------------|---------------------|
| `crust`    | `#141414`           | `#e4e4e4`           |
| `mantle`   | `#191919`           | `#f0f0f0`           |
| `base`     | `#1e1e1e`           | `#f7f7f7`           |
| `surface0` | `#252525`           | `#ececec`           |
| `surface1` | `#303030`           | `#dcdcdc`           |
| `surface2` | `#3a3a3a`           | `#c9c9c9`           |
| `bright`   | `#f4f4f4` (15.16:1) | `#171717` (16.73:1) |
| `fg`       | `#c9c9c9` (10.07:1) | `#3a3a3a` (10.62:1) |
| `subtext`  | `#9e9e9e` (6.22:1)  | `#5e5e5e` (6.05:1)  |
| `faint`    | `#8c8c8c` (4.96:1)  | `#6a6a6a` (5.05:1)  |
<!-- END GENERATED: surfaces -->

### Semantic roles

Every port maps its own token names onto these roles, so changing a role here
changes all 11 targets at once. The `token` column is the palette color the
role points at.

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

See [docs/roles.md](docs/roles.md) for the reasoning behind individual
assignments.

### ANSI 16

The single highest-leverage table in the repo: WezTerm, iTerm2, tmux, Zed's
`terminal.ansi.*`, VS Code's `terminal.ansi*`, Vim's `g:terminal_ansi_colors`
and Herdr's `terminal` mode all consume it.

<!-- BEGIN GENERATED: ansi -->
| slot | name           | dark dim  | dark vivid | light dim | light vivid |
|------|----------------|-----------|------------|-----------|-------------|
| 0    | black          | `#303030` | `#303030`  | `#171717` | `#171717`   |
| 1    | red            | `#e2548e` | `#e2548e`  | `#a93c68` | `#a93c68`   |
| 2    | green          | `#7ab03a` | `#7ab03a`  | `#0b7347` | `#0b7347`   |
| 3    | yellow         | `#d28f27` | `#d28f27`  | `#915d14` | `#915d14`   |
| 4    | blue           | `#77a0d2` | `#77a0d2`  | `#1540e0` | `#1540e0`   |
| 5    | magenta        | `#c48ed0` | `#c48ed0`  | `#9d1ab1` | `#9d1ab1`   |
| 6    | cyan           | `#38a4c2` | `#38a4c2`  | `#25708a` | `#25708a`   |
| 7    | white          | `#c9c9c9` | `#c9c9c9`  | `#dcdcdc` | `#dcdcdc`   |
| 8    | bright black   | `#8c8c8c` | `#8c8c8c`  | `#5e5e5e` | `#5e5e5e`   |
| 9    | bright red     | `#e56c9d` | `#f35998`  | `#93365c` | `#c72f5f`   |
| 10   | bright green   | `#8cba56` | `#91d441`  | `#0d6540` | `#0c9065`   |
| 11   | bright yellow  | `#d79e46` | `#ffab29`  | `#7f5214` | `#aa710e`   |
| 12   | bright blue    | `#8aadd7` | `#2970ff`  | `#153ac2` | `#1b55f5`   |
| 13   | bright magenta | `#cb9dd5` | `#d444f1`  | `#891a9a` | `#bb23d5`   |
| 14   | bright cyan    | `#54b0ca` | `#3fc6eb`  | `#236379` | `#1b6e85`   |
| 15   | bright white   | `#f4f4f4` | `#f4f4f4`  | `#ffffff` | `#ffffff`   |
<!-- END GENERATED: ansi -->

![Grafana Dark ANSI](docs/ansi-dark.svg)

Slot 0 and slot 15 are the extremes of the variant, so the dark and light
mappings are mirrored rather than identical. Two constraints are enforced:
slot 0 is never equal to the background (or `bg=black` would be invisible),
and slot 8 keeps at least 3:1 against it (or dim output disappears).

### There is no red

The Grafana brand palette has no red. Rather than invent one, the roles that
conventionally want red are mapped onto colors the brand does have:

| role | mapped to | why |
|---|---|---|
| `error`, `diff.removed`, `regex` | `pink` | the most red-adjacent brand hue, and distinct from `orange` at every step of both ladders |
| `warning` | `amber` | already the brand's caution color |

The one place this leaks is Herdr, whose token vocabulary hard-codes the name
`red`; that file sets `red` to our pink and says so in a comment.

### Accessibility

- Every entry in `text.*` and `accents.*` clears **4.5:1** (WCAG 2.1 AA for
  normal text) against its variant's background.
- `text.fg` and `text.subtext` additionally clear 4.5:1 against `surface1`,
  and `text.faint` against `surface0`, so text stays readable on a selected
  or current line rather than only on the plain background.
- The vivid ANSI brights are held to **3:1**. They appear only in slots 9–14,
  which terminals render as bright or bold text, where WCAG 1.4.3 applies the
  large-text threshold.
- Accents are additionally required to be **CIE76 ΔE ≥ 10** apart pairwise.
  Contrast alone does not catch the real failure mode of mixing toward a
  background: two brand hues collapsing into the same color.

These rules live in `palette.toml` as data and are enforced by
`python3 tools/generate.py --verify`, which refuses to generate anything from
a palette that violates them.

## Install

<!-- BEGIN GENERATED: install -->
| tool          | files                                | artifacts                                       | install                                                                             |
|---------------|--------------------------------------|-------------------------------------------------|-------------------------------------------------------------------------------------|
| VS Code       | [`targets/vscode`](targets/vscode)   | extension root with 2 theme files               | symlink `targets/vscode` into `~/.vscode/extensions/`, restart, then pick the theme |
| Zed           | [`targets/zed`](targets/zed)         | 1 theme family (both variants)                  | copy `themes/grafana.json` to `~/.config/zed/themes/`                               |
| Emacs         | [`targets/emacs`](targets/emacs)     | 2 theme files                                   | add the directory to `custom-theme-load-path`, then `(load-theme 'grafana-dark t)`  |
| Vim / Neovim  | [`targets/vim`](targets/vim)         | 2 colorschemes                                  | add `targets/vim` to `runtimepath`, then `:colorscheme grafana-dark`                |
| WezTerm       | [`targets/wezterm`](targets/wezterm) | 4 TOML schemes (+ vivid)                        | copy `colors/*.toml` to `~/.config/wezterm/colors/`, then set `color_scheme`        |
| iTerm2        | [`targets/iterm2`](targets/iterm2)   | 4 color presets (+ vivid)                       | Settings > Profiles > Colors > Color Presets > Import                               |
| tmux          | [`targets/tmux`](targets/tmux)       | 2 themes, optional status line, TPM entry point | `source-file` the conf from `~/.tmux.conf`, or install via TPM                      |
| Herdr         | [`targets/herdr`](targets/herdr)     | 2 config fragments                              | paste the `[theme.custom]` block into `~/.config/herdr/config.toml`                 |
| Chroma / Hugo | [`targets/chroma`](targets/chroma)   | 2 XML styles, 3 stylesheets                     | Hugo: copy a CSS file and set `markup.highlight.noClasses = false`                  |
| Slack         | [`targets/slack`](targets/slack)     | 2 sidebar strings                               | Preferences > Themes, paste the string into the custom theme field                  |
| Chrome        | [`targets/chrome`](targets/chrome)   | 2 unpacked themes                               | `chrome://extensions` > Developer mode > Load unpacked                              |
<!-- END GENERATED: install -->

Each directory has its own README with the full steps and any per-tool
caveats. The directories are shaped the way each tool expects, so
`targets/vim` works as a `runtimepath` entry, `targets/vscode` as an
extension root, and so on.

## Terminal flavors

Terminal targets ship two flavors:

- **dim** (the default, unsuffixed) derives all 16 slots from the same values
  the editors use, so a terminal inside your editor matches it exactly.
- **vivid** (`-vivid`) replaces **only slots 9–14** with the undimmed brand
  colors, so `ls` output and bold text separate more sharply from normal
  text. Everything else is shared with dim.

## Regenerate

```sh
python3 tools/generate.py            # rewrite every target and the doc tables
python3 tools/generate.py --verify   # palette invariants and WCAG only
python3 tools/generate.py --check    # fail if anything on disk is stale
python3 tools/generate.py --list     # registered targets
```

Requires Python 3.11 or newer (for `tomllib`) and nothing else.

**Never hand-edit anything under `targets/`** — edit `palette.toml` and
regenerate. `--check` reports staleness, missing files and orphans left
behind by renames.

Adding a twelfth target is three steps; see
[docs/adding-a-target.md](docs/adding-a-target.md).

## Roadmap

- CI running `--check` and `--verify` on every push
- Submit the `.itermcolors` to
  [mbadolato/iTerm2-Color-Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes),
  which auto-generates ~40 more formats and is where WezTerm syncs its
  bundled schemes from
- Upstream `styles/grafana-*.xml` to
  [alecthomas/chroma](https://github.com/alecthomas/chroma), which would let
  Hugo select the style by name and make the bundled CSS unnecessary
- Upstream the palette to Herdr's built-in theme list
- A Neovim Lua module, plus Alacritty / Ghostty / Kitty / Helix
- Screenshots of real editors

Marketplace publishing (VS Code Marketplace, Open VSX, Chrome Web Store, Zed
extensions) is deliberately out of scope for now: a store listing under the
Grafana name is a different trademark question than a GitHub repository.

## License

[Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for attribution and the
trademark disclaimer.
