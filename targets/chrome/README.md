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

## Why no images

A colors-only theme is completely valid. The `theme_frame` family of PNG
bitmaps has fiddly size and tiling expectations and buys nothing for a
palette port, so the `tints` are all set to the `[-1.0, -1.0, -1.0]` no-op
that stops Chrome auto-tinting anything.
