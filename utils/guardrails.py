import re

SKILL_TERMS = {
    "python", "java", "sql", "excel", "power bi", "tableau", "machine learning",
    "data analysis", "data analytics", "project management", "risk", "compliance",
    "finance", "accounting", "audit", "sales", "marketing", "cloud", "aws", "azure",
    "cybersecurity", "network", "communication", "leadership", "stakeholder",
    "operations", "customer service", "banking", "credit", "fraud", "aml", "kyc",
    "analytics", "skill", "skills", "skillset", "skillsets", "experience", "certification"
}

BLOCKED_PATTERNS = [
    r"tell me a joke", r"weather", r"stock price", r"politics", r"write a poem",
    r"who is", r"what is the capital", r"recipe", r"medical advice", r"legal advice"
]


def is_skillset_query(query: str) -> bool:
    """Allow employer prompts that are about job skillsets or candidate capabilities."""
    if not query or not query.strip():
        return False

    text = query.lower().strip()
    if any(re.search(pattern, text) for pattern in BLOCKED_PATTERNS):
        return False

    comma_or_list_like = len(re.split(r"[,;\n]", text)) >= 2
    contains_skill_term = any(term in text for term in SKILL_TERMS)
    short_role_like = bool(re.search(r"\b(manager|analyst|engineer|developer|specialist|officer|consultant)\b", text))

    return contains_skill_term or comma_or_list_like or short_role_like


def guardrail_response() -> str:
    return "The bot does not have the answer to your query. Please enter job skillsets only."
