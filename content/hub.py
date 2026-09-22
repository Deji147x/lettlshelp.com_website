"""LetTLSHelp.com: the shared hub that both practices sit under.

Source: the owner's vision document, 2026-09-16. The Home, Ethics & Compliance,
Disclaimers and Contact copy is verbatim from it; nothing has been added.

Home-page and general enquiries go to LifeSolutions@LetTLSHelp.com, and the hub
carries the Transformative Life Solutions logo (owner's instructions, 2026-09-22).
The footer and the Contact page still offer both practice addresses, so anyone who
already knows which practice they need can write to it directly.
"""
from common import (CONFIDENTIALITY_ACT, CONFIDENTIALITY_REVIEW, EMAIL_LEADERSHIP, EMAIL_LIFE,
                    ETHICS_COMMITMENT, ETHICS_COMPLIANCE_SAFE, ETHICS_REFERRAL_INTRO,
                    ETHICS_SCOPE_LEADERSHIP, ETHICS_SCOPE_LIFE, ETHICS_SCREENING, GSC_TOKEN,
                    LEGAL_REVIEW, NOT_PROVIDED, NOT_PROVIDED_INTRO, PRIVACY_OUTLINE,
                    PROFESSIONAL_STANDARDS, REFERRALS, ROOT_POLICIES)
from screening import STOP_TEXT, STOP_TITLE

LIFE_URL = "https://lettlshelp.com/life-solutions/"
LEADERSHIP_URL = "https://lettlshelp.com/leadership-systems/"

SITE = {
    "key": "hub",
    "slug": "",  # renders straight into wireframes/
    "name": "LetTLSHelp",
    # Owner's instruction (2026-09-22): the home page carries the Transformative Life Solutions
    # logo and lockup. tools/build.py copies the mark and full logo from that practice's assets.
    "word_top": "Transformative",
    "word_bottom": "Life Solutions",
    "brand_from": "life-solutions",
    "domain": "https://lettlshelp.com",
    "base": "",
    "root_depth": 0,  # the hub IS the root
    "css": "hub.css",
    "fonts": "https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Open+Sans:wght@400;600;700"
             "&family=Playfair+Display:ital@1&display=swap",
    "theme_color": "#003853",
    "og_bg": "#F4F7F8",
    "gsc": GSC_TOKEN,
    "ga4_id": None,  # e.g. "G-XXXXXXXXXX"; a Measurement ID, not an API key
    "booking_url": None,
    # Home-page and general enquiries go to Life Solutions (owner's instruction, 2026-09-22).
    "email": EMAIL_LIFE,
    "footer_blurb": "Two sister practices offering private, alternative dispute resolution services that help "
                    "transform lives: family-centered mediation and conflict coaching, and business-to-business "
                    "conflict resolution.",
    "short_disclaimer": "Neutral ADR, conflict-coaching, and organizational facilitation services only. We do not "
                        "provide legal advice, legal representation, or legal advocacy, or medical, mental health, "
                        "or clinical therapeutic services.",
    "keywords": ["alternative dispute resolution", "ADR", "mediation", "arbitration", "conflict coaching",
                 "Maryland mediator"],
    "nav": [
        ("", "Home"),
        ("life-solutions", "Life Solutions", [("life-solutions", "Overview"),
                                              ("life-solutions/about", "About"),
                                              ("life-solutions/services", "Services"),
                                              ("life-solutions/how-it-works", "How It Works"),
                                              ("life-solutions/faq", "FAQ"),
                                              ("life-solutions/contact", "Contact")]),
        ("leadership-systems", "Leadership Systems", [("leadership-systems", "Overview"),
                                                      ("leadership-systems/about", "About"),
                                                      ("leadership-systems/services", "Services"),
                                                      ("leadership-systems/how-it-works", "How It Works"),
                                                      ("leadership-systems/faq", "FAQ"),
                                                      ("leadership-systems/contact", "Contact")]),
        ("ethics", "Ethics & Compliance"),
        ("contact", "Contact"),
    ],
    "nav_external": None,
    "policies": ROOT_POLICIES,
    "sister": None,  # the hub has no sister; it is the parent of both
    "cta": ("contact", "Start a Screening"),
    "topics": [],
}

