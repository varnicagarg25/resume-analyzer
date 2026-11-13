import glob
import os

from src.clean import clean_text
from src.extract import extract_text
from src.validate import check_resume

pdfs = sorted(glob.glob("sample_data/*.pdf"))

if not pdfs:
    print("No PDFs found in sample_data/")

for path in pdfs:
    name = os.path.basename(path)
    print("=" * 60)
    print(name)

    try:
        with open(path, "rb") as f:
            raw = extract_text(f)
    except ValueError as e:
        print("  RESULT: ValueError ->", e)
        continue

    check = check_resume(raw)
    cleaned = clean_text(raw)

    print("  extracted characters:", len(raw))
    print("  word count:", check["word_count"])
    print("  sections found:", check["sections_found"])
    print("  looks like resume:", check["looks_like_resume"])

    # Did the special tech names survive cleaning?
    for term in ["c++", "c#", ".net", "node.js"]:
        if term in cleaned:
            print(f"  found '{term}' in cleaned text")

    print("  cleaned preview:", cleaned[:150])