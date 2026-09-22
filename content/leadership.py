"""Transformative Leadership Systems (TransformativeLeadershipSystems.com): page content.

Sources: 'TLS2_Website Development Guide_ 09132026.pdf' (current) and the owner's brief.
Copy that isn't in those sources carries a `draft` note so it gets owner/legal sign-off.
"""
from common import (COMMERCE_SLOT, FOUNDER_GROUPS, GSC_TOKEN, PHONE,
                    REFERRALS, ROOT_POLICIES)
from common import EMAIL_LEADERSHIP as C_EMAIL_LEADERSHIP
from screening import (LEADERSHIP_INTRO, LEADERSHIP_QUESTIONS, ROLES, STOP_REFERRALS, STOP_TEXT, STOP_TITLE)

# Owner's instruction (vision document, 2026-09-16) for this site. Replaces support@.
EMAIL = C_EMAIL_LEADERSHIP

# Shares lettlshelp.com with Life Solutions; this site is served under /leadership-systems/.
# The root is now the shared hub, so the sister link points at /life-solutions/, not "/".
# Future home: TransformativeLeadershipSystems.com.
SISTER_URL = "https://lettlshelp.com/life-solutions/"

SITE = {
    "key": "leadership",
    "slug": "leadership-systems",
    "name": "Transformative Leadership Systems",
    "word_top": "Transformative",
    "word_bottom": "Leadership Systems",
    "domain": "https://lettlshelp.com",
    "base": "/leadership-systems",
    "root_depth": 1,  # folders between this site's pages and the domain root
    "css": "leadership.css",
    "fonts": "https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Lato:wght@400;700"
             "&family=Playfair+Display:ital@1&display=swap",
    "theme_color": "#0F2040",
    "og_bg": "#F8F8F8",
    "gsc": GSC_TOKEN,  # same lettlshelp.com property as Life while both share the domain
    "ga4_id": None,
    # Google Calendar appointment schedule embed URL (ends in ?gv=true). Set it and the booking
    # section on /contact/ shows the live calendar instead of the placeholder.
    "booking_url": None,
    "email": EMAIL,
    "footer_blurb": "A private ADR practice providing arbitration, mediation, negotiation support, and conflict "
                    "coaching for non-consumer-facing businesses, nonprofits, and professional entities.",
    "short_disclaimer": "Transformative Leadership Systems provides neutral ADR, conflict-coaching, and organizational "
                        "facilitation services only. We do not provide legal advice, legal representation, or legal "
                        "advocacy, or medical, mental health, or clinical therapeutic services.",
    "keywords": ["arbitration", "med-arb", "business mediation", "negotiation", "NDA", "conflict coaching", "ADR",
                 "mediator", "organizational facilitation"],
    # A 2-tuple is a plain link; a 3-tuple adds a dropdown. Every child is a real anchor on the
    # parent's own page, so the submenu is a shortcut and never the only way in.
    "nav": [
        ("", "Home"),
        ("about", "About", [("about#our-founder", "Our Founder"),
                            ("about#completed-trainings", "Completed Trainings"),
                            ("about#credentials", "Credentials"),
                            ("about#affiliations", "Affiliations")]),
        ("services", "Services", [("services#arbitration", "Arbitration & Med‑Arb"),
                                  ("services#mediation", "Business & Organizational Mediation"),
                                  ("services#negotiation", "Negotiation Support"),
                                  ("services#coaching", "Leadership Conflict Coaching")]),
        ("how-it-works", "How It Works"),
        ("faq", "FAQ"),
        ("contact", "Contact"),
    ],
    "nav_external": None,
    "policies": ROOT_POLICIES,  # shared with Life Solutions at the domain root
    "sister": ("Transformative Life Solutions", SISTER_URL, "Family-centered mediation and conflict coaching"),
    "cta": ("contact", "Request a Consultation"),
    "topics": ["Arbitration & Med-Arb", "Business & Organizational Mediation", "Negotiation Support",
               "Conflict Coaching", "Not sure yet"],
}

CONFIDENTIAL_GUIDE = ("All mediation‑related communication will remain confidential in accordance with applicable "
                      "ADR confidentiality standards.")
