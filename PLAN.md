# AI-Powered Resume Analyzer & ATS Matcher — Project Plan

## What It Does
- **Input:** Resume (PDF) + Job Description (plain text)
- **Output:** Match score (0–100%), matched skills, and missing skills

## Pipeline
1. Extract text from uploaded PDF (`src/extract.py`)
2. Clean text (`src/clean.py`)
3. Match skills against `skills.json` (`src/match.py`)
4. Calculate TF-IDF + cosine similarity and combine into final score (`src/score.py`)
5. Display results in Streamlit (`app.py`)

## Function Signatures (The Contract)
*Do not change these signatures without telling the other person.*

### Part A: Varnica (Input & UI)
- `extract_text(pdf_file: BinaryIO) -> str` (in `src/extract.py`)
  - *Failure behavior:* Raises `ValueError` if the PDF is empty or scanned (no selectable text).
- `clean_text(text: str) -> str` (in `src/clean.py`)
  - *Rule:* Lowercase and normalize whitespace, but preserve `+`, `#`, and `.` inside tech names (`C++`, `C#`, `.NET`, `Node.js`).
- `app.py` (Streamlit UI: calls `extract_text`, passes raw text to `final_score`, and displays results).

### Part B: Ishika (Analysis & Scoring)
- `load_skills(path: str) -> dict[str, list[str]]` (in `src/match.py`)
  - *Format:* Maps canonical skill name to aliases, e.g. `{"machine learning": ["ml", "machine learning"]}`.
- `match_skills(text: str, skills: dict[str, list[str]]) -> set[str]` (in `src/match.py`)
  - *Rule:* Uses whole-word regex matching (`\b`) so `"java"` does not match `"javascript"`.
- `similarity(resume: str, jd: str) -> float` (in `src/score.py`)
  - *Output:* Float between `0.0` and `1.0`.
- `final_score(resume: str, jd: str) -> dict` (in `src/score.py`)
  - *Rule:* Calls `clean_text` internally on both inputs so `app.py` doesn't clean twice.
  - *Exact return keys:*
    ```python
    {
        "score": float,               # 0.0 to 100.0
        "similarity": float,          # 0.0 to 1.0
        "matched_skills": list[str],  # sorted list
        "missing_skills": list[str],  # sorted list (jd_skills - resume_skills)
    }
    ```

## Open Decisions (To Settle by Nov 18)
- Exact weighting formula for `score` (e.g., 50% TF-IDF cosine similarity + 50% skill overlap vs 40/60).
- Whether to use a small reference corpus of sample JDs/resumes so TF-IDF IDF weights are meaningful.

## Who Owns What
| File / Task | Owner | Status |
|---|---|---|
| `src/extract.py` | Varnica | Not started |
| `src/clean.py` | Varnica | Not started |
| `app.py` | Varnica | Not started |
| `sample_data/` (5–6 resumes & JDs) | Varnica | Not started |
| `skills.json` (Tools & Soft Skills) | Varnica | Not started |
| `skills.json` (Programming & Data/ML) | Ishika | Not started |
| `src/match.py` | Ishika | Not started |
| `src/score.py` | Ishika | Not started |
| `requirements.txt` & `README.md` | Both | In progress |
| `tests/` | Each tests the OTHER person's functions | Not started |

## Deadlines (Submission: Nov 27, 2026)
- **(Day 2):** Signatures & contract confirmed by both
- **(Day 6):** Own modules working in the terminal
- **(Day 8):** Pull requests reviewed and merged into `main`
- **(Day 10):** `app.py` wired up end-to-end
- **(Day 12):** Testing completed on 5+ resumes/JDs
- **(Day 15):** Final submission, slides & viva prep