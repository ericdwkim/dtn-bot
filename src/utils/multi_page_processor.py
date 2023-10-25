import pikepdf, logging, os
class MultiPageProcessor:
    def __init__(self):
        self.page_objs = []
        self.cur_page_text = ''
        self.page_num = 0
        self.doc_type_short, self.total_target_amt = ('', '')
        self.pdf_data = self.update_pdf_data() # PikePDF instance var
        self.pdf_file_path = os.path.join(self.download_dir, 'messages.pdf')


    @staticmethod
    def get_pdf(filepath):
        if not os.path.exists(filepath):
            logging.info(f'File path does not exist: "{filepath}"')
            return None
        else:
            logging.info(f'Filepath: "{filepath}" exists. Returning opened PikePdf object')
            return pikepdf.open(filepath)

    def update_pdf_data(self):
        self.pdf_data = self.get_pdf(self.pdf_file_path)
        return self.pdf_data


    def collect_page_data(self):
        self.page_objs.clear()  # Clear existing page objs
        page_text_strings = []

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

    def log_extraction_info(self):
        self.doc_type_short = self.get_doc_type_short(self.doc_type_and_num)
        self.total_target_amt = self.extraction_handler.extract_total_target_amt(self.cur_page_text)
        logging.info(
            f'Document Type (abbrv): {self.doc_type_short} | Document Type-Number: {self.doc_type_and_num} | Total Target Amount: {self.total_target_amt}'
        )

    def process_with_post_processing(self):
        if not self.create_and_save_pdf(self.page_objs, post_processing=True):
            logging.error('Could not create and save multipage w/ post processing required PDF')
            return False

        return self.post_processor.extract_and_post_process(self.company_dir)

    def process_without_post_processing(self):
        if not self.create_and_save_pdf(self.page_objs, post_processing=False):
            logging.error('Could not create and save multipage PDF')
            return False
        return True

    def process_multi_page(self):
        self.collect_page_data()
        self.log_extraction_info()

        if (self.doc_type_short == 'CCM' or self.doc_type_short == 'LRD') and self.company_name == 'EXXONMOBIL':
            return self.process_with_post_processing()
        else:
            return self.process_without_post_processing()
