import os
import glob
import subprocess
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO

def get_files_with_identifiers(path, ID, jobID):
    # Define primary patterns and fallback pattern for .3553.pdf
    primary_patterns = [
        f"RPT0000000{ID}.isr.pdf",
        f"RPT00000000{jobID}.ps.pdf",
        f"RPT00000000{jobID}.3600.pdf",
        f"RPT00000000{jobID}.3600.pdf",
        f"RPT00000000{jobID}.3600.pdf",
        f"RPT00000000{jobID}.qual.pdf"
    ]
    
    # Adding .3553.pdf and .ncoa.pdf with a fallback mechanism
    optional_patterns = [f"RPT0000000{ID}.3553.pdf", f"RPT0000000{ID}.ncoa.pdf"]

    files = []
    # Add all primary pattern files
    for pattern in primary_patterns:
        files.extend(glob.glob(os.path.join(path, pattern)))

    # Check for either .3553.pdf or .ncoa.pdf
    found_optional_file = False
    for pattern in optional_patterns:
        matched_files = glob.glob(os.path.join(path, pattern))
        if matched_files:
            files.extend(matched_files)
            found_optional_file = True
            break  # Stop once we find either .3553.pdf or .ncoa.pdf

    return files, primary_patterns + (optional_patterns if not found_optional_file else [])

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

def merge_pdfs(input_files, patterns, output_file, folder_path):
    missing_files = [pattern for pattern in patterns if not any(glob.glob(os.path.join(folder_path, pattern)))]
    if not missing_files:
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
        return f"PDF files merged successfully into '{output_file}'."
    else:
        return f"Error: 1 or more files missing ({', '.join(missing_files)})"

def combine_reports(ID, jobID, folder_path):
    files_with_identifiers, patterns = get_files_with_identifiers(folder_path, ID, jobID)
    if files_with_identifiers:
        output_pdf_filename = os.path.join(folder_path, f"Combined_{ID}_{jobID}.pdf")
        result = merge_pdfs(files_with_identifiers, patterns, output_pdf_filename, folder_path)
        return result
    else:
        return "No matching files found with the specified identifiers."
