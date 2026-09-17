# TLS project handoff (for a new Claude Code session)

Written 2026-09-14 when this project moved out of an unrelated session. **Read this first**, then `README.md` and the other files in `docs/`.

## Scope boundary
- This project is **only** the two TLS websites, in `C:\Users\Parlevu_Global\lettlshelp.com` (its own git repo).
- **dadstillhere / `dadstillhere.com-landingpage` / the home-folder repo is unrelated.** Don't touch it from this project.

## Client & brands
- Owner: **Tanika L. Smith** · +1 (240) 650-0007 · LinkedIn linkedin.com/in/lettlshelp
- **Both sites launch on lettlshelp.com** (owner's decision, 2026-09-16). Life Solutions at
  `https://lettlshelp.com/`, Leadership Systems at `https://lettlshelp.com/leadership-systems/`.
  Canonicals, sitemap, schema, and the shared Search Console token all use those URLs. The vanity
  domains come later: change `domain`/`base` in `content/{life,leadership}.py` and 301-redirect.
- **Transformative Life Solutions** (later TransformativeLifeSolutions.com): family, parenting, divorce/separation, interpersonal, and workplace (non-consumer-facing only) mediation, plus conflict coaching. Contact: **LifeSolutions@LetTLSHelp.com**.
- **Transformative Leadership Systems** (later TransformativeLeadershipSystems.com): B2B-only arbitration and med-arb, business mediation, negotiation support (including NDAs), and leadership conflict coaching. Contact: **LeadershipSystems@LetTLSHelp.com**. The name is **Systems** (the June draft and signature say "Solutions"; that's wrong).
- The owner's personal Gmail is no longer published on either site.

## Source materials (in ~/Downloads)
- **Source of truth:** `TLS_Website Development Guide_ 09132026.pdf` and `TLS2_Website Development Guide_ 09132026.pdf`. The June 29 drafts in `Guides for Website Design/` are superseded.
- `Logos/Logos/`: JPEG logos. The owner also pasted sharper versions in chat, but those weren't saved to disk; ask for SVG/PNG files.
- `Color Pallets/Color Pallets/`: both palette sheets (the Leadership palette was confirmed in chat).
- `Imagery for Websites/Imagery for Websites/`: 27 sample photos. Which ones are used and why is in `docs/consistency-review.md`.
- The owner's full brief (pages, style, integrations, disclaimers, keywords) is summarized in `docs/architecture.md` and `docs/seo-plan.md`.

## Decisions made with the user
| Decision | Detail |
|---|---|
| Deliverable | Phase 1: HTML wireframe (done). Phase 2: WordPress block theme (`tls-base` parent + `tls-life` / `tls-leadership` children) **after owner approval** |
| Repo | One repo, both sites, shared design system; deployed as two separate WordPress installs; hosting target about $10/mo |
| Confidentiality disclaimer | Show both options on each Terms page, flagged "pending legal review" (the owner's guide wording vs. the brief's "Maryland Rule 17" wording) |
| Keywords | Split by service. The Life site mentions arbitration, negotiation, and NDAs only as links to Leadership Systems |
| Header | **Reversed 2026-09-17.** The plain "Leadership Systems ↗" nav link had been removed at the owner's request, leaving only the footer and cross-link bands. It is back as a **sister-practice band under the header**: the practice name plus its one-line descriptor, with the whole strip as a single link. It is **mutual** — each practice promotes the other. It sits below the nav rather than inside it because the nav already carries six items plus the consultation button, and a 60-character descriptor would wrap them. The hub gets no band: it is the parent of both and already lists them as dropdowns. Rendered by `sister_band()` in `tools/build.py` from each site's `SITE["sister"]` |
| SEO checklist (user-supplied) | Every item is implemented and enforced by `tools/seo_check.py`: meta titles ≤60 chars, descriptions, alt text, one H1 plus heading order, canonical, og:image, schema, sitemap, robots, HTTPS `.htaccess`, WebP, internal links, mobile. **Avoid:** noindex (removed) and broken links (0) |
| Git workflow | **Superseded 2026-09-17: no pull requests.** Commit and push straight to `main` on the new repo, `github.com/Deji147x/lettlshelp.com_website`. (The 2026-09-15 PR rule applied to the old `lettlshelp.com` repo and is no longer in force.) The repo is **PUBLIC**, so never commit API keys or passwords. The GA4 Measurement ID and GSC token are fine |
| Content rule | Never invent credentials, testimonials, client stories, or statistics. Unsourced copy carries a `draft` note that renders as a yellow "Review" flag |

## Current state (2026-09-16)
- **On `main`:** wireframes, the PR workflow, the screening intake pages, and 20 FAQs per site.
- **Open PR:** `feat/cta-tracking-and-emails` — final lowercase addresses, CTA tracking, and the move
  to lettlshelp.com.
- **Built:** 11 pages per site (22 total), including `/begin-intake/`; Life's screening has 14
  questions, Leadership's 18, with ineligible answers ending the screening.
- **Checks:** `seo_check.py` 0 failures, 0 warnings. Forms, CTA events, mobile menu, notes toggle,
  WebP hero, and preload verified in the browser. Git history has no secrets.
- **Still wireframe-only:** forms submit by opening a prefilled email. Replace with a secure
  WordPress form before launch (`docs/tracking-and-forms.md`, `docs/screening-form-spec.md`).

## How to work on it
```bash
python tools/build.py                 # render wireframes from content/*.py
python tools/seo_check.py             # must pass before committing
python -m http.server 8765 --directory wireframes   # preview at http://127.0.0.1:8765/
python tools/process_assets.py        # only when logos/photos in ~/Downloads change (needs Pillow)
```
- Copy lives in `content/life.py`, `content/leadership.py`, and `content/common.py`. Styles are in `design-system/`.
- Each section maps to a planned WordPress pattern; "Show wireframe notes" on any page shows the mapping.

## Open questions for the owner and her attorney
1. Which confidentiality statement per site (legal review)? The Life guide's act name ("Maryland Mediation and Confidentiality Act") may be mis-stated.
2. Confirm the scope for separation agreements, prenuptial agreements, and NDAs (avoid implying legal drafting).
3. Privacy Policy and Terms are outlines only; an attorney must draft them.
4. Service area and address (for local SEO and `areaServed`).
5. Credentials, trainings, and roster listings to display; founder portrait; replacement photos (Black and brown elders, families, civic groups); SVG logos plus a horizontal lockup.
6. How It Works details (session length, fees).
7. **GA4 Measurement IDs** (`G-…`, **not** an API key) — CTA tracking is wired and waiting for them.
   (Search Console is settled: the token belongs to the lettlshelp.com property and is on both sites.)
8. Hosting plan and renewal price; whether Google Workspace fits the budget (see `docs/architecture.md`).

## Suggested next steps
1. Merge the open PR.
2. Share the wireframe with Tanika (e.g., as a private artifact link) and collect answers to the questions above.
3. After approval, build the WordPress block theme from `design-system/tokens.json` plus the pattern map in `docs/architecture.md`, as **one install on lettlshelp.com** (Life at the root, Leadership under `/leadership-systems/`).
4. Rebuild both forms in a WordPress form plugin from `docs/screening-form-spec.md`, then remove the email fallback in `design-system/app.js`.
5. Add the GA4 Measurement ID and mark `generate_lead` as a key event.
6. Start the backlink Phase 1 foundations (`docs/backlink-strategy.md`) once the site is live.
