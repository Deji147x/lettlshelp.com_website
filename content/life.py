"""Transformative Life Solutions (TransformativeLifeSolutions.com): page content.

Sources: 'TLS_Website Development Guide_ 09132026.pdf' (current) and the owner's brief.
Copy that isn't in those sources carries a `draft` note so it gets owner/legal sign-off.
"""
from common import (COMMERCE_SLOT, CONSUMER_DISCLAIMER, CREDENTIALS_SLOT,
                    ETHICS_DISCLAIMER, FOUNDER_PHOTO_SLOT, GSC_TOKEN, LEGAL_REVIEW, PHONE,
                    PRIVACY_OUTLINE, REFERRALS, RULE17, TERMS_OUTLINE)
from screening import (LIFE_INTRO, LIFE_QUESTIONS, ROLES, STOP_REFERRALS, STOP_TEXT, STOP_TITLE)

# Owner's instruction (2026-09-16): every call to action on this site goes to this address.
EMAIL = "services@lettlshelp.com"

# Both practices share lettlshelp.com for now (owner's decision, 2026-09-16). Life Solutions sits
# at the root; Leadership Systems sits under /leadership-systems/. When the vanity domains go live,
# change "domain"/"base" here and 301-redirect the old paths.
SISTER_URL = "https://lettlshelp.com/leadership-systems/"

SITE = {
    "key": "life",
    "slug": "life-solutions",
    "name": "Transformative Life Solutions",
    "word_top": "Transformative",
    "word_bottom": "Life Solutions",
    "domain": "https://lettlshelp.com",
    "base": "",  # served at the domain root; future: TransformativeLifeSolutions.com
    "css": "life.css",
    "fonts": "https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Open+Sans:wght@400;600;700"
             "&family=Playfair+Display:ital@1&display=swap",
    "theme_color": "#006B7B",
    "og_bg": "#F4F7F8",
    "gsc": GSC_TOKEN,
    "ga4_id": None,  # e.g. "G-XXXXXXXXXX"; a Measurement ID, not an API key
    # Google Calendar appointment schedule embed URL (ends in ?gv=true). Set it and the booking
    # section on /contact/ shows the live calendar instead of the placeholder.
    "booking_url": None,
    "email": EMAIL,
    "footer_blurb": "A private ADR, mediation, and conflict coaching practice offering trauma-informed, "
                    "culturally grounded support for families, individuals, and non-consumer-facing workplaces.",
    "short_disclaimer": "Transformative Life Solutions provides mediation, coaching, and training services only. "
                        "We do not provide legal advice, legal representation, or legal advocacy, or medical or "
                        "mental health counseling services.",
    "keywords": ["mediation", "mediator", "divorce mediation", "separation agreement", "parenting plan",
                 "prenuptial agreement", "conflict coaching", "ADR", "alternative dispute resolution"],
    "nav": [("", "Home"), ("about", "About"), ("services", "Services"), ("how-it-works", "How It Works"),
            ("resources", "Resources"), ("faq", "FAQ"), ("contact", "Contact")],
    "nav_external": None,  # sister site is linked from the footer and cross-link bands, not the header
    "policies": [("ethics", "Ethics & Compliance"), ("privacy-policy", "Privacy Policy"),
                 ("terms-disclaimers", "Terms & Disclaimers")],
    "sister": ("Transformative Leadership Systems", SISTER_URL,
               "Business-to-business arbitration, mediation, and negotiation support"),
    "cta": ("contact", "Request a Consultation"),
    "topics": ["Family & Parenting Mediation", "Interpersonal Mediation", "Workplace & Organizational Facilitation",
               "Conflict Coaching", "Not sure yet"],
}

CONFIDENTIAL_GUIDE = ("In accordance with the Maryland Mediation and Confidentiality Act, all mediation-related "
                      "communication will remain confidential.")

