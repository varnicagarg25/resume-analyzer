from src.match import load_skills, match_skills
from src.score import final_score


def test_match_skills_handles_special_chars():
    skills = load_skills("skills.json")
    found = match_skills("experienced in c++ c# and .net", skills)
    assert found == [".net", "c#", "c++"]


def test_match_skills_word_boundaries():
    skills = load_skills("skills.json")
    assert match_skills("java script developer", skills) == []
    assert match_skills("java and javascript developer", skills) == ["java", "javascript"]


def test_final_score_strong_vs_weak_tech():
    jd = "Looking for a Python, SQL, and Docker engineer with REST API experience."
    strong_resume = "Skills: Python, SQL, Docker, REST APIs, Git."
    weak_resume = "Experienced retail store manager with customer service background."

    strong = final_score(strong_resume, jd)
    weak = final_score(weak_resume, jd)

    assert strong["score"] > weak["score"]
    assert "python" in strong["matched_skills"]
    assert "docker" in strong["matched_skills"]
    assert strong["missing_skills"] == []


def test_final_score_no_jd_skills_fallback():
    res = final_score("Experienced teacher and counselor", "Seeking a special needs counselor")
    assert res["matched_skills"] == []
    assert res["missing_skills"] == []
    assert 0.0 <= res["score"] <= 100.0