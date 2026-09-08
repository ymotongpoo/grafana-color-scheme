"""Chrome browser themes.

A theme is an extension whose manifest contains a `theme` key and no
functional keys -- adding `permissions` or a background script makes Chrome
reject it.

**The key color goes on the frame and the toolbar.** Browser chrome is a
branding surface, not a reading surface. Leaving the frame neutral and only
tinting `toolbar_button_icon` produces a grey browser with oddly colored
icons, which reads as a bug rather than as a theme. So `frame`, `toolbar`
and the tab strip all carry `browser.key`, and every piece of text and
iconography on top of them flips to `browser.on_key`.

Note that `browser.key` is deliberately not one of the syntax accents. The
accents are derived to sit *quietly* against a code background; a browser
frame wants the opposite.

Colors are RGB INTEGER ARRAYS, not hex. Tints are [hue, saturation,
lightness] floats where 0.5 means "unchanged" and -1.0 means "leave this
component alone".

No images: a colors-only theme is completely valid, and PNG frame bitmaps
have fiddly size expectations that buy nothing for a palette port.
"""

from __future__ import annotations

import json
import re

from .. import color as C
from ..palette import Palette, Variant

NO_TINT = [-1.0, -1.0, -1.0]

# json.dumps(indent=2) puts every element of an RGB triple on its own line,
# which turns a 24-color manifest into 200 lines of noise. Collapse arrays
# that hold only numbers back onto one line.
_NUMERIC_ARRAY = re.compile(r"\[\s*(-?\d+(?:\.\d+)?(?:,\s*-?\d+(?:\.\d+)?)*)\s*\]")


def _dumps(obj: object) -> str:
    text = json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False)
    text = _NUMERIC_ARRAY.sub(
        lambda m: "[" + ", ".join(m.group(1).split()).replace(",,", ",") + "]", text
    )
    return text + "\n"

# Every key in Chromium's kOverwritableColorTable that a palette can speak
# to, mapped to a token reference. The `browser.*` group is what puts the
# brand on the frame; `surfaces`/`text` are only used where the surface is
# genuinely a content area (the omnibox and the new tab page).
_COLOR_KEYS: tuple[tuple[str, str], ...] = (
    # The frame: the strip behind the tabs, and the window border.
    ("frame", "browser.key"),
    ("frame_inactive", "browser.key"),
    ("frame_incognito", "browser.key"),
    ("frame_incognito_inactive", "browser.key"),
    # The toolbar. Chrome merges the SELECTED tab into it, so this is also
    # the selected tab's fill -- which is why it takes key_soft, not key.
    ("toolbar", "browser.key_soft"),
    ("toolbar_text", "browser.on_key_soft"),
    ("toolbar_button_icon", "browser.on_key_soft"),
    ("bookmark_text", "browser.on_key_soft"),
    ("tab_text", "browser.on_key_soft"),
    # Unselected tabs take the key color, so the strip reads as one band and
    # the selected tab is the thing that stands out from it.
    ("background_tab", "browser.key"),
    ("background_tab_inactive", "browser.key"),
    ("background_tab_incognito", "browser.key"),
    ("background_tab_incognito_inactive", "browser.key"),
    ("tab_background_text", "browser.on_key"),
    ("tab_background_text_inactive", "browser.on_key"),
    ("tab_background_text_incognito", "browser.on_key"),
    ("tab_background_text_incognito_inactive", "browser.on_key"),
    ("button_background", "browser.key_accent"),
    # Content surfaces, where reading actually happens. The new tab page has
    # its own warm-tinted background rather than surfaces.base, so everything
    # drawn on it is re-checked against ntp_bg by --verify.
    ("omnibox_background", "browser.omnibox_bg"),
    ("omnibox_text", "browser.omnibox_fg"),
    ("ntp_background", "browser.ntp_bg"),
    ("ntp_text", "browser.ntp_fg"),
    ("ntp_link", "browser.ntp_link"),
    ("ntp_header", "browser.ntp_header"),
)


def _manifest(p: Palette, v: Variant) -> str:
    colors = {key: C.to_rgb_list(v.color(ref)) for key, ref in _COLOR_KEYS}

    # `buttons` tints the icon mask. Drive it to the same pole as
    # `toolbar_button_icon`, which sits on key_soft, so the two cannot
    # disagree on platforms that still honour the tint.
    on_key_is_light = C.luminance(v.browser["on_key_soft"]) > 0.5
    body = {
        "manifest_version": 3,
        "name": v.label,
        "version": "1.0.1",
        "description": (
            f"{v.label}, derived from the Grafana Labs brand palette. "
            "Not an official Grafana Labs project."
        ),
        "theme": {
            "colors": colors,
            "tints": {
                "buttons": [-1.0, -1.0, 1.0 if on_key_is_light else 0.0],
                "frame": NO_TINT,
                "frame_inactive": NO_TINT,
                "frame_incognito": NO_TINT,
                "frame_incognito_inactive": NO_TINT,
                "background_tab": NO_TINT,
            },
            "properties": {
                "ntp_background_alignment": "center",
                "ntp_background_repeat": "no-repeat",
                # 1 selects the white wordmark, for a dark new tab page.
                "ntp_logo_alternate": 1 if v.is_dark else 0,
            },
        },
    }
    return _dumps(body)


def emit(p: Palette) -> dict[str, str]:
    return {f"{v.id}/manifest.json": _manifest(p, v) for _n, v in p.each()}
