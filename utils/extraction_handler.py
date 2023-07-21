from pikepdf import Pdf
import pdfplumber
import io
import re
import datetime
from .mappings import company_name_to_subdir_full_path_mapping_fuel_drafts, company_names


def extract_company_dir_from_map():
    """
    Loops through company_names list and fetches all company name directories in a list
    :return: List of `company_subdirs`
    """
    company_subdirs = []
    for name in company_names:
        company_subdir = company_name_to_subdir_full_path_mapping_fuel_drafts.get(name)
        if company_subdir:
            company_subdirs.append(company_subdir)
    return company_subdirs

def extract_text_from_pdf_page(page):
    """
    Takes in a pikePdf Page object and returns extracted text from page object
    :param page: pikePdf Page object with a specified page number
    :return: extracted text as string
    """
    # Create a BytesIO buffer
    pdf_stream = io.BytesIO()

    # Write the page to the buffer
    with Pdf.new() as pdf:
        pdf.pages.append(page)
        pdf.save(pdf_stream)

    # Use pdfplumber to read the page from the buffer
    pdf_stream.seek(0)
    with pdfplumber.open(pdf_stream) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

    return text

def extract_info_from_text(current_page_text, regex_pattern):
    """
    Extracts target data from text string
    :param current_page_text: string text
    :param regex_pattern: document types(EFT, CCM, CMB, RTV, CBK)
    :return: Tuple (Any | None, `today`, Any | None)
    """
    # Extract regex pattern
    regex_num_matches = re.findall(regex_pattern, current_page_text)
    if regex_num_matches:
        # @dev: Assumes the first regex_num match is the correct, target regex_num from string text
        regex_num = regex_num_matches[0]
    else:
        print(f'No matches for regex: {regex_pattern} in\n {current_page_text}')
        regex_num = None

    # Extract total_target_value
    total_amount_matches = re.findall(r'-?[\d,]+\.\d+-?', current_page_text)
    # print(f'\nGetting total_amount_matches: {total_amount_matches}\n')
    if total_amount_matches:
        # @dev: Assumes the last total_amount match is the correct, target total amount from string text
        total_amount = total_amount_matches[-1]

    else:
        total_amount = None

    today = datetime.today().strftime('%m-%d-%y')


    return regex_num, today, total_amount