FAQ = [
    {"q": "What services does Transformative Life Solutions offer?",
     "a": "Family and parenting mediation, interpersonal mediation, workplace and organizational facilitation "
          "for non-consumer-facing organizations, and one-on-one conflict coaching."},
    {"q": "Do you offer divorce mediation and help with parenting plans?",
     "a": "Yes. Family and parenting mediation supports separation, parenting plans, co-parenting communication, "
          "and family transitions."},
    {"q": "Can mediation help with a separation agreement or prenuptial agreement?",
     "a": "Mediation can help both people talk through the terms they want to reach. We do not provide legal "
          "advice or representation, so you may wish to have your own attorney review any agreement.",
     "draft": "Added for SEO keywords. Owner and legal to confirm this scope."},
    {"q": "Do you provide legal advice?",
     "a": "No. Transformative Life Solutions provides mediation services only. We do not provide legal advice, "
          "legal representation, or legal advocacy."},
    {"q": "Is this counseling or therapy?",
     "a": "No. We provide coaching and training services only. We do not provide medical or mental health "
          "counseling services."},
    {"q": "Is mediation confidential?",
     "a": CONFIDENTIAL_GUIDE,
     "draft": "Pending legal review. The guide and the brief cite different authorities; see Terms & Disclaimers."},
    {"q": "What matters do you not handle?",
     "a": "We do not handle consumer-business disputes (such as refunds, billing, purchases, warranties, or "
          "service agreements), auto sales or repair disputes, home improvement or contractor disputes, housing "
          "disputes, or any matter connected to Maryland consumer protection laws or the Office of the Attorney "
          "General."},
    {"q": "What happens if my matter isn't a fit?",
     "a": "We use written and verbal screening to determine eligibility. If we are unable to facilitate your "
          "matter, we will explain why and provide free supportive referrals."},
    {"q": "Do you meet virtually or in person?",
     "a": "Both. We serve clients with virtual and in-person options."},
    {"q": "Do you offer arbitration, negotiation support, or help with NDAs?",
     "a": f'Arbitration, med-arb, and negotiation support for eligible, non-consumer-facing organizations are '
          f'offered through our sister practice, <a href="{SISTER_URL}">Transformative Leadership Systems</a>.'},
    {"q": "How do I get started?",
     "a": f'Call or text <a href="tel:+12406500007">{PHONE}</a>, email <a href="mailto:{EMAIL}">{EMAIL}</a>, '
          f'or send a brief message through the contact page.'},
    # Added 2026-09-16: questions people commonly search for. Answers that need the owner's own
    # numbers or an attorney's wording carry a draft flag instead of invented detail.
    {"q": "How much does mediation cost?",
     "a": "Fees depend on the service and the time involved. We confirm pricing with you after screening, before "
          "any session is scheduled.",
     "draft": "Owner to supply fees: hourly or flat rate, consultation cost (if any), how fees are split between "
              "parties, deposits, and payment methods."},
    {"q": "How long does mediation take?",
     "a": "It depends on the number of issues and how prepared both people are. We give you an estimate after "
          "screening.",
     "draft": "Owner to supply typical session length and how many sessions a family or interpersonal matter "
              "usually takes."},
    {"q": "What happens in a first mediation session?",
     "a": "The mediator explains the process and ground rules, each person describes what matters most to them, "
          "and together you set an agenda for the issues to work through.",
     "draft": "General description of mediation practice. Owner to confirm it matches how she runs a first "
              "session, including session length and whether parties meet together or separately."},
    {"q": "Do both people have to agree to mediation?",
     "a": "Yes. All parties must agree to participate, unless an order requires it. If the other person has not "
          "agreed yet, you can still complete the screening and we will discuss next steps."},
    {"q": "Do I still need a lawyer if we mediate?",
     "a": "We provide mediation only and do not give legal advice or representation, so many people choose to get "
          "independent legal advice about their options and to review anything they sign. Whether you need a "
          "lawyer is your decision.",
     "draft": "Pending legal review: confirm this wording stays clear of giving legal advice."},
    {"q": "Is a mediated agreement legally binding?",
     "a": "Mediation helps you and the other person reach terms you both accept. Whether those terms become "
          "legally enforceable depends on how they are written, signed, and, in some matters, submitted to a "
          "court. Because we do not provide legal advice, you may wish to have your own attorney review any "
          "agreement.",
     "draft": "Pending legal review: confirm this wording and what the practice does or does not draft."},
    {"q": "What if there has been abuse, violence, or safety concerns?",
     "a": "Tell us during screening. We ask directly about threats, violence, harassment, and coercive control. "
          "Depending on the circumstances we may still be able to help, may suggest a different structure, or may "
          "refer you elsewhere. If you are in immediate danger, call 911.",
     "draft": "Owner to approve the safety wording, including whether to list a crisis line alongside 911."},
    {"q": "How does divorce or separation mediation work?",
     "a": "Instead of arguing positions through others, both people meet with a neutral mediator to talk through "
          "the decisions a separation requires, such as parenting time, communication, and next steps. You "
          "control the outcome; the mediator manages the conversation and keeps it balanced.",
     "draft": "Owner to confirm this describes her family mediation process."},
    {"q": "What is a parenting plan?",
     "a": "A parenting plan is a written arrangement covering how co-parents share time, make decisions, handle "
          "holidays and exchanges, and communicate with each other. Mediation gives both parents a structured "
          "way to build one together."},
]

