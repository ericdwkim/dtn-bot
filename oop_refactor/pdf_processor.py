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


class PdfProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.today = datetime.date.today().strftime('%m-%d-%y')
        self.new_file_name = None  # Instance variable to hold the new file name

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
    def rename_and_move_pdf(file_name, source_dir, target_dir):
        # ...
        # This function does not need to be updated, as it does not rely on the directory structure.
        # ...

    def get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name):
        # This function does not need to be updated, as it does not rely on the directory structure.

    def create_and_save_pdf(pages, new_file_name, destination_dir):
        # ...
        # This function does not need to be updated, as it does not rely on the directory structure.
        # ...

    def get_new_file_name(regex_num, today, total_target_amt):
        # ...
        # This function does not need to be updated, as it does not rely on the directory structure.
        # ...

    def process_multi_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping):
        # This function does not need to be updated, as it does not rely on the directory structure.

    def process_single_page(pdf, page_num, company_names, regex_patterns, company_name_to_company_subdir_mapping):
        # This function does not need to be updated, as it does not rely on the directory structure.

    def process_pages(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns, is_multi_page):
        # This function does not need to be updated, as it does not rely on the directory structure.

    def process_pdfs(filepath, company_name_to_company_subdir_mapping, company_names, regex_patterns, doc_type_abbrv_to_doc_type_map, company_id_to_company_subdir_map,
                     post_processing=False):
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
