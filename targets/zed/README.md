# Zed

One theme family file containing both variants, plus an `extension.toml` so
the directory also works as a Zed extension.

Generated from [`../../palette.toml`](../../palette.toml) — do not edit.

## Install

```sh
mkdir -p ~/.config/zed/themes
cp themes/grafana.json ~/.config/zed/themes/
```

On Windows: `%USERPROFILE%\AppData\Roaming\Zed\themes\`.

Zed picks the file up on next load. Select it with
**cmd-k cmd-t** / **ctrl-k ctrl-t**, or set it directly:

```json
// ~/.config/zed/settings.json
{
  "theme": {
    "mode": "system",
    "light": "Grafana Light",
    "dark": "Grafana Dark"
  }
}
```

## Notes

- Written against theme schema `v0.2.0`, pinned in `palette.toml` under
  `[targets.zed]`. Zed adds keys over time; unknown keys are tolerated but
  missing ones fall back to Zed's defaults, which will not match.
- `border.transparent` and the `ghost_element.*` keys are explicitly
  `#00000000`. Omitting them yields opaque black rather than transparency.
- `syntax.*` entries are objects, and `font_weight` is a **number**
  (`700`), not the string `"bold"`.
- Eight `players` are provided, mapped to distinct accents, so collaborators
  in a shared session get visibly different cursors.
