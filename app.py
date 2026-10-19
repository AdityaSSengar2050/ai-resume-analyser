import os
import json
import re
from pathlib import Path
from datetime import datetime
import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Resume Analyser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1e3a8a; margin-bottom: 0.2rem; }
    .sub-title { color: #64748b; font-size: 1rem; margin-bottom: 1.5rem; }
    .score-card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; text-align: center; }
    .metric-val { font-size: 2.2rem; font-weight: 800; }
    .metric-label { font-size: 0.85rem; color: #64748b; text-transform: uppercase; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Helper functions
def extract_text_from_pdf_bytes(file_bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_text_from_docx_bytes(file_bytes) -> str:
    import io
    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()

SYSTEM_PROMPT = """
You are an expert HR consultant and ATS (Applicant Tracking System) specialist.
When given a resume (and optionally a job description), you MUST respond with a valid JSON object.
Schema:
{
  "candidate": {
    "name": "string or null",
    "email": "string or null",
    "phone": "string or null",
    "location": "string or null",
    "linkedin": "string or null",
    "github": "string or null"
  },
  "summary": "2-3 sentence professional summary",
  "skills": {
    "technical": ["skills"],
    "soft": ["skills"],
    "tools": ["tools"]
  },
  "ats_check": {
    "score": 0-100,
    "verdict": "Pass | Fail | Marginal",
    "issues": ["issues"],
    "strengths": ["strengths"]
  },
  "job_match": {
    "score": 0-100,
    "verdict": "Excellent | Good | Fair | Poor",
    "matched_keywords": ["matched"],
    "missing_keywords": ["missing"]
  },
  "skill_gaps": ["missing skills"],
  "improvements": [
    {"area": "string", "suggestion": "string", "priority": "High | Medium | Low"}
  ],
  "overall_score": 0-100,
  "overall_verdict": "Strong | Average | Needs Work"
}
"""

def analyse_resume(client, resume_text, job_desc=""):
    user_content = f"RESUME:\n{resume_text}"
    if job_desc.strip():
        user_content += f"\n\nJOB DESCRIPTION:\n{job_desc}"
    else:
        user_content += "\n\n(No job description provided - evaluate general strength and ATS readability.)"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/resume.png", width=64)
    st.title("⚙️ Settings")
    api_key_env = os.getenv("OPENAI_API_KEY", "")
    api_key_input = st.text_input("OpenAI API Key", value=api_key_env if api_key_env != "your_openai_api_key_here" else "", type="password", help="Enter your sk-... key")
    
    st.markdown("---")
    st.markdown("### 📌 Features")
    st.markdown("- 📄 Multi-format: PDF & DOCX")
    st.markdown("- 🤖 Powered by GPT-4o")
    st.markdown("- 🎯 Real-time ATS & JD Matching")
    st.markdown("- 📥 Instant JSON Export")

# Main Content
st.markdown('<div class="main-title">📄 AI Resume Analyser</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Evaluate resume strength, check ATS compatibility, and identify skill gaps against target jobs.</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX file", type=["pdf", "docx"])
    
    # Or load demo
    use_sample = st.checkbox("Or use preloaded sample resume (Jane Smith)")
    
with col2:
    st.subheader("2. Target Job Description (Optional)")
    job_desc = st.text_area(
        "Paste the Job Description to calculate Match Score & Missing Keywords",
        height=180,
        placeholder="Paste full job posting or requirements here..."
    )

analyze_btn = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)

if analyze_btn:
    resume_text = ""
    file_name = "sample_resume.pdf"
    
    if uploaded_file:
        file_name = uploaded_file.name
        bytes_data = uploaded_file.read()
        if uploaded_file.name.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf_bytes(bytes_data)
        else:
            resume_text = extract_text_from_docx_bytes(bytes_data)
    elif use_sample:
        sample_path = Path("sample_resume.pdf")
        if sample_path.exists():
            with open(sample_path, "rb") as f:
                resume_text = extract_text_from_pdf_bytes(f.read())
        else:
            st.error("Sample resume not found. Please upload a file.")
    else:
        st.warning("Please upload a resume or select the sample resume checkbox!")
        st.stop()

    if not resume_text or len(resume_text) < 40:
        st.error("Could not extract enough readable text from the file.")
        st.stop()

    active_key = api_key_input.strip()
    
    # If no key, show simulated results for preview or run live
    if not active_key or active_key.startswith("your_"):
        st.info("ℹ️ No valid OpenAI key supplied. Showing simulated demo analysis.")
        analysis = {
            "candidate": {
                "name": "Jane Smith",
                "email": "jane.smith@email.com",
                "phone": "+91 98765 43210",
                "location": "Bangalore, India",
                "linkedin": "linkedin.com/in/janesmith",
                "github": "github.com/janesmith"
            },
            "summary": "Results-driven Software Engineer with 4 years of experience building scalable backend systems and APIs. Proficient in Python, Django, and REST API development with hands-on AWS cloud experience.",
            "skills": {
                "technical": ["Python", "FastAPI", "Django", "PostgreSQL", "Redis", "Docker", "REST APIs"],
                "soft": ["Team Leadership", "Agile", "Communication", "Problem Solving"],
                "tools": ["Git", "AWS (EC2, S3)", "Postman", "Linux"]
            },
            "ats_check": {
                "score": 85,
                "verdict": "Pass",
                "strengths": ["Clear standard headings", "Measurable achievements with metrics", "Clean scannable layout"],
                "issues": ["Could expand on specific CI/CD automation tools", "Missing certifications date details"]
            },
            "job_match": {
                "score": 78,
                "verdict": "Good",
                "matched_keywords": ["Python", "Django", "FastAPI", "AWS", "Docker", "Leadership"],
                "missing_keywords": ["Kubernetes", "CI/CD Pipelines", "GCP", "5+ years experience"]
            },
            "skill_gaps": ["Kubernetes container orchestration", "CI/CD deployment pipelines (GitHub Actions/Jenkins)", "Multi-cloud experience (GCP)"],
            "improvements": [
                {"area": "Cloud & DevOps", "suggestion": "Add hands-on Kubernetes and CI/CD pipelines to match senior level requirements.", "priority": "High"},
                {"area": "Impact Metrics", "suggestion": "Quantify outcomes in your second role with % latency reduction or revenue impact.", "priority": "Medium"},
                {"area": "Certifications", "suggestion": "Highlight AWS Certified Developer Associate prominently at the top.", "priority": "Low"}
            ],
            "overall_score": 82,
            "overall_verdict": "Strong"
        }
    else:
        with st.spinner("Analyzing with GPT-4o..."):
            client = OpenAI(api_key=active_key)
            try:
                analysis = analyse_resume(client, resume_text, job_desc)
            except Exception as e:
                st.error(f"Error calling OpenAI API: {e}")
                st.stop()

    st.success("Analysis complete!")
    st.markdown("---")
    
    # Candidate Header
    cand = analysis.get("candidate", {})
    st.markdown(f"### 👤 {cand.get('name') or 'Candidate Profile'}")
    c1, c2, c3, c4 = st.columns(4)
    c1.write(f"📧 **Email:** {cand.get('email') or 'N/A'}")
    c2.write(f"📱 **Phone:** {cand.get('phone') or 'N/A'}")
    c3.write(f"📍 **Location:** {cand.get('location') or 'N/A'}")
    c4.write(f"🔗 **LinkedIn:** {cand.get('linkedin') or 'N/A'}")

    st.write(f"**Professional Summary:** {analysis.get('summary', 'N/A')}")
    st.markdown("<br>", unsafe_allow_html=True)

    # Metric Dashboard
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="score-card">
            <div class="metric-label">Overall Score</div>
            <div class="metric-val" style="color: #16a34a;">{analysis.get('overall_score', 'N/A')}/100</div>
            <div>{analysis.get('overall_verdict', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        ats_val = analysis.get('ats_check', {}).get('score', 'N/A')
        st.markdown(f"""
        <div class="score-card">
            <div class="metric-label">ATS Compatibility</div>
            <div class="metric-val" style="color: #2563eb;">{ats_val}/100</div>
            <div>{analysis.get('ats_check', {}).get('verdict', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        jm_val = analysis.get('job_match', {}).get('score')
        jm_display = f"{jm_val}/100" if jm_val is not None else "N/A"
        st.markdown(f"""
        <div class="score-card">
            <div class="metric-label">Job Match</div>
            <div class="metric-val" style="color: #ca8a04;">{jm_display}</div>
            <div>{analysis.get('job_match', {}).get('verdict', 'No JD provided')}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        gaps_count = len(analysis.get('skill_gaps', []))
        st.markdown(f"""
        <div class="score-card">
            <div class="metric-label">Skill Gaps</div>
            <div class="metric-val" style="color: #dc2626;">{gaps_count}</div>
            <div>Areas to improve</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Detailed Tabs
    t_skills, t_ats, t_match, t_improve = st.tabs(["🛠️ Skills Extracted", "✅ ATS Checklist", "🎯 Job Match & Gaps", "🚀 Actionable Improvements"])

    with t_skills:
        skills_obj = analysis.get("skills", {})
        st.markdown("**Technical Skills:**")
        st.write(", ".join([f"`{s}`" for s in skills_obj.get("technical", [])]))
        st.markdown("**Tools & Frameworks:**")
        st.write(", ".join([f"`{s}`" for s in skills_obj.get("tools", [])]))
        st.markdown("**Soft Skills:**")
        st.write(", ".join([f"`{s}`" for s in skills_obj.get("soft", [])]))

    with t_ats:
        col_s, col_i = st.columns(2)
        with col_s:
            st.markdown("#### 🟢 Strengths")
            for item in analysis.get("ats_check", {}).get("strengths", []):
                st.write(f"- ✅ {item}")
        with col_i:
            st.markdown("#### 🔴 Identified Issues")
            for item in analysis.get("ats_check", {}).get("issues", []):
                st.write(f"- ⚠️ {item}")

    with t_match:
        jm = analysis.get("job_match", {})
        if jm.get("matched_keywords"):
            st.markdown("**✅ Matched Keywords:**")
            st.write(", ".join([f"`{k}`" for k in jm.get("matched_keywords", [])]))
        if jm.get("missing_keywords"):
            st.markdown("**❌ Missing Target Keywords:**")
            st.write(", ".join([f"`{k}`" for k in jm.get("missing_keywords", [])]))
        
        gaps = analysis.get("skill_gaps", [])
        if gaps:
            st.markdown("#### 💡 Identified Skill Gaps:")
            for g in gaps:
                st.write(f"- ⚠️ {g}")

    with t_improve:
        for imp in analysis.get("improvements", []):
            priority = imp.get("priority", "Medium")
            badge = "🔴" if priority == "High" else ("🟡" if priority == "Medium" else "🟢")
            st.info(f"{badge} **[{priority}] {imp.get('area')}:** {imp.get('suggestion')}")

    st.download_button(
        label="📥 Download JSON Report",
        data=json.dumps(analysis, indent=2),
        file_name=f"{cand.get('name', 'resume')}_analysis.json",
        mime="application/json"
    )
