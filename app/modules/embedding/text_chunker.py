from typing import List, Dict


class TextChunker:
    """
    Responsible for splitting text into overlapping chunks.
    """

    def __init__(self, chunk_size: int = 800, overlap: int = 150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, pages: List[Dict]) -> List[Dict]:

        chunks = []
        chunk_index = 0

        for page in pages:
            text = page["text"]
            page_number = page["page_number"]

            start = 0
            text_length = len(text)

            while start < text_length:
                end = start + self.chunk_size
                chunk_text = text[start:end]

                chunks.append({
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                    "page_number": page_number
                })

                chunk_index += 1
                start += self.chunk_size - self.overlap

        return chunks