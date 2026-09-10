"""Palette invariants.

Every check reports EVERY failure rather than stopping at the first, because
tuning a palette one failure per run turns into a long game of whack-a-mole.

The rules themselves live in palette.toml under [[contrast.rules]],
[contrast.separation] and [ansi.constraints]. This module only enforces them.
"""

from __future__ import annotations

import fnmatch
import itertools

from . import color as C
from .palette import ANSI_SLOTS, Palette, Variant


class Problem:
    __slots__ = ("kind", "message")

    def __init__(self, kind: str, message: str) -> None:
        self.kind = kind
        self.message = message

    def __str__(self) -> str:
        return f"{self.kind:10} {self.message}"


_TOKEN_GROUPS = ("surfaces", "text", "accents", "browser")


def _each(p: Palette):
    for flavor in p.flavors:
        for name, v in p.each(flavor):
            yield f"{name}/{flavor}", v


def check_colors(p: Palette) -> list[Problem]:
    problems = []
    for name, v in _each(p):
        for group in _TOKEN_GROUPS:
            for token, value in getattr(v, group).items():
                if group == "browser" and token == "ntp_image":
                    continue
                try:
                    C.parse(value)
                except ValueError as exc:
                    problems.append(Problem("COLOR", f"{name} {group}.{token}: {exc}"))
    return problems


def _expand(pattern: str | list[str], v: Variant) -> list[tuple[str, str]]:
    """"accents.*" -> [("accents.pink", "#e2548e"), ...]"""
    patterns = [pattern] if isinstance(pattern, str) else list(pattern)
    out: list[tuple[str, str]] = []
    for pat in patterns:
        group, _, key = pat.partition(".")
        if group not in _TOKEN_GROUPS:
            raise KeyError(f"contrast rule names unknown group {group!r}")
        for name, hexv in getattr(v, group).items():
            if fnmatch.fnmatch(name, key or "*"):
                out.append((f"{group}.{name}", hexv))
    return out


def check_contrast(p: Palette) -> list[Problem]:
    problems: list[Problem] = []
    for vname, v in _each(p):
        for rule in p.contrast_rules:
            against_ref = rule["against"]
            group, _, key = against_ref.partition(".")
            bg = getattr(v, group)[key]
            minimum = float(rule["min"])
            for token, hexv in _expand(rule["tokens"], v):
                ratio = C.contrast(hexv, bg)
                if ratio + 1e-9 < minimum:
                    problems.append(
                        Problem(
                            "CONTRAST",
                            f"{vname} {token} ({hexv}) on {against_ref} ({bg}): "
                            f"{ratio:.2f} < {minimum:.2f} "
                            f"(short by {minimum - ratio:.2f})",
                        )
                    )
    return problems


def check_separation(p: Palette) -> list[Problem]:
    """Two brand hues mixed toward the same background can land on the same
    color. Pairwise CIE76 catches that; contrast alone never would."""
    problems: list[Problem] = []
    floor = float(p.separation["accent_delta_e_min"])
    for vname, v in _each(p):
        for a, b in itertools.combinations(sorted(v.accents), 2):
            d = C.delta_e(v.accents[a], v.accents[b])
            if d < floor:
                problems.append(
                    Problem(
                        "SEPARATION",
                        f"{vname} accents.{a} ({v.accents[a]}) and accents.{b} "
                        f"({v.accents[b]}): dE {d:.2f} < {floor:.2f}",
                    )
                )
    return problems


def check_ansi(p: Palette) -> list[Problem]:
    problems: list[Problem] = []
    cons = p.ansi_constraints
    for vname, v in _each(p):
        base = v.surfaces["base"]
        table = v.ansi()
        missing = sorted(set(ANSI_SLOTS) - set(table))
        extra = sorted(set(table) - set(ANSI_SLOTS))
        if missing or extra:
            problems.append(
                Problem("ANSI", f"{vname} missing slots {missing}, extra slots {extra}")
            )
            continue
        for slot, hexv in table.items():
            try:
                C.parse(hexv)
            except ValueError as exc:
                problems.append(Problem("ANSI", f"{vname} slot {slot}: {exc}"))
        if cons.get("slot0_not_base") and table[0] == base:
            problems.append(
                Problem(
                    "ANSI",
                    f"{vname} slot 0 equals surfaces.base ({base}); "
                    "`bg=black` would be invisible",
                )
            )
        floor = cons.get("slot8_min_on_base")
        if floor is not None:
            ratio = C.contrast(table[8], base)
            if ratio + 1e-9 < float(floor):
                problems.append(
                    Problem(
                        "ANSI",
                        f"{vname} slot 8 ({table[8]}) on base: "
                        f"{ratio:.2f} < {float(floor):.2f}; dim output would vanish",
                    )
                )
    return problems


