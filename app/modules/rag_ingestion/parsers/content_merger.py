class ContentMerger:

    def merge(self, text_pages, tables):

        page_map = {}

        for page in text_pages:

            page_map[page["page"]] = {
                "text": page["text"],
                "tables": []
            }

        for table in tables:

            page_map.setdefault(table["page"], {
                "text": "",
                "tables": []
            })

            page_map[table["page"]]["tables"].append(table["content"])

        merged_pages = []

        for page_num in sorted(page_map.keys()):

            page_data = page_map[page_num]

            content = page_data["text"]

            if page_data["tables"]:
                content += "\n\n" + "\n\n".join(page_data["tables"])

            merged_pages.append({
                "page": page_num,
                "content": content
            })

        return merged_pages