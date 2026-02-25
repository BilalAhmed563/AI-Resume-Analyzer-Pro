import streamlit as st
from pdfminer.high_level import extract_text
import spacy
import re
from skills import SKILL_CATEGORIES

# Load NLP model (NO download here)
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Analyzer Pro", layout="wide")
st.title("🚀 AI Resume Analyzer Pro (NLP Powered)")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if uploaded_file is not None and job_description:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    resume_text = extract_text("temp_resume.pdf")
    resume_text_lower = resume_text.lower()
    job_text_lower = job_description.lower()

    resume_doc = nlp(resume_text)
    job_doc = nlp(job_description)

    found_skills = []
    required_skills = []
    missing_skills = []
    skill_frequency = {}

    # =========================
    # NLP SKILL DETECTION
    # =========================

    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:

            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, resume_text_lower):
                found_skills.append(skill)
                skill_frequency[skill] = len(re.findall(pattern, resume_text_lower))

            if re.search(pattern, job_text_lower):
                required_skills.append(skill)

    # Remove duplicates
    found_skills = list(set(found_skills))
    required_skills = list(set(required_skills))

    # =========================
    # MATCH CALCULATION
    # =========================

    match_count = len(set(found_skills) & set(required_skills))

    if len(required_skills) > 0:
        match_percentage = (match_count / len(required_skills)) * 100
    else:
        match_percentage = 0

    missing_skills = list(set(required_skills) - set(found_skills))

    # =========================
    # EXPERIENCE DETECTION (Improved)
    # =========================

    experience_pattern = r"(\d+)\+?\s*(years|year)"
    experience_match = re.findall(experience_pattern, resume_text_lower)

    if experience_match:
        total_experience = max([int(x[0]) for x in experience_match])
    else:
        total_experience = 0

    # =========================
    # EDUCATION EXTRACTION (Using NLP Entities)
    # =========================

    education_keywords = ["bachelor", "master", "phd", "bs", "ms", "bsc", "msc"]
    detected_education = []

    for token in resume_doc:
        if token.text.lower() in education_keywords:
            detected_education.append(token.text)

    detected_education = list(set(detected_education))

    # =========================
    # AUTOMATIC SUGGESTIONS
    # =========================

    suggestions = []

    if match_percentage < 50:
        suggestions.append("Increase job-specific skills in your resume.")

    if total_experience == 0:
        suggestions.append("Clearly mention your work experience (e.g., 2+ years).")

    if len(detected_education) == 0:
        suggestions.append("Add clear education details (BS/MS/PhD).")

    if len(found_skills) < 5:
        suggestions.append("Add more technical skills to strengthen your profile.")

    # =========================
    # UI
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Detected Skills")
        st.write(found_skills)

        st.subheader("📊 Skill Frequency")
        st.write(skill_frequency)

        st.subheader("🎓 Education Found")
        st.write(detected_education)

    with col2:
        st.subheader("📌 Required Skills")
        st.write(required_skills)

        st.subheader("❌ Missing Skills")
        st.write(missing_skills)

        st.subheader("💼 Experience Detected")
        st.write(f"{total_experience} years")

    st.subheader("🎯 Match Score")
    st.progress(int(match_percentage))
    st.write(f"Match Percentage: {match_percentage:.2f}%")

    resume_score = len(found_skills) * 5 + total_experience * 5
    st.subheader("🏆 Resume Strength Score")
    st.write(f"Overall Resume Score: {resume_score}/100")

    st.subheader("🚀 Resume Improvement Recommendations")
    st.write(suggestions)