# Emacs

Two themes, `grafana-dark` and `grafana-light`.

Generated from [`../../palette.toml`](../../palette.toml) — do not edit.

## Install

```sh
mkdir -p ~/.emacs.d/themes
cp grafana-*-theme.el ~/.emacs.d/themes/
```

```elisp
(add-to-list 'custom-theme-load-path "~/.emacs.d/themes/")
(load-theme 'grafana-dark t)
```

The files also self-register via an autoloaded
`custom-theme-load-path` hook, so if you load them from this directory
directly the `add-to-list` is unnecessary.

## Coverage

Basic faces, `font-lock-*` (including the faces added in Emacs 29 —
`font-lock-operator-face`, `font-lock-number-face`,
`font-lock-property-*-face`, `font-lock-delimiter-face`,
`font-lock-punctuation-face`, `font-lock-variable-use-face`,
`font-lock-function-call-face`), line numbers, mode line, header line, tab
bar, `diff-mode`, completions, `dired`, `flymake`, `compilation`, `org-mode`,
`markdown-mode` and the `term` ANSI faces.

`ansi-color-names-vector` is set from the shared ANSI table, so `M-x shell`
and `M-x term` match the terminal files in this repo.

## Terminals

One display spec, `((class color) (min-colors 89))`, so the theme applies in
GUI Emacs and in any terminal Emacs believes has enough colors. In a
256-color terminal Emacs approximates these hexes to the nearest cube entry,
which is close but not exact.

For exact colors in a terminal, use a truecolor-capable one and set:

```sh
export TERM=xterm-direct
```

Requires Emacs 26.1 or newer.
