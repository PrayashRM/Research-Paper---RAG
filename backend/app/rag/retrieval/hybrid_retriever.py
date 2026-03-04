"""
Vector DB layer using Qdrant.
Handles: upsert, dense search, metadata filtering.

Install: pip install qdrant-client
Run Qdrant locally: docker run -p 6333:6333 qdrant/qdrant
"""

from typing import Optional
from ...config.settings import VectorDBConfig
from ...utils.models import Chunk, RetrievedChunk


class VectorDB:
    def __init__(self, config: VectorDBConfig):
        self.config = config
        self._client = None
        self._connect()

    def _connect(self):
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams

        if self.config.qdrant_in_memory:
            self._client = QdrantClient(":memory:")
            print("[VectorDB] Using in-memory Qdrant (dev mode)")
        else:
            self._client = QdrantClient(
                host=self.config.qdrant_host,
                port=self.config.qdrant_port,
            )
            print(f"[VectorDB] Connected to Qdrant at {self.config.qdrant_host}:{self.config.qdrant_port}")

        # Create collection if it doesn't exist
        existing = [c.name for c in self._client.get_collections().collections]
        if self.config.collection_name not in existing:
            self._client.create_collection(
                collection_name=self.config.collection_name,
                vectors_config=VectorParams(
                    size=self.config.embedding_dim,
                    distance=Distance.COSINE,
                ),
            )
            print(f"[VectorDB] Created collection: {self.config.collection_name}")

    def upsert_chunks(self, chunk_embeddings: list[tuple[Chunk, list[float]]]):
        """
        Store chunks + embeddings in Qdrant.
        chunk_embeddings: list of (Chunk, embedding) tuples from Embedder.
        """
        from qdrant_client.models import PointStruct

        points = []
        for chunk, embedding in chunk_embeddings:
            points.append(PointStruct(
                id=chunk.id,
                vector=embedding,
                payload=chunk.to_dict(),
            ))

        self._client.upsert(
            collection_name=self.config.collection_name,
            points=points,
        )
        print(f"[VectorDB] Upserted {len(points)} chunks")

    def dense_search(
        self,
        query_embedding: list[float],
        top_k: int,
        paper_id: Optional[str] = None,
    ) -> list[RetrievedChunk]:
        """
        Dense (semantic) similarity search.
        Optionally filter by paper_id to scope results to one paper.
        """
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        query_filter = None
        if paper_id:
            query_filter = Filter(
                must=[FieldCondition(
                    key="paper_id",
                    match=MatchValue(value=paper_id)
                )]
            )

        results = self._client.search(
            collection_name=self.config.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        )

        retrieved = []
        for hit in results:
            chunk = Chunk.from_dict(hit.payload)
            retrieved.append(RetrievedChunk(
                chunk=chunk,
                dense_score=hit.score,
            ))

        return retrieved

    def delete_paper(self, paper_id: str):
        """Remove all chunks belonging to a paper."""
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        self._client.delete(
            collection_name=self.config.collection_name,
            points_selector=Filter(
                must=[FieldCondition(
                    key="paper_id",
                    match=MatchValue(value=paper_id)
                )]
            ),
        )
        print(f"[VectorDB] Deleted all chunks for paper: {paper_id}")

    def get_chunk_count(self, paper_id: Optional[str] = None) -> int:
        """Return total chunk count, optionally filtered by paper."""
        if paper_id is None:
            return self._client.get_collection(self.config.collection_name).points_count

        from qdrant_client.models import Filter, FieldCondition, MatchValue
        result = self._client.count(
            collection_name=self.config.collection_name,
            count_filter=Filter(
                must=[FieldCondition(
                    key="paper_id",
                    match=MatchValue(value=paper_id)
                )]
            ),
        )
        return result.count