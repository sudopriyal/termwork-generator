from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from utils.utils import split_practical_title, create_filename
from generators.generate import generate_termworks_pdf
import uuid

app = Flask(__name__)
app.secret_key = "dev-secret-key"

generated_files = {}

@app.route("/")
def homepage():
    return render_template(
       "index.html"
    )

@app.route("/generate-termworks", methods=["GET", "POST"])
def generate_termworks():

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

        add_more = request.form.get("add_more") == "true"

        # print("\n========== FORM DATA ==========")
        # print(request.form)
        # print("\n========== PRACTICAL DICT ==========")
        # print(practical_dict)
        # print("\n========== CHECKBOXES ==========")
        # print("add_more:", add_more)
        # print("================================\n")

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
            )

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
            )

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

        temp_dir, final_pdf = generate_termworks_pdf(data_dict)

        file_id = str(uuid.uuid4())

        filename = create_filename(subject, semester, pen)

        generated_files[file_id] = {
            "temp_dir": temp_dir,
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
        file_data["temp_dir"].cleanup()
        generated_files.pop(file_id, None)

    response.call_on_close(cleanup)

    return response

if __name__ == "__main__":
    app.run(debug=True)