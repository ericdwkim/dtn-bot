import os
import re
import time
import pikepdf
import shutil
from datetime import datetime
from utils.post_processing import merge_rename_and_summate, calculate_directory_path, is_last_day_of_month, end_of_month_operations, get_root_directory
from utils.extraction_handler import extract_text_from_pdf_page, extract_info_from_text, extract_company_dir_from_map

def rename_and_delete_pdf(file_path):
    """
    Given a full path to a PDF file, depending on the regex_num found on first page of PDF, it will rename and delete. Hedges against deleting any random PDF. Used for cleaning merged PDFs after post-processing to declutter Downloads dir.
    :param file_path:
    :return: `file_deleted` Bool
    """
    file_deleted = False
    today = datetime.today().strftime('%m-%d-%y')  # @today
    # today = '07-23-23'



    if os.path.exists(file_path):
        pdf = pikepdf.open(file_path)  # Open the PDF file
        if len(pdf.pages) > 0:
            # @dev: Extract text content from first page
            first_page = extract_text_from_pdf_page(pdf.pages[0])

            # todo: clean this up; very confusing. why double ccm?
            if re.search(r'EFT-\d+', first_page) or re.search(r'CMB-\d+ | CCM-\d+ | LRD-\d+', first_page):
                if re.search(r'EFT-\d+', first_page):
                    new_file_name = f'EFT-{today}-TO-BE-DELETED.pdf'
                else:
                    new_file_name = f'CCM-{today}-TO-BE-DELETED.pdf'

                file_directory = os.path.dirname(file_path)
                new_file_path = os.path.join(file_directory, new_file_name)

                print(f"Renaming file: {file_path} to {new_file_path}")
                pdf.close()  # Close the PDF file
                os.rename(file_path, new_file_path)
                file_deleted = True
                print("File renamed successfully.")
                time.sleep(3)

                if os.path.exists(new_file_path):
                    print(f"Deleting file: {new_file_path}")
                    os.remove(new_file_path)
                    print("File deleted successfully.")

    return file_deleted

# Renaming helper func for Invoices PDF
def rename_invoices_pdf(file_path):
    """
    Find `messages.pdf` for Invoices in Downloads directory and rename it
    :param file_name:
    :param source_dir:
    :return:
    """
    today = datetime.today().strftime('%m-%d-%y')  # @today
    # today = '07-23-23'


    if os.path.exists(file_path):
        pdf = pikepdf.open(file_path) # open Invoices PDF as pikePDF object
        new_file_name = today + '.pdf'

        file_directory = os.path.dirname(file_path)
        new_file_path = os.path.join(file_directory, new_file_name)

        print(f'Renaming file {file_path} to {new_file_path}')
        pdf.close() # Close PDF file
        os.rename(file_path, new_file_path)
        if os.path.exists(new_file_path):
           print("File renamed successfully.")
           time.sleep(3)
           return True, new_file_path, new_file_name
        else:
            print(f'Could not rename Invoices `messages.pdf` file in Downloads directory')
            return False, None, None

def get_file_timestamps(file_path):
    """
    Helper function to get creation and modification times of a file
    """
    mod_time = os.path.getmtime(file_path)
    cre_time = os.path.getctime(file_path)

    # convert the time from seconds since the epoch to a datetime object
    mod_time = datetime.fromtimestamp(mod_time)
    cre_time = datetime.fromtimestamp(cre_time)

    return mod_time, cre_time

# Refactored `rename_and_move_pdf`
def rename_and_move_or_overwrite_invoices_pdf(file_path):
    renamed_file, new_file_path, new_file_name = rename_invoices_pdf(file_path)

    if not (renamed_file and new_file_path and new_file_name):
        return False

    # Get final output directory from file prefix
    month_dir = calculate_directory_path('INV')

    # Construct target_file_path variable
    target_file_path = os.path.join(month_dir, new_file_name)

    # Get timestamps for new Invoices file
    mod_time_new, cre_time_new = get_file_timestamps(new_file_path)

    # If file with same name exists in target directory
    if os.path.isfile(target_file_path):
        mod_time_old, cre_time_old = get_file_timestamps(target_file_path)

        print(
            f'File with name: "{new_file_name}" already exists at "{target_file_path}"\nLast modified (old): {mod_time_old} | Last modified (new): {mod_time_new}\nCreated (old): {cre_time_old} | Created (new): {cre_time_new}\nOverwriting duplicate file with latest modified/created...')
        os.remove(target_file_path)

    try:
        shutil.move(new_file_path, month_dir)
        print(f'Moved latest Invoices pdf created on "{cre_time_new}" to "{month_dir}"')
        return True  # File moved successfully
    except Exception as e:
        print(f'An error occurred while moving the file: {e}')
        return False  # File could not be moved

