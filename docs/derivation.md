# Derivation

## Brand flavor

The default flavor exists to look like the Grafana brand. It uses the brand
guide's colors on the brand guide's canvases and does not soften them.

**Dark** sits on Neutral 5 (`#171717`), the dark canvas the brand guide
itself uses. Text is white, Neutral 1, Neutral 2 and Neutral 3, from
brightest to faintest. Every accent is the brand color verbatim: the
primary orange, the four chromatic secondaries, and the five support colors.
All of them read on `#171717`; the lowest is blue at about 4.2:1.

**Light** sits on white, with black and Neutral 5 for text. White is harsher
on pale colors, so accents are chosen in this order:

1. The brand color verbatim, if it reads on white: blue, purple, indigo.
2. Otherwise, a darker step from the brand's own tint and shade ladder:
   orange 120%, green 120%, yellow 160%.
3. Otherwise, the brand color darkened in OKLCH, lowering lightness only
   and keeping hue and chroma: light green, light blue, pink.

Amber is the exception to rule 3. Darkened at its own hue it lands within
ΔE 6 of yellow 160%, so its hue is also nudged about 13° toward orange to
keep the two apart.

The surface ladders are neutral grays stepped from the brand neutrals:
Neutral 4 (`#3a3a3a`) is the top of the dark elevation ladder and Neutral 1
(`#f4f4f4`) is the light `mantle`.

## Dim flavor

Dim is derived from brand, accent by accent, in OKLCH:

    L' = c + (L - c) × 0.45     lightness pulled 55% toward c
    C' = C × 0.6                chroma reduced to 60%
    h' = h                      hue unchanged

with `c = 0.74` on dark and `c = 0.56` on light. Pulling lightness toward a
common level evens out the brand colors' very different brightness (yellow
is far brighter than blue), and the chroma cut takes the saturation down
without turning the hues gray. Colors that fall outside sRGB lose chroma
until they fit.

Dim surfaces move one step off the brand extremes, `#1e1e1e` on dark and
Neutral 1 (`#f4f4f4`) on light, and text moves down from white / up from
black in the same way.

Both flavors share every semantic role, so dim changes how strong each color
is but never which color a token gets.

The computed values are stored as hex in `palette.toml` and are
authoritative; the generator does not recompute them, so any single value
can be hand-tuned. Chrome has independent browser tokens and keeps its
existing colors and contrast rules.

## Surfaces and text

Two surface ladders diverge from `base`:

- Shadow: `base` → `mantle` → `crust`, for tab strips and status bars.
- Elevation: `base` → `surface0` → `surface1` → `surface2`, for current
  lines, selections, borders, and popovers.

Each ladder is monotone; the six surfaces do not form a single sequence.
`bright` is emphasis, `fg` is body text, `subtext` is comments and punctuation,
and `faint` is line numbers and secondary UI text.

## ANSI

Each flavor has its own complete ANSI table. Normal slots 1–6 are the
flavor's pink, green, yellow, blue, purple and light blue. Brand brights
9–14 take the next brand ladder step toward higher contrast where the hue
has a ladder: 80% on dark, and 120%, 140% or 180% on light. Pink and light
blue have no ladder, so their brights move OKLCH lightness by +0.08 (dark)
or −0.07 (light) at the same hue and chroma. Dim brights move the dim
accents by ±0.06 the same way.

## Verification

The verifier checks every variant and flavor for color syntax, role
references and styles, complete ANSI tables, distinct slot 0 and background, monotone surface
ladders, and at least CIE76 ΔE 8 between accents. Contrast is reported for
reference; only the independent browser tokens retain minimum contrast rules.

Vim's cterm fallback selects the nearest fixed xterm color (indices 16–255)
using CIE76 distance, with ties resolved to the smaller index. Its reduced
palette approximates the truecolor theme without assuming the user's first
16 terminal colors.
