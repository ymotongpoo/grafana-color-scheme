"""Data-only Orca plugin with app, editor and terminal colors."""

from __future__ import annotations

import json

from .. import color as C
from ..palette import Palette, Variant
from .vscode import token_colors


_ANSI_NAMES = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")


def _dumps(obj: object) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def _app(v: Variant) -> dict[str, object]:
    s, t = v.surfaces, v.text
    accent = v.rc("keyword")
    link = v.rc("link")
    # Orca drops app links below 4.5:1. The editor's syntax rules keep the palette color.
    if C.contrast(link, s["base"]) < 4.5:
        link = C.mix(link, t["fg"], 0.25)
    muted = t["subtext"]
    # The same muted text is used on the canvas, muted surfaces and host badges.
    if min(C.contrast(muted, s[key]) for key in ("base", "mantle", "surface1")) < 4.5:
        muted = C.mix(muted, t["fg"], 0.25)
    added, removed = v.diff["added"].color, v.diff["removed"].color

    tokens = {
        "--background": s["base"],
        "--foreground": t["fg"],
        "--editor-surface": s["base"],
        "--card": s["surface0"],
        "--popover": s["surface0"],
        "--primary": accent,
        "--primary-foreground": max(
            ("#000000", "#ffffff"), key=lambda color: C.contrast(color, accent)
        ),
        "--muted": s["mantle"],
        "--muted-foreground": muted,
        "--accent": s["surface1"],
        "--border": s["surface2"],
        "--ring": accent,
        "--sidebar": s["mantle"],
        "--worktree-sidebar": s["crust"],
        "--worktree-sidebar-active": s["surface1"],
        "--tab-bar": s["mantle"],
        "--tab-active": s["base"],
        "--tab-inactive": s["mantle"],
        "--tab-active-indicator": accent,
        "--chat-user-message": s["surface1"],
        "--chat-muted-foreground": muted,
        "--chat-inline-code": s["surface1"],
        "--chat-inline-code-foreground": t["fg"],
        "--chat-code-block": s["surface0"],
        "--text-link": link,
        "--editor-selection": f'{v.rc("function")}44',
        "--diff-added": added,
        "--diff-removed": removed,
        "--git-decoration-added": added,
        "--git-decoration-modified": v.diff["changed"].color,
        "--git-decoration-deleted": removed,
    }
    if not v.is_dark:
        # Light chat and editor surfaces need a subtler tint to keep diff text readable.
        tokens["--diff-added-background"] = f"{added}14"
        for side, hue, tint in (("added", added, 0x14 / 255), ("removed", removed, 0.11)):
            # Orca mixes diff text 30% toward the foreground and paints it over the line tint.
            text = C.mix(hue, t["fg"], 0.30)
            line = C.mix(s["surface0"], hue, tint)
            if C.contrast(text, line) < 4.5:
                tokens[f"--diff-{side}"] = C.mix(hue, t["fg"], 0.20)
    syntax = token_colors(v)
    for rule in syntax:
        # Orca matches single TextMate scopes.
        rule["scope"] = [scope for scope in rule["scope"] if " " not in scope]
        settings = rule["settings"]
        if "foreground" in settings and v.contrast_on_base(settings["foreground"]) < 3:
            del settings["foreground"]

    return {"schemaVersion": 1, "base": v.appearance, "tokens": tokens, "tokenColors": syntax}


def _terminal(v: Variant) -> dict[str, object]:
    terminal = {
        "background": v.surfaces["base"],
        "foreground": v.text["fg"],
        "cursor": v.terminal["cursor_bg"],
        "cursorAccent": v.terminal["cursor_fg"],
        "selectionBackground": v.terminal["selection_bg"],
        "selectionForeground": v.terminal["selection_fg"],
    }
    ansi = v.ansi()
    for index, name in enumerate(_ANSI_NAMES):
        terminal[name] = ansi[index]
        terminal[f"bright{name.title()}"] = ansi[index + 8]
    return {"schemaVersion": 1, "mode": v.appearance, "terminal": terminal}


def emit(p: Palette) -> dict[str, str]:
    files: dict[str, str] = {}
    themes = []
    terminal_themes = []
    for _, v in p.every():
        app_path = f"themes/{v.id}.json"
        terminal_path = f"terminal/{v.id}.json"
        files[app_path] = _dumps(_app(v))
        files[terminal_path] = _dumps(_terminal(v))
        themes.append({"id": v.id, "title": v.label, "path": app_path})
        terminal_themes.append({"id": v.id, "title": v.label, "path": terminal_path})

    files["orca-plugin.json"] = _dumps({
        "manifestVersion": 2,
        "id": "grafana-color-scheme",
        "name": f"{p.name} Color Scheme",
        "version": "0.1.1",
        "description": "Grafana Dark and Light, with Dim variants for the app, editor and terminal.",
        "engines": {"orca": ">=1.4.246"},
        "execution": "data",
        "license": p.scheme["license"],
        "contributes": {"themes": themes, "terminalThemes": terminal_themes},
    })
    return files
