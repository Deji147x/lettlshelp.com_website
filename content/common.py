"""Content shared by both sites (contact details, disclaimers, referrals, integration slots).

Contact details and disclaimer text come from the owner's brief and the 09/13/2026
website guides. Don't add claims, credentials, or statistics the owner hasn't supplied.
"""

FOUNDER = "Tanika L. Smith"

# Social profiles, as revised by the owner 2026-09-22. Both are the PRACTICE's pages, not a
# personal profile, so the schema lists them under the organization rather than the founder.
FACEBOOK = "https://www.facebook.com/LetTLSHelp/"
LINKEDIN = "https://www.linkedin.com/company/lettlshelp"
SOCIAL = [("Facebook", FACEBOOK), ("LinkedIn", LINKEDIN)]

# Owner's instruction (vision document, 2026-09-16): one address per practice, both on
# lettlshelp.com. These replace services@ and support@. The casing is the owner's; mail
# delivery ignores it, but it reads better in the header and footer.
EMAIL_LIFE = "LifeSolutions@LetTLSHelp.com"
EMAIL_LEADERSHIP = "LeadershipSystems@LetTLSHelp.com"
# Home-page and general enquiries go to EMAIL_LIFE (owner's instruction, 2026-09-22). The hub's
# footer and Contact page still show both, so anyone who knows which practice they need can
# write to it directly.