ETHICS_5502 = ("If your matter involves a consumer transaction, or if you are a consumer‑facing company or "
               "organization, Transformative Leadership Systems cannot assist due to statutory ethics requirements "
               "under Maryland Public Ethics Law §5‑502.")

FAQ = [
    {"q": "What services does Transformative Leadership Systems offer?",
     "a": "Arbitration and med-arb (business-to-business only), business and organizational mediation, negotiation "
          "support, and conflict coaching for leaders."},
    {"q": "What is the difference between mediation, arbitration, and med-arb?",
     "a": "In mediation, a neutral helps the parties reach their own agreement. In arbitration, a neutral hears each "
          "side and issues a decision that may be binding or non-binding, depending on what the parties agree to. "
          "Med-arb combines the two: mediation first, then arbitration for any issues that remain.",
     "draft": "General explanation. Owner to confirm the wording."},
    {"q": "Who is eligible?",
     "a": "Non-consumer-facing business owners, nonprofit organizations, and professional entities. Typical matters "
          "include internal workplace disputes, leadership and partnership conflicts, board governance issues, and "
          "vendor–supplier disputes between non-consumer-facing entities."},
    {"q": "Can you help with NDAs or other business contracts?",
     "a": "Negotiation support includes contract interpretation for non-consumer agreements and inter-organizational "
          "communication. We remain neutral and do not provide legal advice, so each party may wish to consult its "
          "own attorney.",
     "draft": "The NDA reference was added for SEO keywords. Owner to confirm scope."},
    {"q": "Do you work with consumer-facing companies?", "a": "No. " + ETHICS_5502},
    {"q": "Do you provide legal advice?",
     "a": "No. We provide neutral ADR services only. We do not provide legal advice, legal representation, or legal "
          "advocacy."},
    {"q": "Is this counseling or therapy?",
     "a": "No. We provide conflict-coaching and organizational facilitation services only. We do not provide medical "
          "or mental health counseling or clinical therapeutic services."},
    {"q": "Is the process confidential?", "a": CONFIDENTIAL_GUIDE,
     "draft": "Pending legal review. The guide and the brief cite different authorities; see Terms & Disclaimers."},
    {"q": "What happens if my matter isn't eligible?",
     "a": "We use written and verbal screening to determine eligibility and document every screening decision. If we "
          "are unable to facilitate your matter, we will provide free supportive referrals."},
    {"q": "Do you meet virtually or in person?",
     "a": "Both. We serve eligible B2B clients with virtual and in-person options."},
    {"q": "Do you handle family or personal conflicts?",
     "a": f'Family, parenting, and interpersonal matters are handled by our sister practice, '
          f'<a href="{SISTER_URL}">Transformative Life Solutions</a>.'},
    {"q": "How do I get started?",
     "a": f'Call or text <a href="tel:+12406500007">{PHONE}</a>, email <a href="mailto:{EMAIL}">{EMAIL}</a>, '
          f'or send a brief message through the contact page.'},
    # Added 2026-09-16: questions organizations commonly search for. Answers that need the owner's
    # own numbers or an attorney's wording carry a draft flag instead of invented detail.
    {"q": "How much do arbitration, mediation, and negotiation support cost?",
     "a": "Fees depend on the process, the number of parties, and the time involved. We confirm pricing after "
          "screening, before anything is scheduled.",
     "draft": "Owner to supply fees: hourly or daily rate, retainers, arbitration filing or administrative costs, "
              "and how fees are allocated between organizations."},
    {"q": "Who pays for the process?",
     "a": "Organizations commonly share the cost, though the parties can agree on a different split, and a "
          "contract clause may already say who pays.",
     "draft": "Owner to confirm the practice's standard fee-sharing arrangement and deposit requirements."},
    {"q": "How long does a business mediation or arbitration take?",
     "a": "It depends on the complexity of the dispute, the number of parties, and how much documentation is "
          "involved. We give you an estimate after screening.",
     "draft": "Owner to supply typical session or hearing length and how many sessions a B2B matter usually "
              "takes."},
    {"q": "What happens in the first session?",
     "a": "We confirm the process the parties have agreed to, set ground rules and confidentiality expectations, "
          "identify the issues in dispute, and agree on what information is needed to move forward.",
     "draft": "General description of ADR practice. Owner to confirm it matches how she opens a B2B matter."},
    {"q": "Is an arbitration award binding?",
     "a": "That depends on what the parties agreed to. We offer binding, non-binding, and hybrid processes, so "
          "the agreement or contract clause that brings you to arbitration determines the effect of the outcome.",
     "draft": "Pending legal review: confirm this wording, since enforceability is a legal question."},
    {"q": "What is a mediation or arbitration clause in a contract?",
     "a": "It is a term in a business agreement saying that if a dispute arises, the parties will use mediation or "
          "arbitration rather than going straight to court. If your contract already has one, bring it to "
          "screening so we can confirm the process it requires."},
    {"q": "How is arbitration different from going to court?",
     "a": "Arbitration is private, generally faster, and scheduled around the parties rather than a court docket, "
          "and the parties choose their neutral. Court proceedings are public and follow the court's rules and "
          "calendar.",
     "draft": "General comparison. Pending legal review so it does not read as legal advice."},
    {"q": "Can you help with a partnership dispute or a board conflict?",
     "a": "Yes, for eligible non-consumer-facing organizations. We work with internal workplace disputes, "
          "leadership and partnership conflicts, board governance issues, and vendor–supplier disputes between "
          "non-consumer-facing entities."},
]

