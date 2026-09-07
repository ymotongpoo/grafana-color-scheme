"""Chroma's token types and their short CSS class names.

Pinned here on purpose. If Chroma adds a TokenType and this table does not
know it, the generated stylesheet silently lacks that class and Hugo renders
the token unstyled. Re-check this list when bumping Chroma.

Verified against alecthomas/chroma v2.27.0 (`types.go`, `html.go`).
Order matters: it is the order `hugo gen chromastyles` emits, which keeps our
CSS diffable against Hugo's own output.
"""

from __future__ import annotations

# (Chroma TokenType, CSS class). Structural entries with no color are handled
# separately by the emitter.
TOKENS: tuple[tuple[str, str], ...] = (
    ("Other", "x"),
    ("Error", "err"),
    ("CodeLine", "cl"),
    ("LineLink", "lnlinks"),
    ("LineTableTD", "lntd"),
    ("LineTable", "lntable"),
    ("LineHighlight", "hl"),
    ("LineNumbersTable", "lnt"),
    ("LineNumbers", "ln"),
    ("Line", "line"),
    ("Keyword", "k"),
    ("KeywordConstant", "kc"),
    ("KeywordDeclaration", "kd"),
    ("KeywordNamespace", "kn"),
    ("KeywordPseudo", "kp"),
    ("KeywordReserved", "kr"),
    ("KeywordType", "kt"),
    ("NameAttribute", "na"),
    ("NameClass", "nc"),
    ("NameConstant", "no"),
    ("NameDecorator", "nd"),
    ("NameEntity", "ni"),
    ("NameException", "ne"),
    ("NameLabel", "nl"),
    ("NameNamespace", "nn"),
    ("NameOther", "nx"),
    ("NameTag", "nt"),
    ("NameBuiltin", "nb"),
    ("NameBuiltinPseudo", "bp"),
    ("NameVariable", "nv"),
    ("NameVariableClass", "vc"),
    ("NameVariableGlobal", "vg"),
    ("NameVariableInstance", "vi"),
    ("NameVariableMagic", "vm"),
    ("NameFunction", "nf"),
    ("NameFunctionMagic", "fm"),
    ("LiteralDate", "ld"),
    ("LiteralString", "s"),
    ("LiteralStringAffix", "sa"),
    ("LiteralStringBacktick", "sb"),
    ("LiteralStringChar", "sc"),
    ("LiteralStringDelimiter", "dl"),
    ("LiteralStringDoc", "sd"),
    ("LiteralStringDouble", "s2"),
    ("LiteralStringEscape", "se"),
    ("LiteralStringHeredoc", "sh"),
    ("LiteralStringInterpol", "si"),
    ("LiteralStringOther", "sx"),
    ("LiteralStringRegex", "sr"),
    ("LiteralStringSingle", "s1"),
    ("LiteralStringSymbol", "ss"),
    ("LiteralNumber", "m"),
    ("LiteralNumberBin", "mb"),
    ("LiteralNumberFloat", "mf"),
    ("LiteralNumberHex", "mh"),
    ("LiteralNumberInteger", "mi"),
    ("LiteralNumberIntegerLong", "il"),
    ("LiteralNumberOct", "mo"),
    ("Operator", "o"),
    ("OperatorWord", "ow"),
    ("OperatorReserved", "or"),
    ("Punctuation", "p"),
    ("Comment", "c"),
    ("CommentHashbang", "ch"),
    ("CommentMultiline", "cm"),
    ("CommentSingle", "c1"),
    ("CommentSpecial", "cs"),
    ("CommentPreproc", "cp"),
    ("CommentPreprocFile", "cpf"),
    ("GenericDeleted", "gd"),
    ("GenericEmph", "ge"),
    ("GenericError", "gr"),
    ("GenericHeading", "gh"),
    ("GenericInserted", "gi"),
    ("GenericOutput", "go"),
    ("GenericPrompt", "gp"),
    ("GenericStrong", "gs"),
    ("GenericSubheading", "gu"),
    ("GenericTraceback", "gt"),
    ("GenericUnderline", "gl"),
    ("TextWhitespace", "w"),
)

CLASS_OF = dict(TOKENS)

# Structural rules Chroma emits with no palette involvement.
STRUCTURAL: dict[str, str] = {
    "lnlinks": "outline:none;text-decoration:none;color:inherit",
    "lntd": "vertical-align:top;padding:0;margin:0;border:0",
    "lntable": "border-spacing:0;padding:0;margin:0;border:0",
    "line": "display:flex",
}
