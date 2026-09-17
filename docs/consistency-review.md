# Consistency review (2026-09-14)

Sources reviewed:

- `TLS_Website Development Guide_ 09132026.pdf` (Life Solutions, **current**)
- `TLS2_Website Development Guide_ 09132026.pdf` (Leadership Systems, **current**)
- `FOR DEJI_06_29_2026_…Website Plan.pdf` ×2 (June drafts, superseded)
- The owner's website brief (pages, style, integrations, disclaimers, SEO keywords)
- Logos, two color palettes, and 27 sample photos

Every item still needing a decision is also flagged in yellow ("Review") on the wireframe pages.

## Decisions made

| Topic | Decision |
|---|---|
| Deliverable | HTML wireframe first. After approval it becomes a WordPress block theme. |
| Repo | One repo, two sites, one shared design system. Deployed as two separate WordPress installs. |
| Brand name | **Transformative Leadership *Systems***. The June file name and the email signature say "Solutions"; the logo, guides, and domain say "Systems". |
| Source of truth | 09/13/2026 guides. They dropped the June "Alternate Compliance-Safe Explanation" and the "View Ethics Framework" link, so neither is used. |
| Confidentiality disclaimer | Both wordings are shown on each site's Terms & Disclaimers page and flagged for legal review (see below). |
| Keywords | Split by service. The Life site also names arbitration, negotiation, and NDAs, but only as links to Leadership Systems, because the guide lists arbitration as B2B-only. |

## Inconsistencies found

### Content & pages
1. **Page list vs guides.** The brief lists 10 pages. The guides include an **Ethics & Compliance** page that isn't in the brief (kept and linked in the footer). The guides have **no content for How It Works or FAQ**. Both pages were built only from the guides' Screening Protocol, Services, Disclaimer, and Contact text, and are marked for owner review.
2. **Home services list vs Services page (Life).** Home lists 5 services ("Parenting & Co-Parenting Support" separate). The Services page has 4. The wireframe uses the 4 Services-page groups, with co-parenting folded into Family & Parenting Mediation.
3. **About wording changed between drafts.** June: "seasoned mediator, conflict-resolution practitioner…". September: "seasoned alternative dispute resolution (ADR) practitioner…". September wording used.
4. **Referral list changed.** June "MPME-rostered facilitators" became "MPME-rostered ADR practitioners" (September used). No referral has a verified link yet.
5. **Typos in source PDFs (not copied):** "Smiith" (header), "banded email address" (TLS2 contact), "organizations ly" (June).

### Legal wording (needs attorney review)
6. **Three different confidentiality statements:**
   - Brief: *"Per Maryland Rule 17 … cannot be compelled to disclose any mediation **or arbitration** communication … not subject to discovery."*
   - Life guide: *"In accordance with the **Maryland Mediation and Confidentiality Act** …"* plus *"Maryland Standards of Conduct for Mediators."* The act's name may be mis-stated; confirm the exact title.
   - Leadership guide: *"…in accordance with **applicable ADR confidentiality standards**."*

   These cite different authorities, and arbitration confidentiality isn't the same as mediation confidentiality. Pick one per site.
7. **§5-502 citation.** The brief and the Leadership guide cite Maryland Public Ethics Law §5-502; the Life guide cites the law without a section. The brief's wording is used on both Terms pages.
8. **Keywords vs "no legal advice."** "Separation agreement", "prenuptial agreement", and "NDA" could read as legal document drafting. The copy frames them as *mediating or negotiating terms*, adds "you may wish to have your own attorney review", and is flagged for scope confirmation.
9. **Privacy Policy & Terms** are outlines only. An attorney must draft them before launch.

### Brand & accessibility
10. **Palette colors that fail WCAG text contrast.** They're used only for decoration, never for text:

| Color | On white | Use |
|---|---|---|
| Life Warm Gold `#D4AF37` | 2.10 : 1 | accent lines only |
| Life Soft Grey-Blue `#8BABB1` | 2.45 : 1 | decorative |
| Life Warm Teal-Grey `#A0B7B9` | 2.11 : 1 | background tints |
| Life Silver-Grey `#C1C7CE` | 1.70 : 1 | borders |
| Leadership Ocher `#C89B5F` | 2.53 : 1 | accent lines only |
| Leadership Light Blue-Grey `#8CB5C2` | 2.21 : 1 | background tints |
| Leadership **"Neutral Grey Text" `#7A7A7A`** | 4.29 : 1 (4.04 on `#F8F8F8`) | **below 4.5 : 1 for body text.** Darkened to `#51595C` (6.74 : 1) for secondary text |

    Passing pairs used for text: Life teal `#006B7B` 6.20 : 1, navy-teal `#003853` 12.42 : 1; Leadership blue `#0F2040` 16.1 : 1, teal-green `#2B4E47` 9.20 : 1.
11. **Logos are JPEGs** on an off-white, slightly gradient background, with no transparent or vector versions. Transparent PNGs and favicons were cut from them automatically (`tools/process_assets.py`). **Ask the designer for SVG and horizontal lockups.** The header currently pairs the official mark with the name set in the brand heading font, which is a derived lockup to confirm.
12. **Typography.** Lora + Open Sans (Life) and Merriweather + Lato (Leadership), both from the brief's options, so the sites feel related but distinct. Playfair Display italic is used only for taglines.

### Photography
13. **Not used, with reasons:**
    - `134f498d…`, `7512e8a7…`, `978b21bf…`, `Board-768x509`: unknown source and license. `Board` is also only 768 px wide.
    - `pexels-a-darmel-6643024` and `pexels-liza-summer-6382681`: they show visible distress (a partner walking out; pointing and blaming), which doesn't suit a trauma-informed tone.
    - `pexels-cottonbro-4841959/4841970`: children, not young adults.
14. **Gaps against the imagery brief.** The only elders photo (`pexels-priscilla-cezar…`) shows no Black or brown elders, and there's no family-with-children or civic-group photo. The About page uses a placeholder until better photos are supplied.
15. **No founder photo supplied.** A slot is reserved; stock photos are never used for the founder.

### Setup
16. **Google Analytics:** GA4 needs a **Measurement ID** (`G-XXXXXXXXXX`), not an API key. Never paste API keys into chat or this **public** repository.
17. **Search Console token** (`nueZtT3Z…`) came without a domain. It's placed on the Life site as a meta tag. Confirm which property it belongs to; Leadership Systems needs its own.
18. **Future emails** (`Services@…`) aren't active yet; the wireframe labels them "not active yet".

## Open questions for the owner
- Which confidentiality statement per site (after legal review)?
- Confirm the scope for separation agreements, prenuptial agreements, and NDAs.
- Service area for local SEO (Maryland only? statewide? virtual nationwide?) and whether to show a business address.
- Credentials, trainings, and roster listings to display (none are shown until supplied).
- Founder portrait; replacement elders, family, and civic-group photos.
- Session details for How It Works (length, fees, what to bring).
- Which domain the Search Console token was issued for; the GA4 Measurement ID(s).
