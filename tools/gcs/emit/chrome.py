"""Chrome browser themes.

A theme is an extension whose manifest contains a `theme` key and no
functional keys -- adding `permissions` or a background script makes Chrome
reject it.

Colors are RGB INTEGER ARRAYS, not hex. Tints are [hue, saturation,
lightness] floats where 0.5 means "unchanged" and -1.0 means "leave this
component alone"; [-1.0, -1.0, -1.0] is the idiomatic no-op that stops Chrome
auto-tinting a frame.

No images: a colors-only theme is completely valid, and PNG frame bitmaps
have fiddly size expectations that buy nothing for a palette port.
"""

from __future__ import annotations

import json

from .. import color as C
from ..palette import Palette, Variant

NO_TINT = [-1.0, -1.0, -1.0]

# Every key in Chromium's kOverwritableColorTable that a palette can speak to.
_COLOR_KEYS: tuple[tuple[str, str], ...] = (
    ("frame", "surfaces.crust"),
    ("frame_inactive", "surfaces.mantle"),
    ("frame_incognito", "surfaces.crust"),
    ("frame_incognito_inactive", "surfaces.mantle"),
    ("toolbar", "surfaces.mantle"),
    ("tab_text", "text.bright"),
    ("tab_background_text", "text.faint"),
    ("tab_background_text_inactive", "text.faint"),
    ("tab_background_text_incognito", "text.faint"),
    ("tab_background_text_incognito_inactive", "text.faint"),
    ("background_tab", "surfaces.crust"),
    ("background_tab_inactive", "surfaces.crust"),
    ("background_tab_incognito", "surfaces.crust"),
    ("background_tab_incognito_inactive", "surfaces.crust"),
    ("bookmark_text", "text.fg"),
    ("toolbar_text", "text.fg"),
    ("toolbar_button_icon", "accents.orange"),
    ("omnibox_background", "surfaces.surface0"),
    ("omnibox_text", "text.fg"),
    ("button_background", "surfaces.mantle"),
    ("ntp_background", "surfaces.base"),
    ("ntp_text", "text.fg"),
    ("ntp_link", "accents.light-blue"),
    ("ntp_header", "surfaces.surface0"),
)


def _manifest(p: Palette, v: Variant) -> str:
    colors = {key: C.to_rgb_list(v.color(ref)) for key, ref in _COLOR_KEYS}
    body = {
        "manifest_version": 3,
        "name": v.label,
        "version": "1.0.0",
        "description": (
            f"{v.label}, derived from the Grafana Labs brand palette. "
            "Not an official Grafana Labs project."
        ),
        "theme": {
            "colors": colors,
            "tints": {
                "buttons": NO_TINT,
                "frame": NO_TINT,
                "frame_inactive": NO_TINT,
                "frame_incognito": NO_TINT,
                "frame_incognito_inactive": NO_TINT,
                "background_tab": NO_TINT,
            },
            "properties": {
                "ntp_background_alignment": "center",
                "ntp_background_repeat": "no-repeat",
                # 1 selects the white logo, which is what a dark NTP needs.
                "ntp_logo_alternate": 1 if v.is_dark else 0,
            },
        },
    }
    return json.dumps(body, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def emit(p: Palette) -> dict[str, str]:
    return {f"{v.id}/manifest.json": _manifest(p, v) for _n, v in p.each()}
