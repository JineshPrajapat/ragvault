import pdfplumber


class TableExtractor:

    def extract(self, pdf_path):

        tables = []

        with pdfplumber.open(pdf_path) as pdf:

            for page_number, page in enumerate(pdf.pages, start=1):

                extracted_tables = page.extract_tables()

                if not extracted_tables:
                    continue

                for table_index, table in enumerate(extracted_tables):

                    table_text = self.table_to_text(table)

                    if not table_text:
                        continue

                    tables.append({
                        "page": page_number,
                        "table_index": table_index,
                        "content": table_text
                    })

        return tables


    def sanitize_cell(self, cell):
        """Convert cell safely to text."""
        if cell is None:
            return ""
        return str(cell).strip()


    def table_to_text(self, table):

        if not table:
            return None

        rows = []

        for row in table:

            cleaned_row = [self.sanitize_cell(cell) for cell in row]

            if not any(cleaned_row):
                continue

            rows.append(" | ".join(cleaned_row))

        if not rows:
            return None

        return "\n".join(rows)