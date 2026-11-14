from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.match import load_skills, match_skills

SKILLS_PATH = Path(__file__).resolve().parent.parent / "skills.json"
SIMILARITY_WEIGHT = 0.5


def clean_text(text: str) -> str:
    """Fallback text cleaner until Varnica's extract.py is merged."""
    return " ".join(text.lower().split())


def similarity(resume: str, jd: str) -> float:
    """Compute TF-IDF cosine similarity between resume and job description."""
    if not resume.strip() or not jd.strip():
        return 0.0

    # Allows leading dot (.net) and internal dots (node.js), but prevents trailing period (python.)
    vectorizer = TfidfVectorizer(token_pattern=r"(?u)\.?[\w+#]+(?:\.[\w+#]+)*")
    try:
        tfidf_matrix = vectorizer.fit_transform([resume, jd])
    except ValueError:
        # Handles inputs with no valid tokens like "---"
        return 0.0

    raw_score = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
    return max(0.0, min(1.0, raw_score))

def final_score(
    resume: str,
    jd: str,
    skills_path: Path | str = SKILLS_PATH,
) -> dict:
    """Calculate the final ATS match report comparing a resume against a job description."""
    cleaned_resume = clean_text(resume)
    cleaned_jd = clean_text(jd)

    skills = load_skills(str(skills_path))
    resume_skills = match_skills(cleaned_resume, skills)
    jd_skills = match_skills(cleaned_jd, skills)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)

    sim = similarity(cleaned_resume, cleaned_jd)

    if not jd_skills:
        total = 100.0 * sim
    else:
        overlap = len(matched) / len(jd_skills)
        total = 100.0 * (SIMILARITY_WEIGHT * sim + (1.0 - SIMILARITY_WEIGHT) * overlap)

    return {
        "score": round(total, 2),
        "similarity": round(sim, 4),
        "matched_skills": matched,
        "missing_skills": missing,
    }