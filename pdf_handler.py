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

def split_pdf_pages_on_markers(current_page_text, page_num, new_file_name, start_marker, end_marker, destination_dir, pdf, start_idx=None):

    if start_marker in current_page_text and start_idx is None:
        start_idx = page_num

    if end_marker in current_page_text and start_idx is not None:
        end_idx = page_num
        # Create new pdf obj
        new_pdf = pikepdf.Pdf.new()

        # Append pages from start_idx to current page
        new_pdf.pages.extend(pdf.pages[start_idx:end_idx + 1])
        total_pages_per_file = new_pdf.pages
        print(f'Saving PDF: {new_file_name} from page {start_idx + 1} to {end_idx + 1} for a total of {len(total_pages_per_file)} page(s)\nUsed start_marker: {start_marker} and end_marker: {end_marker}')

        # Save the new pdf with new filename in appropriate dest directory
        new_pdf.save(os.path.join(destination_dir, new_file_name))

        # Reset start index for slicing the next set of page(s)
        start_idx = None

    return start_idx

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

    # Extract total_draft
    total_draft_keyword = target_keywords[0]
    total_draft_matches = re.findall(r'([\d,]+\.\d+)', current_page_text)
    print(f'\nUsing total_draft_keyword: "{total_draft_keyword}"\nGetting total_draft_matches: {total_draft_matches}\n')
    if not total_draft_matches:
        print(f"No matches for regular expression in current_page_text\n*****************************************************\n {total_draft_keyword}\n*****************************************************\n")
        return None, None, None
    total_draft_amt = total_draft_matches[-1]

    # Extract EFT number
    eft_num_pattern = target_keywords[1]  # Assuming keyword is something like 'EFT-'
    eft_num_matches = re.findall(eft_num_pattern, current_page_text)
    if not eft_num_matches:
        print(f"No matches for regular expression in current_page_text: {eft_num_pattern}")
        return None, None, None
    eft_num = eft_num_matches[0]

    today = datetime.date.today().strftime('%m-%d-%y')

    return eft_num, today, total_draft_amt

def get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name):
    full_path_to_downloaded_pdf = os.path.join(download_dir, f"{keyword_in_dl_file_name}.pdf")
    print(f'full_path_to_downloaded_pdf: {full_path_to_downloaded_pdf}')
    return full_path_to_downloaded_pdf


def process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping, start_idx=None):
    # Extract the text of the current page
    current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

    print(f'current_page_text: {current_page_text}')

    # Check each company
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        if company_name in current_page_text:
            print(f"Processing page {page_num + 1} for {company_name}")  # page number starts from 1 for user's perspective
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

            # Update the start index of the PDF slice by calling split_pdf_pages_on_markers
            start_idx = split_pdf_pages_on_markers(current_page_text, page_num, new_file_name, company_name, 'END MSG', destination_dir, pdf, start_idx)
            print(f'Saving page {page_num + 1} to {destination_dir} with new file name: {new_file_name}')

    return start_idx  # Return the start_idx to pass it to the next call of process_page

def process_pdf(keyword_in_dl_file_name, company_name_to_company_subdir_mapping, download_dir, company_name_to_search_keyword_mapping, pdf):
    try:
        # Get all matching files
        full_path_to_downloaded_pdf = get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name)

        # Read original PDF from dls dir
        print(f'Processing file: {full_path_to_downloaded_pdf}')
        with pikepdf.open(full_path_to_downloaded_pdf) as pdf:
            start_idx = None  # Initialize start_idx to None
            for page_num in range(len(pdf.pages)):
                start_idx = process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping, start_idx)  # Pass start_idx to process_page and update it

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False
