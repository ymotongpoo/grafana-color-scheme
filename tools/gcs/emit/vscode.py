"""VS Code color themes.

Two files per variant plus one manifest. `uiTheme` and `path` are the only
required manifest fields, but `id` is emitted too because that is the value
`workbench.colorTheme` persists -- renaming the label later would otherwise
break every user's settings.

semanticHighlighting is enabled and a small semanticTokenColors map is
shipped. With the flag alone, unmatched semantic selectors fall back to the
TextMate scopes, which is visibly inconsistent in TypeScript and Rust where
the semantic highlighter wins.
"""

from __future__ import annotations

import json

from ..palette import Palette, Variant


def _dumps(obj: object) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def _alpha(hex_color: str, aa: str) -> str:
    return f"{hex_color}{aa}"


def _workbench(v: Variant) -> dict[str, str]:
    s, t = v.surfaces, v.text
    accent = v.rc("keyword")
    err = v.diagnostic["error"].color
    warn = v.diagnostic["warning"].color
    info = v.diagnostic["info"].color
    ok = v.diagnostic["ok"].color
    added = v.diff["added"].color
    removed = v.diff["removed"].color
    changed = v.diff["changed"].color
    fn = v.rc("function")

    c: dict[str, str] = {
        # Base
        "focusBorder": accent,
        "foreground": t["fg"],
        "disabledForeground": t["faint"],
        "descriptionForeground": t["subtext"],
        "errorForeground": err,
        "icon.foreground": t["fg"],
        "selection.background": _alpha(fn, "55"),
        "widget.border": s["surface1"],
        "sash.hoverBorder": accent,
        # Editor
        "editor.background": s["base"],
        "editor.foreground": t["fg"],
        "editor.lineHighlightBackground": s["surface0"],
        "editor.selectionBackground": _alpha(fn, "44"),
        "editor.selectionHighlightBackground": _alpha(fn, "26"),
        "editor.wordHighlightBackground": _alpha(info, "26"),
        "editor.wordHighlightStrongBackground": _alpha(info, "3d"),
        "editor.findMatchBackground": _alpha(warn, "66"),
        "editor.findMatchHighlightBackground": _alpha(warn, "33"),
        "editor.hoverHighlightBackground": _alpha(fn, "26"),
        "editor.rangeHighlightBackground": _alpha(s["surface1"], "99"),
        "editorCursor.foreground": v.terminal["cursor_bg"],
        "editorWhitespace.foreground": s["surface2"],
        "editorIndentGuide.background1": s["surface1"],
        "editorIndentGuide.activeBackground1": s["surface2"],
        "editorLineNumber.foreground": t["faint"],
        "editorLineNumber.activeForeground": t["fg"],
        "editorLink.activeForeground": v.rc("link"),
        "editorRuler.foreground": s["surface1"],
        "editorCodeLens.foreground": t["faint"],
        # Editor decorations
        "editorBracketMatch.background": _alpha(fn, "33"),
        "editorBracketMatch.border": fn,
        "editorBracketHighlight.foreground1": v.rc("keyword"),
        "editorBracketHighlight.foreground2": v.rc("function"),
        "editorBracketHighlight.foreground3": v.rc("type"),
        "editorBracketHighlight.foreground4": v.rc("string"),
        "editorBracketHighlight.foreground5": v.rc("number"),
        "editorBracketHighlight.foreground6": v.rc("preprocessor"),
        "editorBracketHighlight.unexpectedBracket.foreground": err,
        "editorError.foreground": err,
        "editorWarning.foreground": warn,
        "editorInfo.foreground": info,
        "editorHint.foreground": t["subtext"],
        "editorGutter.background": s["base"],
        "editorGutter.addedBackground": added,
        "editorGutter.modifiedBackground": changed,
        "editorGutter.deletedBackground": removed,
        "editorOverviewRuler.border": s["surface1"],
        "editorOverviewRuler.errorForeground": err,
        "editorOverviewRuler.warningForeground": warn,
        "editorOverviewRuler.infoForeground": info,
        "editorOverviewRuler.addedForeground": added,
        "editorOverviewRuler.modifiedForeground": changed,
        "editorOverviewRuler.deletedForeground": removed,
        "editorInlayHint.foreground": t["faint"],
        "editorInlayHint.background": _alpha(s["surface0"], "00"),
        # Widgets
        "editorWidget.background": s["mantle"],
        "editorWidget.border": s["surface1"],
        "editorHoverWidget.background": s["mantle"],
        "editorHoverWidget.border": s["surface1"],
        "editorSuggestWidget.background": s["mantle"],
        "editorSuggestWidget.border": s["surface1"],
        "editorSuggestWidget.foreground": t["fg"],
        "editorSuggestWidget.highlightForeground": accent,
        "editorSuggestWidget.selectedBackground": s["surface0"],
        "peekView.border": accent,
        "peekViewEditor.background": s["mantle"],
        "peekViewResult.background": s["mantle"],
        "peekViewTitle.background": s["surface0"],
        # Workbench chrome
        "activityBar.background": s["crust"],
        "activityBar.foreground": t["fg"],
        "activityBar.inactiveForeground": t["faint"],
        "activityBar.border": s["surface1"],
        "activityBar.activeBorder": accent,
        "activityBarBadge.background": accent,
        "activityBarBadge.foreground": s["base"],
        "sideBar.background": s["mantle"],
        "sideBar.foreground": t["fg"],
        "sideBar.border": s["surface1"],
        "sideBarTitle.foreground": t["subtext"],
        "sideBarSectionHeader.background": s["mantle"],
        "sideBarSectionHeader.foreground": t["subtext"],
        "list.activeSelectionBackground": s["surface1"],
        "list.activeSelectionForeground": t["bright"],
        "list.inactiveSelectionBackground": s["surface0"],
        "list.inactiveSelectionForeground": t["fg"],
        "list.focusBackground": s["surface1"],
        "list.focusForeground": t["bright"],
        "list.hoverBackground": s["surface0"],
        "list.hoverForeground": t["fg"],
        "list.highlightForeground": accent,
        "list.errorForeground": err,
        "list.warningForeground": warn,
        "list.dropBackground": _alpha(fn, "33"),
        "tree.indentGuidesStroke": s["surface2"],
        # Tabs
        "tab.activeBackground": s["base"],
        "tab.activeForeground": t["bright"],
        "tab.activeBorderTop": accent,
        "tab.inactiveBackground": s["mantle"],
        "tab.inactiveForeground": t["faint"],
        "tab.border": s["surface1"],
        "tab.hoverBackground": s["surface0"],
        "tab.unfocusedActiveForeground": t["subtext"],
        "editorGroupHeader.tabsBackground": s["mantle"],
        "editorGroupHeader.tabsBorder": s["surface1"],
        "editorGroupHeader.noTabsBackground": s["mantle"],
        "editorGroup.border": s["surface1"],
        "editorGroup.dropBackground": _alpha(fn, "26"),
        # Status and title bars
        "statusBar.background": s["crust"],
        "statusBar.foreground": t["subtext"],
        "statusBar.border": s["surface1"],
        "statusBar.debuggingBackground": v.rc("keyword"),
        "statusBar.debuggingForeground": s["base"],
        "statusBar.noFolderBackground": s["crust"],
        "statusBarItem.hoverBackground": s["surface0"],
        "statusBarItem.remoteBackground": accent,
        "statusBarItem.remoteForeground": s["base"],
        "statusBarItem.errorBackground": err,
        "statusBarItem.errorForeground": s["base"],
        "statusBarItem.warningBackground": warn,
        "statusBarItem.warningForeground": s["base"],
        "titleBar.activeBackground": s["crust"],
        "titleBar.activeForeground": t["fg"],
        "titleBar.inactiveBackground": s["crust"],
        "titleBar.inactiveForeground": t["faint"],
        "titleBar.border": s["surface1"],
        "menu.background": s["mantle"],
        "menu.foreground": t["fg"],
        "menu.selectionBackground": s["surface1"],
        "menu.separatorBackground": s["surface1"],
        "commandCenter.background": s["surface0"],
        "commandCenter.foreground": t["fg"],
        "commandCenter.border": s["surface1"],
        # Panel and terminal
        "panel.background": s["mantle"],
        "panel.border": s["surface1"],
        "panelTitle.activeForeground": t["bright"],
        "panelTitle.activeBorder": accent,
        "panelTitle.inactiveForeground": t["faint"],
        "terminal.foreground": t["fg"],
        "terminal.background": s["base"],
        "terminal.selectionBackground": _alpha(fn, "44"),
        "terminalCursor.foreground": v.terminal["cursor_bg"],
        # Controls
        "button.background": accent,
        "button.foreground": s["base"],
        "button.hoverBackground": v.rc("builtin"),
        "button.secondaryBackground": s["surface1"],
        "button.secondaryForeground": t["fg"],
        "button.secondaryHoverBackground": s["surface2"],
        "input.background": s["surface0"],
        "input.foreground": t["fg"],
        "input.border": s["surface1"],
        "input.placeholderForeground": t["faint"],
        "inputOption.activeBorder": accent,
        "inputValidation.errorBackground": s["mantle"],
        "inputValidation.errorBorder": err,
        "inputValidation.warningBackground": s["mantle"],
        "inputValidation.warningBorder": warn,
        "inputValidation.infoBackground": s["mantle"],
        "inputValidation.infoBorder": info,
        "dropdown.background": s["surface0"],
        "dropdown.foreground": t["fg"],
        "dropdown.border": s["surface1"],
        "badge.background": accent,
        "badge.foreground": s["base"],
        "progressBar.background": accent,
        "scrollbar.shadow": s["crust"],
        "scrollbarSlider.background": _alpha(s["surface2"], "80"),
        "scrollbarSlider.hoverBackground": _alpha(s["surface2"], "b3"),
        "scrollbarSlider.activeBackground": _alpha(accent, "80"),
        "checkbox.background": s["surface0"],
        "checkbox.border": s["surface1"],
        "keybindingLabel.background": s["surface0"],
        "keybindingLabel.foreground": t["fg"],
        "keybindingLabel.border": s["surface1"],
        "keybindingLabel.bottomBorder": s["surface1"],
        # Diff, merge, SCM
        "diffEditor.insertedTextBackground": _alpha(added, "22"),
        "diffEditor.removedTextBackground": _alpha(removed, "22"),
        "diffEditor.border": s["surface1"],
        "merge.currentHeaderBackground": _alpha(fn, "55"),
        "merge.currentContentBackground": _alpha(fn, "26"),
        "merge.incomingHeaderBackground": _alpha(added, "55"),
        "merge.incomingContentBackground": _alpha(added, "26"),
        "merge.border": s["surface1"],
        "gitDecoration.addedResourceForeground": added,
        "gitDecoration.modifiedResourceForeground": changed,
        "gitDecoration.deletedResourceForeground": removed,
        "gitDecoration.untrackedResourceForeground": ok,
        "gitDecoration.ignoredResourceForeground": t["faint"],
        "gitDecoration.conflictingResourceForeground": err,
        "gitDecoration.stageModifiedResourceForeground": changed,
        "gitDecoration.stageDeletedResourceForeground": removed,
        # Quick pick and notifications
        "quickInput.background": s["mantle"],
        "quickInputList.focusBackground": s["surface1"],
        "quickInputList.focusForeground": t["bright"],
        "pickerGroup.border": s["surface1"],
        "pickerGroup.foreground": accent,
        "notifications.background": s["mantle"],
        "notifications.foreground": t["fg"],
        "notifications.border": s["surface1"],
        "notificationCenterHeader.background": s["surface0"],
        "notificationCenterHeader.foreground": t["subtext"],
        "notificationLink.foreground": v.rc("link"),
        "notificationsErrorIcon.foreground": err,
        "notificationsWarningIcon.foreground": warn,
        "notificationsInfoIcon.foreground": info,
        # Misc
        "minimap.background": s["mantle"],
        "minimap.findMatchHighlight": warn,
        "minimap.selectionHighlight": fn,
        "minimap.errorHighlight": err,
        "minimap.warningHighlight": warn,
        "minimapSlider.background": _alpha(s["surface2"], "4d"),
        "minimapSlider.hoverBackground": _alpha(s["surface2"], "80"),
        "minimapGutter.addedBackground": added,
        "minimapGutter.modifiedBackground": changed,
        "minimapGutter.deletedBackground": removed,
        "breadcrumb.foreground": t["faint"],
        "breadcrumb.focusForeground": t["fg"],
        "breadcrumb.activeSelectionForeground": accent,
        "breadcrumbPicker.background": s["mantle"],
        "textLink.foreground": v.rc("link"),
        "textLink.activeForeground": v.rc("function"),
        "textCodeBlock.background": s["surface0"],
        "textBlockQuote.background": s["mantle"],
        "textBlockQuote.border": accent,
        "textPreformat.foreground": v.rc("string"),
        "textSeparator.foreground": s["surface2"],
        "charts.red": err,
        "charts.blue": v.rc("type"),
        "charts.yellow": warn,
        "charts.orange": v.rc("keyword"),
        "charts.green": added,
        "charts.purple": v.rc("function"),
        "charts.foreground": t["fg"],
        "charts.lines": s["surface2"],
        "debugToolBar.background": s["mantle"],
        "debugConsole.infoForeground": info,
        "debugConsole.warningForeground": warn,
        "debugConsole.errorForeground": err,
        "debugConsole.sourceForeground": t["faint"],
        "testing.iconPassed": ok,
        "testing.iconFailed": err,
        "testing.iconQueued": warn,
        "testing.iconSkipped": t["faint"],
        "notebook.cellEditorBackground": s["mantle"],
        "notebook.focusedCellBorder": accent,
        "walkThrough.embeddedEditorBackground": s["mantle"],
        "welcomePage.tileBackground": s["mantle"],
        "welcomePage.progress.background": s["surface1"],
        "extensionButton.prominentBackground": accent,
        "extensionButton.prominentForeground": s["base"],
        "extensionButton.prominentHoverBackground": v.rc("builtin"),
        "ports.iconRunningProcessForeground": ok,
    }

    ansi = v.ansi("dim")
    names = ("Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White")
    for i, name in enumerate(names):
        c[f"terminal.ansi{name}"] = ansi[i]
        c[f"terminal.ansiBright{name}"] = ansi[i + 8]
    return c


