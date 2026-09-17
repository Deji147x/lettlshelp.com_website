#!/usr/bin/env python3
"""SEO and quality gate for the generated wireframes. Exits 1 if anything fails.

    python tools/seo_check.py

Covers the owner's SEO checklist: meta titles/descriptions, alt text, one H1 and heading
order, canonical tags, Open Graph image, schema, Search Console meta, sitemap.xml,
robots.txt, HTTPS enforcement, image weight + WebP, internal links (broken links,
anchors, orphan pages), and "avoid" items (noindex, insecure http:// references).
External links are not fetched here.
"""
import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "content"))

import leadership  # noqa: E402
import life  # noqa: E402

OUT = ROOT / "wireframes"
MAX_IMAGE_KB = 350
fails, warns = [], []


def meta(text, attr, name):
    m = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', text)
    return unescape(m.group(1)) if m else None


def page_url(site, slug=""):
    """Both practices share lettlshelp.com, so each site has a base path under it."""
    return f'{site["domain"]}{site.get("base", "")}/{slug + "/" if slug else ""}'


def check_page(site, page, root, inbound):
    slug = page["slug"]
    tag = f'{site["slug"]}/{slug + "/" if slug else ""}'
    path = root / slug / "index.html" if slug else root / "index.html"
    if not path.exists():
        fails.append(f"{tag}: page missing")
        return
    t = path.read_text("utf-8")

    title = re.search(r"<title>(.*?)</title>", t)
    title = unescape(title.group(1)) if title else ""
    if not 30 <= len(title) <= 70:
        fails.append(f"{tag}: title is {len(title)} chars (30-70)")
    elif len(title) > 60:
        warns.append(f"{tag}: title is {len(title)} chars; Google may truncate past ~60")
    desc = meta(t, "name", "description") or ""
    if not 70 <= len(desc) <= 165:
        fails.append(f"{tag}: meta description is {len(desc)} chars (70-165)")
    elif not 110 <= len(desc) <= 160:
        warns.append(f"{tag}: meta description is {len(desc)} chars (aim for 110-160)")

    if re.search(r'<meta name="robots"[^>]*noindex', t):
        fails.append(f"{tag}: noindex present")
    if len(re.findall(r"<h1[\s>]", t)) != 1:
        fails.append(f"{tag}: needs exactly one <h1>")
    levels = [int(n) for n in re.findall(r"<h([1-6])[\s>]", t)]
    if levels and levels[0] != 1:
        fails.append(f"{tag}: first heading is h{levels[0]}, not h1")
    for a, b in zip(levels, levels[1:]):
        if b > a + 1:
            fails.append(f"{tag}: heading order jumps h{a} -> h{b}")
            break

    for tag_img in re.findall(r"<img\b[^>]*>", t):
        if not re.search(r'\salt="', tag_img):
            fails.append(f"{tag}: <img> without alt attribute")

    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    if not canonical or canonical.group(1) != page_url(site, slug):
        fails.append(f"{tag}: canonical should be {page_url(site, slug)}")
    for prop in ("og:title", "og:description", "og:url", "og:image"):
        if not meta(t, "property", prop):
            fails.append(f"{tag}: missing {prop}")
    og_image = meta(t, "property", "og:image") or ""
    prefix = page_url(site)
    if og_image.startswith(prefix) and not (root / og_image[len(prefix):]).exists():
        fails.append(f"{tag}: og:image file missing")
    if not meta(t, "name", "twitter:card"):
        fails.append(f"{tag}: missing twitter:card")
    if 'name="viewport"' not in t:
        fails.append(f"{tag}: missing viewport meta (mobile)")
    if not re.search(r'<html lang="[a-z]', t):
        fails.append(f"{tag}: missing <html lang>")
    if site.get("gsc") and f'name="google-site-verification" content="{site["gsc"]}"' not in t:
        fails.append(f"{tag}: Search Console verification meta missing")
    if re.search(r'(?:href|src|srcset|content|imagesrcset)="http://', t):
        fails.append(f"{tag}: insecure http:// reference")

    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if not blocks:
        fails.append(f"{tag}: no JSON-LD schema")
    for block in blocks:
        try:
            if "@graph" not in json.loads(block):
                fails.append(f"{tag}: JSON-LD has no @graph")
        except ValueError as exc:
            fails.append(f"{tag}: invalid JSON-LD ({exc})")

    ids = set(re.findall(r'\sid="([^"]+)"', t))
    base = f"http://preview/{tag}"
    urls = re.findall(r'(?:href|src)="([^"]+)"', t)
    urls += [part.strip().split()[0] for group in re.findall(r'(?:srcset|imagesrcset)="([^"]+)"', t)
             for part in group.split(",")]
    for u in urls:
        if u.startswith(("mailto:", "tel:", "https://")):
            continue
        if u.startswith("#"):
            if u[1:] not in ids:
                fails.append(f"{tag}: broken anchor {u}")
            continue
        parsed = urlparse(urljoin(base, u))
        target = OUT / parsed.path.lstrip("/")
        if parsed.path.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            fails.append(f"{tag}: broken link {u}")
            continue
        if parsed.fragment and target.suffix == ".html" and f'id="{parsed.fragment}"' not in target.read_text("utf-8"):
            fails.append(f"{tag}: broken anchor {u}")
        if target.name == "index.html" and target.parent != path.parent:
            try:
                linked = target.parent.relative_to(root).as_posix()
            except ValueError:
                continue
            linked = "" if linked == "." else linked
            if linked in inbound:
                inbound[linked] += 1


