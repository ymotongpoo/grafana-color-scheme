# Chrome

Two unpacked themes. Colors only, no images.

Generated from [`../../palette.toml`](../../palette.toml) — do not edit.

## Install

`chrome://extensions` → turn on **Developer mode** → **Load unpacked** →
select `grafana-dark/` (the directory containing `manifest.json`).

Applies immediately. To remove it, `chrome://settings/appearance` →
**Reset to default**.

The same manifest works in Edge, Brave, Vivaldi and Opera.

Not published to the Chrome Web Store — see the trademark note in the root
[NOTICE](../../NOTICE).

## Notes

- Only one theme can be active at a time; installing this replaces whatever
  you had.
- Chrome will remind you about developer-mode extensions on each launch.
  That is unavoidable without a Web Store listing.
- Chrome's own dynamic color system overrides parts of an installed theme on
  some platforms, so expect `frame` and `ntp_*` to be honored more faithfully
  than `toolbar` and `omnibox_*`.
- `ntp_*` colors only appear on the local New Tab Page. If you use a custom
  NTP extension or a Google background image they have no effect.
- After editing the manifest you must hit **Reload** on the extension card,
  and often restart the browser before frame changes show.

## The key color, not the accent

Browser chrome is a branding surface, not a reading surface. An earlier
version of this theme left the frame neutral and tinted only
`toolbar_button_icon`, which produced a grey browser with orange icons —
it read as a bug rather than as a theme.

So the frame and the unselected tabs carry the **key color**, and the
selected tab breaks away to `key_soft`:

| variant | key (frame + unselected tabs) | key_soft (selected tab + toolbar) | ΔE |
|---|---|---|---|
| Light | `#ff671d` brand orange | `#fee9d4` orange 20% | 79 |
| Dark | `#c72f07` orange 140% | `#32251e` warmed base | 77 |

Chrome merges the selected tab into the toolbar, so `key_soft` fills both.
Giving the unselected tabs the key color makes the strip read as one branded
band with the selected tab standing out of it. Two adjacent steps of the same
ramp — which is what this used to be — left the tabs hard to tell apart.

Text flips per surface: `on_key` on the frame and unselected tabs,
`on_key_soft` on the selected tab and toolbar. In the light variant both are
near-black, because white on `#ff671d` is only 2.8:1 — well under AA. That is
why these are stored tokens rather than something the emitter guesses.

The new tab page gets its own warm background (`ntp_bg`): `#fef3e7` on light,
`#2c221e` on dark. Everything drawn on it is re-checked against that surface
by `--verify` rather than against `surfaces.base`.

These live in `palette.toml` under `[variants.*.browser]` and are
deliberately **not** the syntax accents. The accents are derived to sit
*quietly* against a code background, which is the opposite of what a browser
frame needs.

## Why no images

A colors-only theme is completely valid. The `theme_frame` family of PNG
bitmaps has fiddly size and tiling expectations and buys nothing for a
palette port, so the frame `tints` are set to the `[-1.0, -1.0, -1.0]` no-op
that stops Chrome auto-tinting anything. `tints.buttons` is driven to the
same light or dark pole as `toolbar_button_icon`, so the two cannot disagree
on platforms that still honour the tint.
