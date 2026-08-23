# Termwork Generator (for RNGPIT students only)

A web application that automatically generates termwork PDFs from student details for multiple practical titles.

The goal of this web-app is to eliminate the repetitive work of manually filling out termwork templates for every practical.

The application is lightweight and does not require a database for its core functionality.

This application is solely built for practical utility as a portfolio project demonstrating Flask, PDF processing, file handling, and to apply software development concepts to a practical problem and build a useful, real-world application.

Live application link: https://termwork-generator.onrender.com/

## Tech Stack

* **Python**
* **Flask** — Python Backend Framework
* **PyMuPDF** — PDF template processing
* **pypdf** — merging PDFs
* **HTML / CSS** — Frontend
* **Jinja2** — Flask templating engine
* **Bootstrap** — Responsive Design

## Project Structure

```text
termwork-generator/
│
├── app.py
├── requirements.txt
│
├── generators/
│   ├── generate.py
|   └── template.pdf
|
├── processors/
│   └── processor.py
|
├── utils/
|   └── utils.py
|
├── templates/
│   ├── base.html
│   ├── index.html
│   └── ...
│
├── static/
│   ├── styles/
│   │   └── styles.css
│   ├── images/...
│   └── scripts/...
│
└── ...
```

## How to run

### 1. Clone the repository

```bash
git clone https://github.com/sudopriyal/termwork-generator.git
cd termwork-generator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

## How to use

* Enter basic student details:
  * Name
  * PEN / Enrollment Number
  * Class
  * Semester
  * Subject
* Upload a PDF file containing Practicals serial number followed by the corresponding title in legible font ( Practical List / Index are viable ) OR
* Manually enter the titles of only those Practicals you want to include.
* The application then automatically fills the termwork PDF template (for RNGPIT only).
* It then generates termworks for multiple practicals at once, one pdf per termwork.
* Merges generated PDFs into a single downloadable PDF file that can be downloaded from the download page.

## Future Improvements

* Support multiple templates.
* Improve validation and error handling.

## Implemented improvements

* **File Input Support** — Allow users to upload a PDF file containing practical titles and automatically extract them into the generator eliminating manual input of titles individually.