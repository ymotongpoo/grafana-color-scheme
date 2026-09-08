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

So `frame`, `toolbar` and the tab strip all carry the **key color**, and
every piece of text and iconography on top flips to `on_key`:

| variant | key (frame, toolbar) | inactive tabs | on_key | contrast |
|---|---|---|---|---|
| Light | `#ff671d` brand orange | `#f04205` | `#171717` | 6.16:1 |
| Dark | `#c72f07` orange 140% | `#9d250e` | `#ffffff` | 5.47:1 |

The light variant flips to near-black text because white on `#ff671d` is
only 2.8:1 — well under AA. That is why `on_key` is a stored token rather
than something the emitter guesses.

These live in `palette.toml` under `[variants.*.browser]` and are
deliberately **not** the syntax accents. The accents are derived to sit
*quietly* against a code background, which is the opposite of what a browser
frame needs.

The new tab page is the exception: its background is `surfaces.base`, so
what is drawn on it (`ntp_text`, `ntp_link`, `ntp_header`) uses the syntax
accents, which are already contrast-checked against exactly that surface.

## Why no images

A colors-only theme is completely valid. The `theme_frame` family of PNG
bitmaps has fiddly size and tiling expectations and buys nothing for a
palette port, so the frame `tints` are set to the `[-1.0, -1.0, -1.0]` no-op
that stops Chrome auto-tinting anything. `tints.buttons` is driven to the
same light or dark pole as `toolbar_button_icon`, so the two cannot disagree
on platforms that still honour the tint.
