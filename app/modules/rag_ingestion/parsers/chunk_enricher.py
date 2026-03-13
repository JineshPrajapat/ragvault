class ChunkEnricher:

    def enrich(self, chunk, page, keywords):

        keyword_text = ", ".join(keywords)

        enriched = f"""Page: {page}
Keywords: {keyword_text}

{chunk}
"""

        return enriched