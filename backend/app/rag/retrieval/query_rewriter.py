"""
Query rewriter — converts vague user queries into academic form.
Also handles compound query decomposition.
Uses a small LLM (gpt-4o-mini) with tight prompt.
Default ON.
"""

import os
import json
import re
from ...config.settings import RetrievalConfig


REWRITE_PROMPT = """You are helping retrieve information from a research paper.

Convert the user's question into a precise academic search query.
If the question is compound (asks about multiple things), split it into sub-queries.

Respond ONLY with JSON in this exact format:
{
  "rewritten": "precise single academic query",
  "sub_queries": ["sub-query 1", "sub-query 2"]
}

If the question is simple (not compound), sub_queries should contain only the rewritten query.

Examples:
User: "How do they train it?"
Output: {"rewritten": "What optimization algorithm and training procedure are described in the methodology section?", "sub_queries": ["What optimization algorithm and training procedure are described in the methodology section?"]}

User: "What dataset and accuracy?"
Output: {"rewritten": "What datasets and evaluation metrics are used in the experiments?", "sub_queries": ["What datasets are used in the experimental evaluation?", "What accuracy or performance metrics are reported in the results?"]}

User: "How does this compare to transformers and what GPU was used?"
Output: {"rewritten": "How does this method compare to transformer baselines and what computational resources were used?", "sub_queries": ["How does the proposed method compare to transformer-based baselines?", "What GPU or hardware infrastructure was used for experiments?"]}

Now rewrite this query:
"""


class QueryRewriter:
    def __init__(self, config: RetrievalConfig):
        self.config = config
        self._client = None

    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        return self._client

    def rewrite(self, query: str) -> tuple[str, list[str]]:
        """
        Rewrite a user query into academic form.
        Returns: (rewritten_query, sub_queries)
        sub_queries is used for multi-part question handling.
        """
        if not self.config.query_rewriting_enabled:
            return query, [query]

        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=self.config.query_rewrite_model,
                messages=[
                    {"role": "user", "content": REWRITE_PROMPT + query}
                ],
                max_tokens=300,
                temperature=0.0,
            )

            raw = response.choices[0].message.content.strip()
            parsed = self._parse_response(raw)

            rewritten = parsed.get("rewritten", query)
            sub_queries = parsed.get("sub_queries", [rewritten])

            print(f"[QueryRewriter] Original: '{query}'")
            print(f"[QueryRewriter] Rewritten: '{rewritten}'")
            if len(sub_queries) > 1:
                print(f"[QueryRewriter] Decomposed into {len(sub_queries)} sub-queries")

            return rewritten, sub_queries

        except Exception as e:
            print(f"[QueryRewriter] Failed, using original query. Error: {e}")
            return query, [query]

    def _parse_response(self, raw: str) -> dict:
        """Parse JSON response from LLM, handling common formatting issues."""
        # Strip markdown code fences if present
        raw = re.sub(r'```(?:json)?', '', raw).strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback: extract what we can
            return {"rewritten": raw, "sub_queries": [raw]}