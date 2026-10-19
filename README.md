# 📄 Resume Analyser

An AI-powered resume analysis tool built as a **Jupyter Notebook** using the **OpenAI GPT-4o API**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 File Parsing | Reads PDF and DOCX resume files |
| 🧠 Info Extraction | Name, email, phone, skills, education, experience |
| 🎯 Job Match Scoring | Scores resume against a job description (0-100) |
| ✅ ATS Check | Checks ATS compatibility, finds issues and strengths |
| 💡 Skill Gap Analysis | Suggests missing skills and improvements |
| 📦 Export | Saves report as JSON or professionally styled PDF |
| 🔄 Batch Mode | Analyse multiple resumes at once with a ranking table |

---

## 🛠️ Setup

### 1. Install dependencies
```bash
cd resume_analyser
pip install -r requirements.txt
```

### 2. Configure your OpenAI API key
```bash
# Copy the template
copy .env.example .env

# Edit .env and add your key:
# OPENAI_API_KEY=sk-...
```
Get your API key at: https://platform.openai.com/api-keys

### 3. Launch Jupyter Notebook
```bash
jupyter notebook resume_analyser.ipynb
```

---

## 🚀 Usage

### Single Resume Analysis (Cell 7)
1. Set `RESUME_FILE` to the path of your PDF or DOCX resume
2. Optionally paste a job description into `JOB_DESCRIPTION`
3. Run cells 1–8 in order

### Batch Analysis (Cell 9)
Uncomment the `batch_analyse(...)` call and provide a list of resume file paths.

---

## 📁 Project Structure

```
resume_analyser/
├── resume_analyser.ipynb    # Main notebook (run this)
├── requirements.txt         # Python dependencies
├── .env.example             # API key template → copy to .env
├── .env                     # Your actual API key (not committed)
├── sample_resume.pdf        # (Optional) Test with this
└── exports/                 # Auto-created — JSON & PDF reports saved here
```

---

## 📤 Output Example

```
════════════════════════════════════════════════════════════
  📄 RESUME ANALYSIS REPORT
  👤 Jane Doe
════════════════════════════════════════════════════════════

🏆 SCORES DASHBOARD
────────────────────────────────────────────────────────────
  🟢 Overall Score  : 82/100  [Strong]
  🟡    ATS Score   : 68/100  [Marginal]
  🟢    Job Match   : 78/100  [Good]
```

---

## 📦 Export Formats

- **JSON** — Full structured analysis data, perfect for further processing
- **PDF** — Clean, professional report with color-coded scores table

Exports are saved to the `exports/` folder automatically.

---

## ⚠️ Notes

- Requires an active OpenAI API key with GPT-4o access
- Each analysis call uses ~1000-3000 tokens (≈ \$0.01–\$0.04 per resume)
- Image-based PDFs (scanned documents) won't work — text must be selectable
