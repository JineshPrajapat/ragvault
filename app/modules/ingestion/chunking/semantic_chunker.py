import tiktoken
from .base_chunker import BaseChunker

class SemanticChunker(BaseChunker):
    """
    Token-based semantic chunker that preserves markdown, chapters, sections, keywords, and metadata.
    """

    def __init__(self, chunk_size=800, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def token_count(self, text: str) -> int:
        """Return the number of tokens in the text."""
        return len(self.encoder.encode(text))

    def chunk(self, sections: list) -> list:
        """
        Token-aware chunking.
        Each section can have markdown, chapter, section, page_number, keywords, meta.
        """
        chunks = []
        index = 0

        for section in sections:
            # Use markdown if available
            text = section.get("markdown") or section.get("text")
            if not text:
                continue

            tokens = self.encoder.encode(text)
            start = 0
            end = self.chunk_size

            while start < len(tokens):
                chunk_tokens = tokens[start:end]
                chunk_text = self.encoder.decode(chunk_tokens)

                # Prepare embedding-ready text
                embedding_text = f"""
Chapter: {section.get('chapter')}
Section: {section.get('section')}

{chunk_text}
"""

                chunks.append({
                    "chunk_index": index,
                    "text": embedding_text,
                    "content": chunk_text,
                    "page_number": section.get("page_start"),
                    "chapter_title": section.get("chapter"),
                    "section_title": section.get("section"),
                    "keywords": section.get("keywords"),
                    "meta": section.get("meta")
                })

                index += 1
                start = end - self.overlap
                end = start + self.chunk_size
                if end > len(tokens):
                    end = len(tokens)

        return chunks