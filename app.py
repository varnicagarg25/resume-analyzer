import io
from pathlib import Path
import streamlit as st

import src.score as score_mod
from src.extract import extract_text
from src.validate import check_resume

SKILL_WEIGHT = getattr(score_mod, "SKILL_WEIGHT", 0.6)
SIMILARITY_WEIGHT = getattr(
    score_mod, "SIMILARITY_WEIGHT", round(1.0 - SKILL_WEIGHT, 2)
)

SAMPLES = {
    "Strong Tech Match": (
        Path("sample_data/resume_strong.pdf"),
        Path("sample_data/jd_strong.txt"),
    ),
    "C++ / .NET Match": (
        Path("sample_data/resume_cpp_dotnet.pdf"),
        Path("sample_data/jd_cpp.txt"),
    ),
    "Weak / Unrelated Resume": (
        Path("sample_data/resume_weak.pdf"),
        Path("sample_data/jd_strong.txt"),
    ),
}


def inject_styles():
    st.markdown(
        """
        <style>
        .hero-banner {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 55%, #EC4899 100%);
            padding: 1.6rem 2rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 1.25rem;
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.22);
        }
        .hero-banner h1 {
            margin: 0 0 0.35rem 0;
            font-size: 1.9rem;
            color: white;
        }
        .hero-banner p {
            margin: 0;
            opacity: 0.92;
            font-size: 1rem;
        }
        .metric-card {
            background: #FFFFFF;
            border: 1px solid #DCE3F5;
            border-top: 4px solid #4F46E5;
            border-radius: 14px;
            padding: 1.1rem 1.25rem;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
            height: 100%;
        }
        .metric-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #1E293B;
            margin: 0.2rem 0;
        }
        .badge-strong {
            background: #DCFCE7; color: #166534;
            padding: 0.2rem 0.65rem; border-radius: 999px; font-weight: 700; font-size: 0.82rem;
        }
        .badge-moderate {
            background: #FEF3C7; color: #92400E;
            padding: 0.2rem 0.65rem; border-radius: 999px; font-weight: 700; font-size: 0.82rem;
        }
        .badge-low {
            background: #FEE2E2; color: #991B1B;
            padding: 0.2rem 0.65rem; border-radius: 999px; font-weight: 700; font-size: 0.82rem;
        }
        .pill-green {
            display: inline-block;
            background: #DCFCE7;
            color: #166534;
            border: 1px solid #86EFAC;
            padding: 0.28rem 0.72rem;
            margin: 0.22rem;
            border-radius: 999px;
            font-size: 0.86rem;
            font-weight: 600;
        }
        .pill-red {
            display: inline-block;
            background: #FEE2E2;
            color: #991B1B;
            border: 1px solid #FCA5A5;
            padding: 0.28rem 0.72rem;
            margin: 0.22rem;
            border-radius: 999px;
            font-size: 0.86rem;
            font-weight: 600;
        }
        .pill-section {
            display: inline-block;
            background: #EEF2FF;
            color: #3730A3;
            border: 1px solid #C7D2FE;
            padding: 0.22rem 0.65rem;
            margin: 0.2rem;
            border-radius: 8px;
            font-size: 0.84rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown("## How It Works")
        st.markdown(
            """
            1. **Extract** text from your PDF (`pypdf`)
            2. **Validate** resume structure & length
            3. **Clean & Normalize** text tokens
            4. **Match Skills** with word-boundary rules
            5. **Score Fit** via hybrid NLP formula
            """
        )
        st.divider()
        st.info(
            "**Classical NLP Engine:** Uses deterministic keyword matching + "
            "TF-IDF cosine similarity (no external LLM API)."
        )
        st.caption("Privacy: Resumes are processed in memory and never stored.")


def render_header():
    st.markdown(
        """
        <div class="hero-banner">
            <h1>AI-Powered Resume & Job Description Matcher</h1>
            <p>Check ATS skill coverage, TF-IDF semantic alignment, and missing keywords in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_sample(sample_name: str):
    pdf_path, jd_path = SAMPLES[sample_name]
    if pdf_path.exists() and jd_path.exists():
        st.session_state["sample_pdf_bytes"] = pdf_path.read_bytes()
        st.session_state["sample_pdf_name"] = pdf_path.name
        st.session_state["jd_input"] = jd_path.read_text(encoding="utf-8")
        st.session_state.pop("analysis_result", None)
    else:
        st.warning(f"Sample files for '{sample_name}' were not found in sample_data/.")


def render_inputs():
    st.markdown("#### Try a One-Click Sample Demo")
    btn_cols = st.columns(len(SAMPLES))
    for col, label in zip(btn_cols, SAMPLES.keys()):
        if col.button(f"Load: {label}", use_container_width=True):
            load_sample(label)

    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.subheader("1. Upload Resume (PDF)")
        uploaded = st.file_uploader(
            "Choose a PDF resume",
            type=["pdf"],
            label_visibility="collapsed",
        )
        if uploaded is not None:
            st.session_state.pop("sample_pdf_bytes", None)
            st.session_state.pop("sample_pdf_name", None)
        elif "sample_pdf_name" in st.session_state:
            st.success(f"Loaded sample resume: **{st.session_state['sample_pdf_name']}**")

    with right_col:
        st.subheader("2. Paste Job Description")
        jd_text = st.text_area(
            "Paste target job description",
            key="jd_input",
            height=185,
            placeholder="Paste the full job description here (requirements, tech stack, responsibilities)...",
            label_visibility="collapsed",
        )

    analyze_clicked = st.button(
        "Analyze Resume Match", type="primary", use_container_width=True
    )
    return uploaded, jd_text, analyze_clicked


def run_analysis(uploaded, jd_text: str):
    if uploaded is not None:
        pdf_source = uploaded
        file_label = uploaded.name
    elif "sample_pdf_bytes" in st.session_state:
        pdf_source = io.BytesIO(st.session_state["sample_pdf_bytes"])
        file_label = st.session_state["sample_pdf_name"]
    else:
        st.warning("Please upload a PDF resume or click one of the sample buttons above.")
        return

    if not jd_text or not jd_text.strip():
        st.warning("Please paste a job description before running the analysis.")
        return

    with st.spinner("Extracting text, matching skills, and computing similarity..."):
        try:
            resume_text = extract_text(pdf_source)
        except ValueError as err:
            st.error(str(err))
            return

        validation = check_resume(resume_text)
        scores = score_mod.final_score(resume_text, jd_text)

    st.session_state["analysis_result"] = {
        "file_label": file_label,
        "resume_text": resume_text,
        "validation": validation,
        "scores": scores,
    }


def score_band(score: float):
    if score >= 75:
        return "Strong Match", "badge-strong"
    if score >= 45:
        return "Moderate Match", "badge-moderate"
    return "Low Match", "badge-low"


def build_report_text(data: dict) -> str:
    scores = data["scores"]
    matched = ", ".join(scores["matched_skills"]) or "None"
    missing = ", ".join(scores["missing_skills"]) or "None"
    return (
        f"RESUME MATCH REPORT\n"
        f"===================\n"
        f"Resume File: {data['file_label']}\n"
        f"Overall Score: {scores['score']:.1f} / 100\n"
        f"TF-IDF Similarity: {scores['similarity']:.2f}\n"
        f"Matched Skills ({len(scores['matched_skills'])}): {matched}\n"
        f"Missing Skills ({len(scores['missing_skills'])}): {missing}\n"
    )


def render_results():
    data = st.session_state.get("analysis_result")
    if not data:
        return

    st.divider()
    validation = data["validation"]
    scores = data["scores"]

    if not validation["looks_like_resume"]:
        st.warning(
            f"This file only had {validation['word_count']} words and few standard resume "
            "headings—the match score below may be less reliable."
        )

    score_val = float(scores["score"])
    sim_val = float(scores["similarity"])
    matched = scores["matched_skills"]
    missing = scores["missing_skills"]
    total_jd_skills = len(matched) + len(missing)
    skill_pct = (len(matched) / total_jd_skills * 100) if total_jd_skills > 0 else None
    band_label, band_class = score_band(score_val)

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Overall Match Score</div>
                <div class="metric-value">{score_val:.1f}%</div>
                <span class="{band_class}">{band_label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        skill_display = f"{skill_pct:.0f}%" if skill_pct is not None else "N/A"
        skill_sub = (
            f"{len(matched)} of {total_jd_skills} JD skills matched"
            if total_jd_skills > 0
            else "No tracked skills in JD"
        )
        st.markdown(
            f"""
            <div class="metric-card" style="border-top-color: #10B981;">
                <div class="metric-label">Skill Coverage ({int(SKILL_WEIGHT * 100)}% Weight)</div>
                <div class="metric-value">{skill_display}</div>
                <span style="color:#475569; font-size:0.86rem;">{skill_sub}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-top-color: #EC4899;">
                <div class="metric-label">TF-IDF Similarity ({int(SIMILARITY_WEIGHT * 100)}% Weight)</div>
                <div class="metric-value">{sim_val * 100:.1f}%</div>
                <span style="color:#475569; font-size:0.86rem;">Cosine similarity: {sim_val:.2f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.progress(min(max(int(round(score_val)), 0), 100))

    if total_jd_skills == 0:
        st.info(
            "This job description didn't list any technical skills from our taxonomy, "
            "so the score is based 100% on TF-IDF text similarity."
        )
    else:
        col_m, col_x = st.columns(2, gap="large")
        with col_m:
            st.subheader(f"Matched Skills ({len(matched)})")
            if matched:
                pills = "".join(f'<span class="pill-green">{s}</span>' for s in matched)
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.caption("None of the JD's tracked skills were detected in your resume.")

        with col_x:
            st.subheader(f"Missing Skills ({len(missing)})")
            if missing:
                pills = "".join(f'<span class="pill-red">{s}</span>' for s in missing)
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.success("You matched every tracked skill in this job description!")

    st.write("")
    with st.expander("How the score is calculated"):
        st.markdown(
            f"- **Hybrid Formula:** `{SKILL_WEIGHT:.2f} × Skill Coverage + {SIMILARITY_WEIGHT:.2f} × TF-IDF Cosine Similarity` (scaled to 0–100).\n"
            f"- **Fallback Rule:** When a job description contains 0 recognized skills from `skills.json`, the score falls back to `100 × TF-IDF Cosine Similarity`."
        )

    with st.expander("Resume sections detected"):
        sections = validation.get("sections_found", [])
        if sections:
            tags = "".join(f'<span class="pill-section">{sec.title()}</span>' for sec in sections)
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.caption("No standard section headings (Education, Experience, Skills, Projects) were detected.")

    with st.expander("Text we read from your PDF"):
        st.text_area(
            "Extracted PDF text",
            value=data["resume_text"],
            height=200,
            disabled=True,
            label_visibility="collapsed",
        )

    st.download_button(
        label="Download Match Report (.txt)",
        data=build_report_text(data),
        file_name="resume_match_report.txt",
        mime="text/plain",
    )


def main():
    st.set_page_config(
        page_title="Resume Analyzer & ATS Matcher",
        page_icon="📄",
        layout="wide",
    )
    inject_styles()
    render_sidebar()
    render_header()
    uploaded, jd_text, analyze_clicked = render_inputs()
    if analyze_clicked:
        run_analysis(uploaded, jd_text)
    render_results()


if __name__ == "__main__":
    main()