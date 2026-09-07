# iTerm2

Four presets: `grafana-dark`, `grafana-light`, and a `-vivid` flavor of each
that brightens ANSI slots 9–14 to the undimmed brand colors.

Generated from [`../../palette.toml`](../../palette.toml) — do not edit.

## Install

**Settings → Profiles → Colors → Color Presets… → Import…**, pick the
`.itermcolors` file, then select it by name from the same menu.

The name shown in that menu comes from the **filename**, not from anything
inside the file, so keep the filenames if you want to tell the four apart.

## Notes

- `Color Space` is written explicitly as `sRGB`. When the key is absent
  iTerm2 falls back to `Calibrated` (macOS Generic RGB) for backward
  compatibility, which renders these hexes visibly differently from every
  other file in this repository.
- `Alpha Component` is written for every key. iTerm2 tolerates its absence
  but many third-party converters do not, and `Cursor Guide Color` is
  genuinely translucent (0.25).
- `Bold Color` is set to the `bright` text tone, which only takes effect if
  "Brighten bold text" is enabled in the profile.
- Validate with `plutil -lint grafana-dark.itermcolors`.