# Policy and compliance pages live once, at the domain root, and serve both practices.
# Every footer links to them through Ctx.root_href(), so the path is correct from any depth.
ROOT_POLICIES = [
    ("ethics", "Ethics & Compliance"),
    ("disclaimers", "Disclaimers"),
    ("privacy-policy", "Privacy Policy"),
    ("terms", "Terms of Use"),
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

# Free supportive referrals: name, what it helps with, and where to go. Descriptions and URLs
# supplied by the owner, 2026-09-22.
REFERRALS = [
    {"name": "Maryland's Consumer Protection Division",
     "text": "Get help with a consumer, health billing, or insurance complaint.",
     "url": "https://oag.maryland.gov"},
    {"name": "Maryland Courts Self‑Help Center",
     "text": "Learn how the court system can assist with your dispute through litigation, arbitration, "
             "and mediation.",
     "url": "https://www.mdcourts.gov/helpcenter"},
    {"name": "People's Law Library",
     "text": "Get free legal help and information for Maryland cases.",
     "url": "https://www.peoples-law.org/"},
    {"name": "Community Mediation Maryland",
     "text": "Obtain mediation services through centers across Maryland.",
     "url": "https://mdmediation.org/need-mediation/"},
    {"name": "MPME‑rostered ADR practitioners",
     "text": "Find a Maryland-based ADR practitioner who can assist.",
     "url": "https://www.mdcourts.gov/mpme/find"},
    {"name": "Better Business Bureau",
     "text": "Get help resolving a problem with a business through mediation and arbitration programs.",
     "url": "https://www.bbb.org"},
    {"name": "Crisis Text Line",
     "text": "Reach a crisis counselor by text, 24/7.",
     "url": "https://www.crisistextline.org/"},
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
    "If we are unable to facilitate your matter, we will provide free supportive referrals."
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
# The owner chose (2026-09-22) to publish BOTH confidentiality statements rather than pick one,
# each labelled with where it came from. An attorney still has to settle which is correct.
CONFIDENTIALITY_OPTIONS = [
    ("From the practice's website guide", CONFIDENTIALITY_ACT),
    ("From the practice's brief", RULE17),
]

CONFIDENTIALITY_REVIEW = (
    "Two wordings are on the table and an attorney must choose one. The vision document names the "
    "“Maryland Mediation and Confidentiality Act”; the earlier brief cites Maryland Rule 17 for the "
    "same point. See docs/consistency-review.md."
)

# ---------------------------------------------------------------------------
# Privacy Policy and Terms of Use.
#
# Drafted 2026-09-22 from what this website actually does, not from a template:
# the forms hand off to the visitor's own email app (mailto:), typefaces come
# from Google Fonts, the host keeps ordinary server logs, no analytics is
# switched on, and no cookies or browser storage are used on the live build.
#
# ATTORNEY REVIEW IS STILL REQUIRED. Anything that is a legal judgement rather
# than a description of the site carries a [square-bracket] marker, and the
# pages show a review flag in the review build.
#
# KEEP THIS HONEST: if the site changes, change the policy in the same commit.
# In particular, switching on GA4 (SITE["ga4_id"]) or Google Calendar booking
# (SITE["booking_url"]) makes the analytics and scheduling sections below wrong.
# ---------------------------------------------------------------------------
POLICY_UPDATED = "22 September 2026"
ATTORNEY_REVIEW = (
    "Draft for attorney review. It describes how the website actually works; the items in "
    "[square brackets] need the owner's or an attorney's decision before launch."
)

PRIVACY_POLICY = [
    {"h": "Who this policy covers",
     "p": ["This policy covers lettlshelp.com and both practices on it: Transformative Life Solutions "
           "and Transformative Leadership Systems. Both are operated by Tanika L. Smith.",
           "You can reach us by phone or text on (240) 650‑0007, or by email at "
           "LifeSolutions@LetTLSHelp.com or LeadershipSystems@LetTLSHelp.com."]},
    {"h": "The short version",
     "p": ["This website does not run forms on its own server, set cookies, or store anything on your "
           "device. It does not track you, and we do not sell or rent your information.",
           "What we do hold is what you choose to send us by email, text, or phone, plus the ordinary "
           "server records our web host keeps."]},
    {"h": "When you use a form on this site",
     "p": ["The contact and screening forms do not submit to us over the web. When you press Send or "
           "Submit, the form opens your own email app with your answers already written into a message "
           "addressed to us. <strong>Nothing is sent until you press send in your email app.</strong>",
           "This means your answers travel as an ordinary email, through your email provider and ours. "
           "Email is not encrypted end to end. If a matter is sensitive, call or text instead.",
           "So that a long message is not lost if your email app shortens it, the form also copies your "
           "answers to your device's clipboard. They stay there until you copy something else. We never "
           "see your clipboard.",
           "Because the message is created inside your own email app, this website never receives or "
           "stores what you typed."]},
    {"h": "What we ask for, and what not to send",
     "p": ["The forms ask for your name, email address, phone number, how you prefer to be contacted, "
           "and short answers about the kind of matter you have, so we can tell whether we are allowed "
           "to help.",
           "Please do not send confidential details about your dispute before we confirm eligibility. "
           "The forms say so at the point where it matters."]},
    {"h": "Information collected automatically",
     "p": ["Our web host keeps standard server logs: the IP address you connect from, your browser and "
           "device type, which pages you requested, and when. These are used to keep the site running "
           "and secure, and we do not use them to build a profile of you.",
           "[Owner to confirm the host and how long it keeps logs.]"]},
    {"h": "Typefaces served by Google",
     "p": ["The site's typefaces load from Google Fonts. To deliver them, Google receives your IP "
           "address and basic browser information. Google does not set cookies for this, and we send "
           "Google nothing else about you.",
           "[Recommended: self-host the typefaces when the site moves to WordPress. The fonts then come "
           "from our own server and this section can be removed.]"]},
    {"h": "Cookies, analytics, and tracking",
     "p": ["This site sets no cookies, uses no browser storage, and has no analytics, advertising, or "
           "social media tracking installed. That is why you are not asked to accept cookies.",
           "If we add analytics later, we will update this policy and say plainly what is collected "
           "before it goes live."]},
    {"h": "Booking appointments",
     "p": ["Online booking is not switched on yet. When it is, appointments will be scheduled through "
           "Google Calendar, and the name, email address, and time you enter will be processed by "
           "Google in order to make and confirm the booking."]},
    {"h": "Screening records",
     "p": ["We keep a record of screening decisions, including matters we cannot accept and the reason, "
           "because our ethics obligations require us to document them.",
           "[Owner and attorney to confirm how long screening records are kept and how they are stored.]"]},
    {"h": "Who else sees your information",
     "p": ["Your email reaches our email provider, and our website is served by our web host. We do not "
           "share your information with anyone else except where the law requires it.",
           "We do not sell, rent, or trade personal information, and we never have."]},
    {"h": "Your choices",
     "p": ["You can ask us what information we hold about you, ask us to correct it, or ask us to delete "
           "it. Email or call us and we will respond.",
           "We may need to keep screening records even after a request to delete, where our ethics "
           "obligations require it. [Attorney to confirm which privacy laws apply to this practice and "
           "what rights they give.]"]},
    {"h": "Children",
     "p": ["This website is meant for adults and is not directed to children under 13. We do not "
           "knowingly collect information from children."]},
    {"h": "Changes to this policy",
     "p": ["If we change how the site handles information, we will update this page and change the date "
           "at the top. Significant changes will be described here rather than made quietly."]},
]

TERMS_OF_USE = [
    {"h": "About these terms",
     "p": ["These terms apply to lettlshelp.com and to both practices on it. By using the site, you "
           "agree to them. If you do not agree, please do not use the site."]},
    {"h": "What this website is",
     "p": ["The site describes our alternative dispute resolution services and helps you find out "
           "whether we can help. It is general information only.",
           "Nothing here is legal advice, and nothing here is medical or mental health advice. Do not "
           "act or delay acting on something you read here without getting proper advice for your "
           "own situation."]},
    {"h": "Using the site does not make you a client",
     "p": ["Reading these pages, sending a form, or emailing or calling us does not by itself create a "
           "client relationship. A relationship begins only when we have screened your matter, both "
           "sides have agreed to work together, and any agreement we ask for is in place."]},
    {"h": "Eligibility and screening",
     "p": ["Every matter is screened before we accept it, in writing and by conversation. We cannot "
           "accept matters that fall outside what our ethics rules allow, including consumer matters "
           "and matters involving consumer‑facing businesses.",
           "If we cannot help, we will provide free supportive referrals. Those referrals are "
           "suggestions, not a recommendation of any particular organization or an endorsement of the "
           "advice they may give."]},
    {"h": "What we do not provide",
     "p": ["We provide neutral ADR, conflict‑coaching, and organizational facilitation services only. "
           "We do not provide legal advice, legal representation, or legal advocacy, and we do not "
           "provide medical or mental health counseling or clinical therapeutic services.",
           "You may wish to have your own attorney review any agreement reached in mediation."]},
    {"h": "Confidentiality",
     "p": ["Mediation‑related communication is treated as confidential. The Disclaimers page sets out "
           "the standards we work to."]},
    {"h": "Messages you send us",
     "p": ["Messages sent from this site go through your own email app, so they travel as ordinary "
           "email and are not encrypted end to end. Please do not send confidential details about a "
           "dispute before we confirm we can help. If a matter is sensitive, call or text us.",
           "We cannot guarantee that an email reaches us, so if you do not hear back, please phone."]},
    {"h": "Fees, scheduling, and cancellations",
     "p": ["Services are provided for a fee. Cancellation charges may apply. Please read your "
           "agreements and contracts carefully."]},
    {"h": "Our content",
     "p": ["The text, logos, and design of this site belong to us and may not be copied or reused "
           "commercially without permission. You are welcome to print or share pages for your own "
           "personal use."]},
    {"h": "Links to other sites",
     "p": ["Where we link to another organization, such as a referral, we do so for convenience. We do "
           "not control those sites and are not responsible for their content, accuracy, or privacy "
           "practices."]},
    {"h": "Availability",
     "p": ["We try to keep the site accurate and available, but we cannot promise it will always be up "
           "to date or free of interruptions or errors."]},
    # "Limitation of liability" and "Governing law" were removed at the owner's request
    # (2026-09-22) rather than published as attorney-to-draft placeholders. Both are standard
    # in website terms; add them back once an attorney has drafted the wording.
    {"h": "Changes and contact",
     "p": ["We may update these terms. The date at the top of the page shows when they last changed. "
           "Questions about these terms can go to either practice address or to our phone number."]},
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
