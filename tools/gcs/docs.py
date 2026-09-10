"""Marker-delimited generated blocks inside hand-written docs.

The prose stays hand-written; only the numbers are generated. That is what
makes it safe to print contrast ratios in the README -- they come from the
resolved colors, so a palette tweak either updates the README in
the same commit or fails --check.

    <!-- BEGIN GENERATED: palette-dark -->
    ...replaced...
    <!-- END GENERATED: palette-dark -->
"""

from __future__ import annotations

import re
from pathlib import Path

from . import color as C
from .palette import Palette, Variant
from .registry import TARGETS

_BLOCK = re.compile(
    r"(?P<begin><!-- BEGIN GENERATED: (?P<name>[a-z0-9-]+) -->\n)"
    r"(?P<body>.*?)"
    r"(?P<end><!-- END GENERATED: \2 -->)",
    re.DOTALL,
)

# Where each accent came from, for the README's provenance column. Kept here
# rather than in palette.toml because it is documentation of documentation.
_ORIGIN_DARK = {
    "orange": "orange 80%",
    "amber": "amber",
    "yellow": "yellow 100%",
    "green": "light green",
    "light-green": "green 80%",
    "light-blue": "light blue",
    "blue": "blue 60%",
    "indigo": "indigo",
    "purple": "purple 60%",
    "pink": "pink",
}
_ORIGIN_LIGHT = {
    "orange": "orange 140%",
    "amber": "yellow 180%",
    "yellow": "yellow",
    "green": "green 140%",
    "light-green": "green 180%",
    "light-blue": "light blue",
    "blue": "blue 140%",
    "indigo": "indigo",
    "purple": "purple 140%",
    "pink": "pink",
}

_ROLE_ORDER = (
    "keyword", "keyword-ctrl", "keyword-op", "operator", "builtin", "decorator",
    "string", "string-doc", "string-escape", "regex",
    "number", "boolean", "constant",
    "type", "class", "namespace", "interface",
    "function", "method", "variable", "parameter", "property", "attribute",
    "tag", "label", "preprocessor", "punctuation",
    "comment", "comment-doc", "link", "heading", "deprecated",
)


