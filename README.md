# 🎓 Smart AI Study Buddy & Quiz Generator

An intelligent EdTech & Retrieval-Augmented Generation (RAG) application that transforms lecture notes, PDFs, and study materials into dynamic practice quizzes, spaced repetition flashcards, and a 24/7 grounded AI tutor.

---

## ✨ Features

- 📄 **PDF & Notes Processing:** Extracts and chunks text from uploaded textbook PDFs or plain text lecture notes.
- ❓ **Dynamic MCQ Quiz Generator:** Auto-generates multiple-choice practice questions with randomized distractor options, instant grading, and detailed explanations.
- 🃏 **Spaced Repetition Flashcards:** Active recall study cards with flip-to-reveal answers and self-assessment buttons (`🔴 Needs Review`, `🟡 Good`, `🟢 Mastered`).
- 🤖 **24/7 Grounded RAG AI Tutor:** Ask questions about your study material and receive answers strictly grounded in the document context with source chunk citations.

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit
- **Document Parsing:** `pypdf`
- **RAG & Vector Retrieval:** Scikit-Learn (`TfidfVectorizer` + Cosine Similarity)
- **PDF Generation:** ReportLab
- **Language:** Python 3.10+

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/purva2005/AI_STUDY_BUDDY.git
cd AI_STUDY_BUDDY
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Web Application
```bash
python -m streamlit run study_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser!

---

## 📁 Project Structure

```text
AI_STUDY_BUDDY/
│
├── study_app.py                   # Main Streamlit Dashboard Application
├── requirements.txt               # Dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Files ignored by git
├── sample_study_material.pdf      # Demo lecture notes PDF
│
└── study_buddy/                   # Core Engine Package
    ├── __init__.py                # Package initializer
    ├── processor.py               # PDF Parsing & Semantic Text Chunking
    ├── rag_engine.py              # TF-IDF Vector Search & Q&A Grounding
    └── quiz_generator.py          # Dynamic Quiz & Flashcards Generator
```

---

## 📜 License
Licensed under the [MIT License](LICENSE).
