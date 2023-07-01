import os
import re
from time import sleep
from pikepdf import open, Pdf
from shutil import move
import datetime
from company_getters import get_company_id, get_company_names
from utils.post_processing import merge_rename_and_summate
from utils.extraction_handler import extract_text_from_pdf_page, extract_info_from_text
from utils.filesystem_manager import end_of_month_operations, calculate_directory_path, is_last_day_of_month, cleanup_files
from utils.mappings_refactored import doc_type_abbrv_to_doc_type_subdir_map, regex_patterns


# pdf_handler as a class following OOP
class PdfProcessor:

    # ---------------------------------- Instance attributes ----------------------------------
    def __init__(self, file_path, doc_type, company_id, total_target_amt):
        self.file_path = file_path
        self.new_file_name = None  # Instance variable to hold the new file name
        self.doc_type = doc_type
        self.company_id = company_id
        self.total_target_amt = total_target_amt

        # Construct the file_path_mappings using doc_type and company_id
        self.file_path_mappings = {
            self.doc_type: {
                self.company_id: os.path.join
                    (
                self.root_dir,
                doc_type_abbrv_to_doc_type_subdir_map[self.doc_type],
                company_id_to_subdir_mapping[self.company_id]
                )
            }
        }

    # ----------------------------------  Class Attributes ----------------------------------
    root_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports'
    download_dir = r'/Users/ekim/Downloads'
    today = datetime.date.today().strftime('%m-%d-%y')
    # ----------------------------------  Class Attributes ----------------------------------

    def rename_and_delete_pdf(self):
        file_deleted = False
        # access self.file_path instead of the file_path argument
        if os.path.exists(self.file_path):
            with open(self.file_path) as pdf:
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
                        sleep(3)

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
                target_dir = os.path.join(self.root_dir, self.doc_type_abbrv_to_doc_type_subdir_map[self.doc_type])
                destination_file = os.path.join(target_dir, f'{self.today}.pdf')
                print(f'Moving {destination_file} to {target_dir}')
                move(source_file, destination_file)
                break

    def create_and_save_pdf(self, pages):
        try:
            new_pdf = Pdf.new()
            new_pdf.pages.extend(pages)
            output_path = self.file_path_mappings[self.doc_type][self.company_id]
            output_path = os.path.join(output_path, self.new_file_name)
            new_pdf.save(output_path)
            return True  # Return True if the file was saved successfully
        except Exception as e:
            print(f"Error occurred while creating and saving PDF: {str(e)}")
            return False  # Return False if an error occurred


    def get_new_file_name(self, regex_num):
        if re.match(r'EFT-\s*\d+', regex_num) and re.match(r'-?[\d,]+\.\d+-?', self.total_target_amt):
            if "-" in self.total_target_amt:
                total_target_amt = self.total_target_amt.replace("-", "")
                self.new_file_name = f'{regex_num}-{self.today}-({total_target_amt}).pdf'
            else:
                self.new_file_name = f'{regex_num}-{self.today}-{self.total_target_amt}.pdf'
        elif (re.match(r'CBK-\s*\d+', regex_num) or re.match(r'RTV-\s*\d+', regex_num)):
            self.new_file_name = f'{regex_num}-{self.today}-CHARGEBACK REQUEST.pdf'
        else:
            self.new_file_name = f'{regex_num}-{self.today}-{self.total_target_amt}.pdf'
        return self.new_file_name

    def process_multi_page(self, pdf, page_num, regex_patterns):
        company_names = get_company_names(company_id_to_company_subdir_map)
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
        print(f'Processing page: {page_num + 1}')

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

                        regex_num, self.today, self.total_target_amt = extract_info_from_text(current_page_text, pattern)
                        self.get_new_file_name(regex_num)
                        print(f'\n*********************************************\n multi new_file_name\n*********************************************\n {self.new_file_name}')
                        self.create_and_save_pdf(current_pages)

        return page_num

    def process_single_page(self, pdf, page_num, regex_patterns):
        company_names = get_company_names(company_id_to_company_subdir_map)
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
        print(f'Processing page: {page_num + 1}')

        for company_name in company_names:
            # Handle single page CCM, CBK, RTV, ETF files
            if company_name in current_page_text and 'END MSG' in current_page_text:
                for pattern in regex_patterns:
                    if re.search(pattern, current_page_text, re.IGNORECASE):
                        current_pages = [pdf.pages[page_num]]
                        regex_num, self.today, self.total_target_amt = extract_info_from_text(current_page_text, pattern)
                        self.get_new_file_name(regex_num)
                        print(f'\n*********************************************\n single new_file_name\n*********************************************\n {self.new_file_name}')
    def process_pages(self, regex_patterns,
                      is_multi_page):
        file_path = self.file_path_mappings[self.doc_type][self.company_id]

        try:

            # Read original PDF from downloads dir
            print(f'Processing file: {file_path}')
            with open(file_path) as pdf:
                page_num = 0 # Initialize page_num
                while page_num < len(pdf.pages):
                    print(f'page_num: {page_num + 1}') # zero-idx; user facing 1-idx

                    # Process pages and update the pagge num at original PDF (macro) level)
                    if is_multi_page:
                        new_page_num = self.process_multi_page(pdf, page_num, regex_patterns)
                    else:
                        new_page_num = self.process_single_page(pdf, page_num, regex_patterns)

                    # if process_page has not incremented; prevents one-off issue
                    if new_page_num == page_num:
                        page_num += 1
                    else:
                        page_num = new_page_num

                # if all pages processed w/o errors, return True
                return True

        except Exception as e:
            # if any error occurred, print and return False
            print(f'An unexpected error occurred: {str(e)}')
            return False

    @staticmethod
    def process_pdfs(self, regex_patterns,
                 doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map, post_processing=False):

        file_path = self.file_path_mappings[self.doc_type][self.company_id]

        try:

            # print(f'----------------------------- {file_path}')
            # print(f'Processing all single-page files....\n')
            single_pages_processed = process_pages(file_path, company_names,
                                                   regex_patterns, is_multi_page=False)
            if single_pages_processed:
                print(f'Successfully finished processing all single-paged files\n')

            # print(f'Now processing all multi-page files....\n')
            multi_pages_processed = process_pages(file_path, company_names,
                                                  regex_patterns, is_multi_page=True)
            if multi_pages_processed:
                print(f'Successfully finished processing all multi-paged files\n')

            # Conditional post processing only for EXXON CCMs and LRDs
            if single_pages_processed and multi_pages_processed and post_processing is True:
                # print(f'Post processing for EXXON CCMs & LRDs')
                output_path = self.file_path_mappings[self.doc_type][self.company_id]
                merge_rename_and_summate(output_path, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)

            # Dynamic filesystem mgmt when post processing is False and
            elif single_pages_processed and multi_pages_processed and post_processing is False and is_last_day_of_month():
                end_of_month_operations(self.new_file_name)

            else:
                return single_pages_processed and multi_pages_processed

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False

