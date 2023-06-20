import os
import re
import shutil
import datetime
import pikepdf
from PyPDF2 import PdfReader
from pdfreader import SimplePDFViewer


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

# TODO: Debug - messes up the splitting of pages based on markers.
def split_pdf_pages_on_markers(text, page_num, new_file_name, start_marker, end_marker, destination_dir, pdf):

    start_idx = None
    end_idx = None

    if start_marker in text and start_idx is None:
        start_idx = page_num

    if end_marker in text:
        end_idx = page_num
        # Create new pdf obj
        new_pdf = pikepdf.Pdf.new()

        # Append pages from start_idx to current page
        new_pdf.pages.extend(pdf.pages[start_idx:end_idx + 1])
        total_pages_per_file = pdf.pages[start_idx:end_idx + 1]
        print(f'Saving PDF: {new_file_name} from page {start_idx} to {end_idx} for a total of {len(total_pages_per_file)} page(s)\nUsed start_marker: {start_marker} and end_marker: {end_marker}')

        # Save the new pdf with new filename in appropriate dest directory
        new_pdf.save(os.path.join(destination_dir, new_file_name))

        # Reset start and end indices for slicing the next set of page(s)
        start_idx = None
        end_idx = None

    # Edge case if start_marker found but no end_marker found, then just turn everything from start_marker to the end of the pdf as single pdf
    if start_idx is not None and end_idx is None:
        new_pdf = pikepdf.Pdf.new()
        new_pdf.pages.extend(pdf.pages[start_idx:])
        new_pdf.save(os.path.join(destination_dir, new_file_name))



# EFT Draft Notices
# def save_pdf_page_as_new_file(page, new_file_name, destination_dir):
#     # Create new Pdf object
#     new_pdf = pikepdf.Pdf.new()
#
#     # Append the page to the new Pdf object
#     new_pdf.pages.append(page)
#
#     # Construct the full path for the new PDF file
#     full_path_to_new_file = os.path.join(destination_dir, new_file_name)
#
#     # TODO: "if "END MSG" is hit, then save page or pages as a single PDF
#     # Save the new Pdf object as a file at the specified path
#     new_pdf.save(full_path_to_new_file)

def pdf_and_pages(pdf):
    for page_num in range(len(pdf.pages)):
        yield page_num, pdf.pages[page_num]

def extract_info_from_text(text, target_keywords):
    """Extract the specific information from a page"""

    # Extract total_draft
    total_draft_keyword = target_keywords[0]
    total_draft_matches = re.findall(r'([\d,]+\.\d+)', text)
    print(f'Using total_draft_keyword: {total_draft_keyword} and getting total_draft_matches: {total_draft_matches}')
    if not total_draft_matches:
        print(f"No matches for regular expression in text: {total_draft_keyword}")
        return None, None, None
    total_draft_amt = total_draft_matches[0]
    # TODO: once split_pdf_pages_on_markers works as intended and is validated, replace ^ with `total_draft_amt = total_draft_matches[-1]`

    # Extract EFT number
    eft_num_pattern = target_keywords[1]  # Assuming keyword is something like 'EFT-'
    eft_num_matches = re.findall(eft_num_pattern, text)
    if not eft_num_matches:
        print(f"No matches for regular expression in text: {eft_num_pattern}")
        return None, None, None
    eft_num = eft_num_matches[0]

    today = datetime.date.today().strftime('%m-%d-%y')

    return eft_num, today, total_draft_amt

def get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name):
    full_path_to_downloaded_pdf = os.path.join(download_dir, f"{keyword_in_dl_file_name}.pdf")
    print(f'full_path_to_downloaded_pdf: {full_path_to_downloaded_pdf}')
    return full_path_to_downloaded_pdf


# @dev: 0-idxing default of `enumerate` for start_count assigned to `page_num` resulted in "islice must be None or an int" error as SimplePDFViewer's `navigate()` 1-idxs hence `page_num + 1`
def process_page(viewer, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping, pdf):
    viewer.navigate(page_num + 1)  # navigating starts from 1, not 0
    viewer.render()

    # Get page content as text
    text = ' '.join(viewer.canvas.strings)
    print(f'text: {text}')

    # Check each company
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        if company_name in text:
            print(f"Processing page {page_num + 1} for {company_name}")  # page number starts from 1 for user's perspective
            eft_num, today, total_draft_amt = extract_info_from_text(text, keywords)
            print(f'eft_num: {eft_num} | today: {today}  | total_draft_amt: {total_draft_amt}')

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

            for page_num_pike, page_obj in pdf_and_pages(pdf):
                if page_num_pike == page_num:
                    # save_pdf_page_as_new_file(page_obj, new_file_name, destination_dir)

                    split_pdf_pages_on_markers(text, page_num, new_file_name, company_name, 'END_MSG', destination_dir, pdf)
                    print(f'Saving page {page_num_pike + 1} to {destination_dir} with new file name: {new_file_name}')



def process_pdf(keyword_in_dl_file_name, company_name_to_company_subdir_mapping, download_dir, company_name_to_search_keyword_mapping, pdf):
    try:
        # Get all matching files
        full_path_to_downloaded_pdf = get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name)

        # Read original PDF from dls dir
        print(f'Processing file: {full_path_to_downloaded_pdf}')
        with open(full_path_to_downloaded_pdf, 'rb') as f:
            viewer = SimplePDFViewer(f)

            for page_num, page in enumerate(viewer.doc.pages()):
                process_page(viewer, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping, pdf)

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False