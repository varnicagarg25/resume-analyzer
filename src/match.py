import json
import re


def load_skills(path: str) -> dict[str, list[str]]:
    """Load canonical skills and lowercase aliases from a JSON file.

    Raises:
        FileNotFoundError: If the skills JSON file does not exist at `path`.
        ValueError: If the JSON root is not a dict, invalid JSON, or any value is not a list of strings.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Skills file not found at: {path}") from exc

    if not isinstance(data, dict):
        raise ValueError("Skills JSON must be an object mapping skill names to alias lists.")

    cleaned_skills: dict[str, list[str]] = {}
    for name, aliases in data.items():
        if not isinstance(aliases, list) or not all(isinstance(a, str) for a in aliases):
            raise ValueError(f"Aliases for skill '{name}' must be a list of strings.")
        cleaned_skills[name.strip().lower()] = [a.strip().lower() for a in aliases if a.strip()]

    return cleaned_skills


def match_skills(text: str, skills: dict[str, list[str]]) -> set[str]:
    """Return the set of canonical skills found in text."""
    found: set[str] = set()
    text_lower = text.lower()

    for canonical, aliases in skills.items():
        for alias in aliases:
            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
            if re.search(pattern, text_lower):
                found.add(canonical)
                break

    return found