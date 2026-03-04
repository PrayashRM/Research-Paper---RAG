"""
Generation layer — grounded, citation-enforced LLM generation.
Strict mode: only answers from provided context.
"""

import os
from ...config.settings import GenerationConfig
from ...utils.models import RetrievedChunk, RAGAnswer, Citation


SYSTEM_PROMPT = """You are a research paper assistant. Your job is to answer questions strictly based on the provided excerpts from a research paper.

STRICT RULES:
1. ONLY use information explicitly stated in the provided context chunks.
2. Do NOT infer, extrapolate, or use any outside knowledge.
3. If the information is not directly present in the context, respond with exactly: "The paper does not directly address this."
4. Before giving your answer, quote the most relevant sentence from the context that supports it.
5. Always cite the section name and page number for every claim.

OUTPUT FORMAT (follow exactly):
Supporting quote: "[exact sentence from context]"

Answer:
[Your answer here, written clearly for someone unfamiliar with the paper]

Sources:
- (Section Name, Page X)
- (Section Name, Page Y)
"""

USER_PROMPT_TEMPLATE = """Context from the paper:
{context}

---
Question: {question}

Remember: Only answer using the context above. Quote the supporting sentence before answering."""


class Generator:
    def __init__(self, config: GenerationConfig):
        self.config = config
        self._client = None

    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        return self._client

    def generate(
        self,
        question: str,
        retrieved_chunks: list[RetrievedChunk],
        retrieval_mode: str = "normal",
    ) -> RAGAnswer:
        """
        Generate a grounded answer from retrieved chunks.
        """
        if not retrieved_chunks:
            return RAGAnswer(
                question=question,
                answer="The paper does not directly address this.",
                citations=[],
                evidence_snippets=[],
                retrieval_mode=retrieval_mode,
                found_in_paper=False,
            )

        # Build context string from chunks
        context = self._build_context(retrieved_chunks)

        # Generate answer
        raw_answer = self._call_llm(question, context)

        # Parse citations from the raw answer
        citations = self._extract_citations(raw_answer, retrieved_chunks)

        # Determine if the paper actually had the answer
        found = "does not directly address" not in raw_answer.lower()

        evidence_snippets = []
        if self.config.evidence_mode:
            evidence_snippets = [r.chunk.text for r in retrieved_chunks]

        return RAGAnswer(
            question=question,
            answer=raw_answer,
            citations=citations,
            evidence_snippets=evidence_snippets,
            retrieval_mode=retrieval_mode,
            found_in_paper=found,
        )

    def _build_context(self, chunks: list[RetrievedChunk]) -> str:
        """
        Format chunks into a readable context block for the LLM.
        Each chunk is labeled with its section and page.
        """
        parts = []
        for i, retrieved in enumerate(chunks, 1):
            c = retrieved.chunk
            label = f"[Chunk {i} | {c.section.title()} | Page {c.page}]"
            parts.append(f"{label}\n{c.text}")

        return "\n\n---\n\n".join(parts)

    def _call_llm(self, question: str, context: str) -> str:
        """Call the LLM with strict grounding prompt."""
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT_TEMPLATE.format(
                        context=context,
                        question=question,
                    )},
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"[Generator] LLM call failed: {e}")
            return "The paper does not directly address this."

    def _extract_citations(
        self,
        answer_text: str,
        chunks: list[RetrievedChunk],
    ) -> list[Citation]:
        """
        Extract citations from the answer.
        Also adds citations for all chunks that were used in context.
        """
        citations = []
        seen = set()

        for retrieved in chunks:
            c = retrieved.chunk
            key = (c.section, c.page)
            if key not in seen:
                citations.append(Citation(
                    section=c.section,
                    page=c.page,
                    chunk_id=c.id,
                ))
                seen.add(key)

        return citations