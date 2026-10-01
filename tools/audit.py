#!/usr/bin/env python3
"""Pre-launch audit of the built site: consistency, security, and health.

    python tools/build.py --production
    python tools/audit.py

seo_check.py guards the SEO basics. This looks for the things that break a site in front of a
real visitor: links that go nowhere, anchors that don't exist, images missing their alt text or
their file, copy that contradicts itself between pages, review scaffolding left switched on, and
the handful of security habits that matter for a static site handling sensitive enquiries.

Exit code 1 if anything FAILs. WARNs are judgement calls for a human.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "wireframes"
sys.path.insert(0, str(ROOT / "content"))

import common as C  # noqa: E402

fails, warns, notes = [], [], []


def fail(msg):
    fails.append(msg)


def warn(msg):
    warns.append(msg)


def note(msg):
    notes.append(msg)


class Page(HTMLParser):
    """Just enough parsing to check links, images, headings and ids."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.images, self.headings, self.ids = [], [], [], set()
        self.scripts, self.styles, self.inline_handlers = [], [], []
        self.meta = {}
        self.title = ""
        self._in_title = False
        self._heading = None
        self.text_blocks = []
        self._in_block = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in a:
            if key.startswith("on"):
                self.inline_handlers.append((tag, key))
        if tag == "a" and "href" in a:
            self.links.append((a["href"], a.get("rel", ""), a.get("target", "")))
        elif tag == "img":
            self.images.append((a.get("src", ""), a.get("alt"), a.get("srcset", "")))
        elif tag == "source":
            self.images.append((None, "-", a.get("srcset", "")))
        elif tag == "script" and "src" in a:
            self.scripts.append(a["src"])
        elif tag == "link" and a.get("rel") == "stylesheet":
            self.styles.append(a.get("href", ""))
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.meta["canonical"] = a.get("href", "")
        elif tag == "title":
            self._in_title = True
        elif tag in ("h1", "h2", "h3", "h4"):
            self._heading = tag
            self._buf = []
        elif tag == "p":
            self._in_block = "p"
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4") and self._heading:
            self.headings.append((int(tag[1]), "".join(self._buf).strip()))
            self._heading = None
        elif tag == "p" and self._in_block:
            text = " ".join("".join(self._buf).split())
            if len(text) > 60:
                self.text_blocks.append(text)
            self._in_block = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._heading or self._in_block:
            self._buf.append(data)


def load_pages():
    pages = {}
    for path in sorted(OUT.rglob("index.html")):
        page = Page()
        page.feed(path.read_text("utf-8"))
        pages[path] = page
    return pages


def rel_url(path):
    return "/" + path.relative_to(OUT).parent.as_posix().replace(".", "").lstrip("/")


# ---------------------------------------------------------------- consistency

def check_consistency(pages):
    print("\n== Page consistency ==")
    titles, descriptions = Counter(), Counter()
    for path, page in pages.items():
        url = rel_url(path)

        # One H1, and heading levels that never skip a step.
        h1s = [t for lvl, t in page.headings if lvl == 1]
        if len(h1s) != 1:
            fail(f"{url}: {len(h1s)} H1 headings (want exactly 1)")
        last = 0
        for lvl, text in page.headings:
            if last and lvl > last + 1:
                fail(f"{url}: heading jumps h{last} -> h{lvl} at {text[:45]!r}")
            last = lvl

        # Title and description present, sane length, and unique across the site.
        title = page.title.strip()
        desc = page.meta.get("description", "").strip()
        titles[title] += 1
        descriptions[desc] += 1
        if not 30 <= len(title) <= 70:
            fail(f"{url}: title is {len(title)} chars — {title!r}")
        if not 70 <= len(desc) <= 165:
            warn(f"{url}: meta description is {len(desc)} chars")
        if not page.meta.get("canonical"):
            fail(f"{url}: no canonical URL")
        if not page.meta.get("og:image"):
            warn(f"{url}: no og:image")

        # The same paragraph printed twice on one page is the duplication bug class.
        for text, count in Counter(page.text_blocks).items():
            if count > 1:
                fail(f"{url}: paragraph repeated {count}x — {text[:70]!r}")

    for title, count in titles.items():
        if count > 1:
            fail(f"{count} pages share the title {title!r}")
    for desc, count in descriptions.items():
        if count > 1 and desc:
            warn(f"{count} pages share a meta description — {desc[:60]!r}")

    # Each section must show its own address, and never the other practice's.
    for path, page in pages.items():
        url = rel_url(path)
        body = path.read_text("utf-8")
        expected = None
        if "/life-solutions/" in url:
            expected, other = C.EMAIL_LIFE, C.EMAIL_LEADERSHIP
        elif "/leadership-systems/" in url:
            expected, other = C.EMAIL_LEADERSHIP, C.EMAIL_LIFE
        if expected and f"mailto:{other}" in body and f"mailto:{expected}" not in body:
            fail(f"{url}: shows only the sister practice's address")
        for dead in ("services@lettlshelp.com", "support@lettlshelp.com", "LetTLSHelp@gmail.com"):
            if dead in body:
                fail(f"{url}: retired address {dead} still present")

    # Every page carries the phone number and reaches the policy pages.
    for path, page in pages.items():
        url = rel_url(path)
        body = path.read_text("utf-8")
        if C.PHONE_TEL not in body:
            fail(f"{url}: no phone number")
        for slug, label in C.ROOT_POLICIES:
            if f"{slug}/" not in body:
                fail(f"{url}: footer does not link to /{slug}/")


