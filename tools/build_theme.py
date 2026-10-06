#!/usr/bin/env python3
"""Generate the WordPress block theme from the same source as the static site.

    python tools/build_theme.py

Writes wp-content/themes/:

    tls-base/          parent block theme: layout, typography, components, header/footer,
                       templates, and the block patterns each section maps to
    tls-hub/           child: LetTLSHelp (the domain root)
    tls-life/          child: Transformative Life Solutions
    tls-leadership/    child: Transformative Leadership Systems

Why generate rather than hand-write: the palettes come from design-system/tokens.json and the
brand layers are the very CSS files the static build uses, so the theme cannot drift away from
the site the owner has already approved. Re-run this after changing tokens or CSS.

The patterns hold the same markup and class names as the static pages, so design-system/base.css
styles them unchanged. Headings, paragraphs and buttons are real core blocks, which is the point
of moving to WordPress: the owner edits text in the block editor without touching layout.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "content"))

import common as C  # noqa: E402
import hub  # noqa: E402
import leadership  # noqa: E402
import life  # noqa: E402

DESIGN = ROOT / "design-system"
THEMES = ROOT / "wp-content" / "themes"
TOKENS = json.loads((DESIGN / "tokens.json").read_text("utf-8"))
VERSION = "1.0.0"

# WordPress runs ONE theme at a time, so the three brands cannot be three active child themes on
# one install. Instead a single child ships all three brand layers, each scoped to a body class,
# and functions.php sets that class from the URL path — the same mechanism the static site uses
# (`body class="site-life"`). One install, one theme, three brands.
CHILD = ("tls-lettlshelp", "LetTLSHelp", "life-solutions")

# section key -> (url prefix, site module, brand CSS file)
SECTIONS = [
    ("hub", "", hub, "hub.css"),
    ("life", "life-solutions", life, "life.css"),
    ("leadership", "leadership-systems", leadership, "leadership.css"),
]


def slugify(value):
    out = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def style_header(name, description, template=None):
    tpl = f"Template: {template}\n" if template else ""
    return f"""/*
Theme Name: {name}
Description: {description}
{tpl}Author: Tanika L. Smith
Version: {VERSION}
Requires at least: 6.5
Tested up to: 6.6
Requires PHP: 7.4
License: GPL-2.0-or-later
Text Domain: {slugify(name)}
*/
"""


# ---------------------------------------------------------------- parent theme

def base_theme_json():
    """Layout, spacing and typography only. Colours belong to the child themes."""
    shared = TOKENS["shared"]
    return {
        "$schema": "https://schemas.wp.org/trunk/theme.json",
        "version": 3,
        "settings": {
            "appearanceTools": True,
            "layout": {"contentSize": "46rem", "wideSize": shared["containerWidth"]},
            "useRootPaddingAwareAlignments": True,
            "color": {"custom": True, "customGradient": False, "defaultPalette": False,
                      "defaultGradients": False, "link": True},
            "spacing": {"padding": True, "margin": True, "units": ["px", "rem", "%", "vw"],
                        "spacingSizes": [
                            {"slug": "30", "size": "1rem", "name": "Small"},
                            {"slug": "40", "size": "1.75rem", "name": "Medium"},
                            {"slug": "50", "size": "3rem", "name": "Large"},
                            {"slug": "60", "size": "4.5rem", "name": "Section"},
                        ]},
            "typography": {
                "fluid": True,
                "customFontSize": True,
                "fontSizes": [
                    {"slug": "small", "size": "0.9rem", "name": "Small"},
                    {"slug": "medium", "size": "1.0625rem", "name": "Body"},
                    {"slug": "large", "size": "1.35rem", "name": "Large"},
                    {"slug": "x-large", "size": "clamp(1.9rem, 1.4rem + 2vw, 2.6rem)", "name": "Heading"},
                    {"slug": "xx-large", "size": "clamp(2.4rem, 1.6rem + 3.2vw, 3.4rem)", "name": "Display"},
                ],
            },
            "blocks": {"core/button": {"border": {"radius": True}}},
        },
        "styles": {
            "spacing": {"blockGap": "1.25rem",
                        "padding": {"left": "1.25rem", "right": "1.25rem"}},
            "typography": {"fontFamily": "var(--f-body)", "lineHeight": "1.65",
                           "fontSize": "var(--wp--preset--font-size--medium)"},
            "color": {"text": "var(--c-text)", "background": "#FFFFFF"},
            "elements": {
                "link": {"color": {"text": "var(--c-primary)"},
                         ":hover": {"color": {"text": "var(--c-primary-hover)"}}},
                "heading": {"typography": {"fontFamily": "var(--f-head)", "lineHeight": "1.2",
                                           "fontWeight": "600"},
                            "color": {"text": "var(--c-deep)"}},
                "button": {"border": {"radius": "999px"},
                           "color": {"background": "var(--c-primary)", "text": "#FFFFFF"},
                           ":hover": {"color": {"background": "var(--c-primary-hover)"}}},
            },
        },
        "templateParts": [
            {"name": "header", "title": "Header", "area": "header"},
            {"name": "footer", "title": "Footer", "area": "footer"},
        ],
        "customTemplates": [
            {"name": "page-wide", "title": "Page (full width)", "postTypes": ["page"]},
        ],
    }


FUNCTIONS_PHP = """<?php
/**
 * tls-base: setup and asset loading.
 *
 * The stylesheet is design-system/base.css, the same file the static site uses, so the two
 * cannot drift apart. Each child theme adds only its brand layer: the --c-* custom properties
 * and the two typefaces.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'TLS_BASE_VERSION', '%(version)s' );

add_action( 'after_setup_theme', function () {
    add_theme_support( 'wp-block-styles' );
    add_theme_support( 'responsive-embeds' );
    add_theme_support( 'editor-styles' );
    add_editor_style( 'assets/css/base.css' );
    add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'style', 'script' ) );
} );

/**
 * A cache-busting version for one theme file: when it last changed on disk.
 *
 * A fixed version string means every edit ships under the same address, so browsers and the
 * page cache keep serving the copy they already have and an uploaded stylesheet appears to do
 * nothing. Keying on the file's own timestamp means a changed file always arrives, and an
 * unchanged one still caches for as long as the host allows.
 */