def get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name):
    """
    Given the Downloads directory path and substring keyword to search in filename, it returns the combined full path to Downloads dir. Will be deprecated in next version due to redundancy.
    :param download_dir:
    :param keyword_in_dl_file_name:
    :return:
    """
    full_path_to_downloaded_pdf = os.path.join(download_dir, f"{keyword_in_dl_file_name}.pdf")
    return full_path_to_downloaded_pdf


def create_and_save_pdf(pages, new_file_name, company_dir):
    """
    Given a list a pikePdf pages object, it will create a PDF from all page objects with given new_file_name and outputs to constructed output_filepath from company_dir
    :param pages: List of pikePDF pages
    :param new_file_name: newly constructed filename for new PDF
    :param company_dir: string path to company name directory
    :return:
    """
    file_prefix = new_file_name.split("-")[0]
    try:
        new_pdf = pikepdf.Pdf.new()
        new_pdf.pages.extend(pages)

        # Use file_prefix as key to get doc type `root_dir` from map; "subtract" company_dir to root_dir to get company name var; use company_name as conditional check to separate CCM EXXONMOBIL files to company_dir for post-processing and non ExxonMobil ccm files to month_dir pathing as expected
        # @dev: CCM, LRD files are temporarily saved in company_dir prior to post-processing to prepare for merge_rename_and_summate
        # TODO: easier way to have company name var?
        credit_cards_doc_type_dir = get_root_directory('CCM')
        print(f'credit_cards_doc_type_dir: {credit_cards_doc_type_dir}')
        company_name = company_dir.replace(credit_cards_doc_type_dir, '')
        print(f'company_name: {company_name}')
        if (file_prefix == 'CCM' or file_prefix == 'LRD') and company_name == 'EXXONMOBIL [10005]':
            print('***************************************')
            output_filepath = os.path.join(company_dir, new_file_name)
            print(f' CCM EXXON ONLY - output filepath ------- {output_filepath}')

        # Dynamic filesystem management for Fuel Drafts (EFT) and Combined Message (CMB) document types
        else:
            month_dir = calculate_directory_path(file_prefix, None, company_dir)
            output_filepath = os.path.join(month_dir, new_file_name)
            print(f'output_filepath: ----------- {output_filepath}')
        new_pdf.save(output_filepath)
        return True  # Return True if the file was saved successfully

    except Exception as e:
        print(f"Error occurred while creating and saving PDF: {str(e)}")
        return False  # Return False if an error occurred

def get_new_file_name(regex_num, today, total_target_amt):
    """
    Given regex_num, today's date, and total_target_amt, returns constructed new_file_name depending on document type
    :param regex_num: The numbers that succeed of a document type, ie: `EFT-1234`, would be `1234`
    :param today:
    :param total_target_amt: total_amt fetched from last in list of total_amount_matches array
    :return:
    """
    # File naming convention for total_target_amt preceding/succeeding with a hyphen indicative of a balance owed
    if re.match(r'EFT-\s*\d+', regex_num) and re.match(r'-?[\d,]+\.\d+-?', total_target_amt):
        if "-" in total_target_amt:  # Checks if "-" exists anywhere in total_target_amt
            total_target_amt = total_target_amt.replace("-", "")  # Removes "-"
            new_file_name = f'{regex_num}-{today}-({total_target_amt}).pdf'
        else:  # No "-" in total_target_amt
            new_file_name = f'{regex_num}-{today}-{total_target_amt}.pdf'

    # File naming convention for chargebacks/retrievals
    # @dev: regex_num is included due to edge case of identical filenames overwriting
    # eg: VALERO CBK-0379 gets overwritten by RTV-0955 if regex_num is not included
    elif (re.match(r'CBK-\s*\d+', regex_num) or re.match(r'RTV-\s*\d+', regex_num)):
        new_file_name = f'{regex_num}-{today}-CHARGEBACK REQUEST.pdf'

    # File naming convention for all other files (CCM, CMB, positive ETF `total_amount` values)
    else:
        new_file_name = f'{regex_num}-{today}-{total_target_amt}.pdf'
    # print(f'new_file_name: {new_file_name}')
    return new_file_name


def process_multi_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping):
    """
    Processes original PDF file for all multi-page spanning "mini" PDFs
    :param pdf: pike PDF instance
    :param page_num: cursor to keep track of currently processing page number of original PDF
    :param company_names: List of all company names
    :param regex_patterns: Set of all document type patterns using regex
    :param company_name_to_company_subdir_mapping: Maps company name using typically spelled convention in PDF pages to company subdirectory names DTN Reports/`Company A [company_id]`
    :return: page_num (int)
    """
    current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
    print(f'Processing page: {page_num + 1}')  # @dev: accounts for 0 indexed page number for user facing simplicity

    for company_name in company_names:
        # Handles CCM, CMB, LRD multi page docs
        if company_name in current_page_text and 'END MSG' not in current_page_text:
            for pattern in regex_patterns:
                if re.search(pattern, current_page_text, re.IGNORECASE):

                    current_pages = []
                    current_page_texts = []

                    while 'END MSG' not in current_page_text and page_num < len(pdf.pages):
                        current_pages.append(pdf.pages[page_num])
                        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
                        current_page_texts.append(current_page_text)

                        page_num += 1

                        if page_num >= len(pdf.pages):
                            break

                    current_page_text = "".join(current_page_texts)

                    regex_num, today, total_amount = extract_info_from_text(current_page_text, pattern)
                    new_file_name = get_new_file_name(regex_num, today, total_amount)
                    # print(f'\n*********************************************\n multi new_file_name\n*********************************************\n {new_file_name}')
                    company_dir = company_name_to_company_subdir_mapping[company_name]
                    # print(f'####### company_dir: {company_dir}')
                    create_and_save_pdf(current_pages, new_file_name, company_dir)

    return page_num


