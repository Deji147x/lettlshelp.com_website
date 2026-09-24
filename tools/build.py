#!/usr/bin/env python3
"""Render the static HTML wireframes for both TLS sites.

    python tools/process_assets.py   # once, or when logos/photos change
    python tools/build.py

Reads content/{life,leadership}.py and writes wireframes/<site>/**/index.html plus
sitemap.xml, robots.txt, and site.webmanifest, then copies the design-system CSS and JS.
Each section maps to a planned WordPress block pattern (shown with "Show wireframe
notes"), so the wireframe converts 1:1 into the block theme. See docs/architecture.md.
"""
import json
import re
import shutil
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "content"))

import common as C  # noqa: E402
import hub  # noqa: E402
import leadership  # noqa: E402
import life  # noqa: E402
from icons import ICONS  # noqa: E402

OUT = ROOT / "wireframes"
DESIGN = ROOT / "design-system"
YEAR = 2026

# Two builds from one source.
#   python tools/build.py                → review build: preview banner, "Show wireframe
#                                          notes" toggle, pattern labels, yellow Review flags.
#   python tools/build.py --production   → the live site: none of that chrome.
# The Review flags stay in content/*.py either way. They are the working record of what the
# owner and her attorney still have to sign off, so they are hidden for launch, never deleted.
PRODUCTION = "--production" in sys.argv
WIREFRAME = not PRODUCTION  # review banner, notes toggle, and local sister-site links
SHOW_REVIEW_FLAGS = not PRODUCTION
# The hub is first: it owns the domain root, and the two practices sit in folders beneath it.
MODULES = [hub, life, leadership]
PRACTICES = [life, leadership]  # the two that have their own palette, images, and intake
IMG_SIZES = "(min-width: 860px) 560px, 100vw"


def site_url(site, slug=""):
    """Live URL for a page. Both practices share lettlshelp.com, so each site has a base path."""
    return f'{site["domain"]}{site.get("base", "")}/{slug + "/" if slug else ""}'


def attr(value):
    return escape(str(value), quote=True)


def strip_tags(value):
    return re.sub(r"<[^>]+>", "", value)


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", strip_tags(value).lower()).strip("-")


class Ctx:
    def __init__(self, site, page):
        self.site, self.page = site, page
        # Depth of this page below its own site folder, then below the domain root.
        self.up = "../" * len([p for p in page["slug"].split("/") if p])
        self.root = "../" * site.get("root_depth", 0) + self.up
        self.a = self.up + "assets/"
        manifest_path = OUT / site["slug"] / "assets" / "img" / "manifest.json"
        # The hub has no photographs of its own yet, so it has no image manifest.
        self.manifest = json.loads(manifest_path.read_text("utf-8")) if manifest_path.exists() else {}
        self.ids = set()

    def href(self, target):
        """Resolve a link target.

        A leading "/" means "from the domain root", which is how the practice pages reach the
        shared /ethics/, /disclaimers/ and /privacy-policy/ pages from any depth. Anything else
        is relative to this site's own folder.
        """
        if re.match(r"^(https?:|mailto:|tel:|#)", target):
            return target
        prefix = self.root if target.startswith("/") else self.up
        path, _, frag = target.lstrip("/").partition("#")
        link = (prefix + (path + "/" if path else "")) or "./"
        return link + ("#" + frag if frag else "")

    def url(self, slug=None):
        slug = self.page["slug"] if slug is None else slug
        return site_url(self.site, slug)

    def unique_id(self, text):
        base = slugify(text) or "section"
        candidate, n = base, 2
        while candidate in self.ids:
            candidate, n = f"{base}-{n}", n + 1
        self.ids.add(candidate)
        return candidate


# ---------- small helpers ----------

def icon(name):
    return f'<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[name]}</svg></span>'


def srcset(ctx, name, ext):
    big, small = ctx.manifest[name]["1600"], ctx.manifest[name]["800"]
    return f'{ctx.a}img/{name}-800.{ext} {small[0]}w, {ctx.a}img/{name}-1600.{ext} {big[0]}w'


