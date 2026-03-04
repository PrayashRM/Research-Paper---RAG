"""
Central config for the entire RAG system.
All tunable parameters live here — nothing hardcoded in modules.
"""

from dataclasses import dataclass, field
from typing import Literal


# ─────────────────────────────────────────────
# INGESTION CONFIG
# ─────────────────────────────────────────────

@dataclass
class ParserConfig:
    # Sections to KEEP (in order)
    sections_to_keep: list[str] = field(default_factory=lambda: [
        "abstract",
        "introduction",
        "related work",
        "background",
        "methodology",
        "method",
        "approach",
        "experiments",
        "experimental setup",
        "results",
        "discussion",
        "conclusion",
        "appendix",       # Kept — often has hyperparams, proofs
    ])

    # Sections to DROP entirely
    sections_to_drop: list[str] = field(default_factory=lambda: [
        "references",
        "acknowledgments",
        "acknowledgements",
        "funding",
        "author contributions",
        "conflict of interest",
    ])

    # Whether to extract figures and run vision description
    extract_figures: bool = True

    # Vision model to use for figure description
    vision_model: str = "gpt-4o-mini"   # swap to any vision-capable model


@dataclass
class CleanerConfig:
    remove_inline_citations: bool = True     # (Smith et al., 2021), [14]
    remove_latex_commands: bool = True       # \cite{}, \ref{}, \label{}
    remove_urls: bool = True
    remove_dois: bool = True
    remove_figure_refs: bool = True          # (see Figure 3)
    remove_org_sentences: bool = True        # "This paper is organized as..."


@dataclass
class ChunkerConfig:
    min_tokens: int = 400
    max_tokens: int = 800
    overlap_tokens: int = 80               # ~10% of 800
    respect_sentence_boundaries: bool = True
    treat_tables_as_atomic: bool = True    # Never split a table across chunks


@dataclass
class EmbedderConfig:
    model_name: str = "BAAI/bge-base-en-v1.5"   # Better than MiniLM for academic text
    batch_size: int = 32
    normalize_embeddings: bool = True
    device: str = "cpu"                          # "cuda" if GPU available


# ─────────────────────────────────────────────
# VECTOR DB CONFIG
# ─────────────────────────────────────────────

@dataclass
class VectorDBConfig:
    provider: Literal["qdrant", "chroma"] = "qdrant"
    collection_name: str = "research_papers"
    embedding_dim: int = 768               # bge-base-en-v1.5 dim
    distance_metric: str = "cosine"

    # Qdrant specific
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_in_memory: bool = False         # True for dev/testing


# ─────────────────────────────────────────────
# RETRIEVAL CONFIG
# ─────────────────────────────────────────────

@dataclass
class RetrievalConfig:
    # How many chunks to fetch before reranking
    initial_fetch_count: int = 6           # Was 10 — reduced for reranker speed

    # Final chunks passed to LLM after reranking + deduplication
    final_chunk_count: int = 5

    # RRF (Reciprocal Rank Fusion) constant — standard is 60
    rrf_k: int = 60

    # Deduplication threshold — chunks with similarity above this are deduplicated
    dedup_similarity_threshold: float = 0.92

    # Reranker model
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # Query rewriting — default ON
    query_rewriting_enabled: bool = True
    query_rewrite_model: str = "gpt-4o-mini"   # Small, fast, cheap


@dataclass
class RetrievalMode:
    """
    Three retrieval modes selectable per query.
    quick  → top 2 chunks, no rerank (fast)
    normal → top 5 chunks, with rerank (default)
    deep   → top 8 chunks, with rerank (complex questions)
    """
    mode: Literal["quick", "normal", "deep"] = "normal"

    chunk_counts: dict = field(default_factory=lambda: {
        "quick":  {"fetch": 3,  "final": 2},
        "normal": {"fetch": 6,  "final": 5},
        "deep":   {"fetch": 12, "final": 8},
    })


# ─────────────────────────────────────────────
# GENERATION CONFIG
# ─────────────────────────────────────────────

@dataclass
class GenerationConfig:
    model: str = "gpt-4o-mini"
    max_tokens: int = 1024
    temperature: float = 0.1              # Low temp = more factual, less creative

    # Evidence mode — return full paragraph snippets alongside answer
    evidence_mode: bool = False


# ─────────────────────────────────────────────
# MASTER CONFIG — Single object to pass everywhere
# ─────────────────────────────────────────────

@dataclass
class RAGConfig:
    parser: ParserConfig = field(default_factory=ParserConfig)
    cleaner: CleanerConfig = field(default_factory=CleanerConfig)
    chunker: ChunkerConfig = field(default_factory=ChunkerConfig)
    embedder: EmbedderConfig = field(default_factory=EmbedderConfig)
    vectordb: VectorDBConfig = field(default_factory=VectorDBConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)


# Default instance — import this everywhere
DEFAULT_CONFIG = RAGConfig()