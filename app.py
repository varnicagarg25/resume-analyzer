import streamlit as st

from src.extract import extract_text
from src.score import final_score
from src.validate import check_resume


st.set_page_config(page_title="Resume Analyzer & ATS Matcher")
st.title("Resume Analyzer & ATS Matcher")

uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste the job description", height=200)

if st.button("Analyze"):
    if uploaded is None:
        st.warning("Please upload a resume first.")
        st.stop()
    if not jd_text.strip():
        st.warning("Please paste a job description.")
        st.stop()

    try:
        uploaded.seek(0)
        resume_text = extract_text(uploaded)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    check = check_resume(resume_text)
    if not check["looks_like_resume"]:
        st.warning(
            "This doesn't look like a standard resume, so the score may "
            "not be accurate."
        )

    result = final_score(resume_text, jd_text)  # pass RAW text; it cleans internally

    score = result["score"]
    st.metric("Match score", f"{score:.1f}%")
    st.progress(max(0, min(100, int(round(score)))))
    st.caption(f"Text similarity: {result['similarity']:.2f}")

    if not result["matched_skills"] and not result["missing_skills"]:
        st.info(
            "No known technical/soft skills were detected in the job "
            "description. The score is based purely on text similarity."
        )
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Matched skills")
            if result["matched_skills"]:
                for skill in result["matched_skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("None of the required skills were found.")
        with col2:
            st.subheader("Missing skills")
            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("None. You cover every skill found in the job description.")

    with st.expander("Resume sections detected"):
        st.write(check["sections_found"] or "No standard sections found.")