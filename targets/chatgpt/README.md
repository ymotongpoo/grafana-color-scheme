# ChatGPT / Codex for macOS

Codex Theme v1 import strings for the ChatGPT/Codex macOS desktop app. The
files ending in `.codex-theme.txt` are the values to paste into the app's
theme import dialog.

The files under this directory are generated from
[`../../palette.toml`](../../palette.toml). The `assets/grafana.webp` file is a
small hand-managed solid-color preview/background asset and is not generated.

## Direct import

1. Open **Settings > Appearance** in the macOS app.
2. In the **Dark** row, click **Import** and paste the complete contents of
   `grafana-dark.codex-theme.txt`.
3. In the **Light** row, click **Import** and paste the complete contents of
   `grafana-light.codex-theme.txt`.

Do not paste the Markdown fences or the filename. The value must start with
`codex-theme-v1:`. The variant must match the row: dark into Dark, light into
Light.

## CC Theme package

`family.json`, `unified-theme.json`, and `assets/` also form a CC Theme package
for users of the CC Theme adapter. That is a separate installation path from
the direct Codex Theme v1 import above.

## Compatibility

The direct import target is for the macOS desktop app, not the ChatGPT website
or iOS app. The import format is the app's `codex-theme-v1` format and is
separate from CLI TextMate themes.

All JSON and `.codex-theme.txt` files are generated. Do not edit them by hand;
run `python3 tools/generate.py --target chatgpt` after changing `palette.toml`.
