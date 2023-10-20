import os, re, logging, pikepdf, shutil
from datetime import datetime
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



    def save_merged_pdf(self, file_prefix, merged_pdf, total_amount_sum, company_id):
        """
        Saves pre-merged pike PDF object with constructed filename dependent on doc type with provided target data.
        :param file_prefix: CCM or LRD ; only these for post-processing
        :param merged_pdf:
        :param total_amount_sum:
        :param company_id:
        :return: Bool
        """
        if file_prefix == 'CCM':
            new_file_name = f'{file_prefix}-{self.today}-{total_amount_sum}.pdf'
        else:
            new_file_name = f'{self.today}-Loyalty.pdf'

        month_directory = self.file_handler.construct_month_dir_from_doc_type(file_prefix, company_id)
        output_path = os.path.join(month_directory, new_file_name)

        try:
            merged_pdf.save(output_path)
            merged_pdf.close()
            print(f'{file_prefix} PDFs have been merged, renamed "{new_file_name}" and saved to: {output_path}')
            return True
        except Exception:
            return False

    # todo: clean and refactor w/ error handling and return bool
    def merge_rename_and_summate(self, company_dir):
        """
        Main post-processing wrapper function. Accounts for end of month operations if last day of the month.
        :param company_dir: path to company name directory
        :return: None
        """
        pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = self.extraction_handler.extract_pdf_data(company_dir)
        logging.info(
            f'********************* pdf_data_ccm: {pdf_data_ccm}\n total_amount_sum_ccm: {total_amount_sum_ccm}\n *********** pdf_data_lrd {pdf_data_lrd}  ')

        merged_pdf_ccm = self.merge_pdfs(pdf_data_ccm)
        merged_ccm_pdf_is_saved = self.save_merged_pdf('CCM', merged_pdf_ccm, total_amount_sum_ccm, '10005')
        logging.info(f'merged_pdf_ccm / merged_ccm_pdf_is_saved: {merged_pdf_ccm} / {merged_ccm_pdf_is_saved}')
        # Clean up pre-merged PDFs in EXXON company_dir; loops through file_path (4th elem in tuple) to delete
        self.file_handler.cleanup_files(pdf_data_ccm)
        # PDFs were merged, saved w/ new filename. If it is currently the last day of the month, then perform end of month filesystem management
        if merged_pdf_ccm and merged_ccm_pdf_is_saved and self.file_handler.is_last_day_of_month():
            self.file_handler.end_of_month_operations(company_dir)

        elif merged_ccm_pdf_is_saved and merged_pdf_ccm:
            logging.info(f'merged_ccm_pdf_is_saved: {merged_ccm_pdf_is_saved} | merged_pdf_ccm: {merged_pdf_ccm}')
            return True

        else:
            return False


        merged_pdf_lrd = self.merge_pdfs(pdf_data_lrd)
        merged_lrd_pdf_is_saved = self.save_merged_pdf('LRD', merged_pdf_lrd, None, '10005')
        # Clean up pre-merged PDFs in EXXON company_dir; loops through file_path (4th elem in tuple) to delete
        self.file_handler.cleanup_files(pdf_data_lrd)
        # PDFs were merged, saved w/ new filename. If it is currently the last day of the month, then perform end of month filesystem management
        if merged_pdf_lrd and merged_lrd_pdf_is_saved and self.file_handler.is_last_day_of_month():
            self.file_handler.end_of_month_operations(company_dir)

        elif merged_pdf_lrd and merged_lrd_pdf_is_saved:
            logging.info(f'merged_lrd_pdf_is_saved: {merged_lrd_pdf_is_saved} | merged_pdf_lrd: {merged_pdf_lrd}')
            return True

        else:
            return False
