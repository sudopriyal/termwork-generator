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

def split_practical_title(title, max_chars_first=40, max_chars_second=60):

    if len(title) <= max_chars_first:
        return [title, ""]

    split_position = title.rfind(" ", 0, max_chars_first + 1)

    if split_position == -1:
        split_position = max_chars_first

    first_part = title[:split_position].strip()
    remaining = title[split_position:].strip()

    if len(remaining) > max_chars_second:
        second_part = remaining[:max_chars_second].strip()

        second_split = second_part.rfind(" ")

        if second_split != -1:
            second_part = second_part[:second_split].strip()
    else:
        second_part = remaining

    return [first_part, second_part]
