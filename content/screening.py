"""Online screening (intake) questions. Each site has its own script — keep them separate.

Transformative Life Solutions: 14 questions (family / interpersonal / workplace / coaching).
Transformative Leadership Systems: 18 questions (B2B, with consumer checks up front).
Wording comes from the owner's screening scripts.

Option keys:
    label     text shown in the dropdown
    note      guidance shown under the dropdown when chosen
    detail    label for the follow-up box revealed when chosen (omit = no box)
    required  the follow-up box must be filled in before submitting
    stop      choosing it ends the screening: we cannot assist

Ineligible answers exist because of Maryland Public Ethics Law §5-502 and the consumer-matter
exclusions in the 09/13/2026 guides. Don't soften them.
"""

STOP_TITLE = "Based on your answer, we cannot assist"
STOP_TEXT = ("We follow strict ethics rules, so we cannot take matters that involve consumer transactions, "
             "consumer-facing businesses, or the Maryland Office of the Attorney General. You are welcome to "
             "send the screening anyway; we will confirm and reply with referrals.")
STOP_REFERRALS = ["Another private ADR practitioner", "Community Mediation Maryland", "Better Business Bureau"]

ROLES = ["Select a role", "Contractor", "Contract worker", "Service provider", "Client", "Vendor", "Supplier",
         "Co-worker", "Supervisor", "Supervisee", "Partner", "Board member", "Family member", "Other"]

# ---------- questions worded identically in both scripts ----------

SAFETY = {
    "q": "Are there any safety concerns, including any history of threats, violence, harassment, or coercive "
         "control between the parties?",
    "options": [
        {"label": "No"},
        {"label": "Yes", "note": "We may be able to assist depending on the circumstances.",
         "detail": "Please share more", "required": True},
        {"label": "Unsure", "detail": "Tell us what you do know"},
    ],
}
COURT_ORDERS = {
    "q": "Are there any active court orders that prevent parties from interacting with one another?",
    "options": [
        {"label": "No"},
        {"label": "Yes", "note": "We may be able to assist depending on the circumstances.",
         "detail": "Be specific about any rulings and provide case numbers", "required": True},
        {"label": "Unsure", "detail": "Tell us what you do know"},
    ],
}
COURT_CASES = {
    "q": "Are there any active or closed court cases surrounding this matter?",
    "options": [
        {"label": "No"},
        {"label": "Yes", "note": "We may be able to assist depending on the circumstances.",
         "detail": "Be specific about any rulings and provide case numbers", "required": True},
        {"label": "Unsure", "detail": "Tell us what you do know"},
    ],
}
PROFESSIONALS = {
    "q": "Are any other professionals currently involved (therapists, attorneys, social workers, case managers, "
         "law enforcement, etc.) in this matter?",
    "options": [
        {"label": "No"},
        {"label": "Yes", "note": "We may be able to assist depending on the circumstances.",
         "detail": "Please share more", "required": True},
        {"label": "Unsure", "detail": "Tell us what you do know"},
    ],
}
CONSUMER_SELLER = {
    "q": "To confirm, regardless of the nature of your dispute or need for services through us, do you, any other "
         "party, or any person that will receive services through us sell goods or services directly to consumers "
         "as a contractor, automotive dealer, retailer, landlord, lender, lodging provider, practitioner, or other "
         "business?",
    "options": [
        {"label": "No"},
        {"label": "Yes", "stop": True},
        {"label": "Unsure", "detail": "Describe the business and what it sells", "required": True},
    ],
}
AG_COMPLAINT = {
    "q": "To confirm, regardless of the nature of your dispute or need for services through us, has any party "
         "involved, any person that will receive services through us, or any of their businesses filed — or do "
         "they plan to file — a complaint with the Maryland Attorney General or any of its divisions?",
    "options": [
        {"label": "No"},
        {"label": "Yes", "stop": True},
        {"label": "Unsure", "detail": "Tell us what you do know", "required": True},
    ],
}
AG_INVESTIGATED = {
    "q": "To confirm, regardless of the nature of your dispute or need for services through us, has anyone "
         "involved or their business been contacted by or investigated by the Maryland Attorney General or any of "
         "its divisions?",
    "options": [
        {"label": "No"},
        {"label": "Yes", "stop": True},
        {"label": "Unsure", "detail": "Tell us what you do know", "required": True},
    ],
}
EVENINGS = {
    "q": "Are all parties available to receive services in the evening, on weekends, or on holidays?",
    "options": [
        {"label": "Yes"},
        {"label": "Maybe", "detail": "Please share more", "required": True},
        {"label": "No", "note": "We may be able to assist depending on availability.",
         "detail": "Tell us when parties are available", "required": True},
    ],
}
PARTIES = {
    "type": "parties",
    "q": "Provide the name, email address, phone number, mailing address, and role of each party.",
    "help": "Roles include contractor, contract worker, service provider, client, vendor, supplier, co-worker, "
            "supervisor, supervisee, partner, and others. Include a party even if they have not agreed yet.",
}
INTERPRETATION = {
    "q": "Will a party or individual receiving services require interpretation and/or translation services?",
    "options": [
        {"label": "No"},
        {"label": "Yes", "detail": "List the languages needed", "required": True},
        {"label": "Unknown"},
    ],
}
ACCOMMODATIONS = {
    "q": "What type of accommodation needs are required for a party or individual receiving services?",
    "options": [
        {"label": "None"},
        {"label": "Unknown"},
        {"label": "Known", "detail": "Please list the accommodations needed", "required": True},
    ],
}

