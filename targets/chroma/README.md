# Chroma / Hugo

Two artifacts per variant, because Chroma has two kinds of consumer.

- `styles/grafana-{dark,light}.xml` — Chroma's own style format. Go programs
  can load these at runtime; this is also the file shape the upstream
  `styles/` directory expects.
- `css/grafana-{dark,light}.css` — pre-generated classes, for Hugo.
- `css/grafana-auto.css` — both variants in one stylesheet, following the
  reader's system setting with a `data-theme` override.

Generated from [`../../palette.toml`](../../palette.toml) — do not edit.

## Hugo

**Hugo cannot load a custom Chroma XML file.** `markup.highlight.style`
accepts only the styles compiled into Hugo, and pointing it at a path fails
silently by falling back to a built-in. That is why the CSS is shipped.

```sh
cp css/grafana-dark.css /path/to/site/assets/css/syntax.css
```

```yaml
# hugo.yaml
markup:
  highlight:
    noClasses: false
```

`noClasses: false` is the part people miss. Without it Hugo writes inline
styles and the stylesheet does nothing at all.

Then include the CSS. If you already bundle a stylesheet:

```go-html-template
{{ $css := slice (resources.Get "css/main.css") (resources.Get "css/syntax.css")
    | resources.Concat "css/bundle.css" | minify | fingerprint }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}" integrity="{{ $css.Data.Integrity }}">
```

### Code blocks with no language

A fenced block with no language tag is emitted as a bare `<pre><code>` with
no `.chroma` class, so it will keep whatever background your own CSS gives
`pre` — on a page that also has highlighted blocks, that looks broken. Add:

```css
pre { background: #1e1e1e; color: #c9c9c9; tab-size: 4; }
```

## Go

```go
import (
    "github.com/alecthomas/chroma/v2"
    "github.com/alecthomas/chroma/v2/styles"
)

//go:embed grafana-dark.xml
var grafanaDark string

style := chroma.MustNewXMLStyle(strings.NewReader(grafanaDark))
styles.Register(style)
```

`v2` is the current stable module (`v3` is alpha-only as of September 2026);
the XML format is identical in both.

## Notes

- The XML filename stem must equal the lowercased style name — upstream
  Chroma has a test asserting it. Keep them in sync if you rename anything.
- The two styles cross-reference each other with `counterpart`, so
  `styles.GetForMode` can pair them. That attribute is in use in Chroma's own
  `styles/github.xml`, so it is safe on stable.
- The token-to-class table is pinned in
  `tools/gcs/emit/chroma_tokens.py`, verified against Chroma v2.27.0. If
  Chroma adds a token type, the generated CSS will silently lack that class —
  re-check the table when bumping Chroma.