# The two practice cards. Service lists are verbatim from the vision document.
PRACTICES = [
    {
        "key": "life",
        "name": "Transformative Life Solutions",
        "href": LIFE_URL,
        "path": "life-solutions",
        "services": ["Family‑Centered Mediation", "Conflict Coaching", "Communication Facilitation"],
        "scope": "For private, non‑commercial conflicts: family, interpersonal, workplace "
                 "(non‑consumer‑facing) and community matters.",
        "email": EMAIL_LIFE,
        "explore": "Explore Life Solutions",
    },
    {
        "key": "leadership",
        "name": "Transformative Leadership Systems",
        "href": LEADERSHIP_URL,
        "path": "leadership-systems",
        "services": ["Business‑to‑Business Conflict Resolution", "Organizational Facilitation",
                     "Leadership & Partnership Dispute Support"],
        "scope": "For private, non‑consumer‑facing organizational conflicts: internal workplace disputes, "
                 "board governance and vendor–supplier matters.",
        "email": EMAIL_LEADERSHIP,
        "explore": "Explore Leadership Systems",
    },
]

# The home page's three questions, as a working form (owner's markup, 2026-09-20: "Can those
# three questions become the screening for that box?"). Answers go to LifeSolutions@ — the
# owner's instruction for home-page and general enquiries, 2026-09-22. It uses the same form
# machinery as the two practice intakes, so a "Yes" to the consumer question shows the same
# "we cannot assist" notice, here with the full linked referral list.
GENERAL_SCREENING = {
    "type": "intake", "wf": "Pattern: tls/screening-form (3 questions, general)", "tone": "soft",
    "h2": "Not sure which practice?",
    "intro": ["Answer three quick questions and we will point you to the right practice. Nothing "
              "confidential is asked before eligibility is confirmed."],
    "questions": [
        {"q": "Who is involved?",
         "options": [{"label": "Individuals or family members"},
                     {"label": "An organization, its leaders, or its partners"},
                     {"label": "Not sure"}]},
        {"q": "Is this a consumer matter?",
         "help": "For example, a dispute with a business about something you bought, a bill, a warranty, "
                 "or a service agreement.",
         "options": [{"label": "No"},
                     {"label": "Yes", "stop": True},
                     {"label": "Not sure", "note": "That's fine. We will confirm during screening."}]},
        {"q": "What kind of support are you looking for?",
         "options": [{"label": "Mediation"}, {"label": "Arbitration or med-arb"},
                     {"label": "Facilitation"}, {"label": "Conflict coaching"},
                     {"label": "Not sure yet"}]},
    ],
    "roles": [], "stop_title": STOP_TITLE, "stop_text": STOP_TEXT, "stop_referrals": REFERRALS,
    "draft": "Question wording drafted from the owner's three home-page steps. Owner to confirm.",
}

CTA = {"type": "cta", "wf": "Pattern: tls/cta-band", "h2": "Call or text us",
       "text": "Virtual and in‑person options during off‑peak hours. Serving eligible clients in Maryland and beyond.",
       "primary": ("contact", "Contact Us")}