def check_site(module):
    site, pages = module.SITE, module.PAGES
    root = OUT / site["slug"]
    inbound = {p["slug"]: 0 for p in pages}
    for page in pages:
        check_page(site, page, root, inbound)
    for slug, count in inbound.items():
        if slug and count == 0:
            fails.append(f'{site["slug"]}/{slug}/: orphan page (nothing links to it)')

    # sitemap.xml, robots.txt and .htaccess are shared: one domain, one WordPress install.
    sitemap = OUT / "sitemap.xml"
    if not sitemap.exists():
        fails.append("sitemap.xml missing at the site root")
    else:
        locs = set(re.findall(r"<loc>([^<]+)</loc>", sitemap.read_text("utf-8")))
        for page in pages:
            if page_url(site, page["slug"]) not in locs:
                fails.append(f'sitemap.xml missing {page_url(site, page["slug"])}')
    robots_text = (OUT / "robots.txt").read_text("utf-8") if (OUT / "robots.txt").exists() else ""
    if f'Sitemap: {site["domain"]}/sitemap.xml' not in robots_text:
        fails.append("robots.txt missing or has no Sitemap line")
    if re.search(r"^Disallow: /\s*$", robots_text, re.M):
        fails.append("robots.txt blocks the whole site")
    htaccess = OUT / ".htaccess"
    if not htaccess.exists() or "RewriteCond %{HTTPS} !=on" not in htaccess.read_text("utf-8"):
        fails.append(".htaccess HTTPS redirect missing")
    if not site.get("gsc"):
        warns.append(f'{site["slug"]}: no Search Console token yet (verify via DNS TXT or add token)')

    for image in (root / "assets").rglob("*"):
        if image.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".ico"}:
            kb = image.stat().st_size / 1024
            if kb > MAX_IMAGE_KB:
                fails.append(f"{image.relative_to(ROOT).as_posix()}: {kb:.0f} KB > {MAX_IMAGE_KB} KB")
    for jpg in (root / "assets" / "img").glob("*.jpg"):
        for modern in (".webp", ".avif"):
            if not jpg.with_suffix(modern).exists():
                fails.append(f"{jpg.relative_to(ROOT).as_posix()}: no {modern[1:].upper()} version")


def main():
    for module in (life, leadership):
        check_site(module)
    images = [f for f in OUT.rglob("*") if f.suffix.lower() in {".jpg", ".webp", ".png"}]
    webp = sum(f.stat().st_size for f in images if f.suffix == ".webp")
    jpg = sum(f.stat().st_size for f in images if f.suffix == ".jpg" and "/img/" in f.as_posix())
    print(f"photos: {jpg / 1e6:.2f} MB JPEG fallback, {webp / 1e6:.2f} MB WebP")
    for w in warns:
        print("WARN", w)
    for f in fails:
        print("FAIL", f)
    print(f"{len(fails)} failures, {len(warns)} warnings")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
