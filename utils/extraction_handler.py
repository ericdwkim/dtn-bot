from pikepdf import Pdf
import pdfplumber
import io
import re
import datetime
from .mappings import company_name_to_subdir_full_path_mapping_fuel_drafts, company_names


def extract_company_dir_from_map():
    company_subdirs = []
    for name in company_names:
        company_subdir = company_name_to_subdir_full_path_mapping_fuel_drafts.get(name)
        if company_subdir:
            company_subdirs.append(company_subdir)
    return company_subdirs

# Take in pikepdf Pdf object, return extracted text
def extract_text_from_pdf_page(page):
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
    # Extract regex pattern (EFT, CCM, CMB, RTV, CBK)
    regex_num_matches = re.findall(regex_pattern, current_page_text)
    if regex_num_matches:
        regex_num = regex_num_matches[0]
        # print(f'-------------------------------------------------- regex_num--------------------------------: {regex_num}')
    else:
        print(f'No matches for regex: {regex_pattern} in\n {current_page_text}')
        regex_num = None

    # Extract total_target_value
    total_amount_matches = re.findall(r'-?[\d,]+\.\d+-?', current_page_text)
    # print(f'\nGetting total_amount_matches: {total_amount_matches}\n')
    if total_amount_matches:
        # print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: {total_amount_matches}')
        total_amount = total_amount_matches[-1]
        # print(f'=================================================: {total_amount}')

    else:
        total_amount = None

    today = datetime.date.today().strftime('%m-%d-%y')

    return regex_num, today, total_amount

