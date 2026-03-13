from app.modules.rag_ingestion.parsers.text_extractor import TextExtractor
from app.modules.rag_ingestion.parsers.image_extractor import ImageExtractor
from app.modules.rag_ingestion.parsers.table_extractor import TableExtractor
from pathlib import Path


class PDFParser:

    def __init__(self):

        self.text_extractor = TextExtractor()
        self.image_extractor = ImageExtractor()
        self.table_extractor = TableExtractor()

    def parse(self, pdf_path):

        pdf_path = Path(pdf_path).resolve()
        print("path:",pdf_path)

        text = self.text_extractor.extract(pdf_path)

        images = self.image_extractor.extract(pdf_path)

        tables = self.table_extractor.extract(pdf_path)

        return {
            "text": text,
            "images": images,
            "tables": tables
        }