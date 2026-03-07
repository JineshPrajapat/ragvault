class MetadataBuilder:

    def build(self, sections):

        enriched = []

        for section in sections:

            enriched.append({
                **section,
                "meta": {
                    "page_start": section.get("page_start"),
                    "section_title": section.get("title"),
                    "source": "pdf"
                }
            })

        return enriched