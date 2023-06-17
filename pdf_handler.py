import os
import re
import shutil
import datetime
from PyPDF2 import PdfReader

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
# def extract_content_from_pdf(file_path, target_company):
#     """Read a PDF and return its content if it contains the target company"""
#     with open(file_path, 'rb') as f:
#         reader = PdfReader(f)
#         for page in reader.pages:
#             text = page.extract_text()
#             if target_company in text:
#                 return text
#     return None
#
#
# def extract_info(text):
#     """Extract the specific information for CVR Supply"""
#     lines = text.splitlines()
#     eft_num_line = lines[1]
#     eft_num = eft_num_line.split()[2]
#     today = datetime.date.today().strftime('%m-%d-%y')
#
#     total_draft_line = [line for line in lines if 'Total Draft' in line][0]
#     total_draft = re.findall(r'(\d+\.\d+)', total_draft_line)[0]
#
#     return eft_num, today, total_draft
#
#
# def rename_and_move_eft(file_name, source_dir, target_dir, target_company):
#     """Find specific information in PDF files that contain the target company, rename and move the file"""
#     for file in os.listdir(source_dir):
#         if file.endswith('.pdf') and file_name in file:
#             source_file = os.path.join(source_dir, file)

            text = extract_content_from_pdf(source_file, target_company)
            if text:
                eft_num, today, total_draft = extract_info(text)
                new_file_name = f'{eft_num}-{today}-{total_draft}.pdf'
                destination_file = os.path.join(target_dir, new_file_name)

                print(f'Moving {source_file} to {destination_file}')
                shutil.move(source_file, destination_file)


# --------------- TEST ------------------------------
def get_target_directories(parent_dir, company_keyword_mapping):
    target_directories = {}
    subdirs = os.listdir(parent_dir)
    for company, keyword in company_keyword_mapping.items():
        company_lower = company.lower()
        for subdir in subdirs:
            if company_lower in subdir.lower():
                full_path = os.path.join(parent_dir, subdir)
                target_directories[company] = full_path
    return target_directories

def extract_info_from_page(page, target_keyword):
    """Extract the specific information from a page"""
    text = page.extract_text()
    lines = text.splitlines()
    eft_num_line = lines[1]
    eft_num = eft_num_line.split()[2]
    today = datetime.date.today().strftime('%m-%d-%y')

    total_draft_line = [line for line in lines if target_keyword in line][0]
    total_draft = re.findall(r'(\d+\.\d+)', total_draft_line)[0]

    return eft_num, today, total_draft


def process_pdf(file_name, source_dir, company_subdir_mapping, mapping):
    """Process a PDF file, extract info from pages that contain target company and move to target dir"""
    # Create full file path where it gets downloaded
    file_path = os.path.join(source_dir, f"{file_name}.pdf")  # ~Downloads/messages.pdf

    with open(file_path, 'rb') as f:
        reader = PdfFileReader(f)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            # Check each company
            for company, keyword in mapping.items():
                if company in text:
                    eft_num, today, total_draft = extract_info_from_page(page, keyword)
                    if company == 'EXXONMOBIL':
                        new_file_name = f'{eft_num}-{today}-({total_draft}).pdf'  # adds () to value
                    else:
                        new_file_name = f'{eft_num}-{today}-{total_draft}.pdf'

                    # Use the company_subdir_mapping to get the correct target_dir for this company
                    target_dir = company_subdir_mapping[company]
                    destination_file = os.path.join(target_dir, new_file_name)

                    # Save the page to a new PDF
                    writer = PdfFileWriter()
                    writer.addPage(page)
                    with open(destination_file, 'wb') as output_pdf:
                        writer.write(output_pdf)

                    print(f'Moved page {page_num} to {destination_file}')
                    break  # If we found a match, no need to check the other companies

