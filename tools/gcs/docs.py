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
_ORIGIN = {
    ("dark", "brand"): {
        "orange": "primary", "yellow": "secondary", "green": "secondary",
        "blue": "secondary", "purple": "secondary", "amber": "support",
        "light-green": "support", "light-blue": "support", "indigo": "support",
        "pink": "support",
    },
    ("light", "brand"): {
        "orange": "orange 120%", "yellow": "yellow 160%", "green": "green 120%",
        "blue": "secondary", "purple": "secondary", "amber": "amber; darkened",
        "light-green": "light green; darkened", "light-blue": "light blue; darkened",
        "indigo": "support", "pink": "pink; darkened",
    },
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


def _variant_block(p: Palette, name: str) -> str:
    v, d = p.variant(name), p.variant(name, "dim")
    base, dbase = v.surfaces["base"], d.surfaces["base"]
    origins = _ORIGIN[name, v.flavor]
    rows = []
    for token, hexv in v.accents.items():
        rows.append(
            [
                f"`{token}`",
                f"`{hexv}`",
                origins.get(token, "-"),
                f"{C.contrast(hexv, base):.2f}:1",
                f"`{d.accents[token]}`",
                f"{C.contrast(d.accents[token], dbase):.2f}:1",
            ]
        )
    return _table(rows, ["token", "brand", "origin", f"on `{base}`", "dim", f"on `{dbase}`"])


def _surfaces_block(p: Palette) -> str:
    cols = [p.variant(n, f) for n in ("dark", "light") for f in p.flavors]
    rows = []
    for name in ("crust", "mantle", "base", "surface0", "surface1", "surface2"):
        rows.append([f"`{name}`"] + [f"`{v.surfaces[name]}`" for v in cols])
    for name in ("bright", "fg", "subtext", "faint"):
        rows.append(
            [f"`{name}`"]
            + [f"`{v.text[name]}` ({C.contrast(v.text[name], v.surfaces['base']):.2f}:1)"
               for v in cols]
        )
    return _table(rows, ["token"] + [f"{v.name} {v.flavor}" for v in cols])


def _roles_block(p: Palette) -> str:
    cols = [p.variant(n, f) for n in ("dark", "light") for f in p.flavors]
    groups = [("", lambda v: v.roles, _ROLE_ORDER),
              ("diagnostic.", lambda v: v.diagnostic, ("error", "warning", "info", "hint", "ok")),
              ("diff.", lambda v: v.diff, ("added", "removed", "changed"))]
    rows = []
    for prefix, table, names in groups:
        for name in names:
            role = table(cols[0])[name]
            rows.append(
                [f"`{prefix}{name}`", f"`{role.token}`"]
                + [f"`{table(v)[name].color}`" for v in cols]
                + [role.style or "-"]
            )
    return _table(rows, ["role", "token"] + [f"{v.name} {v.flavor}" for v in cols] + ["style"])


def _ansi_block(p: Palette) -> str:
    cols = [p.variant(n, f) for n in ("dark", "light") for f in p.flavors]
    names = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
    rows = []
    for i in range(16):
        label = names[i % 8] if i < 8 else f"bright {names[i % 8]}"
        rows.append([str(i), label] + [f"`{v.ansi()[i]}`" for v in cols])
    return _table(rows, ["slot", "name"] + [f"{v.name} {v.flavor}" for v in cols])


def _install_block(p: Palette) -> str:
    rows = []
    for slug, t in TARGETS.items():
        rows.append(
            [
                t.display,
                f"[`targets/{slug}`](targets/{slug})",
                t.artifacts + ("" if t.flavors else " (brand only)"),
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
        "palette-dark": _variant_block(p, "dark"),
        "palette-light": _variant_block(p, "light"),
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
