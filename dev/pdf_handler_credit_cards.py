import pikepdf
import pdfplumber
import re
import datetime
import os
from utils.post_processing import process_directory
from utils.extraction_handler import extract_text_from_pdf_page, extract_info_from_text
import subprocess

subprocess.run(["../scripts/delete_pdf_files.sh"], shell=True)
print(f'===========================================================================================')


file_path = '/Users/ekim/workspace/txb/docs/ccm_full.pdf'
temp_dir_ccm = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)/temp/CCM'
temp_dir_lrd = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)/temp/LRD'
temp_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)/temp'



company_names = ['VALERO', 'CONCORD FIRST DATA RETRIEVAL', 'EXXONMOBIL', 'U.S. OIL COMPANY', 'DK Trading & Supply', 'CVR SUPPLY & TRADING, LLC']

regex_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}


company_name_to_subdir_full_path_mapping_credit_cards = {

    'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/Valero (10006)',

    'CONCORD FIRST DATA RETRIEVAL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/First Data',

    'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)'

}


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

def get_new_file_name(regex_num, today, total_target_amt, company_name):
    # File naming convention for EXXONMOBIL ETFs only; wrapping amount in () to indicate amount owed
    if company_name == 'EXXONMOBIL' and re.match(r'EFT-\s*\d+', regex_num):
        new_file_name = f'{regex_num}-{today}-({total_target_amt}).pdf'

    # File naming convention for chargebacks/retrievals
    # @dev: regex_num is included due to edge case of identical filenames overwriting
    # eg: VALERO CBK-0379 gets overwritten by RTV-0955 if regex_num is not included
    elif (re.match(r'CBK-\s*\d+', regex_num) or re.match(r'RTV-\s*\d+', regex_num)):
        new_file_name = f'{regex_num}-{today}-CHARGEBACK REQUEST.pdf'

    # File naming convention for all other files (CCM, CMB, non-EXXON ETFs)
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

                    new_file_name = get_new_file_name(regex_num, today, total_amount, company_name)
                    print(f'\nnew_file_name: {new_file_name}')
                    destination_dir = company_name_to_company_subdir_mapping[company_name]

                    if company_name != 'EXXONMOBIL':
                        create_and_save_pdf(current_pages, new_file_name, destination_dir)

                    # POST PROCESSING ONLY FOR EXXON CCMs  'TOTAL DISTRIBUTOR' AND LRDs
                    elif company_name == 'EXXONMOBIL' and re.match(r'CCM-\s*\d+', regex_num):
                        create_and_save_pdf(current_pages, new_file_name, temp_dir_ccm)

                    elif company_name == 'EXXONMOBIL' and re.match(r'LRD-\s*\d+', regex_num):
                        create_and_save_pdf(current_pages, new_file_name, temp_dir_lrd)



    return page_num


def process_single_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping):
    current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
    print(f'Processing page: {page_num + 1}')

    for company_name in company_names:
        # Handle single page CCM, CBK, RTV files
        if company_name in current_page_text and 'END MSG' in current_page_text:
            for pattern in regex_patterns:
                if re.search(pattern, current_page_text, re.IGNORECASE):
                    current_pages = [pdf.pages[page_num]]
                    regex_num, today, total_amount = extract_info_from_text(current_page_text, pattern)
                    new_file_name = get_new_file_name(regex_num, today, total_amount, company_name)
                    destination_dir = company_name_to_company_subdir_mapping[company_name]

                    # VALERO RTV, CBK, CCM
                    if company_name != 'EXXONMOBIL':
                        create_and_save_pdf(current_pages, new_file_name, destination_dir)

                    # ONLY SEND SINGLE PAGE EXXON CCM FILES TO TEMP
                    elif company_name == 'EXXONMOBIL' and re.match(r'CCM-\s*\d+', regex_num):
                        create_and_save_pdf(current_pages, new_file_name, temp_dir_ccm)

                    # single LRDs
                    elif company_name == 'EXXONMOBIL' and re.match(r'LRD-\s*\d+', regex_num):
                        create_and_save_pdf(current_pages, new_file_name, temp_dir_lrd)


                    elif company_name == 'EXXONMOBIL':
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


def process_pdfs(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns):
    try:
        print(f'Processing all single-page CCMs....\n')
        single_pages_processed = process_pages(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns, is_multi_page=False)
        if single_pages_processed:
            print(f'successfully finished processing all single page CCMs\n')

        print(f'Now processing all multi-page CCMs....\n')
        multi_pages_processed = process_pages(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns, is_multi_page=True)
        if multi_pages_processed:
            print(f'successfully finished processing all multi paged CCMs\n')

        # once all single and multi page CCMs for EXXON are done,
        # post process all pdfs in temp dir
        if single_pages_processed and multi_pages_processed:
            print(f'Post processing for EXXON CCMs.....')
            temp_dir_ccm = os.path.join(temp_dir, 'CCM')
            temp_dir_lrd = os.path.join(temp_dir, 'LRD')
            process_directory(temp_dir_ccm)
            process_directory(temp_dir_lrd)
    except Exception as e:
        print(f'An error occurred: {str(e)}')


process_pdfs(file_path, company_name_to_subdir_full_path_mapping_credit_cards, company_names, regex_patterns)