NOT_HANDLED = [
    "Consumer‑business disputes",
    "Any business that sells goods or services to consumers, such as auto sales or repairs, home improvement, "
    "contractors, retail, hospitality, telecom, or finance",
    "Any matter involving a business regulated by or investigated under Maryland consumer protection laws",
    "Any case where a party has filed a complaint with, been contacted by, or been investigated by the Maryland "
    "Office of the Attorney General",
    "Any matter that could reasonably appear connected to the work of the Consumer Protection Division of Maryland",
]

FOCUS = [
    {"icon": "users", "title": "Internal workplace disputes",
     "text": "Conflict within teams, departments, and staff."},
    {"icon": "layers", "title": "Leadership & partnership conflicts",
     "text": "Disagreements among leaders, co-owners, and business partners."},
    {"icon": "clipboard", "title": "Board governance issues",
     "text": "Governance challenges among board members and leadership."},
    {"icon": "briefcase", "title": "Vendor–supplier disputes",
     "text": "Disputes between non‑consumer‑facing entities."},
]

APPROACH = [
    {"icon": "heart", "title": "Trauma‑informed",
     "text": "A steady, respectful process, even when stakes and emotions run high."},
    {"icon": "globe", "title": "Culturally grounded",
     "text": "Awareness of the identities, cultures, and histories leaders bring to the table."},
    {"icon": "layers", "title": "Organizationally aware",
     "text": "Attention to the structures, roles, and relationships that shape conflict at work."},
]
PILLARS = [
    {"icon": "heart", "title": "Trauma‑informed practice", "text": APPROACH[0]["text"]},
    {"icon": "globe", "title": "Culturally competent care", "text": APPROACH[1]["text"]},
    {"icon": "shield", "title": "Ethical service delivery",
     "text": "Strict ethics protocols, documented screening, and safeguards against conflicts of interest."},
]
DESC_DRAFT = "Headings are from the owner's guide; the one-line descriptions are draft copy for owner review."

STEPS = [
    {"title": "Reach out", "text": f"Call or text {PHONE}, send an email, or begin intake online."},
    {"title": "Eligibility screening",
     "text": "Written and verbal screening confirms your organization and matter are eligible. Every decision is "
             "documented."},
    {"title": "Confirm next steps",
     "text": "If it's a fit, we agree on the right process. If not, we share free supportive "
             "referrals."},
    {"title": "Meet virtually or in person", "text": "Sessions for eligible B2B clients, in the setting that works."},
]
STEPS_DRAFT = ("Steps are drawn from the guide's Screening Protocol and Contact sections. Owner to confirm the order "
               "and add details such as timelines or fees.")

CTA = {"type": "cta", "wf": "Pattern: tls/cta-band", "h2": "Let's talk about your organization's needs",
       "text": "Request a consultation. We'll confirm eligibility through our screening process, and if we can't "
               "assist, we'll provide free supportive referrals.",
       "primary": ("contact", "Request a Consultation")}

