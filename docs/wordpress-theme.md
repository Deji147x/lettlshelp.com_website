# The WordPress block theme

Generated, not hand-written:

```bash
python tools/build_theme.py
```

That reads `design-system/tokens.json`, the brand CSS, and `content/*.py`, and writes
`wp-content/themes/`. **Edit the sources and re-run it — never edit the generated theme
directly**, or the theme and the static site drift apart and the owner gets two different sites.

## What it produces

| Theme | Role |
|---|---|
| `tls-base` | Parent. Layout, typography, spacing, header, footer, templates, and the section patterns. **Never activate this one.** |
| `tls-lettlshelp` | Child. All three brands in one theme. **This is the one you activate.** |

### Why one child theme, not three

WordPress activates **one theme at a time**. The root and the two practice sections each have
their own palette, typefaces and logo, but they are all one install, so they cannot be three
active child themes — activating one would paint the whole site in its colours.

Instead the child ships all three brand layers, each scoped to a body class exactly as in the
static build (`.site-hub`, `.site-life`, `.site-leadership`), and `functions.php` sets that class
from the URL path:

| URL starts with | Body class | Brand |
|---|---|---|
| `/life-solutions/` | `site-life` | Teal, Lora + Open Sans |
| `/leadership-systems/` | `site-leadership` | Navy, Merriweather + Lato |
| anything else | `site-hub` | The root |

Each section also loads only its own typefaces, and swaps the Site Logo image to its own mark.

## Installing

1. Zip `tls-base` and `tls-lettlshelp`, upload both under **Appearance → Themes → Add New**.
2. Activate **tls-lettlshelp**, never the parent.
3. **Appearance → Editor → Patterns** shows the sections under **TLS sections**.
4. Build each page from the static site's equivalent, dropping in the patterns in the same order.
   Every page's section order is on the review build at `/page-index.html` with "Show wireframe
   notes" switched on.

## Why the design survives the move

The theme loads `design-system/base.css` — the same file the static site uses — and the patterns
carry the same class names (`hero`, `practice-card`, `sister-band`, `referrals`, `credgroup`).
So the WordPress pages inherit the design without it being rebuilt in block settings, where it
would quietly diverge.

Headings, paragraphs, lists and buttons are real core blocks, so the owner edits text in the
block editor without being able to break the layout.

## What still has to be done by hand

- **Pages.** The theme supplies the sections; someone still has to create the 20 pages and place
  the patterns. The patterns carry sample text, deliberately, so nothing unreviewed goes live
  pretending to be final copy.
- **Menus.** The header and footer use the Navigation block. Build the menus once in the editor,
  including the About and Services dropdowns.
- **Forms.** The contact and screening forms are still the static markup plus `app.js`. They work
  as they stand (the `mailto:` hand-off), but a form plugin would be better: it would keep a
  record of enquiries, which `mailto:` cannot.
- **Typefaces.** Still loaded from Google Fonts, via the `tls_google_fonts_url` filter in each
  child. Self-hosting them removes a third-party request and lets the Privacy Policy drop its
  Google Fonts section.
- **Redirects.** `tools/build.py` writes the `.htaccess` rules. Put them above the
  `# BEGIN WordPress` block, and leave the WordPress block alone.

## When something changes

| Change | Do this |
|---|---|
| A new section with its own brand | Add it to `SECTIONS` in `tools/build_theme.py` and give it a brand CSS file |
| A colour or typeface | Edit `design-system/tokens.json` or the brand CSS, re-run `build_theme.py` |
| Shared component styling | Edit `design-system/base.css`, re-run `build_theme.py` |
| Referral list, social links, founder credentials | Edit `content/common.py`, re-run `build_theme.py` |
| Page copy | Edit it in WordPress. The static build stays the reference for structure |
