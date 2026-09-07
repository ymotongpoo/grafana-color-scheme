# WezTerm

Four schemes: `grafana-dark`, `grafana-light`, and a `-vivid` flavor of each
that brightens ANSI slots 9–14 to the undimmed brand colors.

## Install

```sh
mkdir -p ~/.config/wezterm/colors
cp colors/*.toml ~/.config/wezterm/colors/
```

Then in `wezterm.lua`:

```lua
config.color_scheme = 'Grafana Dark'
```

Schemes in `~/.config/wezterm/colors` are picked up with no further config,
and they override built-ins of the same name. To load them from somewhere
else, set `config.color_scheme_dirs = { '/path/to/colors' }`.

The scheme name shown to WezTerm comes from `[metadata].name`, not the
filename: `Grafana Dark`, `Grafana Dark Vivid`, `Grafana Light`,
`Grafana Light Vivid`.

## The window frame is not part of a color scheme

WezTerm's *fancy* tab bar draws its surrounding frame from `window_frame`,
which lives in `wezterm.lua` and cannot be set from a scheme file. Without
this the frame keeps its default color and looks detached from the rest:

```lua
config.window_frame = {
  active_titlebar_bg = '#191919',    -- mantle
  inactive_titlebar_bg = '#141414',  -- crust
}
```

For the light variant use `#f0f0f0` and `#e4e4e4`.

`[colors.tab_bar]` in the scheme file covers the retro tab bar's strip and
the per-tab items in both modes.

## Notes

- `alpha` is ignored on everything except `selection_fg` and `selection_bg`.
- Since 20220903 `colors` overrides `color_scheme` key by key rather than
  replacing it, so you can keep the scheme and override one value.
- If you also install the `.itermcolors` file from `../iterm2`, note that
  WezTerm bundles over a thousand schemes generated from
  `mbadolato/iTerm2-Color-Schemes`; contributing there is the eventual route
  to having these available without any local file.