function tls_asset_version( $file ) {
    $stamp = @filemtime( $file );
    return $stamp ? (string) $stamp : TLS_BASE_VERSION;
}

add_action( 'wp_enqueue_scripts', function () {
    $base = get_template_directory_uri();
    $child = get_stylesheet_directory_uri();
    $base_dir = get_template_directory();
    $child_dir = get_stylesheet_directory();

    // Typefaces. Self-hosting these is the next improvement: it removes a third-party request
    // and lets the Privacy Policy drop its Google Fonts section.
    $fonts = apply_filters( 'tls_google_fonts_url', '' );
    if ( $fonts ) {
        wp_enqueue_style( 'tls-fonts', $fonts, array(), null );
    }

    wp_enqueue_style( 'tls-base', $base . '/assets/css/base.css', array(),
        tls_asset_version( $base_dir . '/assets/css/base.css' ) );
    if ( $child !== $base ) {
        wp_enqueue_style( 'tls-brand', $child . '/style.css', array( 'tls-base' ),
            tls_asset_version( $child_dir . '/style.css' ) );
    }
    wp_enqueue_script( 'tls-app', $base . '/assets/js/app.js', array(),
        tls_asset_version( $base_dir . '/assets/js/app.js' ), true );
} );

/**
 * Group the practice's own patterns together in the inserter, away from the core ones.
 */
add_action( 'init', function () {
    if ( function_exists( 'register_block_pattern_category' ) ) {
        register_block_pattern_category( 'tls', array( 'label' => __( 'TLS sections', 'tls-base' ) ) );
    }
} );

/**
 * Referral and sister-practice links leave the site, so they never leak which page someone
 * came from, and never hand the opened tab a reference back to this one.
 */
add_filter( 'the_content', function ( $content ) {
    return str_replace( '<a class="referral-link" href=', '<a class="referral-link" rel="noopener noreferrer" href=', $content );
} );
"""


def nav_link(label, url):
    return (f'<!-- wp:navigation-link {{"label":"{label}","url":"{url}","kind":"custom"}} /-->')


def header_part():
    """The header, with its menu written out explicitly.

    An empty Navigation block falls back to listing every page on the site alphabetically,
    which wraps onto several lines and crushes the button. Writing the items here means the
    menu is correct the moment the theme is activated, with nothing to configure.
    """
    def submenu(label, path, children):
        items = "".join(nav_link(t, f"/{path}/{slug}/" if slug else f"/{path}/")
                        for t, slug in children)
        return (f'<!-- wp:navigation-submenu {{"label":"{label}","url":"/{path}/","kind":"custom"}} -->'
                f'{items}'
                f'<!-- /wp:navigation-submenu -->')

    practice_pages = [("Overview", ""), ("About", "about"), ("Services", "services"),
                      ("How It Works", "how-it-works"), ("FAQ", "faq"), ("Contact", "contact"),
                      ("Begin Intake", "begin-intake")]
    items = "".join([
        nav_link("Home", "/"),
        submenu("Life Solutions", "life-solutions", practice_pages),
        submenu("Leadership Systems", "leadership-systems", practice_pages),
        nav_link("Ethics &amp; Compliance", "/ethics/"),
        nav_link("Contact", "/contact/"),
    ])
    return f"""<!-- wp:group {{"tagName":"header","className":"site-header","layout":{{"type":"constrained"}}}} -->
<header class="wp-block-group site-header">
  <!-- wp:group {{"className":"container header-inner","layout":{{"type":"flex","flexWrap":"nowrap","justifyContent":"space-between","verticalAlignment":"center"}}}} -->
  <div class="wp-block-group container header-inner">
    <!-- wp:site-logo {{"width":48,"className":"brand-mark"}} /-->
    <!-- wp:navigation {{"overlayMenu":"mobile","className":"primary-nav","layout":{{"type":"flex","justifyContent":"center","flexWrap":"nowrap"}}}} -->
    {items}
    <!-- /wp:navigation -->
    <!-- wp:buttons {{"className":"header-cta"}} -->
    <div class="wp-block-buttons header-cta">
      <!-- wp:button -->
      <div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/contact/">Request a Consultation</a></div>
      <!-- /wp:button -->
    </div>
    <!-- /wp:buttons -->
  </div>
  <!-- /wp:group -->
