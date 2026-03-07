from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import ConversionStatus
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    PdfFormatOption
)

from pathlib import Path


class DoclingExtractor:

    def __init__(self):
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False            # disable OCR if text exists
        pipeline_options.do_table_structure = True
        pipeline_options.generate_page_images = False
        pipeline_options.generate_picture_images = False
        pipeline_options.images_scale = 0.5

        self._converter = DocumentConverter(format_options={
                "pdf": PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            })

    def extract(self, document: dict):

        elements = []

        try:
            file_path = Path(document["file_path"])

            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            result = self._converter.convert(file_path)

            if result.status not in {ConversionStatus.SUCCESS, ConversionStatus.PARTIAL_SUCCESS}:
                raise RuntimeError( f"Docling conversion failed with status: {result.status}")
            
            if result.status == ConversionStatus.PARTIAL_SUCCESS:
                print(
                    f"Partial conversion for {file_path.name} — some pages may be missing"
                )
            
            if not result.document:
                raise RuntimeError("Docling returned empty document")
            
            doc = result.document

            extracted_pages = len(doc.pages)
            missing_pages = list(range(extracted_pages + 1, document.get("page_count", 0) +1))
            print("missing pages", missing_pages)
            

            for item in doc.texts:

                try:
                    # Extract text safely
                    text = getattr(item, "text", None)

                    if not text:
                        continue

                    text = text.strip()

                    if not text:
                        continue

                    # Extract label safely
                    label = getattr(item, "label", "text")
                    level = getattr(item, "level", None)

                    # Extract page number safely
                    page_number = 1
                    prov = getattr(item, "prov", None)

                    if prov and len(prov) > 0:
                        page_number = getattr(prov[0], "page_no", 1)

                    elements.append({
                        "type": label,
                        "text": text,
                        "page_number": page_number,
                        "level": level,
                    })

                    print("extracted text element lenght", len(elements))

                except Exception as element_error:
                    print(f"Skipping corrupted element: {element_error}")
                    continue

            for table in doc.tables:
                table_text = table.export_to_markdown()
                elements.append({
                    "type": "table",
                    "text": table_text,
                    "page_number": table.prov[0].page_no
                })

        except Exception as e:

            print(f"Docling extraction failed: {e}")

            return []

        return elements





# import fitz
# import pdfplumber
# from pathlib import Path


# class DoclingExtractor:

#     def __init__(self):
#         pass


#     def _detect_heading(self, spans):
#         """
#         Detect heading based on font size.
#         """
#         if not spans:
#             return "text", None

#         max_size = max(span.get("size", 0) for span in spans)

#         if max_size >= 18:
#             return "heading", 1
#         elif max_size >= 15:
#             return "heading", 2
#         elif max_size >= 13:
#             return "heading", 3

#         return "text", None


#     def _extract_text_blocks(self, page, page_number):
#         """
#         Extract structured text blocks using PyMuPDF.
#         """
#         elements = []

#         try:
#             blocks = page.get_text("dict").get("blocks", [])

#             for block in blocks:

#                 if "lines" not in block:
#                     continue

#                 spans = []
#                 text_parts = []

#                 for line in block["lines"]:
#                     for span in line["spans"]:
#                         text = span.get("text", "").strip()

#                         if not text:
#                             continue

#                         spans.append(span)
#                         text_parts.append(text)

#                 text = " ".join(text_parts).strip()

#                 if not text:
#                     continue

#                 label, level = self._detect_heading(spans)

#                 elements.append({
#                     "type": label,
#                     "text": text,
#                     "page_number": page_number,
#                     "level": level
#                 })

#         except Exception as e:
#             print(f"Text extraction error on page {page_number}: {e}")

#         return elements


#     def _extract_tables(self, file_path):
#         """
#         Extract tables using pdfplumber and convert to markdown.
#         """
#         elements = []

#         try:
#             with pdfplumber.open(file_path) as pdf:

#                 for page_index, page in enumerate(pdf.pages):

#                     tables = page.extract_tables()

#                     if not tables:
#                         continue

#                     for table in tables:

#                         rows = []
#                         for row in table:
#                             cleaned = [
#                                 (cell or "").replace("\n", " ").strip()
#                                 for cell in row
#                             ]
#                             rows.append(cleaned)

#                         if not rows:
#                             continue

#                         header = rows[0]
#                         body = rows[1:]

#                         markdown = "| " + " | ".join(header) + " |\n"
#                         markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"

#                         for r in body:
#                             markdown += "| " + " | ".join(r) + " |\n"

#                         elements.append({
#                             "type": "table",
#                             "text": markdown.strip(),
#                             "page_number": page_index + 1,
#                             "level": None
#                         })

#         except Exception as e:
#             print(f"Table extraction failed: {e}")

#         return elements


#     def extract(self, document: dict):

#         elements = []

#         try:

#             file_path = Path(document["file_path"])

#             if not file_path.exists():
#                 raise FileNotFoundError(f"File not found: {file_path}")

#             pdf = fitz.open(file_path)

#             for page_index in range(len(pdf)):

#                 page = pdf.load_page(page_index)

#                 page_number = page_index + 1

#                 page_elements = self._extract_text_blocks(page, page_number)

#                 elements.extend(page_elements)

#             pdf.close()

#             # Extract tables separately
#             table_elements = self._extract_tables(file_path)

#             elements.extend(table_elements)

#         except Exception as e:

#             print(f"Extraction failed: {e}")

#             return []

#         print("Total extracted elements:", len(elements))

#         return elements