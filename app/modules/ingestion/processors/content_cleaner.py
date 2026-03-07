import re


class ContentCleaner:

    """
    Normalize extracted text.
    """

    def clean(self, sections):

        cleaned_sections = []

        for section in sections:

            text = section.get("text", "")

            text = self._fix_hyphenation(text)
            text = self._normalize_spaces(text)
            text = self.remove_page_numbers(text)
            text = self.remove_headers_footers(text)

            section["text"] = text.strip()

            cleaned_sections.append(section)

        return cleaned_sections

    def _fix_hyphenation(self, text):
        return re.sub(r"-\n(\w+)", r"\1", text)

    def _normalize_spaces(self, text):
        text = re.sub(r"\n{2,}", "\n\n", text)
        text = re.sub(r"\s+", " ", text)
        return text
    
    def remove_page_numbers(self, text):

        text = re.sub(r'Page\s+\d+\s+of\s+\d+', '', text)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)

        return text
    
    def remove_headers_footers(self, text):

        lines = text.split("\n")

        cleaned = []

        for line in lines:
            if len(line) < 3:
                continue
            cleaned.append(line)

        return "\n".join(cleaned)