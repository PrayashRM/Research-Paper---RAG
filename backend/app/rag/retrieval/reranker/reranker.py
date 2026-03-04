"""
Cross-encoder reranker + MMR-based deduplication.
Runs after hybrid retrieval.

Install: pip install sentence-transformers
"""

import numpy as np
from ...config.settings import RetrievalConfig
from ...utils.models import RetrievedChunk
from ...ingestion.embedder.embedder import Embedder


class Reranker:
    def __init__(self, config: RetrievalConfig, embedder: Embedder):
        self.config = config
        self.embedder = embedder
        self._cross_encoder = None

    def _load_model(self):
        if self._cross_encoder is None:
            from sentence_transformers import CrossEncoder
            print(f"[Reranker] Loading cross-encoder: {self.config.reranker_model}")
            self._cross_encoder = CrossEncoder(self.config.reranker_model)
            print("[Reranker] Cross-encoder loaded.")

    def rerank(
        self,
        query: str,
        candidates: list[RetrievedChunk],
        final_k: int,
    ) -> list[RetrievedChunk]:
        """
        Full reranking pipeline:
        1. Cross-encoder scoring
        2. MMR deduplication
        3. Return top final_k
        """
        if not candidates:
            return []

        # Step 1: Cross-encoder reranking
        reranked = self._cross_encode(query, candidates)

        # Step 2: MMR deduplication — remove near-duplicate chunks
        deduplicated = self._deduplicate_mmr(reranked, final_k)

        return deduplicated

    def _cross_encode(
        self,
        query: str,
        candidates: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """Score each (query, chunk) pair with the cross-encoder."""
        self._load_model()

        pairs = [(query, r.chunk.text) for r in candidates]
        scores = self._cross_encoder.predict(pairs)

        for retrieved, score in zip(candidates, scores):
            retrieved.rerank_score = float(score)
            retrieved.final_score = float(score)

        return sorted(candidates, key=lambda x: x.final_score, reverse=True)

    def _deduplicate_mmr(
        self,
        candidates: list[RetrievedChunk],
        final_k: int,
    ) -> list[RetrievedChunk]:
        """
        Maximal Marginal Relevance deduplication.
        Removes chunks that are too similar to already-selected chunks.
        Uses cosine similarity on pre-computed embeddings.
        """
        if len(candidates) <= final_k:
            return candidates

        threshold = self.config.dedup_similarity_threshold

        # Embed all candidate texts for similarity comparison
        texts = [r.chunk.text for r in candidates]
        embeddings = [
            np.array(self.embedder.embed_text(t)) for t in texts
        ]

        selected = []
        selected_embeddings = []

        for i, candidate in enumerate(candidates):
            if len(selected) >= final_k:
                break

            emb = embeddings[i]

            # Check similarity against all already-selected chunks
            too_similar = False
            for sel_emb in selected_embeddings:
                # Cosine similarity (embeddings are already normalized)
                similarity = float(np.dot(emb, sel_emb))
                if similarity > threshold:
                    too_similar = True
                    break

            if not too_similar:
                selected.append(candidate)
                selected_embeddings.append(emb)

        return selected