</header>
<!-- /wp:group -->
"""


def footer_part():
    """The footer, with every link written out.

    Like the header, an empty Navigation block here would list every page alphabetically.
    The practice addresses and the disclaimer come from content/, so they match the rest
    of the site and change in one place.
    """
    def links(pairs):
        return "".join(
            f'<!-- wp:paragraph --><p><a href="{url}">{label}</a></p><!-- /wp:paragraph -->\n      '
            for label, url in pairs)

    # Ethics & Compliance is deliberately absent here: it is listed under Policies below, and
    # carrying it in both columns listed it twice in the same footer (owner's review, 2026-10-05).
    explore = links([("Life Solutions", "/life-solutions/"),
                     ("Leadership Systems", "/leadership-systems/"),
                     ("Contact", "/contact/")])
    policies = links([(label, f"/{slug}/") for slug, label in C.ROOT_POLICIES])
    social = "".join(
        f'<!-- wp:paragraph --><p><a href="{url}" rel="noopener">{label}</a></p><!-- /wp:paragraph -->\n      '
        for label, url in C.SOCIAL)
    emails = "".join(
        f'<!-- wp:paragraph --><p><a href="mailto:{addr}">{addr}</a></p><!-- /wp:paragraph -->\n      '
        for addr in (C.EMAIL_LIFE, C.EMAIL_LEADERSHIP))
    return f"""<!-- wp:group {{"tagName":"footer","className":"site-footer","layout":{{"type":"constrained"}}}} -->
<footer class="wp-block-group site-footer">
  <!-- wp:columns {{"className":"container footer-grid"}} -->
  <div class="wp-block-columns container footer-grid">
    <!-- wp:column -->
    <div class="wp-block-column">
      <!-- wp:site-logo {{"width":170,"className":"footer-logo"}} /-->
      <!-- wp:paragraph --><p>{hub.SITE["footer_blurb"]}</p><!-- /wp:paragraph -->
    </div>
    <!-- /wp:column -->
    <!-- wp:column -->
    <div class="wp-block-column">
      <!-- wp:heading {{"level":2,"className":"footer-h"}} --><h2 class="wp-block-heading footer-h">Explore</h2><!-- /wp:heading -->
      {explore}
    </div>
    <!-- /wp:column -->
    <!-- wp:column -->
    <div class="wp-block-column">
      <!-- wp:heading {{"level":2,"className":"footer-h"}} --><h2 class="wp-block-heading footer-h">Contact</h2><!-- /wp:heading -->
      <!-- wp:paragraph --><p><a href="tel:{C.PHONE_TEL}">Call or text {C.PHONE}</a></p><!-- /wp:paragraph -->
      {emails}
      <!-- wp:heading {{"level":2,"className":"footer-h"}} --><h2 class="wp-block-heading footer-h">Follow</h2><!-- /wp:heading -->
      {social}
    </div>
    <!-- /wp:column -->
    <!-- wp:column -->
    <div class="wp-block-column">
      <!-- wp:heading {{"level":2,"className":"footer-h"}} --><h2 class="wp-block-heading footer-h">Policies</h2><!-- /wp:heading -->
      {policies}
    </div>
    <!-- /wp:column -->
  </div>
  <!-- /wp:columns -->
  <!-- wp:group {{"className":"container footer-legal","layout":{{"type":"constrained"}}}} -->
  <div class="wp-block-group container footer-legal">
    <!-- wp:paragraph --><p>{hub.SITE["short_disclaimer"]}</p><!-- /wp:paragraph -->
  </div>
  <!-- /wp:group -->
