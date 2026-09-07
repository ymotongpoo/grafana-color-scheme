# Derivation

How the two variants were produced from the Grafana Labs brand palette, and
which values had to be argued with.

## The goal

A brand palette is designed for marketing surfaces: large areas, short
strings, maximum impact. A syntax palette needs the opposite — twenty
colors sharing one dense screen, none of them shouting. Dropping the brand
hexes straight into an editor produces a theme where keywords and function
names fight each other for attention.

So the target is not "maximum contrast". It is a **narrow contrast band**:
every accent lands close enough to its neighbours that the eye reads the
code, not the colors. Concretely, 4.7–7.1:1 on dark and 5.1–7.6:1 on light,
with a hard floor of 4.5:1 so nothing drops below WCAG AA.

## Dark

The background comes first, because everything else is derived against it.
Brand `neutral-5` (`#171717`) is nearly black, which makes every accent
land at very high contrast. Mixing 20% of `neutral-4` into it gives
`#1e1e1e` — still clearly a dark theme, but with the ceiling lowered enough
that the accents can sit comfortably below it.

Each accent is then the brand hue **mixed 5–30% toward that background**.
This matters more than plain darkening: blending toward the background
lowers luminance *and* saturation together, which is the difference between
"dim" and merely "dark". A darkened-but-saturated palette still shouts.

The mix ratio per hue is whatever lands it in the band, which is why they
differ: pink needs only 8% (it is already the least luminous brand hue),
while orange-60 needs 30%.

Several accents start from a ladder step rather than the base hue, because
the base was in the wrong luminance neighbourhood to begin with:

| accent | starts from | why not the base color |
|---|---|---|
| `orange` | orange 80% | brand orange `#ff671d` is the primary and reads as a call to action; 80% is calmer |
| `blue` | blue 60% | brand blue `#2970ff` is only 4.15:1 on this background, under AA before any dimming |
| `purple` | purple 60% | brand purple `#d444f1` is 5.03:1 undimmed, leaving no headroom to dim |
| `indigo` | indigo, lifted | brand indigo `#7d64ff` is 4.39:1, under AA |
| `green` | light green | brand green `#04bc4c` is a signal green; light green is the readable one at text size |
| `light-green` | green 80% | keeps it distinguishable from `green` |

## Light

Light is the harder variant, and not symmetric with dark.

The background is `#f7f7f7` — brand `neutral-1` lifted slightly, so that
`neutral-1` itself remains usable as a surface. Accents cannot be produced
by mixing toward this background, because mixing toward white *raises*
luminance and drops contrast. They start from the brand's 140–180% shades
instead, deepened toward `neutral-5` only as far as needed.

Where a shade lands in the band on its own, it is used as-is: orange 140%,
green 140%, green 180%, blue 140%, purple 140%. Only `light-blue`, `indigo`
and `pink` needed deepening, because the brand has no dark step for them.

### Yellow on white

The one genuinely awkward case. Yellow hues have to be darkened so far to
reach 4.5:1 on white that they stop being yellow and become brown — and
`amber` and `yellow` both collapse into the *same* brown. The first attempt
had them at `#7c5216` and `#6d4a19`, only ΔE 7.6 apart, which the separation
check correctly rejected.

The fix was to stop deriving both from the same source. `amber` is the
yellow-180% shade as-is (`#915d14`, an orange-brown), and `yellow` is
derived from brand yellow `#ffed23`, which is the greener of the two, giving
an olive cast (`#6f681c`). That puts them ΔE 22.9 apart while both stay in
the band.

This is worth knowing if you ever retune the palette: the yellow family is
where a light variant breaks first.

## Surfaces

Six surface tones per variant, as **two ladders diverging from `base`**:

- shadow: `base` → `mantle` → `crust`, for sunken chrome — title bars,
  status bars, the tab strip
- elevation: `base` → `surface0` → `surface1` → `surface2`, for raised or
  active things — the current line, selections, borders, popovers

They are not one monotone chain. In the light variant `mantle` (`#f0f0f0`)
is *lighter* than `surface0` (`#ececec`), and `crust` (`#e4e4e4`) sits
between `surface0` and `surface1`. Any code that assumes a single ordering
of the six will be wrong; `--verify` asserts each ladder separately.

## Text

Four tones, all measured against `base`:

- `bright` — headings and emphasis, maximum contrast
- `fg` — body text, around 10:1 (rather than the 16:1 a pure white would
  give, which is what makes long reading sessions comfortable)
- `subtext` — comments and de-emphasized output, around 6:1
- `faint` — line numbers and inlay hints, around 5:1

`subtext` at 6:1 is the deliberate part. Comments have to be legible — a
comment you cannot read is worse than no comment — but they should recede
behind the code. 6:1 clears AA with room to spare while staying visibly
quieter than `fg`.

`faint` was originally `#8a8a8a` / `#6e6e6e`. Both failed the check against
`surface0`, meaning line numbers on the *current line* dropped below AA even
though they passed on the plain background. Nudged to `#8c8c8c` / `#6a6a6a`.

## Why the checks are data

The rules live in `palette.toml` under `[[contrast.rules]]`,
`[contrast.separation]` and `[ansi.constraints]`, and `--verify` refuses to
generate from a palette that breaks them.

The point is that accessibility is the whole reason this palette exists, and
palettes get retuned. Two of the values above — the `faint` nudge and the
yellow/amber split — were found by the checker, not by eye. Without them the
scheme would have shipped with line numbers and light-mode diff colors that
looked fine and measured badly.
