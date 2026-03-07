from typing import List, Dict
import re
from collections import Counter


class StructureBuilder:

    def build(self, pages: List[Dict]) -> Dict:
        mode = self._detect_mode(pages)
        print("Detected document mode:", mode)

        if mode == "structured":
            return self._build_structured(pages)
        else:
            return self._build_generic(pages)

    # ----------------------------------------
    # MODE DETECTION
    # ----------------------------------------

    def _detect_mode(self, pages: List[Dict]) -> str:
        """
        Heuristics:
        - Large font variation
        - Numbered headings (1.1, 2.3)
        - 'Chapter' keyword
        """

        heading_patterns = 0
        font_sizes = []

        for page in pages[:20]:
            for block in page["blocks"]:
                text = block["text"]

                font_sizes.append(block.get("font_size", 0))

                if re.match(r"^Chapter\s+\d+", text):
                    heading_patterns += 2

                if re.match(r"^\d+\.\d+", text):
                    heading_patterns += 1

        font_variation = len(set(font_sizes)) > 3

        if heading_patterns > 3 and font_variation:
            return "structured"

        return "generic"

    # ----------------------------------------
    # MODE 1: STRUCTURED BOOK
    # ----------------------------------------

    def _build_structured(self, pages: List[Dict]) -> Dict:

        document = {
            "type": "structured_book",
            "chapters": []
        }

        current_chapter = None
        current_section = None

        body_font = self._detect_body_font_size(pages)

        for page in pages:
            for block in page["blocks"]:

                text = block["text"]
                font_size = block.get("font_size", body_font)

                # Chapter detection
                if self._is_chapter_heading(text, font_size, body_font):
                    current_chapter = {
                        "title": text,
                        "sections": [],
                        "page_start": page["page_number"]
                    }
                    document["chapters"].append(current_chapter)
                    current_section = None
                    continue

                # Section detection
                if self._is_section_heading(text, font_size, body_font):
                    if not current_chapter:
                        continue

                    current_section = {
                        "title": text,
                        "content": [],
                        "page_start": page["page_number"]
                    }
                    current_chapter["sections"].append(current_section)
                    continue

                # Normal paragraph
                if current_section:
                    current_section["content"].append({
                        "text": text,
                        "page": page["page_number"]
                    })
                elif current_chapter:
                    # paragraph before first section
                    current_chapter.setdefault("intro", []).append({
                        "text": text,
                        "page": page["page_number"]
                    })

        return document

    # ----------------------------------------
    # MODE 2: GENERIC DOCUMENT
    # ----------------------------------------

    def _build_generic(self, pages: List[Dict]) -> Dict:

        document = {
            "type": "generic_document",
            "sections": []
        }

        current_section = None

        for page in pages:
            for block in page["blocks"]:
                text = block["text"]

                # Try lightweight heading detection
                if self._looks_like_heading(text):
                    current_section = {
                        "title": text,
                        "content": [],
                        "page_start": page["page_number"]
                    }
                    document["sections"].append(current_section)
                    continue

                if not current_section:
                    current_section = {
                        "title": "Untitled Section",
                        "content": [],
                        "page_start": page["page_number"]
                    }
                    document["sections"].append(current_section)

                current_section["content"].append({
                    "text": text,
                    "page": page["page_number"]
                })

        return document

    # ----------------------------------------
    # Helpers
    # ----------------------------------------

    def _detect_body_font_size(self, pages):
        sizes = []

        for page in pages[:20]:
            for block in page["blocks"]:
                sizes.append(block.get("font_size", 0))

        return Counter(sizes).most_common(1)[0][0]

    def _is_chapter_heading(self, text, font_size, body_font):
        return (
            re.match(r"^Chapter\s+\d+", text)
            or (font_size > body_font + 2 and text.isupper())
        )

    def _is_section_heading(self, text, font_size, body_font):
        return (
            re.match(r"^\d+\.\d+", text)
            or font_size > body_font + 1
        )

    def _looks_like_heading(self, text):
        return (
            len(text) < 80
            and text.isupper()
        )