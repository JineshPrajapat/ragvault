import fitz
from pathlib import Path
from .base_loader import BaseLoader


class PDFLoader(BaseLoader):

    def load(self, file_path: str):

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")
        
        doc = fitz.open(file_path)

        # Word count per page
        words_per_page: list[int] = []
        for page in doc:
            words = page.get_text("words")
            words_per_page.append(len(words))

        total_words = sum(words_per_page)
        page_count  = len(doc)

        return {
            "file_path": file_path,
            "page_count": page_count,
            "total_words": total_words,
            "words_per_page": words_per_page,
            "avg_words_per_page": total_words / max(page_count, 1),
            "doc": doc,
            "page_count": len(doc),
            "toc": doc.get_toc()
        }