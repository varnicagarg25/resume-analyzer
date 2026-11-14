import re

from src.clean import clean_text

# Each section counts once if ANY of its keywords appears as a whole word.
SECTIONS = {
    "education": ["education", "academic background", "qualifications"],
    "experience": ["experience", "employment", "work history", "internship"],
    "skills": ["skills", "technical skills", "core competencies"],
    "projects": ["projects", "project"],
    "summary": ["summary", "objective", "profile", "about me"],
    "certifications": ["certifications", "certificates", "achievements"],
}

MIN_SECTIONS = 2   # need at least this many different sections
MIN_WORDS = 100    # a real resume is rarely shorter than this


def check_resume(text: str) -> dict:
    """Rough check that text looks like a resume (not just keywords).

    Returns:
        {
            "looks_like_resume": bool,
            "sections_found": list[str],  # sorted
            "word_count": int,
        }
    """
    cleaned = clean_text(text)
    word_count = len(cleaned.split())

    found = []
    for section, keywords in SECTIONS.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", cleaned):
                found.append(section)
                break  # one hit is enough for this section

    return {
        "looks_like_resume": len(found) >= MIN_SECTIONS and word_count >= MIN_WORDS,
        "sections_found": sorted(found),
        "word_count": word_count,
    }