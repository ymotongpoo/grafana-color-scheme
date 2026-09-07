"""Load palette.toml and resolve token references.

A `Variant` is the unit every emitter works with: it knows its surfaces, text
tones, accents, resolved semantic roles and its two ANSI tables. Token
references like "accents.pink" or "surfaces.base" are resolved here so no
emitter ever parses a string.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ANSI_SLOTS = tuple(range(16))
# Slots the vivid flavor is allowed to override. Everything else is shared
# with dim, which is what makes "vivid" a six-color delta.
VIVID_SLOTS = (9, 10, 11, 12, 13, 14)


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
    id: str  # "grafana-dark"
    label: str  # "Grafana Dark"
    appearance: str  # "dark" | "light"
    surfaces: dict[str, str]
    text: dict[str, str]
    accents: dict[str, str]
    accents_vivid: dict[str, str]
    roles: dict[str, Role]
    diagnostic: dict[str, Role]
    diff: dict[str, Role]
    ansi_dim: dict[int, str]
    ansi_vivid: dict[int, str]
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

    def ansi(self, flavor: str) -> dict[int, str]:
        return self.ansi_dim if flavor == "dim" else self.ansi_vivid

    def contrast_on_base(self, hex_color: str) -> float:
        from . import color as C

        return C.contrast(hex_color, self.surfaces["base"])


@dataclass(frozen=True)
class Palette:
    scheme: dict
    brand: dict
    variants: dict[str, Variant]
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

    def variant(self, name: str) -> Variant:
        return self.variants[name]

    def each(self):
        """(variant_name, Variant) in declared order."""
        for name in self.scheme["variants"]:
            yield name, self.variants[name]

    def brand_hex(self, name: str) -> str:
        return self.brand["colors"][name]["hex"]

    def target_pin(self, slug: str, key: str, default=None):
        return self.targets.get(slug, {}).get(key, default)


_GROUPS = ("accents", "accents_vivid", "surfaces", "text")


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


def _ansi_table(raw: dict, v_partial: Variant, base: dict[int, str] | None) -> dict[int, str]:
    table: dict[int, str] = dict(base or {})
    for key, ref in raw.items():
        table[int(key)] = _resolve(ref, v_partial)
    return table


def load(path: Path | str = "palette.toml") -> Palette:
    path = Path(path)
    with path.open("rb") as fh:
        raw = tomllib.load(fh)

    variants: dict[str, Variant] = {}
    for name in raw["scheme"]["variants"]:
        vraw = raw["variants"][name]
        # Built in two passes: roles and ANSI tables need a Variant to resolve
        # token references against, so the color tables land first.
        stub = Variant(
            name=name,
            id=vraw["id"],
            label=vraw["label"],
            appearance=vraw["appearance"],
            surfaces=dict(vraw["surfaces"]),
            text=dict(vraw["text"]),
            accents=dict(vraw["accents"]),
            accents_vivid=dict(vraw["accents_vivid"]),
            roles={},
            diagnostic={},
            diff={},
            ansi_dim={},
            ansi_vivid={},
            terminal={},
            derivation=dict(vraw.get("derivation", {})),
        )

        roles_raw = raw["roles"]
        roles = _build_roles(roles_raw, stub)
        diagnostic = _build_roles(roles_raw.get("diagnostic", {}), stub)
        diff = _build_roles(roles_raw.get("diff", {}), stub)

        ansi_dim = _ansi_table(raw["ansi"][name]["dim"], stub, None)
        ansi_vivid = _ansi_table(raw["ansi"][name]["vivid"], stub, ansi_dim)
        terminal = {k: _resolve(ref, stub) for k, ref in raw["terminal"].items()}

        variants[name] = Variant(
            name=name,
            id=stub.id,
            label=stub.label,
            appearance=stub.appearance,
            surfaces=stub.surfaces,
            text=stub.text,
            accents=stub.accents,
            accents_vivid=stub.accents_vivid,
            roles=roles,
            diagnostic=diagnostic,
            diff=diff,
            ansi_dim=ansi_dim,
            ansi_vivid=ansi_vivid,
            terminal=terminal,
            derivation=stub.derivation,
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
