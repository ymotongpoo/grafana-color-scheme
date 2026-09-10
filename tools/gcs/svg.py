"""Generated swatch boards.

GitHub does not render inline color chips in README markdown (it does in
issues), so a text table cannot show the palette. An SVG board can, it needs
no external service, and it follows the palette automatically.
"""

from __future__ import annotations

from . import color as C
from .palette import Palette, Variant

CELL_W = 132
CELL_H = 76
PAD = 16
COLS = 5
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _label_on(bg: str) -> str:
    """Pick whichever of near-white / near-black reads better on `bg`."""
    return "#171717" if C.contrast("#171717", bg) >= C.contrast("#f4f4f4", bg) else "#f4f4f4"


def _swatch(x: int, y: int, name: str, hexv: str, sub: str) -> list[str]:
    fg = _label_on(hexv)
    return [
        f'<rect x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" rx="6" fill="{hexv}"/>',
        f'<text x="{x + 10}" y="{y + 24}" font-family="{MONO}" font-size="12" '
        f'font-weight="600" fill="{fg}">{_esc(name)}</text>',
        f'<text x="{x + 10}" y="{y + 43}" font-family="{MONO}" font-size="11" '
        f'fill="{fg}" opacity="0.85">{hexv}</text>',
        f'<text x="{x + 10}" y="{y + 61}" font-family="{MONO}" font-size="10" '
        f'fill="{fg}" opacity="0.7">{_esc(sub)}</text>',
    ]


def _section(title: str, items: list[tuple[str, str, str]], x0: int, y0: int,
             page_fg: str, cols: int = COLS) -> tuple[list[str], int]:
    body = [
        f'<text x="{x0}" y="{y0 + 12}" font-family="{MONO}" font-size="12" '
        f'font-weight="700" fill="{page_fg}" opacity="0.75">{_esc(title)}</text>'
    ]
    y = y0 + 24
    for i, (name, hexv, sub) in enumerate(items):
        col, row = i % cols, i // cols
        body += _swatch(x0 + col * (CELL_W + 8), y + row * (CELL_H + 8), name, hexv, sub)
    rows = (len(items) + cols - 1) // cols
    return body, y + rows * (CELL_H + 8) + 12


def _board(v: Variant) -> str:
    base = v.surfaces["base"]
    page_fg = v.text["fg"]
    width = PAD * 2 + COLS * (CELL_W + 8) - 8

    def ratio(hexv: str) -> str:
        return f"{C.contrast(hexv, base):.2f}:1"

    surfaces = [
        (name, v.surfaces[name], "background" if name == "base" else "surface")
        for name in ("crust", "mantle", "base", "surface0", "surface1", "surface2")
    ]
    text = [(name, v.text[name], ratio(v.text[name])) for name in ("bright", "fg", "subtext", "faint")]
    accents = [(name, hexv, ratio(hexv)) for name, hexv in v.accents.items()]
    ansi_dim = [(f"ansi {i}", v.ansi()[i], ratio(v.ansi()[i])) for i in range(16)]

    body: list[str] = []
    y = PAD + 16
    body.append(
        f'<text x="{PAD}" y="{PAD + 6}" font-family="{MONO}" font-size="14" '
        f'font-weight="700" fill="{v.text["bright"]}">{_esc(v.label)}</text>'
    )
    for title, items in (
        ("surfaces", surfaces),
        ("text", text),
        ("accents", accents),
        ("ansi 16 (dim)", ansi_dim),
    ):
        chunk, y = _section(title, items, PAD, y, page_fg)
        body += chunk

    height = y + PAD - 12
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{_esc(v.label)} palette swatches">\n'
        f'<rect width="{width}" height="{height}" fill="{base}"/>\n'
        + "\n".join(body)
        + "\n</svg>\n"
    )


def _ansi_board(p: Palette, name: str) -> str:
    """Compare complete flavors on their own backgrounds."""
    cols = 8
    width = PAD * 2 + cols * (CELL_W + 8) - 8
    body: list[str] = []
    y = 0
    for flavor in p.flavors:
        v = p.variant(name, flavor)
        base = v.surfaces["base"]
        table = v.ansi()
        items = [
            (str(i), table[i], f"{C.contrast(table[i], base):.2f}:1") for i in range(16)
        ]
        chunk, end = _section(
            f"{v.label} / {flavor} / background {base}", items,
            PAD, y + PAD, v.text["fg"], cols=cols,
        )
        body.append(f'<rect x="0" y="{y}" width="{width}" height="{end - y}" fill="{base}"/>')
        body.extend(chunk)
        y = end
    label = p.variant(name).label
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{y}" '
        f'viewBox="0 0 {width} {y}" role="img" '
        f'aria-label="{_esc(label)} ANSI palette">\n'
        + "\n".join(body) + "\n</svg>\n"
    )


def emit(p: Palette) -> dict[str, str]:
    files: dict[str, str] = {}
    for _name, v in p.each():
        files[f"palette-{v.name}.svg"] = _board(v)
        files[f"ansi-{v.name}.svg"] = _ansi_board(p, v.name)
    return files
