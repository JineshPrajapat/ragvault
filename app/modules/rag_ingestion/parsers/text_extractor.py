import fitz
from app.modules.rag_ingestion.processing.cleaner import TextCleaner


class TextExtractor:

    def __init__(self):
        self.cleaner = TextCleaner()

    def extract(self, pdf_path):

        doc = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(doc, start=1):

            text = page.get_text()

            cleaned = self.cleaner.clean(text)

            if cleaned:

                pages.append({
                    "page": page_number,
                    "text": cleaned
                })

        doc.close()

        return pages