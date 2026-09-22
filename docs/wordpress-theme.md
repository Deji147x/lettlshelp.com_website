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
| `tls-hub` | Child for the domain root (LetTLSHelp), carrying the Life Solutions logo and palette |
| `tls-life` | Child for Transformative Life Solutions — teal, Lora + Open Sans |
| `tls-leadership` | Child for Transformative Leadership Systems — navy, Merriweather + Lato |

Each child holds only its brand layer: the `--c-*` custom properties, its two typefaces, its
colour palette for the editor, and its logo. Everything else is inherited.

## Installing

1. Zip `tls-base` and the child you want, upload both under **Appearance → Themes → Add New**.
2. Activate the **child**, never the parent.
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
| A colour or typeface | Edit `design-system/tokens.json` or the brand CSS, re-run `build_theme.py` |
| Shared component styling | Edit `design-system/base.css`, re-run `build_theme.py` |
| Referral list, social links, founder credentials | Edit `content/common.py`, re-run `build_theme.py` |
| Page copy | Edit it in WordPress. The static build stays the reference for structure |
