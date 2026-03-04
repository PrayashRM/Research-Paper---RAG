"""
RAG Pipeline — the main orchestrator.
Ties together: ingestion, retrieval, generation.

Usage:
    from rag.pipeline import RAGPipeline
    from rag.config.settings import RAGConfig

    rag = RAGPipeline(RAGConfig())
    rag.ingest_paper("paper.pdf")
    answer = rag.ask("What training method did they use?", paper_id="...")
    print(answer.answer)
"""

from .config.settings import RAGConfig, DEFAULT_CONFIG
from .utils.models import RAGAnswer, ParsedPaper, Chunk

from .ingestion.parser.pdf_parser import PDFParser
from .ingestion.cleaner.text_cleaner import TextCleaner
from .ingestion.chunker.chunker import Chunker
from .ingestion.embedder.embedder import Embedder
from .vectordb.vector_store import VectorDB
from .retrieval.hybrid_retriever import HybridRetriever
from .retrieval.reranker.reranker import Reranker
from .retrieval.query_rewriter import QueryRewriter
from .generation.generator import Generator


class RAGPipeline:
    def __init__(self, config: RAGConfig = DEFAULT_CONFIG):
        self.config = config

        # ── Ingestion
        self.parser   = PDFParser(config.parser)
        self.cleaner  = TextCleaner(config.cleaner)
        self.chunker  = Chunker(config.chunker)
        self.embedder = Embedder(config.embedder)

        # ── Storage
        self.vector_db = VectorDB(config.vectordb)

        # ── Retrieval
        self.retriever = HybridRetriever(config.retrieval, self.vector_db, self.embedder)
        self.reranker  = Reranker(config.retrieval, self.embedder)
        self.query_rewriter = QueryRewriter(config.retrieval)

        # ── Generation
        self.generator = Generator(config.generation)

        print("[RAGPipeline] Initialized successfully.")

    # ─────────────────────────────────────────────
    # PHASE 1 — INGESTION
    # ─────────────────────────────────────────────

    def ingest_paper(self, pdf_path: str) -> str:
        """
        Full ingestion pipeline for a PDF.
        Returns the paper_id for use in queries.
        """
        print(f"\n{'='*50}")
        print(f"[Pipeline] Ingesting: {pdf_path}")
        print(f"{'='*50}")

        # Step 1: Parse PDF into sections
        paper: ParsedPaper = self.parser.parse(pdf_path)

        # Step 2: Clean text + chunk each section
        all_chunks: list[Chunk] = []

        for section in paper.sections:
            # Clean the raw text
            cleaned_text, had_citations = self.cleaner.clean_section(section.raw_text)
            section.raw_text = cleaned_text   # Replace with cleaned version

            # Chunk the section
            section_chunks = self.chunker.chunk_section(section, paper.paper_id)

            # Stamp had_citations on each chunk from this section
            for chunk in section_chunks:
                chunk.had_citations = had_citations

            all_chunks.extend(section_chunks)

        # Step 3: Generate figure description chunks
        for section in paper.sections:
            for fig in section.figures:
                if fig.description:
                    fig_chunk = self.chunker.create_figure_chunk(
                        figure_description=fig.description,
                        section_name=section.name,
                        page=fig.page,
                        paper_id=paper.paper_id,
                        chunk_index=len(all_chunks),
                    )
                    all_chunks.append(fig_chunk)

        # Step 4: Embed all chunks
        chunk_embeddings = self.embedder.embed_chunks(all_chunks)

        # Step 5: Store in vector DB
        self.vector_db.upsert_chunks(chunk_embeddings)

        # Step 6: Build BM25 index for this paper
        self.retriever.add_paper_to_bm25(paper.paper_id, all_chunks)

        print(f"\n[Pipeline] ✓ Ingestion complete.")
        print(f"[Pipeline]   Paper ID : {paper.paper_id}")
        print(f"[Pipeline]   Title    : {paper.title}")
        print(f"[Pipeline]   Sections : {len(paper.sections)}")
        print(f"[Pipeline]   Chunks   : {len(all_chunks)}")
        print(f"{'='*50}\n")

        return paper.paper_id

    # ─────────────────────────────────────────────
    # PHASE 2+3 — QUERY + GENERATE
    # ─────────────────────────────────────────────

    def ask(
        self,
        question: str,
        paper_id: str,
        mode: str = "normal",
    ) -> RAGAnswer:
        """
        Full RAG query pipeline.

        Args:
            question: User's question in plain language
            paper_id: ID of the paper to search (from ingest_paper)
            mode: "quick" | "normal" | "deep"

        Returns:
            RAGAnswer with answer text + citations
        """
        mode_config = self.config.retrieval
        retrieval_modes = {
            "quick":  {"fetch": 3,  "final": 2},
            "normal": {"fetch": 6,  "final": 5},
            "deep":   {"fetch": 12, "final": 8},
        }
        fetch_k = retrieval_modes.get(mode, retrieval_modes["normal"])["fetch"]
        final_k = retrieval_modes.get(mode, retrieval_modes["normal"])["final"]

        print(f"\n[Pipeline] Question: '{question}' | Mode: {mode}")

        # Step 1: Rewrite query + decompose if compound
        rewritten_query, sub_queries = self.query_rewriter.rewrite(question)

        # Step 2: Retrieve for each sub-query, merge results
        all_retrieved = []
        seen_ids = set()

        for sub_query in sub_queries:
            results = self.retriever.retrieve(
                query=sub_query,
                paper_id=paper_id,
                top_k=fetch_k,
            )
            for r in results:
                if r.chunk.id not in seen_ids:
                    all_retrieved.append(r)
                    seen_ids.add(r.chunk.id)

        print(f"[Pipeline] Retrieved {len(all_retrieved)} unique candidates")

        # Step 3: Rerank + deduplicate
        final_chunks = self.reranker.rerank(
            query=rewritten_query,
            candidates=all_retrieved,
            final_k=final_k,
        )

        print(f"[Pipeline] Final chunks after rerank: {len(final_chunks)}")

        # Step 4: Generate grounded answer
        answer = self.generator.generate(
            question=question,
            retrieved_chunks=final_chunks,
            retrieval_mode=mode,
        )

        return answer