def _font_style(*, bold: bool = False, italic: bool = False, underline: bool = False,
                strike: bool = False) -> str:
    bits = []
    if bold:
        bits.append("bold")
    if italic:
        bits.append("italic")
    if underline:
        bits.append("underline")
    if strike:
        bits.append("strikethrough")
    return " ".join(bits)


def _token_colors(v: Variant) -> list[dict]:
    r = v.rc
    out: list[dict] = []

    def add(name: str, scope: list[str], fg: str | None = None, style: str = "") -> None:
        settings: dict[str, str] = {}
        if fg:
            settings["foreground"] = fg
        if style:
            settings["fontStyle"] = style
        out.append({"name": name, "scope": scope, "settings": settings})

    add("Comment", ["comment", "punctuation.definition.comment"], r("comment"), "italic")
    add("Comment doc", ["comment.block.documentation", "string.quoted.docstring"],
        r("comment-doc"), "italic")
    add("String", ["string", "string.quoted", "string.template"], r("string"))
    add("String escape", ["constant.character.escape", "string.regexp constant.character.escape"],
        r("string-escape"))
    add("Regex", ["string.regexp"], r("regex"))
    add("Number", ["constant.numeric"], r("number"))
    add("Boolean and language constant",
        ["constant.language", "constant.language.boolean", "constant.language.null"], r("boolean"))
    add("Constant", ["constant.other", "variable.other.constant", "entity.name.constant"],
        r("constant"))
    add("Keyword", ["keyword", "keyword.other", "storage.modifier"], r("keyword"))
    add("Keyword control", ["keyword.control", "keyword.control.flow"], r("keyword-ctrl"))
    add("Storage type", ["storage.type", "keyword.declaration"], r("keyword"))
    add("Operator", ["keyword.operator"], r("operator"))
    add("Punctuation",
        ["punctuation", "punctuation.separator", "punctuation.terminator",
         "punctuation.definition.parameters", "meta.brace"], r("punctuation"))
    add("Type", ["entity.name.type", "support.type", "storage.type.primitive"], r("type"))
    add("Class", ["entity.name.class", "support.class", "entity.other.inherited-class"], r("class"))
    add("Interface", ["entity.name.type.interface"], r("interface"))
    add("Namespace", ["entity.name.namespace", "entity.name.scope-resolution",
                      "entity.name.type.module"], r("namespace"))
    add("Function", ["entity.name.function", "support.function", "meta.function-call"],
        r("function"))
    add("Method", ["entity.name.function.member", "meta.function-call.method"], r("method"))
    add("Builtin", ["support.function.builtin", "support.type.builtin", "variable.language"],
        r("builtin"))
    add("Decorator", ["entity.name.function.decorator", "meta.decorator", "punctuation.decorator"],
        r("decorator"))
    add("Variable", ["variable", "variable.other.readwrite", "meta.definition.variable"],
        r("variable"))
    add("Parameter", ["variable.parameter"], r("parameter"))
    add("Property", ["variable.other.property", "variable.other.object.property",
                     "support.variable.property", "meta.object-literal.key"], r("property"))
    add("Tag", ["entity.name.tag", "punctuation.definition.tag"], r("tag"))
    add("Attribute", ["entity.other.attribute-name"], r("attribute"))
    add("Label", ["entity.name.label"], r("label"))
    add("Preprocessor", ["meta.preprocessor", "keyword.control.directive",
                         "entity.name.function.preprocessor"], r("preprocessor"))
    add("Invalid", ["invalid", "invalid.illegal"], v.diagnostic["error"].color)
    add("Deprecated", ["invalid.deprecated"], v.rc("deprecated"), "strikethrough")
    # Markup
    add("Markup heading", ["markup.heading", "entity.name.section"], r("heading"), "bold")
    add("Markup bold", ["markup.bold"], None, "bold")
    add("Markup italic", ["markup.italic"], None, "italic")
    add("Markup link", ["markup.underline.link", "string.other.link"], r("link"), "underline")
    add("Markup code", ["markup.inline.raw", "markup.raw"], r("string"))
    add("Markup list", ["markup.list", "punctuation.definition.list"], r("keyword"))
    add("Markup quote", ["markup.quote"], r("comment"), "italic")
    add("Markup inserted", ["markup.inserted"], v.diff["added"].color)
    add("Markup deleted", ["markup.deleted"], v.diff["removed"].color)
    add("Markup changed", ["markup.changed"], v.diff["changed"].color)
    # Data languages
    add("JSON key", ["support.type.property-name.json"], r("property"))
    add("YAML key", ["entity.name.tag.yaml"], r("property"))
    add("CSS selector", ["entity.name.selector", "entity.other.attribute-name.class",
                         "entity.other.attribute-name.id"], r("class"))
    add("CSS property", ["support.type.property-name.css"], r("property"))
    add("Shell prompt", ["punctuation.definition.prompt"], r("keyword"))
    return out