# ---------------------------------------------------------------- links, images

def check_links(pages):
    print("\n== Links and images ==")
    external = Counter()
    for path, page in pages.items():
        url = rel_url(path)
        ids = page.ids
        for href, rel, target in page.links:
            if href.startswith(("mailto:", "tel:")):
                continue
            if href.startswith("http://"):
                fail(f"{url}: insecure http:// link — {href}")
                continue
            if href.startswith("https://"):
                host = href.split("/")[2]
                # A link to our own domain written absolute still leaves the site anywhere it
                # isn't served from that exact host — staging, a preview under a subpath, or
                # after a move. Those should be relative.
                if host.endswith("lettlshelp.com"):
                    fail(f"{url}: internal link written as an absolute URL — {href}")
                    continue
                external[host] += 1
                if "noopener" not in rel:
                    fail(f"{url}: external link without rel=noopener — {href}")
                if target == "_blank" and "noopener" not in rel:
                    fail(f"{url}: target=_blank without rel=noopener — {href}")
                continue
            if href.startswith("javascript:"):
                fail(f"{url}: javascript: link — {href}")
                continue
            frag = ""
            link = href
            if "#" in href:
                link, frag = href.split("#", 1)
            if link in ("", "./"):
                if frag and frag not in ids:
                    fail(f"{url}: anchor #{frag} does not exist on this page")
                continue
            target_path = (path.parent / link).resolve()
            if target_path.is_dir():
                target_path = target_path / "index.html"
            elif not target_path.suffix:
                target_path = target_path / "index.html"
            if not target_path.exists():
                fail(f"{url}: broken link — {href}")
            elif frag:
                other = pages.get(target_path)
                if other and frag not in other.ids:
                    fail(f"{url}: {href} points at an anchor that does not exist")

        for src, alt, srcset in page.images:
            if alt is None:
                fail(f"{url}: <img> with no alt attribute — {src}")
            elif alt == "":
                pass  # decorative, deliberate
            for candidate in re.findall(r"([^\s,]+)\s+\d+w", srcset) + ([src] if src else []):
                if candidate.startswith(("http", "data:")):
                    continue
                if not (path.parent / candidate).resolve().exists():
                    fail(f"{url}: missing image file — {candidate}")

        for asset in page.scripts + page.styles:
            if asset.startswith("http"):
                external[asset.split("/")[2]] += 1
                continue
            if not (path.parent / asset).resolve().exists():
                fail(f"{url}: missing asset — {asset}")

    note("Third-party hosts contacted: " + (", ".join(f"{h} ({n})" for h, n in external.most_common())
                                            or "none"))
    for host in external:
        if host not in {"fonts.googleapis.com", "fonts.gstatic.com"} and not host.endswith(
                ("maryland.gov", "mdcourts.gov", "peoples-law.org", "mdmediation.org", "bbb.org",
                 "crisistextline.org", "facebook.com", "linkedin.com", "lettlshelp.com")):
            warn(f"unexpected third-party host: {host}")


# ---------------------------------------------------------------- security

