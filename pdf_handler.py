import os
import re
import shutil
import datetime
import glob
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
# def get_target_directories(parent_dir, company_keywords_mapping):
#     """
#     :param parent_dir: The parent directory path where the subdirectories are located.
#     :param company_keywords_mapping: A mapping of company names to their respective search keywords.
#     :return: A mapping of company names to the full paths of their respective subdirectories.
#     """
#     target_directories = {}
#     subdirs = os.listdir(parent_dir)
#     for company in company_keywords_mapping.keys():
#         company_lower = company.lower()
#         for subdir in subdirs:
#             if company_lower in subdir.lower():
#                 full_path = os.path.join(parent_dir, subdir)
#                 target_directories[company] = full_path
#     return target_directories
#



def extract_info_from_text(text, target_keywords):
    """Extract the specific information from a page"""

    # Extract total_draft
    total_draft_keyword = target_keywords[0]
    total_draft_matches = re.findall(r'(\d+\.\d+)', text)
    if not total_draft_matches:
        print(f"No matches for regular expression in text: {total_draft_keyword}")
        return None, None, None
    total_draft_amt = total_draft_matches[0]

    # Extract EFT number
    eft_num_pattern = target_keywords[1]  # Assuming keyword is something like 'EFT-'
    eft_num_matches = re.findall(eft_num_pattern, text)
    if not eft_num_matches:
        print(f"No matches for regular expression in text: {eft_num_pattern}")
        return None, None, None
    eft_num = eft_num_matches[0]

    today = datetime.date.today().strftime('%m-%d-%y')

    return eft_num, today, total_draft_amt


def get_matching_pdf_file(keyword_in_dl_file_name, download_dir):
    matching_file = os.path.join(download_dir, f"{keyword_in_dl_file_name}.pdf")
    print(f'matching_file: {matching_file}')
    return matching_file



# @dev: 0-idxing default of `enumerate` for start_count assigned to `page_num` resulted in "islice must be None or an int" error as SimplePDFViewer's `navigate()` 1-idxs hence `page_num + 1`
def process_page(viewer, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping, f):
    viewer.navigate(page_num + 1)  # navigating starts from 1, not 0
    viewer.render()

    # Get page content as text
    text = ' '.join(viewer.canvas.strings)
    print(f'text: {text}')

    # Check each company
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        if company_name in text:
            print(f"Processing page {page_num + 1} for {company_name}")  # page number starts from 1 for user's perspective
            eft_num, today, total_draft_amt = extract_info_from_text(text, keywords)
            # print(f'-----------------eft_num: {eft_num} | today: {today}  | total_draft_amt: {total_draft_amt}')

            # If any of the extracted values is None, continue to next company
            if eft_num is None or today is None or total_draft_amt is None:
                continue

            if company_name == 'EXXONMOBIL':
                new_file_name = f'{eft_num}-{today}-({total_draft_amt}).pdf'
                # print(f'new_file_name: {new_file_name}')
            else:
                new_file_name = f'{eft_num}-{today}-{total_draft_amt}.pdf'
                # print(f'new_file_name: {new_file_name}')

            # Use subdir mapping to search company_name to get full subdir path for newly renamed eft file
            destination_dir = company_name_to_company_subdir_mapping[company_name]
            print(f'destination_dir: {destination_dir}')
            full_path_to_renamed_company_file = os.path.join(destination_dir, new_file_name)
            print(f'full_path_to_renamed_company_file: {full_path_to_renamed_company_file}')

            # Save the page to a new PDF
            with open(full_path_to_renamed_company_file, 'wb') as output_pdf:
                print(f' writing new pdf in correct subdir--------')
                writer = SimplePDFViewer(f)
                writer.navigate(page_num + 1)  # navigating starts from 1, not 0
                writer.render()
                output_pdf.write(writer.canvas.container.raw_content)

            print(f'Moved page {page_num + 1} to {destination_dir}')  # page number starts from 1 for user's perspective

def process_pdf(keyword_in_dl_file_name, company_name_to_company_subdir_mapping, download_dir, company_name_to_search_keyword_mapping):
    """
    :param keyword_in_dl_file_name: substring keyword that is contained in the original downloaded EFT/draft notices PDF for all companies; 'messages' in messages.pdf
    :param company_name_to_company_subdir_mapping: eg: {company_name: company_subdirectory}
    :param download_dir: downloads directory folder (~/Downloads)
    :param company_name_to_search_keyword_mapping: eg: { 'CVR SUPPLY & TRADING, LLC': 'Total Draft' }
    :return: boolean indicating success or failure
    """
    try:
        # Get all matching files
        matching_file = get_matching_pdf_file(keyword_in_dl_file_name, download_dir)

        print(f'Processing file: {matching_file}')
        with open(matching_file, 'rb') as f:
            viewer = SimplePDFViewer(f)

            for page_num, page in enumerate(viewer.doc.pages()):
                process_page(viewer, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping, f)

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False
