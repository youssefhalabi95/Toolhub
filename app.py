from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger
import os
import tkinter
from tkinter import filedialog, messagebox
from io import BytesIO
from zipfile import ZipFile

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/health")
def health():
    return "ToolHub is running"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/pdf-merge")
def pdf_merge_page():
    return render_template("pdf_merge.html")

@app.route("/merge-pdf", methods=["POST"])
def merge_pdf():

    pdf_files = request.files.getlist("pdfs")

    merger = PdfMerger()

    for pdf in pdf_files:

        filepath = os.path.join(UPLOAD_FOLDER, pdf.filename)

        pdf.save(filepath)

        merger.append(filepath)

    output_path = os.path.join(OUTPUT_FOLDER, "merged.pdf")

    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)

@app.route("/excel-cleanup")
def excel_cleanup_page():

    return render_template("Excel-Cleanup.html")

@app.route("/download-excel-cleanup")
def download_excel_cleanup():

    return send_file(
        "static/downloads/ExcelCleanup.zip",
        as_attachment=True
    )

@app.route("/file-organizer")
def organize_files ():

    return render_template("File-Organizer.html")

@app.route("/download-file-organizer")
def download_file_organizer ():

    return send_file(
        "static/downloads/File_Organizer_2.zip",
        as_attachment=True
    )

@app.route("/file-renamer")
def rename_files_page ():

    return render_template("File-Renamer.html")

@app.route("/file-renamer-tool", methods=["POST"])
def rename_files():

    uploaded_files = request.files.getlist("files")

    if not uploaded_files:
        return "No files uploaded."

    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, "w") as zip_file:

        counter = 1

        for file in uploaded_files:

            # Skip empty selections
            if file.filename == "":
                continue

            # Get original extension
            _, extension = os.path.splitext(file.filename)

            # New filename
            new_name = f"file_{counter}{extension}"

            # Read uploaded file content
            file_content = file.read()

            # Add renamed file to zip
            zip_file.writestr(new_name, file_content)

            counter += 1

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="renamed_files.zip",
        mimetype="application/zip"
    )


@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    print("New Contact Request")
    print("Name:", name)
    print("Email:", email)
    print("Message:", message)

    return "Request received successfully!"


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )