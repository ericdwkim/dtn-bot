import os
import re
import time
import pikepdf
import shutil
import pdfplumber
import datetime
from utils.post_processing import merge_rename_and_summate
from utils.extraction_handler import extract_text_from_pdf_page, extract_info_from_text
from utils.filesystem_manager import end_of_month_operations, calculate_directory_path, is_last_day_of_month, cleanup_files



# pdf_handler as a class following OOP
class PdfProcessor:

    # ---------------------------------- Instance attributes ----------------------------------
    def __init__(self, file_path, doc_type):
        self.file_path = file_path
        self.new_file_name = None  # Instance variable to hold the new file name
        self.doc_type = doc_type

    # ----------------------------------  Class Attributes ----------------------------------
    root_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports'
    download_dir = r'/Users/ekim/Downloads'
    today = datetime.date.today().strftime('%m-%d-%y')

    # Mapping from company id to company directory
    company_id_to_company_subdir_map = {
        '10482': 'COFFEYVILLE [10482]',
        '12351': 'CVR Supply & Trading 12351',
        '12293': 'DK TRADING [12293]',
        '10005': 'EXXONMOBIL [10005]',
        '11177': 'FLINT HILLS [11177]',
        '10351': 'FRONTIER [10351]',
        '10350': 'FUEL MASTERS [10350]',
        '11465': 'JUNIPER [11465]',
        '12123': 'LA LOMITA [12123]',
        '11480': 'MANSFIELD OIL [11480]',
        '11096': 'MERITUM - PICO [11096]',
        '10420': 'MOTIVA [10420]',
        '12170': 'OFFEN PETROLEUM [12170]',
        '10007': 'PHILLIPS [10007]',
        '11293': 'SEIFS [11293]',
        '11613': 'SUNOCO [11613]',
        '10280': 'TEXAS TRANSEASTERN [10280]',
        '12262': 'U S VENTURE - U S OIL COMPANY [12262]',
        '10006': 'VALERO [10006]',
        '10778': 'WINTERS OIL [10778]',
    }

    # Mapping from document type to its respective directory under the root directory
    doc_type_to_subdir_mapping = {
        ('CCM', 'LRD'): 'Credit Cards',
        'EFT': 'Fuel Drafts',
        'INV': 'Fuel Invoices',
    }

    # Mapping of document type to company ID to file path
    file_path_mappings = {
        doc_type: {
            company_id: os.path.join(root_dir, doc_type_to_subdir_mapping[doc_type], company_dir)
            for company_id, company_dir in company_id_to_subdir_mapping.items()
        }
        for doc_type in doc_type_to_subdir_mapping.keys()
    }

    # Company names and regex patterns
    company_names = ['VALERO', 'CONCORD FIRST DATA RETRIEVAL', 'EXXONMOBIL', 'U.S. OIL COMPANY', 'DK Trading & Supply', 'CVR SUPPLY & TRADING, LLC']
    regex_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}

    # ----------------------------------  Class Attributes ----------------------------------



    def rename_and_delete_pdf(self):
        file_deleted = False
        # access self.file_path instead of the file_path argument
        if os.path.exists(self.file_path):
            with pikepdf.open(self.file_path) as pdf:
                if len(pdf.pages) > 0:
                    first_page = extract_text_from_pdf_page(pdf.pages[0])

                    if re.search(r'EFT-\d+', first_page) or re.search(r'CCM-\d+ | CMD-\d+', first_page):
                        if re.search(r'EFT-\d+', first_page):
                            self.new_file_name = f'EFT-{self.today}-TO-BE-DELETED.pdf'
                        else:
                            self.new_file_name = f'CCM-{self.today}-TO-BE-DELETED.pdf'

                        file_directory = os.path.dirname(self.file_path)
                        new_file_path = os.path.join(file_directory, self.new_file_name)

                        print(f"Renaming file: {self.file_path} to {new_file_path}")
                        os.rename(self.file_path, new_file_path)
                        file_deleted = True
                        print("File renamed successfully.")
                        time.sleep(3)

                        if os.path.exists(new_file_path):
                            print(f"Deleting file: {new_file_path}")
                            os.remove(new_file_path)
                            print("File deleted successfully.")

                return file_deleted

    # Invoices
    def rename_and_move(self):
        """Helper function to rename and move a PDF file"""
        for file in os.listdir(self.download_dir):
            if file.endswith('.pdf') and "messages" in file:  # static string "messages" for now
                source_file = os.path.join(self.download_dir, file)
                target_dir = os.path.join(self.root_dir, self.doc_type_to_subdir_mapping[self.doc_type])
                destination_file = os.path.join(target_dir, f'{self.today}.pdf')
                print(f'Moving {destination_file} to {target_dir}')
                shutil.move(source_file, destination_file)
                break

    """
    rename_and_move use example:
    processor = PdfProcessor('INV') 
    processor.rename_and_move()
    """


    def create_and_save_pdf(self, pages):
        try:
            new_pdf = pikepdf.Pdf.new()
            new_pdf.pages.extend(pages)
            output_path = self.file_path_mappings[self.doc_type][self.company_id]
            output_path = os.path.join(output_path, self.new_file_name)
            new_pdf.save(output_path)
            return True  # Return True if the file was saved successfully
        except Exception as e:
            print(f"Error occurred while creating and saving PDF: {str(e)}")
            return False  # Return False if an error occurred


    def get_new_file_name(regex_num, today, total_target_amt):
        # @dev: only EFTs that follow this convention
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
        # This function does not need to be updated, as it does not rely on the directory structure.

    def process_single_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping):
        # This function does not need to be updated, as it does not rely on the directory structure.

    def process_pages(company_id, doc_type, company_name_to_company_subdir_mapping, company_names, regex_patterns,
                      is_multi_page):
        file_path = self.file_path_mappings[doc_type][company_id]

    def process_pdfs(company_id, doc_type, company_name_to_company_subdir_mapping, company_names, regex_patterns,
                 doc_type_abbrv_to_doc_type_map, company_id_to_company_subdir_map, post_processing=False):

        file_path = self.file_path_mappings[doc_type][company_id]

        try:
            print(f'----------------------------- {filepath}')
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

            # Conditional post processing only for EXXON CCMs and LRDs
            if single_pages_processed and multi_pages_processed and post_processing is True:
                print(f'Post processing for EXXON CCMs & LRDs')
                output_directory_exxon = company_name_to_company_subdir_mapping['EXXONMOBIL']
                merge_rename_and_summate(output_directory_exxon, doc_type_abbrv_to_doc_type_map, company_id_to_company_subdir_map)

            # Dynamic filesystem mgmt when post processing is False and
            elif single_pages_processed and multi_pages_processed and post_processing is False and is_last_day_of_month():
                directory, filename = os.path.split(filepath)
                end_of_month_operations(directory, filename)

            else:
                return single_pages_processed and multi_pages_processed

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False


# Usage:
processor = PdfProcessor("example.pdf")
processor.rename_and_delete_pdf()
