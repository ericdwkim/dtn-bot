import pikepdf
import pdfplumber
import re
import datetime
import os
from utils.post_processing import merge_rename_and_summate

file_path = '/Users/ekim/workspace/txb/docs/ccm_full.pdf'

company_name_to_search_keyword_mapping_credit_cards = {
    'VALERO': ['-NET CREDIT 51000', 'CCM-\d+'],
    'CONCORD FIRST DATA RETRIEVAL': ['MARKETER TOTAL', 'CMB-\d+'],
    'EXXONMOBIL': ['TOTAL DISTRIBUTOR', 'CCM-\d+']


}


company_name_to_subdir_full_path_mapping_credit_cards = {

    'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/Valero (10006)',

    'CONCORD FIRST DATA RETRIEVAL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/First Data',

    'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)/temp'

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

def get_new_file_name_cc(regex_num, today, total_credit_amt):
    new_file_name = f'{regex_num}-{today}-{total_credit_amt}.pdf'
    # print(f'new_file_name: {new_file_name}')
    return new_file_name

def extract_text_from_pdf_page(page):
    # Create a BytesIO buffer
    pdf_stream = io.BytesIO()

    # Write the page to the buffer
    with pikepdf.Pdf.new() as pdf:
        pdf.pages.append(page)
        pdf.save(pdf_stream)

    # Use pdfplumber to read the page from the buffer
    pdf_stream.seek(0)
    with pdfplumber.open(pdf_stream) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

    return text

def extract_info_from_text_cc(current_page_text, target_keywords):
    """Extract the specific information from a page"""

    # Extract regex pattern (EFT, CCM, CMB, RTV, CBK)
    regex_num_pattern = target_keywords[1]
    regex_num_matches = re.findall(regex_num_pattern, current_page_text)
    print(f'\nUsing regex_num_pattern: {regex_num_pattern}\nGetting regex_num_matches: {regex_num_matches}')
    if regex_num_matches:
        regex_num = regex_num_matches[0]
    else:
        print(f'No matches for regex: {regex_num_pattern} in\n {current_page_text}')
        regex_num = None


    # Extract total_target_value
    # total_credit_keyword = target_keywords[0]
    total_amount_matches = re.findall(r'([\d,]+\.\d+)', current_page_text)
    # print(f'\nUsing total_credit_keyword: "{total_credit_keyword}"\nGetting total_amount_matches: {total_amount_matches}\n')
    if total_amount_matches:
        total_amount = total_amount_matches[-1]
    else:
        # print(f"No matches for regular expression using keyword: {total_credit_keyword} in text:\n*****************************************************\n {current_page_text}\n*****************************************************\n")
        total_amount = None

    today = datetime.date.today().strftime('%m-%d-%y')

    # Debugging purposes
    # if regex_num is not None and total_amount is None:
    #     return eft_num, today, None
    # elif regex_num is None and total_amount is not None:
    #     return None, today, total_amount
    # elif regex_num is None and total_amount is None:
    #     return None, today, None

    return regex_num, today, total_amount

def process_page_cc(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):
    for company_name, keywords in company_name_to_search_keyword_mapping.items():


        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
        print(f'Processing page: {page_num + 1}')
        print(f'\n*****************************\n{current_page_text}\n*****************************\n')

        # Handles CCM, CMB multi page docs
        # if (re.search(r'CCM-\d+', current_page_text) or re.search(r'CMB-\d+', current_page_text)) and company_name in current_page_text and 'END MSG' not in current_page_text:
        #     # print(f'page_num: {page_num}')
        #     current_pages =[]
        #     current_page_texts = []
        #
        #
        #
        #     while 'END MSG' not in current_page_text and page_num < len(pdf.pages):
        #         current_pages.append(pdf.pages[page_num])
        #         current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
        #         current_page_texts.append(current_page_text)
        #         print(f'current_page_texts: {current_page_texts}')
        #
        #
        #         page_num += 1
        #
        #
        #         if page_num >= len(pdf.pages):
        #             break
        #
        #     current_page_text = "".join(current_page_texts)
        #
        #     regex_num, today, total_amount = extract_info_from_text_cc(current_page_text, keywords)
        #     new_file_name = get_new_file_name_cc(regex_num, today, total_amount)
        #     print(f'new_file_name: {new_file_name}')
        #     destination_dir = company_name_to_company_subdir_mapping[company_name]
        #     multi_page_pdf_saved = create_and_save_pdf(current_pages, new_file_name, destination_dir)
        #
        #     # POST PROCESSING - ONLY FOR EXXON CCM 'TOTAL DISTRIBUTOR'
        #     if company_name == 'EXXONMOBIL' and re.match(r'CCM-\d+', regex_num) and multi_page_pdf_saved:
        #         merge_rename_and_summate(destination_dir)
        #     else:
        #         print(f'Could not post process')




        # Handle single page CCM docs
        if re.search(r'CCM-\d+', current_page_text) and company_name in current_page_text and 'END MSG' in current_page_text:
            current_pages = [pdf.pages[page_num]]
            regex_num, today, total_amount = extract_info_from_text_cc(current_page_text, keywords)
            new_file_name = get_new_file_name_cc(regex_num, today, total_amount)
            # print(f'new_file_name: {new_file_name}')

            destination_dir = company_name_to_company_subdir_mapping[company_name]
            # print(f'destination_dir: {destination_dir}')

            create_and_save_pdf(current_pages, new_file_name, destination_dir)
            page_num += 1

            if page_num >= len(pdf.pages):
                break

    return page_num

def process_pdf_cc(filepath,  company_name_to_company_subdir_mapping,company_name_to_search_keyword_mapping):
    try:

        # Read original PDF from dls dir
        print(f'Processing file: {filepath}')
        with pikepdf.open(filepath) as pdf:
            page_num = 0  # Initialize page_num
            while page_num < len(pdf.pages):
                print(f'page_num: {page_num + 1}')
                # Process pages and update the page number at original PDF (macro) level
                new_page_num = process_page_cc(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping)

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

results = process_pdf_cc(file_path, company_name_to_subdir_full_path_mapping_credit_cards, company_name_to_search_keyword_mapping_credit_cards)
if results:
    print('Finished')

# TODO
"""
6/23/23 - 8:10 PM CST 

1) current issue is the processing order of the PDF is mixed of multi CCM (exxon) and single page ccm (exxon). the single pages get saved in the same temp_dir which merge_rename_and_summate() deletes ; also multi page doesn't get merged --> a different way than having an intermediary subdir?????

2) RTV and CBK files 

3) Replace extract_info_from_text() in extraction_handler.py with the one on here ; only diff is the logic to ensure that as many vars are returned which is only necessary for debugging purposes. 

4) Move/merge/refactor all functions in here to their respective modules or main.py

"""