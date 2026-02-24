import streamlit as st
from pdfminer.high_level import extract_text
import spacy
import re
from skills import SKILL_CATEGORIES

nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Analyzer Pro", layout="wide")
st.title("🚀 AI Resume Analyzer Pro")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if uploaded_file is not None:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    resume_text = extract_text("temp_resume.pdf").lower()
    job_text = job_description.lower()

    found_skills = []
    required_skills = []
    missing_skills = []
    skill_frequency = {}

    # Skill Detection
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:

            if skill in resume_text:
                found_skills.append(skill)
                skill_frequency[skill] = resume_text.count(skill)

            if skill in job_text:
                required_skills.append(skill)

    # Match Calculation
    match_count = 0

    for skill in required_skills:
        if skill in found_skills:
            match_count += 1
        else:
            missing_skills.append(skill)

    if len(required_skills) > 0:
        match_percentage = (match_count / len(required_skills)) * 100
    else:
        match_percentage = 0

    # =========================
    # EXPERIENCE DETECTION
    # =========================

    experience_pattern = r"(\d+)\s+years"
    experience_match = re.findall(experience_pattern, resume_text)

    if experience_match:
        total_experience = max([int(x) for x in experience_match])
    else:
        total_experience = 0

    # =========================
    # EDUCATION EXTRACTION
    # =========================

    education_keywords = ["bs", "bachelor", "master", "msc", "phd", "bsc"]
    detected_education = []

    for word in education_keywords:
        if word in resume_text:
            detected_education.append(word)

    # =========================
    # AUTOMATIC SUGGESTIONS
    # =========================

    suggestions = []

    if match_percentage < 50:
        suggestions.append("Your resume has low job match. Add more relevant skills.")

    if total_experience == 0:
        suggestions.append("Mention your work experience clearly (e.g., 2 years experience).")

    if len(detected_education) == 0:
        suggestions.append("Add clear education details (BS/MS/PhD).")

    if len(found_skills) < 5:
        suggestions.append("Add more technical skills to strengthen resume.")

    # =========================
    # UI LAYOUT
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