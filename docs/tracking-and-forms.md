# Call-to-action tracking and form activation

## What is tracked

Every call to action carries `data-cta` (what it is) and `data-cta-page` (where it was clicked).
`design-system/app.js` turns clicks into analytics events. It sends GA4 events when a Measurement
ID is configured and always pushes to `dataLayer`, so Google Tag Manager can read the same events.
With neither installed, nothing breaks and nothing is sent.

### Events

| Event | Fires when | Parameters |
| --- | --- | --- |
| `cta_click` | Any `[data-cta]` element is clicked | `cta_id`, `cta_page`, `cta_type` (call / email / navigate), `link_url`, `link_text` |
| `generate_lead` | A contact or screening form passes validation and submits | `form_id` (contact / screening), `method` |
| `form_submit` | Same moment as above | `form_id` |
| `screening_ineligible` | An answer marks the matter ineligible | `form_id`, `question` |

`generate_lead` is a GA4 recommended event, so mark it as a **key event (conversion)** in GA4.

### `cta_id` values

| `cta_id` | Where |
| --- | --- |
| `header-consultation` | "Request a Consultation" button in the header |
| `call-utility`, `email-utility` | Top contact bar |
| `call-hero` | "Prefer to talk?" line under the hero |
| `call-cta`, `email-cta` | Phone and email in the closing call-to-action band |
| `call`, `email` | Contact page cards |
| `intake-start` | "Start the screening" on the contact page |
| `start-the-screening` | "Start the screening" button on How It Works |
| `request-a-consultation`, `explore-services`, `see-all-questions`, … | Buttons, derived from their text |
| `card-<service>` | Service and topic cards |
| `sister-site` | Cross-links between the two practices |

## Turning GA4 on

1. Create a GA4 property per domain and copy each Measurement ID (`G-XXXXXXXXXX`).
   A Measurement ID is **not** an API key and is safe to commit.
2. Put it in `content/life.py` / `content/leadership.py` → `SITE["ga4_id"]`, then `python tools/build.py`.
   The gtag snippet is then written into every page.
3. In WordPress, prefer **Site Kit** (or GTM) to inject the tag, and leave `ga4_id` unset so the tag
   isn't added twice.
4. In GA4, mark `generate_lead` as a key event. Optionally build audiences from `cta_click` where
   `cta_type = call`.

Using Tag Manager instead: add the container as usual and create Custom Event triggers for
`cta_click`, `generate_lead`, and `screening_ineligible`. No page changes are needed.

## Form activation

Today both forms validate, then open the visitor's email app with the answers filled in and copy
them to the clipboard. That needs no server, which suits the wireframe, but it depends on the
visitor having an email app and it is not private enough for screening answers.

**Before launch**, rebuild each form in WordPress:

1. Use `docs/screening-form-spec.md` (generated from `content/screening.py`) to recreate the
   screening in a form plugin. Keep the field names.
2. Route notifications to the site's address: Life → `services@lettlshelp.com`,
   Leadership → `support@lettlshelp.com`.
3. Send mail through an authenticated service (Google Workspace SMTP or an SMTP plugin) so
   notifications aren't treated as spam. Confirm SPF, DKIM, and DMARC for `lettlshelp.com`.
4. Turn on spam protection that doesn't profile visitors (honeypot or Cloudflare Turnstile ahead of
   reCAPTCHA).
5. Set entry retention and restrict who can read entries. Screening answers include safety and
   court details.
6. Point the form's confirmation at a thank-you page and fire `generate_lead` there, or keep the
   inline event by adding `data-cta` to the plugin's submit button.

Remove the wireframe fallback from `app.js` once the real forms are live.