def check_roles(p: Palette) -> list[Problem]:
    """Roles resolved at load time, so this catches shape problems rather than
    missing names: an unknown token would already have raised."""
    problems: list[Problem] = []
    valid_styles = {"", "italic", "bold", "underline", "strikethrough"}
    for vname, v in _each(p):
        for group_name, group in (
            ("roles", v.roles),
            ("diagnostic", v.diagnostic),
            ("diff", v.diff),
        ):
            for name, role in group.items():
                parts = set(role.style.split()) if role.style else {""}
                unknown = parts - valid_styles
                if unknown:
                    problems.append(
                        Problem(
                            "ROLE",
                            f"{vname} {group_name}.{name} has unknown style {sorted(unknown)}",
                        )
                    )
                try:
                    C.parse(role.color)
                except ValueError as exc:
                    problems.append(Problem("ROLE", f"{vname} {group_name}.{name}: {exc}"))
    return problems


def check_ladders(p: Palette) -> list[Problem]:
    """Surfaces are two ladders diverging from `base`, not one monotone chain.

    In the light variant `mantle` is lighter than `surface0` and `crust` sits
    between `surface0` and `surface1`, so asserting a single ordering would
    fail on a correct palette.
    """
    problems: list[Problem] = []
    ladders = {"shadow": ["mantle", "crust"], "elevation": ["surface0", "surface1", "surface2"]}
    for vname, v in _each(p):
        base_lum = C.luminance(v.surfaces["base"])
        for ladder, names in ladders.items():
            steps = [("base", base_lum)] + [(n, C.luminance(v.surfaces[n])) for n in names]
            # Direction is set by the first step, then every later step must
            # continue the same way. Which direction is correct differs by
            # variant (dark elevation lightens, light elevation darkens), so
            # the invariant asserted here is monotonicity, not a fixed sign.
            direction = 1 if steps[1][1] > steps[0][1] else -1
            for (prev_name, prev), (name, lum) in zip(steps, steps[1:]):
                if (lum - prev) * direction <= 0:
                    problems.append(
                        Problem(
                            "LADDER",
                            f"{vname} {ladder} ladder is not monotone: "
                            f"surfaces.{name} ({v.surfaces[name]}) does not continue "
                            f"past surfaces.{prev_name}",
                        )
                    )
                prev_name, prev = name, lum
        # A shadow surface that is lighter than base is not a shadow.
        for name in ladders["shadow"]:
            if C.luminance(v.surfaces[name]) >= base_lum:
                problems.append(
                    Problem(
                        "LADDER",
                        f"{vname} surfaces.{name} ({v.surfaces[name]}) is not darker "
                        "than surfaces.base",
                    )
                )
    return problems


def run(p: Palette) -> list[Problem]:
    problems = check_colors(p)
    if problems:
        return problems  # Color math requires valid hex input.
    for check in (check_contrast, check_separation, check_ansi, check_roles, check_ladders):
        problems.extend(check(p))
    return problems


def report(p: Palette) -> tuple[list[Problem], str]:
    problems = run(p)
    if not problems:
        counts = []
        for vname, v in _each(p):
            worst_token, worst = min(
                ((n, C.contrast(h, v.surfaces["base"])) for n, h in v.accents.items()),
                key=lambda kv: kv[1],
            )
            closest = min(
                (
                    (C.delta_e(v.accents[a], v.accents[b]), a, b)
                    for a, b in itertools.combinations(sorted(v.accents), 2)
                ),
            )
            counts.append(
                f"  {vname:5} lowest accent contrast {worst:.2f}:1 ({worst_token}), "
                f"closest pair dE {closest[0]:.1f} ({closest[1]}/{closest[2]})"
            )
        body = "\n".join(counts)
        return [], f"OK  all palette invariants hold\n{body}"
    lines = [str(x) for x in problems]
    kinds = sorted({x.kind for x in problems})
    return problems, "\n".join(lines) + f"\n\n{len(problems)} problem(s): {', '.join(kinds)}"