# ---------- Transformative Life Solutions: 14 questions ----------

LIFE_INTRO = [
    "Thank you for your willingness to complete our screening tool for Transformative Life Solutions. Once we have "
    "your responses, we can fully determine if it is appropriate to proceed and offer services.",
    "We thoroughly screen all potential clients before discussing services in detail. Please answer the following "
    "questions and, when appropriate, provide additional details.",
]

LIFE_QUESTIONS = [
    {
        "q": "Please identify the type of service(s) you are seeking.",
        "notes": [
            "<strong>Family &amp; Parenting Mediation:</strong> support for separation, parenting plans, "
            "co‑parenting communication, and family transitions.",
            "<strong>Interpersonal Mediation:</strong> facilitation for relationship, roommate, neighbor, and "
            "community conflicts. We do not handle landlord‑tenant, short‑term stay, long‑term stay, HOA, co‑op, "
            "or condominium matters.",
            "<strong>Workplace &amp; Organizational Facilitation:</strong> communication support for teams, "
            "supervisors, and staff navigating conflict or change. We serve non‑consumer‑facing companies and "
            "organizations only.",
            "<strong>Conflict Coaching:</strong> one‑on‑one support to strengthen communication, decision‑making, "
            "boundary setting, and conflict‑management skills.",
        ],
        "options": [
            {"label": "Family & Parenting Mediation"},
            {"label": "Interpersonal Mediation"},
            {"label": "Workplace & Organizational Facilitation"},
            {"label": "Conflict Coaching"},
            {"label": "More than one service", "detail": "Which services?", "required": True},
            {"label": "Not sure yet", "detail": "Briefly describe what you need"},
        ],
    },
    {
        "q": "Have all parties agreed to participate in mediation, or is there an order requiring it?",
        "options": [
            {"label": "Yes"},
            {"label": "No", "note": "All parties must agree. You can continue the screening with the understanding "
                                    "that additional details will be required for all parties.",
             "detail": "Tell us more (optional)"},
            {"label": "Unsure", "detail": "Tell us what you do know"},
        ],
    },
    EVENINGS,
    {
        "q": "We primarily offer remote services. Are all parties available for and open to participating in secure "
             "phone or video conferences?",
        "options": [
            {"label": "Yes"},
            {"label": "Maybe", "detail": "Please share more", "required": True},
            {"label": "No", "note": "We may be able to assist depending on availability.",
             "detail": "Provide details", "required": True},
        ],
    },
    SAFETY,
    COURT_ORDERS,
    COURT_CASES,
    PROFESSIONALS,
    CONSUMER_SELLER,
    AG_COMPLAINT,
    AG_INVESTIGATED,
    PARTIES,
    INTERPRETATION,
    ACCOMMODATIONS,
]

