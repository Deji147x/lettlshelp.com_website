# Architecture: one hub, two practice sections, one design system

## Sites

| | Hub (LetTLSHelp) | Transformative Life Solutions | Transformative Leadership Systems |
|---|---|---|---|
| URL | https://lettlshelp.com/ | https://lettlshelp.com/life-solutions/ | https://lettlshelp.com/leadership-systems/ |
| Domain (later) | stays the parent | https://transformativelifesolutions.com | https://transformativeleadershipsystems.com |
| Focus | Introduces both; routes visitors into the right screening | Family, interpersonal, workplace (non-consumer) mediation; conflict coaching | B2B arbitration, med-arb, business mediation, negotiation support, coaching |
| Palette | Deep navy-teal / gold (neutral) | Teal / navy-teal / gold | Leadership blue / teal-green / ocher |
| Fonts | Lora + Open Sans | Lora + Open Sans | Merriweather + Lato |
| Email | none by design — shows both | LifeSolutions@LetTLSHelp.com | LeadershipSystems@LetTLSHelp.com |

**The root is a shared hub** (owner's vision document, 2026-09-16). Life Solutions used to be the
root and moved down into `/life-solutions/`, so the two practices are now symmetrical: same depth,
same page set, same treatment. `tools/build.py` writes the 301s for every URL that moved.

Run the whole thing as **one WordPress install**: hub pages at the root, each practice under its
own folder, with the child themes applied per section (or one theme switching palette by path).
That keeps hosting to a single site and one SSL certificate. When the vanity domains are ready,
split each practice into its own install and 301-redirect its folder to the new domain.

Once separated, the two practices are **separate WordPress installs** on one hosting plan that allows multiple sites. Each has its own logo, palette, content, images, navigation, SEO, and contact details. They don't share a database, so either one can move, grow, or add e-commerce without affecting the other. The hub stays at the root as the parent.

## URL map

```
Hub (shared, speaks for both)          Each practice (identical structure)
/                      Home            <practice>/                Home
/ethics/               Ethics &        <practice>/about/          About (#our-founder
                       Compliance                                  #completed-trainings
/disclaimers/          Disclaimers                                 #credentials #affiliations)
/privacy-policy/       Privacy Policy  <practice>/services/       Services (anchored per service)
/contact/              Contact,        <practice>/how-it-works/   How It Works (screening slot)
                       routes to a     <practice>/faq/            FAQ (FAQPage schema)
                       practice        <practice>/contact/        Contact (form + booking slot)
                                       <practice>/begin-intake/   Screening intake
```
`<practice>` is `/life-solutions/` or `/leadership-systems/`.

**Retired 2026-09-16:** `/resources/` (the blog index), on the owner's instruction. Without it the
domain ranks on its static pages alone, with no route to long-tail search terms; the renderer and
the `posts` section type are still in `tools/build.py` if it comes back.

**Folded into the hub:** the per-practice `/ethics/`, `/terms-disclaimers/` and `/privacy-policy/`
pages became one copy of each at the root, so there are no near-duplicate legal pages competing
with each other.

## Navigation

- **About** and **Services** are dropdowns in each practice header. Every child is a real anchor on
  the parent's own page, so the submenu is a shortcut and never the only way in. The toggle is a
  real `<button aria-expanded>`; with JavaScript off the panel stays in the flow and nothing is
  unreachable. On mobile it becomes an accordion inside the existing menu.
- A **sister-practice band** sits directly under the header on both practices, each promoting the
  other by name and descriptor. It is below the nav, not in it: the nav already carries six items
  plus the consultation button.
- The hub nav lists both practices as dropdowns; it has no sister band, being the parent of both.
- Each footer links to the sister practice, and cross-link bands on Home and Services point to it.

## Theme plan (phase 2, after wireframe approval)

```
wp-content/themes/
  tls-base/            parent block theme: layout, spacing, radii, components, patterns, header/footer parts
    theme.json         shared layout + typography scale (no brand colors)
    patterns/          tls/hero-split, tls/page-header, tls/intro, tls/services-grid, tls/audience-grid,
                       tls/media-text, tls/process-steps, tls/trust-grid, tls/scope-notice, tls/faq,
                       tls/sister-site-link, tls/cta-band, tls/service-detail, tls/founder, tls/referrals,
                       tls/disclaimers, tls/integration-slot
    parts/             header.html, footer.html
  tls-life/            child theme: theme.json palette + fonts, logo, favicon
  tls-leadership/      child theme: theme.json palette + fonts, logo, favicon
```
- Every wireframe section is labeled with its planned pattern ("Show wireframe notes" on any page).
- `design-system/tokens.json` maps directly to each child theme's `settings.color.palette` and `settings.typography.fontFamilies`.
- Fonts will be **self-hosted** through `theme.json` `fontFace` (faster, and no Google Fonts request).
- **No page builder.** The owner edits text, images, and posts in the block editor; patterns are locked where layout matters.

## Plugins (keep the list short)

| Need | Plugin | Notes |
|---|---|---|
| SEO | Yoast SEO **or** Rank Math (pick one) | Titles, meta descriptions, XML sitemap, Open Graph, breadcrumbs, schema |
| Search Console + GA4 | Site Kit by Google | Connects both; no API key needed |
| Caching / speed | LiteSpeed Cache (if the host runs LiteSpeed) | Page cache, image optimization, WebP |
| Forms | One form plugin (e.g., Fluent Forms, WPForms Lite) | Contact form now; multi-step and conditional screening later |
| Security | Host firewall + a 2FA plugin | Plus limit login attempts and auto-updates |
| Backups | Host daily backups | Test a restore once before launch |

## Integration readiness (reserved, not built)

These are marked on the wireframe as dashed "Integration slot" boxes, backed by the `tls/integration-slot` pattern.

### Screening / assessment tool (How It Works, Contact)
- **Provider-agnostic:** the slot accepts a block, shortcode, or iframe, so the WordPress form plugin can be swapped for a third-party screening platform without redesigning the page.
- Requirements the tool must meet: multi-step questions, conditional logic, secure HTTPS submission, results or recommendations (including free referrals when ineligible), and **minimal data collection**. Screening records are documented per the guides.
- Don't collect confidential details in open text fields before screening; the contact form already tells visitors this.

### Booking (Contact)
- Planned for **Google Workspace**: Google Calendar appointment schedules, embedded as a button or iframe, with availability syncing, confirmation emails, and rescheduling or cancellation.
- Can switch to a WordPress booking plugin that syncs with Google Calendar later, in the same slot.
- Confirm which appointment-schedule features the chosen Workspace plan includes.

### E-commerce (Services, Resources)
- **Not installed.** When needed: WooCommerce (or similar) for online payments, digital products, services, customer accounts, and order management.
- The parent theme will declare WooCommerce support only when it's activated. Header space for an account link is left in the layout.
- It's added to one site at a time; the other site is unaffected.

## Hosting & cost (target ≈ $10/month)
- **While both practices share lettlshelp.com, one WordPress site is enough** — the cheapest tier that
  allows a single site, with one SSL certificate. A plan allowing **at least 2 websites** is only needed
  once the vanity domains launch. Intro prices usually rise at renewal, so **check renewal pricing**.
- Domains are billed yearly and separately.
- **Email:** LifeSolutions@LetTLSHelp.com and LeadershipSystems@LetTLSHelp.com are the published addresses. The cheapest
  option is mailboxes or forwarding included with the hosting plan for lettlshelp.com. **Google Workspace
  is per user, per month on top of hosting**, which likely exceeds the $10 target; if Workspace is wanted
  for calendar booking, one user with the other domains added as alias domains keeps it to a single seat.
  Verify current plan terms.

## Security & privacy
- HTTPS everywhere; strong unique admin passwords with 2FA; separate editor accounts for day-to-day editing.
- **This repository is public:** never commit `.env` files, `wp-config.php`, API keys, SMTP or app passwords, or form-plugin licence keys.
- Forms use spam protection (honeypot or Cloudflare Turnstile) rather than CAPTCHAs that hurt accessibility.
- Privacy Policy must list GA4, form, screening, and booking processors before launch.

## Accessibility & performance targets
- WCAG 2.2 AA:
  - text contrast ≥ 4.5:1 (see `docs/consistency-review.md`)
  - visible focus states
  - skip link and landmarks
  - one H1 per page with a logical H2/H3 order
  - labeled form fields
  - 44 px+ touch targets
  - no motion (`prefers-reduced-motion` respected)
- Performance:
  - one small CSS file per site and about 1 KB of JS (mobile menu)
  - responsive, lazy-loaded images (hero loads eagerly)
  - no sliders, animations, or page builders
