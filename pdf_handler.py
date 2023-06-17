import os
import re
import shutil
import datetime
from PyPDF2 import PdfReader

# TODO: need to add if current month directory doesn't exist in filesystem, then create directory and place file in directory; also create additional appropriate new subdirs if necessary (ie: new companies, etc..)

# Invoices
def rename_and_move_pdf(file_name, source_dir, target_dir):
    # Get today's date and format it as MM-DD-YY
    today = datetime.date.today().strftime('%m-%d-%y')

    # Find the downloaded PDF
    for file in os.listdir(source_dir):
        if file.endswith('.pdf') and file_name in file:  # Adjust this as needed to match your file
            source_file = os.path.join(source_dir, file)
            # Rename file
            destination_file = os.path.join(target_dir, f'{today}.pdf')
            # Move the file
            print(f'Moving {destination_file} to {target_dir}')
            shutil.move(source_file, destination_file)
            break  # If you're only expecting one such file, you can break the loop after the first one found

# EFT Draft Notices - currently hardcoded for CVR EFT files only
def extract_content_from_pdf(file_path, target_company):
    """Read a PDF and return its content if it contains the target company"""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if target_company in text:
                return text
    return None


def extract_info(text):
    """Extract the specific information for CVR Supply"""
    lines = text.splitlines()
    eft_num_line = lines[1]
    eft_num = eft_num_line.split()[2]
    # date = eft_num_line.split()[3]
    today = datetime.date.today().strftime('%m-%d-%y')


    total_draft_line = [line for line in lines if 'Total Draft' in line][0]
    total_draft = re.findall(r'(\d+\.\d+)', total_draft_line)[0]

    return eft_num, today, total_draft


def rename_and_move_eft(file_name, source_dir, target_dir, target_company):
    """Find specific information in PDF files that contain the target company, rename and move the file"""
    for file in os.listdir(source_dir):
        if file.endswith('.pdf') and file_name in file:
            source_file = os.path.join(source_dir, file)

            text = extract_content_from_pdf(source_file, target_company)
            print(f'------------------------------- text: {text}------------------------------\n')
            if text:
                eft_num, today, total_draft = extract_info(text)
                new_file_name = f'{eft_num}-{today}-{total_draft}.pdf'
                destination_file = os.path.join(target_dir, new_file_name)

                print(f'Moving {source_file} to {destination_file}')
                shutil.move(source_file, destination_file)