NOT_HANDLED = [
    "Consumer‑business disputes (refunds, billing, purchases, warranties, service agreements, etc.)",
    "Auto sales or repair disputes",
    "Home improvement or contractor disputes",
    "Housing disputes",
    "Any matter involving a business regulated by or investigated under Maryland consumer protection laws",
    "Any case where a party has filed a complaint with, been contacted by, or been investigated by the Office "
    "of the Attorney General or any of its divisions",
    "Any matter that could reasonably appear connected to the work of the Consumer Protection Division of Maryland",
]

PILLARS = [
    {"icon": "heart", "title": "Trauma‑informed practice",
     "text": "A calm, predictable process that puts safety, choice, and respect first."},
    {"icon": "globe", "title": "Culturally competent care",
     "text": "Support that honors each person's background, identity, and lived experience."},
    {"icon": "shield", "title": "Ethics‑aligned service delivery",
     "text": "Strict neutrality, careful screening, and safeguards against conflicts of interest."},
]
PILLAR_DRAFT = "Pillar names are from the owner's guide; the one-line descriptions are draft copy for owner review."

STEPS = [
    {"title": "Reach out", "text": f"Call or text {PHONE}, send an email, or begin intake online."},
    {"title": "Eligibility screening",
     "text": "Written and verbal screening confirms your matter is one we can ethically facilitate."},
    {"title": "Confirm next steps",
     "text": "If it's a fit, we plan next steps together. If not, we explain why and share free supportive referrals."},
    {"title": "Meet virtually or in person", "text": "Choose the setting that feels right for you."},
]
STEPS_DRAFT = ("Steps are drawn from the guide's Screening Protocol and Contact sections. Owner to confirm the order "
               "and add details such as session length or fees.")

CTA = {"type": "cta", "wf": "Pattern: tls/cta-band", "h2": "Ready to talk it through?",
       "text": "Request a consultation. We'll confirm whether your matter is a good fit, and if it isn't, "
               "we'll point you toward free supportive referrals.",
       "primary": ("contact", "Request a Consultation")}

CROSSLINK = {"type": "crosslink", "wf": "Pattern: tls/sister-site-link", "tone": "white",
             "text": "Are you a business, nonprofit, or professional entity looking for <strong>arbitration</strong>, "
                     "<strong>negotiation support</strong>, or help with an <strong>NDA</strong> or other "
                     "business-to-business dispute?",
             "href": SISTER_URL, "label": "Visit Transformative Leadership Systems"}

