"""Content shared by both sites (contact details, disclaimers, referrals, integration slots).

Contact details and disclaimer text come from the owner's brief and the 09/13/2026
website guides. Don't add claims, credentials, or statistics the owner hasn't supplied.
"""

FOUNDER = "Tanika L. Smith"
LINKEDIN = "https://www.linkedin.com/in/lettlshelp/"

# Owner's instruction (vision document, 2026-09-16): one address per practice, both on
# lettlshelp.com. These replace services@ and support@. The casing is the owner's; mail
# delivery ignores it, but it reads better in the header and footer.
EMAIL_LIFE = "LifeSolutions@LetTLSHelp.com"
EMAIL_LEADERSHIP = "LeadershipSystems@LetTLSHelp.com"
# The shared hub pages deliberately carry NO address of their own: they lead with the phone
# number and offer both practice addresses, so nobody has to guess which one to write to.

# Policy and compliance pages live once, at the domain root, and serve both practices.
# Every footer links to them through Ctx.root_href(), so the path is correct from any depth.
ROOT_POLICIES = [
    ("ethics", "Ethics & Compliance"),
    ("disclaimers", "Disclaimers"),
    ("privacy-policy", "Privacy Policy"),
]

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

# ---------------------------------------------------------------------------
# Founder background. Supplied by the owner in the vision document (2026-09-16),
# so this is real content, not a placeholder. Both practice sections render the
# same three groups from here so they can never drift apart.
# ---------------------------------------------------------------------------
FOUNDER_TRAININGS = [
    "40‑Hour Basic Mediation Training",
    "24‑Hour Child Access Mediation Training",
    "8‑Hour Re‑Entry Mediation Training",
    "Marital Separation Training",
    "36‑Hours Crisis Counseling",
]
FOUNDER_CREDENTIALS = [
    "Advanced‑Degree Communications Scholar",
]
FOUNDER_AFFILIATIONS = [
    "Member, Maryland Program for Mediator Excellence (MPME)",
    "Former Day of Trial Mediator, Maryland Judiciary’s Mediation and Conflict Resolution Office (MACRO)",
    "Rostered Arbitrator, Financial Industry Regulatory Authority (FINRA)",
    "Member, ADR Section, Maryland State Bar Association",
]

# The three groups above, as the About page renders them. The ids are the anchors the
# About dropdown deep-links to, so the submenu and the page stay in step automatically.
FOUNDER_GROUPS = [
    ("completed-trainings", "Completed Trainings Include", FOUNDER_TRAININGS),
    ("credentials", "Credentials", FOUNDER_CREDENTIALS),
    ("affiliations", "Affiliations Include", FOUNDER_AFFILIATIONS),
]

# ---------------------------------------------------------------------------
# Ethics & Compliance and Disclaimers now live once, at the root, for both
# practices. Every paragraph below is verbatim from the owner's vision document.
# ---------------------------------------------------------------------------
ETHICS_COMMITMENT = (
    "We operate in full compliance with Maryland Public Ethics Law §5‑502 and maintain strict "
    "boundaries to avoid conflicts of interest."
)
ETHICS_COMPLIANCE_SAFE = (
    "We do not provide services related to consumer‑business disputes or any matter that falls under "
    "Maryland consumer protection laws or the authority of the Office of the Attorney General."
)
ETHICS_SCOPE_LIFE = (
    "Through Transformative Life Solutions, we focus exclusively on private, non‑commercial conflicts "
    "such as family, interpersonal, workplace (non‑consumer‑facing companies and organizations), and "
    "community matters."
)
ETHICS_SCOPE_LEADERSHIP = (
    "Through Transformative Leadership Systems, we focus exclusively on private, non‑consumer‑facing "
    "organizational conflicts, including internal workplace disputes, leadership and partnership "
    "conflicts, board governance issues, and vendor–supplier disputes between non‑consumer‑facing entities."
)
ETHICS_SCREENING = (
    "We use written and verbal screening processes to determine client eligibility and maintain "
    "documentation of all screening decisions."
)
ETHICS_REFERRAL_INTRO = (
    "If we are unable to facilitate your matter, we will provide free supportive "
    "referrals. Suggested referrals may include:"
)

NOT_PROVIDED = [
    "Legal advice",
    "Legal representation",
    "Legal advocacy",
    "Medical or mental health counseling",
    "Clinical therapeutic services",
]
NOT_PROVIDED_INTRO = (
    "Through Transformative Life Solutions and Transformative Leadership Systems, we provide neutral "
    "ADR, conflict‑coaching, and organizational facilitation services only. We do not provide:"
)
CONFIDENTIALITY_ACT = (
    "In accordance with the Maryland Mediation and Confidentiality Act, all mediation‑related "
    "communication will remain confidential."
)
PROFESSIONAL_STANDARDS = (
    "Our practitioners abide by recognized professional standards for mediators, arbitrators, and "
    "conflict‑resolution professionals including the Maryland Standards of Conduct for Mediators and "
    "Maryland Uniform Arbitration Act (MUAA)."
)
CONFIDENTIALITY_REVIEW = (
    "Two wordings are on the table and an attorney must choose one. The vision document names the "
    "“Maryland Mediation and Confidentiality Act”; the earlier brief cites Maryland Rule 17 for the "
    "same point. See docs/consistency-review.md."
)

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
