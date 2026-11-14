# resume-analyzer

## Setup
1. Create and activate a virtual environment.
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Input modules (Varnica)
- `src/extract.py`: `extract_text(pdf_file)` reads text from a PDF with pypdf. Raises `ValueError` for scanned, empty or invalid PDFs.
- `src/clean.py`: `clean_text(text)` lowercases, normalizes whitespace, removes punctuation noise, and preserves `+`, `#` and `.` in names like C++, C#, .NET and Node.js.
- `src/validate.py`: `check_resume(text)` checks for at least 2 standard resume sections and 100 words. If it fails, the app warns that the score may be unreliable.
- `app.py`: Streamlit UI for upload, job description input and results.

## Known limitations
- Scanned PDFs are rejected (no OCR).
- The resume check can be fooled by keyword stuffing under fake headings.
- Hyphens and slashes become spaces, so skill aliases are written in cleaned form.