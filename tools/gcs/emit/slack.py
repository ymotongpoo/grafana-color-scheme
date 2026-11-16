"""Slack sidebar themes.

Not a file format -- a comma-separated hex string pasted into
Preferences > Themes. Slack writes uppercase, no spaces, no alpha, no
3-digit shorthand.

Eight values are the stable, documented form. A ten-value string adding the
top navigation bar also parses in current clients but is poorly documented,
so the .txt ships 8 and the 10-value variant is recorded in the JSON and in
the target README.

A Slack theme is sidebar-only: the message pane, code blocks and composer
are not themeable.

Current clients keep only positions 1, 3, 7 and 8 of the string (system
navigation, selected items, presence, notifications) and choose every text
color themselves. Position 1 fills the workspace rail, the top bar and the
base of the sidebar. Slack keeps its hue but picks its lightness for the
current color mode, lightening it in light mode and darkening it in dark
mode, so a darker or lighter input does not change how bright the frame
looks. Every theme therefore puts the brand orange in position 1 and lets
Slack fit it to the mode. The selected row in position 3 is rendered as
given. Positions 2, 4, 5 and 6 are still written so older clients keep a
sensible theme.
"""

from __future__ import annotations

import json

from ..palette import Palette, Variant

# (slot label, token reference). Order is the wire order and must not change.
SLOTS = (
    ("Column BG", "browser.key"),
    ("Menu BG Hover", "surfaces.surface0"),
    ("Active Item", "accents.orange"),
    ("Active Item Text", "surfaces.base"),
    ("Hover Item", "surfaces.surface1"),
    ("Text Color", "text.fg"),
    ("Active Presence", "accents.green"),
    ("Mention Badge", "accents.pink"),
)
TOP_NAV = (
    ("Top Nav BG", "surfaces.base"),
    ("Top Nav Text", "text.bright"),
)


def _values(v: Variant, include_top_nav: bool) -> list[str]:
    slots = SLOTS + (TOP_NAV if include_top_nav else ())
    return [v.color(ref).upper() for _label, ref in slots]


def emit(p: Palette) -> dict[str, str]:
    files: dict[str, str] = {}
    payload: dict[str, object] = {
        "scheme": p.name,
        "note": (
            "Paste `value` into Slack > Preferences > Themes > custom theme. "
            "Eight values are the documented form; value_with_top_nav adds the "
            "top navigation bar and also parses in current clients."
        ),
        "slots": [label for label, _ in SLOTS],
        "themes": {},
    }

    for _name, v in p.every():
        eight = _values(v, False)
        ten = _values(v, True)
        files[f"{v.id}.txt"] = ",".join(eight) + "\n"
        payload["themes"][v.id] = {  # type: ignore[index]
            "label": v.label,
            "value": ",".join(eight),
            "value_with_top_nav": ",".join(ten),
            "colors": {label: val for (label, _), val in zip(SLOTS, eight)},
        }

    files["themes.json"] = (
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    )
    return files
