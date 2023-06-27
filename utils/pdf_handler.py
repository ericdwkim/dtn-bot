import os
import re
import shutil
import datetime
import pikepdf
import pdfplumber
from utils.post_processing import merge_rename_and_summate
from utils.extraction_handler import extract_text_from_pdf_page, extract_info_from_text

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


def get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name):
    full_path_to_downloaded_pdf = os.path.join(download_dir, f"{keyword_in_dl_file_name}.pdf")
    return full_path_to_downloaded_pdf


def create_and_save_pdf(pages, new_file_name, destination_dir):
    new_pdf = pikepdf.Pdf.new()
    new_pdf.pages.extend(pages)
    dest_dir_with_new_file_name = os.path.join(destination_dir, new_file_name)
    new_pdf.save(dest_dir_with_new_file_name)


def get_new_file_name(eft_num, today, total_draft_amt, company_name):
    if company_name == 'EXXONMOBIL':
        new_file_name = f'{eft_num}-{today}-({total_draft_amt}).pdf'
    else:
        new_file_name = f'{eft_num}-{today}-{total_draft_amt}.pdf'
    print(f'new_file_name: {new_file_name}')
    return new_file_name

# TODO: refactor for credit card & draft notice reuse or just new process fn?
def process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

        # Only single page EFT docs only
        if re.search(r'EFT-\d+', current_page_text) and company_name in current_page_text and 'END MSG' in current_page_text:
            current_pages = [pdf.pages[page_num]]
            eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)

            new_file_name = get_new_file_name(eft_num, today, total_draft_amt, company_name)
            destination_dir = company_name_to_company_subdir_mapping[company_name]

            create_and_save_pdf(current_pages, new_file_name, destination_dir)

            # Move cursor at single page (micro) level
            page_num += 1

            # If there aren't anymore pages, exit loop
            if page_num >= len(pdf.pages):
                break

        # Only multipage EFT docs only
        elif re.search(r'EFT-\d+', current_page_text) and company_name in current_page_text and 'END MSG' not in current_page_text:
            current_pages = []
            current_page_texts = []

            while 'END MSG' not in current_page_text and page_num < len(pdf.pages) - 1:
                current_pages.append(pdf.pages[page_num])
                current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
                current_page_texts.append(current_page_text)
                # Move cursor at multi-page (micro) level
                page_num += 1

                # If there aren't anymore pages, exit loop
                if page_num >= len(pdf.pages):
                    break

            current_page_text = "".join(current_page_texts)
            eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)

            new_file_name = get_new_file_name(eft_num, today, total_draft_amt, company_name)
            destination_dir = company_name_to_company_subdir_mapping[company_name]

            create_and_save_pdf(current_pages, new_file_name, destination_dir)

    return page_num

def process_pdf(keyword_in_dl_file_name, company_name_to_company_subdir_mapping, download_dir, company_name_to_search_keyword_mapping):
    try:
        # Get all matching files
        full_path_to_downloaded_pdf = get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name)

        # Read original PDF from dls dir
        print(f'Processing file: {full_path_to_downloaded_pdf}')
        with pikepdf.open(full_path_to_downloaded_pdf) as pdf:
            page_num = 0  # Initialize page_num
            while page_num < len(pdf.pages):
                # Process pages and update the page number at original PDF (macro) level
                page_num = process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping)

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False


