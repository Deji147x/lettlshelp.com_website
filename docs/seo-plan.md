# SEO plan

## Target keywords → pages

The owner's keywords: mediation, arbitration, negotiation, conflict coaching, ADR, divorce mediation, separation agreement, parenting plan, prenuptial agreement, mediator, NDA.

### Transformative Life Solutions
| Page | Primary keywords | Title tag |
|---|---|---|
| Home | mediation, conflict coaching, mediator, ADR | Family Mediation & Coaching \| Transformative Life Solutions |
| Services | divorce mediation, parenting plan, separation agreement, prenuptial agreement, conflict coaching | Divorce Mediation Services \| Transformative Life Solutions |
| FAQ | divorce mediation, parenting plans, separation/prenuptial agreement, arbitration (cross-link) | Mediation FAQ \| Transformative Life Solutions |
| Contact | mediator | Contact a Mediator \| Transformative Life Solutions |
| Resources | mediation resources (blog categories below) | Mediation Resources \| Transformative Life Solutions |

Arbitration, negotiation, and NDA are mentioned on the Life site **only** as links to Leadership Systems (Home and Services cross-link bands, plus an FAQ answer). The guide lists arbitration as a B2B-only service, so the Life site doesn't claim it.

### Transformative Leadership Systems
| Page | Primary keywords | Title tag |
|---|---|---|
| Home | arbitration, business mediation, negotiation, ADR | B2B Arbitration & ADR \| Transformative Leadership Systems |
| Services | arbitration, med-arb, negotiation, NDA, conflict coaching | Arbitration Services \| Transformative Leadership Systems |

All titles are 60 characters or fewer, so Google shouldn't cut them off. Secondary keywords (parenting plans, negotiation, NDAs) go in each page's H1/H2 and meta description.
| FAQ | arbitration vs mediation, NDA, eligibility | Arbitration FAQ \| Transformative Leadership Systems |

Every page has a unique title and a meta description of about 110–160 characters (see `content/*.py`). The WordPress SEO plugin takes these over at launch.

## Technical foundations (in the wireframe now)
- Clean, lowercase, hyphenated URLs with trailing slashes; canonical tags point to the production domains.
- One H1 per page, then H2 sections and H3 cards; descriptive image alt text (checked automatically, 0 issues).
- Open Graph and Twitter card tags, with a 1200×630 `og-image.jpg` per site.
- JSON-LD `@graph` on every page:
  - `ProfessionalService` (name, phone, email, founder, `knowsAbout` keywords) and `WebSite`
  - `WebPage` / `AboutPage` / `ContactPage` / `CollectionPage`
  - `BreadcrumbList` on inner pages
  - `FAQPage` on the FAQ page only
- `sitemap.xml`, `robots.txt`, and `site.webmanifest` per site; favicons at 16, 32, 48, 180, 192, and 512 px.
- **No `noindex` tags anywhere.** Canonical tags point each page to its production URL instead.
- **HTTPS enforced:** `wireframes/<site>/.htaccess` forces a 301 to `https://` and removes `www`. It also sends HSTS and security headers and enables compression and browser caching. Merge it above the WordPress block at launch.
- **Images:** WebP with JPEG fallback (`<picture>`), responsive `srcset`, explicit width/height (no layout shift), lazy loading below the fold, and a preloaded hero image for faster LCP.
- **More schema:** a `Person` (founder) node on every page, and one `Service` node per service on each Services page.
- **Preview links:** in the preview, sister-site links point to the local wireframe so nothing is broken before the domains are live. Production uses the real domains.
- **Quality gate:** `python tools/seo_check.py` checks every item on the owner's SEO checklist and exits with an error if anything fails. Run it before each commit.
- **Backlinks:** see `docs/backlink-strategy.md`.
- Internal linking: service cards → service anchors; every page ends in a CTA to Contact; scope notices → Ethics; Terms reached from How It Works and the footer; sister-site links on both sites.

## Google Search Console
Token supplied: `nueZtT3ZZsV8SutwZKliXMbZEHgZePLeyCRynDhq78c`

The token belongs to the **lettlshelp.com** property, which now covers both practices.

- **Domain property (recommended):** add a DNS **TXT** record `google-site-verification=nueZtT3ZZsV8SutwZKliXMbZEHgZePLeyCRynDhq78c` at the registrar for lettlshelp.com. This covers http/https and all subdomains.
- **URL-prefix property:** every page on both sites already carries `<meta name="google-site-verification" content="…">`. In WordPress, paste it into the SEO plugin or let Site Kit verify.
- Verification only succeeds once lettlshelp.com actually serves the site.
- After launch, submit the single `https://lettlshelp.com/sitemap.xml` (or the SEO plugin's sitemap index); it lists all 22 pages across both practices.
- Each vanity domain will need **its own** property and token when it goes live.

## Google Analytics 4
- Create one GA4 property per site. Each gives a **Measurement ID** (`G-XXXXXXXXXX`), which is public and safe to commit.
- **No API key is needed** for tracking. If an API key was generated for something else, keep it out of chat and out of this public repo.
- In WordPress, connect via Site Kit. For the wireframe, set `ga4_id` in `content/life.py` or `content/leadership.py` and rebuild.
- Mark key events: contact form submission, `tel:` clicks, `mailto:` clicks, and later booking or screening completion.

## Blog / Resources architecture
- Posts live under `/resources/<slug>/`, with categories chosen to match keywords.
- **Life:** Divorce & Separation Mediation · Parenting Plans · Conflict Coaching · Communication Skills · ADR Basics
- **Leadership:** Arbitration & Med-Arb · Business Mediation · Negotiation & NDAs · Board Governance · Leadership Conflict Coaching
- Each post links to its matching service anchor and ends with the site CTA. Use `Article` schema (SEO plugin) and a real author byline (Tanika L. Smith).
- Article ideas to review with the owner (not written yet): "What happens in divorce mediation?", "How to build a parenting plan that works", "Mediation vs. arbitration: which fits a business dispute?", "What is med-arb?", "Negotiating an NDA between organizations: where a neutral helps".
- Don't publish invented case studies, client stories, or statistics.

## Local SEO (needs owner input)
The service area and address aren't in the source documents, so `areaServed` and an address are left out of the schema. Once they're confirmed, add them to `ProfessionalService` and set up a Google Business Profile if in-person sessions have a public location.
