import os, re, logging, pikepdf, shutil
from datetime import datetime
from src.utils.log_config import handle_errors  # TODO
from src.utils.file_handler import FileHandler
from src.utils.extraction_handler import ExtractionHandler

class PDFPostProcessor:

    def __init__(self):
        self.today = datetime.today().strftime('%m-%d-%y')
        self.file_handler = FileHandler()
        self.extraction_handler = ExtractionHandler()
        self.new_pdf= pikepdf.Pdf.new()


    def merge_pdfs(self, pdf_data):
        """
        Merges PDFs by fetching 4th element in tuple `file_path` by looping, opening each file_path\nand creating them as pikePDF pages to combine and merge them all into a single PDF object
        :param pdf_data:
        """

        for _, _, _, file_path in pdf_data:
            try:
                pdf = pikepdf.Pdf.open(file_path)
                self.new_pdf.pages.extend(pdf.pages)
            except pikepdf.PdfError:
                return False
        merged_pdf = self.new_pdf
        return merged_pdf

    def get_new_file_name_for_merged_ccm_or_lrd_docs(self, doc_type_short, total_amount_sum):
        if doc_type_short == 'CCM':
            new_file_name = f'{doc_type_short}-{self.today}-{total_amount_sum}.pdf'
        else:
            new_file_name = f'{self.today}-Loyalty.pdf'
        return new_file_name

    def construct_final_output_path(self, doc_type_short, company_id):
        try:
            month_directory = self.file_handler.construct_month_dir_from_doc_type_short(doc_type_short, company_id)

            if not month_directory:
                logging.error(f'Could not construct month directory from doc_type_short: {doc_type_short} and company_id: {company_id}')

            output_path = os.path.join(month_directory, new_file_name)

            return output_path

        except Exception as e:
            logging.exception(f'An unexpected error occurred trying to construct final output path for post processing: {e}')
            return None


    def save_merged_pdf(self, merged_pdf, output_path):
        try:
            merged_pdf.save(output_path)
            merged_pdf.close()
            logging.info(f'Post processed PDFs have been merged, renamed and saved: {output_path}')
            return True
        except Exception as e:
            logging.exception(f'An unexpected error has occurred trying to save_merged_pdf: {e}')

    def merge_rename_and_save(self, pdf_data, doc_type_short, total_amount_sum, company_id):

        merged_pdf = self.merge_pdfs(pdf_data)
        if not merged_pdf:
            logging.error(f'PDFs could not be merged using pdf_data: {pdf_data}')
            return False

        new_file_name = self.get_new_file_name_for_merged_ccm_or_lrd_docs(doc_type_short, total_amount_sum)
        if not new_file_name:
            logging.error(f'Could not get new file name for merged {doc_type_short} document')
            return False

        output_path = self.construct_final_output_path(doc_type_short, company_id)
        if not output_path:
            logging.error(f'Output path could not be constructed using args: doc_type: {doc_type} / company_id: {company_id}')
            return False

        merged_pdf_is_saved = self.save_merged_pdf(merged_pdf, output_path)
        if not merged_pdf_is_saved:
            logging.error(f'Could not save merged pdf using args: merged_pdf: {merged_pdf} | output_path: {output_path}')
            return False

        logging.info(f'Successfully merged, renamed, and saved post-processed PDFs!')
        return True

    # todo: use decorate `    @handle_errors

    def get_pdf_data_and_total_amount_sum(self, company_dir):
        pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = self.extraction_handler.extract_pdf_data(company_dir)
        # todo: fix log and use decorate
        logging.info(
            f'********************* pdf_data_ccm: {pdf_data_ccm}\n total_amount_sum_ccm: {total_amount_sum_ccm}\n *********** pdf_data_lrd {pdf_data_lrd} ')
        return pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd


    def post_processor(self, company_dir, pdf_data, doc_type_short, total_amount_sum=None, company_id='10005'):
        try:
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

        except Exception as e:
            logging.exception(f'An unexpected error occurred trying to post_process document type: {doc_type_short}. Error Message: {e}')
            return False


    def extract_and_post_process(self, company_dir):
        try:
            pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = self.extraction_handler.extract_pdf_data(company_dir)

            ccms_pdf_post_processed = self.post_processor(company_dir, pdf_data_ccm, doc_type_short='CCM', total_amount_sum=total_amount_sum_ccm)

            if not ccms_pdf_post_processed:
                logging.warning(f'Could not post process CCMs')


            lrds_pdf_post_processed = self.post_processor(company_dir, pdf_data_lrd, doc_type_short='LRD')

            if not lrds_pdf_post_processed:
                logging.warning(f'Could not post process LRDs')


            if not ccms_pdf_post_processed and not lrds_pdf_post_processed:
                logging.error(f'Could not post process CCMs and LRDs')
                return False

            return True
        except Exception as e:
            logging.exception(f'An unexpected error occurred trying to post process: {e}')
