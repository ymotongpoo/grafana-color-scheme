"""Color math. sRGB, WCAG relative luminance and contrast, CIE76 delta-E.

Standard library only. Every function takes and returns plain values so the
emitters never need a color object.
"""

from __future__ import annotations

import math
import re

_HEX_RE = re.compile(r"^#[0-9a-f]{6}$")


def parse(hex_color: str) -> tuple[int, int, int]:
    """'#1e1e1e' -> (30, 30, 30). Rejects anything not lowercase 6-digit."""
    if not _HEX_RE.match(hex_color):
        raise ValueError(f"expected lowercase #rrggbb, got {hex_color!r}")
    h = hex_color[1:]
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def format(rgb: tuple[float, float, float]) -> str:
    """(30, 30, 30) -> '#1e1e1e'. Rounds and clamps."""
    return "#" + "".join(f"{max(0, min(255, round(c))):02x}" for c in rgb)


def to_floats(hex_color: str) -> tuple[float, float, float]:
    """'#1e1e1e' -> (0.1176, 0.1176, 0.1176). For iTerm2 plists."""
    return tuple(c / 255 for c in parse(hex_color))  # type: ignore[return-value]


def _linearize(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    """WCAG 2.1 relative luminance."""
    r, g, b = (_linearize(c) for c in parse(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    """WCAG 2.1 contrast ratio. Order-independent, always >= 1."""
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def mix(a: str, b: str, t: float) -> str:
    """Blend `t` of `b` into `a`, linearly in sRGB space.

    sRGB rather than linear-light on purpose: the palette was derived this way
    and the derivation notes in palette.toml quote these ratios.
    """
    ra, rb = parse(a), parse(b)
    return format(tuple(ra[i] * (1 - t) + rb[i] * t for i in range(3)))


def _to_lab(hex_color: str) -> tuple[float, float, float]:
    r, g, b = (_linearize(c) for c in parse(hex_color))
    # sRGB -> CIE XYZ (D65), then normalized by the D65 white point.
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a: str, b: str) -> float:
    """CIE76 delta-E. Crude next to CIEDE2000, but adequate and dependency-free
    for the question we ask of it: did two brand hues collapse into one color."""
    return math.dist(_to_lab(a), _to_lab(b))


def to_rgb_list(hex_color: str) -> list[int]:
    """'#1e1e1e' -> [30, 30, 30]. Chrome manifests want integer arrays."""
    return list(parse(hex_color))
