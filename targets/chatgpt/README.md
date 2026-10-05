# ChatGPT for macOS

A [CC Theme](https://github.com/quanzhankeji/cc-theme) package for the ChatGPT
macOS desktop app, applied through CC Theme's `mac-codex` adapter. It uses the
same Grafana palette as the other targets and includes separate light and dark
semantic color sets.

The files under this directory are generated from
[`../../palette.toml`](../../palette.toml). The `assets/grafana.webp` file is a
small hand-managed solid-color preview/background asset and is not generated.

## Install

1. Install [CC Theme](https://github.com/quanzhankeji/cc-theme) and confirm
   that its ChatGPT macOS (`mac-codex`) adapter supports your app version.
2. Create the package from this directory:

   ```sh
   cd targets/chatgpt
   zip -r grafana-1.0.0.cctheme family.json unified-theme.json assets
   ```

3. In CC Theme, choose **Import local theme** and select
   `grafana-1.0.0.cctheme`.
4. Apply the imported theme to ChatGPT Desktop.

The package contains no JavaScript, CSS, selectors, or host paths. CC Theme
validates the manifest, source digest, and asset digest before applying it.
This repository does not modify or re-sign the ChatGPT application.

## Compatibility

The target is for ChatGPT Desktop on macOS via CC Theme's `mac-codex` adapter,
not for the ChatGPT website or iOS app. CC Theme's adapter support is versioned;
check its compatibility report when ChatGPT updates.

`family.json` and `unified-theme.json` are generated. Do not edit them by hand;
run `python3 tools/generate.py --target chatgpt` after changing
`palette.toml`.