CROSSLINK = {"type": "crosslink", "wf": "Pattern: tls/sister-site-link", "tone": "mist",
             "text": "Looking for <strong>family</strong>, <strong>parenting</strong>, or <strong>interpersonal "
                     "mediation</strong>?",
             "href": SISTER_URL, "label": "Visit Transformative Life Solutions"}

PAGES = [
    {
        "slug": "", "label": "Home",
        "title": "B2B Arbitration & ADR | Transformative Leadership Systems",
        "description": "B2B arbitration, med-arb, business mediation, negotiation support, and conflict coaching "
                       "for non-consumer-facing businesses and nonprofits.",
        "sections": [
            {"type": "hero", "wf": "Pattern: tls/hero-split", "eyebrow": "Business‑to‑Business ADR",
             "h1": "Business arbitration, mediation, and negotiation support",
             "tagline": "Helping you transform, lead, and solve.",
             "lede": "Advanced conflict resolution for non‑consumer‑facing business owners, nonprofit organizations, "
                     "and professional entities, with virtual and in‑person options.",
             "primary": ("contact", "Request a Consultation"), "secondary": ("services", "Explore Services"),
             "image": "hero-women-led-meeting",
             "alt": "Women leaders collaborate in a discussion around a conference table"},
            {"type": "text", "wf": "Pattern: tls/intro", "tone": "white", "center": True, "eyebrow": "Who we are",
             "h2": "Conflict resolution with clarity, dignity, and strategic insight",
             "paras": ["Transformative Leadership Systems helps leaders, teams, and organizations navigate conflict. "
                       "We focus exclusively on non‑consumer, non‑public‑facing conflicts that support healthy "
                       "communication, effective decision‑making, and sustainable agreements."]},
            {"type": "cards", "wf": "Pattern: tls/services-grid", "tone": "soft", "eyebrow": "Services",
             "h2": "How we can help",
             "items": [
                 {"icon": "scale", "title": "Arbitration & Med‑Arb",
                  "text": "Binding, non‑binding, or hybrid dispute resolution for eligible organizations (B2B only).",
                  "link": ("services#arbitration", "About arbitration")},
                 {"icon": "users", "title": "Business Mediation",
                  "text": "Internal workplace disputes, leadership conflicts, and partnership disagreements.",
                  "link": ("services#mediation", "About business mediation")},
                 {"icon": "message", "title": "Negotiation Support",
                  "text": "High‑stakes conversations and non‑consumer contract interpretation.",
                  "link": ("services#negotiation", "About negotiation support")},
                 {"icon": "target", "title": "Conflict Coaching",
                  "text": "One‑on‑one support for executives, managers, team leads, and board members.",
                  "link": ("services#coaching", "About conflict coaching")},
             ],
             "link": ("services", "View all services")},
            {"type": "cards", "wf": "Pattern: tls/audience-grid", "tone": "white", "center": True,
             "eyebrow": "Who we serve", "h2": "Built for non‑consumer‑facing organizations",
             "items": [
                 {"icon": "briefcase", "title": "Business owners",
                  "text": "Owners of non‑consumer‑facing businesses."},
                 {"icon": "heart", "title": "Nonprofit organizations",
                  "text": "Nonprofits and their leadership teams."},
                 {"icon": "layers", "title": "Professional entities",
                  "text": "Professional organizations working through internal or inter‑organizational conflict."},
                 {"icon": "users", "title": "Executives & team leads",
                  "text": "Executives, managers, and team leads."},
                 {"icon": "clipboard", "title": "Boards of directors",
                  "text": "Board members navigating governance issues."},
                 {"icon": "globe", "title": "Business partners",
                  "text": "Partners, vendors, and suppliers between non‑consumer‑facing entities."},
             ]},
            {"type": "split", "wf": "Pattern: tls/media-text (approach)", "tone": "soft", "eyebrow": "Our approach",
             "h2": "Trauma‑informed. Culturally grounded. Organizationally aware.",
             "paras": ["We help leaders, teams, and organizations navigate conflict with clarity, dignity, and "
                       "strategic insight."],
             "bullets": [f"<strong>{p['title']}:</strong> {p['text'][0].lower() + p['text'][1:]}" for p in APPROACH],
             "draft": DESC_DRAFT, "image": "leader-dialogue",
             "alt": "A leader listens closely as a colleague shares her perspective during a meeting",
             "link": ("about", "About our practice")},
            {"type": "cards", "wf": "Pattern: tls/focus-grid", "tone": "white", "eyebrow": "Focus areas",
             "h2": "Matters we focus on", "items": FOCUS},
            {"type": "steps", "wf": "Pattern: tls/process-steps", "tone": "mist", "eyebrow": "How it works",
             "h2": "A structured, neutral process", "items": STEPS, "link": ("how-it-works", "See how it works")},
            {"type": "cards", "wf": "Pattern: tls/trust-grid", "tone": "white", "center": True,
             "eyebrow": "Trust & credibility", "h2": "Neutral, ethical, and transparent",
             "draft": "Confidentiality wording is pending legal review. Credentials appear only once the owner "
                      "supplies them.",
             "items": [
                 {"icon": "shield", "title": "Ethics compliance",
                  "text": "Operates in full compliance with Maryland Public Ethics Law §5‑502."},
                 {"icon": "clipboard", "title": "Documented screening",
                  "text": "Written and verbal screening, with every eligibility decision documented."},
                 {"icon": "check", "title": "Free referrals",
                  "text": "If we can't assist, we provide free supportive referrals."},
                 {"icon": "lock", "title": "Confidential process",
                  "text": "Mediation‑related communication remains confidential."},
             ],
             # The owner supplied real trainings, credentials, and affiliations in the vision
             # document, so the old "owner to supply" placeholder is gone; this links to them.
             "link": ("about#credentials", "See credentials & affiliations")},
            {"type": "notlist", "wf": "Pattern: tls/scope-notice", "tone": "soft", "h2": "What we don't handle",
             "intro": "We do not mediate, arbitrate, coach, or negotiate matters involving:",
             "bullets": ["Consumer‑business disputes",
                         "Businesses that sell goods or services to consumers",
                         "Any matter connected to Maryland consumer protection laws or the Office of the Attorney "
                         "General"],
             "link": ("/ethics", "Read our ethics commitment")},
            {"type": "faq", "wf": "Pattern: tls/faq-preview (Details blocks)", "tone": "white", "center": True,
             "eyebrow": "FAQ", "h2": "Common questions", "items": [FAQ[1], FAQ[12], FAQ[4]],
             "link": ("faq", "See all questions")},
            CROSSLINK,
            CTA,
        ],
    },
    {
        "slug": "about", "label": "About", "schema_type": "AboutPage",
        "title": "About Tanika L. Smith | Transformative Leadership Systems",
        "description": "Transformative Leadership Systems was founded by Tanika L. Smith, an ADR practitioner and "
                       "organizational communication strategist.",
        "sections": [
            {"type": "page_hero", "eyebrow": "About", "h1": "About Transformative Leadership Systems",
             "lede": "Neutral, ethical conflict resolution for leaders and organizations."},
            {"type": "split", "id": "our-founder", "wf": "Pattern: tls/founder", "tone": "white",
             "eyebrow": "Our founder", "h2": "Founded by Tanika L. Smith",
             "paras": ["Transformative Leadership Systems was founded by Tanika L. Smith, a seasoned alternative "
                       "dispute resolution (ADR) practitioner and organizational communication strategist."],
             },
            {"type": "credgroups", "wf": "Pattern: tls/founder-credentials", "tone": "soft",
             "groups": FOUNDER_GROUPS},
            {"type": "cards", "wf": "Pattern: tls/pillars", "tone": "white", "center": True, "eyebrow": "Our pillars",
             "h2": "Three pillars guide our work", "items": PILLARS, "draft": DESC_DRAFT},
            {"type": "text", "wf": "Pattern: tls/text", "tone": "soft", "h2": "Strict ethics protocols",
             "paras": ["We maintain strict ethics protocols, and all services are structured to avoid conflicts of "
                       "interest and to protect integrity."],
             "link": ("/ethics", "Ethics & Compliance")},
            {"type": "split", "wf": "Pattern: tls/media-text", "tone": "mist", "reverse": True,
             "h2": "Serving eligible B2B clients",
             "paras": ["We work with eligible business‑to‑business clients through virtual and in‑person options."],
             "image": "conference-room-team",
             "alt": "A diverse team meets around a long table in a bright conference room"},
            CTA,
        ],
    },
    {
        "slug": "services", "label": "Services",
        "title": "Arbitration Services | Transformative Leadership Systems",
        "description": "B2B arbitration and med-arb, business and organizational mediation, negotiation support "
                       "including NDAs, and conflict coaching for leaders.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Services", "h1": "Business ADR services",
             "lede": "Arbitration, mediation, negotiation support, and conflict coaching for non‑consumer‑facing "
                     "organizations."},
            {"type": "split", "id": "arbitration", "wf": "Pattern: tls/service-detail", "tone": "white",
             "eyebrow": "Arbitration & Med‑Arb (B2B Only)", "h2": "Arbitration and med‑arb",
             "paras": ["Neutral resolution processes for eligible organizations seeking binding, non‑binding, or "
                       "hybrid dispute resolution."],
             "bullets": ["Binding arbitration", "Non‑binding arbitration", "Hybrid med‑arb processes"],
             "image": "facilitated-negotiation",
             "alt": "A neutral facilitator reviews documents with two business representatives"},
            {"type": "split", "id": "mediation", "wf": "Pattern: tls/service-detail", "tone": "soft",
             "reverse": True, "eyebrow": "Business & Organizational Mediation",
             "h2": "Business and organizational mediation",
             "paras": ["Support for internal workplace disputes, leadership conflicts, partnership disagreements, and "
                       "organizational communication challenges."],
             "bullets": ["Internal workplace disputes", "Leadership conflicts", "Partnership disagreements",
                         "Organizational communication challenges"],
             "image": "business-meeting", "alt": "Colleagues shake hands across a meeting table after a discussion"},
            {"type": "split", "id": "negotiation", "wf": "Pattern: tls/service-detail", "tone": "white",
             "eyebrow": "Negotiation Support", "h2": "Negotiation support",
             "paras": ["Assistance for leaders navigating high‑stakes conversations, contract interpretation "
                       "(non‑consumer), and inter‑organizational communication."],
             "bullets": ["High‑stakes conversations", "Non‑consumer contract interpretation, including NDAs",
                         "Inter‑organizational communication"],
             "after": ["We remain neutral and do not provide legal advice. Each party may wish to consult its own "
                       "attorney."],
             "draft": "The NDA reference was added for SEO keywords. Owner to confirm scope.",
             "image": "signing-agreement", "alt": "A hand signs a business agreement with a pen"},
            {"type": "split", "id": "coaching", "wf": "Pattern: tls/service-detail", "tone": "soft", "reverse": True,
             "eyebrow": "Conflict Coaching", "h2": "Conflict coaching for leaders",
             "paras": ["One‑on‑one support for executives, managers, team leads, and board members seeking to "
                       "strengthen communication, decision‑making, and conflict‑management skills."],
             "bullets": ["Executives and managers", "Team leads", "Board members"],
             "image": "leaders-in-conversation", "alt": "Two professional women talk through ideas at a conference table"},
            {"type": "notlist", "wf": "Pattern: tls/scope-notice", "tone": "mist", "h2": "What we do not handle",
             "intro": "Transformative Leadership Systems does not mediate, arbitrate, coach, or negotiate matters "
                      "involving:",
             "bullets": NOT_HANDLED, "outro": ETHICS_5502, "link": ("/ethics", "Ethics & Compliance")},
            dict(CROSSLINK, tone="white"),
            {"type": "slot", "tone": "white", **COMMERCE_SLOT},
            CTA,
        ],
    },
    {
        "slug": "how-it-works", "label": "How It Works",
        "title": "Our ADR Process | Transformative Leadership Systems",
        "description": "Reach out, complete documented eligibility screening, confirm the right process, and meet "
                       "virtually or in person. Free referrals if we can't assist.",
        "sections": [
            {"type": "page_hero", "eyebrow": "How It Works", "h1": "How our process works",
             "lede": "Structured, neutral, and transparent from the first conversation."},
            {"type": "steps", "wf": "Pattern: tls/process-steps", "tone": "white", "h2": "What to expect",
             "items": STEPS, "draft": STEPS_DRAFT},
            {"type": "text", "wf": "Pattern: tls/intake-cta", "tone": "soft", "eyebrow": "Step one",
             "h2": "Begin intake online",
             "paras": ["Our online screening confirms eligibility first, then asks about the services you need, "
                       "availability, and any court or safety considerations. We reply with next steps or free "
                       "referrals."],
             "link": ("begin-intake", "Start the screening")},
            {"type": "list", "wf": "Pattern: tls/referrals", "tone": "white",
             "h2": "If we can't assist, we'll point you to support",
             "intro": "If we are unable to facilitate your matter, we will provide free supportive "
                      "referrals. Suggested referrals may include:",
             "items": REFERRALS},
            {"type": "text", "wf": "Pattern: tls/text", "tone": "mist", "h2": "Before you begin",
             "bullets": ["We provide neutral ADR services only. We do not provide legal advice, legal representation, "
                         "or legal advocacy.",
                         "We provide conflict‑coaching and organizational facilitation services only. We do not "
                         "provide medical or mental health counseling or clinical therapeutic services."],
             "link": ("/disclaimers", "Read all disclaimers")},
            CTA,
        ],
    },
    # Resources (the blog index) was removed on the owner's instruction, 2026-09-16. The renderer
    # and the "posts" section type are still in tools/build.py, so restoring it is a paste job --
    # see git history for the original block.
    {
        "slug": "faq", "label": "FAQ",
        "title": "Arbitration FAQ | Transformative Leadership Systems",
        "description": "Answers about arbitration, med-arb, business mediation, NDAs, eligibility, confidentiality, "
                       "and getting started with Transformative Leadership Systems.",
        "sections": [
            {"type": "page_hero", "eyebrow": "FAQ", "h1": "Frequently asked questions",
             "lede": "Clear answers about eligibility, processes, and boundaries."},
            {"type": "faq", "wf": "Pattern: tls/faq (Details blocks + FAQPage schema)", "tone": "white",
             "items": FAQ, "schema": True},
            CTA,
        ],
    },
    {
        "slug": "contact", "label": "Contact", "schema_type": "ContactPage",
        "title": "Contact | Transformative Leadership Systems",
        "description": f"Request a consultation for B2B arbitration, mediation, or negotiation support. Call or "
                       f"text (240) 650-0007 or email {EMAIL}.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Contact", "h1": "Contact Transformative Leadership Systems",
             "lede": "Private ADR, Arbitration, Mediation & Conflict Coaching Practice. Serving eligible B2B clients "
                     "with virtual and in‑person options."},
            {"type": "contact", "tone": "white"},
            {"type": "booking", "wf": "Block: Google Calendar appointment schedule (embed)", "tone": "soft",
             "eyebrow": "Scheduling", "h2": "Book a consultation",
             "intro": "Pick a time that works for your organization once online booking is live."},
        ],
    },
    {
        "slug": "begin-intake", "label": "Begin Intake",
        "title": "Begin Intake | Transformative Leadership Systems",
        "description": "Complete our B2B screening: eligibility checks, the services you need, availability, and "
                       "any court considerations. We reply with next steps or free referrals.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Screening", "h1": "Begin intake",
             "lede": "A short, private screening so we can confirm whether your matter is one we can ethically "
                     "accept."},
            {"type": "intake", "wf": "Pattern: tls/screening-form (18 questions)", "tone": "mist",
             "h2": "Screening questions",
             "intro": LEADERSHIP_INTRO, "questions": LEADERSHIP_QUESTIONS, "roles": ROLES,
             "stop_title": STOP_TITLE, "stop_text": STOP_TEXT, "stop_referrals": STOP_REFERRALS,
             "outro": "We look forward to receiving your responses and determining your eligibility.",
             "draft": "Screening wording supplied by the owner. Before launch, replace the email hand-off with a "
                      "secure WordPress form (encrypted storage and retention rules) and confirm what is kept."},
        ],
    },
    # Ethics & Compliance, Disclaimers and Privacy Policy moved to the domain root on the owner's
    # instruction, 2026-09-16: one copy of each, serving both practices. They are built from
    # content/hub.py, and the old per-practice URLs 301 there.
]
