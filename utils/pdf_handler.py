import os
import re
import time
import pikepdf
import shutil
import pdfplumber
import datetime
from utils.post_processing import merge_rename_and_summate
from utils.extraction_handler import extract_text_from_pdf_page, extract_info_from_text
from utils.filesystem_manager import end_of_month_operations, calculate_directory_path, is_last_day_of_month, cleanup_files



def rename_and_delete_pdf(file_path):
    file_deleted = False
    today = datetime.date.today().strftime('%m-%d-%y')

    if os.path.exists(file_path):
        with pikepdf.open(file_path) as pdf:
            if len(pdf.pages) > 0:
                first_page = extract_text_from_pdf_page(pdf.pages[0])

                if re.search(r'EFT-\d+', first_page) or re.search(r'CCM-\d+ | CMD-\d+', first_page):
                    if re.search(r'EFT-\d+', first_page):
                        new_file_name = f'EFT-{today}-TO-BE-DELETED.pdf'
                    else:
                        new_file_name = f'CCM-{today}-TO-BE-DELETED.pdf'

                    file_directory = os.path.dirname(file_path)
                    new_file_path = os.path.join(file_directory, new_file_name)

                    print(f"Renaming file: {file_path} to {new_file_path}")
                    os.rename(file_path, new_file_path)
                    file_deleted = True
                    print("File renamed successfully.")
                    time.sleep(3)

                    if os.path.exists(new_file_path):
                        print(f"Deleting file: {new_file_path}")
                        os.remove(new_file_path)
                        print("File deleted successfully.")

    return file_deleted

# Invoices
def rename_and_move_pdf(file_name, source_dir, target_dir):
    # Get today's date and format it as MM-DD-YY
    today = datetime.date.today().strftime('%m-%d-%y')

    # Find the downloaded PDF
    for file in os.listdir(source_dir):
        if file.endswith('.pdf') and file_name in file:
            source_file = os.path.join(source_dir, file)
            # Rename file
            destination_file = os.path.join(target_dir, f'{today}.pdf')
            # Move the file
            print(f'Moving {destination_file} to {target_dir}')
            shutil.move(source_file, destination_file)
            break  # Only expecting one file, so exit loop after first one is found


def get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name):
    full_path_to_downloaded_pdf = os.path.join(download_dir, f"{keyword_in_dl_file_name}.pdf")
    return full_path_to_downloaded_pdf


def create_and_save_pdf(pages, new_file_name, destination_dir):
    try:
        new_pdf = pikepdf.Pdf.new()
        new_pdf.pages.extend(pages)
        dest_dir_with_new_file_name = os.path.join(destination_dir, new_file_name)
        new_pdf.save(dest_dir_with_new_file_name)
        return True  # Return True if the file was saved successfully
    except Exception as e:
        print(f"Error occurred while creating and saving PDF: {str(e)}")
        return False  # Return False if an error occurred

def get_new_file_name(regex_num, today, total_target_amt):
    # @dev: only EFTs that follow this convention
    # File naming convention for total_target_amt preceding/succeeding with a hyphen indicative of a balance owed
    if re.match(r'EFT-\s*\d+', regex_num) and re.match(r'-?[\d,]+\.\d+-?', total_target_amt):
        if "-" in total_target_amt:  # Checks if "-" exists anywhere in total_target_amt
            total_target_amt = total_target_amt.replace("-", "")  # Removes "-"
            new_file_name = f'{regex_num}-{today}-({total_target_amt}).pdf'
        else:  # No "-" in total_target_amt
            new_file_name = f'{regex_num}-{today}-{total_target_amt}.pdf'

    # File naming convention for chargebacks/retrievals
    # @dev: regex_num is included due to edge case of identical filenames overwriting
    # eg: VALERO CBK-0379 gets overwritten by RTV-0955 if regex_num is not included
    elif (re.match(r'CBK-\s*\d+', regex_num) or re.match(r'RTV-\s*\d+', regex_num)):
        new_file_name = f'{regex_num}-{today}-CHARGEBACK REQUEST.pdf'

    # File naming convention for all other files (CCM, CMB, positive ETF `total_amount` values)
    else:
        new_file_name = f'{regex_num}-{today}-{total_target_amt}.pdf'
    # print(f'new_file_name: {new_file_name}')
    return new_file_name


