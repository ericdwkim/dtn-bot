import argparse
import logging
import os
import re
import time
import pikepdf
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from src.utils.log_config import setup_logger
from src.app.flow_manager import FlowManager
from src.utils.pdf_processor import PdfProcessor
from src.utils.post_processing import PDFPostProcessor
from src.utils.file_handler import FileHandler
from src.utils.extraction_handler import ExtractionHandler
from src.utils.mappings import *


class Main:

    root_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports'
    today = datetime.today()
    _initialized = False
    download_dir = str(Path.home() / "Downloads")

    def __init__(self, headless=False):
        self.flow_manager = FlowManager(headless=headless)
        self.file_handler = FileHandler()
        self.extraction_handler = ExtractionHandler()
        self.company_dir = ''
        # self.company_dir = '/Users/ekim/workspace/txb/mock/k-drive/Dtn reports/Credit Cards/EXXONMOBIL [10005]'
        self.pdf_file_path = os.path.join(self.download_dir, 'messages.pdf')
        self.page_num = 0
        self.pdf_data = self.update_pdf_data() # PikePDF instance var
        logging.info(f'The PikePDF instance variable `pdf_data`: {self.pdf_data}')
        self.doc_type, self.total_target_amt = ('', '')
        if not PdfProcessor._initialized:
            self.set_today_str_and_datetime()
            PdfProcessor._initialized = True



    @classmethod
    def set_today_str_and_datetime(cls):
        cls.today_str = cls.today.strftime('%m-%d-%y')
        cls.today_datetime  = datetime.strptime(cls.today_str, '%m-%d-%y')

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

        # @dev: handles key as tuple
        doc_type_full = self.file_handler.get_doc_type_full(self.doc_type)

        self.file_path_mappings = {
            self.doc_type: {
                self.company_id: os.path.join
                    (
                    self.root_dir,
                    doc_type_full,
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
        # logging.info(f'\ncompany_names\n {company_names}\n')
        # logging.info(f'\ncur_page_text\n {cur_page_text}\n')
        for company_name in company_names:
            if company_name in cur_page_text.upper():
                logging.info(f'Checking company_name: {company_name}\nFound matching company name in current page!')
                return company_name

        # logging.warning(f'Could not find matching Company Name in current page text.')
        return None

    @staticmethod
    def get_doc_type(cur_page_text):
        """
        Helper func for getting doc_type_pattern instance
        :param cur_page_text:
        :return:
        """
        for doc_type_pattern in doc_type_patterns:
                doc_type_and_num_matches = re.findall(doc_type_pattern, cur_page_text, re.IGNORECASE)
                if not doc_type_and_num_matches:
                    logging.warning(f'Could not find doc_type_and_num on current page text')
                    return None
                else:
                    doc_type_and_num = doc_type_and_num_matches[0]
                    # assumes first match is correct doc type
                    logging.info(f'Current page text has doc_type_and_num: {doc_type_and_num} using pattern: {doc_type_pattern}')
                    return doc_type_and_num, doc_type_pattern

    def initialize_pdf_data(self):
        logging.info(f'Prior to updating pdf data instance: {self.pdf_data}')
        self.pdf_data = self.update_pdf_data()
        logging.info(f'After updating pdf_data instance using setter: {self.pdf_data}')

    def log_warning_and_skip_page(self, msg):
        logging.warning(msg)

    def is_company_name_set(self):
        company_name = self.get_company_name(self.cur_page_text)
        if company_name is not None:
            self.company_name = company_name
            logging.info(f'Updated company_name to: {company_name}')
            return True
        elif self.company_name is not None:  # company_name is already set, no need to update
            return True
        return False  # company_name wasn't set and we couldn't update it

    def is_doc_type_pattern_set(self):
        doc_type_and_num, doc_type_pattern = self.get_doc_type(self.cur_page_text)
        if (doc_type_and_num is not None) and (doc_type_pattern is not None):
            self.doc_type_pattern = doc_type_pattern
            self.doc_type_and_num = doc_type_and_num
            logging.info(f'Updated doc_type_pattern to: {doc_type_pattern}')
            return True
        elif (self.doc_type_pattern is not None) and (self.doc_type_and_num is not None):  # if doc_type_pattern and doc_type_and_num instances are alraedy set, no need to update
            return True
        return False  # todo: add exception /error hadling

    def is_doc_type_pattern_and_company_name_present(self):
        if self.company_name and self.doc_type_pattern in self.cur_page_text:
            return True
        else:
            self.log_warning_and_skip_page(f'Company name "{self.company_name}" and Document Type pattern: "{self.doc_type_pattern}" not found in current page text')
            return None

    def rename_and_delete_pdf(self):
        file_deleted = False
        if os.path.exists(self.pdf_file_path):
            with pikepdf.open(self.pdf_file_path) as pdf:
                if len(pdf.pages) > 0:
                    first_page = self.extraction_handler.extract_text_from_pdf_page(pdf.pages[0])

                    if re.search(r'EFT-\d+', first_page) or re.search(r'CCM-\d+ | CMB-\d+', first_page):
                        if re.search(r'EFT-\d+', first_page):
                            self.new_file_name = f'EFT-{self.today_str}-TO-BE-DELETED.pdf'
                        else:
                            self.new_file_name = f'CCM-{self.today_str}-TO-BE-DELETED.pdf'

                        file_directory = os.path.dirname(self.pdf_file_path)
                        new_file_path = os.path.join(file_directory, self.new_file_name)

                        logging.info(f"Renaming file: {self.pdf_file_path} to {new_file_path}")
                        os.rename(self.pdf_file_path, new_file_path)
                        file_deleted = True
                        logging.info("File renamed successfully.")
                        time.sleep(3)

                        if os.path.exists(new_file_path):
                            logging.info(f"Deleting file: {new_file_path}")
                            os.remove(new_file_path)
                            logging.info("File deleted successfully.")

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
        logging.crticial(f'Could not retrieve Company ID from Company Name: {company_name}.')
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
                logging.info(f'Setting output filepath to: {output_file_path}')

            else:
                # send to month_dir for all other doc types
                output_file_path = self.construct_final_output_filepath()
                logging.info(f'Setting output filepath to: {output_file_path}')
            new_pdf.save(output_file_path)
            return True

        except Exception as e:
            logging.exception(f'An error occurred while creating and saving PDF: "{str(e)}"')
            return False

    def get_new_file_name(self):
        if re.match(r'EFT-\s*\d+', self.doc_type_and_num) and re.match(r'-?[\d,]+\.\d+-?', self.total_target_amt):
            logging.critical(f'******************************************* self.total_target_amt: {self.total_target_amt} ***********************')
            if "-" in self.total_target_amt:
                total_target_amt = self.total_target_amt.replace("-", "")
                new_file_name = f'{self.doc_type_and_num}-{self.today_str}-({total_target_amt}).pdf'
            else:
                new_file_name = f'{self.doc_type_and_num}-{self.today_str}-{self.total_target_amt}.pdf'
        elif (re.match(r'CBK-\s*\d+', self.doc_type_and_num) or re.match(r'RTV-\s*\d+', self.doc_type_and_num)):
            new_file_name = f'{self.doc_type_and_num}-{self.today_str}-CHARGEBACK REQUEST.pdf'
        else:
            new_file_name = f'{self.doc_type_and_num}-{self.today_str}-{self.total_target_amt}.pdf'
        return new_file_name


    def process_multi_page(self):
        page_objs = []
        page_text_strings = []

        # @deV: inner loop for the multi-page spanning mini PDF
        while 'END MSG' not in self.cur_page_text and self.page_num < len(self.pdf_data.pages) - 1:
            logging.info(f'processing multipage page num: {self.page_num + 1}')

            cur_page = self.pdf_data.pages[self.page_num]
            page_objs.append(cur_page)
            self.cur_page_text = self.extraction_handler.extract_text_from_pdf_page(cur_page)
            page_text_strings.append(self.cur_page_text)


            self.page_num += 1

            if self.page_num >= len(self.pdf_data.pages) -1:
                break
        self.cur_page_text = "".join(page_text_strings)
        # print(f'------------cur_page_text--------------------\n')
        # print(self.cur_page_text)
        # print(f'\n--------------------------------')
        logging.info(f'Extracting Document Type and Total Target Amount....')
        self.doc_type, self.doc_type_num, self.total_target_amt = self.extraction_handler.extract_doc_type_and_total_target_amt(self.doc_type_and_num, self.cur_page_text)
        logging.info(f'Document Type: {self.doc_type} | Document Type Number: {self.doc_type_num} | Total Target Amount: {self.total_target_amt}')

        # Construct new file name instance
        self.new_file_name = self.get_new_file_name()

        # Move (save) new file to final output path
        multi_page_pdf_created_and_saved = self.create_and_save_pdf(page_objs)
        return multi_page_pdf_created_and_saved


    def process_single_page(self):

        # end marker and current instance company name in text
        if 'END MSG' in self.cur_page_text and self.page_num < len(self.pdf_data.pages) - 1:
            cur_page = self.pdf_data.pages[self.page_num] # single pikepdf page obj --> req'd obj to create and save the page

            # @dev: `self.cur_page_text` instance is already the extracted cur_page_text which already has been extracted from process_pages since it is a single page
            # fetch target data from already extracted page text
            self.doc_type, self.doc_type_num, self.total_target_amt = self.extraction_handler.extract_doc_type_and_total_target_amt(self.doc_type_and_num, self.cur_page_text)
            logging.info(
                f'Document Type: {self.doc_type} | Document Type Number: {self.doc_type_num} | Total Target Amount: {self.total_target_amt}')

            if self.page_num >= len(self.pdf_data.pages) - 1:
                return # exit func b/c finished with pdf

            # move page cursor after check; ensures that when last_page_num == len(last_page), it exits and prevents misleading final "error" message that last_page_num + 1 could not be processed
            self.page_num +=1
            # fetch file name
            self.new_file_name = self.get_new_file_name()

            # Create single page pdf and save in correct dir
            single_page_pdf_created_and_saved = self.create_and_save_pdf(cur_page)
            logging.info(f'single_page_pdf_created_and_saved: {single_page_pdf_created_and_saved}')
            return single_page_pdf_created_and_saved

    def process_pages(self):
        """
        main processing func
        """

        logging.info(f'pdf_file_path: {self.pdf_file_path}')
        try:
            # @dev: outer while loop for the main downloaded PDF
            while self.page_num < len(self.pdf_data.pages) - 1:

                logging.info(f'Processing page number: {self.page_num + 1}')
                # ---------------------------------------------------
                page = self.pdf_data.pages[self.page_num]

                self.cur_page_text = self.extraction_handler.extract_text_from_pdf_page(page)
                logging.info(f'self.cur_page_text: \n{self.cur_page_text}\n')

                if self.is_company_name_set() and self.is_doc_type_pattern_set():
                    if self.is_doc_type_pattern_and_company_name_present():
                        continue
                else:  # if company_name or doc_type_pattern instances were not set in the current iteration nor in the previous iteration, then exit function
                    return

                logging.info(f'PAGE NUM BEFORE MULTI OR SINGLE PROCESSING ----------------------- {self.page_num + 1} ---------------------------')

                if re.search(self.doc_type_pattern, self.cur_page_text, re.IGNORECASE) and ('END MSG' not in self.cur_page_text):
                    if not self.process_multi_page():
                        raise ValueError(f"Failed processing multi-page PDF at page {self.page_num + 1}.")
                    continue

                elif re.search(self.doc_type_pattern, self.cur_page_text, re.IGNORECASE) and ('END MSG' in self.cur_page_text):
                    if not self.process_single_page():
                        raise ValueError(f"Failed processing single-page PDF at page {self.page_num + 1}.")
                    continue

                # logging.info(f'--------------------- self.page_num: {self.page_num} | len(self.pdf_data.pages): {len(self.pdf_data.pages)} -----------------------')
                # @dev: main outer loop exit  logic
                if self.page_num >= len(self.pdf_data.pages) - 1:
                    break
                # ---------------------------------------------------

            logging.info("\n******************************\nCompleted processing all pages!\n******************************\n")
            return True

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    # def first_flow(self):
    #     try:
    #
    #         group_filter_set_to_invoice =  self.flow_manager.data_connect_driver.set_group_filter_to_invoice()
    #
    #         if not group_filter_set_to_invoice:
    #             logging.error('Could not set group filter to invoice')
    #
    #         invoices_renamed_and_filed_away = self.processor.rename_and_move_or_overwrite_invoices_pdf()
    #
    #         if not invoices_renamed_and_filed_away:
    #             logging.error('Could not rename and file away invoices. Does the Invoices PDF exist?')
    #
    #         elif invoices_renamed_and_filed_away and self.file_handler.is_last_day_of_month():
    #             self.processor.month_and_year_handler(first_flow=True)
    #
    #     except Exception as e:
    #         logging.info(f'An unexpected error has occurred during first_flow: {e}')
    #
    #
    # def second_flow(self):
    #
    #     try:
    #         group_filter_set_to_draft_notice = self.flow_manager.data_connect_driver.set_group_filter_to_draft_notice()
    #         logging.info(f'group_filter_set_to_draft_notice: {group_filter_set_to_draft_notice}')
    #
    #         if not group_filter_set_to_draft_notice:
    #             logging.error('Could not set group filter to Draft Notice during second_flow')
    #
    #
    #         draft_notices_processed_and_filed = self.processor.process_pages()
    #
    #         if not draft_notices_processed_and_filed:
    #             logging.error('Could not rename and file away Draft Notices. Do the notices PDF exist?')
    #
    #         elif draft_notices_processed_and_filed and self.file_handler.is_last_day_of_month():
    #             processor.month_and_year_handler(first_flow=False)
    #
    #     except Exception as e:
    #         logging.info(f'An unexpected error has occurred during second_flow: {e}')
    #
    #
    def third_flow(self):
        try:
            group_filter_set_to_credit_card = self.flow_manager.data_connect_driver.set_group_filter_to_credit_card()
            logging.info(f'group filter set to CC: {group_filter_set_to_credit_card}')

            if not group_filter_set_to_credit_card:
                logging.error('Could not set group filter to CC during third flow')

            credit_card_pdf_downloaded = self.flow_manager.data_connect_driver.data_connect_page.check_all_then_click_print()
            if not credit_card_pdf_downloaded:
                logging.critical(f'Credit cards PDF was not downloaded. Exiting...')
                return

            ccms_processed_and_filed = self.process_pages()

            if not ccms_processed_and_filed:
                logging.error('Could not rename and file away CCMs')
            elif ccms_processed_and_filed and self.file_handler.is_last_day_of_month():
                self.processor.month_and_year_handler(first_flow=False)

        except Exception as e:
            logging.exception(f'An unexpected error has occurred during third_flow: {e}')

    def run_flows(self, flows):
        setup_logger()
        num_flows = len(flows)

        for i, (flow_func, flow_name) in enumerate(flows):
            logging.info(f'\n---------------------------\nInitiating Flow: {flow_name}\n---------------------------\n')

            # Only start the flow at the beginning of the list of flows.
            if i == 0:
                if flow_name == 'third_flow':
                    self.flow_manager.start_flow(third_flow=True)
                elif flow_name == 'first_flow':
                    self.flow_manager.start_flow(third_flow=False)
                    self.flow_manager.data_connect_driver.data_connect_page.check_all_then_click_print()
                else:
                    self.flow_manager.start_flow(third_flow=False)

            flow_func()  # Execute flows

            # if flow_name in ['second_flow', 'third_flow']:
            #     original_pdf_deleted = self.rename_and_delete_pdf()
            #     logging.info(f'original_pdf_deleted: {original_pdf_deleted}')

            logging.info(f'\n---------------------------\nCommencing Flow: {flow_name}\n---------------------------\n')

            # Only end the flow if it's the last one in the list of flows.
            if i == num_flows - 1:
                # self.flow_manager.end_flow()
                logging.info('tearing down placeholder')
                time.sleep(300000)


    def test_post_processing(self):
        setup_logger()
        pp = PDFPostProcessor()
        print(f'self.company_dir: {self.company_dir}')

        pp.merge_rename_and_summate(self.company_dir)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DTN Bot V2')
    parser.add_argument('--skipFlow1', required=False, action='store_true', help='Skip the first flow')
    parser.add_argument('--skipFlow2', required=False, action='store_true', help='Skip the second flow')
    parser.add_argument('--skipFlow3', required=False, action='store_true', help='Skip the third flow')
    args = parser.parse_args()

    main = Main()
    flows_to_run = []
    if not args.skipFlow1:
        flows_to_run.append((main.first_flow, 'first_flow'))
    if not args.skipFlow2:
        flows_to_run.append((main.second_flow, 'second_flow'))
    if not args.skipFlow3:
        flows_to_run.append((main.third_flow, 'third_flow'))



    main.run_flows(flows_to_run)
    logging.info(f'\n---------------------------\nCommencing All Flows\n---------------------------\n')


    # main.test_post_processing()