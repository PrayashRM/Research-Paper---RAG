"""
PDF Parser — uses Marker for academic PDF parsing.
Marker is purpose-built for research papers (handles 2-column, math, tables).

Install: pip install marker-pdf
"""

import os
import re
from pathlib import Path
from typing import Optional
import uuid

from ...config.settings import ParserConfig
from ...utils.models import ParsedPaper, ParsedSection, ParsedFigure


class PDFParser:
    def __init__(self, config: ParserConfig):
        self.config = config
        self._section_pattern = re.compile(
            r'^(?:\d+\.?\s+)?([A-Z][A-Za-z\s\-]+)$',
            re.MULTILINE
        )

    def parse(self, pdf_path: str) -> ParsedPaper:
        """
        Main entry point. Parses a PDF into a structured ParsedPaper.
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        print(f"[Parser] Parsing: {path.name}")

        # Step 1: Extract raw markdown from PDF via Marker
        raw_markdown = self._extract_with_marker(pdf_path)

        # Step 2: Extract metadata (title, authors)
        title, authors = self._extract_metadata(raw_markdown)

        # Step 3: Split into sections
        sections = self._split_into_sections(raw_markdown)

        # Step 4: Filter — keep only relevant sections, drop noise sections
        sections = self._filter_sections(sections)

        paper_id = str(uuid.uuid4())

        print(f"[Parser] Extracted {len(sections)} sections from '{title}'")

        return ParsedPaper(
            paper_id=paper_id,
            title=title,
            authors=authors,
            sections=sections,
            total_pages=self._estimate_pages(raw_markdown),
            source_path=pdf_path,
        )

    def _extract_with_marker(self, pdf_path: str) -> str:
        """
        Use Marker to convert PDF → clean markdown.
        Marker handles: 2-column layout, equations, tables, figure captions.
        """
        try:
            from marker.convert import convert_single_pdf
            from marker.models import load_all_models

            models = load_all_models()
            full_text, _images, _metadata = convert_single_pdf(
                pdf_path,
                models,
                max_pages=None,
                langs=["English"],
                batch_multiplier=2,
            )
            return full_text

        except ImportError:
            print("[Parser] WARNING: Marker not installed. Falling back to pdfplumber.")
            return self._fallback_pdfplumber(pdf_path)

    def _fallback_pdfplumber(self, pdf_path: str) -> str:
        """
        Fallback parser using pdfplumber.
        Less accurate than Marker for complex layouts but always available.
        Install: pip install pdfplumber
        """
        try:
            import pdfplumber
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            return "\n\n".join(text_parts)

        except ImportError:
            raise ImportError(
                "No PDF parser available. "
                "Install marker-pdf: pip install marker-pdf  "
                "Or pdfplumber: pip install pdfplumber"
            )

    def _extract_metadata(self, text: str) -> tuple[str, list[str]]:
        """
        Extract title and authors from the beginning of the document.
        Heuristic: first non-empty line is usually the title.
        """
        lines = [l.strip() for l in text.split('\n') if l.strip()]

        title = lines[0] if lines else "Unknown Title"

        # Authors typically appear in lines 1-5, comma or newline separated
        # This is a heuristic — real papers vary a lot
        authors = []
        for line in lines[1:5]:
            if any(char.isdigit() for char in line):  # Skip affiliation lines
                continue
            if '@' in line:  # Skip email lines
                continue
            if len(line) > 150:  # Skip abstract-length lines
                break
            if line:
                authors.append(line)

        return title, authors

    def _split_into_sections(self, text: str) -> list[ParsedSection]:
        """
        Split document text into sections based on heading detection.
        Handles common academic paper heading formats.
        """
        # Heading patterns (order matters — most specific first)
        heading_patterns = [
            # "1. Introduction" or "1 Introduction"
            re.compile(r'^(\d+\.?\s+[A-Z][A-Za-z\s\-]+)$', re.MULTILINE),
            # "## Introduction" (Marker markdown headings)
            re.compile(r'^#{1,3}\s+(.+)$', re.MULTILINE),
            # "INTRODUCTION" (all caps)
            re.compile(r'^([A-Z]{3,}(?:\s+[A-Z]+)*)$', re.MULTILINE),
        ]

        # Find all section boundaries
        boundaries = []
        for pattern in heading_patterns:
            for match in pattern.finditer(text):
                heading_text = match.group(1) if match.lastindex else match.group(0)
                boundaries.append((match.start(), heading_text.strip()))

        # Sort by position
        boundaries.sort(key=lambda x: x[0])

        if not boundaries:
            # No sections detected — treat whole doc as one section
            return [ParsedSection(
                name="full_text",
                raw_text=text,
                page_start=1,
                page_end=1,
            )]

        sections = []
        for i, (start, heading) in enumerate(boundaries):
            end = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(text)
            section_text = text[start:end].strip()

            # Remove the heading line itself from the body text
            body_lines = section_text.split('\n')[1:]
            body_text = '\n'.join(body_lines).strip()

            if len(body_text) < 50:  # Skip near-empty sections
                continue

            sections.append(ParsedSection(
                name=self._normalize_section_name(heading),
                raw_text=body_text,
                page_start=self._estimate_page_number(start, text),
                page_end=self._estimate_page_number(end, text),
            ))

        return sections

    def _normalize_section_name(self, heading: str) -> str:
        """Normalize heading to lowercase standard form."""
        # Remove leading numbers: "3. Methodology" → "Methodology"
        heading = re.sub(r'^\d+\.?\s*', '', heading)
        return heading.strip().lower()

    def _filter_sections(self, sections: list[ParsedSection]) -> list[ParsedSection]:
        """
        Keep only sections in sections_to_keep.
        Drop sections in sections_to_drop.
        Unknown sections are kept by default (better to have more).
        """
        filtered = []
        for section in sections:
            name = section.name.lower()

            # Drop explicitly
            should_drop = any(
                drop_name in name
                for drop_name in self.config.sections_to_drop
            )
            if should_drop:
                print(f"[Parser] Dropping section: '{section.name}'")
                continue

            filtered.append(section)

        return filtered

    def _estimate_page_number(self, char_position: int, full_text: str) -> int:
        """
        Rough page estimate from character position.
        ~3000 chars per page is a reasonable academic paper estimate.
        """
        chars_per_page = 3000
        return max(1, char_position // chars_per_page + 1)

    def _estimate_pages(self, full_text: str) -> int:
        return max(1, len(full_text) // 3000)