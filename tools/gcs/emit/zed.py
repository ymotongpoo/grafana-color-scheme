"""Zed theme family.

One file carries both variants in a `themes` array, which is how Zed models a
theme family.

Two things Zed will punish you for: colors that need alpha must actually
carry it (border.transparent and ghost_element.background have to be
"#00000000" or you get opaque black), and syntax entries are objects whose
font_weight is a NUMBER, not the string "bold".
"""

from __future__ import annotations

import json

from ..palette import Palette, Variant

TRANSPARENT = "#00000000"


def _a(hex_color: str, aa: str) -> str:
    return f"{hex_color}{aa}"


def _syntax(v: Variant) -> dict[str, dict[str, object]]:
    r = v.rc

    def spec(color: str, *, italic: bool = False, weight: int | None = None) -> dict[str, object]:
        out: dict[str, object] = {"color": color}
        if italic:
            out["font_style"] = "italic"
        if weight is not None:
            out["font_weight"] = weight
        return out

    return {
        "comment": spec(r("comment"), italic=True),
        "comment.doc": spec(r("comment-doc"), italic=True),
        "string": spec(r("string")),
        "string.escape": spec(r("string-escape")),
        "string.regex": spec(r("regex")),
        "string.special": spec(r("string-escape")),
        "string.special.symbol": spec(r("string")),
        "number": spec(r("number")),
        "boolean": spec(r("boolean")),
        "constant": spec(r("constant")),
        "keyword": spec(r("keyword")),
        "operator": spec(r("operator")),
        "punctuation": spec(r("punctuation")),
        "punctuation.bracket": spec(r("punctuation")),
        "punctuation.delimiter": spec(r("punctuation")),
        "punctuation.list_marker": spec(r("keyword")),
        "punctuation.special": spec(r("string-escape")),
        "function": spec(r("function")),
        "function.builtin": spec(r("builtin")),
        "function.method": spec(r("method")),
        "function.definition": spec(r("function")),
        "type": spec(r("type")),
        "type.builtin": spec(r("builtin")),
        "type.interface": spec(r("interface")),
        "constructor": spec(r("class")),
        "variable": spec(r("variable")),
        "variable.special": spec(r("builtin")),
        "variable.parameter": spec(r("parameter")),
        "variable.member": spec(r("property")),
        "property": spec(r("property")),
        "attribute": spec(r("attribute")),
        "tag": spec(r("tag")),
        "label": spec(r("label")),
        "namespace": spec(r("namespace")),
        "preproc": spec(r("preprocessor")),
        "embedded": spec(v.text["fg"]),
        "primary": spec(v.text["fg"]),
        "predictive": spec(v.text["faint"], italic=True),
        "hint": spec(v.text["faint"]),
        "emphasis": spec(r("keyword"), italic=True),
        "emphasis.strong": spec(r("keyword"), weight=700),
        "title": spec(r("heading"), weight=700),
        "link_text": spec(r("link"), italic=True),
        "link_uri": spec(r("link")),
    }