def _semantic(v: Variant) -> dict[str, object]:
    r = v.rc
    return {
        "namespace": r("namespace"),
        "class": r("class"),
        "enum": r("type"),
        "interface": r("interface"),
        "struct": r("class"),
        "typeParameter": r("type"),
        "type": r("type"),
        "parameter": r("parameter"),
        "variable": r("variable"),
        "variable.readonly": r("constant"),
        "variable.defaultLibrary": r("builtin"),
        "property": r("property"),
        "property.readonly": r("constant"),
        "enumMember": r("constant"),
        "decorator": r("decorator"),
        "event": r("property"),
        "function": r("function"),
        "function.defaultLibrary": r("builtin"),
        "method": r("method"),
        "macro": r("preprocessor"),
        "label": r("label"),
        "comment": {"foreground": r("comment"), "italic": True},
        "string": r("string"),
        "keyword": r("keyword"),
        "number": r("number"),
        "regexp": r("regex"),
        "operator": r("operator"),
        "*.deprecated": {"strikethrough": True},
        "*.declaration": {"bold": True},
    }


def _theme(v: Variant) -> str:
    return _dumps(
        {
            "name": v.label,
            "type": v.appearance,
            "semanticHighlighting": True,
            "colors": _workbench(v),
            "tokenColors": _token_colors(v),
            "semanticTokenColors": _semantic(v),
        }
    )


def _manifest(p: Palette) -> str:
    themes = []
    for _name, v in p.each():
        themes.append(
            {
                "id": v.id,
                "label": v.label,
                "uiTheme": "vs-dark" if v.is_dark else "vs",
                "path": f"./themes/{v.id}-color-theme.json",
            }
        )
    return _dumps(
        {
            "name": "grafana-color-scheme",
            "displayName": f"{p.name} Color Scheme",
            "description": (
                f"{p.name}, a dim color scheme derived from the Grafana Labs brand "
                "palette. Every syntax token clears WCAG AA."
            ),
            "version": "1.0.0",
            "engines": {"vscode": p.target_pin("vscode", "engine", "^1.90.0")},
            "categories": ["Themes"],
            "keywords": ["theme", "color-theme", "dark", "light", "accessibility", "wcag"],
            "license": p.scheme["license"],
            "repository": {"type": "git", "url": p.scheme["homepage"]},
            "contributes": {"themes": themes},
        }
    )


def emit(p: Palette) -> dict[str, str]:
    files = {"package.json": _manifest(p)}
    for _name, v in p.each():
        files[f"themes/{v.id}-color-theme.json"] = _theme(v)
    return files
