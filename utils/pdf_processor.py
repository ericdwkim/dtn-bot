import os
import re
import io
import pdfplumber
from glob import glob
from time import sleep
from pikepdf import open, Pdf
import pikepdf
from shutil import move
import datetime
from pathlib import Path
from utils.post_processing import merge_rename_and_summate
from utils.extraction_handler import extract_text_from_pdf_page, extract_info_from_text, extract_doc_type_and_total_target_amt
from utils.filesystem_manager import end_of_month_operations, calculate_directory_path, is_last_day_of_month, cleanup_files
from utils.mappings_refactored import doc_type_abbrv_to_doc_type_subdir_map, doc_type_patterns, company_id_to_company_subdir_map


class PdfProcessor:
    # ----------------------------------  Class Attributes ----------------------------------
    today = datetime.date.today().strftime('%m-%d-%y')
    root_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports'
    download_dir = str(Path.home() / "Downloads")
    # ----------------------------------  Class Attributes ----------------------------------

    # ---------------------------------- Instance attributes ----------------------------------
    def __init__(self):
        self.pdf_file_path = self.get_pdf_file_path()
        self.page_num = 0 
        self.page_text = ''
        self.doc_type_num = ''
        self.pattern = None
        self.pdf_data = self.get_pdf(self.pdf_file_path)
        self.page_text = self.get_page_text()
        self.company_name = None
        self.pages = []
        self.page_texts= []
        self.company_id = self.get_company_id()
        self.doc_type, self.total_target_amt = self.extract_doc_type_and_total_target_amt()


        # Construct the file_path_mappings using doc_type and company_id
        self.file_path_mappings = {
            self.doc_type: {
                self.company_id: os.path.join
                    (
                    self.root_dir,
                    doc_type_abbrv_to_doc_type_subdir_map[self.doc_type],
                    company_id_to_company_subdir_map[self.company_id]
                )
            }
        }

    # ---------------------------------- Instance attributes ----------------------------------

    @classmethod
    def get_pdf_file_path(cls):
        files = Path(cls.download_dir).glob('*messages*.pdf')
        target_file = max(files, key=lambda x: x.stat().st_mtime)
        return str(target_file)

    def get_pdf(self, filepath):
        if os.path.exists(filepath):
            return pikepdf.open(filepath)

    def get_company_names(self):
        company_names = []
        for company_dir in company_id_to_company_subdir_map.values():
            # Slice the string to remove the company id and brackets
            company_name = company_dir.split('[')[0].strip()
            company_names.append(company_name)
        return company_names
    def get_company_name(self):
        company_names = self.get_company_names()
        # print(f'++++++++++++++++++++ {company_names}')
        for company_name in company_names:
            # print(f'++++++++++++++++++++ {company_name}')
            if company_name in self.page_text:
                self.company_name = company_name
                print(f'self.company_name: {self.company_name}|\nself.page_text: {self.page_text}')
                # return company_name
        # Return None if no company name is found in the page_text
        return None

    def get_company_id(self):
        for company_id, company_dir in company_id_to_company_subdir_map.items():
            if company_name == company_dir.split('[')[0].strip():
                return company_id
        return None
    def get_pattern(self):
        for pattern in doc_type_patterns:
            if re.search(pattern, self.page_text, re.IGNORECASE):
                self.pattern = pattern
        return None

    def get_page_text(self):

        self.company_name = self.get_company_name()

        while self.page_num < len(self.pdf_data.pages):
            print(f'Processing page number: {self.page_num + 1}')
            self.page_text = extract_text_from_pdf_page(self.pdf_data.pages[self.page_num])
            print(f'\n********************************\n{self.page_text}\n********************************\n')
            print(f'&&&&&&&&&&&&&&&&&& {self.company_name}')
            if self.company_name and 'END MSG' not in self.page_text:
                self.process_multi_page(self.pdf_data, self.page_text)

            elif self.company_name and 'END MSG' in self.page_text:
                self.process_single_page(self.pdf_data, self.page_text)

            else:
                print(f'Could not find company name: {self.company_name} in text')
                # move page cursor
                self.page_num += 1
                # exit loop if at last page
                if self.page_num >= len(self.pdf_data.pages):
                    break

    def extract_doc_type_and_total_target_amt(self):
        self.pattern = self.get_pattern()
        print(f'---------------- {self.page_text}')
        # Extract regex pattern (EFT, CCM, CMB, RTV, CBK)
        self.doc_type = None # todo: necessary?
        self.doc_type = self.pattern.split('-')[0]  # Extracting the document type prefix from the pattern.
        print(f'--------------- pattern: {self.pattern} | doc_type: {self.doc_type}')

        if self.doc_type is None:
            print(f'Could not find document type using pattern {self.pattern} in current text: {self.page_text}')
            return None, None

        total_amount_matches = re.findall(r'-?[\d,]+\.\d+-?', self.page_text)
        # print(f'\nGetting total_amount_matches: {total_amount_matches}\n')
        if total_amount_matches:
            # print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: {total_amount_matches}')
            self.total_target_amt = total_amount_matches[-1]
            # print(f'=================================================: {total_amount}')
        else:
            self.total_target_amt = None

        return self.doc_type, self.total_target_amt

    def rename_and_delete_pdf(self):
        file_deleted = False
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

    def create_and_save_pdf(self, pages, new_file_name):
        try:
            new_pdf = pikepdf.Pdf.new()
            new_pdf.pages.extend(pages)
            output_path = self.file_path_mappings[self.doc_type][self.company_id]
            output_path = os.path.join(output_path, new_file_name)
            new_pdf.save(output_path)
            return True  # Return True if the file was saved successfully
        except Exception as e:
            print(f"Error occurred while creating and saving PDF: {str(e)}")
            return False  # Return False if an error occurred

    def get_new_file_name(self):
        if re.match(r'EFT-\s*\d+', self.doc_type_num) and re.match(r'-?[\d,]+\.\d+-?', self.total_target_amt):
            if "-" in self.total_target_amt:
                total_target_amt = self.total_target_amt.replace("-", "")
                self.new_file_name = f'{self.doc_type_num}-{self.today}-({total_target_amt}).pdf'
            else:
                self.new_file_name = f'{self.doc_type_num}-{self.today}-{self.total_target_amt}.pdf'
        elif (re.match(r'CBK-\s*\d+', self.doc_type_num) or re.match(r'RTV-\s*\d+', self.doc_type_num)):
            self.new_file_name = f'{self.doc_type_num}-{self.today}-CHARGEBACK REQUEST.pdf'
        else:
            self.new_file_name = f'{self.doc_type_num}-{self.today}-{self.total_target_amt}.pdf'
        return self.new_file_name

    def process_multi_page(self):

        # split large pdf into their smaller, multi page pdfs while keeping track of page nums and texts
        while 'END MSG' not in self.page_text and self.page_num < len(self.pdf_data.pages):
            self.pages.append(self.pdf_data.pages[self.page_num])
            self.page_texts = extract_text_from_pdf_page(self.pdf_data.pages[self.page_num])
            self.page_texts.append(self.page_text)

            self.page_num += 1

            # if at the end of the original pdf, exit loop
            if self.page_num >= len(self.pdf_data.pages):
                break

        # form list of related strings into large string
        self.page_text = "".join(self.page_texts)
        self.doc_type_num, self.today, self.total_target_amt = extract_info_from_text(self.page_text)
        new_file_name = self.get_new_file_name()
        print(
            f'\n*********************************************\n multi new_file_name\n*********************************************\n {new_file_name}')
        # save the split up multipage pdfs into their own pdfs
        multi_page_pdf_created_and_saved = self.create_and_save_pdf(pages, new_file_name)
        if not multi_page_pdf_created_and_saved:
            print(f'Could not save multi page pdf {multi_page_pdf_created_and_saved}')

    def process_single_page(self):
        self.pages = [self.pdf_data.pages[self.page_num]]
        self.doc_type_num, self.today, self.total_target_amt = extract_info_from_text(self.page_text)
        new_file_name = self.get_new_file_name()
        # print(f'\n*********************************************\n single new_file_name\n*********************************************\n {new_file_name}')
        single_page_pdf_created_and_saved = self.create_and_save_pdf(self.pages, new_file_name)
        if single_page_pdf_created_and_saved:
            self.page_num += 1
            if self.page_num >= len(self.pdf_data.pages):
                return
        else:
            print(f'Could not save single page pdf {single_page_pdf_created_and_saved}')


    def process_pdfs(self, post_processing=False):

        output_path = self.file_path_mappings[self.doc_type][self.company_id]
        print(f'output_path: {output_path}')

        try:

            # Conditional post processing only for EXXON CCMs and LRDs
            if post_processing is True:
                # print(f'Post processing for EXXON CCMs & LRDs')
                merge_rename_and_summate(output_path, doc_type_abbrv_to_doc_type_subdir_map,
                                         company_id_to_company_subdir_map)
                
            

            else:
                # Dynamic filesystem mgmt for files that do not need post processing
                end_of_month_operations(output_path, self.new_file_name)
                return True

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False
