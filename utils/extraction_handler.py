from pikepdf import Pdf
import pdfplumber
import io
import re
import datetime
from utils.mappings_refactored import doc_type_abbrv_to_doc_type_subdir_map, regex_patterns, company_id_to_company_subdir_map


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

# WIP: combine w/ extract_doc_type_and_total_target_amt to return regex_num, total_target_amt, and doc_type; have all three as instance variables; then `self.regex_num` where applicable
def extract_info_from_text(page_text):
    # Extract regex pattern (EFT, CCM, CMB, RTV, CBK)
    regex_num_matches = re.findall(regex_pattern, page_text)
    if regex_num_matches:
        regex_num = regex_num_matches[0]
        # print(f'-------------------------------------------------- regex_num--------------------------------: {regex_num}')
    else:
        print(f'No matches for regex: {regex_pattern} in\n {page_text}')
        regex_num = None

    # Extract total_target_value
    total_amount_matches = re.findall(r'-?[\d,]+\.\d+-?', page_text)
    # print(f'\nGetting total_amount_matches: {total_amount_matches}\n')
    if total_amount_matches:
        # print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: {total_amount_matches}')
        total_amount = total_amount_matches[-1]
        # print(f'=================================================: {total_amount}')

    else:
        total_amount = None

    return regex_num, total_amount


# WIP: combine w/ extract_info_from_text to return regex_num, total_target_amt, and doc_type; have all three as instance variables; then `self.regex_num` where applicable
def extract_doc_type_and_total_target_amt(page_text):
    # Extract regex pattern (EFT, CCM, CMB, RTV, CBK)
    doc_type = None
    for pattern in regex_patterns:
        if re.search(pattern, page_text):
            doc_type = pattern.split('-')[0]  # Extracting the document type prefix from the pattern.
            break

    if doc_type is None:
        print(f"No matches for regex patterns: {regex_patterns} in\n {page_text}")
        return None, None

    # Extract total_target_value
    total_amount_matches = re.findall(r'-?[\d,]+\.\d+-?', page_text)
    # print(f'\nGetting total_amount_matches: {total_amount_matches}\n')
    if total_amount_matches:
        # print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: {total_amount_matches}')
        total_amount = total_amount_matches[-1]
        # print(f'=================================================: {total_amount}')
    else:
        total_amount = None

    return doc_type, total_amount