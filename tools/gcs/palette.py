"""Load palette.toml and resolve token references.

A `Variant` is the unit every emitter works with: it knows its surfaces, text
tones, accents, resolved semantic roles and ANSI table for one flavor. Token
references like "accents.pink" or "surfaces.base" are resolved here so no
emitter ever parses a string.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field, replace
from pathlib import Path

ANSI_SLOTS = tuple(range(16))


@dataclass(frozen=True)
class Role:
    """A semantic role resolved against one variant."""

    name: str
    color: str  # hex
    token: str  # the token name it came from, e.g. "orange"
    style: str = ""  # "", "italic", "bold", "underline", "strikethrough"

    @property
    def italic(self) -> bool:
        return "italic" in self.style

    @property
    def bold(self) -> bool:
        return "bold" in self.style

    @property
    def underline(self) -> bool:
        return "underline" in self.style

    @property
    def strikethrough(self) -> bool:
        return "strikethrough" in self.style


@dataclass(frozen=True)
class Variant:
    name: str  # "dark" | "light"
    flavor: str  # "dim" | "vivid"
    id: str  # "grafana-dark"
    label: str  # "Grafana Dark"
    appearance: str  # "dark" | "light"
    surfaces: dict[str, str]
    text: dict[str, str]
    accents: dict[str, str]
    browser: dict[str, str]
    roles: dict[str, Role]
    diagnostic: dict[str, Role]
    diff: dict[str, Role]
    ansi_colors: dict[int, str]
    terminal: dict[str, str]
    derivation: dict[str, str]

    @property
    def is_dark(self) -> bool:
        return self.appearance == "dark"

    def color(self, token: str) -> str:
        """Resolve a bare token name or a dotted reference to a hex value."""
        return _resolve(token, self)

    def role(self, name: str) -> Role:
        return self.roles[name]

    def rc(self, name: str) -> str:
        """Shorthand: the hex color of a role."""
        return self.roles[name].color

    def ansi(self) -> dict[int, str]:
        return self.ansi_colors

    def contrast_on_base(self, hex_color: str) -> float:
        from . import color as C

        return C.contrast(hex_color, self.surfaces["base"])


@dataclass(frozen=True)
class Palette:
    scheme: dict
    brand: dict
    variants: dict[tuple[str, str], Variant]
    contrast_rules: list[dict]
    separation: dict
    ansi_constraints: dict
    targets: dict
    schema_version: int
    source: Path = field(default=Path("palette.toml"))

    @property
    def slug(self) -> str:
        return self.scheme["slug"]

    @property
    def name(self) -> str:
        return self.scheme["name"]

    @property
    def flavors(self) -> list[str]:
        return list(self.scheme["flavors"])

    def variant(self, name: str, flavor: str = "dim") -> Variant:
        return self.variants[name, flavor]

    def each(self, flavor: str = "dim"):
        """(variant_name, Variant) in declared order."""
        for name in self.scheme["variants"]:
            yield name, self.variant(name, flavor)

    def brand_hex(self, name: str) -> str:
        return self.brand["colors"][name]["hex"]

    def target_pin(self, slug: str, key: str, default=None):
        return self.targets.get(slug, {}).get(key, default)


_GROUPS = ("accents", "surfaces", "text", "browser")


def _resolve(ref: str, v: Variant) -> str:
    """"#aabbcc" -> itself. "accents.pink" -> that value. "pink" -> searched."""
    if ref.startswith("#"):
        return ref
    if "." in ref:
        group, _, key = ref.partition(".")
        table = getattr(v, group, None)
        if table is None or key not in table:
            raise KeyError(f"{v.name}: cannot resolve {ref!r}")
        return table[key]
    for group in _GROUPS:
        table = getattr(v, group)
        if ref in table:
            return table[ref]
    raise KeyError(f"{v.name}: unknown token {ref!r}")


def _build_roles(spec: dict, v_partial: Variant) -> dict[str, Role]:
    out: dict[str, Role] = {}
    for name, body in spec.items():
        if not isinstance(body, dict) or "color" not in body:
            continue
        token = body["color"]
        out[name] = Role(
            name=name,
            color=_resolve(token, v_partial),
            token=token,
            style=body.get("style", ""),
        )
    return out


def _ansi_table(raw: dict, v_partial: Variant) -> dict[int, str]:
    return {int(key): _resolve(ref, v_partial) for key, ref in raw.items()}


def load(path: Path | str = "palette.toml") -> Palette:
    path = Path(path)
    with path.open("rb") as fh:
        raw = tomllib.load(fh)

    variants: dict[tuple[str, str], Variant] = {}
    for name in raw["scheme"]["variants"]:
        vraw = raw["variants"][name]
        for flavor in raw["scheme"]["flavors"]:
            # Vivid is a complete snapshot: no reading colors fall back to dim.
            colors = vraw if flavor == "dim" else vraw[flavor]
            stub = Variant(
                name=name,
                flavor=flavor,
                id=vraw["id"],
                label=vraw["label"],
                appearance=vraw["appearance"],
                surfaces=dict(colors["surfaces"]),
                text=dict(colors["text"]),
                accents=dict(colors["accents"]),
                browser=dict(vraw["browser"]),
                roles={}, diagnostic={}, diff={}, ansi_colors={}, terminal={},
                derivation=dict(colors.get("derivation", {})),
            )
            roles_raw = raw["roles"]
            variants[name, flavor] = replace(
                stub,
                roles=_build_roles(roles_raw, stub),
                diagnostic=_build_roles(roles_raw.get("diagnostic", {}), stub),
                diff=_build_roles(roles_raw.get("diff", {}), stub),
                ansi_colors=_ansi_table(raw["ansi"][name][flavor], stub),
                terminal={k: _resolve(ref, stub) for k, ref in raw["terminal"].items()},
            )

    return Palette(
        scheme=raw["scheme"],
        brand=raw["brand"],
        variants=variants,
        contrast_rules=list(raw["contrast"]["rules"]),
        separation=dict(raw["contrast"]["separation"]),
        ansi_constraints=dict(raw["ansi"].get("constraints", {})),
        targets=dict(raw.get("targets", {})),
        schema_version=raw["schema_version"],
        source=path,
    )
