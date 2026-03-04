"""
Embedding generator using sentence-transformers.
Uses bge-base-en-v1.5 — best small model for academic text.

Install: pip install sentence-transformers
"""

import numpy as np
from typing import Union
from ...config.settings import EmbedderConfig
from ...utils.models import Chunk


class Embedder:
    def __init__(self, config: EmbedderConfig):
        self.config = config
        self._model = None   # Lazy load — don't load until first use

    def _load_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            print(f"[Embedder] Loading model: {self.config.model_name}")
            self._model = SentenceTransformer(
                self.config.model_name,
                device=self.config.device,
            )
            print("[Embedder] Model loaded.")

    def embed_chunks(self, chunks: list[Chunk]) -> list[tuple[Chunk, list[float]]]:
        """
        Embed a list of chunks.
        Returns list of (chunk, embedding) tuples.
        bge models need a query prefix for queries but NOT for documents.
        """
        self._load_model()

        texts = [chunk.text for chunk in chunks]
        print(f"[Embedder] Embedding {len(texts)} chunks in batches of {self.config.batch_size}...")

        embeddings = self._model.encode(
            texts,
            batch_size=self.config.batch_size,
            normalize_embeddings=self.config.normalize_embeddings,
            show_progress_bar=True,
        )

        return list(zip(chunks, embeddings.tolist()))

    def embed_query(self, query: str) -> list[float]:
        """
        Embed a user query.
        bge models use "Represent this sentence for searching relevant passages: "
        prefix for queries to improve retrieval quality.
        """
        self._load_model()

        # bge-specific query prefix
        prefixed_query = f"Represent this sentence for searching relevant passages: {query}"

        embedding = self._model.encode(
            prefixed_query,
            normalize_embeddings=self.config.normalize_embeddings,
        )
        return embedding.tolist()

    def embed_text(self, text: str) -> list[float]:
        """Embed a single arbitrary text (no query prefix)."""
        self._load_model()
        embedding = self._model.encode(
            text,
            normalize_embeddings=self.config.normalize_embeddings,
        )
        return embedding.tolist()