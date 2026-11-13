from typing import BinaryIO

from pypdf import PdfReader
from pypdf.errors import PyPdfError


def extract_text(pdf_file: BinaryIO) -> str:
    """Extract all selectable text from a PDF file-like object.

    Raises:
        ValueError: if the file isn't a readable PDF, or if it contains
        no selectable text (empty or scanned).
    """
    try:
        reader = PdfReader(pdf_file)
        page_texts = []
        for page in reader.pages:
            # extract_text() can return None/"" for a blank page
            page_texts.append(page.extract_text() or "")
    except PyPdfError as e:
        raise ValueError(
            "Could not read this file. Please upload a valid, unencrypted PDF."
        ) from e

    text = "\n".join(page_texts)

    if not text.strip():
        raise ValueError(
            "No selectable text found. This PDF may be scanned or image-only. "
            "Please upload a text-based PDF."
        )

    return text