def img(ctx, name, alt, sizes=IMG_SIZES, eager=False):
    """AVIF → WebP → JPEG; explicit dimensions prevent layout shift (CLS)."""
    big = ctx.manifest[name]["1600"]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{srcset(ctx, name, "avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset(ctx, name, "webp")}" sizes="{sizes}">'
            f'<img src="{ctx.a}img/{name}-1600.jpg" srcset="{srcset(ctx, name, "jpg")}" sizes="{sizes}" '
            f'width="{big[0]}" height="{big[1]}" alt="{attr(alt)}" {loading}></picture>')


def cta(name, ctx, aria=None):
    """Tracking hooks for every call to action: GA4/GTM read these in app.js."""
    label = f' aria-label="{attr(aria)}"' if aria else ""
    return f'data-cta="{attr(name)}" data-cta-page="{attr(ctx.page["slug"] or "home")}"{label}'


def button(ctx, pair, cls):
    name = pair[2] if len(pair) > 2 else slugify(pair[1])
    return f'<a class="btn {cls}" href="{ctx.href(pair[0])}" {cta(name, ctx)}>{pair[1]}</a>'


def paras(items):
    return "".join(f"<p>{p}</p>" for p in items or [])


def checklist(items):
    return f'<ul class="checklist">{"".join(f"<li>{i}</li>" for i in items)}</ul>' if items else ""


def draft_flag(text, small=False):
    if not text or not SHOW_REVIEW_FLAGS:
        return ""
    return f'<p class="draft-flag{" small" if small else ""}" role="note"><strong>Review:</strong> {text}</p>'


def slot_html(sl, heading_level=3):
    """An integration or owner-to-supply placeholder.

    heading_level=None renders the title as plain text. Use it where the slot sits beside an h1
    (the hub hero) so the placeholder doesn't break the page's heading order.
    """
    bullets = "".join(f"<li>{b}</li>" for b in sl.get("bullets", []))
    title = (f'<p class="slot-title">{sl["title"]}</p>' if heading_level is None
             else f'<h{heading_level}>{sl["title"]}</h{heading_level}>')
    return (f'<div class="slot" role="note"><span class="slot-label">{sl["label"]}</span>'
            f'{title}<p>{sl["text"]}</p>'
            f'{f"<ul class=softlist>{bullets}</ul>" if bullets else ""}</div>')


def heading(ctx, s, center=False):
    """Section eyebrow/h2/intro. Returns (html, heading id or None)."""
    if not (s.get("eyebrow") or s.get("h2") or s.get("intro")):
        return "", None
    hid = ctx.unique_id(s["h2"]) if s.get("h2") else None
    parts = [f'<p class="eyebrow">{s["eyebrow"]}</p>' if s.get("eyebrow") else "",
             f'<h2 id="{hid}">{s["h2"]}</h2>' if hid else "",
             f'<p class="lede">{s["intro"]}</p>' if s.get("intro") else ""]
    return f'<div class="section-head{" center" if center else ""}">{"".join(parts)}</div>', hid


def more_link(ctx, s, cls="btn-secondary", center=False):
    if not s.get("link"):
        return ""
    return f'<div class="btn-row{" center" if center else ""}">{button(ctx, s["link"], cls)}</div>'


def section(s, inner, cls="", hid=None):
    id_attr = f' id="{s["id"]}"' if s.get("id") else ""
    wf = f' data-wf="{attr(s["wf"])}"' if s.get("wf") else ""
    labelled = f' aria-labelledby="{hid}"' if hid else ""
    classes = f'section tone-{s.get("tone", "white")}' + (f" {cls}" if cls else "")
    return (f'<section class="{classes}"{id_attr}{wf}{labelled}>'
            f'<div class="container">{draft_flag(s.get("draft"))}{inner}</div></section>')


# ---------- section renderers ----------

def r_hero(ctx, s):
    copy = "".join([
        f'<p class="eyebrow">{s["eyebrow"]}</p>' if s.get("eyebrow") else "",
        f'<h1>{s["h1"]}</h1>',
        f'<p class="tagline">{s["tagline"]}</p>' if s.get("tagline") else "",
        f'<p class="lede">{s["lede"]}</p>' if s.get("lede") else "",
        '<div class="btn-row">' + button(ctx, s["primary"], "btn-primary")
        + (button(ctx, s["secondary"], "btn-secondary") if s.get("secondary") else "") + "</div>",
        f'<p class="hero-call">Prefer to talk? Call or text '
        f'<a href="tel:{C.PHONE_TEL}" {cta("call-hero", ctx)}>{C.PHONE}</a></p>',
    ])
    media = f'<div class="hero-media">{img(ctx, s["image"], s["alt"], eager=True)}</div>'
    return (f'<section class="hero" data-wf="{attr(s.get("wf", ""))}"><div class="container hero-grid">'
            f'<div class="hero-copy">{copy}</div>{media}</div></section>')


def r_page_hero(ctx, s):
    crumbs = (f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="{ctx.href("")}">Home</a></li>'
              f'<li aria-current="page">{ctx.page["label"]}</li></ol></nav>')
    eyebrow = f'<p class="eyebrow">{s["eyebrow"]}</p>' if s.get("eyebrow") else ""
    lede = f'<p class="lede">{s["lede"]}</p>' if s.get("lede") else ""
    return (f'<section class="page-hero" data-wf="Pattern: tls/page-header (Breadcrumbs + Title)">'
            f'<div class="container">{crumbs}{eyebrow}<h1>{s["h1"]}</h1>{lede}</div></section>')


def r_text(ctx, s):
    center = s.get("center", False)
    head, hid = heading(ctx, s, center)
    body = paras(s.get("paras")) + checklist(s.get("bullets")) + more_link(ctx, s, center=center)
    return section(s, f'<div class="prose{" center" if center else ""}">{head}{body}</div>', hid=hid)


def r_cards(ctx, s):
    head, hid = heading(ctx, s, s.get("center", False))
    cards = []
    for it in s["items"]:
        link = ""
        if it.get("link"):
            link = (f'<a class="card-link" href="{ctx.href(it["link"][0])}" '
                    f'{cta("card-" + slugify(it["title"]), ctx)}>{it["link"][1]} '
                    f'<span aria-hidden="true">→</span></a>')
        card_icon = icon(it["icon"]) if it.get("icon") else ""
        text = f'<p>{it["text"]}</p>' if it.get("text") else ""
        cards.append(f'<li class="card">{card_icon}<h3>{it["title"]}</h3>{text}{link}</li>')
    slot = f'<div class="section-slot">{slot_html(s["slot"])}</div>' if s.get("slot") else ""
    return section(s, f'{head}<ul class="grid" role="list">{"".join(cards)}</ul>{slot}'
                      f'{more_link(ctx, s, center=s.get("center", False))}', hid=hid)


def r_split(ctx, s):
    head, hid = heading(ctx, s)
    copy = head + paras(s.get("paras")) + checklist(s.get("bullets")) + paras(s.get("after")) + more_link(ctx, s)
    if s.get("image"):
        media = f'<div class="split-media">{img(ctx, s["image"], s["alt"])}</div>'
    elif s.get("media_slot"):
        media = f'<div class="split-media">{slot_html(s["media_slot"])}</div>'
    else:
        media = ""
    slot = f'<div class="section-slot">{slot_html(s["slot"])}</div>' if s.get("slot") else ""
    return section(s, f'<div class="split{" reverse" if s.get("reverse") else ""}">'
                      f'<div class="split-copy">{copy}</div>{media}</div>{slot}', hid=hid)


def r_steps(ctx, s):
    head, hid = heading(ctx, s, True)
    items = "".join(f'<li><h3>{i["title"]}</h3><p>{i["text"]}</p></li>' for i in s["items"])
    return section(s, f'{head}<ol class="steps">{items}</ol>{more_link(ctx, s, center=True)}', hid=hid)


def r_notlist(ctx, s):
    head, hid = heading(ctx, {"h2": s["h2"]})
    bullets = "".join(f"<li>{b}</li>" for b in s["bullets"])
    outro = f'<p>{s["outro"]}</p>' if s.get("outro") else ""
    return section(s, f'<div class="panel">{head}<p>{s["intro"]}</p><ul class="softlist">{bullets}</ul>'
                      f'{outro}{more_link(ctx, s)}</div>', hid=hid)


def r_faq(ctx, s):
    center = s.get("center", False)
    head, hid = heading(ctx, s, center)
    rows = "".join(f'<details><summary>{it["q"]}</summary><div class="answer"><p>{it["a"]}</p>'
                   f'{draft_flag(it.get("draft"), small=True)}</div></details>' for it in s["items"])
    return section(s, f'{head}<div class="faq{" center" if center else ""}">{rows}</div>'
                      f'{more_link(ctx, s, center=center)}', hid=hid)


def list_item(ctx, item):
    """A plain string, or a referral: {"name", "text", "url"} rendered as a named link."""
    if isinstance(item, str):
        return f"<li>{item}</li>"
    # noopener: the external site can't reach back into this tab. noreferrer: the referral
    # doesn't tell a crisis line or a court which dispute-resolution page someone came from.
    return (f'<li class="referral"><a href="{attr(item["url"])}" rel="noopener noreferrer" '
            f'{cta("referral-" + slugify(item["name"]), ctx)}>{item["name"]}</a>'
            f'<span class="referral-text">{item["text"]}</span></li>')


def r_list(ctx, s):
    head, hid = heading(ctx, s)
    referrals = any(not isinstance(i, str) for i in s["items"])
    items = "".join(list_item(ctx, i) for i in s["items"])
    cls = "referrals" if referrals else "columns"
    return section(s, f'{head}<ul class="{cls}">{items}</ul>{more_link(ctx, s)}', hid=hid)


def r_crosslink(ctx, s):
    return section(s, f'<div class="crosslink"><p>{s["text"]}</p>'
                      f'<a class="btn btn-secondary" href="{s["href"]}" '
                      f'{cta("sister-site", ctx)}>{s["label"]}</a></div>')


def r_cta(ctx, s):
    hid = ctx.unique_id(s["h2"])
    # The hub has no mailbox of its own, so its CTA band shows the phone number alone.
    mail = (f' &nbsp;·&nbsp; <a href="mailto:{ctx.site["email"]}" {cta("email-cta", ctx)}>'
            f'{ctx.site["email"]}</a>') if ctx.site.get("email") else ""
    contact = (f'<p class="cta-contact">'
               f'<a href="tel:{C.PHONE_TEL}" {cta("call-cta", ctx)}>Call or text {C.PHONE}</a>{mail}</p>')
    return section(dict(s, tone=s.get("tone", "deep")),
                   f'<div class="cta-box"><h2 id="{hid}">{s["h2"]}</h2><p>{s["text"]}</p>'
                   f'<div class="btn-row center">{button(ctx, s["primary"], "btn-primary")}</div>{contact}</div>',
                   hid=hid)


def r_slot(ctx, s):
    head, hid = heading(ctx, s)
    return section(s, head + slot_html(s, heading_level=3 if hid else 2), hid=hid)


def r_disclaimers(ctx, s):
    head, hid = heading(ctx, s)
    items = "".join(f"<li>{i}</li>" for i in s["items"])
    options = "".join(f'<div class="option"><p class="option-label">{o["label"]}</p><p>{o["text"]}</p></div>'
                      for o in s.get("options", []))
    return section(s, f'<div class="prose">{head}<ul class="checklist">{items}</ul>'
                      f'<h3>{s.get("options_h", "Options")}</h3>{options}</div>', hid=hid)


def r_policy(ctx, s):
    """A real policy document: "Last updated", then one h2 per section.

    Unlike r_legal (which renders an outline of headings still to be written), this renders
    finished prose. Items in [square brackets] are decisions the owner or an attorney still
    has to make, so they are marked up rather than left to blend into the text.
    """
    blocks = []
    for part in s["sections"]:
        hid = ctx.unique_id(part["h"])
        paragraphs = "".join(f"<p>{mark_open_items(p)}</p>" for p in part.get("p", []))
        bullets = (f'<ul class="softlist">{"".join(f"<li>{mark_open_items(b)}</li>" for b in part["ul"])}</ul>'
                   if part.get("ul") else "")
        blocks.append(f'<h2 id="{hid}">{part["h"]}</h2>{paragraphs}{bullets}')
    updated = f'<p class="policy-updated">Last updated: {s["updated"]}</p>'
    return section(s, f'<div class="prose policy">{updated}{"".join(blocks)}</div>')


def mark_open_items(text):
    """Wrap [bracketed] decisions so they read as notes, not as part of the policy."""
    return re.sub(r"\[([^\]]+)\]", r'<span class="open-item">[\1]</span>', text)


def r_options(ctx, s):
    """Two wordings of the same statement, each labelled with where it came from.

    Used for the confidentiality statement, where the owner's guide and her brief cite
    different authorities and both are published until an attorney settles it.
    """
    head, hid = heading(ctx, s)
    blocks = "".join(f'<div class="option"><p class="option-label">{label}</p><p>{text}</p></div>'
                     for label, text in s["options"])
    return section(s, f'<div class="prose">{head}{blocks}</div>', hid=hid)


def r_legal(ctx, s):
    head, hid = heading(ctx, s)
    blocks = "".join(f'<h3>{title}</h3><p class="placeholder-text">{note}</p>' for title, note in s["outline"])
    return section(s, f'<div class="prose legal">{head}{blocks}</div>', hid=hid)


def r_credgroups(ctx, s):
    """The founder's trainings, credentials, and affiliations, straight from the owner.

    Each group's id is the anchor the About dropdown deep-links to, so the submenu and the page
    can never fall out of step: both read content.common.FOUNDER_GROUPS.
    """
    blocks = []
    for gid, title, items in s["groups"]:
        rows = "".join(f"<li>{i}</li>" for i in items)
        blocks.append(f'<div class="credgroup" id="{gid}"><h3>{title}</h3>'
                      f'<ul class="checklist">{rows}</ul></div>')
        ctx.ids.add(gid)
    return section(s, f'<div class="credgroups">{"".join(blocks)}</div>')


def r_practices(ctx, s):
    """The two sister practices, presented as equals. Neither card outranks the other."""
    head, hid = heading(ctx, s)
    cards = []
    for p in s["items"]:
        services = "".join(f"<li>{x}</li>" for x in p["services"])
        cards.append(
            f'<li class="practice-card practice-{p["key"]}">'
            f'<h3><a href="{ctx.href("/" + p["path"])}" {cta("practice-" + p["key"], ctx)}>{p["name"]}</a></h3>'
            f'<ul class="checklist">{services}</ul>'
            f'<p class="practice-scope">{p["scope"]}</p>'
            f'<div class="btn-row">'
            f'<a class="btn btn-primary" href="{ctx.href("/" + p["path"])}" '
            f'{cta("explore-" + p["key"], ctx)}>{p["explore"]}</a>'
            f'<a class="btn btn-secondary" href="{ctx.href("/" + p["path"] + "/begin-intake")}" '
            f'{cta("screen-" + p["key"], ctx)}>Start screening</a></div>'
            f'<p class="practice-email"><a href="mailto:{p["email"]}" '
            f'{cta("email-" + p["key"], ctx)}>{p["email"]}</a></p></li>')
    return section(s, f'{head}<ul class="grid practices" role="list">{"".join(cards)}</ul>', hid=hid)


def r_router(ctx, s):
    """Three questions that send a visitor to the right screening, or to the free referrals."""
    head, hid = heading(ctx, s)
    steps = "".join(f'<li><h3>{i["title"]}</h3><p>{i["text"]}</p></li>' for i in s["items"])
    slot = f'<div class="section-slot">{slot_html(s["slot"])}</div>' if s.get("slot") else ""
    return section(s, f'{head}<ol class="steps router-steps">{steps}</ol>{slot}', hid=hid)


def r_hub_contact(ctx, s):
    """Both practice addresses side by side, so nobody has to guess which one to write to."""
    head, hid = heading(ctx, s)
    cards = []
    for p in s["items"]:
        cards.append(f'<li class="card practice-{p["key"]}"><h3>{p["name"]}</h3><p>{p["scope"]}</p>'
                     f'<p class="practice-email"><a href="mailto:{p["email"]}" '
                     f'{cta("contact-email-" + p["key"], ctx)}>{p["email"]}</a></p></li>')
    phone = (f'<p class="cta-contact"><a href="tel:{C.PHONE_TEL}" {cta("call-hub", ctx)}>'
             f'Call or text {C.PHONE_INTL}</a></p>')
    return section(s, f'{head}{phone}<ul class="grid" role="list">{"".join(cards)}</ul>', hid=hid)


def r_notprovided(ctx, s):
    """The five services neither practice provides. Verbatim from the owner's vision document."""
    # heading() renders "intro" as the section lede, and this renders it again below, so the
    # paragraph appeared twice on the page. Keep it out of the heading and print it once.
    head, hid = heading(ctx, dict(s, intro=None))
    rows = "".join(f"<li>{i}</li>" for i in s["items"])
    return section(s, f'<div class="prose">{head}<p>{s["intro"]}</p>'
                      f'<ul class="softlist not-provided">{rows}</ul></div>', hid=hid)


def r_hub_hero(ctx, s):
    """The hub hero. Unlike the practice heroes it has no photograph yet, so it shows a slot."""
    copy = "".join([
        f'<p class="eyebrow">{s["eyebrow"]}</p>' if s.get("eyebrow") else "",
        f'<h1>{s["h1"]}</h1>',
        f'<p class="tagline">{s["tagline"]}</p>' if s.get("tagline") else "",
        f'<p class="lede">{s["lede"]}</p>' if s.get("lede") else "",
        '<div class="btn-row">' + button(ctx, s["primary"], "btn-primary")
        + f'<a class="btn btn-secondary" href="tel:{C.PHONE_TEL}" {cta("call-hero", ctx)}>'
          f'Call or text {C.PHONE}</a></div>',
    ])
    if s.get("image"):
        media = f'<div class="hero-media">{img(ctx, s["image"], s["alt"], eager=True)}</div>'
    elif s.get("media_slot"):
        # No heading in the hero slot: it sits beside the h1, and an h3 there would break
        # the page's heading order.
        media = f'<div class="hero-media">{slot_html(s["media_slot"], heading_level=None)}</div>'
    else:
        media = ""
    # With no media the copy gets the full width instead of sitting in a half-empty grid.
    grid = "container hero-grid" if media else "container hero-copy-only"
    return (f'<section class="hero" data-wf="{attr(s.get("wf", ""))}"><div class="{grid}">'
            f'<div class="hero-copy">{copy}</div>{media}</div></section>')


def r_posts(ctx, s):
    head, hid = heading(ctx, s)
    chips = "".join(f"<li>{c}</li>" for c in s["cats"])
    cards = "".join(f'<li class="card post-card"><div class="ph" aria-hidden="true">Featured image</div>'
                    f'<p class="eyebrow">{c}</p><h3>Article title</h3>'
                    f'<p>Excerpt pulled from the post (one or two sentences).</p></li>' for c in s["cats"][:3])
    return section(s, f'{head}<ul class="chips" aria-label="Categories">{chips}</ul>'
                      f'<ul class="grid" role="list">{cards}</ul>', hid=hid)


def r_contact(ctx, s):
    site = ctx.site
    call_label = f'Call or text {site["name"]}'
    mail_label = f'Email {site["name"]}'
    items = [
        ("phone", "Phone or text",
         f'<a href="tel:{C.PHONE_TEL}" {cta("call", ctx, call_label)}>{C.PHONE_INTL}</a>'),
        ("mail", "Email",
         f'<a href="mailto:{site["email"]}" {cta("email", ctx, mail_label)}>{site["email"]}</a>'),
        ("clipboard", "Begin intake",
         f'Complete the online screening so we can confirm eligibility. '
         f'<a href="{ctx.href("begin-intake")}" {cta("intake-start", ctx)}>Start the screening</a>.'),
    ]
    contact_list = "".join(f'<li class="contact-item">{icon(i)}<div><strong>{t}</strong><p>{body}</p></div></li>'
                           for i, t, body in items)
    topics = "".join(f"<option>{t}</option>" for t in site["topics"])
    form = f'''<form class="wf-form mailto-form" data-email="{attr(site["email"])}" data-subject="Website enquiry — {attr(site["name"])}" novalidate aria-labelledby="form-title" data-wf="Form block: provider-agnostic form plugin">
<h2 id="form-title">Send a message</h2>
<p class="field-hint" id="form-privacy">Please share only a brief, general description. Don't include confidential details; we'll follow up to talk privately.</p>
<div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="f-phone">Phone <span class="optional">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
<div class="field"><label for="f-method">Preferred way to reach you</label><select id="f-method" name="method"><option>Email</option><option>Phone call</option><option>Text message</option></select></div>
<div class="field"><label for="f-topic">What can we help with?</label><select id="f-topic" name="topic">{topics}</select></div>
<div class="field"><label for="f-msg">Brief description</label><textarea id="f-msg" name="message" aria-describedby="form-privacy"></textarea></div>
<label class="check"><input type="checkbox" name="ack" required> <span>I understand this form is not for emergencies and that {site["name"]} does not provide legal advice or counseling.</span></label>
<button class="btn btn-primary" type="submit">Send message</button>
<p class="field-hint">Send opens your email app with your message ready to go to <a href="mailto:{attr(site["email"])}">{site["email"]}</a>. <strong>Press Send in your email app to finish</strong> — until then, nothing has been sent. Prefer to talk? Call or text <a href="tel:{C.PHONE_TEL}">{C.PHONE}</a>.</p>
<p class="form-error" role="alert" hidden></p>
</form>'''
    note = draft_flag("Suggested safety line for a trauma-informed site; owner to approve: "
                      "“If you are in immediate danger, call 911.”")
    head, hid = heading(ctx, {"h2": "Request a consultation"})
    return section(s, f'<div class="contact-grid"><div>{head}<ul class="contact-list">{contact_list}</ul>{note}'
                      f'<p class="muted">Serving clients with virtual and in‑person options.</p></div>{form}</div>',
                   hid=hid)


def party_block(n, roles, required=False):
    """One party's contact details. Party 1 is required; the rest are optional."""
    req = " required" if required else ""
    opt = "" if required else ' <span class="optional">(optional)</span>'
    role_opts = "".join(f"<option>{escape(r)}</option>" for r in roles)
    return f'''<fieldset class="party"><legend>Party {n}{opt}</legend>
<div class="party-grid">
<div class="field"><label for="p{n}-name">Full name</label><input id="p{n}-name" name="party{n}_name"{req}></div>
<div class="field"><label for="p{n}-role">Role</label><select id="p{n}-role" name="party{n}_role">{role_opts}</select></div>
<div class="field"><label for="p{n}-email">Email</label><input id="p{n}-email" name="party{n}_email" type="email"{req}></div>
<div class="field"><label for="p{n}-phone">Phone</label><input id="p{n}-phone" name="party{n}_phone" type="tel"></div>
<div class="field span-2"><label for="p{n}-address">Mailing address</label><input id="p{n}-address" name="party{n}_address"></div>
</div></fieldset>'''


def intake_question(q, n, roles):
    qid = f"q{n}"
    head = (f'<div class="q-head"><span class="q-num" aria-hidden="true">{n}</span>'
            f'<h3 id="{qid}-label">{q["q"]}</h3></div>')
    notes = (f'<ul class="q-notes">{"".join(f"<li>{x}</li>" for x in q["notes"])}</ul>') if q.get("notes") else ""
    hint = f'<p class="q-help">{q["help"]}</p>' if q.get("help") else ""
    if q.get("type") == "parties":
        parties = party_block(1, roles, required=True) + party_block(2, roles)
        extra = ('<div class="field"><label for="q-parties-more">Additional parties '
                 '<span class="optional">(optional)</span></label>'
                 '<textarea id="q-parties-more" name="parties_additional" '
                 'placeholder="Name, email, phone, mailing address, and role for each additional party"></textarea></div>')
        return f'<li class="q" data-q="{n}">{head}{hint}{notes}{parties}{extra}</li>'
    options = ['<option value="" selected disabled>Select an answer</option>']
    for o in q["options"]:
        data = ""
        if o.get("note"):
            data += f' data-note="{attr(o["note"])}"'
        if o.get("detail"):
            data += f' data-detail="{attr(o["detail"])}"'
        if o.get("required"):
            data += ' data-required="1"'
        if o.get("stop"):
            data += ' data-stop="1"'
        options.append(f'<option value="{attr(o["label"])}"{data}>{escape(o["label"])}</option>')
    select = (f'<div class="field"><label for="{qid}">Your answer</label>'
              f'<select id="{qid}" name="{qid}" required aria-describedby="{qid}-note">{"".join(options)}</select></div>')
    note = f'<p class="q-note" id="{qid}-note" role="status" hidden></p>'
    detail = (f'<div class="field q-detail" hidden><label for="{qid}-detail"></label>'
              f'<textarea id="{qid}-detail" name="{qid}_detail"></textarea></div>')
    return f'<li class="q" data-q="{n}">{head}{notes}{hint}{select}{note}{detail}</li>'


def r_intake(ctx, s):
    """Screening questionnaire. Dropdown answers reveal follow-up boxes; ineligible answers stop it."""
    site = ctx.site
    # "intro" here is a list of paragraphs rendered by paras() below, so keep it away from
    # heading(), which expects a single string and would print the list itself.
    head, hid = heading(ctx, dict(s, intro=None))
    questions = "".join(intake_question(q, i, s["roles"]) for i, q in enumerate(s["questions"], start=1))
    referrals = "".join(list_item(ctx, r) for r in s["stop_referrals"])
    linked = any(not isinstance(r, str) for r in s["stop_referrals"])
    stop = (f'<div class="stop-banner" role="status" hidden><h3>{s["stop_title"]}</h3><p>{s["stop_text"]}</p>'
            f'<ul class="{"referrals" if linked else "softlist"}">{referrals}</ul></div>')
    your_details = f'''<fieldset class="party"><legend>Your details</legend>
<div class="party-grid">
<div class="field"><label for="you-name">Full name</label><input id="you-name" name="your_name" autocomplete="name" required></div>
<div class="field"><label for="you-email">Email</label><input id="you-email" name="your_email" type="email" autocomplete="email" required></div>
<div class="field"><label for="you-phone">Phone</label><input id="you-phone" name="your_phone" type="tel" autocomplete="tel"></div>
<div class="field"><label for="you-contact">Preferred way to reach you</label><select id="you-contact" name="your_contact"><option>Email</option><option>Phone call</option><option>Text message</option></select></div>
</div></fieldset>'''
    form = f'''<form class="intake-form" data-email="{attr(site["email"])}" data-subject="Screening request — {attr(site["name"])}" novalidate data-wf="Form block: multi-step screening (provider-agnostic)">
{your_details}
<ol class="q-list">{questions}</ol>
{stop}
<div class="intake-actions">
<label class="check"><input type="checkbox" name="ack" required> <span>My answers are accurate to the best of my knowledge, and I understand that {site["name"]} screens every matter before offering services.</span></label>
<button class="btn btn-primary" type="submit">Submit screening</button>
<p class="field-hint">Submit opens your email app with your answers ready to go to <a href="mailto:{attr(site["email"])}">{site["email"]}</a>. <strong>Press Send in your email app to finish</strong> — until then, nothing has been sent. Prefer to talk? Call or text <a href="tel:{C.PHONE_TEL}">{C.PHONE}</a>.</p>
<p class="form-error" role="alert" hidden></p>
</div>
</form>'''
    outro = f'<p class="intake-outro">{s["outro"]}</p>' if s.get("outro") else ""
    return section(s, f'<div class="intake">{head}{paras(s.get("intro"))}{form}{outro}</div>', hid=hid)


def r_booking(ctx, s):
    """Google Calendar appointment scheduling.

    Set SITE["booking_url"] to the appointment schedule's embed URL (it ends in `?gv=true`) and the
    real calendar is embedded. Until then this renders the placeholder with the ways to get in touch.
    """
    site = ctx.site
    head, hid = heading(ctx, s)
    url = site.get("booking_url")
    if url:
        body = (f'<div class="booking-embed"><iframe src="{attr(url)}" width="100%" height="700" '
                f'loading="lazy" style="border:0" '
                f'title="Schedule a consultation with {attr(site["name"])}"></iframe></div>')
    else:
        body = (f'<div class="booking-placeholder">{icon("calendar")}'
                f'<p class="booking-title">Online booking is being set up.</p>'
                f'<p>In the meantime, call or text '
                f'<a href="tel:{C.PHONE_TEL}" {cta("call-booking", ctx)}>{C.PHONE}</a>, email '
                f'<a href="mailto:{site["email"]}" {cta("email-booking", ctx)}>{site["email"]}</a>, or '
                f'<a href="{ctx.href("begin-intake")}" {cta("intake-from-booking", ctx)}>start the '
                f'screening</a> and we will arrange a time with you.</p></div>')
    return section(s, f"{head}{body}{slot_html(C.BOOKING_SETUP)}", hid=hid)


RENDER = {
    "hero": r_hero, "page_hero": r_page_hero, "text": r_text, "cards": r_cards, "split": r_split,
    "steps": r_steps, "notlist": r_notlist, "faq": r_faq, "list": r_list, "crosslink": r_crosslink,
    "cta": r_cta, "slot": r_slot, "disclaimers": r_disclaimers, "legal": r_legal, "posts": r_posts,
    "contact": r_contact, "intake": r_intake, "booking": r_booking,
    # Hub and About additions, 2026-09-16.
    "hub_hero": r_hub_hero, "practices": r_practices, "router": r_router, "hub_contact": r_hub_contact,
    "notprovided": r_notprovided, "credgroups": r_credgroups, "policy": r_policy,
    "options": r_options,
}


# ---------- document chrome ----------

def schema(ctx):
    site, page = ctx.site, ctx.page
    base = site_url(site)
    org_id = base + "#organization"
    webpage = {
        "@type": page.get("schema_type", "WebPage"), "@id": ctx.url() + "#webpage", "url": ctx.url(),
        "name": page["title"], "description": page["description"], "inLanguage": "en-US",
        "isPartOf": {"@id": base + "#website"}, "about": {"@id": org_id},
    }
    faqs = [it for s in page["sections"] if s["type"] == "faq" and s.get("schema") for it in s["items"]]
    if faqs:
        webpage["@type"] = ["WebPage", "FAQPage"]
        webpage["mainEntity"] = [{"@type": "Question", "name": strip_tags(it["q"]),
                                  "acceptedAnswer": {"@type": "Answer", "text": strip_tags(it["a"])}} for it in faqs]
    contact_point = {"@type": "ContactPoint", "contactType": "customer service",
                     "telephone": C.PHONE_SCHEMA, "availableLanguage": "English"}
    org = {"@type": "ProfessionalService", "@id": org_id, "name": site["name"], "url": base,
           "logo": base + "assets/logo.png", "image": base + "assets/og-image.jpg",
           "description": site["footer_blurb"], "telephone": C.PHONE_SCHEMA,
           "founder": {"@id": base + "#founder"},
           "knowsAbout": site["keywords"], "contactPoint": contact_point,
           # The practice's own social profiles: this is what ties the site to them for search.
           "sameAs": [url for _, url in C.SOCIAL]}
    if site.get("email"):
        org["email"] = contact_point["email"] = site["email"]
    if not site.get("sister"):
        # The hub is the parent of both practices rather than a peer.
        org["subOrganization"] = [{"@type": "ProfessionalService", "name": p["name"], "url": p["href"],
                                   "email": p["email"]} for p in hub.PRACTICES]
    graph = [
        org,
        {"@type": "WebSite", "@id": base + "#website", "url": base, "name": site["name"], "inLanguage": "en-US",
         "publisher": {"@id": org_id}},
        webpage,
        {"@type": "Person", "@id": base + "#founder", "name": C.FOUNDER, "jobTitle": "Founder",
         "worksFor": {"@id": org_id}},
    ]
    if page["slug"] == "services":
        for s in page["sections"]:
            if s["type"] == "split" and s.get("id"):
                graph.append({"@type": "Service", "@id": f'{ctx.url()}#{s["id"]}', "url": f'{ctx.url()}#{s["id"]}',
                              "name": strip_tags(s["eyebrow"]), "serviceType": strip_tags(s["h2"]),
                              "description": strip_tags(s["paras"][0]), "provider": {"@id": org_id}})
    if page["slug"]:
        webpage["breadcrumb"] = {"@id": ctx.url() + "#breadcrumb"}
        graph.append({"@type": "BreadcrumbList", "@id": ctx.url() + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": base},
            {"@type": "ListItem", "position": 2, "name": page["label"], "item": ctx.url()}]})
    return {"@context": "https://schema.org", "@graph": graph}


