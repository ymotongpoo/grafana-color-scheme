# tmux

Colors and status-line content are separate files, because most people
already have a status line they like and only want the palette.

- `src/grafana-{dark,light}.conf` — colors only
- `src/grafana-{dark,light}-status.conf` — optional status-line layout
- `grafana.tmux` — TPM entry point

Requires tmux 2.9 or newer (the legacy `*-fg` / `*-bg` options this would
otherwise need were removed there). The `popup-*` and `menu-*` options are
guarded by a version check and only apply on 3.2+.

## Install

Manually:

```sh
mkdir -p ~/.config/tmux/grafana
cp -r src ~/.config/tmux/grafana/
```

```tmux
# ~/.tmux.conf
source-file ~/.config/tmux/grafana/src/grafana-dark.conf
# optional:
source-file ~/.config/tmux/grafana/src/grafana-dark-status.conf
```

With [TPM](https://github.com/tmux-plugins/tpm):

```tmux
set -g @plugin 'ymotongpoo/grafana-color-scheme'
set -g @grafana_variant 'dark'   # or 'light'
set -g @grafana_status  'off'    # 'on' to also take the status layout
```

Reload with `tmux source-file ~/.tmux.conf`, or `prefix + I` under TPM.

## Truecolor

The theme does not set `terminal-features` or `terminal-overrides`. Those are
**server** options, so setting them wrongly breaks colors in every session —
that has to be your call, not the theme's. Add whichever matches your tmux:

```tmux
set -as terminal-features ',*:RGB'          # tmux 3.2+
set -ga terminal-overrides ',*:Tc'          # tmux < 3.2
```

Without one of these tmux quantizes the palette to 256 colors and the dim
tones flatten out noticeably.

## Using the palette in your own status line

Every color is published as a user option, so your own format strings can
reference it and stay in sync:

```tmux
set -g status-right "#[fg=#{@grafana_light_blue}]%H:%M"
```

Available: `bg` `bg_alt` `surface` `border` `fg` `subtext` `faint` `bright`
`orange` `amber` `yellow` `green` `light_green` `light_blue` `blue` `indigo`
`purple` `pink`.

They are set with `set -gq`, so your own `set -g @grafana_*` before sourcing
the theme wins.

## Notes

- `pane-border-format` and `pane-status-*` only render when you set
  `pane-border-status` to `top` or `bottom`; the theme leaves that to you.
- The status file sets `window-status-separator ""` because it draws its own
  padding. Drop that if you use your own window format.
