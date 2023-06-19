import os
import re
import shutil
import datetime
import pikepdf

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


def extract_info_from_text(text, target_keywords):
    """Extract the specific information from a page"""

    # Extract total_draft
    total_draft_keyword = target_keywords[0]
    total_draft_matches = re.findall(r'(\d+\.\d+)', text)
    if not total_draft_matches:
        print(f"No matches for regular expression in text: {total_draft_keyword}")
        return None, None, None
    total_draft_amt = total_draft_matches[0]

    # Extract EFT number
    eft_num_pattern = target_keywords[1]  # Assuming keyword is something like 'EFT-'
    eft_num_matches = re.findall(eft_num_pattern, text)
    if not eft_num_matches:
        print(f"No matches for regular expression in text: {eft_num_pattern}")
        return None, None, None
    eft_num = eft_num_matches[0]

    today = datetime.date.today().strftime('%m-%d-%y')

    return eft_num, today, total_draft_amt


# TODO: reimplement into process_pdf to account for default filename of dl'd PDF
def get_matching_pdf_file(keyword_in_dl_file_name, download_dir):
    matching_file = os.path.join(download_dir, f"{keyword_in_dl_file_name}.pdf")
    print(f'matching_file: {matching_file}')
    return matching_file



def process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):

    page = pdf.pages[page_num]

    # Check each company
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        if company_name in text:
            print(f"Processing page {page_num + 1} for {company_name}")  # page number starts from 1 for user's perspective
            eft_num, today, total_draft_amt = extract_info_from_text(text, keywords)
            print(f'-----------------eft_num: {eft_num} | today: {today}  | total_draft_amt: {total_draft_amt}')

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
            full_path_to_renamed_company_file = os.path.join(destination_dir, new_file_name)
            print(f'full_path_to_renamed_company_file: {full_path_to_renamed_company_file}')

            # Save the page to a new PDF
            with pikepdf.Pdf.new() as output_pdf:
                print(f' writing new pdf in correct subdir--------')
                output_pdf.pages.append(page)
                output_pdf.save(full_path_to_renamed_company_file)

            print(f'Moved page {page_num + 1} to {destination_dir} as {new_file_name}\nFull path to new Draft Notice: {full_path_to_renamed_company_file} ')  # page number starts from 1 for user's perspective

def process_pdf(company_name_to_company_subdir_mapping, company_name_to_search_keyword_mapping):

    try:
        matching_file = r'/Users/ekim/Downloads/messages.pdf'

        # Open the PDF
        pdf = pikepdf.Pdf.open(matching_file)

        for page_num in range(len(pdf.pages)):
            process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping)
        return True

    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False
