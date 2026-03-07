from .base_chunker import BaseChunker


class TOCChunker(BaseChunker):

    """
    Uses Table of Contents to create context aware chunks.
    """

    def chunk(self, document):

        chunks = []
        toc = document["toc"]

        for section in document["sections"]:

            text = section["text"]
            page = section["page"]

            chunks.append({
                "text": text,
                "page": page,
                "section": self._match_section(toc, page)
            })

        return chunks

    def _match_section(self, toc, page):

        if not toc:
            return None

        current = None

        for level, title, toc_page in toc:

            if toc_page <= page:
                current = title
            else:
                break

        return current