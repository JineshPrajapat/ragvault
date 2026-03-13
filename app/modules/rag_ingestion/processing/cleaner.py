import re


class TextCleaner:

    def clean(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = text.replace("\x00", "")
        return text.strip()