</footer>
<!-- /wp:group -->
"""


TEMPLATES = {
    "index.html": """<!-- wp:template-part {"slug":"header","tagName":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
  <!-- wp:query {"query":{"inherit":true}} -->
  <div class="wp-block-query">
    <!-- wp:post-template -->
      <!-- wp:post-title {"isLink":true,"level":2} /-->
      <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
""",
    "page.html": """<!-- wp:template-part {"slug":"header","tagName":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
  <!-- wp:post-content {"layout":{"type":"constrained"}} /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
""",
    "404.html": """<!-- wp:template-part {"slug":"header","tagName":"header"} /-->
<!-- wp:group {"tagName":"main","className":"section tone-white","layout":{"type":"constrained"}} -->
<main class="wp-block-group section tone-white">
  <!-- wp:heading {"level":1} --><h1 class="wp-block-heading">That page isn't here</h1><!-- /wp:heading -->
  <!-- wp:paragraph --><p>The page may have moved. Try the menu above, or call or text us and we'll point you to the right place.</p><!-- /wp:paragraph -->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
""",
}
TEMPLATES["page-wide.html"] = TEMPLATES["page.html"]
TEMPLATES["front-page.html"] = TEMPLATES["page.html"]
TEMPLATES["single.html"] = TEMPLATES["page.html"]


def pattern(slug, title, body, categories="tls"):
    return f"""<?php
/**
 * Title: {title}
 * Slug: tls-base/{slug}
 * Categories: {categories}
 */
?>
{body}"""


def patterns():
    """One pattern per section the site uses. Names match the labels on the wireframe."""
    out = {}

    out["hero-split"] = pattern("hero-split", "Hero (split)", """
<!-- wp:group {"tagName":"section","className":"hero","layout":{"type":"constrained"}} -->
<section class="wp-block-group hero">
  <!-- wp:columns {"className":"container hero-grid"} -->
  <div class="wp-block-columns container hero-grid">
    <!-- wp:column {"className":"hero-copy"} -->
    <div class="wp-block-column hero-copy">
      <!-- wp:paragraph {"className":"eyebrow"} --><p class="eyebrow">Private ADR &middot; Mediation &middot; Conflict Coaching</p><!-- /wp:paragraph -->
      <!-- wp:heading {"level":1,"fontSize":"xx-large"} --><h1 class="wp-block-heading has-xx-large-font-size">Headline goes here</h1><!-- /wp:heading -->
      <!-- wp:paragraph {"className":"tagline"} --><p class="tagline">A short tagline.</p><!-- /wp:paragraph -->
      <!-- wp:paragraph {"className":"lede"} --><p class="lede">One or two sentences describing the service.</p><!-- /wp:paragraph -->
      <!-- wp:buttons -->
      <div class="wp-block-buttons">
        <!-- wp:button --><div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/contact/">Request a Consultation</a></div><!-- /wp:button -->
        <!-- wp:button {"className":"is-style-outline"} --><div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="/services/">Explore Services</a></div><!-- /wp:button -->
      </div>
      <!-- /wp:buttons -->
    </div>
    <!-- /wp:column -->
    <!-- wp:column {"className":"hero-media"} -->
    <div class="wp-block-column hero-media">
      <!-- wp:image {"sizeSlug":"large"} --><figure class="wp-block-image size-large"><img alt="Describe the photograph for people using a screen reader"/></figure><!-- /wp:image -->
    </div>
    <!-- /wp:column -->
  </div>
  <!-- /wp:columns -->
</section>
<!-- /wp:group -->
""")

    out["practice-cards"] = pattern("practice-cards", "Two sister practices", """
<!-- wp:group {"tagName":"section","className":"section tone-white","layout":{"type":"constrained"}} -->
<section class="wp-block-group section tone-white">
  <!-- wp:heading --><h2 class="wp-block-heading">Choose the practice that fits your matter</h2><!-- /wp:heading -->
  <!-- wp:columns {"className":"grid practices"} -->
  <div class="wp-block-columns grid practices">
    <!-- wp:column {"className":"practice-card practice-life"} -->
    <div class="wp-block-column practice-card practice-life">
      <!-- wp:heading {"level":3} --><h3 class="wp-block-heading"><a href="/life-solutions/">Transformative Life Solutions</a></h3><!-- /wp:heading -->
      <!-- wp:list {"className":"checklist"} --><ul class="wp-block-list checklist"><!-- wp:list-item --><li>Family-Centered Mediation</li><!-- /wp:list-item --><!-- wp:list-item --><li>Conflict Coaching</li><!-- /wp:list-item --><!-- wp:list-item --><li>Communication Facilitation</li><!-- /wp:list-item --></ul><!-- /wp:list -->
    </div>
    <!-- /wp:column -->
    <!-- wp:column {"className":"practice-card practice-leadership"} -->
    <div class="wp-block-column practice-card practice-leadership">
      <!-- wp:heading {"level":3} --><h3 class="wp-block-heading"><a href="/leadership-systems/">Transformative Leadership Systems</a></h3><!-- /wp:heading -->
      <!-- wp:list {"className":"checklist"} --><ul class="wp-block-list checklist"><!-- wp:list-item --><li>Business-to-Business Conflict Resolution</li><!-- /wp:list-item --><!-- wp:list-item --><li>Organizational Facilitation</li><!-- /wp:list-item --><!-- wp:list-item --><li>Leadership &amp; Partnership Dispute Support</li><!-- /wp:list-item --></ul><!-- /wp:list -->
    </div>
    <!-- /wp:column -->
  </div>
  <!-- /wp:columns -->
</section>
<!-- /wp:group -->
""")

    out["sister-band"] = pattern("sister-band", "Sister-practice band", """
<!-- wp:group {"tagName":"aside","className":"sister-band","layout":{"type":"constrained"}} -->
<aside class="wp-block-group sister-band">
  <!-- wp:paragraph {"className":"sister-band-link"} -->
  <p class="sister-band-link"><span class="sister-band-eyebrow">Sister practice</span> <a href="/leadership-systems/"><strong>Transformative Leadership Systems</strong> <span class="sister-band-desc">Business-to-business arbitration, mediation, and negotiation support</span></a></p>
  <!-- /wp:paragraph -->
</aside>
<!-- /wp:group -->
""")

    out["cta-band"] = pattern("cta-band", "Call to action band", """
<!-- wp:group {"tagName":"section","className":"section tone-deep","layout":{"type":"constrained"}} -->
<section class="wp-block-group section tone-deep">
  <!-- wp:group {"className":"cta-box","layout":{"type":"constrained"}} -->
  <div class="wp-block-group cta-box">
    <!-- wp:heading --><h2 class="wp-block-heading">Ready to talk it through?</h2><!-- /wp:heading -->
    <!-- wp:paragraph --><p>Request a consultation. We'll confirm whether your matter is a good fit, and if it isn't, we'll point you toward free supportive referrals.</p><!-- /wp:paragraph -->
    <!-- wp:buttons {"className":"btn-row center"} -->
    <div class="wp-block-buttons btn-row center"><!-- wp:button --><div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/contact/">Request a Consultation</a></div><!-- /wp:button --></div>
    <!-- /wp:buttons -->
  </div>
  <!-- /wp:group -->
</section>
<!-- /wp:group -->
""")

    out["scope-notice"] = pattern("scope-notice", "Scope notice (what we don't handle)", """
<!-- wp:group {"tagName":"section","className":"section tone-white","layout":{"type":"constrained"}} -->
<section class="wp-block-group section tone-white">
  <!-- wp:group {"className":"panel","layout":{"type":"constrained"}} -->
  <div class="wp-block-group panel">
    <!-- wp:heading --><h2 class="wp-block-heading">What we don't handle</h2><!-- /wp:heading -->
    <!-- wp:paragraph --><p>To protect clients and maintain the integrity of state processes, we do not handle:</p><!-- /wp:paragraph -->
    <!-- wp:list {"className":"softlist"} --><ul class="wp-block-list softlist"><!-- wp:list-item --><li>Consumer-business disputes</li><!-- /wp:list-item --></ul><!-- /wp:list -->
  </div>
  <!-- /wp:group -->
</section>
<!-- /wp:group -->
""")

    referrals = "".join(
        f'<!-- wp:list-item --><li class="referral"><a class="referral-link" href="{r["url"]}">{r["name"]}</a>'
        f'<span class="referral-text">{r["text"]}</span></li><!-- /wp:list-item -->'
        for r in C.REFERRALS)
    out["referrals"] = pattern("referrals", "Free supportive referrals", f"""
<!-- wp:group {{"tagName":"section","className":"section tone-white","layout":{{"type":"constrained"}}}} -->
<section class="wp-block-group section tone-white">
  <!-- wp:heading --><h2 class="wp-block-heading">Suggested referrals</h2><!-- /wp:heading -->
  <!-- wp:paragraph --><p>{C.ETHICS_REFERRAL_INTRO}</p><!-- /wp:paragraph -->
  <!-- wp:list {{"className":"referrals"}} --><ul class="wp-block-list referrals">{referrals}</ul><!-- /wp:list -->
</section>
<!-- /wp:group -->
""")

    out["faq"] = pattern("faq", "FAQ (details blocks)", """
<!-- wp:group {"tagName":"section","className":"section tone-soft","layout":{"type":"constrained"}} -->
<section class="wp-block-group section tone-soft">
  <!-- wp:heading --><h2 class="wp-block-heading">Frequently asked questions</h2><!-- /wp:heading -->
  <!-- wp:details {"className":"faq-item"} -->
  <details class="wp-block-details faq-item"><summary>A question</summary><!-- wp:paragraph --><p>The answer.</p><!-- /wp:paragraph --></details>
  <!-- /wp:details -->
</section>
<!-- /wp:group -->
""")

    out["founder-credentials"] = pattern("founder-credentials", "Founder credentials", "".join([
        '\n<!-- wp:group {"tagName":"section","className":"section tone-soft","layout":{"type":"constrained"}} -->\n'
        '<section class="wp-block-group section tone-soft">\n'
        '  <!-- wp:columns {"className":"credgroups"} -->\n  <div class="wp-block-columns credgroups">\n',
        "".join(
            '    <!-- wp:column {"className":"credgroup"} -->\n    <div class="wp-block-column credgroup">\n'
            f'      <!-- wp:heading {{"level":3,"anchor":"{gid}"}} --><h3 class="wp-block-heading" id="{gid}">{title}</h3><!-- /wp:heading -->\n'
            '      <!-- wp:list {"className":"checklist"} --><ul class="wp-block-list checklist">'
            + "".join(f"<!-- wp:list-item --><li>{i}</li><!-- /wp:list-item -->" for i in items)
            + "</ul><!-- /wp:list -->\n    </div>\n    <!-- /wp:column -->\n"
            for gid, title, items in C.FOUNDER_GROUPS),
        "  </div>\n  <!-- /wp:columns -->\n</section>\n<!-- /wp:group -->\n",
    ]))
    return out


def build_base():
    base = THEMES / "tls-base"
    write(base / "style.css", style_header(
        "TLS Base",
        "Shared block theme for LetTLSHelp: layout, components, header and footer, and the "
        "section patterns. Activate a child theme, never this one."))
    write(base / "theme.json", json.dumps(base_theme_json(), indent=2) + "\n")
    write(base / "functions.php",
          FUNCTIONS_PHP % {"version": VERSION} + SEO_PHP + seo_map() + IMAGES_PHP)
    (base / "seo.php").unlink(missing_ok=True)
    copy_photographs(base)
    write(base / "parts" / "footer.html", footer_part())
    write(base / "parts" / "header.html", header_part())
    for name, markup in TEMPLATES.items():
        write(base / "templates" / name, markup)
    for slug, php in patterns().items():
        write(base / "patterns" / f"{slug}.php", php)
    (base / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (base / "assets" / "js").mkdir(parents=True, exist_ok=True)
    shutil.copy2(DESIGN / "base.css", base / "assets" / "css" / "base.css")
    shutil.copy2(DESIGN / "app.js", base / "assets" / "js" / "app.js")
    return base


def copy_photographs(base):
    """Gather both sections' photographs into one folder inside the theme.

    In the static build each practice serves its own images from its own folder, and the page
    markup reaches them with relative paths. WordPress pages do not sit in those folders, so
    the pictures have to live at a fixed address instead. The file names do not collide across
    the two practices, so one flat folder is enough, and IMAGES_PHP points the markup at it.
    """
    dest = base / "assets" / "img"
    dest.mkdir(parents=True, exist_ok=True)
    kept = set()
    for section in ("life-solutions", "leadership-systems"):
        source = ROOT / "wireframes" / section / "assets" / "img"
        if not source.exists():
            raise SystemExit(f"No images at {source}. Run: python tools/build.py --production")
        for photo in source.iterdir():
            if photo.suffix.lower() not in (".avif", ".webp", ".jpg", ".jpeg", ".png"):
                continue
            if photo.name in kept:
                raise SystemExit(f"Two sections both have {photo.name}; the flat folder breaks.")
            shutil.copy2(photo, dest / photo.name)
            kept.add(photo.name)
    for stale in dest.iterdir():
        if stale.name not in kept:
            stale.unlink()
    return len(kept)


def child_theme_json(palette_key):
    palette = TOKENS[palette_key]["palette"]
    fonts = TOKENS[palette_key]["fonts"]
    colors = [{"slug": slugify(name), "name": name.replace("-", " ").title(), "color": meta["hex"]}
              for name, meta in palette.items()]
    families = [
        {"fontFamily": f'"{fonts["heading"]}", Georgia, serif', "slug": "heading", "name": fonts["heading"]},
        {"fontFamily": f'"{fonts["body"]}", system-ui, sans-serif', "slug": "body", "name": fonts["body"]},
        {"fontFamily": f'"{fonts["accent"]}", Georgia, serif', "slug": "accent", "name": fonts["accent"]},
    ]
    return {
        "$schema": "https://schemas.wp.org/trunk/theme.json",
        "version": 3,
        "settings": {
            "color": {"palette": colors, "defaultPalette": False},
            "typography": {"fontFamilies": families},
        },
    }


def seo_map():
    """Per-page title, description, social image and structured data.

    WordPress builds a title from the page name plus the site name, has no description, and
    emits no structured data. All of that was written for the static build and is lost in the
    move, so it is lifted straight out of the rendered pages and handed to the theme, keyed by
    URL path. Nothing is retyped, and it stays in step with content/ on every rebuild.

    Written into functions.php rather than a file beside it, so installing the theme by hand
    is one file to copy and cannot half-arrive.
    """
    import html as html_mod
    import re

    built = ROOT / "wireframes"
    if not built.exists():
        raise SystemExit("No build found. Run: python tools/build.py --production")

    entries = {}
    for path in sorted(built.rglob("index.html")):
        rel = path.relative_to(built).parent.as_posix()
        url_path = "/" if rel == "." else f"/{rel}/"
        markup = path.read_text("utf-8")

        def grab(pattern):
            found = re.search(pattern, markup, re.S)
            return html_mod.unescape(found.group(1)).strip() if found else ""

        entries[url_path] = {
            "title": grab(r"<title>(.*?)</title>"),
            "description": grab(r'<meta name="description" content="([^"]*)"'),
            "og_image": grab(r'<meta property="og:image" content="([^"]*)"'),
            "jsonld": grab(r'<script type="application/ld\+json">(.*?)</script>'),
        }

    def php_string(value):
        return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"

    rows = []
    for url_path, data in entries.items():
        rows.append(
            f"    {php_string(url_path)} => array(\n"
            f"        'title' => {php_string(data['title'])},\n"
            f"        'description' => {php_string(data['description'])},\n"
            f"        'og_image' => {php_string(data['og_image'])},\n"
            f"        'jsonld' => {php_string(data['jsonld'])},\n"
            f"    ),"
        )
    return f"""
/**
 * Per-page search-engine data, generated by tools/build_theme.py from the built pages.
 *
 * Do not edit by hand: re-run the generator instead, or it will drift from content/.
 */
function tls_seo_map() {{
    return array(
{chr(10).join(rows)}
    );
}}
"""


SEO_PHP = """
/**
 * Search-engine data for the current page, or null if we have none for this address.
 */
function tls_seo() {
    static $map = null;
    if ( $map === null ) {
        $map = tls_seo_map();
    }
    $path = wp_parse_url( $_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH );
    $path = '/' . trim( (string) $path, '/' );
    if ( $path !== '/' ) {
        $path .= '/';
    }
    return $map[ $path ] ?? null;
}

/**
 * Use the written title rather than "Page name - Site name".
 */
add_filter( 'pre_get_document_title', function ( $title ) {
    $seo = tls_seo();
    return ( $seo && $seo['title'] ) ? $seo['title'] : $title;
} );

/**
 * The description, social tags and structured data WordPress does not produce.
 *
 * An SEO plugin would output its own versions of these. If one is installed later, either
 * let it take over and delete this block, or turn the plugin's title and meta features off.
 */
add_action( 'wp_head', function () {
    $seo = tls_seo();
    if ( ! $seo ) {
        return;
    }
    if ( $seo['description'] ) {
        printf( '<meta name="description" content="%s">' . "\\n", esc_attr( $seo['description'] ) );
        printf( '<meta property="og:description" content="%s">' . "\\n", esc_attr( $seo['description'] ) );
    }
    if ( $seo['title'] ) {
        printf( '<meta property="og:title" content="%s">' . "\\n", esc_attr( $seo['title'] ) );
    }
    if ( $seo['og_image'] ) {
        printf( '<meta property="og:image" content="%s">' . "\\n", esc_url( $seo['og_image'] ) );
        printf( '<meta name="twitter:card" content="summary_large_image">' . "\\n" );
    }
    printf( '<meta property="og:type" content="website">' . "\\n" );
    printf( '<meta property="og:url" content="%s">' . "\\n", esc_url( home_url( add_query_arg( array() ) ) ) );
    if ( $seo['jsonld'] ) {
        echo '<script type="application/ld+json">' . $seo['jsonld'] . '</script>' . "\\n";
    }
}, 5 );
"""


IMAGES_PHP = """
/**
 * Point the pages' photographs at the theme.
 *
 * The page markup was written for the static build, where each practice served its pictures
 * from a folder beside the page: src="assets/img/..." on a top-level page, "../assets/img/..."
 * one level down. A WordPress page is not in that folder, so those paths resolve to nothing
 * and every photograph comes up blank. The pictures now live in one folder in the theme, and
 * this rewrites the addresses on the way out.
 *
 * Rewriting on output, rather than editing twenty pages, keeps the stored content identical to
 * the approved build. If the pictures are ever moved into the Media Library, delete this.
 */
add_filter( 'the_content', function ( $content ) {
    return preg_replace(
        '#(?<=["\\'\\s,])(?:\\.\\./)*assets/img/#',
        trailingslashit( get_template_directory_uri() ) . 'assets/img/',
        $content
    );
}, 20 );
"""


def build_child():
    """One child theme carrying all three brands, switched by URL path.

    WordPress activates a single theme, so the three practices cannot be three active child
    themes. Each brand layer keeps its own body-class scope (.site-hub, .site-life,
    .site-leadership) exactly as in the static build, and functions.php sets that class from
    the request path. Same CSS, same result, one theme.
    """
    folder, name, palette_key = CHILD
    path = THEMES / folder

    layers = [style_header(name, "Brand layers for all three sections of lettlshelp.com. The "
                                 "active section is set from the URL path by functions.php.",
                           template="tls-base")]
    layers.append("\n/* Default, before a section class is applied (wp-admin, the editor). */\n"
                  + (DESIGN / "hub.css").read_text("utf-8").replace(".site-hub", ":root"))
    for key, _prefix, _module, brand_css in SECTIONS:
        layers.append(f"\n/* --- {key} --- */\n" + (DESIGN / brand_css).read_text("utf-8"))

    # Each section shows its own logo. The header's Site Logo block renders <img class="custom-logo">,
    # so the brand mark is swapped per section rather than needing three separate media settings.
    layers.append("""
