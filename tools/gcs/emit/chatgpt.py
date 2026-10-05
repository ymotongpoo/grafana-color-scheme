"""CC Theme package files for the ChatGPT macOS desktop app.

The macOS app is reached through CC Theme's ``mac-codex`` adapter.  This
emitter writes the adapter-neutral source and its integrity manifest; the
background asset is hand-managed under targets/chatgpt/assets/.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..palette import Palette, Variant

ASSET_NAME = "grafana.webp"
ASSET_PATH = Path(__file__).resolve().parents[3] / "targets" / "chatgpt" / "assets" / ASSET_NAME
VERSION = "1.0.0"
MINIMUM_MANAGER_VERSION = "0.1.0"


def _dump(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def _colors(v: Variant) -> dict[str, str]:
    return {
        "surfaceBase": v.surfaces["base"],
        "surfaceRaised": v.surfaces["surface0"],
        "surfaceElevated": v.surfaces["surface1"],
        "surfaceCode": v.surfaces["mantle"],
        "text": v.text["bright"],
        "textStrong": v.text["bright"],
        "textMuted": v.text["bright"],
        "placeholder": v.text["faint"],
        "borderSubtle": v.text["faint"],
        "borderDefault": v.surfaces["surface2"],
        "borderStrong": v.color("blue"),
        "action": v.color("orange"),
        "actionHover": v.rc("keyword-ctrl"),
        "actionPressed": v.rc("keyword-op"),
        "actionForeground": "#171717",
        "hoverSurface": v.surfaces["surface1"],
        "pressedSurface": v.surfaces["surface2"],
        "selectedSurface": v.surfaces["surface2"],
        "selectedHoverSurface": v.color("orange"),
        "focusRing": v.color("blue"),
        "link": v.color("light-blue"),
        "danger": v.diagnostic["error"].color,
        "success": v.diagnostic["ok"].color,
        "warning": v.diagnostic["warning"].color,
        "sidebarSurface": v.surfaces["mantle"],
        "headerSurface": v.surfaces["surface0"],
        "mainScrimStart": v.surfaces["base"],
        "mainScrimMid": v.surfaces["surface0"],
        "mainScrimEnd": v.surfaces["surface1"],
        "composerSurface": v.surfaces["surface0"],
    }


def _theme(p: Palette) -> dict:
    dark = p.variant("dark")
    light = p.variant("light")
    dark_colors = _colors(dark)
    light_colors = _colors(light)
    return {
        "kind": "cc-theme.unified-theme",
        "schemaVersion": 1,
        "id": "grafana",
        "name": "Grafana",
        "version": VERSION,
        "sharedCore": {
            "tokens": {
                "colors": dark_colors,
                "fonts": {
                    "ui": ["SF Pro Text", "system-ui"],
                    "display": ["SF Pro Display", "system-ui"],
                    "code": ["SFMono-Regular", "monospace"],
                },
                "appearance": {
                    "shellMode": "auto",
                    "backdropBlurPx": 0,
                    "backdropSaturation": 1,
                    "radiusScale": 1,
                },
            },
            "background": {
                "mode": "media",
                "image": ASSET_NAME,
                "position": {"xPercent": 50, "yPercent": 50},
            },
            "accessibility": {
                "reducedMotion": "static",
                "minimumTextContrast": 4.5,
                "minimumLargeTextContrast": 3,
                "preserveSystemFocusRing": True,
                "transparencyFallback": "opaque",
            },
            "appearanceVariants": {
                "light": {"colors": light_colors},
                "dark": {"colors": dark_colors},
            },
        },
        "targets": ["mac-codex"],
    }


def emit(p: Palette) -> dict[str, str]:
    theme = _theme(p)
    source = _dump(theme).encode("utf-8")
    asset = ASSET_PATH.read_bytes()
    family = {
        "kind": "cc-theme.theme-family-package",
        "schemaVersion": 1,
        "id": "grafana",
        "version": VERSION,
        "minimumManagerVersion": MINIMUM_MANAGER_VERSION,
        "metadata": {
            "author": "Yoshi Yamaguchi",
            "defaultLocale": "en-US",
            "locales": {
                "zh-CN": {
                    "name": "Grafana",
                    "description": "Grafanaブランドカラーに基づくChatGPT macOSアプリ用テーマ。",
                },
                "en-US": {
                    "name": "Grafana",
                    "description": "A ChatGPT macOS theme derived from the Grafana brand palette.",
                },
            },
            "previewAsset": ASSET_NAME,
            "license": "Apache-2.0",
            "assetLicense": "Apache-2.0",
        },
        "source": {
            "path": "unified-theme.json",
            "bytes": len(source),
            "sha256": hashlib.sha256(source).hexdigest(),
        },
        "assets": [
            {
                "path": f"assets/{ASSET_NAME}",
                "bytes": len(asset),
                "sha256": hashlib.sha256(asset).hexdigest(),
                "contentType": "image/webp",
                "roles": ["background", "preview"],
            }
        ],
    }
    return {
        "unified-theme.json": source.decode("utf-8"),
        "family.json": _dump(family),
    }
