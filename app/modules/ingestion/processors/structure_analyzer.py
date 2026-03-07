class StructureAnalyzer:

    def analyze(self, document, layout):

        toc = document.get("toc")

        headings = [e for e in layout if "header" in str(e["type"]).lower()]

        return {
            "toc": toc,
            "has_headings": len(headings) > 0
        }