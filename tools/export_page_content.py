#!/usr/bin/env python3
"""Export each built page's main content, ready to paste into WordPress.

    python tools/build.py --production
    python tools/export_page_content.py

Writes page-content/<slug>.txt. Each file holds everything inside <main> — the page itself,
without the site header, navigation, breadcrumbs or footer, which WordPress supplies.

Each file is wrapped as a single WordPress HTML block, so pasting it into the block editor's
Code editor reproduces the page exactly, with the same markup and class names the theme's
stylesheet already targets. Nothing is retyped and nothing drifts from the approved design.

Links are rewritten from relative paths to site-root paths (/ethics/, /life-solutions/about/)
because the content moves from a folder structure into WordPress pages.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "wireframes"
DEST = ROOT / "page-content"

# Built folder -> the WordPress page it belongs in.
def wp_path(page_dir):
    rel = page_dir.relative_to(OUT).as_posix()
    return "/" if rel == "." else f"/{rel}/"


def resolve_links(html, page_dir):
    """Turn ../leadership-systems/ and about/ into /leadership-systems/ and /life-solutions/about/."""
    def fix(match):
        prefix, href = match.group(1), match.group(2)
        if re.match(r"^(https?:|mailto:|tel:|#|/)", href):
            return match.group(0)
        target = (page_dir / href).resolve()
        try:
            rel = target.relative_to(OUT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        rel = rel.rstrip("/")
        return f'{prefix}/{rel}/"' if rel else f'{prefix}/"'

    return re.sub(r'(<a\s[^>]*?href=")([^"]*)"', fix, html)


def main():
    if not OUT.exists():
        sys.exit("No build found. Run: python tools/build.py --production")
    DEST.mkdir(exist_ok=True)
    for old in DEST.glob("*.txt"):
        old.unlink()

    written = 0
    for path in sorted(OUT.rglob("index.html")):
        html = path.read_text("utf-8")
        match = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
        if not match:
            print(f"  skipped (no <main>): {path.relative_to(OUT)}")
            continue
        body = match.group(1).strip()

        # Breadcrumbs duplicate what WordPress and the menu already show.
        body = re.sub(r'<nav class="breadcrumbs".*?</nav>', "", body, flags=re.S)
        body = resolve_links(body, path.parent)

        target = wp_path(path.parent)
        name = ("home" if target == "/" else target.strip("/").replace("/", "--")) + ".txt"
        (DEST / name).write_text(
            "<!-- wp:html -->\n" + body + "\n<!-- /wp:html -->\n", encoding="utf-8")
        print(f"  {name:<40} -> {target}")
        written += 1

    print(f"\n{written} files in page-content/")


if __name__ == "__main__":
    main()
