import os, re, logging, pikepdf, shutil
from datetime import datetime
from src.utils.log_config import handle_errors
from src.utils.file_handler import FileHandler
from src.utils.extraction_handler import ExtractionHandler

class PostProcessor:

    def __init__(self):
        self.today = datetime.today().strftime('%m-%d-%y')
        self.file_handler = FileHandler()
        self.extraction_handler = ExtractionHandler()

        # @dev: may require redesign with PdfProcessor as parent and PostProcessor as child class
        # would also be able to pass self.new_pdf
        # self.company_dir = company_dir
        # self.doc_type_short = doc_type_short
        # self.total_amount_sum

    # @dev: wasn't sure if this can also use handle_errors due to PdfError exception which would be more specific error handling
    def merge_pdfs(self, pdf_data):
        """
        Merges PDFs by fetching 4th element in tuple `file_path` by looping, opening each file_path\nand creating them as pikePDF pages to combine and merge them all into a single PDF object
        :param pdf_data:
        """
        merged_pdf = pikepdf.Pdf.new()
        for _, _, _, file_path in pdf_data:
            try:
                pdf = pikepdf.Pdf.open(file_path)
                merged_pdf.pages.extend(pdf.pages)
            except pikepdf.PdfError:
                logging.error(f'An error occurred trying to merge_pdfs with provided pdf_data: {pdf_data}')
            return merged_pdf

    def get_new_file_name_for_merged_ccm_or_lrd_docs(self, doc_type_short, total_amount_sum):
        if doc_type_short == 'CCM':
            new_file_name = f'{doc_type_short}-{self.today}-{total_amount_sum}.pdf'
        else:
            new_file_name = f'{self.today}-Loyalty.pdf'
        return new_file_name

    def construct_final_output_path(self, doc_type_short, company_id, new_file_name):
        month_directory = self.file_handler.construct_month_dir_from_doc_type_short(doc_type_short, company_id)

        if not month_directory:
            logging.error(f'Could not construct month directory from doc_type_short: {doc_type_short} and company_id: {company_id}')

        output_path = os.path.join(month_directory, new_file_name)

        return output_path


    @handle_errors
    def save_merged_pdf(self, merged_pdf, output_path):
        merged_pdf.save(output_path)
        merged_pdf.close()
        logging.info(f'Post processed PDFs have been merged, renamed and saved: {output_path}')

    @handle_errors
    def merge_rename_and_save(self, pdf_data, doc_type_short, total_amount_sum, company_id):
        if not pdf_data:
            logging.warning(f'Empty list of PDFs: {pdf_data}')

        merged_pdf = self.merge_pdfs(pdf_data)
        if not merged_pdf:
            logging.error(f'Could not merge PDFs')
            return False

        new_file_name = self.get_new_file_name_for_merged_ccm_or_lrd_docs(doc_type_short, total_amount_sum)

        output_path = self.construct_final_output_path(doc_type_short, company_id, new_file_name)

        merged_pdf_is_saved = self.save_merged_pdf(merged_pdf, output_path)

        if merged_pdf and new_file_name and output_path and merged_pdf_is_saved:
            logging.info(f'Successfully merged, renamed, and saved post-processed PDFs!')
            return True
        logging.error(f'Could not merge, rename, and save post-processed PDFs')
        return False

    @handle_errors
    def post_processor(self, company_dir, pdf_data, doc_type_short, total_amount_sum=None, company_id='10005'):
        merged_renamed_and_saved = self.merge_rename_and_save(pdf_data, doc_type_short, total_amount_sum, company_id)
        logging.info(f'merged_renamed_and_saved: {merged_renamed_and_saved}')

        # Clean up pre-merged PDFs in EXXON company_dir; loops through file_path (4th elem in tuple) to delete
        self.file_handler.cleanup_files(pdf_data)


        # PDFs were merged, saved w/ new filename. If it is currently the last day of the month, then perform end of month filesystem management
        if merged_renamed_and_saved and self.file_handler.is_last_day_of_month():
            self.file_handler.end_of_month_operations(company_dir)

        elif merged_renamed_and_saved:
            logging.info(f'doc type {doc_type_short} | merged_renamed_and_saved: {merged_renamed_and_saved}')
            return True

        logging.error(f'An error occurred trying to post_process document type: {doc_type_short}. Error Message: {e}')
        return False

    @handle_errors
    def extract_and_post_process(self, company_dir):
        pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = self.extraction_handler.extract_pdf_data(company_dir)

        ccms_pdf_post_processed = self.post_processor(company_dir, pdf_data_ccm, 'CCM', total_amount_sum_ccm)

        if not ccms_pdf_post_processed:
            logging.warning(f'Could not post process CCMs')
            return False


        lrds_pdf_post_processed = self.post_processor(company_dir, pdf_data_lrd, 'LRD')

        if not lrds_pdf_post_processed:
            logging.warning(f'Could not post process LRDs')
            return False


        if not ccms_pdf_post_processed and not lrds_pdf_post_processed:
            logging.error(f'Could not post process CCMs and LRDs')
            return False

        return True
