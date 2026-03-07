# app/modules/embedding/pdf/processor.py

from typing import List, Dict

from app.modules.ingestion.processors.keyword_extractor import KeywordExtractor
from .extractor import PDFExtractor
from .cleaner import PDFCleaner


class PDFProcessor:
    """
    Phase 1 Processor:
    Extract + Clean
    """

    def __init__(self):
        self.extractor = PDFExtractor()
        self.cleaner = PDFCleaner()
        self.keyword_extractor = KeywordExtractor()

    def process(self, file_path: str) -> List[Dict]:
        raw_pages = self.extractor.extract(file_path)
        cleaned_pages = self.cleaner.clean(raw_pages)
        enriched_pages = self.keyword_extractor.extract(cleaned_pages)
        
        chunks = []
        for i, page in enumerate(enriched_pages):
            chunk = {
                "chunk_index": i,
                "text": page["text"],
                "page_number": page["page_number"],
                "chapter_title": page.get("chapter_title", ""),
                "section_title": page.get("section_title", ""),
                "keywords": page.get("keywords", []),
                "meta": page.get("meta", {}),
            }
            chunks.append(chunk)
        print("procesed chunks", chunks[4])
        return chunks