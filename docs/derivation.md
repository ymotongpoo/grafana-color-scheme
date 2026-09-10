# Derivation

## Reading palette

The default dim palette combines warm gray surfaces with softened Grafana
hues. [Nord](https://www.nordtheme.com/docs/colors-and-palettes/) is the
reference for its muted pastel accents. The background has an orange tint
rather than Nord's blue tint, and Grafana's semantic color assignments remain:
orange keywords, green strings, blue types, purple functions, and pink errors.

Dark uses `#241f1c` as its base. Light uses `#e8e1d9`. The foreground,
comments, emphasis, and accents were selected together by visual comparison.
They are not constrained to a minimum contrast ratio. In particular, the
light palette no longer darkens accents until they meet WCAG AA.

The resolved hex values in `palette.toml` are authoritative. The generator
never retunes them. The brand tables retain the original Grafana colors;
only the reading palette is softened. Chrome has independent browser tokens
and retains its existing colors and contrast rules.

## Surfaces and text

Two surface ladders diverge from `base`:

- Shadow: `base` → `mantle` → `crust`, for tab strips and status bars.
- Elevation: `base` → `surface0` → `surface1` → `surface2`, for current
  lines, selections, borders, and popovers.

Each ladder is monotone; the six surfaces do not form a single sequence.
`bright` is emphasis, `fg` is body text, `subtext` is comments and punctuation,
and `faint` is line numbers and secondary UI text.

## Terminal flavors

Dim shares its palette with the editor themes. ANSI slots 9–14 are derived
by mixing each corresponding normal color 8% toward `text.fg` in sRGB,
then storing the rounded hex value. This gently emphasizes bright colors
without returning to the saturated brand originals. Light slot 15 uses
`#efe8e0` instead of pure white.

Vivid preserves the previous unsuffixed theme in full, including backgrounds,
text, accents, UI colors, and all ANSI slots. Its tokens are stored separately
so future dim tuning cannot change Vivid's appearance. Both flavors resolve
the shared semantic and terminal role references against their own tokens.
The old Vivid palette of undimmed brand brights is replaced. Existing theme
names and filenames are retained in WezTerm and iTerm2.

## Verification

The verifier checks both flavors for color syntax, role references and styles,
complete ANSI tables, distinct slot 0 and background, monotone surface
ladders, and at least CIE76 ΔE 8 between accents. Contrast is reported for
reference; only the independent browser tokens retain minimum contrast rules.

Vim's cterm fallback selects the nearest fixed xterm color (indices 16–255)
using CIE76 distance, with ties resolved to the smaller index. Its reduced
palette approximates the truecolor theme without assuming the user's first
16 terminal colors.
