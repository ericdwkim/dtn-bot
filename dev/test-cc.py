import pikepdf
import pdfplumber
import re
import datetime
import os
from utils.post_processing import merge_rename_and_summate
from utils.extraction_handler import extract_text_from_pdf_page, extract_info_from_text

file_path = '/Users/ekim/workspace/txb/docs/ccm_full.pdf'
temp_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)/temp'


company_name_to_search_keyword_mapping_credit_cards = {
    'VALERO': ['-NET CREDIT 51000', 'CCM-\d+'],
    'CONCORD FIRST DATA RETRIEVAL': ['MARKETER TOTAL', 'CMB-\d+'],
    'EXXONMOBIL': ['TOTAL DISTRIBUTOR', 'CCM-\d+']


}


company_name_to_subdir_full_path_mapping_credit_cards = {

    'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/Valero (10006)',

    'CONCORD FIRST DATA RETRIEVAL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/First Data',

    'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)'

}

# def process_exxon_ccm(current_pages, new_file_name, destination_dir, temp_dir, company_name, regex_num):
#     if company_name != 'EXXONMOBIL':
#         single_made_pdf_saved = create_and_save_pdf(current_pages, new_file_name, destination_dir)
#     elif company_name == 'EXXONMOBIL':
#         single_page_pdf_saved_in_temp = create_and_save_pdf(current_pages, new_file_name, temp_dir)
#         if single_page_pdf_saved_in_temp:
#             merge_rename_and_summate(temp_dir)
#         else:
#             print(f'Could not post process multi page pdfs')
#     if company_name != 'EXXONMOBIL' and re.match(r'CMB-\d+', regex_num):
#         multi_page_pdf_saved = create_and_save_pdf(current_pages, new_file_name, destination_dir)
#     elif company_name == 'EXXONMOBIL' and re.match(r'CCM-\d+', regex_num):
#         multi_page_pdf_saved_in_temp = create_and_save_pdf(current_pages, new_file_name, temp_dir)
#         if multi_page_pdf_saved_in_temp:
#             merge_rename_and_summate(temp_dir)
#         else:
#             print(f'Could not post process multi page pdfs')


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

def get_new_file_name_cc(regex_num, today, total_credit_amt):
    new_file_name = f'{regex_num}-{today}-{total_credit_amt}.pdf'
    # print(f'new_file_name: {new_file_name}')
    return new_file_name


def process_multi_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):
    for company_name, keywords in company_name_to_search_keyword_mapping.items():

        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
        print(f'Processing page: {page_num + 1}')
        print(f'\n*****************************\n{current_page_text}\n*****************************\n')

        # Handles CCM, CMB multi page docs
        if (re.search(r'CCM-\d+', current_page_text) or re.search(r'CMB-\d+',
                                                                  current_page_text)) and company_name in current_page_text and 'END MSG' not in current_page_text:
            # print(f'page_num: {page_num}')
            current_pages = []
            current_page_texts = []

            while 'END MSG' not in current_page_text and page_num < len(pdf.pages):
                current_pages.append(pdf.pages[page_num])
                current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
                current_page_texts.append(current_page_text)
                print(f'current_page_texts: {current_page_texts}')

                page_num += 1

                if page_num >= len(pdf.pages):
                    break

            current_page_text = "".join(current_page_texts)

            regex_num, today, total_amount = extract_info_from_text(current_page_text, keywords)
            new_file_name = get_new_file_name_cc(regex_num, today, total_amount)
            print(f'new_file_name: {new_file_name}')
            destination_dir = company_name_to_company_subdir_mapping[company_name]

            if company_name != 'EXXONMOBIL' and re.match(r'CMB-\d+', regex_num):
                multi_page_pdf_saved = create_and_save_pdf(current_pages, new_file_name, destination_dir)

            # POST PROCESSING ONLY FOR EXXON CCM 'TOTAL DISTRIBUTOR'
            elif company_name == 'EXXONMOBIL' and re.match(r'CCM-\d+', regex_num):
                multi_page_pdf_saved_in_temp = create_and_save_pdf(current_pages, new_file_name, temp_dir)

    return page_num


def process_single_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
        print(f'Processing page: {page_num + 1}')
        print(f'\n*****************************\n{current_page_text}\n*****************************\n')

        # Handle single page CCM docs
        if re.search(r'CCM-\d+',
                     current_page_text) and company_name in current_page_text and 'END MSG' in current_page_text:
            current_pages = [pdf.pages[page_num]]
            regex_num, today, total_amount = extract_info_from_text(current_page_text, keywords)
            new_file_name = get_new_file_name_cc(regex_num, today, total_amount)
            destination_dir = company_name_to_company_subdir_mapping[company_name]

            if company_name != 'EXXONMOBIL':
                single_made_pdf_saved = create_and_save_pdf(current_pages, new_file_name, destination_dir)

            elif company_name == 'EXXONMOBIL':
                print(f'----------------------------------------------------------------')
                single_page_pdf_saved_in_temp = create_and_save_pdf(current_pages, new_file_name, temp_dir)
            page_num += 1

            if page_num >= len(pdf.pages):
                break

    return page_num


def process_multi_pages(filepath,  company_name_to_company_subdir_mapping,company_name_to_search_keyword_mapping):
    try:

        # Read original PDF from dls dir
        print(f'Processing file: {filepath}')
        with pikepdf.open(filepath) as pdf:
            page_num = 0  # Initialize page_num
            while page_num < len(pdf.pages):
                print(f'page_num: {page_num + 1}')
                # Process pages and update the page number at original PDF (macro) level
                new_page_num = process_multi_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping)


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


def process_single_pages(filepath, company_name_to_company_subdir_mapping, company_name_to_search_keyword_mapping):
    try:

        # Read original PDF from dls dir
        print(f'Processing file: {filepath}')
        with pikepdf.open(filepath) as pdf:
            page_num = 0  # Initialize page_num
            while page_num < len(pdf.pages):
                print(f'page_num: {page_num + 1}')

                # Process pages and update the page number at original PDF (macro) level
                new_page_num = process_single_page(pdf, page_num, company_name_to_search_keyword_mapping,
                                                   company_name_to_company_subdir_mapping)

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


def process_pdfs(filepath, company_name_to_company_subdir_mapping, company_name_to_search_keyword_mapping):
    try:
        print(f'Processing all single-page CCMs....\n')
        single_pages_processed = process_single_pages(filepath, company_name_to_company_subdir_mapping, company_name_to_search_keyword_mapping)
        if single_pages_processed:
            print(f'successfully finished processing all single page CCMs\n')

        print(f'Now processing all multi-page CCMs....\n')
        multi_pages_processed = process_multi_pages(filepath, company_name_to_company_subdir_mapping, company_name_to_search_keyword_mapping)
        if multi_pages_processed:
            print(f'successfully finished processing all multi paged CCMs\n')

        # once all single and multi page CCMs for EXXON are done,
        # post process all pdfs in temp dir
        if single_pages_processed and multi_pages_processed:
            # Exxon Temp dir post processing
            print(f'Post processing for EXXON CCMs.....')
            merge_rename_and_summate(temp_dir)

    except Exception as e:
        print(f'An error occurred: {str(e)}')


process_pdfs(file_path, company_name_to_subdir_full_path_mapping_credit_cards, company_name_to_search_keyword_mapping_credit_cards)


# TODO: RTV / CBK files & Loyalty Files  6/26/23 *******************************