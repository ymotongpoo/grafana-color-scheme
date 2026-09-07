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
    chroma,
    chrome,
    emacs,
    herdr,
    iterm2,
    slack,
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
    flavors: bool = False  # True when it also ships -vivid files


TARGETS: dict[str, Target] = {
    t.slug: t
    for t in (
        Target(
            slug="vscode",
            display="VS Code",
            emit=vscode.emit,
            artifacts="extension root with 2 theme files",
            install="symlink `targets/vscode` into `~/.vscode/extensions/`, restart, then pick the theme",
            upstream="https://code.visualstudio.com/api/references/theme-color",
        ),
        Target(
            slug="zed",
            display="Zed",
            emit=zed.emit,
            artifacts="1 theme family (both variants)",
            install="copy `themes/grafana.json` to `~/.config/zed/themes/`",
            upstream="https://zed.dev/docs/extensions/themes",
        ),
        Target(
            slug="emacs",
            display="Emacs",
            emit=emacs.emit,
            artifacts="2 theme files",
            install="add the directory to `custom-theme-load-path`, then `(load-theme 'grafana-dark t)`",
            upstream="https://www.gnu.org/software/emacs/manual/html_node/elisp/Custom-Themes.html",
        ),
        Target(
            slug="vim",
            display="Vim / Neovim",
            emit=vim.emit,
            artifacts="2 colorschemes",
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
            flavors=True,
        ),
        Target(
            slug="iterm2",
            display="iTerm2",
            emit=iterm2.emit,
            artifacts="4 color presets",
            install="Settings > Profiles > Colors > Color Presets > Import",
            upstream="https://iterm2.com/documentation-preferences-profiles-colors.html",
            flavors=True,
        ),
        Target(
            slug="tmux",
            display="tmux",
            emit=tmux.emit,
            artifacts="2 themes, optional status line, TPM entry point",
            install="`source-file` the conf from `~/.tmux.conf`, or install via TPM",
            upstream="https://man.openbsd.org/tmux#STYLES",
        ),
        Target(
            slug="herdr",
            display="Herdr",
            emit=herdr.emit,
            artifacts="2 config fragments",
            install="paste the `[theme.custom]` block into `~/.config/herdr/config.toml`",
            upstream="https://herdr.dev/docs/config-reference/",
        ),
        Target(
            slug="chroma",
            display="Chroma / Hugo",
            emit=chroma.emit,
            artifacts="2 XML styles, 3 stylesheets",
            install="Hugo: copy a CSS file and set `markup.highlight.noClasses = false`",
            upstream="https://github.com/alecthomas/chroma",
        ),
        Target(
            slug="slack",
            display="Slack",
            emit=slack.emit,
            artifacts="2 sidebar strings",
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
        ),
    )
}


def get(slug: str) -> Target:
    try:
        return TARGETS[slug]
    except KeyError:
        known = ", ".join(sorted(TARGETS))
        raise SystemExit(f"unknown target {slug!r}. known targets: {known}") from None
