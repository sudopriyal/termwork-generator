from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from utils.utils import split_practical_title, create_filename
from generators.generate import generate_termworks_pdf
from processors.processor import extract_titles_from_pdf
import uuid

app = Flask(__name__)
app.secret_key = "dev-secret-key"

ALLOWED_EXTENSIONS = {"pdf"}

generated_files = {}

@app.route("/")
def homepage():
    return render_template(
       "index.html"
    )

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@app.route("/generate-termworks", methods=["GET", "POST"])
def generate_termworks():

    manual_entry=False

    if request.method == "POST":

        subject = request.form.get("subject", "").strip()
        pen = request.form.get("pen", "").strip()
        student_name = request.form.get("student_name", "").strip()
        class_name = request.form.get("class", "").strip()
        term = request.form.get("term", "").strip()
        semester = request.form.get("semester", "").strip()
        batch = request.form.get("batch", "").strip()
        faculty_name = request.form.get("faculty_name", "").strip()

        practical_dict = {
            str(i): title
            for i in range(1, 16)
            if (title := request.form.get(f"practical_{i}", "").strip())
        }

        manual_entry = request.form.get("manual_entry") == "manual"
        add_more = request.form.get("add_more") == "true"

        practical_file = request.files.get("practical_file")

        if not subject:
            flash("Please enter the subject name.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if not pen:
            flash("Please enter the PEN / enrollment number.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if not student_name:
            flash("Please enter the student's name.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if not class_name:
            flash("Please enter the class.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if not term:
            flash("Please enter the term.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if not semester:
            flash("Please select a semester.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if not batch:
            flash("Please enter the batch.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if not faculty_name:
            flash("Please enter the faculty name.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if semester not in {"1", "2", "3", "4", "5", "6", "7", "8"}:
            flash("Please select a valid semester.", "danger")
            return render_template(
                "generator.html",
                subject=subject,
                pen=pen,
                student_name=student_name,
                class_name=class_name,
                term=term,
                semester=semester,
                batch=batch,
                faculty_name=faculty_name,
                practical_dict=practical_dict,
                add_more=add_more,
                manual_entry=manual_entry,
            )

        if manual_entry:
            if not practical_dict:
                flash(
                    "Please enter at least one of the practical titles.",
                    "danger"
                )
                return render_template(
                    "generator.html",
                    subject=subject,
                    pen=pen,
                    student_name=student_name,
                    class_name=class_name,
                    term=term,
                    semester=semester,
                    batch=batch,
                    faculty_name=faculty_name,
                    practical_dict=practical_dict,
                    add_more=add_more,
                    manual_entry=manual_entry,
                )

        else:
            if not practical_file or not practical_file.filename:
                flash(
                    "Please upload a PDF containing the practical titles.",
                    "danger"
                )
                return render_template(
                    "generator.html",
                    subject=subject,
                    pen=pen,
                    student_name=student_name,
                    class_name=class_name,
                    term=term,
                    semester=semester,
                    batch=batch,
                    faculty_name=faculty_name,
                    practical_dict=practical_dict,
                    add_more=add_more,
                    manual_entry=manual_entry,
                )

            if not allowed_file(practical_file.filename):
                flash(
                    "Please upload a PDF file.",
                    "danger"
                )
                return render_template(
                    "generator.html",
                    subject=subject,
                    pen=pen,
                    student_name=student_name,
                    class_name=class_name,
                    term=term,
                    semester=semester,
                    batch=batch,
                    faculty_name=faculty_name,
                    practical_dict=practical_dict,
                    add_more=add_more,
                    manual_entry=manual_entry,
                )

            titles = extract_titles_from_pdf(practical_file)

            if not titles:
                flash(
                    "No practical titles could be found in the uploaded PDF.",
                    "danger"
                )
                return render_template(
                    "generator.html",
                    subject=subject,
                    pen=pen,
                    student_name=student_name,
                    class_name=class_name,
                    term=term,
                    semester=semester,
                    batch=batch,
                    faculty_name=faculty_name,
                    practical_dict={},
                    add_more=add_more,
                    manual_entry=manual_entry,
                )

            practical_dict = {
                str(i): title
                for i, title in enumerate(titles, start=1)
            }

        data_dict = {}

        for practical_no, title in practical_dict.items():
        
            first_part, last_part = split_practical_title(title)

            data_dict[practical_no] = {
                "term": term,
                "subject": subject,
                "pen": pen,
                "semester": semester,
                "student_name": student_name,
                "class": class_name,
                "batch": batch,
                "practical_title_fp": first_part,
                "practical_title_lp": last_part,
                "practical_no": practical_no,
                "faculty_name": faculty_name,
            }

        file_id = str(uuid.uuid4())

        final_pdf = generate_termworks_pdf(data_dict, file_id)

        filename = create_filename(subject, semester, pen)

        generated_files[file_id] = {
            "pdf_path": final_pdf,
            "filename": filename
        }

        return render_template(
            "generated.html",
            filename=filename,
            subject=subject,
            semester=semester,
            practical_count=len(data_dict),
            file_id=file_id,
        )

    return render_template(
        "generator.html",
        subject="",
        pen="",
        student_name="",
        class_name="",
        term="",
        semester="",
        batch="",
        faculty_name="",
        practical_dict={},
        add_more=False,
        manual_entry=False,
    )

@app.route("/download/<file_id>")
def download_pdf(file_id):

    file_data = generated_files.get(file_id)

    if not file_data:
        flash("This PDF is no longer available.", "danger")
        return redirect(url_for("generate_termworks"))

    response = send_file(
        file_data["pdf_path"],
        as_attachment=True,
        download_name=file_data["filename"],
        mimetype="application/pdf"
    )

    def cleanup():
        generated_files.pop(file_id, None)

    response.call_on_close(cleanup)

    return response

if __name__ == "__main__":
    app.run(debug=True)