def process_single_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping):
    """
    Processes all single paged PDFs
    :param pdf: pikePDF instance
    :param page_num: page cursor
    :param company_names: List
    :param regex_patterns: Set
    :param company_name_to_company_subdir_mapping: Maps company name using typically spelled convention in PDF pages to company subdirectory names DTN Reports/`Company A [company_id]`
    :return: int
    """
    current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
    print(f'Processing page: {page_num + 1}')

    for company_name in company_names:
        # Handle single page CCM, CBK, RTV, ETF files
        if company_name in current_page_text and 'END MSG' in current_page_text:
            for pattern in regex_patterns:
                if re.search(pattern, current_page_text, re.IGNORECASE):
                    current_pages = [pdf.pages[page_num]]
                    regex_num, today, total_amount = extract_info_from_text(current_page_text, pattern)
                    new_file_name = get_new_file_name(regex_num, today, total_amount)
                    # print(f'\n*********************************************\n single new_file_name\n*********************************************\n {new_file_name}')
                    company_dir = company_name_to_company_subdir_mapping[company_name]
                    create_and_save_pdf(current_pages, new_file_name, company_dir)

                    page_num += 1

                    if page_num >= len(pdf.pages):
                        break

    return page_num

def process_pages(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns, is_multi_page):
    """
    Wrapper for both process_multi and process_single of original PDF file. Accounts for page_num cursor. Keeps original PDF object open using `with` keyword. Will be deprecated in next version.
    :param filepath: Downloads directory path
    :param company_name_to_company_subdir_mapping:
    :param company_names: List
    :param regex_patterns: Set
    :param is_multi_page: Bool (flag) to indicate whether pages being processed is multi spanning or not
    :return: Bool
    """
    try:

        # Read original PDF from dls dir
        print(f'Processing file: {filepath}')
        with pikepdf.open(filepath) as pdf:
            page_num = 0  # Initialize page_num
            while page_num < len(pdf.pages):
                # print(f'page_num: {page_num + 1}')

                # Process pages and update the page number at original PDF (macro) level
                if is_multi_page:
                    new_page_num = process_multi_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping)
                else:
                    new_page_num = process_single_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping)

                # if process_page has not incremented
                # prevents one off issue
                if new_page_num == page_num:
                    page_num += 1
                else:
                    page_num = new_page_num

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False


def process_pdfs(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns,
                 post_processing=False):
    """
    Wrapper for process_pages of both multi and single page processing instances. Accounts for last day of month processes for all file types, companies for dynamic file system management
    :param filepath: Downloads directory path
    :param company_name_to_company_subdir_mapping:
    :param company_names: List
    :param regex_patterns: Set
    :param post_processing: Bool (flag) used to indicate whether merge_rename_and_summate required or not
    :return:
    """
    try:
        # print(f'----------------------------- {filepath}')
        print(f'Processing all single-page files....\n')
        single_pages_processed = process_pages(filepath, company_name_to_company_subdir_mapping, company_names,
                                               regex_patterns, is_multi_page=False)
        if single_pages_processed:
            print(f'Successfully finished processing all single-paged files\n')

        print(f'Now processing all multi-page files....\n')
        multi_pages_processed = process_pages(filepath, company_name_to_company_subdir_mapping, company_names,
                                              regex_patterns, is_multi_page=True)
        if multi_pages_processed:
            print(f'Successfully finished processing all multi-paged files\n')

        # Conditional post-processing only for EXXON CCMs and LRDs
        if single_pages_processed and multi_pages_processed and post_processing is True:
            print(f'Post processing for EXXON CCMs & LRDs')
            exxon_company_dir = company_name_to_company_subdir_mapping['EXXONMOBIL']
            merge_rename_and_summate(exxon_company_dir)

        elif single_pages_processed and multi_pages_processed and post_processing is False and is_last_day_of_month() is True:

            # End of month operations for EFTs
            company_dirs = extract_company_dir_from_map()
            for company_name, company_dir in zip(company_names, company_dirs):
                print(f"The subdirectory for {company_name} is: {company_dir}")
                end_of_month_operations(company_dir)

        return single_pages_processed and multi_pages_processed

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return False