SECRET_PATTERNS = [
    (r"(?i)\b(api[_-]?key|secret|passwd|password)\s*[:=]\s*['\"][^'\"]{8,}", "credential assignment"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key"),
    (r"\bghp_[A-Za-z0-9]{30,}\b", "GitHub token"),
    (r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b", "Slack token"),
    (r"\bsk-[A-Za-z0-9]{32,}\b", "OpenAI-style key"),
]


def check_security(pages):
    print("\n== Security ==")
    # Secrets in the tracked tree. The repo is public, so this matters.
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix in {".png", ".jpg", ".webp",
                                                                          ".avif", ".ico"}:
            continue
        try:
            text = path.read_text("utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, text):
                fail(f"possible {label} in {path.relative_to(ROOT).as_posix()}")

    # Inline event handlers are the classic XSS foothold; this site should have none.
    for path, page in pages.items():
        for tag, attr in page.inline_handlers:
            fail(f"{rel_url(path)}: inline {attr} handler on <{tag}>")

    # Review scaffolding must not survive into the production build.
    for path in OUT.rglob("index.html"):
        body = path.read_text("utf-8")
        for marker, label in [("data-wf=", "pattern label"), ("draft-flag", "Review flag"),
                              ("wf-banner", "preview banner"), ("wf-toggle", "notes toggle"),
                              ("In this wireframe", "wireframe wording")]:
            if marker in body:
                fail(f"{rel_url(path)}: {label} present in the production build")

    # The security headers only exist if .htaccess ships with the site.
    htaccess = OUT / ".htaccess"
    if not htaccess.exists():
        fail(".htaccess missing — no security headers, no HTTPS redirect, no 301s")
    else:
        text = htaccess.read_text("utf-8")
        for needle, label in [("Strict-Transport-Security", "HSTS"),
                              ("X-Content-Type-Options", "nosniff"),
                              ("X-Frame-Options", "clickjacking protection"),
                              ("Referrer-Policy", "referrer policy"),
                              ("Content-Security-Policy", "CSP"),
                              ("RewriteCond %{HTTPS} !=on", "HTTPS redirect")]:
            if needle not in text:
                fail(f".htaccess: {label} missing")
        if "'unsafe-inline'" in text:
            warn("CSP allows 'unsafe-inline' for scripts — needed today by the JSON-LD and "
                 "analytics snippets. Move them to nonces to tighten it.")
        note("Security headers ship in .htaccess, so they apply on Apache/LiteSpeed hosting only. "
             "They do nothing on GitHub Pages, where the preview lives.")

    # Forms: this build has no server, so submissions leave via the visitor's mail client.
    form_pages = [rel_url(p) for p in OUT.rglob("index.html")
                  if "mailto-form" in p.read_text("utf-8") or "intake-form" in p.read_text("utf-8")]
    if form_pages:
        note(f"{len(form_pages)} pages carry a mailto form: {', '.join(form_pages)}")
        warn("Enquiries travel as ordinary email via the visitor's own mail client. They are not "
             "encrypted end to end, and nothing is recorded if the visitor never presses send. "
             "The owner chose this; a server-side form would fix both.")


# ---------------------------------------------------------------- health

def check_health(pages):
    print("\n== Health ==")
    expected = 20
    if len(pages) != expected:
        warn(f"{len(pages)} pages built (expected {expected})")

    sitemap = OUT / "sitemap.xml"
    if not sitemap.exists():
        fail("sitemap.xml missing")
    else:
        locs = set(re.findall(r"<loc>([^<]+)</loc>", sitemap.read_text("utf-8")))
        note(f"sitemap lists {len(locs)} URLs")
        if len(locs) != len(pages):
            fail(f"sitemap lists {len(locs)} URLs but {len(pages)} pages were built")

    robots = OUT / "robots.txt"
    if not robots.exists():
        fail("robots.txt missing")
    elif re.search(r"^Disallow: /\s*$", robots.read_text("utf-8"), re.M):
        fail("robots.txt blocks the whole site")

    # Schema: every page should carry a parseable JSON-LD graph.
    for path in OUT.rglob("index.html"):
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                            path.read_text("utf-8"), re.S)
        if not blocks:
            fail(f"{rel_url(path)}: no JSON-LD schema")
            continue
        for block in blocks:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                fail(f"{rel_url(path)}: invalid JSON-LD ({exc.msg})")

    # Page weight, which is what slow connections actually feel.
    heavy = []
    for path in OUT.rglob("index.html"):
        kb = path.stat().st_size / 1024
        if kb > 100:
            heavy.append((rel_url(path), kb))
    for url, kb in sorted(heavy, key=lambda x: -x[1])[:5]:
        warn(f"{url}: HTML is {kb:.0f} KB before assets")

    # Decisions still open, deliberately marked on the page.
    open_items = sum(len(re.findall(r'class="open-item"', p.read_text("utf-8")))
                     for p in OUT.rglob("index.html"))
    note(f"{open_items} bracketed decisions still awaiting the owner or an attorney")

    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    note(f"site total: {total / 1e6:.1f} MB across {sum(1 for f in OUT.rglob('*') if f.is_file())} files")


def main():
    if not OUT.exists():
        sys.exit("No build found. Run: python tools/build.py --production")
    pages = load_pages()
    check_consistency(pages)
    check_links(pages)
    check_security(pages)
    check_health(pages)

    print("\n== Result ==")
    for n in notes:
        print(f"  note  {n}")
    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    print(f"\n{len(fails)} failures, {len(warns)} warnings, {len(pages)} pages audited")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
