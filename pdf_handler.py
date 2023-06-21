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
    print(f'full_path_to_downloaded_pdf: {full_path_to_downloaded_pdf}')
    return full_path_to_downloaded_pdf


def process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping,
                 start_idx=None):
    # We will use a list to store pages
    current_pages = []

    # Initial page to start processing
    current_pages.append(pdf.pages[page_num])

    # Extract text
    current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

    # Check each company
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        if company_name in current_page_text:
            print(
                f"***************************************************\nProcessing page {page_num + 1} for {company_name}")  # page number starts from 1 for user's perspective

            # Look for start and end markers, include more pages if needed
            while company_name in current_page_text and 'END MSG' not in current_page_text and page_num < len(
                    pdf.pages) - 1:
                page_num += 1
                current_pages.append(pdf.pages[page_num])
                current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

            eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)
            print(f'\neft_num: {eft_num} | today: {today}  | total_draft_amt: {total_draft_amt}\n')

            # If any of the extracted values is None, continue to next company
            if eft_num is None or today is None or total_draft_amt is None:
                continue

            if company_name == 'EXXONMOBIL':
                new_file_name = f'{eft_num}-{today}-({total_draft_amt}).pdf'
                print(f'new_file_name: {new_file_name}')
            else:
                new_file_name = f'{eft_num}-{today}-{total_draft_amt}.pdf'
                print(f'new_file_name: {new_file_name}')

            # Use subdir mapping to search company_name to get full subdir path for newly renamed eft file
            destination_dir = company_name_to_company_subdir_mapping[company_name]
            print(f'destination_dir: {destination_dir}')

            # Create new pdf obj
            new_pdf = pikepdf.Pdf.new()

            # Append pages from current_pages to new_pdf
            new_pdf.pages.extend(current_pages)
            total_pages_per_file = new_pdf.pages
            print(
                f'Saving PDF: {new_file_name} from page {page_num + 1 - len(current_pages)} to {page_num + 1} for a total of {len(total_pages_per_file)} page(s)\nUsed start_marker: {company_name}')

            # Save the new pdf with new filename in appropriate dest directory
            new_pdf.save(os.path.join(destination_dir, new_file_name))
            print(
                f'Saved page(s) {page_num + 1 - len(current_pages)} to {page_num + 1} to {destination_dir} with new file name: {new_file_name}\n************************************************\n')

            # Update start_idx for the next document
            start_idx = None if 'END MSG' in current_page_text else page_num

    # Return the start_idx and page_num to pass them to the next call of process_page
    return start_idx, page_num


def process_pdf(keyword_in_dl_file_name, company_name_to_company_subdir_mapping, download_dir, company_name_to_search_keyword_mapping, pdf):
    try:
        # Get all matching files
        full_path_to_downloaded_pdf = get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name)

        # Read original PDF from dls dir
        print(f'Processing file: {full_path_to_downloaded_pdf}')
        with pikepdf.open(full_path_to_downloaded_pdf) as pdf:
            start_idx = 0  # Initialize start index
            while start_idx < len(pdf.pages):
                # Process pages and update the start index and page number
                start_idx, page_num = process_page(pdf, start_idx, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping)
                start_idx = page_num + 1  # Update the start index to the next page after the last processed page

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False
