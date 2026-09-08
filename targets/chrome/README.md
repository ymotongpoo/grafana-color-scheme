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
| Dark | `#ff671d` brand orange | `#33261f` warmed base | 90 |

**The key color is the same in both variants.** The brand does not get
duller because someone prefers a dark editor, so `key`, `on_key` and
`key_accent` are identical and only the content surfaces below them flip.
An earlier version used orange 140% for the dark frame and it read as a
brownish orange rather than as Grafana's.

Chrome merges the selected tab into the toolbar, so `key_soft` fills both.
Giving the unselected tabs the key color makes the strip read as one branded
band with the selected tab standing out of it. Two adjacent steps of the same
ramp — which is what this used to be — left the tabs hard to tell apart.

Text flips per surface: `on_key` on the frame and unselected tabs,
`on_key_soft` on the selected tab and toolbar. `on_key` is near-black in
*both* variants, because white on `#ff671d` is only 2.8:1 — well under AA.
That is why these are stored tokens rather than something the emitter
guesses.

The new tab page gets its own warm background (`ntp_bg`): `#fef3e7` on light,
`#251d19` on dark. It is deliberately kept one step away from the toolbar so
the page reads as content rather than as more browser chrome. Everything
drawn on it is re-checked against that surface by `--verify` rather than
against `surfaces.base`.

These live in `palette.toml` under `[variants.*.browser]` and are
deliberately **not** the syntax accents. The accents are derived to sit
*quietly* against a code background, which is the opposite of what a browser
frame needs.

## The Grot on the new tab page

Each theme bundles `images/grot.png`, anchored bottom right on the new tab
page.

**A theme cannot randomize it.** `theme.images` is a static map baked into
the theme pack when the theme is installed, and a theme may not contain a
script — a manifest carrying both `theme` and functional keys is not a theme.
So it is one fixed illustration, not a rotating set. Getting a different Grot
per new tab would need a separate extension that overrides
`chrome_url_overrides.newtab`, which replaces Chrome's own new tab page
(losing the search box and shortcuts).

To swap the artwork, replace `images/grot.png` in **both** theme directories.
Other Grot illustrations:

- <https://grafana.com/media/grot/grafana-grot-error-meteor.svg>
- <https://grafana.com/oss/assets/oss_hero-graphic.svg>

Current Chromium accepts SVG in theme images as well as raster formats
(`IsSupportedExtensionImageMimeType` allows `image/svg+xml` explicitly), even
though the documentation reads as PNG-only. Older Chrome versions may not, so
PNG is the safer choice for something you hand to other people.

`images/` is hand-managed, not generated. `--check` ignores it.

### License

The bundled Grot is **not** Apache-2.0. It is copyright Grafana Labs, used
under CC BY-NC (noncommercial, attribution required) — see the root
[NOTICE](../../NOTICE) for the full carve-out. If you intend any commercial
use, delete `images/` and drop the `theme.images` block from the manifest.

### If the image does not appear

`ntp_background` only affects Chrome's own local new tab page. It is ignored
when a custom new-tab extension is installed, and when the user has chosen a
Google background image or a Chrome color in
`chrome://settings/appearance`.

## Why no frame images

The `theme_frame` family of PNG bitmaps has fiddly size and tiling
expectations and buys nothing for a palette port, so the frame `tints` are set to the `[-1.0, -1.0, -1.0]` no-op
that stops Chrome auto-tinting anything. `tints.buttons` is driven to the
same light or dark pole as `toolbar_button_icon`, so the two cannot disagree
on platforms that still honour the tint.
