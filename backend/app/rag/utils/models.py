"""
Shared data models for the RAG system.
Every module uses these types — defined once here.
"""

from dataclasses import dataclass, field
from typing import Optional
import uuid


# ─────────────────────────────────────────────
# INGESTION MODELS
# ─────────────────────────────────────────────

@dataclass
class ParsedFigure:
    """A figure extracted from the PDF with its vision-generated description."""
    figure_number: int
    caption: str
    page: int
    description: str = ""          # Filled by vision model
    image_path: Optional[str] = None


@dataclass
class ParsedSection:
    """A single section of a research paper after PDF parsing."""
    name: str                      # e.g. "methodology"
    raw_text: str                  # Original text, pre-cleaning
    page_start: int
    page_end: int
    figures: list[ParsedFigure] = field(default_factory=list)


@dataclass
class ParsedPaper:
    """Full parsed representation of a research paper."""
    paper_id: str
    title: str
    authors: list[str]
    sections: list[ParsedSection]
    total_pages: int
    source_path: str               # Original PDF path


# ─────────────────────────────────────────────
# CHUNK MODEL — Core unit of the RAG system
# ─────────────────────────────────────────────

@dataclass
class Chunk:
    """
    The atomic unit stored in the vector DB.
    Every retrieval result is a Chunk.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    paper_id: str = ""
    text: str = ""                 # Cleaned text ready for embedding
    section: str = ""              # e.g. "methodology"
    page: int = 0
    paragraph: int = 0
    chunk_index: int = 0           # Position within section
    is_figure_description: bool = False
    had_citations: bool = False    # True if original text had inline citations
    token_count: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "paper_id": self.paper_id,
            "text": self.text,
            "section": self.section,
            "page": self.page,
            "paragraph": self.paragraph,
            "chunk_index": self.chunk_index,
            "is_figure_description": self.is_figure_description,
            "had_citations": self.had_citations,
            "token_count": self.token_count,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Chunk":
        return cls(**d)


# ─────────────────────────────────────────────
# RETRIEVAL MODELS
# ─────────────────────────────────────────────

@dataclass
class RetrievedChunk:
    """A chunk returned from retrieval with its scores."""
    chunk: Chunk
    dense_score: float = 0.0
    sparse_score: float = 0.0
    rrf_score: float = 0.0         # Final fused score
    rerank_score: float = 0.0      # Score after cross-encoder reranking
    final_score: float = 0.0       # Ultimate score used for final ranking


@dataclass
class RetrievalResult:
    """Full result of a retrieval pass."""
    query: str
    rewritten_query: Optional[str]
    sub_queries: list[str]         # From query decomposition
    chunks: list[RetrievedChunk]
    retrieval_mode: str = "normal"


# ─────────────────────────────────────────────
# GENERATION MODELS
# ─────────────────────────────────────────────

@dataclass
class Citation:
    section: str
    page: int
    chunk_id: str


@dataclass
class RAGAnswer:
    """Final answer returned to the user."""
    question: str
    answer: str
    citations: list[Citation]
    evidence_snippets: list[str]   # Raw chunk text, for evidence mode
    retrieval_mode: str = "normal"
    found_in_paper: bool = True    # False if answer is "not found"