def _table(rows: list[list[str]], header: list[str]) -> str:
    widths = [max(len(h), *(len(r[i]) for r in rows)) if rows else len(h)
              for i, h in enumerate(header)]
    out = ["| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(header)) + " |"]
    out.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for r in rows:
        out.append("| " + " | ".join(r[i].ljust(widths[i]) for i in range(len(header))) + " |")
    return "\n".join(out)


def _brand_block(p: Palette) -> str:
    groups = {"primary": [], "secondary": [], "support": [], "neutral": []}
    for name, body in p.brand["colors"].items():
        groups[body["group"]].append((name, body["hex"]))
    rows = []
    for group in ("primary", "secondary", "support", "neutral"):
        for name, hexv in groups[group]:
            rows.append([f"`{name}`", f"`{hexv}`", group])
    return _table(rows, ["brand color", "hex", "group"])


def _ladder_block(p: Palette) -> str:
    ladders = p.brand["ladders"]
    steps = ["20", "40", "60", "80", "100", "120", "140", "160", "180"]
    rows = []
    for hue, values in ladders.items():
        rows.append([f"`{hue}`"] + [f"`{values[s]}`" for s in steps])
    return _table(rows, ["hue"] + [f"{s}%" for s in steps])


def _variant_block(p: Palette, v: Variant) -> str:
    base = v.surfaces["base"]
    origins = _ORIGIN_DARK if v.is_dark else _ORIGIN_LIGHT
    rows = []
    for name, hexv in v.accents.items():
        rows.append(
            [
                f"`{name}`",
                f"`{hexv}`",
                origins.get(name, "-") + "; hand-muted",
                f"{C.contrast(hexv, base):.2f}:1",
            ]
        )
    return _table(rows, ["token", "hex", "brand origin", f"contrast on `{base}`"])


def _surfaces_block(p: Palette) -> str:
    dark, light = p.variant("dark"), p.variant("light")
    rows = []
    for name in ("crust", "mantle", "base", "surface0", "surface1", "surface2"):
        rows.append([f"`{name}`", f"`{dark.surfaces[name]}`", f"`{light.surfaces[name]}`"])
    for name in ("bright", "fg", "subtext", "faint"):
        rows.append(
            [
                f"`{name}`",
                f"`{dark.text[name]}` ({C.contrast(dark.text[name], dark.surfaces['base']):.2f}:1)",
                f"`{light.text[name]}` ({C.contrast(light.text[name], light.surfaces['base']):.2f}:1)",
            ]
        )
    return _table(rows, ["token", "dark", "light"])


def _roles_block(p: Palette) -> str:
    dark, light = p.variant("dark"), p.variant("light")
    rows = []
    for name in _ROLE_ORDER:
        role = dark.roles[name]
        rows.append(
            [
                f"`{name}`",
                f"`{role.token}`",
                f"`{role.color}`",
                f"`{light.roles[name].color}`",
                role.style or "-",
            ]
        )
    for label, group in (("error", "error"), ("warning", "warning"), ("info", "info"),
                         ("hint", "hint"), ("ok", "ok")):
        d = dark.diagnostic[group]
        rows.append(
            [f"`diagnostic.{label}`", f"`{d.token}`", f"`{d.color}`",
             f"`{light.diagnostic[group].color}`", d.style or "-"]
        )
    for label in ("added", "removed", "changed"):
        d = dark.diff[label]
        rows.append(
            [f"`diff.{label}`", f"`{d.token}`", f"`{d.color}`",
             f"`{light.diff[label].color}`", d.style or "-"]
        )
    return _table(rows, ["role", "token", "dark", "light", "style"])


def _ansi_block(p: Palette) -> str:
    dark, light = p.variant("dark"), p.variant("light")
    names = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
    rows = []
    for i in range(16):
        label = names[i % 8] if i < 8 else f"bright {names[i % 8]}"
        rows.append(
            [
                str(i),
                label,
                f"`{dark.ansi()[i]}`",
                f"`{p.variant('dark', 'vivid').ansi()[i]}`",
                f"`{light.ansi()[i]}`",
                f"`{p.variant('light', 'vivid').ansi()[i]}`",
            ]
        )
    return _table(rows, ["slot", "name", "dark dim", "dark vivid", "light dim", "light vivid"])


def _install_block(p: Palette) -> str:
    rows = []
    for slug, t in TARGETS.items():
        rows.append(
            [
                t.display,
                f"[`targets/{slug}`](targets/{slug})",
                t.artifacts + (" (+ vivid)" if t.flavors else ""),
                t.install,
            ]
        )
    return _table(rows, ["tool", "files", "artifacts", "install"])


def _targets_index(p: Palette) -> str:
    rows = []
    for slug, t in TARGETS.items():
        rows.append([t.display, f"[`{slug}/`]({slug}/)", t.artifacts, f"[format]({t.upstream})"])
    return _table(rows, ["tool", "directory", "artifacts", "reference"])


def _blocks(p: Palette) -> dict[str, str]:
    return {
        "brand": _brand_block(p),
        "ladders": _ladder_block(p),
        "palette-dark": _variant_block(p, p.variant("dark")),
        "palette-light": _variant_block(p, p.variant("light")),
        "surfaces": _surfaces_block(p),
        "roles": _roles_block(p),
        "ansi": _ansi_block(p),
        "install": _install_block(p),
        "targets-index": _targets_index(p),
    }


def emit(p: Palette, root: Path) -> dict[Path, str]:
    """Rewrite generated blocks in place. Missing files are skipped so the
    prose can be authored before the first generate run."""
    blocks = _blocks(p)
    out: dict[Path, str] = {}
    for rel in ("README.md", "targets/README.md", "docs/roles.md", "docs/derivation.md"):
        path = root / rel
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")

        def replace(m: re.Match[str]) -> str:
            name = m.group("name")
            if name not in blocks:
                raise SystemExit(f"{rel}: unknown generated block {name!r}")
            return m.group("begin") + blocks[name] + "\n" + m.group("end")

        updated = _BLOCK.sub(replace, original)
        if updated != original:
            out[path] = updated
    return out