PAGES = [
    {
        "slug": "", "label": "Home",
        "title": "Private Dispute Resolution in Maryland | LetTLSHelp",
        "description": "Two sister ADR practices: family-centered mediation and conflict coaching, and "
                       "business-to-business conflict resolution. Read how each works, then screen in.",
        "sections": [
            {"type": "hub_hero", "wf": "Pattern: tls/hub-hero",
             "eyebrow": "Private alternative dispute resolution",
             "h1": "We help transform lives through private dispute resolution",
             "tagline": "Two sister practices. One place to start.",
             "lede": "Transformative Life Solutions and Transformative Leadership Systems offer private, "
                     "alternative dispute resolution services. Read how each one works, then complete a short "
                     "screening for the practice that fits your matter.",
             "primary": ("#practices", "Learn more about how we help"),
             # The hero runs as type only. The owner removed the "supply a hero image"
             # placeholder (markup, 2026-09-20); add "image"/"alt" here to bring one back.
             },
            {"type": "practices", "id": "practices", "wf": "Pattern: tls/practice-cards", "tone": "white",
             "h2": "Choose the practice that fits your matter",
             "items": PRACTICES},
            GENERAL_SCREENING,
            {"type": "split", "wf": "Pattern: tls/scope-notice", "tone": "white",
             "h2": "Our commitment to ethical practice",
             "paras": [ETHICS_COMMITMENT, ETHICS_COMPLIANCE_SAFE],
             "link": ("ethics", "Read Ethics & Compliance"),
             "media_slot": {
                 "label": "If we cannot help",
                 "title": "Free supportive referrals",
                 "text": "We point you to seven trusted organizations. The full list is on the "
                         "Ethics & Compliance page.",
             }},
            CTA,
        ],
    },
    {
        "slug": "ethics", "label": "Ethics & Compliance",
        "title": "Ethics, Compliance & Screenings | LetTLSHelp",
        "description": "How both practices comply with Maryland Public Ethics Law §5-502, screen every matter, "
                       "and provide free supportive referrals when a matter is not eligible.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Ethics & Compliance", "h1": "Ethics, Compliance, and Screenings",
             },
            {"type": "text", "wf": "Pattern: tls/text", "tone": "white",
             "h2": "Our Commitment to Ethical Practice", "paras": [ETHICS_COMMITMENT]},
            {"type": "text", "wf": "Pattern: tls/text", "tone": "soft",
             "h2": "Compliance‑Safe Explanation", "paras": [ETHICS_COMPLIANCE_SAFE]},
            {"type": "cards", "wf": "Pattern: tls/scope-split", "tone": "white",
             "h2": "What each practice focuses on",
             "items": [
                 {"icon": "heart", "title": "Transformative Life Solutions", "text": ETHICS_SCOPE_LIFE},
                 {"icon": "briefcase", "title": "Transformative Leadership Systems",
                  "text": ETHICS_SCOPE_LEADERSHIP},
             ]},
            {"type": "text", "wf": "Pattern: tls/text", "tone": "soft", "h2": "Screening Protocol",
             "paras": [ETHICS_SCREENING, ETHICS_REFERRAL_INTRO]},
            {"type": "list", "wf": "Pattern: tls/referrals", "tone": "white",
             "h2": "Suggested referrals", "items": REFERRALS},
            CTA,
        ],
    },
    {
        "slug": "disclaimers", "label": "Disclaimers",
        "title": "ADR Disclaimers & Confidentiality | LetTLSHelp",
        "description": "What we do and do not provide, confidentiality of mediation-related communication, and "
                       "the professional standards our practitioners abide by.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Disclaimers", "h1": "Disclaimers",
             "lede": "Covers both Transformative Life Solutions and Transformative Leadership Systems."},
            {"type": "notprovided", "wf": "Pattern: tls/disclaimers", "tone": "white",
             "h2": "What we do not provide", "intro": NOT_PROVIDED_INTRO, "items": NOT_PROVIDED},
            {"type": "text", "wf": "Pattern: tls/text", "tone": "soft", "h2": "Confidentiality",
             "paras": [CONFIDENTIALITY_ACT], "draft": CONFIDENTIALITY_REVIEW},
            {"type": "text", "wf": "Pattern: tls/text", "tone": "white", "h2": "Professional Standards",
             "paras": [PROFESSIONAL_STANDARDS]},
            {"type": "legal", "wf": "Pattern: tls/legal-outline", "tone": "soft", "h2": "Terms of use",
             "draft": LEGAL_REVIEW,
             "outline": [
                 ("Use of this website", "General information only; not legal, medical, or mental health advice."),
                 ("No professional relationship", "Contacting either practice or using this website does not by "
                                                  "itself create a client relationship."),
                 ("Eligibility & screening", "Services are subject to written and verbal screening; some matters "
                                             "cannot be accepted."),
                 ("Scheduling, fees & cancellations", "To be added when booking and payments launch."),
                 ("Intellectual property", "Website content, logos, and materials."),
                 ("Third-party links", "Referrals and external resources are provided for convenience."),
                 ("Limitation of liability", "Attorney to draft."),
                 ("Governing law", "Attorney to confirm."),
             ]},
        ],
    },
    {
        "slug": "contact", "label": "Contact", "schema_type": "ContactPage",
        "title": "Contact Our Maryland ADR Practice | LetTLSHelp",
        "description": "Private ADR, arbitration, mediation and conflict coaching. Call or text "
                       "+1 (240) 650-0007, or email the practice that fits your matter.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Contact", "h1": "Contact Us",
             "lede": "Private ADR, Arbitration, Mediation &amp; Conflict Coaching Practice. Serving eligible "
                     "clients with virtual and in‑person options during off‑peak hours."},
            {"type": "hub_contact", "wf": "Pattern: tls/hub-contact", "tone": "white",
             "h2": "Email the right practice",
             "intro": "Both addresses reach the same founder. Choosing the right one gets you a faster answer.",
             "items": PRACTICES},
            GENERAL_SCREENING,
        ],
    },
    {
        "slug": "privacy-policy", "label": "Privacy Policy",
        "title": "Privacy Policy | LetTLSHelp ADR Practices",
        "description": "How lettlshelp.com collects, uses, and protects information shared through this website, "
                       "including contact forms, screening responses, and analytics.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Policies", "h1": "Privacy policy",
             "lede": "How we collect, use, and protect your information, across both practices."},
            {"type": "legal", "wf": "Pattern: tls/legal-outline", "tone": "white", "h2": "Policy outline",
             "draft": LEGAL_REVIEW, "outline": PRIVACY_OUTLINE},
        ],
    },
]
