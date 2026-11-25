"""The target registry.

Adding a target is: write `emit/<slug>.py` with one `emit(palette) -> dict`,
then add one Target line here. The README install matrix and `--list` both
read this table, so nothing else in the repo needs to know how many targets
exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .emit import (
    chatgpt,
    chroma,
    chrome,
    emacs,
    herdr,
    iterm2,
    orca,
    slack,
    t3code,
    tmux,
    vim,
    vscode,
    wezterm,
    zed,
)
from .palette import Palette


@dataclass(frozen=True)
class Target:
    slug: str  # directory name under targets/
    display: str  # human name for docs
    emit: Callable[[Palette], dict[str, str]]
    artifacts: str  # what gets produced, for the README matrix
    install: str  # one-line install, for the README matrix
    upstream: str  # where the format is documented
    flavors: bool = True  # False when it ships the default flavor only


TARGETS: dict[str, Target] = {
    t.slug: t
    for t in (
        Target(
            slug="chatgpt",
            display="ChatGPT macOS",
            emit=chatgpt.emit,
            artifacts="4 Codex theme import strings + CC Theme package",
            install="paste the matching `*.codex-theme.txt` string into Codex Settings > Appearance > Import",
            upstream="https://github.com/openai/codex",
        ),
        Target(
            slug="vscode",
            display="VS Code",
            emit=vscode.emit,
            artifacts="extension root with 4 theme files",
            install="symlink `targets/vscode` into `~/.vscode/extensions/`, restart, then pick the theme",
            upstream="https://code.visualstudio.com/api/references/theme-color",
        ),
        Target(
            slug="zed",
            display="Zed",
            emit=zed.emit,
            artifacts="1 theme family (4 themes)",
            install="copy `themes/grafana.json` to `~/.config/zed/themes/`",
            upstream="https://zed.dev/docs/extensions/themes",
        ),
        Target(
            slug="t3code",
            display="T3 Code",
            emit=t3code.emit,
            artifacts="2 importable theme files, each with light and dark appearances",
            install="Settings → Appearance → Import theme, then choose `grafana.json` or `grafana-dim.json`",
            upstream="https://github.com/pingdotgg/t3code/blob/main/docs/user/appearance.md#custom-themes",
        ),
        Target(
            slug="orca",
            display="Orca IDE",
            emit=orca.emit,
            artifacts="1 plugin with 4 app/editor and 4 terminal themes",
            install="run `orca plugin install ./targets/orca` on Orca Desktop, then pick the theme",
            upstream="https://github.com/stablyai/orca/blob/v1.4.273/docs/reference/plugin-themes.md",
        ),
        Target(
            slug="emacs",
            display="Emacs",
            emit=emacs.emit,
            artifacts="4 theme files",
            install="add the directory to `custom-theme-load-path`, then `(load-theme 'grafana-dark t)`",
            upstream="https://www.gnu.org/software/emacs/manual/html_node/elisp/Custom-Themes.html",
        ),
        Target(
            slug="vim",
            display="Vim / Neovim",
            emit=vim.emit,
            artifacts="4 colorschemes",
            install="add `targets/vim` to `runtimepath`, then `:colorscheme grafana-dark`",
            upstream="https://vimhelp.org/syntax.txt.html",
        ),
        Target(
            slug="wezterm",
            display="WezTerm",
            emit=wezterm.emit,
            artifacts="4 TOML schemes",
            install="copy `colors/*.toml` to `~/.config/wezterm/colors/`, then set `color_scheme`",
            upstream="https://wezterm.org/config/appearance.html",
        ),
        Target(
            slug="iterm2",
            display="iTerm2",
            emit=iterm2.emit,
            artifacts="4 color presets",
            install="Settings > Profiles > Colors > Color Presets > Import",
            upstream="https://iterm2.com/documentation-preferences-profiles-colors.html",
        ),
        Target(
            slug="tmux",
            display="tmux",
            emit=tmux.emit,
            artifacts="4 themes, optional status lines, TPM entry point",
            install="`source-file` the conf from `~/.tmux.conf`, or install via TPM",
            upstream="https://man.openbsd.org/tmux#STYLES",
        ),
        Target(
            slug="herdr",
            display="Herdr",
            emit=herdr.emit,
            artifacts="6 config fragments (2 auto-switching)",
            install="paste the `[theme.custom]` block into `~/.config/herdr/config.toml`",
            upstream="https://herdr.dev/docs/config-reference/",
        ),
        Target(
            slug="chroma",
            display="Chroma / Hugo",
            emit=chroma.emit,
            artifacts="4 XML styles, 6 stylesheets",
            install="Hugo: copy a CSS file and set `markup.highlight.noClasses = false`",
            upstream="https://github.com/alecthomas/chroma",
        ),
        Target(
            slug="slack",
            display="Slack",
            emit=slack.emit,
            artifacts="4 sidebar strings",
            install="Preferences > Themes, paste the string into the custom theme field",
            upstream="https://slack.com/help/articles/205166337",
        ),
        Target(
            slug="chrome",
            display="Chrome",
            emit=chrome.emit,
            artifacts="2 unpacked themes",
            install="`chrome://extensions` > Developer mode > Load unpacked",
            upstream="https://developer.chrome.com/docs/extensions/develop/ui/themes",
            flavors=False,
        ),
    )
}


def get(slug: str) -> Target:
    try:
        return TARGETS[slug]
    except KeyError:
        known = ", ".join(sorted(TARGETS))
        raise SystemExit(f"unknown target {slug!r}. known targets: {known}") from None
