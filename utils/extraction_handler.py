from pikepdf import Pdf
import pdfplumber

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


def extract_info_from_text(current_page_text, target_keywords):
    """Extract the specific information from a page"""

    # Extract EFT number
    eft_num_pattern = target_keywords[1]  # Assuming keyword is something like 'EFT-'
    eft_num_matches = re.findall(eft_num_pattern, current_page_text)
    print(f'\nUsing eft_num_pattern: "{eft_num_pattern}"\nGetting eft_num_matches: {eft_num_matches}\n')
    if eft_num_matches:
        eft_num = eft_num_matches[0]
    else:
        print(f"No matches for regular expression: {eft_num_pattern} in text:\n*****************************************************\n {current_page_text}\n*****************************************************\n")
        eft_num = None

    # Extract total_draft
    # total_draft_keyword = target_keywords[0]
    total_draft_matches = re.findall(r'([\d,]+\.\d+)', current_page_text)
    # print(f'\nUsing total_draft_keyword: "{total_draft_keyword}"\nGetting total_draft_matches: {total_draft_matches}\n')
    if total_draft_matches:
        total_draft_amt = total_draft_matches[-1]
    else:
        print(f"No matches for regular expression using keyword: {total_draft_keyword} in text:\n*****************************************************\n {current_page_text}\n*****************************************************\n")
        total_draft_amt = None

    today = datetime.date.today().strftime('%m-%d-%y')

    if eft_num is not None and total_draft_amt is None:
        return eft_num, today, None
    elif eft_num is None and total_draft_amt is not None:
        return None, today, total_draft_amt
    elif eft_num is None and total_draft_amt is None:
        return None, today, None

    return eft_num, today, total_draft_amt
