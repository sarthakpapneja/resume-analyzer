# Resume-Job Match Analyzer

A production-ready, AI-powered system to analyze resumes against job descriptions. Built with FastAPI, Next.js, and Sentence Transformers.

## Architecture

```mermaid
graph TD
    User[User] -->|Uploads PDF| Frontend[Next.js Frontend]
    Frontend -->|POST /analyze| Backend[FastAPI Backend]
    Backend -->|Extract Text| Parser[Resume Parser]
    Backend -->|Generate Embeddings| NLP[NLP Engine (MiniLM-L6)]
    Backend -->|Store/Retrieve| DB[FAISS Vector Store]
    Backend -->|Calculate Score| Scorer[Scoring Engine]
    Scorer -->|JSON| Frontend
```

## Features
- **Resume Parsing**: Supports PDF and DOCX.
- **AI Scoring**: Hybrid scoring using Semantic Similarity (Cosine) and Skill Overlap (Jaccard).
- **Skill Gap Analysis**: Identifies missing critical skills.
- **Recommendations**: Smart suggestions for improvement.
- **Dockerized**: specific `Dockerfile` for both services.

## Setup & Run

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.10+ / Node.js 18+

### Quick Start (Recommended)
1. Run the automated startup script:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
2. Access the app:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Manual Setup
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Demo
Use the files in `demo_data/` to test the system:
- `demo_data/sample_resume.pdf`
- `demo_data/sample_job_description.txt`

## Tech Stack
- **Frontend**: Next.js, Tailwind CSS, Shadcn UI
- **Backend**: FastAPI, Python
- **ML**: SentenceTransformers, Spacy, Scikit-learn, FAISS
- **Infra**: Docker, Docker Compose
