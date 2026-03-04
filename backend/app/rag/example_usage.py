"""
Quick start — shows exactly how to use the RAG system end-to-end.

Setup:
    1. pip install -r requirements.txt
    2. cp .env.example .env  →  add your OPENAI_API_KEY
    3. Start Qdrant: docker run -p 6333:6333 qdrant/qdrant
    4. python example_usage.py
"""

import os
from dotenv import load_dotenv
load_dotenv()

from rag.pipeline import RAGPipeline
from rag.config.settings import RAGConfig, VectorDBConfig


def main():
    # ── Configure (override any defaults here)
    config = RAGConfig()
    config.vectordb.qdrant_in_memory = True   # Use in-memory for this demo

    # ── Initialize pipeline (loads models lazily)
    rag = RAGPipeline(config)

    # ── Ingest a paper
    paper_id = rag.ingest_paper("your_paper.pdf")

    # ── Ask questions
    questions = [
        "What method did they propose?",
        "What dataset and accuracy did they achieve?",    # Compound — will decompose
        "How does this compare to transformer baselines?",
        "What were the training hyperparameters?",
        "What are the limitations of this approach?",
    ]

    for question in questions:
        print(f"\n{'─'*60}")
        print(f"Q: {question}")
        print(f"{'─'*60}")

        # Normal mode for most questions
        answer = rag.ask(question, paper_id=paper_id, mode="normal")

        print(answer.answer)
        print("\nSources:")
        for citation in answer.citations:
            print(f"  - ({citation.section.title()}, Page {citation.page})")


if __name__ == "__main__":
    main()