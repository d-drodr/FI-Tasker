import os
import glob
import subprocess
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO

def get_files_with_identifiers(path, ID, jobID):
    patterns = [
        f"RPT0000000{ID}.isr.pdf",
        f"RPT00000000{jobID}.ps.pdf",
        f"RPT00000000{jobID}.3600.pdf",
        f"RPT00000000{jobID}.3600.pdf",
        f"RPT00000000{jobID}.3600.pdf",
        f"RPT00000000{jobID}.qual.pdf",
        f"RPT0000000{ID}.3553.pdf"
    ]

    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(path, pattern)))
    return files

def remove_last_page(input_pdf):
    reader = PdfReader(input_pdf)
    if len(reader.pages) > 1:
        writer = PdfWriter()
        for page in reader.pages[:-1]:
            writer.add_page(page)
        output_stream = BytesIO()
        writer.write(output_stream)
        return output_stream
    else:
        return open(input_pdf, 'rb')

def merge_pdfs(input_files, output_file):
    if all(os.path.exists(file) for file in input_files):
        merger = PdfMerger()
        for file in input_files:
            pdf_without_last_page = remove_last_page(file)
            merger.append(pdf_without_last_page)

        with open(output_file, 'wb') as output_pdf:
            merger.write(output_pdf)
        
        # Automatically open the generated PDF file
        if os.name == 'nt':  # for Windows
            os.startfile(output_file)
        elif os.name == 'posix':  # for macOS and Linux
            subprocess.call(('open', output_file) if sys.platform == 'darwin' else ('xdg-open', output_file))
    else:
        print("One or more files are missing. Please check the file paths and try again.")

def combine_reports(ID, jobID, folder_path):
    files_with_identifiers = get_files_with_identifiers(folder_path, ID, jobID)
    if files_with_identifiers:
        output_pdf_filename = os.path.join(folder_path, f"Combined_{ID}_{jobID}.pdf")
        merge_pdfs(files_with_identifiers, output_pdf_filename)
        return f"PDF files merged successfully into '{output_pdf_filename}'."
    else:
        return "No matching files found with the specified identifiers."
