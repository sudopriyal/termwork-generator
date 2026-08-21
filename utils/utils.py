def create_filename(subject, semester, pen):
    subject = "".join(
        char if char.isalnum() or char == " " else ""
        for char in subject
    )

    semester = "".join(
        char if char.isalnum() else ""
        for char in semester
    )

    pen = "".join(
        char if char.isalnum() else ""
        for char in pen
    )

    subject = "_".join(subject.split())

    return f"{subject}_Sem{semester}_{pen}_Termwork.pdf"

def split_practical_title(title, max_chars=40):

    if len(title) <= max_chars:
        return [title, ""]

    split_position = title.rfind(" ", 0, max_chars + 1)

    if split_position == -1:
        split_position = max_chars

    first_part = title[:split_position].strip()
    last_part = title[split_position:].strip()

    return [first_part, last_part]