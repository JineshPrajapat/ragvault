# app/modules/embedding/pdf/cleaner.py

import re
from collections import Counter
from typing import List, Dict


class PDFCleaner:
    """
    Cleans extracted PDF pages:
    - Removes repeated headers/footers
    - Fixes hyphenation
    - Removes page numbers
    - Normalizes whitespace
    """

    def clean(self, pages: List[Dict]) -> List[Dict]:
        header_footer_candidates = self._detect_repeated_lines(pages)

        cleaned_pages = []

        for page in pages:
            lines = []

            for block in page["blocks"]:
                text = block["text"]

                if text in header_footer_candidates:
                    continue

                if self._is_page_number(text):
                    continue

                lines.append(text)

            merged_text = "\n".join(lines)
            merged_text = self._fix_hyphenation(merged_text)
            merged_text = self._normalize_paragraphs(merged_text)

            cleaned_pages.append({
                "page_number": page["page_number"],
                "text": merged_text.strip(),
                "chapter_title": page.get("chapter_title"),
                "section_title": page.get("section_title"),
                "keywords": page.get("keywords", []),
                "meta": page.get("meta", {}),
            })

        return cleaned_pages

    # -------------------------
    # Helpers
    # -------------------------

    def _detect_repeated_lines(self, pages: List[Dict]) -> set:
        """
        Detect repeated header/footer lines across pages.
        """
        counter = Counter()

        sample_pages = pages[: min(len(pages), 30)]

        for page in sample_pages:
            for block in page["blocks"]:
                text = block["text"].strip()
                if len(text) < 3:
                    continue
                counter[text] += 1

        repeated = {
            line for line, count in counter.items()
            if count > len(sample_pages) * 0.6
        }

        return repeated

    def _is_page_number(self, text: str) -> bool:
        return bool(re.fullmatch(r"(Page\s*)?\d+", text.strip()))

    def _fix_hyphenation(self, text: str) -> str:
        # Fix word breaks across lines
        text = re.sub(r"-\n(\w+)", r"\1", text)
        return text

    def _normalize_paragraphs(self, text: str) -> str:
        # Merge broken lines but keep paragraph breaks
        text = re.sub(r"\n{2,}", "\n\n", text)
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
        return text.strip()