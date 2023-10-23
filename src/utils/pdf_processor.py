import os, re, time, pikepdf, shutil, logging
from datetime import datetime, timedelta
from pathlib import Path
from src.utils.extraction_handler import ExtractionHandler
from src.utils.file_handler import FileHandler
from src.utils.mappings import doc_type_short_to_doc_type_full_map, doc_type_patterns, company_id_to_company_subdir_map
from src.utils.post_processing import PostProcessor
from src.utils.log_config import handle_errors

class PdfProcessor:
    # ----------------------------------  Class Attributes ----------------------------------
    today = datetime.today()
    _initialized = False
    root_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports'
    # root_dir_prod = r'K:/DTN Reports'
    download_dir = str(Path.home() / "Downloads")
    # ----------------------------------  Class Attributes ----------------------------------

    # ---------------------------------- Instance attributes ----------------------------------
    def __init__(self):
        self.extraction_handler = ExtractionHandler()
        self.file_handler = FileHandler()
        self.new_pdf = pikepdf.Pdf.new()
        self.post_processing = PostProcessor()
        self.company_dir = ''  # todo necessary?
        self.pdf_file_path = os.path.join(self.download_dir, 'messages.pdf')
        self.page_num = 0
        self.pdf_data = self.update_pdf_data() # PikePDF instance var
        logging.info(f'The PikePDF instance variable `pdf_data`: {self.pdf_data}')
        self.doc_type, self.total_target_amt = ('', '')
        if not PdfProcessor._initialized:
            self.set_today_str_and_datetime()
            PdfProcessor._initialized = True

    # ---------------------------------- Instance attributes ----------------------------------
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

        logging.info(f'self.doc_type_short: {self.doc_type_short}  | self.total_target_amt: {self.total_target_amt} | self.company_name: {self.company_name}  | self.company_id: {self.company_id}' )

        # @dev: handles key as tuple
        doc_type_full = self.extraction_handler.get_doc_type_full(self.doc_type_short)

        self.file_path_mappings = {
            self.doc_type_short: {
                self.company_id: os.path.join
                    (
                    self.root_dir,
                    doc_type_full,
                    company_id_to_company_subdir_map[self.company_id]
                )
            }
        }

        # print(f'{self.doc_type_short}   | {self.total_target_amt} | {self.company_name} ' )
        if self.doc_type_short is None:
            logging.error("Error: Document type is None. File path mappings could not be assigned.")
            return None

        elif self.company_id is None:
            logging.error("Error: Company ID is None. File path mappings could not be assigned.")
            return None
        else:
            # Return output path from nested value in nested mapping
            # return self.file_path_mappings[self.doc_type_short][self.company_id]
            self.company_dir =  self.file_path_mappings[self.doc_type_short][self.company_id]
            return self.company_dir


    def construct_final_output_filepath(self, post_processing=False):
        """
        assign_file_path_mappings & construct_month_dir_from_doc_type_short wrapper to construct dynamic final output paths for both company_dir and month_dir;
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

    # @dev: todo- this acts the same way as extract_total_target_amt , so consider moving to extraction_handler; could even create a wrapper for both extractions (improved logic b/c separation of concerns); wrapper(self.cur_page_text) and return vars as tuple
    @staticmethod
    def get_doc_type_and_num(cur_page_text):
        """
        Helper func for getting doc_type_pattern instance
        :param cur_page_text:
        :return:
        """
        for doc_type_pattern in doc_type_patterns:
            # todo: log_config.wrapper func for logging cur page text ; prevent bloating stdout logs`
            # logging.info(
                # f'Using regex pattern {doc_type_pattern} for any matches in current page text:\n************************************************************\n{cur_page_text}\n************************************************************\n')
            doc_type_and_num_matches = re.findall(doc_type_pattern, cur_page_text, re.IGNORECASE)
            if not doc_type_and_num_matches:
                logging.warning(f'Could not find doc_type_and_num on current page text')
                continue  # Skips the rest of the loop body and goes to the next iteration
            else:
                doc_type_and_num = doc_type_and_num_matches[0]
                # assumes first match is correct doc type
                logging.info(
                    f'Current page text has doc_type_and_num: {doc_type_and_num} using pattern: {doc_type_pattern}')
                return doc_type_and_num, doc_type_pattern

        # If you reach here, that means no pattern has matched
        return None
    def get_doc_type_short(self, doc_type_and_num):
        if not doc_type_and_num:
            logging.error(f'doc_type_and_num is None. Could not get doc_type_short from NoneType')
        self.doc_type_short = doc_type_and_num.split('-')[0]

    def initialize_pdf_data(self):
        mod_time, cre_time = self.file_handler.get_file_timestamps(self.pdf_file_path)

        logging.info(f'Prior to updating pdf data instance: {self.pdf_data}\n | Modified Time: {mod_time} | Created Time: {cre_time} | ')

        self.pdf_data = self.update_pdf_data()
        logging.info(f'After updating pdf_data instance using setter: {self.pdf_data}')

    def is_company_name_set(self):
        company_name = self.get_company_name(self.cur_page_text)
        if company_name is not None:
            self.company_name = company_name
            logging.info(f'Updated company_name to: {company_name}')
            return True
        elif self.company_name is not None:  # company_name is already set, no need to update
            return True
        return False  # company_name wasn't set and we couldn't update it

    @handle_errors
    def is_doc_type_pattern_set(self):
        doc_type_and_num, doc_type_pattern = self.get_doc_type_and_num(self.cur_page_text)
        if (doc_type_and_num is not None) and (doc_type_pattern is not None):
            self.doc_type_pattern = doc_type_pattern
            logging.info(f'Updated doc_type_pattern instance to: {doc_type_pattern}')
            self.doc_type_and_num = doc_type_and_num
            logging.info(f'Updated doc_type_and_num instance to: {doc_type_and_num}')
            return True
        elif (self.doc_type_pattern is not None) and (self.doc_type_and_num is not None):  # if doc_type_pattern and doc_type_and_num instances are alraedy set, no need to update
            return True
        return False

    def is_doc_type_pattern_and_company_name_present(self):
        if self.company_name and self.doc_type_pattern in self.cur_page_text:
            return True
        else:
            logging.warning(f'Company name "{self.company_name}" and Document Type pattern: "{self.doc_type_pattern}" not found in current page text')
            return None

    def process_pages(self):
        """
        main processing func
        """
        self.initialize_pdf_data()

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
            logging.error(f"An error occurred trying to process_pages: {e}")
            return False

    # Invoices PDF rename helper
    def rename_invoices_pdf(self):

        # Pass `/Users/ekim/Downloads/messages.pdf` to get PikePDf object
        pdf = self.get_pdf(self.pdf_file_path)

        if pdf is not None:

            self.new_file_name = self.today_str + '.pdf'
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
        month_dir = self.file_handler.construct_month_dir_from_doc_type_short('INV')

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
                logging.info(
                    f'Match found!\n************************\nCompany Name: {company_name} | Company ID: {company_id}\n************************\n')
                # Turn local var to instance var for dynamic file path construction
                self.company_id = company_id
                return self.company_id
        logging.crticial(f'Could not retrieve Company ID from Company Name: {company_name}.')
        return None

    @handle_errors
    def create_and_save_pdf(self, pages, post_processing):

        # todo: helper func for this logic; extend vs append
        if isinstance(pages, list):
            # Merge multi page spanning pdfs w/ page objs instance
            self.new_pdf.pages.extend(pages)
        else:
            # Create single page pdf from page obj instance
            self.new_pdf.pages.append(pages)

        # send to month_dir for all other doc types
        output_file_path = self.construct_final_output_filepath(post_processing)
        logging.info(f'Setting output filepath to: {output_file_path}')

        self.new_pdf.save(output_file_path)
        return True

    @handle_errors
    def get_new_file_name(self):
        if re.match(r'EFT-\s*\d+', self.doc_type_and_num) and re.match(r'-?[\d,]+\.\d+-?', self.total_target_amt):
            logging.critical(
                f'******************************************* self.total_target_amt: {self.total_target_amt} ***********************')
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

            if self.page_num >= len(self.pdf_data.pages) - 1:
                break
        self.cur_page_text = "".join(page_text_strings)
        # print(f'------------cur_page_text--------------------\n')
        # print(self.cur_page_text)
        # print(f'\n--------------------------------')
        logging.info(f'Extracting Document Type and Total Target Amount....')
        self.get_doc_type_short(self.doc_type_and_num)  # set doc_type_short
        self.total_target_amt = self.extraction_handler.extract_total_target_amt(self.cur_page_text)
        logging.info(
            f'Document Type (abbrv): {self.doc_type_short} | Document Type-Number: {self.doc_type_and_num} | Total Target Amount: {self.total_target_amt}')

        # Construct new file name instance
        self.new_file_name = self.get_new_file_name()

        # todo: abstract post processing block into wrapper
        if (self.doc_type_short == 'CCM' or self.doc_type_short == 'LRD') and self.company_name == 'EXXONMOBIL':

            if not self.create_and_save_pdf(page_objs, post_processing=True):
                logging.error(f'Could not create and save multipage w/ post processing required PDF')
                return False

            # Post processing core logic

            ccms_and_lrds_post_processed = self.post_processor.extract_and_post_process(self.company_dir)
            if not ccms_and_lrds_post_processed:
                logging.error(f'ccms_and_lrds_post_processed: {ccms_and_lrds_post_processed}')
            logging.info(f'Successfully post processed CCMs and LRDs')
            return True

        # @dev: post processing not needed multi page spanning pdfs
        elif not self.create_and_save_pdf(page_objs, post_processing=False):
            logging.error(f'Could not create and save multipage PDF')
            return False

        logging.info('Successfully processed all multi pages in PDF')
        return True

    def process_single_page(self):

        # end marker and current instance company name in text
        if 'END MSG' in self.cur_page_text and self.page_num < len(self.pdf_data.pages) - 1:
            page_obj = self.pdf_data.pages[
                self.page_num]  # single pikepdf page obj --> req'd obj to create and save the page

            self.get_doc_type_short(self.doc_type_and_num)  # set doc_type_short
            self.total_target_amt = self.extraction_handler.extract_total_target_amt(self.cur_page_text)
            logging.info(
                f'Document Type (abbrv): {self.doc_type_short} | Document Type-Number: {self.doc_type_and_num} | Total Target Amount: {self.total_target_amt}')

            if self.page_num >= len(self.pdf_data.pages) - 1:
                return  # exit func b/c finished with pdf

            # move page cursor after check; ensures that when last_page_num == len(last_page), it exits and prevents misleading final "error" message that last_page_num + 1 could not be processed
            self.page_num += 1
            # fetch file name
            self.new_file_name = self.get_new_file_name()

            # todo: abstract post processing block into wrapper
            if (self.doc_type_short == 'CCM' or self.doc_type_short == 'LRD') and self.company_name == 'EXXONMOBIL':

                if not self.create_and_save_pdf(page_objs, post_processing=True):
                    logging.error(f'Could not create and save single page  w/ post processing required PDF')
                    return False

                # Post processing core logic

                ccms_and_lrds_post_processed = self.post_processor.extract_and_post_process(self.company_dir)
                if not ccms_and_lrds_post_processed:
                    logging.error(f'ccms_and_lrds_post_processed: {ccms_and_lrds_post_processed}')
                logging.info(f'Successfully post processed CCMs and LRDs')
                return True

            # Create single page pdf and save in correct dir
            elif not self.create_and_save_pdf(page_obj, post_processing=False):
                logging.error(f'Could not create and save single page PDF')
                return False
            logging.info('Successfully processed all multi pages in PDF')
            return True
