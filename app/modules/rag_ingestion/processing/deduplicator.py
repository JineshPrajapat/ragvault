from app.modules.rag_ingestion.utils.hashing import generate_hash


class Deduplicator:

    def __init__(self):
        self.seen = set()

    def is_duplicate(self, content: str):

        h = generate_hash(content)

        if h in self.seen:
            return True

        self.seen.add(h)
        return False