"""T3 Code custom theme files.

Each file is a ThemeFile v1 import with both light and dark appearances.
The default and Vivid flavors are separate themes so they stay selectable in
T3 Code's theme picker.
"""

from __future__ import annotations

import json

from .. import color as C
from ..palette import Palette, Variant


def _on_color(color: str) -> str:
    """Pick whichever neutral gives readable text on a colored surface."""
    black, white = "#000000", "#ffffff"
    return max((black, white), key=lambda foreground: C.contrast(foreground, color))


def _tint(v: Variant, color: str, amount: float) -> str:
    """Mix a semantic color into the canvas for an opaque theme surface."""
    return C.mix(v.surfaces["base"], color, amount)


def _colors(v: Variant) -> dict[str, str]:
    s, t = v.surfaces, v.text
    accent = v.rc("keyword")
    link = v.rc("link")
    error = v.diagnostic["error"].color
    warning = v.diagnostic["warning"].color
    info = v.diagnostic["info"].color
    # Match T3 Code's standard status-surface tint for each appearance.
    tint = 0.16 if v.is_dark else 0.08
    sidebar = s["crust"]

    return {
        "canvas": s["base"],
        "chrome": s["mantle"],
        "toolbar": s["base"],
        "toolbarForeground": t["fg"],
        "toolbarBorder": s["surface1"],
        "toolbarControl": s["surface0"],
        "toolbarControlForeground": t["fg"],
        "toolbarControlHover": s["surface1"],
        "surface": s["base"],
        "surfaceRaised": s["surface0"],
        "surfaceOverlay": s["surface1"],
        "text": t["fg"],
        "textMuted": t["subtext"],
        "border": s["surface1"],
        "input": s["surface0"],
        "focus": accent,
        "accent": accent,
        "accentForeground": _on_color(accent),
        "secondary": s["surface0"],
        "secondaryForeground": t["fg"],
        "muted": s["mantle"],
        "mutedForeground": t["subtext"],
        "placeholder": t["faint"],
        "secondaryLabel": t["subtext"],
        "iconMuted": t["subtext"],
        "error": error,
        "errorForeground": error,
        "errorSurface": _tint(v, error, tint),
        "warning": warning,
        "warningForeground": warning,
        "warningSurface": _tint(v, warning, tint),
        "update": info,
        "updateForeground": info,
        "updateSurface": _tint(v, info, tint),
        "accentSurface": _tint(v, accent, tint),
        "accentSurfaceForeground": t["fg"],
        "messageSurface": s["surface0"],
        "messageForeground": t["fg"],
        "messageAction": link,
        "messageActionForeground": _on_color(link),
        "messageActionHover": link,
        "codeBackground": s["base"],
        "codeForeground": t["fg"],
        "searchMatchBackground": _tint(v, warning, 0.25),
        "searchMatchForeground": t["fg"],
        "searchMatchActiveBackground": warning,
        "searchMatchActiveForeground": _on_color(warning),
        "sidebar": sidebar,
        "sidebarForeground": t["fg"],
        "sidebarMutedForeground": t["subtext"],
        "sidebarControlSurface": s["surface0"],
        "sidebarRowHover": C.mix(sidebar, s["surface0"], 0.5),
        "sidebarRowActive": s["surface1"],
        "sidebarRowSelected": _tint(v, accent, tint),
        "sidebarBorder": s["surface1"],
        "terminalBackground": s["base"],
        "terminalForeground": t["fg"],
        "terminalCursor": v.terminal["cursor_bg"],
        "terminalSelection": v.terminal["selection_bg"],
        "terminalScrollbar": s["surface1"],
        "terminalScrollbarHover": s["surface2"],
    }


def _theme(p: Palette, flavor: str, theme_id: str, theme_name: str) -> dict[str, object]:
    appearances = {mode: _colors(p.variant(mode, flavor)) for mode in ("light", "dark")}
    return {
        "version": 1,
        "id": theme_id,
        "name": theme_name,
        "appearance": "light",
        "colors": appearances["light"],
        "variants": {"dark": appearances["dark"]},
    }


def emit(p: Palette) -> dict[str, str]:
    """Return the importable dim and Vivid T3 Code theme files."""
    out: dict[str, str] = {}
    default_flavor = p.scheme["default_flavor"]
    flavors = [default_flavor, *(flavor for flavor in p.flavors if flavor != default_flavor)]
    for flavor in flavors:
        suffix = "" if flavor == default_flavor else f"-{flavor}"
        theme_id = f"grafana{suffix}"
        theme_name = "Grafana" if flavor == default_flavor else f"Grafana {flavor.title()}"
        out[f"grafana{suffix}.json"] = (
            json.dumps(
                _theme(p, flavor, theme_id, theme_name),
                indent=2,
                ensure_ascii=False,
                sort_keys=False,
            )
            + "\n"
        )
    return out
