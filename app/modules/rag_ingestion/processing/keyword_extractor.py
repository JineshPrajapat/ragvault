import re
from collections import Counter


KEYWORD_TOP_K = 5

STOPWORDS = {
"a","an","the","is","are","was","were","in","on","at","of","and","or",
"to","for","with","by","as","from","that","this","it","be","can","will"
}


class KeywordExtractor:

    def extract(self, text):

        text = text.lower()

        words = re.findall(r"\b[a-zA-Z]{3,}\b", text)

        words = [w for w in words if w not in STOPWORDS]

        freq = Counter(words)

        return [w for w, _ in freq.most_common(KEYWORD_TOP_K)]