def head(ctx):
    site, page = ctx.site, ctx.page
    title, desc, url = page["title"], page["description"], ctx.url()
    og_image = site_url(site) + "assets/og-image.jpg"
    gsc = (f'<meta name="google-site-verification" content="{site["gsc"]}">' if site.get("gsc")
           else "<!-- Search Console: add this domain's verification meta tag or DNS TXT record -->")
    if site.get("ga4_id"):
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={site["ga4_id"]}"></script>'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}"
              f"gtag('js',new Date());gtag('config','{site['ga4_id']}');</script>")
    else:
        ga = "<!-- GA4: set ga4_id (G-XXXXXXXXXX Measurement ID) in content; in WordPress use Site Kit -->"
    hero = next((s for s in page["sections"] if s["type"] == "hero"), None)
    # Preload the hero (LCP) image so it starts downloading before CSS is parsed.
    preload = (f'<link rel="preload" as="image" type="image/avif" fetchpriority="high" '
               f'imagesrcset="{srcset(ctx, hero["image"], "avif")}" imagesizes="{IMG_SIZES}">'
               f'<link rel="preload" as="image" type="image/webp" fetchpriority="high" '
               f'imagesrcset="{srcset(ctx, hero["image"], "webp")}" imagesizes="{IMG_SIZES}">') if hero else ""
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{attr(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="{attr(site["name"])}">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{attr(site["name"])} logo">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(title)}">
<meta name="twitter:description" content="{attr(desc)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="{ctx.a}favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="{ctx.a}favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{ctx.a}favicon-16.png">
<link rel="apple-touch-icon" href="{ctx.a}apple-touch-icon.png">
<link rel="manifest" href="{ctx.up}site.webmanifest">
<meta name="theme-color" content="{site["theme_color"]}">
{gsc}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{site["fonts"]}">
<link rel="stylesheet" href="{ctx.a}css/base.css">
<link rel="stylesheet" href="{ctx.a}css/{site["css"]}">
{preload}
{ga}
<script type="application/ld+json">{json.dumps(schema(ctx), ensure_ascii=False)}</script>
</head>
<body class="site-{site["key"]}">
'''


def nav_item(ctx, entry, n):
    """One top-level navigation entry. A 2-tuple is a plain link; a 3-tuple opens a dropdown.

    The dropdown is driven by a real <button aria-expanded>, and its first child links to the
    parent page itself, so the submenu is a shortcut and never the only way in. With JavaScript
    off, app.js never runs, the panel keeps its default open state, and nothing is unreachable.
    """
    slug, label = entry[0], entry[1]
    children = entry[2] if len(entry) > 2 else None
    current = ' aria-current="page"' if slug == ctx.page["slug"] else ""
    if not children:
        return f'<li><a href="{ctx.href(slug)}"{current}>{label}</a></li>'
    panel_id = f"nav-panel-{n}"
    rows = "".join(f'<li><a href="{ctx.href(child)}">{child_label}</a></li>' for child, child_label in children)
    return (f'<li class="has-sub" data-nav-sub>'
           f'<a href="{ctx.href(slug)}"{current}>{label}</a>'
           f'<button class="nav-sub-toggle" type="button" aria-expanded="false" aria-controls="{panel_id}">'
           f'<span class="visually-hidden">Show {strip_tags(label)} pages</span>'
           f'<svg viewBox="0 0 10 7" aria-hidden="true" focusable="false"><path d="M1 1.5 5 5.5 9 1.5" '
           f'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
           f'stroke-linejoin="round"/></svg></button>'
           f'<ul class="nav-sub" id="{panel_id}">{rows}</ul></li>')


def sister_band(ctx):
    """A slim cross-practice strip directly under the nav.

    The two practices are sisters, so each one promotes the other by name and by what it
    actually does. It sits below the header rather than inside it: the nav already carries six
    items and the consultation button, and a 60-character descriptor would wrap them.

    The hub has no sister — it is the parent of both — so it gets no band.
    """
    if not ctx.site.get("sister"):
        return ""
    name, url, desc = ctx.site["sister"]
    arrow = ('<svg class="sister-band-arrow" viewBox="0 0 16 12" aria-hidden="true" focusable="false">'
             '<path d="M1 6h13M9.5 1.5 14 6l-4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.6" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>')
    # The name and the descriptor are separate flex items, so without an explicit label a screen
    # reader runs them together ("…Leadership SystemsBusiness-to-business…").
    label = f"Sister practice: {strip_tags(name)} — {strip_tags(desc)}"
    return f'''<aside class="sister-band" data-wf="Pattern: tls/sister-band (header)">
<div class="container">
<a class="sister-band-link" href="{url}" {cta("sister-band", ctx, label)}>
<span class="sister-band-eyebrow">Sister practice</span>
<span class="sister-band-text"><strong>{name}</strong><span class="sister-band-desc">{desc}</span></span>
{arrow}</a>
</div>
</aside>
'''


def header(ctx):
    site = ctx.site
    items = [nav_item(ctx, entry, n) for n, entry in enumerate(site["nav"])]
    if site.get("nav_external"):
        url, label = site["nav_external"]
        items.append(f'<li><a href="{url}">{label} <span aria-hidden="true">↗</span></a></li>')
    banner = ('<div class="wf-banner" role="note">Wireframe preview, not the live site. '
              'Yellow “Review” notes need owner or legal sign-off.</div>') if WIREFRAME else ""
    # The hub has no mailbox of its own, so its utility bar carries the phone number alone.
    utility_email = (f'<a href="mailto:{site["email"]}" {cta("email-utility", ctx)}>{site["email"]}</a>'
                     if site.get("email") else
                     '<span class="utility-note">Virtual &amp; in‑person options</span>')
    # No LetTLSHelp logo file exists yet, so the hub renders its brand as type.
    mark = "" if site.get("wordmark") else f'<img src="{ctx.a}logo-mark.png" width="48" height="48" alt="">'
    return f'''<a class="skip-link" href="#main">Skip to main content</a>
{banner}
<div class="utility-bar"><div class="container"><a href="tel:{C.PHONE_TEL}" {cta("call-utility", ctx)}>Call or text {C.PHONE}</a>{utility_email}</div></div>
<header class="site-header" data-wf="Template part: header (Site logo + Navigation block)">
<div class="container header-inner">
<a class="brand{" brand-wordmark" if site.get("wordmark") else ""}" href="{ctx.href("")}">{mark}<span class="brand-text">{site["word_top"]}<small>{site["word_bottom"]}</small></span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">Menu</button>
<nav id="primary-nav" aria-label="Main"><ul>{"".join(items)}</ul></nav>
<a class="btn btn-primary header-cta" href="{ctx.href(site["cta"][0])}" {cta("header-consultation", ctx)}>{site["cta"][1]}</a>
</div>
</header>
{sister_band(ctx)}'''


def footer(ctx):
    site = ctx.site
    # Footer navigation stays flat: top-level entries only, so it doesn't restate the dropdowns.
    nav = "".join(f'<li><a href="{ctx.href(entry[0])}">{entry[1]}</a></li>' for entry in site["nav"])
    # The policy pages live at the domain root and serve both practices, so they are root-relative.
    policies = "".join(f'<li><a href="{ctx.href("/" + slug)}">{label}</a></li>' for slug, label in site["policies"])
    if site.get("wordmark"):
        brand = f'<p class="footer-wordmark">{site["word_top"]}</p>'
    else:
        logo_w, logo_h = ctx.manifest["_logo"]
        brand = (f'<img class="footer-logo" src="{ctx.a}logo.png" width="{logo_w}" height="{logo_h}" '
                 f'alt="{attr(site["name"])}">')
    if site.get("sister"):
        email_row = (f'<li><a href="mailto:{site["email"]}" {cta("email-footer", ctx)}>{site["email"]}</a></li>'
                     f'<li class="footer-muted">Virtual &amp; in‑person options</li>')
    else:
        # The hub's footer offers both practice addresses, so anyone who already knows which
        # practice they need can write to it directly.
        email_row = "".join(
            f'<li><a href="mailto:{p["email"]}" {cta("email-footer-" + p["key"], ctx)}>{p["email"]}</a></li>'
            for p in hub.PRACTICES) + '<li class="footer-muted">Virtual &amp; in‑person options</li>'
    if site.get("sister"):
        sister_name, sister_url, sister_desc = site["sister"]
        sister = (f'<h2 class="footer-h">Sister practice</h2><p><a href="{sister_url}">{sister_name}</a><br>'
                  f'<span class="footer-muted">{sister_desc}</span></p>')
    else:
        rows = "".join(f'<li><a href="{ctx.href("/" + p["path"])}">{p["name"]}</a></li>' for p in hub.PRACTICES)
        sister = f'<h2 class="footer-h">Our practices</h2><ul>{rows}</ul>'
    follow = "".join(f'<li><a href="{url}" rel="noopener" {cta("social-" + label.lower(), ctx)}>{label}</a></li>'
                     for label, url in C.SOCIAL)
    toggle = '<button class="wf-toggle" type="button" aria-pressed="false">Show wireframe notes</button>' if WIREFRAME else ""
    return f'''<footer class="site-footer" data-wf="Template part: footer">
<div class="container footer-grid">
<div>{brand}<p>{site["footer_blurb"]}</p></div>
<nav aria-label="Footer"><h2 class="footer-h">Explore</h2><ul>{nav}</ul></nav>
<div><h2 class="footer-h">Contact</h2><ul><li><a href="tel:{C.PHONE_TEL}" {cta("call-footer", ctx)}>Call or text {C.PHONE}</a></li>{email_row}</ul>
<h2 class="footer-h">Follow</h2><ul>{follow}</ul></div>
<div><h2 class="footer-h">Policies</h2><ul>{policies}</ul>
{sister}</div>
</div>
<div class="container footer-legal"><p>{site["short_disclaimer"]}</p><p>© {YEAR} {site["name"]}. All rights reserved.</p></div>
</footer>
{toggle}
<script src="{ctx.a}js/app.js" defer></script>
</body>
</html>
'''


def render_page(site, page):
    ctx = Ctx(site, page)
    body = "".join(RENDER[s["type"]](ctx, s) for s in page["sections"])
    html = head(ctx) + header(ctx) + f'<main id="main" tabindex="-1">{body}</main>\n' + footer(ctx)
    if WIREFRAME:
        # Preview only: cross-practice links point at the local wireframe folders, so nothing 404s
        # before launch. Canonical, Open Graph, sitemap, and schema URLs keep the real
        # lettlshelp.com paths. Ctx.root already knows how deep this page sits.
        for other in MODULES:
            if other.SITE is not site and other.SITE["slug"]:
                target = re.escape(site_url(other.SITE))
                local = ctx.root + other.SITE["slug"] + "/"
                html = re.sub(rf'(<a\s[^>]*?href="){target}"', rf'\g<1>{local}"', html)
    else:
        # The pattern labels are notes to whoever builds the WordPress theme, not site content.
        html = re.sub(r'\s+data-wf="[^"]*"', "", html)
    dest = OUT.joinpath(site["slug"], page["slug"], "index.html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    return dest


HUB_ICONS = ["favicon.ico", "favicon-16.png", "favicon-32.png", "apple-touch-icon.png",
             "icon-192.png", "icon-512.png", "og-image.jpg"]


def site_files(site, pages):
    root = OUT.joinpath(site["slug"])
    (root / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (root / "assets" / "js").mkdir(parents=True, exist_ok=True)
    shutil.copy2(DESIGN / "base.css", root / "assets" / "css" / "base.css")
    shutil.copy2(DESIGN / site["css"], root / "assets" / "css" / site["css"])
    shutil.copy2(DESIGN / "app.js", root / "assets" / "js" / "app.js")
    if site.get("brand_from"):
        # The hub has no brand files of its own: it carries the Transformative Life Solutions
        # logo, icons and OG image (owner's instruction, 2026-09-22). The image manifest comes
        # too, because the footer reads the logo's dimensions from it.
        source_assets = OUT / site["brand_from"] / "assets"
        (root / "assets" / "img").mkdir(parents=True, exist_ok=True)
        for name in HUB_ICONS + ["logo.png", "logo-mark.png", "img/manifest.json"]:
            source = source_assets / name
            if source.exists():
                shutil.copy2(source, root / "assets" / name)
    manifest = {"name": site["name"], "short_name": site["word_bottom"],
                "start_url": site.get("base", "") + "/", "display": "browser",
                "background_color": "#FFFFFF", "theme_color": site["theme_color"],
                "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    (root / "site.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def redirect_rules():
    """301s for every URL that moved when the root became the shared hub.

    Life Solutions used to BE the root, so each of its pages moved down a level; Ethics,
    Privacy and Terms & Disclaimers moved up from both practices into one shared copy.
    """
    # A slug the hub now serves must NOT be redirected, or the hub's own page becomes
    # unreachable. /contact/ is the live case: it used to be Life Solutions' contact page and
    # is now the hub's routing one, which is a fine landing place for the old traffic.
    hub_slugs = {p["slug"] for p in hub.PAGES}
    moved_out = [p["slug"] for p in life.PAGES if p["slug"] and p["slug"] not in hub_slugs]
    rules = ["# Life Solutions moved from the root into /life-solutions/",
             "# (/contact/ is left alone: the hub serves it now)"]
    rules += [f"RewriteRule ^{slug}/?$ /life-solutions/{slug}/ [L,R=301]" for slug in moved_out]
    rules.append("# Policy pages folded into one shared copy at the root")
    for practice in ("life-solutions", "leadership-systems"):
        rules.append(f"RewriteRule ^{practice}/ethics/?$ /ethics/ [L,R=301]")
        rules.append(f"RewriteRule ^{practice}/terms-disclaimers/?$ /disclaimers/ [L,R=301]")
        rules.append(f"RewriteRule ^{practice}/privacy-policy/?$ /privacy-policy/ [L,R=301]")
    rules.append("# Old root policy URLs (Life Solutions served them before the move)")
    rules.append("RewriteRule ^terms-disclaimers/?$ /disclaimers/ [L,R=301]")
    rules.append("# Resources was retired on 2026-09-16")
    for practice in ("life-solutions", "leadership-systems"):
        rules.append(f"RewriteRule ^{practice}/resources/?$ /{practice}/ [L,R=410]")
    rules.append("RewriteRule ^resources/?$ / [L,R=410]")
    return "\n".join(rules)


def shared_files(modules):
    """One sitemap, robots.txt, and .htaccess: both practices share lettlshelp.com."""
    domain = modules[0].SITE["domain"]
    host = domain.split("//", 1)[1]
    today = date.today().isoformat()
    redirects = redirect_rules()
    urls = "".join(f'  <url><loc>{site_url(m.SITE, p["slug"])}</loc><lastmod>{today}</lastmod></url>\n'
                   for m in modules for p in m.PAGES)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     f'{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text("# Production robots.txt (WordPress/SEO plugin generates the live one)\n"
                                    f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n",
                                    encoding="utf-8")
    (OUT / ".htaccess").write_text(f"""# Production .htaccess for {host} (Apache / LiteSpeed, e.g. Hostinger).
# Place these rules ABOVE the "# BEGIN WordPress" block; leave the WordPress block unchanged.

<IfModule mod_rewrite.c>
RewriteEngine On
# Enforce HTTPS (301)
RewriteCond %{{HTTPS}} !=on
RewriteCond %{{HTTP:X-Forwarded-Proto}} !https
RewriteRule ^ https://%{{HTTP_HOST}}%{{REQUEST_URI}} [L,R=301]
# One canonical host: https://{host} (no www)
RewriteCond %{{HTTP_HOST}} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{{REQUEST_URI}} [L,R=301]
</IfModule>

<IfModule mod_headers.c>
# HSTS: add "; includeSubDomains; preload" only once every subdomain serves HTTPS
Header always set Strict-Transport-Security "max-age=31536000"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), interest-cohort=()"
Header always set Cross-Origin-Opener-Policy "same-origin"

# Content Security Policy for the PUBLIC pages. Allows Google Fonts, Google Analytics/Tag Manager,
# and the Google Calendar booking embed. 'unsafe-inline' is needed for the JSON-LD schema and the
# analytics snippet; drop it once those use nonces.
# Test before enabling: wp-admin relies on inline scripts, so scope this to the front end
# (<If "%{{REQUEST_URI}} !~ m#^/wp-admin#">) or set it from the theme instead.
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://www.googletagmanager.com https://*.google-analytics.com; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://www.googletagmanager.com; frame-src https://calendar.google.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'; upgrade-insecure-requests"
</IfModule>

# --- Moved pages (301) ---------------------------------------------------------------
# The domain root became the shared hub on 2026-09-16, so Life Solutions moved out of it,
# and Ethics / Disclaimers / Privacy moved in from both practices. Keep these until the
# old URLs stop appearing in Search Console.
<IfModule mod_rewrite.c>
RewriteEngine On
{redirects}
</IfModule>

# Block access to files that should never be public
<FilesMatch "^(\\.env|\\.git.*|wp-config\\.php|readme\\.html|license\\.txt|xmlrpc\\.php)$">
Require all denied
</FilesMatch>

# Compression + browser caching (Core Web Vitals)
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/xml application/javascript application/json application/ld+json image/svg+xml
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/x-icon "access plus 1 year"
ExpiresByType text/css "access plus 1 month"
ExpiresByType application/javascript "access plus 1 month"
ExpiresByType text/html "access plus 0 seconds"
</IfModule>

# When TransformativeLifeSolutions.com / TransformativeLeadershipSystems.com go live, 301-redirect
# these paths to the new domains and update "domain"/"base" in content/{{life,leadership}}.py.
""", encoding="utf-8")


def page_index():
    """A developer list of every page, for previewing. Not part of the site.

    The domain root is the real Home page now, so this can no longer live at index.html.
    """
    blocks = []
    for module in MODULES:
        s = module.SITE
        prefix = s["slug"] + "/" if s["slug"] else ""
        links = "".join(f'<li><a href="{prefix}{p["slug"] + "/" if p["slug"] else ""}">{p["label"]}</a></li>'
                        for p in module.PAGES)
        blocks.append(f'<section><h2>{s["name"]}</h2><p><code>{site_url(s)}</code></p><ul>{links}</ul></section>')
    html = f'''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TLS wireframe page index</title>
<style>body{{font:16px/1.6 system-ui,sans-serif;margin:0;background:#F4F7F8;color:#1C2B33}}main{{max-width:960px;margin:0 auto;padding:3rem 1.5rem}}
.grid{{display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}}section{{background:#fff;border-radius:16px;padding:1.5rem 1.75rem;border:1px solid #D5E0E2}}
h1{{font-family:Georgia,serif;color:#003853}}h2{{font-family:Georgia,serif;margin:.2rem 0}}a{{color:#006B7B}}li{{margin:.25rem 0}}</style></head>
<body><main><h1>Page index</h1>
<p>Every page in the build, for review. The real entry point is <a href="./">the Home page</a>. Use “Show wireframe notes” (bottom right) on any page to see the planned WordPress block pattern for each section. Yellow “Review” notes need owner or legal sign-off; the full list is in <code>docs/consistency-review.md</code>.</p>
<div class="grid">{"".join(blocks)}</div></main></body></html>
'''
    (OUT / "page-index.html").write_text(html, encoding="utf-8")


def main():
    # Practices first: the hub borrows their icon set until it has one of its own.
    for module in PRACTICES + [hub]:
        site_files(module.SITE, module.PAGES)
    for module in MODULES:
        for page in module.PAGES:
            print("wrote", render_page(module.SITE, page).relative_to(ROOT))
    shared_files(MODULES)
    page_index()


if __name__ == "__main__":
    main()
