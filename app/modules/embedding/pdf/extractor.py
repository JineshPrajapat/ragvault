# app/modules/embedding/pdf/extractor.py

from typing import List, Dict
import fitz


class PDFExtractor:
    """
    Extracts structured block-level text from digital PDFs.
    """

    def extract(self, file_path: str) -> List[Dict]:
        doc = fitz.open(file_path)
        toc = doc.get_toc()

        pages = []
        for page_index, page in enumerate(doc):
            blocks = page.get_text("blocks")
            structured_blocks = []

            chapter_title = None
            section_title = None

            for block in blocks:
                x0, y0, x1, y1, text, *_ = block

                clean_text = text.strip()
                if not clean_text:
                    continue

                structured_blocks.append({
                    "bbox": (x0, y0, x1, y1),
                    "text": clean_text
                })

            
                for entry in toc:
                    level, title, toc_page = entry
                    if toc_page - 1 <= page_index:
                        if level == 1:
                            chapter_title = title
                        elif level == 2:
                            section_title = title

            pages.append({
                "page_number": page_index + 1,
                "blocks": structured_blocks,
                "chapter_title": chapter_title,
                "section_title": section_title,
                "keywords": [],   # placeholder, can be added with NLP
                "meta": {"source": file_path}
            })
        return pages
