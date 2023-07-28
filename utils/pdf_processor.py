import os
import re
import time
from glob import glob
import pikepdf
import shutil
from datetime import datetime
from pathlib import Path
from utils.post_processing import merge_rename_and_summate
from extraction_handler import PDFExtractor
from utils.filesystem_manager import end_of_month_operations, calculate_directory_path, is_last_day_of_month, cleanup_files
from utils.mappings_refactored import doc_type_abbrv_to_doc_type_subdir_map, doc_type_patterns, company_id_to_company_subdir_map


class PdfProcessor:
    # ----------------------------------  Class Attributes ----------------------------------
    today = datetime.today().strftime('%m-%d-%y')
    root_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports'
    download_dir = str(Path.home() / "Downloads")
    # ----------------------------------  Class Attributes ----------------------------------

    # ---------------------------------- Instance attributes ----------------------------------
    def __init__(self):
        self.pdf_file_path = self.get_pdf_file_path()
        self.page_num = 0
        self.pdf_data = self.get_pdf(self.pdf_file_path) # PikePDF instance var
        self.extractor = PDFExtractor()
        # self.pages = []
        # self.company_id = self.get_company_id()
        # self.doc_type, self.total_target_amt = (None, None)
        # self.file_path_mappings = None
        # self.assign_file_path_mappings()

    # ---------------------------------- Instance attributes ----------------------------------
    def get_pdf_file_path(self):
        try:
            files = Path(self.download_dir).glob('*messages.pdf')
            tar_file = max(files, key=lambda x: x.stat().st_mtime)
            return str(tar_file)
        except ValueError as e:
            print(f'An error occurred: {e}. Check if `messages.pdf` exists?')

    def get_pdf(self, filepath):
        if os.path.exists(filepath):
            return pikepdf.open(filepath)

    def assign_file_path_mappings(self):
        print('assign_file_path_mappings was called') # TODO
    # def assign_file_path_mappings(self):
    #     print(f'{self.doc_type}   | {self.total_target_amt} | {self.company_name} ' )
    #     print(f'self.doc_type: {self.doc_type}   | self.total_target_amt: {self.total_target_amt} | self.company_name: {self.company_name}  | self.company_id: {self.company_id}' )
    #
    #     self.file_path_mappings = {
    #         self.doc_type: {
    #             self.company_id: os.path.join
    #                 (
    #                 self.root_dir,
    #                 doc_type_abbrv_to_doc_type_subdir_map[self.doc_type],
    #                 company_id_to_company_subdir_map[self.company_id]
    #             )
    #         }
    #     }
    #
    #     # print(f'{self.doc_type}   | {self.total_target_amt} | {self.company_name} ' )
    #     if self.doc_type is None:
    #         print("Error: Document type is None. File path mappings could not be assigned.")
    #         return None
    #
    #     elif self.company_id is None:
    #         print("Error: Company ID is None. File path mappings could not be assigned.")
    #         return None
    #     else:
    #         return self.file_path_mappings

    @staticmethod
    def get_company_names():
        company_names = []
        for company_dir in company_id_to_company_subdir_map.values():
            # Slice the string to remove the company id and brackets
            company_name = company_dir.split('[')[0].strip()
            company_names.append(company_name)
        # print(f'******** {company_names} *******')
        return company_names

    def get_company_name(self, cur_page_text):
        """
        Helper func for getting company_name instance
        :param cur_page_text:
        :return:
        """
        # print(
            # f'\n########################################\n{self.cur_page_text}\n########################################\n')
        for company_name in PdfProcessor.get_company_names():
            # print(f'Checking company_name: {company_name}')
            if company_name in cur_page_text:
                return company_name
        # Return None if no company name is found in the cur_page_text
        return None

    def get_doc_type(self, cur_page_text):
        """
        Helper func for getting doc_type_pattern instance
        :param cur_page_text:
        :return:
        """
        for doc_type_pattern in doc_type_patterns:
            if re.search(doc_type_pattern, cur_page_text, re.IGNORECASE):
                return doc_type_pattern
        return None

    def get_page_text(self):
        while self.page_num < len(self.pdf_data.pages):
            print(f'Processing page number: {self.page_num + 1}')
            self.cur_page_text = self.extractor.extract_text_from_pdf_page(self.pdf_data.pages[self.page_num])
            self.company_name = self.get_company_name(self.cur_page_text)
            self.doc_type_pattern = self.get_doc_type(self.cur_page_text)

        #
            if (self.company_name in self.cur_page_text) and (re.search(self.doc_type_pattern, self.cur_page_text, re.IGNORECASE)) and ('END MSG' not in self.cur_page_text):
                self.process_multi_page()
            else:
                self.page_num += 1

            if self.page_num >= len(self.pdf_data.pages):
                break
        return self.cur_page_text

    def rename_and_delete_pdf(self):
        file_deleted = False
        if os.path.exists(self.file_path):
            with pikepdf.open(self.file_path) as pdf:
                if len(pdf.pages) > 0:
                    first_page = self.extractor.extract_text_from_pdf_page(pdf.pages[0])

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


    # Invoices PDF rename helper
    def rename_invoices_pdf(self):

        # Pass `/Users/ekim/Downloads/messages.pdf` to get PikePDf object
        pdf = self.get_pdf(self.pdf_file_path)


        self.new_file_name = self.today + '.pdf'
        # given the original `messages.pdf` full filepath, return new full filepath
        file_dir = os.path.dirname(self.pdf_file_path)
        new_file_path = os.path.join(file_dir, self.new_file_name)
        print(f'Renaming original Invoices PDF file "{self.pdf_file_path}" to {new_file_path}')

        pdf.close() # Close PDF
        os.rename(self.pdf_file_path, new_file_path)
        # Check file got saved correctly
        if os.path.exists(new_file_path):
            print(f'File renamed successfully.')
            time.sleep(3)
            return True
        else:
            print(f'Could not rename Invoices PDF')
            return False










    # def rename_and_move_refactor(self):

    # Invoices
    def rename_and_move(self):
        """Helper function to rename and move a PDF file"""
        for file in os.listdir(self.download_dir):
            if file.endswith('.pdf') and "messages" in file:  # static string "messages" for now
                source_file = os.path.join(self.download_dir, file)
                target_dir = os.path.join(self.root_dir, self.doc_type_abbrv_to_doc_type_subdir_map[self.doc_type])
                destination_file = os.path.join(target_dir, f'{self.today}.pdf')
                print(f'Moving {destination_file} to {target_dir}')
                shutil.move(source_file, destination_file)
                break

    # TODO: turn into a regular helper function to be used within `assign_file_path_mappings` such that `self.company_id = self.assign_file_path_mappings()
    # def get_company_id(self):
    #     company_subdir_to_id_map = {v: k for k, v in company_id_to_company_subdir_map.items()}
    #     print(f'-------------- company_subdir_to_id_map----------------\n {company_subdir_to_id_map}\n----------------')
    #     self.company_name = self.company_name.lower()
    #     for company_dir, company_id in company_subdir_to_id_map.items():
    #         if self.company_name in company_dir.lower():
    #             print(f'For company: {self.company_name}, we got company id:  {company_id}')
    #             self.company_id = company_id
    #         else:
    #             return None
    #
    # def get_company_id_fixed(self, company_name):
    #     company_subdir_to_map = {v: k for k, v in company_id_to_company_subdir_map.items()}
    #

    # TODO:
    # def create_and_save_pdf(self, pages):
    #     # print(f'\n##########self.pages##########:\n {self.pages}\n##########self.pages##########:\n')
    #     # print(f'\n##########self.pages##########:\n {type(self.pages)}\n##########self.pages##########:\n')
    #     try:
    #         new_pdf = pikepdf.Pdf.new()
    #         new_pdf.pages.extend(pages)
    #         print(f'$$$$$$$$$$$$$$$$$$ {self.doc_type} | {self.company_id}')
    #         output_path = self.file_path_mappings[self.doc_type][self.company_id]
    #         output_path = os.path.join(output_path, self.new_file_name)
    #         new_pdf.save(output_path)
    #         return True  # Return True if the file was saved successfully
    #     except Exception as e:
    #         print(f"Error occurred while creating and saving PDF: {str(e)}")
    #         return False  # Return False if an error occurred

    def get_new_file_name(self):
        if re.match(r'EFT-\s*\d+', self.doc_type) and re.match(r'-?[\d,]+\.\d+-?', self.total_target_amt):
            if "-" in self.total_target_amt:
                total_target_amt = self.total_target_amt.replace("-", "")
                new_file_name = f'{self.doc_type}-{self.today}-({total_target_amt}).pdf'
            else:
                new_file_name = f'{self.doc_type}-{self.today}-{self.total_target_amt}.pdf'
        elif (re.match(r'CBK-\s*\d+', self.doc_type) or re.match(r'RTV-\s*\d+', self.doc_type)):
            new_file_name = f'{self.doc_type}-{self.today}-CHARGEBACK REQUEST.pdf'
        else:
            new_file_name = f'{self.doc_type}-{self.today}-{self.total_target_amt}.pdf'
        return new_file_name

    def process_multi_page(self):
        page_objs = []
        page_text_strings = []
        while 'END MSG' not in self.cur_page_text and self.page_num < len(self.pdf_data.pages):
            page_objs.append(self.pdf_data.pages[self.page_num])
            self.cur_page_text = self.extractor.extract_text_from_pdf_page(self.pdf_data.pages[self.page_num])
            page_text_strings.append(self.cur_page_text)
            self.doc_type_pattern = self.get_doc_type(self.cur_page_text)
            self.page_num += 1
            if self.page_num >= len(self.pdf_data.pages):
                break
        self.cur_page_text = "".join(page_text_strings)
        self.doc_type, self.total_target_amt = self.extractor.extract_doc_type_and_total_target_amt(self.doc_type_pattern, self.cur_page_text)
        # print(f'self.doc_type: {self.doc_type}\nself.tot_tar_amt: {self.total_target_amt}')

        self.new_file_name = self.get_new_file_name()
        output_path = self.assign_file_path_mappings()
        print(f'----------------------------------------output_path: {output_path}\n ------------------------ new_file_name: {self.new_file_name}')


        # save the split up multipage pdfs into their own pdfs
        # multi_page_pdf_created_and_saved = self.create_and_save_pdf(pages)
        # if not multi_page_pdf_created_and_saved:
        #     print(f'Could not save multi page pdf {multi_page_pdf_created_and_saved}')

    # def process_single_page(self):2
    #     self.pages = [self.pdf_data.pages[self.page_num]]
    #     self.doc_type_num, self.total_target_amt = self.extract_doc_type_and_total_target_amt()
        # single_page_pdf_created_and_saved = self.create_and_save_pdf(self.pages)


        #
        # if not single_page_pdf_created_and_saved:
        #     print(f'Could not save single page pdf {single_page_pdf_created_and_saved}')
        #
        # self.page_num += 1
        # if self.page_num >= len(self.pdf_data.pages):
        #     return

        # print('processing single page function called!')

    # def process_pdfs(self, post_processing=False):
    #
    #     output_path = self.file_path_mappings[self.doc_type][self.company_id]
    #     print(f'output_path: {output_path}')
    #
    #     try:
    #
    #         # Conditional post processing only for EXXON CCMs and LRDs
    #         if post_processing is True:
    #             # print(f'Post processing for EXXON CCMs & LRDs')
    #             merge_rename_and_summate(output_path, doc_type_abbrv_to_doc_type_subdir_map,
    #                                      company_id_to_company_subdir_map)
    #
    #
    #
    #         else:
    #             # Dynamic filesystem mgmt for files that do not need post processing
    #             end_of_month_operations(output_path, self.new_file_name)
    #             return True
    #
    #     except Exception as e:
    #         print(f'An error occurred: {str(e)}')
    #         return False