/* Per-section logo. The Site Logo block gives one image site-wide, so each practice section
   points it at its own mark. Set the Life Solutions logo as the WordPress Site Icon/Logo; the
   rules below override it inside the other sections. */
.site-leadership .custom-logo { content: url("assets/leadership-logo-mark.png"); }
.site-life .custom-logo,
.site-hub .custom-logo { content: url("assets/life-logo-mark.png"); }

/* ---------------------------------------------------------------------------
   WordPress block markup.
   The static site's header is a plain flex row; WordPress wraps every block in
   its own containers, so the row needs rebuilding here. Without these the
   navigation wraps onto several lines and squeezes the button into a circle.
   --------------------------------------------------------------------------- */
/* WordPress caps every direct child of a constrained group at the *content* width (46rem).
   That is right for a paragraph and wrong for a full-width bar: the header row was squeezed
   into 736px, which left the five menu items about 412px to sit in. Being centred and set to
   never wrap, they spilled out of their box in both directions and landed on top of the logo
   on one side and the Request a Consultation button on the other. The header row and the
   footer grid take the site container width instead, exactly as they do in the static build.
   `.container` then does the rest, including the gutter on narrow screens. */
.site-header .header-inner,
.site-footer .footer-grid { max-width: none; }

.site-header .header-inner {
  display: flex; align-items: center; gap: 1.5rem; flex-wrap: nowrap;
  padding-block: .85rem;
}
.site-header .wp-block-site-logo { flex-shrink: 0; line-height: 0; }
.site-header .wp-block-site-logo img { width: 48px; height: auto; }

