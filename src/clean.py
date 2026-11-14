import re

# Anything that is NOT a letter/digit/underscore, whitespace, or one of + # .
# gets replaced with a space. \w also covers accented letters like é.
_UNWANTED = re.compile(r"[^\w\s+#.]")

# A token is only worth keeping if it has at least one letter or digit.
_HAS_ALNUM = re.compile(r"[^\W_]")


def clean_text(text: str) -> str:
    """Lowercase, normalize whitespace, strip punctuation noise, but keep
    + # . inside tech names such as c++, c#, .net and node.js."""
    text = text.lower()
    text = _UNWANTED.sub(" ", text)

    words = []
    for token in text.split():  # split() with no args also collapses all whitespace
        token = token.rstrip(".")  # sentence-ending periods: "python." -> "python"
        if _HAS_ALNUM.search(token):  # drops leftovers like "+", "#", "..."
            words.append(token)

    return " ".join(words)