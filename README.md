# TLS websites: Transformative Life Solutions & Transformative Leadership Systems

Wireframes and the design system for two related but separate WordPress websites:

- **Transformative Life Solutions**: family-centered mediation, interpersonal mediation, workplace facilitation, conflict coaching
- **Transformative Leadership Systems**: B2B arbitration & med-arb, business mediation, negotiation support, conflict coaching

**Both launch on lettlshelp.com for now** (owner's decision, 2026-09-16): Life Solutions at
`https://lettlshelp.com/`, Leadership Systems at `https://lettlshelp.com/leadership-systems/`.
TransformativeLifeSolutions.com and TransformativeLeadershipSystems.com come later; change each
site's `domain` and `base` in `content/` then, and 301-redirect the old paths.

Owner: Tanika L. Smith · services@lettlshelp.com (Life) · support@lettlshelp.com (Leadership) · +1 (240) 650-0007

## Status
**Phase 1: HTML wireframe (this commit).** All 10 pages per site are branded, responsive, and SEO-ready, with integration slots for screening, booking, and e-commerce.
**Phase 2: WordPress block theme** (`tls-base` parent + two child themes), after the owner approves the wireframe.

Yellow **"Review"** notes on the pages mark copy that needs owner or legal sign-off. The full list is in [`docs/consistency-review.md`](docs/consistency-review.md).

## Structure
```
content/         Page copy for each site (life.py, leadership.py) + shared contact/disclaimers (common.py)
design-system/   base.css (shared components), life.css / leadership.css (brand layers), app.js, tokens.json
tools/           process_assets.py (logos, favicons, OG images, photos) · build.py (renders wireframes) · icons.py
brand/           Original logo and palette files per site
wireframes/      Generated output: index.html hub, life-solutions/, leadership-systems/
docs/            consistency-review.md · architecture.md · seo-plan.md
```

## Preview
```bash
python -m http.server 8765 --directory wireframes
```
Open http://127.0.0.1:8765/ and click **Show wireframe notes** (bottom right) to see the planned WordPress pattern for each section.

## Rebuild after editing copy
```bash
python tools/build.py
```
To regenerate images after new logos or photos land in `~/Downloads` (requires Pillow):
```bash
python tools/process_assets.py
```

## Rules for this repo
- **It is public.** Never commit API keys, `.env` files, `wp-config.php`, or passwords. GA4 Measurement IDs and the Search Console token are fine.
- Don't invent credentials, testimonials, client stories, or statistics.
- Legal pages and disclaimers need attorney review before launch.
- Photos are from Pexels (free licence); images of unknown origin are excluded.
