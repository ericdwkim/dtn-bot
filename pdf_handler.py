import os
import re
import shutil
import datetime
from PyPDF2 import PdfReader
from pdfreader import SimplePDFViewer


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

            # text = extract_content_from_pdf(source_file, target_company)
            # if text:
            #     eft_num, today, total_draft = extract_info(text)
            #     new_file_name = f'{eft_num}-{today}-{total_draft}.pdf'
            #     destination_file = os.path.join(target_dir, new_file_name)
            #
            #     print(f'Moving {source_file} to {destination_file}')
            #     shutil.move(source_file, destination_file)


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


def process_pdf(keyword_in_dl_file_name, company_name_to_target_subdir_mapping, dl_dir, company_name_to_search_keyword_mapping):
    """

    :param keyword_in_dl_file_name: substring keyword that is contained in the original downloaded EFT/draft notices PDF for all companies; 'messages' in messages.pdf
    :param company_name_to_target_subdir_mapping: eg: {company_name: company_subdirectory}
    :param dl_dir: downloads directory folder (~/Downloads)
    :param company_name_to_search_keyword_mapping: eg: { 'CVR SUPPLY & TRADING, LLC': 'Total Draft' }
    :return:
    """

    # Create full file path where it gets downloaded; replaces the need to pass `dl_dir` param
    full_file_path_to_downloaded_pdf = os.path.join(dl_dir, f"{keyword_in_dl_file_name}.pdf")
    # ~/Downloads/messages.pdf

    with open(full_file_path_to_downloaded_pdf, 'rb') as fd:
        viewer = SimplePDFViewer(fd)

        # Get total number of pages in the PDF
        total_pages = len(viewer.pages)

        # Check each page
        for page_num in range(total_pages):
            viewer.navigate(page_num + 1)
            viewer.render()

            # Get page content as text
            text = ' '.join(viewer.canvas.strings)

            # Check each company
            for company_name, keyword in company_name_to_search_keyword_mapping.items():
                if company_name in text:
                    eft_num, today, total_draft = extract_info_from_page(text, keyword)
                    if company_name == 'EXXONMOBIL':
                        new_file_name = f'{eft_num}-{today}-({total_draft}).pdf'
                    else:
                        new_file_name = f'{eft_num}-{today}-{total_draft}.pdf'
                    # TODO: we don't need full destination_file path; we need `dest_dir` for each company to then render output pdf into
                    destination_file = os.path.join(company_name_to_target_subdir_mapping[company_name], new_file_name)

                    # Save the page to a new PDF
                    # writer = SimplePDFViewer(fd)
                    # writer.navigate(page_num + 1)
                    # writer.render()
                    #
                    # with open(destination_file, 'wb') as output_pdf:
                    #     output_pdf.write(writer.canvas.container.raw_content)
                    #
                    # print(f'Moved page {page_num} to {destination_file}')
                    # break  # If we found a match, no need to check the other companies
