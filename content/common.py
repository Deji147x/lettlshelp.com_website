"""Content shared by both sites (contact details, disclaimers, referrals, integration slots).

Contact details and disclaimer text come from the owner's brief and the 09/13/2026
website guides. Don't add claims, credentials, or statistics the owner hasn't supplied.
"""

FOUNDER = "Tanika L. Smith"
LINKEDIN = "https://www.linkedin.com/in/lettlshelp/"
# Each site sets its own contact address (see life.py / leadership.py); the owner's personal
# Gmail is no longer published on either site.
PHONE = "(240) 650-0007"
PHONE_INTL = "+1 (240) 650-0007"
PHONE_TEL = "+12406500007"
PHONE_SCHEMA = "+1-240-650-0007"

# Google Search Console token supplied by the owner (safe to publish; it is not a secret).
GSC_TOKEN = "nueZtT3ZZsV8SutwZKliXMbZEHgZePLeyCRynDhq78c"

# Owner's brief, confidentiality statement. Pending legal review against each site's guide wording.
RULE17 = (
    "Per Maryland Rule 17, all communication with this ADR practice is confidential. Our practitioners "
    "cannot be compelled to disclose any mediation or arbitration communication in any judicial, "
    "administrative, or other proceeding, and such communications are not subject to discovery."
)

CONSUMER_DISCLAIMER = (
    "We do not facilitate consumer matters or work with individuals or companies that sell products "
    "or services to consumers."
)
ETHICS_DISCLAIMER = (
    "We follow strict ethics rules to ensure neutrality, transparency, and compliance with Maryland "
    "Public Ethics Law §5‑502."
)

REFERRALS = [
    "Maryland's Consumer Protection Division",
    "Maryland Courts Self‑Help Center",
    "People's Law Library",
    "Community Mediation Maryland",
    "MPME‑rostered ADR practitioners",
    "Better Business Bureau",
    "Crisis Text Line",
]

INTAKE_SLOT = {
    "label": "Integration slot · Screening tool",
    "title": "Eligibility screening & intake",
    "text": "Reserved for a future screening tool. It is provider-agnostic: embed it with a block, shortcode, "
            "or iframe so the platform can change without redesigning the page.",
    "bullets": [
        "Multi-step questionnaire with conditional questions",
        "Secure (HTTPS) submission that collects only what screening needs",
        "Results or next-step recommendations, including free referrals when a matter isn't eligible",
        "Works with a WordPress form plugin or any third-party screening platform",
    ],
}

BOOKING_SETUP = {
    "label": "Setup · Google Calendar",
    "title": "How to switch this on",
    "text": "This section is already wired for Google Calendar appointment scheduling (Google "
            "Workspace). Nothing else on the page needs to change.",
    "bullets": [
        "In Google Calendar, create an appointment schedule for consultations and set availability, "
        "appointment length, and buffer time",
        "Open <strong>Share → Embed</strong> and copy the URL ending in <code>?gv=true</code>",
        "Paste it into <code>SITE[\"booking_url\"]</code> in content/life.py or content/leadership.py, "
        "then rebuild: the live calendar replaces the placeholder",
        "Google Calendar sends confirmations and handles rescheduling and cancellation; a WordPress "
        "booking plugin can replace it later without layout changes",
    ],
}

COMMERCE_SLOT = {
    "label": "Future · E-commerce (not active)",
    "title": "Digital products & service packages",
    "text": "Reserved for WooCommerce or a similar reputable platform when needed: online payments, digital "
            "products, services, customer accounts, and order management. Nothing is installed or active yet.",
}

CREDENTIALS_SLOT = {
    "label": "Owner to supply",
    "title": "Credentials & affiliations",
    "text": "Add verified certifications, trainings, roster listings, and memberships here. "
            "Nothing is filled in until the owner provides it.",
}

FOUNDER_PHOTO_SLOT = {
    "label": "Owner to supply",
    "title": "Founder portrait",
    "text": "A warm, natural, professional photo of Tanika L. Smith. Stock photography should never stand in "
            "for the founder.",
}

PRIVACY_OUTLINE = [
    ("Who we are", "Practice name, contact details, and which website this policy covers."),
    ("Information we collect", "Contact form details (name, email, phone, message), intake and screening "
                               "responses, and basic website analytics."),
    ("How we use information", "Responding to inquiries, screening eligibility, scheduling, and improving the "
                               "website. State whether personal information is ever sold or shared."),
    ("Confidentiality of ADR communications", "How mediation-related communications are protected, consistent "
                                              "with the Terms & Disclaimers page."),
    ("Cookies & analytics", "Google Analytics 4 and any consent choices offered to visitors."),
    ("Third-party services", "Google Workspace (email, calendar), form or screening providers, and future "
                             "booking or payment processors."),
    ("Data retention & security", "How long records, including screening documentation, are kept and how they "
                                  "are secured."),
    ("Your choices", "How to request access to, correction of, or deletion of your information."),
    ("Children's privacy", "Whether the website is directed to children under 13."),
    ("Changes & contact", "How updates are posted and how to contact the practice about privacy."),
]

TERMS_OUTLINE = [
    ("Use of this website", "General information only; not legal, medical, or mental health advice."),
    ("No professional relationship", "Contacting the practice or using this website does not by itself create a "
                                     "client relationship."),
    ("Eligibility & screening", "Services are subject to written and verbal screening; some matters cannot be "
                                "accepted."),
    ("Scheduling, fees & cancellations", "To be added when booking and payments launch."),
    ("Intellectual property", "Website content, logo, and materials."),
    ("Third-party links", "Referrals and external resources are provided for convenience."),
    ("Limitation of liability", "Attorney to draft."),
    ("Governing law", "Attorney to confirm."),
    ("Contact", "How to reach the practice about these terms."),
]

LEGAL_REVIEW = "Outline only. The final text must be drafted or reviewed by a licensed attorney before launch."
