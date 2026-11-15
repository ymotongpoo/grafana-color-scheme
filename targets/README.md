# Targets

Every directory here is generated from [`palette.toml`](../palette.toml).
**Do not edit these files** — edit the palette and run
`python3 tools/generate.py`.

Each directory is shaped the way its tool expects, so you can symlink the
subtree into place rather than copying files one by one.

<!-- BEGIN GENERATED: targets-index -->
| tool          | directory              | artifacts                                                      | reference                                                                                     |
|---------------|------------------------|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| ChatGPT macOS | [`chatgpt/`](chatgpt/) | 4 Codex theme import strings + CC Theme package                | [format](https://github.com/openai/codex)                                                     |
| VS Code       | [`vscode/`](vscode/)   | extension root with 4 theme files                              | [format](https://code.visualstudio.com/api/references/theme-color)                            |
| Zed           | [`zed/`](zed/)         | 1 theme family (4 themes)                                      | [format](https://zed.dev/docs/extensions/themes)                                              |
| T3 Code       | [`t3code/`](t3code/)   | 2 importable theme files, each with light and dark appearances | [format](https://github.com/pingdotgg/t3code/blob/main/docs/user/appearance.md#custom-themes) |
| Emacs         | [`emacs/`](emacs/)     | 4 theme files                                                  | [format](https://www.gnu.org/software/emacs/manual/html_node/elisp/Custom-Themes.html)        |
| Vim / Neovim  | [`vim/`](vim/)         | 4 colorschemes                                                 | [format](https://vimhelp.org/syntax.txt.html)                                                 |
| WezTerm       | [`wezterm/`](wezterm/) | 4 TOML schemes                                                 | [format](https://wezterm.org/config/appearance.html)                                          |
| iTerm2        | [`iterm2/`](iterm2/)   | 4 color presets                                                | [format](https://iterm2.com/documentation-preferences-profiles-colors.html)                   |
| tmux          | [`tmux/`](tmux/)       | 4 themes, optional status lines, TPM entry point               | [format](https://man.openbsd.org/tmux#STYLES)                                                 |
| Herdr         | [`herdr/`](herdr/)     | 6 config fragments (2 auto-switching)                          | [format](https://herdr.dev/docs/config-reference/)                                            |
| Chroma / Hugo | [`chroma/`](chroma/)   | 4 XML styles, 6 stylesheets                                    | [format](https://github.com/alecthomas/chroma)                                                |
| Slack         | [`slack/`](slack/)     | 4 sidebar strings                                              | [format](https://slack.com/help/articles/205166337)                                           |
| Chrome        | [`chrome/`](chrome/)   | 2 unpacked themes                                              | [format](https://developer.chrome.com/docs/extensions/develop/ui/themes)                      |
<!-- END GENERATED: targets-index -->

The per-directory `README.md` files are hand-written and are not regenerated.
