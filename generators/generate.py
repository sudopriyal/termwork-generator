import pymupdf
import os

def merge_pdfs(pdf_files, output_path):
    merged_doc = pymupdf.open()

    for pdf_file in pdf_files:
        doc = pymupdf.open(pdf_file)
        merged_doc.insert_pdf(doc)
        doc.close()

    merged_doc.save(output_path)
    merged_doc.close()


def generate_termworks_pdf(data_dict, file_id):

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    input_pdf = os.path.join(
        BASE_DIR,
        "generators",
        "template.pdf"
    )

    generated_dir = os.path.join(
        BASE_DIR,
        "generated"
    )

    os.makedirs(generated_dir, exist_ok=True)

    # L: x1-n x2-n
    # R: x1+n x2+n
    # U: y1-n y2-n
    # D: y1+n y2+n

    fields = {
        "term": (503, 219, 542, 235),
        "subject": (114, 243, 528, 259),
        "pen": (101, 267, 387, 283),
        "semester": (483, 267, 528, 283),
        "student_name": (160, 287, 527, 307),
        "class": (107, 311, 387, 327),
        "batch": (470, 311, 515, 327),
        "practical_title_fp": (283, 334, 529, 350),
        "practical_title_lp": (70, 359, 527, 375),
        "practical_no": (413, 415, 538, 437),
        "faculty_name": (141, 565, 529, 581),
    }

    generated_pdfs = []

    try:

        for practical_no, data in data_dict.items():

            output_pdf = os.path.join(
                generated_dir,
                f"{file_id}_practical_{practical_no}.pdf"
            )

            doc = pymupdf.open(input_pdf)

            page = doc[0]

            for field_name, coords in fields.items():

                rect = pymupdf.Rect(coords)
                value = str(data[field_name])

                print(f"{field_name}: {value}")

                page.insert_text(
                    (rect.x0, rect.y1 - 3),
                    value,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )

            doc.save(output_pdf)
            doc.close()

            generated_pdfs.append(output_pdf)

            print("PDF generated:", output_pdf)

        final_pdf = os.path.join(
            generated_dir,
            f"{file_id}_termwork.pdf"
        )

        merge_pdfs(
            generated_pdfs,
            final_pdf
        )

    finally:
        # Delete individual practical PDFs
        for pdf in generated_pdfs:
            os.remove(pdf)

        print("Final PDF generated:", final_pdf)

        return final_pdf
