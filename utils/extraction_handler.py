from pikepdf import Pdf
import pdfplumber
import io
import re
import datetime
from utils.mappings_refactored import doc_type_abbrv_to_doc_type_subdir_map, doc_type_patterns, company_id_to_company_subdir_map

# TODO: create class PDFExtractor; migrate extraction helpers from post_processing.py as instance methods for this class

class PDFExtractor():
    def __init__(self):
        self.doc_type, self.total_target_amt = (None, None)

    def extract_text_from_pdf_page(self, pdf_page):
        """
        Take in pikepdf Pdf page object, return extracted text from current instance pdf page
        :param pdf_page:
        :return:
        """
        # Create a BytesIO buffer
        pdf_stream = io.BytesIO()

        # Write the page to the buffer
        with Pdf.new() as pdf:
            pdf.pages.append(pdf_page)
            pdf.save(pdf_stream)

        # Use pdfplumber to read the page from the buffer
        pdf_stream.seek(0)
        with pdfplumber.open(pdf_stream) as pdf:
            pdf_page = pdf.pages[0]
            cur_page_text = pdf_page.extract_text()
        return cur_page_text

    def extract_doc_type_and_total_target_amt(self, pattern, cur_page_text):
        """
        replaces deprecated `extract_info_from_text`
        :param pattern:
        :param cur_page_text:
        :return:
        """

        if re.search(pattern, cur_page_text):
            self.doc_type = pattern.split('-')[0]

        if self.doc_type is None:
            print(f'Could not find document type using pattern {pattern} in current text: {cur_page_text}')
            return None, None

        total_amount_matches = re.findall(r'-?[\d,]+\.\d+-?', cur_page_text)

        # print(f'\nGetting total_amount_matches: {total_amount_matches}\n')
        if total_amount_matches:
            self.total_target_amt = total_amount_matches[-1]
        else:
            self.total_target_amt = None

        return self.doc_type, self.total_target_amt