def _style(v: Variant) -> dict[str, object]:
    s, t = v.surfaces, v.text
    accent = v.rc("keyword")
    fn = v.rc("function")
    err = v.diagnostic["error"].color
    warn = v.diagnostic["warning"].color
    info = v.diagnostic["info"].color
    ok = v.diagnostic["ok"].color
    added = v.diff["added"].color
    removed = v.diff["removed"].color
    changed = v.diff["changed"].color

    style: dict[str, object] = {
        "background": s["base"],
        "background.appearance": "opaque",
        "foreground": t["fg"],
        "border": s["surface1"],
        "border.variant": s["surface0"],
        "border.focused": accent,
        "border.selected": accent,
        "border.transparent": TRANSPARENT,
        "border.disabled": s["surface0"],
        "elevated_surface.background": s["mantle"],
        "surface.background": s["mantle"],
        "drop_target.background": _a(fn, "80"),
        "element.background": s["surface0"],
        "element.hover": s["surface1"],
        "element.active": s["surface2"],
        "element.selected": s["surface1"],
        "element.disabled": s["surface0"],
        "ghost_element.background": TRANSPARENT,
        "ghost_element.hover": s["surface0"],
        "ghost_element.active": s["surface1"],
        "ghost_element.selected": s["surface1"],
        "ghost_element.disabled": TRANSPARENT,
        "text": t["fg"],
        "text.muted": t["subtext"],
        "text.placeholder": t["faint"],
        "text.disabled": t["faint"],
        "text.accent": accent,
        "link_text.hover": v.rc("link"),
        "icon": t["fg"],
        "icon.muted": t["subtext"],
        "icon.disabled": t["faint"],
        "icon.placeholder": t["faint"],
        "icon.accent": accent,
        "status_bar.background": s["crust"],
        "title_bar.background": s["crust"],
        "title_bar.inactive_background": s["mantle"],
        "toolbar.background": s["base"],
        "tab_bar.background": s["mantle"],
        "tab.active_background": s["base"],
        "tab.inactive_background": s["mantle"],
        "panel.background": s["mantle"],
        "panel.focused_border": accent,
        "panel.indent_guide": s["surface1"],
        "panel.indent_guide_active": s["surface2"],
        "panel.indent_guide_hover": s["surface2"],
        "pane.focused_border": accent,
        "pane_group.border": s["surface1"],
        "scrollbar.thumb.background": _a(s["surface2"], "80"),
        "scrollbar.thumb.hover_background": _a(s["surface2"], "b3"),
        "scrollbar.thumb.border": TRANSPARENT,
        "scrollbar.track.background": TRANSPARENT,
        "scrollbar.track.border": s["surface0"],
        "editor.foreground": t["fg"],
        "editor.background": s["base"],
        "editor.gutter.background": s["base"],
        "editor.subheader.background": s["mantle"],
        "editor.active_line.background": _a(s["surface0"], "cc"),
        "editor.highlighted_line.background": s["surface0"],
        "editor.line_number": t["faint"],
        "editor.active_line_number": t["fg"],
        "editor.invisible": s["surface2"],
        "editor.wrap_guide": s["surface1"],
        "editor.active_wrap_guide": s["surface2"],
        "editor.indent_guide": s["surface1"],
        "editor.indent_guide_active": s["surface2"],
        "editor.document_highlight.read_background": _a(info, "33"),
        "editor.document_highlight.write_background": _a(s["surface2"], "66"),
        "editor.document_highlight.bracket_background": _a(fn, "33"),
        "search.match_background": _a(warn, "4d"),
        "created": added,
        "created.background": _a(added, "1a"),
        "created.border": added,
        "modified": changed,
        "modified.background": _a(changed, "1a"),
        "modified.border": changed,
        "deleted": removed,
        "deleted.background": _a(removed, "1a"),
        "deleted.border": removed,
        "renamed": info,
        "renamed.background": _a(info, "1a"),
        "renamed.border": info,
        "conflict": accent,
        "conflict.background": _a(accent, "1a"),
        "conflict.border": accent,
        "error": err,
        "error.background": _a(err, "1a"),
        "error.border": err,
        "warning": warn,
        "warning.background": _a(warn, "1a"),
        "warning.border": warn,
        "info": info,
        "info.background": _a(info, "1a"),
        "info.border": info,
        "success": ok,
        "success.background": _a(ok, "1a"),
        "success.border": ok,
        "hidden": t["faint"],
        "hidden.background": TRANSPARENT,
        "hidden.border": s["surface1"],
        "ignored": t["faint"],
        "ignored.background": TRANSPARENT,
        "ignored.border": s["surface1"],
        "predictive": t["faint"],
        "predictive.background": TRANSPARENT,
        "predictive.border": s["surface1"],
        "unreachable": t["faint"],
        "unreachable.background": TRANSPARENT,
        "unreachable.border": s["surface1"],
        "terminal.background": s["base"],
        "terminal.foreground": t["fg"],
        "terminal.bright_foreground": t["bright"],
        "terminal.dim_foreground": t["faint"],
        "terminal.ansi.background": s["base"],
    }

    ansi = v.ansi()
    names = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
    for i, name in enumerate(names):
        style[f"terminal.ansi.{name}"] = ansi[i]
        style[f"terminal.ansi.bright_{name}"] = ansi[i + 8]
    # dim_* are Zed-specific; derive them from the shared surfaces and accents
    # rather than inventing a third ramp.
    for i, name in enumerate(names):
        style[f"terminal.ansi.dim_{name}"] = _a(ansi[i], "b3")

    players = []
    for token in ("keyword", "function", "string", "type", "number", "property",
                  "preprocessor", "regex"):
        color = v.rc(token)
        players.append({"cursor": color, "background": color, "selection": _a(color, "33")})
    style["players"] = players
    style["syntax"] = _syntax(v)
    return style


def emit(p: Palette) -> dict[str, str]:
    family = {
        "$schema": p.target_pin("zed", "schema", "https://zed.dev/schema/themes/v0.2.0.json"),
        "name": p.name,
        "author": p.scheme["author"],
        "themes": [
            {"name": v.label, "appearance": v.appearance, "style": _style(v)}
            for _n, v in p.each()
        ],
    }
    extension = f"""id = "{p.slug}"
name = "{p.name}"
version = "1.0.0"
schema_version = 1
authors = ["{p.scheme['author']}"]
description = "A dim color scheme derived from the Grafana Labs brand palette."
repository = "{p.scheme['homepage']}"
"""
    return {
        "themes/grafana.json": json.dumps(
            family, indent=2, ensure_ascii=False, sort_keys=False
        )
        + "\n",
        "extension.toml": extension,
    }
