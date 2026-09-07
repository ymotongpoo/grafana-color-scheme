"""iTerm2 color presets (.itermcolors).

An Apple XML plist of NSColor-ish dicts whose components are floats in 0..1.

Two details that bite:

  Color Space must be written explicitly as sRGB. When the key is absent
  iTerm2 falls back to "Calibrated" (macOS Generic RGB) for backward
  compatibility, which renders these hexes visibly differently from every
  other file in this repo.

  The preset name shown in iTerm2's menu comes from the FILENAME, not from
  anything inside the plist, so the four files need distinguishable stems.
"""

from __future__ import annotations

import plistlib

from .. import color as C
from ..palette import Palette, Variant

# Alpha is written for every key. iTerm2 tolerates its absence but many
# third-party converters do not, and Cursor Guide is genuinely translucent.
_GUIDE_ALPHA = 0.25


def _entry(hex_color: str, alpha: float = 1.0) -> dict[str, object]:
    r, g, b = C.to_floats(hex_color)
    return {
        "Alpha Component": alpha,
        "Blue Component": b,
        "Color Space": "sRGB",
        "Green Component": g,
        "Red Component": r,
    }


def _preset(v: Variant, flavor: str) -> bytes:
    ansi = v.ansi(flavor)
    t = v.terminal

    body: dict[str, object] = {}
    for slot in range(16):
        body[f"Ansi {slot} Color"] = _entry(ansi[slot])

    body["Background Color"] = _entry(v.surfaces["base"])
    body["Badge Color"] = _entry(v.diagnostic["error"].color)
    body["Bold Color"] = _entry(v.text["bright"])
    body["Cursor Color"] = _entry(t["cursor_bg"])
    body["Cursor Guide Color"] = _entry(v.surfaces["surface1"], _GUIDE_ALPHA)
    body["Cursor Text Color"] = _entry(t["cursor_fg"])
    body["Foreground Color"] = _entry(v.text["fg"])
    body["Link Color"] = _entry(v.rc("link"))
    # Selection Color is the background; Selected Text Color is the foreground.
    body["Selected Text Color"] = _entry(t["selection_fg"])
    body["Selection Color"] = _entry(t["selection_bg"])
    body["Tab Color"] = _entry(v.surfaces["mantle"])

    return plistlib.dumps(body, fmt=plistlib.FMT_XML, sort_keys=True)


def emit(p: Palette) -> dict[str, str]:
    files: dict[str, str] = {}
    for _name, v in p.each():
        for flavor in p.flavors:
            suffix = "" if flavor == p.scheme["default_flavor"] else f"-{flavor}"
            raw = _preset(v, flavor).decode("utf-8")
            if not raw.endswith("\n"):
                raw += "\n"
            files[f"{v.id}{suffix}.itermcolors"] = raw
    return files
