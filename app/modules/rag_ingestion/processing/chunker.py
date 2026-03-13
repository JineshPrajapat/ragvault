import re


CHUNK_SIZE= 1800
CHUNK_OVERLAP = 300

class SemanticChunker:

    def chunk(self, text: str):

        sentences = re.split(r'(?<=[.!?]) +', text)

        chunks = []
        current = ""

        for sentence in sentences:

            if len(current) + len(sentence) < CHUNK_SIZE:
                current += " " + sentence

            else:
                chunks.append(current.strip())
                current = current[-CHUNK_OVERLAP:] + sentence

        if current:
            chunks.append(current.strip())

        return chunks