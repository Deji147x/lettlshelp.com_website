# Architecture: two WordPress sites, one design system

## Sites

| | Transformative Life Solutions | Transformative Leadership Systems |
|---|---|---|
| URL (now) | https://lettlshelp.com/ | https://lettlshelp.com/leadership-systems/ |
| Domain (later) | https://transformativelifesolutions.com | https://transformativeleadershipsystems.com |
| Focus | Family, interpersonal, workplace (non-consumer) mediation; conflict coaching | B2B arbitration, med-arb, business mediation, negotiation support, coaching |
| Palette | Teal / navy-teal / gold | Leadership blue / teal-green / ocher |
| Fonts | Lora + Open Sans | Merriweather + Lato |
| Email | services@lettlshelp.com | support@lettlshelp.com |

**While both sites share lettlshelp.com**, run them as **one WordPress install**: Life Solutions
pages at the root and Leadership Systems pages under `/leadership-systems/`, with the two child
themes applied per section (or one theme switching palette by path). That keeps hosting to a single
site and one SSL certificate. When the vanity domains are ready, split Leadership Systems into its
own install and 301-redirect `/leadership-systems/*` to the new domain.

Once separated, the two sites are **separate WordPress installs** on one hosting plan that allows multiple sites. Each has its own logo, palette, content, images, navigation, SEO, and contact details. They don't share a database, so either one can move, grow, or add e-commerce without affecting the other.

## URL map (same on both sites)

```
/                     Home
/about/               About
/services/            Services (#family #interpersonal #workplace #coaching | #arbitration #mediation #negotiation #coaching)
/how-it-works/        How It Works  (screening slot)
/resources/           Blog index (Posts page) → /resources/<post-slug>/
/faq/                 FAQ (FAQPage schema)
/contact/             Contact (form + booking slot)
/ethics/              Ethics & Compliance
/privacy-policy/      Privacy Policy
/terms-disclaimers/   Terms & Disclaimers
```
The header navigation stays on-site. Each footer links to the sister practice, and cross-link bands on Home and Services point to it.

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
- **Email:** services@lettlshelp.com and support@lettlshelp.com are the published addresses. The cheapest
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
