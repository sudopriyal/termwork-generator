import pymupdf
import re

def extract_titles_from_pdf(file):

    pdf_bytes = file.read()

    if not pdf_bytes:
        return []

    try:
        doc = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )
    except Exception:
        return []

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    titles = []
    current_title = None

    for line in lines:

        # Format 1:
        # 1
        # Write a program to...
        if re.fullmatch(r"\d+", line):

            if current_title:
                titles.append(current_title)

            current_title = ""
            continue

        # Format 2:
        # 1 Write a program to... CO1
        match = re.match(
            r"^(\d+)\s+(.+?)(?:\s+CO\d+)?$",
            line
        )

        if match:

            if current_title:
                titles.append(current_title)

            current_title = match.group(2).strip()
            continue

        # Continuation of the current title
        if current_title is not None:

            # Don't include CO numbers
            line = re.sub(
                r"\s+CO\d+$",
                "",
                line
            ).strip()

            if line:
                current_title += (
                    " " if current_title else ""
                ) + line

    # Save final title
    if current_title:
        titles.append(current_title)

    return titles[:15]