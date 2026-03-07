from keybert import KeyBERT
from typing import List, Dict


class KeywordExtractor:
    """
    Extract keywords for each chunk using KeyBERT.
    """

    def __init__(self):
        self.model = KeyBERT()

    def extract(self, sections: List[Dict]) -> List[Dict]:
        for section in sections:
            text = section.get("text")
            if not text:
                section["keywords"] = []
                continue

            keywords = self.model.extract_keywords(
                text,
                top_n=5
            )
            section["keywords"] = [k[0] for k in keywords]

        return sections