.site-header .primary-nav { flex-grow: 1; min-width: 0; }
.site-header .primary-nav .wp-block-navigation__container {
  flex-wrap: nowrap; justify-content: center; gap: .15rem;
}
.site-header .primary-nav .wp-block-navigation-item__content {
  padding: .5rem .7rem; border-radius: 999px; color: var(--c-text);
  text-decoration: none; font-size: .95rem; white-space: nowrap;
}
.site-header .primary-nav .wp-block-navigation-item__content:hover {
  background: var(--c-soft-1); color: var(--c-deep);
}
.site-header .primary-nav .current-menu-item > .wp-block-navigation-item__content {
  background: var(--c-soft-1); color: var(--c-primary); font-weight: 600;
}

/* The button must never shrink into a circle: it keeps its text on one line. */
.site-header .header-cta { flex-shrink: 0; margin: 0; }
.site-header .header-cta .wp-block-button__link { white-space: nowrap; padding: .75rem 1.4rem; }

/* Below the desktop breakpoint the navigation becomes WordPress's overlay menu,
   so the inline row is not needed and the button steps aside. */
@media (max-width: 1100px) {
  .site-header .header-cta { display: none; }
  .site-header .primary-nav { flex-grow: 0; margin-left: auto; }
}

/* Footer: WordPress columns in place of the static grid. */
.site-footer .footer-grid { gap: 2.5rem; }
.site-footer .footer-grid p { margin: 0 0 .45rem; }
.site-footer .wp-block-site-logo img {
  width: 170px; height: auto; background: #FFFFFF;
  border-radius: var(--radius); padding: .9rem;
}
.site-footer .footer-h { margin: 0 0 .9rem; }
""")
    write(path / "style.css", "".join(layers))
    write(path / "theme.json", json.dumps(child_theme_json(palette_key), indent=2) + "\n")

    fonts_php = "\n".join(
        f"        case '{key}':\n            return '{module.SITE['fonts']}';"
        for key, _prefix, module, _css in SECTIONS)
    prefixes = "\n".join(
        f"    if ( strpos( $path, '/{prefix}/' ) === 0 ) {{\n        return '{key}';\n    }}"
        for key, prefix, _module, _css in SECTIONS if prefix)

    write(path / "functions.php", f"""<?php
