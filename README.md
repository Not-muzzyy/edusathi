<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LLM-Groq_LLaMA_3.3-6C63FF?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/RAG-FAISS+LangChain-4ECDC4?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<h1 align="center">🎓 EduSathi</h1>
<h3 align="center">AI-Powered Study Companion for VSKUB Students</h3>

<p align="center">
  A production-grade, role-based educational platform that uses <strong>RAG (Retrieval-Augmented Generation)</strong> and <strong>LLMs</strong> to help students learn from their own study materials — with AI tutoring, adaptive quizzes, exam simulations, flashcards, and progress tracking and separate features 
</p>

---

## ✨ Features

### 🎒 Student Portal
| Feature | Description |
|---------|-------------|
| **AI Chat Tutor** | Ask questions from your uploaded PDFs — answers grounded in your study material |
| **Quiz Mode** | AI-generated MCQs with adaptive difficulty based on your performance |
| **Exam Simulation** | Timed mock exams with countdown timer and instant scoring |
| **Flashcards** | Auto-generated flashcards from your notes for quick revision |
| **Progress Tracker** | Track quizzes, scores, topic mastery, and export PDF reports |
| **Dashboard** | Personalized overview with metrics, score trends, and quick actions |

### 👨‍🏫 Faculty Portal
| Feature | Description |
|---------|-------------|
| **Student Analytics** | View all quiz attempts, filter by subject, monitor performance |
| **Platform Metrics** | Active students count, quiz completion rates |

### ⚙️ Admin Portal
| Feature | Description |
|---------|-------------|
| **User Management** | View, search, promote/demote roles, delete accounts |
| **Analytics Dashboard** | Platform-wide usage metrics and performance data |
| **Question Paper Upload** | Ingest past papers into the RAG knowledge base |
| **Paper Analysis** | AI-powered topic extraction with frequency, subtopics, and question types |

### 🔒 Role-Based Access Control
- **Students** — Can only access learning tools (Chat, Quiz, Exam, Flashcards, Progress)
- **Faculty** — Access to student analytics and performance monitoring
- **Admin** — Full access including user management and paper uploads
- Unauthorized pages auto-redirect to login — no data leakage

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit with custom glassmorphic CSS, SVG icon system |
| **LLM** | Groq API → LLaMA 3.3 70B Versatile |
| **RAG Pipeline** | LangChain + FAISS vector store + Sentence Transformers |
| **Embeddings** | `all-MiniLM-L6-v2` (384-dim) |
| **Database** | SQLite (users, quiz attempts, documents, progress) |
| **Auth** | bcrypt password hashing + session-based authentication |
| **PDF Processing** | pdfplumber + PyPDF2 |
| **Reports** | ReportLab PDF generation |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- A free [Groq API Key](https://console.groq.com/keys)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/edusathi.git
cd edusathi
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example env file
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=gsk_your_actual_key_here
DB_PATH=./data/users.db
VECTOR_STORE_DIR=./data/vector_stores
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile
SECRET_KEY=change_this_to_a_random_secret
APP_ENV=production
```

### 5. Run the App

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📁 Project Structure

```
edusathi/
├── app.py                      # Main entry point + login/register
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
│
├── .streamlit/
│   └── config.toml             # Streamlit theme config
│
├── data/
│   ├── .gitkeep                # Keeps data/ dir in git
│   ├── users.db                # SQLite database (auto-created)
│   ├── vector_stores/          # FAISS indexes (auto-created)
│   └── question_papers/        # Uploaded papers (auto-created)
│
├── modules/
│   ├── __init__.py
│   ├── auth.py                 # Authentication, user/quiz DB operations
│   ├── llm_client.py           # Groq LLM wrapper (chat, MCQ, analysis)
│   ├── rag_pipeline.py         # PDF ingestion + FAISS retrieval
│   ├── quiz_engine.py          # Quiz session state management
│   ├── flashcard_generator.py  # LLM-powered flashcard creation
│   ├── progress_tracker.py     # Score tracking + mastery calculation
│   ├── report_generator.py     # PDF report generation
│   ├── ui_components.py        # Global CSS + reusable UI components
│   ├── icons.py                # SVG icon registry (Lucide-style)
│   ├── modern_ui.py            # Input validation + toast notifications
│   └── validation.py           # Security validators
│
└── pages/
    ├── 1_Dashboard.py          # Student dashboard
    ├── 2_Chat_Tutor.py         # AI chat with uploaded PDFs
    ├── 3_Quiz_Mode.py          # Adaptive quiz generation
    ├── 4_Exam_Simulation.py    # Timed exam mode
    ├── 5_Flashcards.py         # Auto-generated flashcards
    ├── 6_Progress_Tracker.py   # Analytics + PDF report export
    ├── 7_Admin_Panel.py        # Admin: users, papers, analytics
    └── 8_Faculty_Panel.py      # Faculty: student performance
```

---

## 👤 Default Test Accounts

After first run, register new accounts through the app. To test role-based access:

1. **Register** a new account (defaults to `student` role)
2. To create an **admin** account, register normally, then manually update the role in the database:

```bash
# Open SQLite shell
sqlite3 data/users.db

# Promote a user to admin
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';

# Or create a faculty account
UPDATE users SET role = 'faculty' WHERE email = 'faculty@email.com';

.quit
```

---

## 🌐 Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path**: `app.py`
5. Add your secrets in **Advanced Settings → Secrets**:

```toml
GROQ_API_KEY = "gsk_your_key_here"
DB_PATH = "./data/users.db"
VECTOR_STORE_DIR = "./data/vector_stores"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"
SECRET_KEY = "your_random_secret"
APP_ENV = "production"
```

> ⚠️ **Note:** Streamlit Cloud uses ephemeral storage. The SQLite database and vector stores will reset on redeployment. For persistent data, consider migrating to PostgreSQL + a cloud vector DB.

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Your Groq API key for LLM access |
| `DB_PATH` | ❌ | SQLite database path (default: `./data/users.db`) |
| `VECTOR_STORE_DIR` | ❌ | FAISS vector store directory (default: `./data/vector_stores`) |
| `EMBEDDING_MODEL` | ❌ | Sentence transformer model (default: `all-MiniLM-L6-v2`) |
| `LLM_MODEL` | ❌ | Groq model name (default: `llama-3.3-70b-versatile`) |
| `SECRET_KEY` | ❌ | App secret for session security |
| `APP_ENV` | ❌ | `development` or `production` |

---

## 🛠️ Troubleshooting

<details>
<summary><b>App shows "GROQ_API_KEY not configured"</b></summary>

Make sure your `.env` file exists and contains a valid key:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```
Get a free key at [console.groq.com/keys](https://console.groq.com/keys)
</details>

<details>
<summary><b>ModuleNotFoundError on import</b></summary>

Ensure you activated your virtual environment and installed dependencies:
```bash
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```
</details>

<details>
<summary><b>Sidebar not showing after login</b></summary>

Hard-refresh the browser with `Ctrl + Shift + R`. The sidebar state may be cached from a previous session.
</details>

<details>
<summary><b>PDF upload fails or returns empty results</b></summary>

- Ensure the PDF has selectable text (not scanned images)
- Check file size is under 50MB
- Verify your Groq API key is valid and has remaining quota
</details>

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  built by contributors : 1. Mohammed Muzammil C <br> 2. Mohammed Muzammil 3. Maniyar Zahid Ahmed <br> 
</p>
