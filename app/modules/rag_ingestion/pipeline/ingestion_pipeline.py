import uuid
from app.modules.rag_ingestion.parsers.pdf_parser import PDFParser
from app.modules.rag_ingestion.processing.chunker import SemanticChunker
from app.modules.rag_ingestion.processing.keyword_extractor import KeywordExtractor
from app.modules.rag_ingestion.processing.deduplicator import Deduplicator
from app.modules.rag_ingestion.parsers.content_merger import ContentMerger
from app.modules.rag_ingestion.parsers.chunk_enricher import ChunkEnricher

class IngestionPipeline:

    def __init__(self):

        self.parser = PDFParser()
        self.chunker = SemanticChunker()
        self.keyword_extractor = KeywordExtractor()
        self.deduplicator = Deduplicator()
        self.merger = ContentMerger()
        self.enricher = ChunkEnricher()

    def run(self, pdf_path):

        parsed = self.parser.parse(pdf_path)

        merged_pages = self.merger.merge(
            parsed["text"],
            parsed["tables"]
        )

        text_elements = []
        chunk_index = 0

        for page in merged_pages:

            chunks = self.chunker.chunk(page["content"])

            for chunk in chunks:

                if self.deduplicator.is_duplicate(chunk):
                    continue

                keywords = self.keyword_extractor.extract(chunk)

                enriched_text = self.enricher.enrich(
                    chunk,
                    page["page"],
                    keywords
                )

                text_elements.append({
                    "id": str(uuid.uuid4()),
                    "type": "text",
                    "chunk_index": chunk_index,
                    "content": enriched_text,
                    "metadata": {
                        "page": page["page"],
                        "keywords": keywords
                    }
                })

                chunk_index += 1

        return {
            "text": text_elements,
            "images": parsed.get("images", []),
            "tables":parsed.get("tables", [])
        }