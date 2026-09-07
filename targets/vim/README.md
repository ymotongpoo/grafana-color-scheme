# Vim / Neovim

Two colorschemes covering classic Vim highlight groups, Neovim's
`Diagnostic*` and `Lsp*` groups, and the treesitter `@` captures — all in
vimscript, so one file serves both editors.

Generated from [`../../palette.toml`](../../palette.toml) — do not edit.

## Install

This directory is a valid `runtimepath` entry:

```vim
set runtimepath+=/path/to/grafana-color-scheme/targets/vim
colorscheme grafana-dark
```

Or copy the file:

```sh
mkdir -p ~/.vim/colors            # or ~/.config/nvim/colors
cp colors/grafana-dark.vim ~/.vim/colors/
```

With a plugin manager, point it at the repo and give it the subdirectory:

```lua
-- lazy.nvim
{ 'ymotongpoo/grafana-color-scheme',
  config = function()
    vim.opt.rtp:append(vim.fn.stdpath('data') ..
      '/lazy/grafana-color-scheme/targets/vim')
    vim.cmd.colorscheme('grafana-dark')
  end }
```

## Truecolor

The colorscheme does **not** call `set termguicolors`. That is your
decision — turning it on unasked breaks plain Vim inside tmux and on older
terminals. Add it yourself:

```vim
set termguicolors
```

Inside tmux you also need the terminal to advertise truecolor:

```tmux
set -as terminal-features ',*:RGB'
```

Without `termguicolors` the scheme still works: every group defines
`ctermfg`/`ctermbg` alongside `guifg`/`guibg`, using 256-color indices
chosen to track the same role assignments.

## Options

Set before `:colorscheme`:

```vim
let g:grafana_italic = 0   " default 1; disable if italics render as reverse video
let g:grafana_bold   = 0   " default 1
```

## Notes

- `g:terminal_ansi_colors` and Neovim's `g:terminal_color_0..15` are set from
  the shared ANSI table, so `:terminal` matches the terminal files here.
- `undercurl` falls back to `underline` for `cterm`, since most terminals
  cannot draw it.
- A dedicated Neovim Lua module is on the roadmap; the vimscript file already
  covers the treesitter captures, so there is no functional gap today.
