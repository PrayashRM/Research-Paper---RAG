# 📄 ResearchLens

> Making research papers accessible and appealing to everyone.

## ✨ Features

- **Structured Notes Generation** — Automatically generate comprehensive, structured notes from research papers using your own LLM API key
- **RAG-based Q&A** — Interactive question-answering system powered by a hybrid retrieval-augmented generation architecture
- **Multi-Model Support** — Choose from OpenAI, Anthropic, Google, and open-source models
- **Bring Your Own Key** — Use your own API keys for complete control and privacy

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vite + React |
| Backend | Python (FastAPI) + uv |
| LLM Integration | LangChain |
| PDF Processing | PyMuPDF |

## 🚀 Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend (coming soon)

```bash
uv sync --extra backend
uv run uvicorn backend.app.main:app --reload
```

## 📁 Project Structure

```
Project-ResearchPaper/
├── frontend/          # Vite + React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── context/
│   │   └── hooks/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   └── core/
│   └── tests/
├── pyproject.toml
└── README.md
```

## 📝 License

MIT
