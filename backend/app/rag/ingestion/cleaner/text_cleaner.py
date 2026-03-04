"""
Text cleaner for research paper content.
Rule-based, deterministic — no LLM involved.
Runs between PDF parsing and chunking.
"""

import re
from dataclasses import dataclass
from ..config.settings import CleanerConfig


class TextCleaner:
    def __init__(self, config: CleanerConfig):
        self.config = config

        # Pre-compile all regex patterns for performance
        self._patterns = self._build_patterns()

    def _build_patterns(self) -> list[tuple[str, re.Pattern, str]]:
        """
        Returns list of (name, pattern, replacement) tuples.
        Each applied conditionally based on config flags.
        """
        patterns = []

        if self.config.remove_inline_citations:
            patterns += [
                # (Smith et al., 2021) or (Smith & Jones, 2020)
                ("citation_author_year",
                 re.compile(r'\([A-Z][a-zA-Z\s\-]+(?:et al\.?|&[^)]+)?,?\s*\d{4}[a-z]?\)'),
                 ""),
                # [14] or [1, 2, 3] or [1-3]
                ("citation_numeric",
                 re.compile(r'\[\d+(?:[,\-]\s*\d+)*\]'),
                 ""),
                # Superscript-style: word¹ or word^1
                ("citation_superscript",
                 re.compile(r'(?<=\w)[¹²³⁴⁵⁶⁷⁸⁹⁰]+'),
                 ""),
            ]

        if self.config.remove_latex_commands:
            patterns += [
                # \cite{key}, \citep{key}, \citet{key}
                ("latex_cite",
                 re.compile(r'\\cite[pt]?\{[^}]*\}'),
                 ""),
                # \ref{label}, \label{name}, \eqref{eq}
                ("latex_ref",
                 re.compile(r'\\(?:ref|label|eqref|autoref)\{[^}]*\}'),
                 ""),
                # \footnote{text}
                ("latex_footnote",
                 re.compile(r'\\footnote\{[^}]*\}'),
                 ""),
                # Leftover LaTeX commands like \textbf{} → keep content
                ("latex_textbf",
                 re.compile(r'\\text(?:bf|it|rm|sf|tt)\{([^}]*)\}'),
                 r'\1'),
            ]

        if self.config.remove_urls:
            patterns += [
                ("urls",
                 re.compile(r'https?://\S+|www\.\S+'),
                 ""),
            ]

        if self.config.remove_dois:
            patterns += [
                ("dois",
                 re.compile(r'\bdoi:\s*10\.\d{4,}/\S+', re.IGNORECASE),
                 ""),
                ("arxiv_ids",
                 re.compile(r'\barXiv:\s*\d{4}\.\d{4,5}(?:v\d+)?', re.IGNORECASE),
                 ""),
            ]

        if self.config.remove_figure_refs:
            patterns += [
                # (see Figure 3), (Figure 3), (Fig. 3a), (Table 2)
                ("figure_table_refs",
                 re.compile(
                     r'\((?:see\s+)?(?:Figure|Fig\.?|Table|Eq\.?|Equation)\s*\d+[a-zA-Z]?\)',
                     re.IGNORECASE
                 ),
                 ""),
            ]

        if self.config.remove_org_sentences:
            patterns += [
                # "The rest of this paper is organized as follows..."
                ("org_sentences",
                 re.compile(
                     r'(?:The rest of this paper|This paper is organized|'
                     r'The remainder of this paper|In the rest of this paper|'
                     r'The paper is structured|This work is organized)[^.]+\.',
                     re.IGNORECASE
                 ),
                 ""),
            ]

        # Always clean these regardless of config
        patterns += [
            # Empty parentheses left after citation removal: (, ) or ( , )
            ("empty_parens",
             re.compile(r'\(\s*,?\s*\)'),
             ""),
            # Empty brackets
            ("empty_brackets",
             re.compile(r'\[\s*\]'),
             ""),
            # Multiple spaces → single space
            ("multi_space",
             re.compile(r' {2,}'),
             " "),
            # Space before punctuation
            ("space_before_punct",
             re.compile(r'\s+([,\.;:])'),
             r'\1'),
            # Multiple newlines → max two
            ("multi_newline",
             re.compile(r'\n{3,}'),
             "\n\n"),
        ]

        return patterns

    def clean(self, text: str) -> tuple[str, bool]:
        """
        Clean a block of text.

        Returns:
            (cleaned_text, had_citations)
            had_citations: True if inline citations were present before removal.
                           Stored in chunk metadata for retrieval hints.
        """
        had_citations = False

        if self.config.remove_inline_citations:
            # Check BEFORE removing
            citation_check = re.search(
                r'\[[0-9]+\]|\([A-Z][a-zA-Z]+.*?\d{4}\)', text
            )
            had_citations = citation_check is not None

        for _name, pattern, replacement in self._patterns:
            text = pattern.sub(replacement, text)

        return text.strip(), had_citations

    def clean_section(self, section_text: str) -> tuple[str, bool]:
        """Convenience wrapper for full section text."""
        return self.clean(section_text)