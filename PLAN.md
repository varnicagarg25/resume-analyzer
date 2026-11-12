# AI-Powered Resume Analyzer & ATS Matcher — Project Plan

## What It Does
- **Input:** Resume (PDF) + Job Description (plain text)
- **Output:** Match score, matched skills, and missing skills

## Pipeline
1. Extract text from PDF (`src/extract.py`)
2. Clean text (`src/clean.py`)
3. Match skills against `skills.json` (`src/match.py`)
4. Calculate TF-IDF + cosine similarity and combine into final score (`src/score.py`)
5. Display results in Streamlit (`app.py`)

## Function Signatures (The Contract)
*Do not change these signatures without telling the other person.*

### Part A (VARNICA — Input & UI)
- `extract_text(pdf_path: str) -> str` (in `src/extract.py`)
- `clean_text(text: str) -> str` (in `src/clean.py`)
- `app.py` (Streamlit UI calling Part B's functions)

### Part B (ISHIKA — Analysis & Scoring)
- `load_skills(path: str) -> list[str]` (in `src/match.py`)
- `match_skills(text: str, skills: list[str]) -> set[str]` (in `src/match.py`)
- `similarity(resume: str, jd: str) -> float` (in `src/score.py`)
- `final_score(resume: str, jd: str) -> dict` (in `src/score.py`)

## Who Owns What
| File | Owner | Status |
|---|---|---|
| `src/extract.py` | Part A (Her) | Not started |
| `src/clean.py` | Part A (Her) | Not started |
| `app.py` | Part A (Her) | Not started |
| `skills.json` | Both | Not started |
| `src/match.py` | Part B (Me) | Not started |
| `src/score.py` | Part B (Me) | Not started |
| `tests/` | Each tests the OTHER person's functions | Not started |

## Deadlines
- **Day 2:** Signatures agreed
- **Day 6:** Own modules working in the terminal
- **Day 8:** Pull requests reviewed and merged
- **Day 10:** `app.py` wired up
- **Day 12:** Testing done
- **Day 15:** Submit