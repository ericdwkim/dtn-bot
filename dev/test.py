import pikepdf
import io
import pdfplumber
import re
import datetime
import os

file_path = '/Users/ekim/workspace/txb/docs/ccm_full.pdf'
file_path_val_ccm = '/Users/ekim/workspace/txb/docs/val_ccm.pdf'

company_name_to_search_keyword_mapping_valero = {
    'VALERO': ['-NET CREDIT 51000', 'CCM-\d+'],
    'CONCORD FIRST DATA RETRIEVAL': ['MARKETER TOTAL', 'CMB-\d+'],
    'EXXONMOBIL': ['TOTAL DISTRIBUTOR', 'CCM-\d+']


}


company_name_to_subdir_full_path_mapping_valero = {

    'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/Valero (10006)',

    'CONCORD FIRST DATA RETRIEVAL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/First Data',

    'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)/temp'

}



def create_and_save_pdf(pages, new_file_name, destination_dir):
    new_pdf = pikepdf.Pdf.new()
    new_pdf.pages.extend(pages)
    dest_dir_with_new_file_name = os.path.join(destination_dir, new_file_name)
    new_pdf.save(dest_dir_with_new_file_name)


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

    # Extract regex pattern (CCM, CMB, RTV, CBK)
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
    total_credit_matches = re.findall(r'([\d,]+\.\d+)', current_page_text)
    # print(f'\nUsing total_credit_keyword: "{total_credit_keyword}"\nGetting total_credit_matches: {total_credit_matches}\n')
    if total_credit_matches:
        total_credit_amt = total_credit_matches[-1]
    else:
        # print(f"No matches for regular expression using keyword: {total_credit_keyword} in text:\n*****************************************************\n {current_page_text}\n*****************************************************\n")
        total_credit_amt = None

    today = datetime.date.today().strftime('%m-%d-%y')

    if total_credit_amt is None:
        return today, None

    return regex_num, today, total_credit_amt


def process_page_cc(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
        print(f'Processing page: {page_num}')
        print(f'\n*****************************\n{current_page_text}\n*****************************\n')

        # Handle single page CCM docs
        if re.search(r'CCM-\d+', current_page_text) and company_name in current_page_text and 'END MSG' in current_page_text:
            current_pages = [pdf.pages[page_num]]
            regex_num, today, total_credit_amt = extract_info_from_text_cc(current_page_text, keywords)

            new_file_name = get_new_file_name_cc(regex_num, today, total_credit_amt)
            destination_dir = company_name_to_company_subdir_mapping[company_name]
            create_and_save_pdf(current_pages, new_file_name, destination_dir)
            print(f'Processing pageA: {page_num}')

            page_num += 1

            if page_num >= len(pdf.pages):
                break

        # Handles Valero CCM & CFDR CMB multi page docs
        if (re.search(r'CCM-\d+', current_page_text) or re.search(r'CMB-\d+', current_page_text)) and company_name in current_page_text and 'END MSG' not in current_page_text:
            current_pages =[]
            current_page_texts = []
            # todo: TOTAL DISTRIBUTOR : $411,947.66; why not processed?


            while 'END MSG' not in current_page_text and page_num < len(pdf.pages):
                current_pages.append(pdf.pages[page_num])
                print(f'---------------------------------current_pages: {current_pages}')
                current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
                current_page_texts.append(current_page_text)
                print(f'\n#######################################\n: {current_page_texts}\n#######################################\n')

                page_num += 1

                if page_num > len(pdf.pages):
                    break
            current_page_text = "".join(current_page_texts)
            print(
                f'\n#######################################\n: {current_page_text}\n#######################################\n')
            regex_num, today, total_credit_amt = extract_info_from_text_cc(current_page_text, keywords)



            new_file_name = get_new_file_name_cc(regex_num, today, total_credit_amt)

            destination_dir = company_name_to_company_subdir_mapping[company_name]


            create_and_save_pdf(current_pages, new_file_name, destination_dir)


    return page_num



def process_pdf_cc(filepath,  company_name_to_company_subdir_mapping,company_name_to_search_keyword_mapping):
    try:

        # Read original PDF from dls dir
        print(f'Processing file: {filepath}')
        with pikepdf.open(filepath) as pdf:
            page_num = 0  # Initialize page_num
            while page_num < len(pdf.pages ):
                # Process pages and update the page number at original PDF (macro) level
                page_num = process_page_cc(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping)
                page_num += 1


            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False


results = process_pdf_cc(file_path, company_name_to_subdir_full_path_mapping_valero, company_name_to_search_keyword_mapping_valero)
if results:
    print('Finished')