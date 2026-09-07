# Herdr

[Herdr](https://herdr.dev) compiles its themes into the binary — there is no
`~/.config/herdr/themes/` loader. So these are **config fragments**, not
theme files.

- `grafana-{dark,light}.config.toml` — one variant each
- `grafana-auto.config.toml` — both, following the host terminal's appearance

Generated from [`../../palette.toml`](../../palette.toml) — do not edit.

## The easy route first

Herdr's `terminal` theme follows the host terminal's ANSI palette. If you
have already installed the WezTerm or iTerm2 scheme from this repo, this is
all you need and it stays in sync automatically:

```toml
[theme]
name = "terminal"
```

## The precise route

Paste the contents of one of the `.config.toml` files into
`~/.config/herdr/config.toml`, then:

```sh
herdr server reload-config
```

Precedence is: built-in theme → `[theme.custom]` → the matching
`[theme.custom.light]` or `[theme.custom.dark]` sub-table.

## The token mapping is lossy

Herdr's palette vocabulary is Catppuccin's, so several of its token names
describe a color this palette does not have. The mapping:

| Herdr token | our color | note |
|---|---|---|
| `accent`, `peach` | `orange` | |
| `mauve` | `purple` | |
| `red` | `pink` | the Grafana brand has no red |
| `yellow` | `amber` | our `yellow` is reserved for diff-changed |
| `teal` | `light-green` | |
| `green`, `blue` | same | |
| `text`, `subtext0` | `fg`, `subtext` | |
| `panel_bg`, `sidebar_bg` | `base`, `mantle` | |
| `surface0`, `surface1`, `surface_dim` | `surface0`, `surface1`, `crust` | |
| `overlay0`, `overlay1` | `surface2`, `faint` | |
| `active_row_bg`, `selection_bg` | `surface0`, `surface1` | |

All 19 tokens are written, so nothing falls back to Catppuccin.

## Notes

- Validated against Herdr 0.8, recorded in `palette.toml` under
  `[targets.herdr]`. Herdr has no theme schema to check against, so a token
  rename in a future release cannot be caught automatically — this is manual
  maintenance.
- `auto_switch = true` combined with `[theme.custom]` overrides works, but
  `light_name` / `dark_name` only accept **built-in** theme names, so they
  cannot point at this palette.
- Getting the palette into Herdr's built-in list is on the roadmap. `nord`
  is already built in, so there is precedent.
