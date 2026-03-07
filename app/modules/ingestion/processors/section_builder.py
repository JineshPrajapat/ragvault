from collections import defaultdict
import re

class SectionBuilder:

    def build(self, elements, structure):

        sections = []
        current_section = {
            "chapter": None,
            "section": None,
            "content": [],
            "page_start": None
        }

        for el in elements:
            if self.is_heading(el):
                if current_section["content"]:
                    sections.append(self._finalize(current_section))

                current_section = {
                    "chapter": el["text"],
                    "section": None,
                    "content": [],
                    "page_start": el["page_number"]
                }

            else:
                current_section["content"].append(el["text"])

        if current_section["content"]:
            sections.append(self._finalize(current_section))

        return sections
    

    def _finalize(self, section):

        return {
            "chapter": section["chapter"],
            "section": section["section"],
            "text": " ".join(section["content"]),
            "page_start": section["page_start"]
        }
    

    def is_heading(self, element):

        text = element["text"]

        if element["type"] in ["title", "section_header", "header"]:
            return True

        if re.match(r"^\d+(\.\d+)*\s+[A-Z]", text):
            return True
        
        if len(text.split()) <= 2:
            return False

        if len(text) < 80 and text.isupper():
            return True

        return False