import os
import re
import shutil
import datetime
import pikepdf
import pdfplumber
import io


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

# Take in pikepdf Pdf object, return extracted text
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
    total_draft_keyword = target_keywords[0]
    total_draft_matches = re.findall(r'([\d,]+\.\d+)', current_page_text)
    print(f'\nUsing total_draft_keyword: "{total_draft_keyword}"\nGetting total_draft_matches: {total_draft_matches}\n')
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
