import re
from typing import Dict, List

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def extract_matched_terms(query: str, resume_text: str) -> str:
    tokens = [t.strip().lower() for t in re.split(r"[,;\n]| and | with ", query) if t.strip()]
    resume_lower = resume_text.lower()
    matches = [token for token in tokens if token and token in resume_lower]
    return ", ".join(sorted(set(matches))) if matches else "Semantic match based on resume content"


def rank_candidates(skill_query: str, resumes: List[Dict[str, str]], top_k: int = 3) -> pd.DataFrame:
    """Rank candidates by semantic similarity to the employer skill query."""
    model = get_model()
    query_embedding = model.encode([skill_query])
    rows = []

    for resume in resumes:
        text = resume.get("text", "") or ""
        if not text.strip():
            score = 0.0
        else:
            resume_embedding = model.encode([text[:12000]])
            score = float(cosine_similarity(query_embedding, resume_embedding)[0][0])

        rows.append({
            "Candidate Resume": resume.get("file_name"),
            "Match Score": round(score, 4),
            "Matched Terms / Reason": extract_matched_terms(skill_query, text),
            "Resume Path": resume.get("path"),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values("Match Score", ascending=False).head(top_k).reset_index(drop=True)
