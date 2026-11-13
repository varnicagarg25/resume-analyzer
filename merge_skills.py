import json

parts = ["skills_tools_soft.json", "skills_programming_data.json"]
merged = {}

for part in parts:
    with open(part, encoding="utf-8") as f:
        data = json.load(f)
    for canonical, aliases in data.items():
        if canonical in merged:
            print(f"Note: '{canonical}' appears twice, merging aliases")
            aliases = sorted(set(merged[canonical]) | set(aliases))
        merged[canonical] = aliases

with open("skills.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"Wrote skills.json with {len(merged)} skills")