import io

import pytest

from src.clean import clean_text
from src.extract import extract_text
from src.validate import check_resume


def test_clean_preserves_tech_names():
    assert clean_text("Experienced in C++ and C#.") == "experienced in c++ and c#"
    assert clean_text("Built apps with .NET and Node.js") == "built apps with .net and node.js"


def test_clean_whitespace_and_punctuation():
    assert clean_text("  Lots   of\n\n spaces\tand tabs  ") == "lots of spaces and tabs"
    assert clean_text("Python, Java and SQL.") == "python java and sql"
    assert clean_text("") == ""


def test_extract_good_pdf():
    with open("sample_data/resume_strong.pdf", "rb") as f:
        assert extract_text(f).strip() != ""


def test_extract_scanned_pdf_raises():
    with open("sample_data/scanned.pdf", "rb") as f:
        with pytest.raises(ValueError):
            extract_text(f)


def test_extract_non_pdf_raises():
    with pytest.raises(ValueError):
        extract_text(io.BytesIO(b"this is not a pdf"))


def test_check_resume_rejects_keyword_stuffing():
    result = check_resume("machine learning python " * 50)
    assert result["looks_like_resume"] is False