# ---------- Transformative Leadership Systems: 18 questions ----------

LEADERSHIP_INTRO = [
    "Thank you for your willingness to complete our online screening tool for Transformative Leadership Systems. "
    "Once we have your responses, we can fully determine if it is appropriate to proceed and offer services.",
    "We screen all potential clients before discussing services in detail. Please answer the following questions "
    "and, when appropriate, provide additional details.",
]

LEADERSHIP_QUESTIONS = [
    {
        "q": "Please identify the type of service(s) you are seeking.",
        "notes": [
            "<strong>Arbitration &amp; Med‑Arb (B2B only):</strong> neutral resolution processes for eligible "
            "organizations seeking binding, non‑binding, or hybrid dispute resolution.",
            "<strong>Business &amp; Organizational Mediation:</strong> support for internal workplace disputes, "
            "leadership conflicts, partnership disagreements, and organizational communication challenges.",
            "<strong>Negotiation Support:</strong> assistance for leaders navigating high‑stakes conversations, "
            "contract interpretation (non‑consumer), and inter‑organizational communication.",
            "<strong>Conflict Coaching:</strong> one‑on‑one support for executives, managers, team leads, and board "
            "members seeking to strengthen communication, decision‑making, and conflict‑management skills.",
        ],
        "options": [
            {"label": "Arbitration & Med-Arb (B2B only)"},
            {"label": "Business & Organizational Mediation"},
            {"label": "Negotiation Support"},
            {"label": "Conflict Coaching"},
            {"label": "More than one service", "detail": "Which services?", "required": True},
            {"label": "Not sure yet", "detail": "Briefly describe what you need"},
        ],
    },
    {
        "q": "Is any party a business that sells goods or services to consumers?",
        "options": [
            {"label": "No"},
            {"label": "Yes", "stop": True},
            {"label": "Unsure", "detail": "Describe the business and what it sells", "required": True},
        ],
    },
    {
        "q": "Does your dispute, or the issue for which you are seeking services, involve a consumer transaction?",
        "options": [
            {"label": "No"},
            {"label": "Yes", "stop": True},
            {"label": "Unsure", "detail": "Describe the transaction", "required": True},
        ],
    },
    {
        "q": "Has any party, individual seeking services, or their business filed a complaint with the Maryland "
             "Office of the Attorney General or any of its divisions?",
        "options": [
            {"label": "No"},
            {"label": "Yes", "stop": True},
            {"label": "Unsure", "detail": "Tell us what you do know", "required": True},
        ],
    },
    {
        "q": "Has any party, individual seeking services, or their business been contacted or investigated by the "
             "Maryland Office of the Attorney General?",
        "options": [
            {"label": "No"},
            {"label": "Yes", "stop": True},
            {"label": "Unsure", "detail": "Tell us what you do know", "required": True},
        ],
    },
    {
        "q": "Have all parties agreed to arbitration or mediation, or is there a contract requiring such services?",
        "options": [
            {"label": "Yes"},
            {"label": "No", "note": "All parties must agree. Please complete the remainder of the screening with the "
                                    "understanding that you will be required to provide contact details for all "
                                    "parties.",
             "detail": "Tell us more (optional)"},
            {"label": "Unsure", "detail": "Tell us what you do know"},
        ],
    },
    EVENINGS,
    {
        "q": "We primarily offer remote services. Are all parties available for and open to participating in phone "
             "or video conferences and hearings?",
        "options": [
            {"label": "Yes"},
            {"label": "Maybe", "detail": "Please share more", "required": True},
            {"label": "No", "note": "We may be able to assist with in-person services depending on availability.",
             "detail": "Please share more", "required": True},
        ],
    },
    SAFETY,
    COURT_ORDERS,
    COURT_CASES,
    PROFESSIONALS,
    CONSUMER_SELLER,
    AG_COMPLAINT,
    AG_INVESTIGATED,
    PARTIES,
    INTERPRETATION,
    ACCOMMODATIONS,
]
