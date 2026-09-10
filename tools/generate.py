#!/usr/bin/env python3
"""Render every target file from palette.toml.

    python3 tools/generate.py                       regenerate everything
    python3 tools/generate.py --check               exit 1 if anything is stale
    python3 tools/generate.py --check --diff        ... and show what differs
    python3 tools/generate.py --verify              palette invariants + browser contrast
    python3 tools/generate.py --target wezterm zed  a subset
    python3 tools/generate.py --list                registered targets

Standard library only, Python 3.11+ (tomllib). Emitters never touch the
filesystem; this file is the only writer.
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gcs import docs, palette as palette_mod, registry, svg, verify  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TARGETS_DIR = ROOT / "targets"
DOCS_DIR = ROOT / "docs"

# Hand-written files that live inside targets/ and are not generated.
NOT_GENERATED = {"README.md"}
# Directories of hand-managed binary assets. They are referenced by generated
# manifests but are not themselves derived from the palette, so orphan
# detection must leave them alone.
NOT_GENERATED_DIRS = {"images"}


def _render(pal, slugs: list[str]) -> dict[Path, str]:
    """{absolute path: content} for the requested targets, plus docs."""
    out: dict[Path, str] = {}
    for slug in slugs:
        target = registry.get(slug)
        for rel, content in target.emit(pal).items():
            if not content.endswith("\n") or content.endswith("\n\n"):
                raise SystemExit(
                    f"{slug} emitted {rel!r} without exactly one trailing newline"
                )
            out[TARGETS_DIR / slug / rel] = content
    return out


def _render_docs(pal) -> dict[Path, str]:
    out: dict[Path, str] = {}
    for rel, content in svg.emit(pal).items():
        out[DOCS_DIR / rel] = content
    return out


def _orphans(slugs: list[str], expected: dict[Path, str]) -> list[Path]:
    found: list[Path] = []
    for slug in slugs:
        base = TARGETS_DIR / slug
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.name in NOT_GENERATED:
                continue
            if NOT_GENERATED_DIRS & set(path.relative_to(base).parts):
                continue
            if path not in expected:
                found.append(path)
    return found


def cmd_list(pal) -> int:
    width = max(len(t.slug) for t in registry.TARGETS.values())
    print(f"{'slug'.ljust(width)}  {'name':<14}  artifacts")
    for slug in registry.TARGETS:
        t = registry.TARGETS[slug]
        flav = " (+vivid)" if t.flavors else ""
        print(f"{slug.ljust(width)}  {t.display:<14}  {t.artifacts}{flav}")
    print(f"\n{len(registry.TARGETS)} targets, variants: {', '.join(pal.scheme['variants'])}")
    return 0


def cmd_verify(pal) -> int:
    problems, message = verify.report(pal)
    print(message)
    return 1 if problems else 0


def cmd_check(pal, slugs: list[str], show_diff: bool) -> int:
    expected = _render(pal, slugs)
    expected.update(_render_docs(pal))
    expected.update(docs.emit(pal, ROOT))

    stale: list[Path] = []
    missing: list[Path] = []
    for path, content in sorted(expected.items()):
        if not path.exists():
            missing.append(path)
        elif path.read_text(encoding="utf-8") != content:
            stale.append(path)

    orphan = _orphans(slugs, expected)

    for path in missing:
        print(f"MISSING {path.relative_to(ROOT)}")
    for path in stale:
        print(f"STALE   {path.relative_to(ROOT)}")
    for path in orphan:
        print(f"ORPHAN  {path.relative_to(ROOT)}")

    if show_diff:
        for path in stale:
            got = path.read_text(encoding="utf-8").splitlines(keepends=True)
            want = expected[path].splitlines(keepends=True)
            rel = str(path.relative_to(ROOT))
            sys.stdout.writelines(
                difflib.unified_diff(got, want, fromfile=f"a/{rel}", tofile=f"b/{rel}")
            )

    total = len(stale) + len(missing) + len(orphan)
    if total:
        affected = {p.relative_to(TARGETS_DIR).parts[0] for p in stale + missing + orphan if TARGETS_DIR in p.parents}
        print(
            f"\n{total} problem(s)"
            + (f" in {len(affected)} target(s)" if affected else "")
            + ". Run: python3 tools/generate.py"
        )
        return 1
    print(f"OK  {len(expected)} generated file(s) match {pal.source.name}")
    return 0


def cmd_write(pal, slugs: list[str]) -> int:
    expected = _render(pal, slugs)
    expected.update(_render_docs(pal))
    expected.update(docs.emit(pal, ROOT))

    written = 0
    for path, content in sorted(expected.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_text(encoding="utf-8") == content:
            continue
        with path.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        written += 1

    for path in _orphans(slugs, expected):
        print(f"ORPHAN  {path.relative_to(ROOT)} (not generated; remove it by hand)")

    print(f"wrote {written} file(s), {len(expected)} total from {pal.source.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="generate.py", description="Render color scheme files from palette.toml"
    )
    ap.add_argument("--palette", default=str(ROOT / "palette.toml"), help="source palette")
    ap.add_argument("--target", nargs="+", metavar="SLUG", help="only these targets")
    ap.add_argument("--check", action="store_true", help="verify without writing")
    ap.add_argument("--diff", action="store_true", help="with --check, print diffs")
    ap.add_argument("--verify", action="store_true", help="check palette invariants only")
    ap.add_argument("--list", action="store_true", help="list registered targets")
    args = ap.parse_args(argv)

    pal = palette_mod.load(args.palette)

    if args.list:
        return cmd_list(pal)
    if args.verify:
        return cmd_verify(pal)

    slugs = args.target or list(registry.TARGETS)
    for slug in slugs:
        registry.get(slug)

    # Never emit from a palette that violates its own rules.
    problems, message = verify.report(pal)
    if problems:
        print(message, file=sys.stderr)
        print("\nrefusing to generate from an invalid palette", file=sys.stderr)
        return 1

    if args.check:
        return cmd_check(pal, slugs, args.diff)
    return cmd_write(pal, slugs)


if __name__ == "__main__":
    raise SystemExit(main())
