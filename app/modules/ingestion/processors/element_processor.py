class ElementProcessor:

    def process(self, elements):

        processed = []

        for el in elements:

            t = el["type"]
            text = el["text"]

            if t == "table":

                processed.append({
                    "type": "table",
                    "text": f"Table Data:\n{text}",
                    "page_number": el["page_number"]
                })

            elif t == "figure":

                processed.append({
                    "type": "figure",
                    "text": f"Figure Description:\n{text}",
                    "page_number": el["page_number"]
                })

            elif t == "list":

                processed.append({
                    "type": "list",
                    "text": text,
                    "page_number": el["page_number"]
                })

            else:

                processed.append(el)

        return processed