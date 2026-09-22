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

# Each child theme: folder, display name, the site module, its brand CSS, and which palette in
# tokens.json to expose in the editor. The hub has no palette of its own, so it borrows the
# Life Solutions one, exactly as it borrows that logo.
CHILDREN = [
    ("tls-hub", "TLS — LetTLSHelp (hub)", hub, "hub.css", "life-solutions"),
    ("tls-life", "TLS — Transformative Life Solutions", life, "life.css", "life-solutions"),
    ("tls-leadership", "TLS — Transformative Leadership Systems", leadership, "leadership.css",
     "leadership-systems"),
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

add_action( 'wp_enqueue_scripts', function () {
    $base = get_template_directory_uri();
    $child = get_stylesheet_directory_uri();

    // Typefaces. Self-hosting these is the next improvement: it removes a third-party request
    // and lets the Privacy Policy drop its Google Fonts section.
    $fonts = apply_filters( 'tls_google_fonts_url', '' );
    if ( $fonts ) {
        wp_enqueue_style( 'tls-fonts', $fonts, array(), null );
    }

    wp_enqueue_style( 'tls-base', $base . '/assets/css/base.css', array(), TLS_BASE_VERSION );
    if ( $child !== $base ) {
        wp_enqueue_style( 'tls-brand', $child . '/style.css', array( 'tls-base' ), TLS_BASE_VERSION );
    }
    wp_enqueue_script( 'tls-app', $base . '/assets/js/app.js', array(), TLS_BASE_VERSION, true );
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


HEADER_PART = """<!-- wp:group {"tagName":"header","className":"site-header","layout":{"type":"constrained"}} -->
<header class="wp-block-group site-header">
  <!-- wp:group {"className":"container header-inner","layout":{"type":"flex","flexWrap":"nowrap","justifyContent":"space-between"}} -->
  <div class="wp-block-group container header-inner">
    <!-- wp:site-logo {"width":48,"className":"brand-mark"} /-->
    <!-- wp:navigation {"overlayMenu":"mobile","className":"primary-nav"} /-->
    <!-- wp:buttons {"className":"header-cta"} -->
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
    policies = "".join(
        f'<!-- wp:paragraph --><p><a href="/{slug}/">{label}</a></p><!-- /wp:paragraph -->\n      '
        for slug, label in C.ROOT_POLICIES)
    social = "".join(
        f'<!-- wp:paragraph --><p><a href="{url}" rel="noopener">{label}</a></p><!-- /wp:paragraph -->\n      '
        for label, url in C.SOCIAL)
    return f"""<!-- wp:group {{"tagName":"footer","className":"site-footer","layout":{{"type":"constrained"}}}} -->
<footer class="wp-block-group site-footer">
  <!-- wp:columns {{"className":"container footer-grid"}} -->
  <div class="wp-block-columns container footer-grid">
    <!-- wp:column -->
    <div class="wp-block-column">
      <!-- wp:site-logo {{"width":170,"className":"footer-logo"}} /-->
      <!-- wp:paragraph --><p>Edit this description in the footer template part.</p><!-- /wp:paragraph -->
    </div>
    <!-- /wp:column -->
    <!-- wp:column -->
    <div class="wp-block-column">
      <!-- wp:heading {{"level":2,"className":"footer-h"}} --><h2 class="wp-block-heading footer-h">Explore</h2><!-- /wp:heading -->
      <!-- wp:navigation {{"overlayMenu":"never"}} /-->
    </div>
    <!-- /wp:column -->
    <!-- wp:column -->
    <div class="wp-block-column">
      <!-- wp:heading {{"level":2,"className":"footer-h"}} --><h2 class="wp-block-heading footer-h">Contact</h2><!-- /wp:heading -->
      <!-- wp:paragraph --><p><a href="tel:{C.PHONE_TEL}">Call or text {C.PHONE}</a></p><!-- /wp:paragraph -->
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
    <!-- wp:paragraph --><p>Neutral ADR, conflict-coaching, and organizational facilitation services only. We do not provide legal advice, legal representation, or legal advocacy, or medical, mental health, or clinical therapeutic services.</p><!-- /wp:paragraph -->
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
    write(base / "functions.php", FUNCTIONS_PHP % {"version": VERSION})
    write(base / "parts" / "header.html", HEADER_PART)
    write(base / "parts" / "footer.html", footer_part())
    for name, markup in TEMPLATES.items():
        write(base / "templates" / name, markup)
    for slug, php in patterns().items():
        write(base / "patterns" / f"{slug}.php", php)
    (base / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (base / "assets" / "js").mkdir(parents=True, exist_ok=True)
    shutil.copy2(DESIGN / "base.css", base / "assets" / "css" / "base.css")
    shutil.copy2(DESIGN / "app.js", base / "assets" / "js" / "app.js")
    return base


def child_theme_json(site, palette_key):
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


def build_children(base):
    made = []
    for folder, name, module, brand_css, palette_key in CHILDREN:
        site = module.SITE
        path = THEMES / folder
        header = style_header(name, f'Brand layer for {site["name"]}.', template="tls-base")
        brand = (DESIGN / brand_css).read_text("utf-8")
        # The static site scopes the brand layer to a body class; in WordPress the child theme
        # is the only one active, so the custom properties go straight onto :root.
        scoped = brand.replace(f'.site-{site["key"]}', ":root, body")
        write(path / "style.css", header + "\n" + scoped)
        write(path / "theme.json", json.dumps(child_theme_json(site, palette_key), indent=2) + "\n")

        # The Google Fonts URL each site already uses, so the typefaces match the static build.
        write(path / "functions.php", f"""<?php
/**
 * {name}: brand-specific setup.
 */

if ( ! defined( 'ABSPATH' ) ) {{
    exit;
}}

add_filter( 'tls_google_fonts_url', function () {{
    return '{site["fonts"]}';
}} );
""")
        assets = ROOT / "wireframes" / site["slug"] / "assets"
        for asset in ("logo.png", "logo-mark.png", "favicon.ico", "og-image.jpg"):
            source = assets / asset
            if source.exists():
                (path / "assets").mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, path / "assets" / asset)
        made.append(path)
    return made


def main():
    if THEMES.exists():
        shutil.rmtree(THEMES)
    base = build_base()
    children = build_children(base)
    for path in [base] + children:
        count = sum(1 for _ in path.rglob("*") if _.is_file())
        print(f"wrote {path.relative_to(ROOT).as_posix()}  ({count} files)")


if __name__ == "__main__":
    main()
