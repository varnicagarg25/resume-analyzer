import json
import sys

from src.clean import clean_text

path = sys.argv[1] if len(sys.argv) > 1 else "skills_tools_soft.json"

with open(path, encoding="utf-8") as f:
    skills = json.load(f)

problems = 0
seen = {}  # alias -> canonical skill

for canonical, aliases in skills.items():
    if not isinstance(aliases, list) or not aliases:
        print(f"PROBLEM: '{canonical}' needs a non-empty list of aliases")
        problems += 1
        continue
    if canonical not in aliases:
        print(f"PROBLEM: '{canonical}' is not in its own alias list")
        problems += 1
    for alias in aliases:
        if clean_text(alias) != alias:
            print(f"PROBLEM: alias '{alias}' (in '{canonical}') cleans to '{clean_text(alias)}'")
            problems += 1
        if alias in seen and seen[alias] != canonical:
            print(f"PROBLEM: alias '{alias}' is used by both '{seen[alias]}' and '{canonical}'")
            problems += 1
        seen[alias] = canonical

print(f"\n{len(skills)} skills, {len(seen)} aliases, {problems} problem(s)")