/**
 * {name}: one theme, three brands.
 *
 * lettlshelp.com runs as a single WordPress install, but the root and the two practice
 * sections each have their own palette, typefaces and logo. WordPress activates one theme,
 * so the section is decided from the URL path and applied as a body class — the same
 * mechanism the static build uses.
 */

if ( ! defined( 'ABSPATH' ) ) {{
    exit;
}}

/**
 * Which section of the site is being viewed: 'life', 'leadership', or 'hub'.
 */
function tls_section() {{
    $path = isset( $_SERVER['REQUEST_URI'] ) ? wp_parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ) : '/';
    $path = '/' . trim( (string) $path, '/' ) . '/';
{prefixes}
    return 'hub';
}}

/**
 * The body class every brand layer in style.css is scoped to.
 */
add_filter( 'body_class', function ( $classes ) {{
    $classes[] = 'site-' . tls_section();
    return $classes;
}} );

/**
 * Each section loads only the typefaces it uses, rather than all three everywhere.
 */
add_filter( 'tls_google_fonts_url', function () {{
    switch ( tls_section() ) {{
{fonts_php}
    }}
    return '';
}} );
""")

    (path / "assets").mkdir(parents=True, exist_ok=True)
    for key, _prefix, module, _css in SECTIONS:
        source_slug = module.SITE["slug"] or "life-solutions"
        assets = ROOT / "wireframes" / source_slug / "assets"
        for asset in ("logo.png", "logo-mark.png", "favicon.ico", "og-image.jpg"):
            source = assets / asset
            if source.exists():
                shutil.copy2(source, path / "assets" / f"{key}-{asset}")
    return path


def main():
    if THEMES.exists():
        shutil.rmtree(THEMES)
    base = build_base()
    child = build_child()
    for path in (base, child):
        count = sum(1 for _ in path.rglob("*") if _.is_file())
        print(f"wrote {path.relative_to(ROOT).as_posix()}  ({count} files)")


if __name__ == "__main__":
    main()
