import fitz


class ImageExtractor:

    def extract(self, pdf_path):

        doc = fitz.open(pdf_path)

        images = []

        for page_number, page in enumerate(doc, start=1):

            for img_index, img in enumerate(page.get_images(full=True)):

                xref = img[0]

                base = doc.extract_image(xref)

                images.append({
                    "page": page_number,
                    "image_index": img_index,
                    "content": base["image"]
                })

        doc.close()

        return images