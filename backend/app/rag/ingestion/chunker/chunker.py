"""
Smart chunker — sentence-aware, section-respecting.
Never mixes sections. Never splits mid-sentence.
Tables and equations treated as atomic units.
"""

import re
from ...config.settings import ChunkerConfig
from ...utils.models import Chunk, ParsedSection, ParsedPaper


class Chunker:
    def __init__(self, config: ChunkerConfig):
        self.config = config

    def chunk_paper(self, paper: ParsedPaper) -> list[Chunk]:
        """Chunk all sections of a paper into Chunk objects."""
        all_chunks = []
        for section in paper.sections:
            section_chunks = self.chunk_section(section, paper.paper_id)
            all_chunks.extend(section_chunks)

        print(f"[Chunker] Created {len(all_chunks)} chunks from {len(paper.sections)} sections")
        return all_chunks

    def chunk_section(self, section: ParsedSection, paper_id: str) -> list[Chunk]:
        """
        Chunk a single section into overlapping, sentence-boundary-respecting chunks.
        """
        text = section.raw_text.strip()
        if not text:
            return []

        # Step 1: Identify and extract atomic blocks (tables, equations)
        atomic_blocks, text_without_atomics = self._extract_atomic_blocks(text)

        # Step 2: Split remaining text into sentences
        sentences = self._split_into_sentences(text_without_atomics)

        # Step 3: Group sentences into chunks respecting token limits
        sentence_chunks = self._group_sentences_into_chunks(sentences)

        chunks = []
        chunk_index = 0

        # Add sentence-based chunks
        for chunk_text in sentence_chunks:
            if not chunk_text.strip():
                continue

            chunk = Chunk(
                paper_id=paper_id,
                text=chunk_text.strip(),
                section=section.name,
                page=section.page_start,
                paragraph=0,
                chunk_index=chunk_index,
                is_figure_description=False,
                token_count=self._count_tokens(chunk_text),
            )
            chunks.append(chunk)
            chunk_index += 1

        # Add atomic blocks (tables/equations) as their own chunks
        for block_text in atomic_blocks:
            chunk = Chunk(
                paper_id=paper_id,
                text=block_text.strip(),
                section=section.name,
                page=section.page_start,
                paragraph=0,
                chunk_index=chunk_index,
                is_figure_description=False,
                token_count=self._count_tokens(block_text),
            )
            chunks.append(chunk)
            chunk_index += 1

        return chunks

    def _extract_atomic_blocks(self, text: str) -> tuple[list[str], str]:
        """
        Extract tables and equation blocks that should NOT be split.
        Returns (list of atomic blocks, text with atomics removed).

        Detects:
        - Markdown tables (| col | col |)
        - LaTeX equation environments
        - Numbered equations
        """
        atomic_blocks = []
        remaining_text = text

        if self.config.treat_tables_as_atomic:
            # Markdown table pattern: lines starting with |
            table_pattern = re.compile(
                r'(\|.+\|(?:\n\|.+\|)+)',
                re.MULTILINE
            )
            for match in table_pattern.finditer(text):
                atomic_blocks.append(match.group(0))
            remaining_text = table_pattern.sub('', remaining_text)

            # LaTeX equation environments
            eq_pattern = re.compile(
                r'(\$\$[\s\S]+?\$\$|\\begin\{(?:equation|align|gather|eqnarray)\}[\s\S]+?\\end\{(?:equation|align|gather|eqnarray)\})',
                re.MULTILINE
            )
            for match in eq_pattern.finditer(text):
                atomic_blocks.append(match.group(0))
            remaining_text = eq_pattern.sub('', remaining_text)

        return atomic_blocks, remaining_text

    def _split_into_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences using simple but robust rules.
        Handles abbreviations, decimal numbers, etc.
        """
        # Protect common abbreviations from being split on
        abbreviations = ['et al', 'e.g', 'i.e', 'vs', 'Fig', 'Eq', 'Sec', 'cf', 'approx']
        protected = text
        for abbr in abbreviations:
            protected = protected.replace(f'{abbr}.', f'{abbr}DOTPROTECT')

        # Split on sentence boundaries: . ! ? followed by space and capital
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', protected)

        # Restore protected abbreviations
        sentences = [s.replace('DOTPROTECT', '.') for s in sentences]

        return [s.strip() for s in sentences if s.strip()]

    def _group_sentences_into_chunks(self, sentences: list[str]) -> list[str]:
        """
        Group sentences into chunks within [min_tokens, max_tokens].
        Apply overlap between chunks.
        """
        if not sentences:
            return []

        chunks = []
        current_sentences = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = self._count_tokens(sentence)

            # If adding this sentence would exceed max, finalize current chunk
            if current_tokens + sentence_tokens > self.config.max_tokens and current_sentences:
                chunk_text = ' '.join(current_sentences)
                chunks.append(chunk_text)

                # Overlap: keep last N tokens worth of sentences
                current_sentences, current_tokens = self._compute_overlap(current_sentences)

            current_sentences.append(sentence)
            current_tokens += sentence_tokens

        # Don't forget the last chunk
        if current_sentences:
            chunk_text = ' '.join(current_sentences)
            # Merge tiny final chunk into previous if too small
            if chunks and current_tokens < self.config.min_tokens // 2:
                chunks[-1] = chunks[-1] + ' ' + chunk_text
            else:
                chunks.append(chunk_text)

        return chunks

    def _compute_overlap(
        self, sentences: list[str]
    ) -> tuple[list[str], int]:
        """
        Return the tail sentences that fit within overlap_tokens.
        This becomes the start of the next chunk.
        """
        overlap_sentences = []
        overlap_tokens = 0

        for sentence in reversed(sentences):
            t = self._count_tokens(sentence)
            if overlap_tokens + t > self.config.overlap_tokens:
                break
            overlap_sentences.insert(0, sentence)
            overlap_tokens += t

        return overlap_sentences, overlap_tokens

    def _count_tokens(self, text: str) -> int:
        """
        Fast token count approximation: ~4 chars per token.
        Replace with tiktoken for exact counts if needed.
        """
        return max(1, len(text) // 4)

    def create_figure_chunk(
        self,
        figure_description: str,
        section_name: str,
        page: int,
        paper_id: str,
        chunk_index: int = 0,
    ) -> Chunk:
        """Create a chunk specifically for a figure description."""
        return Chunk(
            paper_id=paper_id,
            text=figure_description,
            section=section_name,
            page=page,
            paragraph=0,
            chunk_index=chunk_index,
            is_figure_description=True,
            token_count=self._count_tokens(figure_description),
        )