class MarkdownBuilder:

    def build(self, sections):

        enriched = []

        for s in sections:

            md = ""

            if s["chapter"]:
                md += f"# {s['chapter']}\n\n"

            if s["section"]:
                md += f"## {s['section']}\n\n"

            md += s["text"]

            enriched.append({
                **s,
                "markdown": md
            })

        return enriched