PAGES = [
    {
        "slug": "", "label": "Home",
        "title": "Family Mediation & Coaching | Transformative Life Solutions",
        "description": "Trauma-informed family mediation, divorce mediation, parenting plans, and conflict coaching. "
                       "A private ADR practice with virtual and in-person options.",
        "sections": [
            {"type": "hero", "wf": "Pattern: tls/hero-split",
             "eyebrow": "Private ADR · Mediation · Conflict Coaching",
             "h1": "Family‑centered mediation and conflict coaching",
             "tagline": "Helping people move forward with clarity, dignity, and respect.",
             "lede": "Trauma‑informed, culturally grounded support for families, individuals, and workplaces, "
                     "with virtual and in‑person options.",
             "primary": ("contact", "Request a Consultation"), "secondary": ("services", "Explore Services"),
             "image": "hero-facilitated-conversation",
             "alt": "A mediator guides a calm conversation between two people seated in a bright room"},
            {"type": "text", "wf": "Pattern: tls/intro", "tone": "white", "center": True, "eyebrow": "Who we are",
             "h2": "What is Transformative Life Solutions?",
             "paras": ["We provide family‑centered, interpersonal, and workplace conflict resolution services. Our "
                       "approach is trauma‑informed, culturally grounded, and rooted in the belief that people can "
                       "resolve conflict when given the right structure and support.",
                       "We focus exclusively on private, non‑commercial, non‑consumer conflicts that support healthy "
                       "communication and sustainable agreements."]},
            {"type": "cards", "wf": "Pattern: tls/services-grid", "tone": "soft", "eyebrow": "Services",
             "h2": "How we can help",
             "items": [
                 {"icon": "home", "title": "Family & Parenting Mediation",
                  "text": "Divorce and separation mediation, parenting plans, co‑parenting communication, and family "
                          "transitions.",
                  "link": ("services#family", "About family mediation")},
                 {"icon": "message", "title": "Interpersonal Mediation",
                  "text": "Facilitation for relationship, roommate, neighbor, and community conflicts.",
                  "link": ("services#interpersonal", "About interpersonal mediation")},
                 {"icon": "briefcase", "title": "Workplace & Team Communication",
                  "text": "Support for teams, supervisors, and staff at non‑consumer‑facing organizations.",
                  "link": ("services#workplace", "About workplace facilitation")},
                 {"icon": "target", "title": "Conflict Coaching",
                  "text": "One‑on‑one support for communication, decision‑making, and boundary setting.",
                  "link": ("services#coaching", "About conflict coaching")},
             ],
             "link": ("services", "View all services")},
            {"type": "cards", "wf": "Pattern: tls/audience-grid", "tone": "white", "center": True,
             "eyebrow": "Who we serve", "h2": "Support for the people and relationships that matter",
             "items": [
                 {"icon": "heart", "title": "Spouses & partners",
                  "text": "Couples navigating separation or divorce and the decisions that follow."},
                 {"icon": "users", "title": "Parents & co‑parents",
                  "text": "Building parenting plans and healthier co‑parenting communication."},
                 {"icon": "home", "title": "Families in transition",
                  "text": "Families working through change together."},
                 {"icon": "message", "title": "Individuals & neighbors",
                  "text": "Relationship, roommate, and neighbor conflicts."},
                 {"icon": "globe", "title": "Community & civic groups",
                  "text": "Community conflicts that benefit from a neutral, structured conversation."},
                 {"icon": "briefcase", "title": "Workplace teams",
                  "text": "Teams, supervisors, and staff at non‑consumer‑facing organizations."},
             ]},
            {"type": "split", "wf": "Pattern: tls/media-text (pillars)", "tone": "soft",
             "eyebrow": "Why choose Transformative Life Solutions", "h2": "Built on three pillars",
             "paras": ["Every service is shaped by the same commitments, so you know what to expect from the first "
                       "conversation."],
             "bullets": [f"<strong>{p['title']}:</strong> {p['text'][0].lower() + p['text'][1:]}" for p in PILLARS],
             "draft": PILLAR_DRAFT,
             "image": "calm-conversation",
             "alt": "Two women share a relaxed conversation at a round table beside a city window",
             "link": ("about", "About our practice")},
            {"type": "steps", "wf": "Pattern: tls/process-steps", "tone": "white", "eyebrow": "How it works",
             "h2": "A simple, supportive process", "items": STEPS, "link": ("how-it-works", "See how it works")},
            {"type": "cards", "wf": "Pattern: tls/trust-grid", "tone": "mist", "center": True,
             "eyebrow": "Trust & credibility", "h2": "A practice built on ethics and care",
             "draft": "Confidentiality wording is pending legal review. Credentials appear only once the owner "
                      "supplies them.",
             "items": [
                 {"icon": "shield", "title": "Ethics‑aligned",
                  "text": "Operates in compliance with Maryland Public Ethics Law, with strict boundaries to avoid "
                          "conflicts of interest."},
                 {"icon": "clipboard", "title": "Careful screening",
                  "text": "Written and verbal screening confirms each matter is a good fit before we begin."},
                 {"icon": "check", "title": "Free referrals",
                  "text": "If we can't take your matter, we'll explain why and share free supportive referrals."},
                 {"icon": "lock", "title": "Confidential process",
                  "text": "Mediation‑related communication remains confidential."},
             ],
             "slot": CREDENTIALS_SLOT},
            {"type": "notlist", "wf": "Pattern: tls/scope-notice", "tone": "white", "h2": "What we don't handle",
             "intro": "To protect clients and maintain the integrity of state processes, we do not handle:",
             "bullets": ["Consumer‑business disputes (refunds, billing, purchases, warranties, service agreements)",
                         "Housing, auto sales or repair, home improvement, or contractor disputes",
                         "Any matter connected to Maryland consumer protection laws or the Office of the Attorney "
                         "General"],
             "link": ("ethics", "Read our ethics commitment")},
            {"type": "faq", "wf": "Pattern: tls/faq-preview (Details blocks)", "tone": "soft", "center": True,
             "eyebrow": "FAQ", "h2": "Common questions",
             "items": [FAQ[1], FAQ[11], FAQ[3]], "link": ("faq", "See all questions")},
            CROSSLINK,
            CTA,
        ],
    },
    {
        "slug": "about", "label": "About", "schema_type": "AboutPage",
        "title": "About Tanika L. Smith | Transformative Life Solutions",
        "description": "Founded by Tanika L. Smith, an ADR practitioner and communication strategist. Trauma-informed, "
                       "culturally competent, ethics-aligned mediation.",
        "sections": [
            {"type": "page_hero", "eyebrow": "About", "h1": "About Transformative Life Solutions",
             "lede": "A private ADR, mediation, and conflict coaching practice rooted in dignity, respect, and "
                     "ethical service."},
            {"type": "split", "wf": "Pattern: tls/founder", "tone": "white", "eyebrow": "Our founder",
             "h2": "Founded by Tanika L. Smith",
             "paras": ["Transformative Life Solutions was founded by Tanika L. Smith, a seasoned alternative dispute "
                       "resolution (ADR) practitioner and communication strategist."],
             "media_slot": FOUNDER_PHOTO_SLOT, "slot": CREDENTIALS_SLOT},
            {"type": "cards", "wf": "Pattern: tls/pillars", "tone": "soft", "center": True, "eyebrow": "Our approach",
             "h2": "Three pillars guide our work", "items": PILLARS, "draft": PILLAR_DRAFT},
            {"type": "text", "wf": "Pattern: tls/text", "tone": "white", "h2": "An ethics‑aligned separation",
             "paras": ["Transformative Life Solutions maintains a strict ethics‑aligned separation. All services are "
                       "structured to avoid conflicts of interest and to protect the integrity of state processes."],
             "link": ("ethics", "Ethics & Compliance")},
            {"type": "split", "wf": "Pattern: tls/media-text", "tone": "mist", "reverse": True,
             "h2": "Meeting people where they are",
             "paras": ["We serve clients with virtual and in‑person options, working with families, couples, "
                       "individuals, community groups, and non‑consumer‑facing workplaces."],
             "image": "elders-community",
             "alt": "Older women share a warm moment together at a community gathering",
             "draft": "Placeholder image. Replace with a photo that includes Black and brown elders, per the "
                      "imagery brief."},
            CTA,
        ],
    },
    {
        "slug": "services", "label": "Services",
        "title": "Divorce Mediation Services | Transformative Life Solutions",
        "description": "Family and divorce mediation, parenting plans, interpersonal mediation, workplace "
                       "facilitation, and conflict coaching. Virtual and in-person.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Services", "h1": "Mediation and conflict coaching services",
             "lede": "Family‑centered, interpersonal, and workplace conflict resolution: trauma‑informed, culturally "
                     "grounded, and focused on private, non‑consumer matters."},
            {"type": "split", "id": "family", "wf": "Pattern: tls/service-detail", "tone": "white",
             "eyebrow": "Family & Parenting Mediation", "h2": "Family and divorce mediation",
             "paras": ["Support for separation, parenting plans, co‑parenting communication, and family transitions."],
             "bullets": ["Separation and divorce mediation", "Parenting plans and co‑parenting communication",
                         "Talking through separation agreement and prenuptial agreement terms", "Family transitions"],
             "after": ["Mediation does not replace legal advice. You may wish to have your own attorney review any "
                       "agreement."],
             "draft": "Divorce, separation agreement, and prenuptial agreement wording was added for SEO keywords. "
                      "Owner and legal to confirm scope.",
             "image": "couple-reviewing-agreement",
             "alt": "A couple sits together at a table calmly reviewing paperwork"},
            {"type": "split", "id": "interpersonal", "wf": "Pattern: tls/service-detail", "tone": "soft",
             "reverse": True, "eyebrow": "Interpersonal Mediation", "h2": "Interpersonal mediation",
             "paras": ["Facilitation for relationship, roommate, neighbor, and community conflicts."],
             "bullets": ["Relationship conflicts", "Roommate and neighbor disagreements",
                         "Community and civic group conflicts"],
             "image": "supportive-talk", "alt": "Two women talk openly on a sofa in a quiet, sunlit space"},
            {"type": "split", "id": "workplace", "wf": "Pattern: tls/service-detail", "tone": "white",
             "eyebrow": "Workplace & Organizational Facilitation", "h2": "Workplace and team communication",
             "paras": ["Communication support for teams, supervisors, and staff navigating conflict or change."],
             "bullets": ["Team and staff conflict", "Supervisor and staff communication",
                         "Navigating organizational change"],
             "after": ["<strong>For non‑consumer‑facing companies and organizations only.</strong>"],
             "image": "young-adults-group",
             "alt": "A small team of young professionals talks around a table in a bright office"},
            {"type": "split", "id": "coaching", "wf": "Pattern: tls/service-detail", "tone": "soft", "reverse": True,
             "eyebrow": "Conflict Coaching", "h2": "One‑on‑one conflict coaching",
             "paras": ["One‑on‑one support to strengthen communication, decision‑making, boundary setting, and "
                       "conflict‑management skills."],
             "bullets": ["Communication", "Decision‑making", "Boundary setting", "Conflict‑management skills"],
             "image": "mediation-session", "alt": "A facilitator listens during a relaxed session in a bright room"},
            dict(CROSSLINK, text="Need <strong>arbitration</strong>, <strong>med‑arb</strong>, or "
                                 "<strong>negotiation support</strong> for a business or nonprofit?"),
            {"type": "notlist", "wf": "Pattern: tls/scope-notice", "tone": "mist", "h2": "What we do not handle",
             "intro": "Transformative Life Solutions does not mediate:", "bullets": NOT_HANDLED,
             "link": ("ethics", "Ethics & Compliance")},
            {"type": "slot", "tone": "white", **COMMERCE_SLOT},
            CTA,
        ],
    },
    {
        "slug": "how-it-works", "label": "How It Works",
        "title": "How Mediation Works | Transformative Life Solutions",
        "description": "What to expect: reach out, complete a brief eligibility screening, confirm next steps, and "
                       "meet virtually or in person. Free referrals if we can't help.",
        "sections": [
            {"type": "page_hero", "eyebrow": "How It Works",
             "h1": "How mediation with Transformative Life Solutions works",
             "lede": "A clear, supportive process, from your first message to your first session."},
            {"type": "steps", "wf": "Pattern: tls/process-steps", "tone": "white", "h2": "What to expect",
             "items": STEPS, "draft": STEPS_DRAFT},
            {"type": "text", "wf": "Pattern: tls/intake-cta", "tone": "soft", "eyebrow": "Step one",
             "h2": "Begin intake online",
             "paras": ["Our online screening asks about the services you need, availability, safety, and "
                       "eligibility. We review every response and reply with next steps or free referrals."],
             "link": ("begin-intake", "Start the screening")},
            {"type": "list", "wf": "Pattern: tls/referrals", "tone": "white",
             "h2": "If we can't help, we'll point you to support",
             "intro": "If we are unable to facilitate your matter, we will explain why and provide free supportive "
                      "referrals. Suggested referrals may include:",
             "items": REFERRALS, "draft": "Add verified website links for each referral."},
            {"type": "text", "wf": "Pattern: tls/text", "tone": "mist", "h2": "Before you begin",
             "bullets": ["We provide mediation services only. We do not provide legal advice, legal representation, "
                         "or legal advocacy.",
                         "We provide coaching and training services only. We do not provide medical or mental health "
                         "counseling services."],
             "link": ("terms-disclaimers", "Read all disclaimers")},
            CTA,
        ],
    },
    {
        "slug": "resources", "label": "Resources", "schema_type": "CollectionPage",
        "title": "Mediation Resources | Transformative Life Solutions",
        "description": "Articles and guides on divorce mediation, parenting plans, communication, conflict "
                       "coaching, and alternative dispute resolution.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Resources", "h1": "Mediation and conflict resolution resources",
             "lede": "Guides and articles on mediation, parenting plans, communication, and conflict coaching."},
            {"type": "posts", "wf": "Query Loop: Posts (blog index)", "tone": "white", "h2": "Latest articles",
             "cats": ["Divorce & Separation Mediation", "Parenting Plans", "Conflict Coaching",
                      "Communication Skills", "ADR Basics"],
             "draft": "Blog architecture only. Categories target the SEO keywords; post cards fill in automatically "
                      "from WordPress. No articles are published yet."},
            {"type": "list", "wf": "Pattern: tls/referrals", "tone": "soft", "h2": "Community resources",
             "intro": "Organizations that may be helpful:", "items": REFERRALS,
             "draft": "Add verified website links for each resource."},
            {"type": "slot", "tone": "white", **COMMERCE_SLOT},
            CTA,
        ],
    },
    {
        "slug": "faq", "label": "FAQ",
        "title": "Mediation FAQ | Transformative Life Solutions",
        "description": "Answers about divorce mediation, parenting plans, confidentiality, eligibility, legal "
                       "advice, and how to get started with Transformative Life Solutions.",
        "sections": [
            {"type": "page_hero", "eyebrow": "FAQ", "h1": "Frequently asked questions",
             "lede": "Clear answers about our services, process, and boundaries."},
            {"type": "faq", "wf": "Pattern: tls/faq (Details blocks + FAQPage schema)", "tone": "white",
             "items": FAQ, "schema": True},
            CTA,
        ],
    },
    {
        "slug": "contact", "label": "Contact", "schema_type": "ContactPage",
        "title": "Contact a Mediator | Transformative Life Solutions",
        "description": f"Request a consultation with Transformative Life Solutions. Call or text (240) 650-0007 or "
                       f"email {EMAIL}. Virtual and in-person options.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Contact", "h1": "Contact Transformative Life Solutions",
             "lede": "Private ADR, Mediation & Conflict Coaching Practice. Serving clients with virtual and "
                     "in‑person options."},
            {"type": "contact", "tone": "white"},
            {"type": "booking", "wf": "Block: Google Calendar appointment schedule (embed)", "tone": "soft",
             "eyebrow": "Scheduling", "h2": "Book a consultation",
             "intro": "Pick a time that works for you once online booking is live."},
        ],
    },
    {
        "slug": "begin-intake", "label": "Begin Intake",
        "title": "Begin Intake | Transformative Life Solutions",
        "description": "Complete our online screening: the services you need, availability, safety, court matters, "
                       "and eligibility. We reply with next steps or free referrals.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Screening", "h1": "Begin intake",
             "lede": "A short, private screening so we can confirm whether we are able to help."},
            {"type": "intake", "wf": "Pattern: tls/screening-form (14 questions)", "tone": "mist",
             "h2": "Screening questions",
             "intro": LIFE_INTRO, "questions": LIFE_QUESTIONS, "roles": ROLES,
             "stop_title": STOP_TITLE, "stop_text": STOP_TEXT, "stop_referrals": STOP_REFERRALS,
             "outro": "We look forward to receiving your responses and determining your eligibility.",
             "draft": "Screening wording supplied by the owner. Before launch, replace the email hand-off with a "
                      "secure WordPress form (encrypted storage and retention rules) and confirm what is kept."},
        ],
    },
    {
        "slug": "ethics", "label": "Ethics & Compliance",
        "title": "Ethics & Compliance | Transformative Life Solutions",
        "description": "How Transformative Life Solutions maintains neutrality and compliance with Maryland Public "
                       "Ethics Law, screens every matter, and provides free referrals.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Ethics & Compliance", "h1": "Our commitment to ethical practice",
             "lede": "Neutral, transparent, and structured to avoid conflicts of interest."},
            {"type": "text", "tone": "white", "h2": "Operating within Maryland Public Ethics Law",
             "paras": ["Transformative Life Solutions operates within full compliance of Maryland Public Ethics Law "
                       "and maintains strict boundaries to avoid conflicts of interest."]},
            {"type": "text", "tone": "soft", "h2": "What we focus on",
             "paras": ["Transformative Life Solutions does not provide services related to consumer‑business disputes "
                       "or any matter that falls under Maryland consumer protection laws or the authority of the "
                       "Office of the Attorney General.",
                       "We focus exclusively on private, non‑commercial conflicts such as family, interpersonal, "
                       "workplace (non‑consumer‑facing companies and organizations), and community matters."]},
            {"type": "notlist", "tone": "white", "h2": "What we do not handle",
             "intro": "Transformative Life Solutions does not mediate:", "bullets": NOT_HANDLED},
            {"type": "text", "tone": "mist", "h2": "Screening protocol",
             "paras": ["To determine client eligibility, Transformative Life Solutions uses written and verbal "
                       "screening processes and maintains documentation of them. If we are unable to facilitate "
                       "your matter, we will explain why and provide free supportive referrals."]},
            {"type": "list", "tone": "white", "h2": "Suggested referrals", "items": REFERRALS},
            CTA,
        ],
    },
    {
        "slug": "privacy-policy", "label": "Privacy Policy",
        "title": "Privacy Policy | Transformative Life Solutions",
        "description": "How Transformative Life Solutions collects, uses, and protects information shared through "
                       "this website, including contact forms, screening, and analytics.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Policies", "h1": "Privacy policy",
             "lede": "How we collect, use, and protect your information."},
            {"type": "legal", "tone": "white", "h2": "Policy outline", "draft": LEGAL_REVIEW,
             "outline": PRIVACY_OUTLINE},
        ],
    },
    {
        "slug": "terms-disclaimers", "label": "Terms & Disclaimers",
        "title": "Terms & Disclaimers | Transformative Life Solutions",
        "description": "Important disclaimers: no legal advice or representation, no medical or mental health "
                       "counseling, consumer-matter exclusions, ethics, and confidentiality.",
        "sections": [
            {"type": "page_hero", "eyebrow": "Policies", "h1": "Terms & disclaimers",
             "lede": "Please read these important disclaimers before working with us."},
            {"type": "disclaimers", "wf": "Pattern: tls/disclaimers", "tone": "white", "h2": "Important disclaimers",
             "items": ["Transformative Life Solutions provides mediation services only. We do not provide legal "
                       "advice, legal representation, or legal advocacy.",
                       "Transformative Life Solutions provides coaching and training services only. We do not provide "
                       "medical, mental health, or counseling services.",
                       CONSUMER_DISCLAIMER, ETHICS_DISCLAIMER],
             "options_h": "Confidentiality",
             "options": [
                 {"label": "Option A · Owner's guide (09/13/2026)",
                  "text": CONFIDENTIAL_GUIDE + " This mediation practitioner abides by the Maryland Standards of "
                                               "Conduct for Mediators."},
                 {"label": "Option B · Website brief", "text": RULE17},
             ],
             "draft": "Pending legal review: choose one confidentiality statement. The two options cite different "
                      "authorities, and Option B also covers arbitration."},
            {"type": "legal", "tone": "soft", "h2": "Terms of use", "draft": LEGAL_REVIEW, "outline": TERMS_OUTLINE},
        ],
    },
]
