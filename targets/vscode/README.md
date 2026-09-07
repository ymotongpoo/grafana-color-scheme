# VS Code

This directory is a valid extension root. Both variants are contributed from
one `package.json`.

Generated from [`../../palette.toml`](../../palette.toml) — do not edit.

## Install

Not published to a marketplace (see the trademark note in the root
[NOTICE](../../NOTICE)), so sideload it. Symlinking means `git pull` updates
the theme:

```sh
ln -s "$PWD" ~/.vscode/extensions/grafana-color-scheme
```

For VS Code Insiders use `~/.vscode-insiders/extensions/`, and for
VSCodium `~/.vscode-oss/extensions/`. Restart the editor, then
**Ctrl/Cmd+K Ctrl/Cmd+T** and pick *Grafana Dark* or *Grafana Light*.

To develop against it instead:

```sh
code --extensionDevelopmentPath="$PWD"
```

## Notes

- The theme ids are `grafana-dark` and `grafana-light`; those are the values
  `workbench.colorTheme` stores in your settings.
- `semanticHighlighting` is on and `semanticTokenColors` is populated.
  Without the latter, TypeScript and Rust look inconsistent with everything
  else, because their semantic highlighters override the TextMate scopes.
- All 16 `terminal.ansi*` keys are set from the shared ANSI table, so the
  integrated terminal matches the WezTerm and iTerm2 files in this repo
  exactly.
- Selection and highlight layers use `#RRGGBBAA`, which VS Code supports.

To pin the theme in a workspace:

```jsonc
// .vscode/settings.json
{ "workbench.colorTheme": "grafana-dark" }
```
