from src.match import load_skills, match_skills
from src.score import final_score, similarity


def test_java_does_not_match_javascript():
    skills = {"java": ["java"]}
    assert match_skills("i know javascript", skills) == set()
    assert match_skills("i know java", skills) == {"java"}


def test_cpp_is_matched():
    skills = {"c++": ["c++"]}
    assert match_skills("experienced in c++ and python", skills) == {"c++"}


def test_dotnet_is_matched():
    skills = {".net": [".net"]}
    assert match_skills("built apps with .net and node.js", skills) == {".net"}


def test_similarity_range_and_extremes():
    same = similarity("python sql docker", "python sql docker")
    different = similarity("python sql docker", "zebra giraffe lion")
    assert 0.0 <= different <= same <= 1.0
    assert same > 0.99
    assert different < 0.1


def test_final_score_contract():
    resume = "Skills: python and sql. Built projects using python."
    jd = "We need python and docker experience."
    result = final_score(resume, jd)

    assert set(result.keys()) == {
        "score", "similarity", "matched_skills", "missing_skills"
    }
    assert 0.0 <= result["score"] <= 100.0
    assert 0.0 <= result["similarity"] <= 1.0
    assert result["matched_skills"] == sorted(result["matched_skills"])
    assert result["missing_skills"] == sorted(result["missing_skills"])
    assert "python" in result["matched_skills"]
    assert "docker" in result["missing_skills"]