def process_multi_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping):
    current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
    print(f'Processing page: {page_num + 1}')

    for company_name in company_names:
        # Handles CCM, CMB, LRD multi page docs
        if company_name in current_page_text and 'END MSG' not in current_page_text:
            for pattern in regex_patterns:
                if re.search(pattern, current_page_text, re.IGNORECASE):

                    current_pages = []
                    current_page_texts = []

                    while 'END MSG' not in current_page_text and page_num < len(pdf.pages):
                        current_pages.append(pdf.pages[page_num])
                        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
                        current_page_texts.append(current_page_text)

                        page_num += 1

                        if page_num >= len(pdf.pages):
                            break

                    current_page_text = "".join(current_page_texts)

                    regex_num, today, total_amount = extract_info_from_text(current_page_text, pattern)
                    new_file_name = get_new_file_name(regex_num, today, total_amount)
                    print(f'\n*********************************************\n multi new_file_name\n*********************************************\n {new_file_name}')
                    destination_dir = company_name_to_company_subdir_mapping[company_name]
                    create_and_save_pdf(current_pages, new_file_name, destination_dir)

    return page_num


def process_single_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping):
    current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
    print(f'Processing page: {page_num + 1}')

    for company_name in company_names:
        # Handle single page CCM, CBK, RTV, ETF files
        if company_name in current_page_text and 'END MSG' in current_page_text:
            for pattern in regex_patterns:
                if re.search(pattern, current_page_text, re.IGNORECASE):
                    current_pages = [pdf.pages[page_num]]
                    regex_num, today, total_amount = extract_info_from_text(current_page_text, pattern)
                    new_file_name = get_new_file_name(regex_num, today, total_amount)
                    print(f'\n*********************************************\n single new_file_name\n*********************************************\n {new_file_name}')
                    destination_dir = company_name_to_company_subdir_mapping[company_name]
                    create_and_save_pdf(current_pages, new_file_name, destination_dir)

                    page_num += 1

                    if page_num >= len(pdf.pages):
                        break

    return page_num



def process_pages(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns, is_multi_page):
    try:

        # Read original PDF from dls dir
        print(f'Processing file: {filepath}')
        with pikepdf.open(filepath) as pdf:
            page_num = 0  # Initialize page_num
            while page_num < len(pdf.pages):
                print(f'page_num: {page_num + 1}')

                # Process pages and update the page number at original PDF (macro) level
                if is_multi_page:
                    new_page_num = process_multi_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping)
                else:
                    new_page_num = process_single_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping)

                # if process_page has not incremented
                # prevents one off issue
                if new_page_num == page_num:
                    page_num += 1
                else:
                    page_num = new_page_num

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False


def process_pdfs(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns, doc_type_abbrv_to_doc_type_map, company_id_to_company_subdir_map,
                 post_processing=False):
    try:
        print(f'----------------------------- {filepath}')
        print(f'Processing all single-page files....\n')
        single_pages_processed = process_pages(filepath, company_name_to_company_subdir_mapping, company_names,
                                               regex_patterns, is_multi_page=False)
        if single_pages_processed:
            print(f'Successfully finished processing all single-paged files\n')

        print(f'Now processing all multi-page files....\n')
        multi_pages_processed = process_pages(filepath, company_name_to_company_subdir_mapping, company_names,
                                              regex_patterns, is_multi_page=True)
        if multi_pages_processed:
            print(f'Successfully finished processing all multi-paged files\n')

        # Conditional post processing only for EXXON CCMs and LRDs
        if single_pages_processed and multi_pages_processed and post_processing is True:
            print(f'Post processing for EXXON CCMs & LRDs')
            output_directory_exxon = company_name_to_company_subdir_mapping['EXXONMOBIL']
            merge_rename_and_summate(output_directory_exxon, doc_type_abbrv_to_doc_type_map, company_id_to_company_subdir_map)

        # Dynamic filesystem mgmt when post processing is False and
        elif single_pages_processed and multi_pages_processed and post_processing is False and is_last_day_of_month():
            end_of_month_operations(directory, filename) # undefined filename

        else:
            return single_pages_processed and multi_pages_processed

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return False

