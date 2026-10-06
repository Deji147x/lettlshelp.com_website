#!/usr/bin/env python3
"""Export the whole site as a WordPress import file.

    python tools/build.py --production
    python tools/export_wordpress.py

Writes lettlshelp-pages.xml — a standard WordPress eXtended RSS (WXR) file holding all 20
pages: title, address, parent, and the full page content.

This replaces pasting each page in by hand. In WordPress: Tools -> Import -> WordPress,
upload the file, and every page is created with its content, its address, and its place in
the hierarchy already correct.

The content of each page is the same markup the static build produces, wrapped as a single
WordPress HTML block, so the pages render exactly as the approved preview does.
"""
import html
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "wireframes"
DEST = ROOT / "lettlshelp-pages.xml"
SITE = "https://lettlshelp.com"
AUTHOR = "admin"

# Page titles, keyed by the built folder. Everything else is derived.
TITLES = {
    "": "Home",
    "ethics": "Ethics & Compliance",
    "disclaimers": "Disclaimers",
    "privacy-policy": "Privacy Policy",
    "terms": "Terms of Use",
    "contact": "Contact",
    "life-solutions": "Life Solutions",
    "leadership-systems": "Leadership Systems",
    "about": "About",
    "services": "Services",
    "how-it-works": "How It Works",
    "faq": "FAQ",
    "begin-intake": "Begin Intake",
}

# WordPress's importer skips any page whose title, date and type already exist. Both practices
# have an About, Services, How It Works, FAQ, Contact and Begin Intake, and every page carried
# the same timestamp, so the second practice's six pages and the second Contact were silently
# dropped — seven in all. Worse, WordPress then guessed at the missing addresses and sent
# /leadership-systems/services/ to the Life Solutions page. Each page now carries the practice
# in its title and a timestamp of its own, so nothing collides. The title is only the name in
# the admin list; each page's own H1 comes from its content and is unchanged.
SECTIONS = {"life-solutions": "Life Solutions", "leadership-systems": "Leadership Systems"}


def page_content(path):
    """Everything inside <main>, with the breadcrumbs dropped and links made absolute."""
    markup = path.read_text("utf-8")
    match = re.search(r"<main[^>]*>(.*?)</main>", markup, re.S)
    if not match:
        return None
    body = match.group(1).strip()
    body = re.sub(r'<nav class="breadcrumbs".*?</nav>', "", body, flags=re.S)

    def fix(m):
        prefix, href = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|tel:|#|/)", href):
            return m.group(0)
        target = (path.parent / href).resolve()
        try:
            rel = target.relative_to(OUT.resolve()).as_posix().rstrip("/")
        except ValueError:
            return m.group(0)
        return f'{prefix}/{rel}/"' if rel else f'{prefix}/"'

    body = re.sub(r'(<a\s[^>]*?href=")([^"]*)"', fix, body)
    return "<!-- wp:html -->\n" + body + "\n<!-- /wp:html -->"


def collect():
    """Every built page, with a post id and its parent's id."""
    pages, ids = [], {}
    dirs = sorted(OUT.rglob("index.html"), key=lambda p: len(p.relative_to(OUT).parts))
    for n, path in enumerate(dirs, start=100):
        rel = path.relative_to(OUT).parent.as_posix()
        rel = "" if rel == "." else rel
        ids[rel] = n
    for path in dirs:
        rel = path.relative_to(OUT).parent.as_posix()
        rel = "" if rel == "." else rel
        slug = rel.rsplit("/", 1)[-1] if rel else "home"
        parent_path = rel.rsplit("/", 1)[0] if "/" in rel else ""
        parent_id = ids.get(parent_path, 0) if "/" in rel else 0
        content = page_content(path)
        if content is None:
            continue
        title = TITLES.get(slug, slug.replace("-", " ").title())
        section = rel.split("/")[0] if "/" in rel else ""
        if section in SECTIONS:
            title = f"{SECTIONS[section]} — {title}"
        pages.append({
            "id": ids[rel],
            "title": title,
            "slug": slug,
            "parent": parent_id,
            "link": f"{SITE}/{rel + '/' if rel else ''}",
            "content": content,
        })
    return pages


def item(page, stamp):
    return f"""
  <item>
    <title><![CDATA[{page["title"]}]]></title>
    <link>{html.escape(page["link"])}</link>
    <pubDate>{stamp:%a, %d %b %Y %H:%M:%S} +0000</pubDate>
    <dc:creator><![CDATA[{AUTHOR}]]></dc:creator>
    <guid isPermaLink="false">{html.escape(page["link"])}</guid>
    <description></description>
    <content:encoded><![CDATA[{page["content"]}]]></content:encoded>
    <excerpt:encoded><![CDATA[]]></excerpt:encoded>
    <wp:post_id>{page["id"]}</wp:post_id>
    <wp:post_date><![CDATA[{stamp:%Y-%m-%d %H:%M:%S}]]></wp:post_date>
    <wp:post_date_gmt><![CDATA[{stamp:%Y-%m-%d %H:%M:%S}]]></wp:post_date_gmt>
    <wp:comment_status><![CDATA[closed]]></wp:comment_status>
    <wp:ping_status><![CDATA[closed]]></wp:ping_status>
    <wp:post_name><![CDATA[{page["slug"]}]]></wp:post_name>
    <wp:status><![CDATA[publish]]></wp:status>
    <wp:post_parent>{page["parent"]}</wp:post_parent>
    <wp:menu_order>0</wp:menu_order>
    <wp:post_type><![CDATA[page]]></wp:post_type>
    <wp:post_password><![CDATA[]]></wp:post_password>
    <wp:is_sticky>0</wp:is_sticky>
  </item>"""


def main():
    if not OUT.exists():
        sys.exit("No build found. Run: python tools/build.py --production")
    pages = collect()
    stamp = datetime.now(timezone.utc)
    # A minute apart each, so no two pages ever share a title *and* a timestamp.
    items = "".join(item(p, stamp - timedelta(minutes=n)) for n, p in enumerate(pages))
    DEST.write_text(f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
  xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:wfw="http://wellformedweb.org/CommentAPI/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
  <title>LetTLSHelp</title>
  <link>{SITE}</link>
  <description>Pages for lettlshelp.com</description>
  <pubDate>{stamp:%a, %d %b %Y %H:%M:%S} +0000</pubDate>
  <language>en-US</language>
  <wp:wxr_version>1.2</wp:wxr_version>
  <wp:base_site_url>{SITE}</wp:base_site_url>
  <wp:base_blog_url>{SITE}</wp:base_blog_url>
  <wp:author>
    <wp:author_id>1</wp:author_id>
    <wp:author_login><![CDATA[{AUTHOR}]]></wp:author_login>
    <wp:author_email><![CDATA[]]></wp:author_email>
    <wp:author_display_name><![CDATA[{AUTHOR}]]></wp:author_display_name>
    <wp:author_first_name><![CDATA[]]></wp:author_first_name>
    <wp:author_last_name><![CDATA[]]></wp:author_last_name>
  </wp:author>
{items}
</channel>
</rss>
""", encoding="utf-8")

    print(f"wrote {DEST.name}  ({DEST.stat().st_size/1024:.0f} KB, {len(pages)} pages)\n")
    for p in sorted(pages, key=lambda x: x["link"]):
        parent = next((q["title"] for q in pages if q["id"] == p["parent"]), "—")
        print(f"  {p['title']:<22} {parent:<22} {p['link'].replace(SITE, '') or '/'}")


if __name__ == "__main__":
    main()
