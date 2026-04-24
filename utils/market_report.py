import os
import re
from collections import Counter
from datetime import datetime
from typing import Dict, List

import pandas as pd

COMMON_SKILLS = [
    "python", "sql", "excel", "power bi", "tableau", "machine learning",
    "data analysis", "project management", "risk management", "compliance",
    "audit", "finance", "accounting", "sales", "marketing", "aws", "azure",
    "cloud", "cybersecurity", "fraud", "aml", "kyc", "customer service",
    "communication", "leadership", "stakeholder management"
]


def generate_market_skill_report(resumes: List[Dict[str, str]], output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok=True)
    counter = Counter()

    for resume in resumes:
        text = (resume.get("text") or "").lower()
        for skill in COMMON_SKILLS:
            if re.search(rf"\b{re.escape(skill)}\b", text):
                counter[skill.title()] += 1

    df = pd.DataFrame(counter.most_common(), columns=["Skill", "Resume Count"])
    if df.empty:
        df = pd.DataFrame(columns=["Skill", "Resume Count"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(output_dir, f"market_skill_report_{timestamp}.xlsx")
    df.to_excel(path, index=False)
    return path
