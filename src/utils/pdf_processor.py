import os
import re
import time
import pikepdf
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
from src.utils.extraction_handler import ExtractionHandler
from src.utils.file_handler import FileHandler
from src.utils.mappings import doc_type_short_to_doc_type_full_map, doc_type_patterns, company_id_to_company_subdir_map

class PdfProcessor:
    # ----------------------------------  Class Attributes ----------------------------------
    # TODO: figure out which `today` in `datetime` should be used; also needs formatting.
    # @deV: seems like most cases require it to be datetime object, so just instantiate attr as datetime and convert to str locally where neeeded

    root_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports'
    # root_dir_prod = r'K:/DTN Reports'
    download_dir = str(Path.home() / "Downloads")
    # ----------------------------------  Class Attributes ----------------------------------

    # ---------------------------------- Instance attributes ----------------------------------
    def __init__(self):

        # Get today's date as a datetime object
        today = datetime.today()
        # If you need the date in string format with specific format
        self.today_str = today.strftime('%m-%d-%y')
        self.today = datetime.strptime(datetime.today().strftime('%m-%d-%y'), '%m-%d-%y')
        self.company_dir = ''
        self.pdf_file_path = os.path.join(self.download_dir, 'messages.pdf')
        self.page_num = 0
        self.pdf_data = self.update_pdf_data() # PikePDF instance var
        logging.info(f'The PikePDF instance variable `pdf_data`: {self.pdf_data}')
        self.extraction_handler = ExtractionHandler()
        self.doc_type, self.total_target_amt = ('', '')

        self.file_handler = FileHandler()

        # self.cur_page_text = cur_page_text # todo

    # ---------------------------------- Instance attributes ----------------------------------

    def get_pdf(self, filepath):
        if not os.path.exists(filepath):
            logging.info(f'File path does not exist: "{filepath}"')
            return None
        else:
            logging.info(f'Filepath: "{filepath}" exists. Returning opened PikePdf object')
            return pikepdf.open(filepath)

    # @dev: workaround to update `pdf_data` instance being initialized as None during start of run_flows
    def update_pdf_data(self):
        self.pdf_data = self.get_pdf(self.pdf_file_path)
        return self.pdf_data

    def assign_file_path_mappings(self):

        # fetch company_id from company_name using helper instance method
        self.company_id = self.get_company_id_fixed(self.company_name)

        logging.info(f'self.doc_type: {self.doc_type}   | self.total_target_amt: {self.total_target_amt} | self.company_name: {self.company_name}  | self.company_id: {self.company_id}' )

        self.file_path_mappings = {
            self.doc_type: {
                self.company_id: os.path.join
                    (
                    self.root_dir,
                    doc_type_short_to_doc_type_full_map[self.doc_type],
                    company_id_to_company_subdir_map[self.company_id]
                )
            }
        }

        # print(f'{self.doc_type}   | {self.total_target_amt} | {self.company_name} ' )
        if self.doc_type is None:
            logging.error("Error: Document type is None. File path mappings could not be assigned.")
            return None

        elif self.company_id is None:
            logging.error("Error: Company ID is None. File path mappings could not be assigned.")
            return None
        else:
            # Return output path from nested value in nested mapping
            # return self.file_path_mappings[self.doc_type][self.company_id]
            self.company_dir =  self.file_path_mappings[self.doc_type][self.company_id]
            return self.company_dir


    def construct_final_output_filepath(self, post_processing=False):
        """
        assign_file_path_mappings & construct_month_dir_from_doc_type wrapper to construct dynamic final output paths for both company_dir and month_dir;
        allows flexibility for both up to company_dir or up to month_dir
     ideally have assign_file_path_mappings construct up to month_dir and # TODO: perform post processing in memory and not on disk; requires breaking into smaller classes

        """
        # Construct company dir
        self.company_dir = self.assign_file_path_mappings()
        logging.info(f'Company directory: {self.company_dir}')

        current_year, current_month = self.file_handler.cur_month_and_year_from_today()

        month_dir = self.file_handler.create_and_return_directory_path(self.company_dir, current_year, current_month)
        # print(f'******************** month_dir {month_dir} *******************')


        if not self.company_dir or not month_dir:
            logging.error('Company directory or month directory could not be constructed')
            return

        elif post_processing is True:
            output_file_path = os.path.join(self.company_dir, self.new_file_name)
            return output_file_path

        else:
            output_file_path = os.path.join(self.company_dir, month_dir, self.new_file_name)
            return output_file_path


    @staticmethod
    def get_company_names():
        company_names = []
        for company_dir in company_id_to_company_subdir_map.values():
            # Slice the string to remove the company id and brackets
            company_name = company_dir.split('[')[0].strip()
            company_names.append(company_name)
        # print(f'******** {company_names} *******')
        return company_names

    @staticmethod
    def get_company_name(cur_page_text):
        """
        Helper func for getting company_name instance
        :param cur_page_text:
        :return:
        """
        company_names = PdfProcessor.get_company_names()
        logging.info(f'\ncompany_names\n {company_names}\n')
        logging.info(f'\ncur_page_text\n {cur_page_text}\n')
        for company_name in company_names:
            if company_name in cur_page_text.upper():
                logging.info(f'Checking company_name: {company_name}\nFound matching company name in current page!')
                return company_name

        logging.error(f'Could not find matching Company Name in current page text.')
        return None

    @staticmethod
    def get_doc_type(cur_page_text):
        """
        Helper func for getting doc_type_pattern instance
        :param cur_page_text:
        :return:
        """
        for doc_type_pattern in doc_type_patterns:
            if re.search(doc_type_pattern, cur_page_text, re.IGNORECASE):
                logging.info(f'Found matching document type using regex patter: "{doc_type_pattern}" in current page text.')
                return doc_type_pattern

        logging.error(f'Could not find matching document type using regex pattern in current page text.')
        return None

    def process_pages(self):
        """
        main processing func
        """
        logging.info(f'Prior to updating pdf data instance: {self.pdf_data}')
        self.pdf_data = self.update_pdf_data()
        logging.info(f'After updating pdf_data instance using setter: {self.pdf_data}')
        # logging.info(f'pdf_file_path: {self.pdf_file_path}')
        try:
            while self.page_num < len(self.pdf_data.pages):

                logging.info(f'Processing page number: {self.page_num + 1}')
                page = self.pdf_data.pages[self.page_num]

                self.cur_page_text = self.extraction_handler.extract_text_from_pdf_page(page)
                logging.info(f'self.cur_page_text: \n{self.cur_page_text}\n')

                self.company_name = self.get_company_name(self.cur_page_text)
                logging.info(f'self.company_name: \n{self.company_name}\n')

                # todo: self.doc_type_pattern; @dev: catch22 b/c it gets initialized as '' in constructor; must be a way to turn this into an instance att...
                doc_type_pattern = self.get_doc_type(self.cur_page_text)
                logging.info(f'doc_type_pattern: \n{doc_type_pattern}\n')


                if self.company_name not in self.cur_page_text: # todo: either this or simply use the one in get_company_name()
                    logging.critical(f'Company name "{self.company_name}" not found in current page.')
                    self.page_num += 1
                    continue
                # todo: either this or simply use the one in get_doc_type()
                if re.search(doc_type_pattern, self.cur_page_text, re.IGNORECASE) and (
                        'END MSG' not in self.cur_page_text):
                    if not self.process_multi_page():
                        raise ValueError(f"Failed processing multi-page PDF at page {self.page_num + 1}.")
                elif re.search(doc_type_pattern, self.cur_page_text, re.IGNORECASE) and (
                        'END MSG' in self.cur_page_text):
                    if not self.process_single_page():
                        raise ValueError(f"Failed processing single-page PDF at page {self.page_num + 1}.")
                else:
                    logging.warning(f"Pattern '{doc_type_pattern}' not found in current page.")
                    self.page_num += 1

                if self.page_num >= len(self.pdf_data.pages):
                    break

            logging.info("Completed processing all pages.")
            return True

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    # Invoices PDF rename helper
    def rename_invoices_pdf(self):

        # Pass `/Users/ekim/Downloads/messages.pdf` to get PikePDf object
        pdf = self.get_pdf(self.pdf_file_path)

        if pdf is not None:

            self.new_file_name = self.today.strftime('%m-%d-%y') + '.pdf'
            # given the original `messages.pdf` full filepath, return new full filepath
            file_dir = os.path.dirname(self.pdf_file_path)
            self.new_file_path = os.path.join(file_dir, self.new_file_name)
            logging.info(f'Renaming original Invoices PDF file "{self.pdf_file_path}" to {self.new_file_path}')

            pdf.close() # Close PDF
            os.rename(self.pdf_file_path, self.new_file_path)
            # Check file got saved correctly
            if os.path.exists(self.new_file_path):
                logging.info(f'File renamed successfully.')
                time.sleep(3)
                return True
            else:
                logging.error(f'Could not rename Invoices PDF')
                return False
        else:
            logging.critical(f'Could not find downloaded Invoices PDF in Downloads directory. Something went wrong. Does it even exist?')
            return False

    # Refactored `rename_and_move_pdf` with OOP
    def rename_and_move_or_overwrite_invoices_pdf(self):

        invoices_file_has_been_renamed = self.rename_invoices_pdf()

        if not invoices_file_has_been_renamed:
            return False

        # Get final output dir from file prefix
        month_dir = self.file_handler.construct_month_dir_from_doc_type('INV')

        # Construct final output path
        target_file_path = os.path.join(self.root_dir, month_dir, self.new_file_name)

        # Get timestamps for new Invoices file
        mod_time_new, cre_time_new = self.file_handler.get_file_timestamps(self.new_file_path)

        # If conflicting filename exists in target directory, replace with newest
        if os.path.isfile(target_file_path):
            mod_time_old, cre_time_old = self.file_handler.get_file_timestamps(target_file_path)

            logging.info(
                f'File with name: "{self.new_file_name}" already exists at "{target_file_path}"\nLast modified (old): {mod_time_old} | Last modified (new): {mod_time_new}\nCreated (old): {cre_time_old} | Created (new): {cre_time_new}\nOverwriting duplicate file with latest modified/created...')
            os.remove(target_file_path)

        try:
            shutil.move(self.new_file_path, target_file_path)
            logging.info(f'Moved latest Invoices pdf created on "{cre_time_new}" to "{target_file_path}"')
            return True  # File moved successfully
        except Exception as e:
            logging.exception(f'An error occurred while moving the file: {e}')
            return False  # File could not be moved

    def rename_and_delete_pdf(self):
        file_deleted = False
        if os.path.exists(self.pdf_file_path):
            with pikepdf.open(self.pdf_file_path) as pdf:
                if len(pdf.pages) > 0:
                    first_page = self.extraction_handler.extract_text_from_pdf_page(pdf.pages[0])

                    if re.search(r'EFT-\d+', first_page) or re.search(r'CCM-\d+ | CMD-\d+', first_page):
                        if re.search(r'EFT-\d+', first_page):
                            self.new_file_name = f'EFT-{self.today}-TO-BE-DELETED.pdf'
                        else:
                            self.new_file_name = f'CCM-{self.today}-TO-BE-DELETED.pdf'

                        file_directory = os.path.dirname(self.pdf_file_path)
                        new_file_path = os.path.join(file_directory, self.new_file_name)

                        print(f"Renaming file: {self.pdf_file_path} to {new_file_path}")
                        os.rename(self.pdf_file_path, new_file_path)
                        file_deleted = True
                        print("File renamed successfully.")
                        time.sleep(3)

                        if os.path.exists(new_file_path):
                            print(f"Deleting file: {new_file_path}")
                            os.remove(new_file_path)
                            print("File deleted successfully.")

                return file_deleted

    def get_company_id_fixed(self, company_name):
        company_subdir_to_company_id_map = {v: k for k, v in company_id_to_company_subdir_map.items()}
        # print(f'-------------- company_subdir_to_company_id_map----------------\n {company_subdir_to_company_id_map}\n----------------')
        for company_dir, company_id in company_subdir_to_company_id_map.items():
            logging.info(f'Using {company_name} to fetch matching company_id: {company_id}')

            # print(f'if "{company_name}" == "{cleaned_comp_dir}"')
            if company_name == company_dir.split('[')[0].strip():
                logging.info(f'Match found!\nCompany Name: {company_name} has Company ID: {company_id}')
                # Turn local var to instance var for dynamic file path construction
                self.company_id = company_id
                return self.company_id
        print(f'Could not retrieve Company ID from Company Name: {company_name}.')
        return None

    def create_and_save_pdf(self, pages):
        """
        pages - single or list of pike pdf page objects
        """


        try:
            new_pdf = pikepdf.Pdf.new()
            if isinstance(pages, list):
                # Merge multi page spanning pdfs w/ page objs instance
                new_pdf.pages.extend(pages)
            else:
                # Create single page pdf from page obj instance
                new_pdf.pages.append(pages)


            if (self.doc_type == 'CCM' or self.doc_type == 'LRD') and self.company_name == 'EXXONMOBIL':
                # send to company_dir for post processing
                output_file_path = self.construct_final_output_filepath(post_processing=True)
                # print(f'1output_file_path: {output_file_path}')

            else:
                # send to month_dir for all other doc types
                output_file_path = self.construct_final_output_filepath()
                # print(f'2output_file_path: {output_file_path}')
            new_pdf.save(output_file_path)
            return True

        except Exception as e:
            logging.exception(f'An error occurred while creating and saving PDF: {e}')
            return False

    def get_new_file_name(self):
        if re.match(r'EFT-\s*\d+', self.doc_type) and re.match(r'-?[\d,]+\.\d+-?', self.total_target_amt):
            logging.critical(f'******************************************* self.total_target_amt: {self.total_target_amt} ***********************')
            # todo: debug why this formatting conditional doesn't work
            if "-" in self.total_target_amt:
                total_target_amt = self.total_target_amt.replace("-", "")
                new_file_name = f'{self.doc_type}-{today_str}-({total_target_amt}).pdf'
            else:
                new_file_name = f'{self.doc_type}-{today_str}-{self.total_target_amt}.pdf'
        elif (re.match(r'CBK-\s*\d+', self.doc_type) or re.match(r'RTV-\s*\d+', self.doc_type)):
            new_file_name = f'{self.doc_type}-{today_str}-CHARGEBACK REQUEST.pdf'
        else:
            new_file_name = f'{self.doc_type}-{today_str}-{self.total_target_amt}.pdf'
        return new_file_name


    def process_multi_page(self):
        page_objs = []
        page_text_strings = []

        # Enter loop by checking for absence of end marker in first page of multi page spanning text
        while 'END MSG' not in self.cur_page_text and self.page_num < len(self.pdf_data.pages):
            cur_page = self.pdf_data.pages[self.page_num]
            page_objs.append(cur_page)
            self.cur_page_text = self.extraction_handler.extract_text_from_pdf_page(cur_page)
            page_text_strings.append(self.cur_page_text)
            self.doc_type_pattern = self.get_doc_type(self.cur_page_text)
            self.page_num += 1
            if self.page_num >= len(self.pdf_data.pages):
                break
        self.cur_page_text = "".join(page_text_strings)
        # print(f'------------cur_page_text--------------------\n')
        # print(self.cur_page_text)
        # print(f'\n--------------------------------')
        logging.info(f'Extracting Document Type and Total Target Amount....')
        self.doc_type, self.total_target_amt = self.extraction_handler.extract_doc_type_and_total_target_amt(self.doc_type_pattern, self.cur_page_text)
        logging.info(f'Document Type: {self.doc_type} | Total Target Amount: {self.total_target_amt}')

        # Construct new file name instance
        self.new_file_name = self.get_new_file_name()

        # Construct final output filepath using wrapper
        self.final_output_filepath = self.construct_final_output_filepath()

        logging.info(f'final_output_filepath: {self.final_output_filepath}\nnew_file_name: {self.new_file_name}')

        # Move (save) new file to final output path
        multi_page_pdf_created_and_saved = self.create_and_save_pdf(page_objs)
        # print('\n--------------------------------------------------------------------')
        return multi_page_pdf_created_and_saved


    def process_single_page(self):

        # end marker and current instance company name in text
        if 'END MSG' in self.cur_page_text and self.page_num < len(self.pdf_data.pages):
            cur_page = self.pdf_data.pages[self.page_num] # single pikepdf page obj
            # @dev: cur_page_text instance is the same instance to extract text from b/c single page
            self.doc_type_pattern = self.get_doc_type(self.cur_page_text)
            # fetch target data
            self.doc_type, self.total_target_amt = self.extraction_handler.extract_doc_type_and_total_target_amt(self.doc_type_pattern, self.cur_page_text)
            logging.info(f'Document Type: {self.doc_type} | Total Target Amount: {self.total_target_amt}')

            if self.page_num >= len(self.pdf_data.pages):
                return # exit func b/c finished with pdf

            # move page cursor after check; ensures that when last_page_num == len(last_page), it exits and prevents misleading final "error" message that last_page_num + 1 could not be processed
            self.page_num +=1
            # fetch file name
            self.new_file_name = self.get_new_file_name()

            #  fetch output filepath
            self.final_output_filepath = self.construct_final_output_filepath()

            logging.info(f'final_output_filepath: {self.final_output_filepath}\nnew_file_name: {self.new_file_name}')

            # Create single page pdf and save in correct dir
            single_page_pdf_created_and_saved = self.create_and_save_pdf(cur_page)
            logging.info(f'single_page_pdf_created_and_saved: {single_page_pdf_created_and_saved}')
            return single_page_pdf_created_and_saved