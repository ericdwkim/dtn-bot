import logging
import os
from pikepdf import Pdf
import pdfplumber
import io
import re
from datetime import datetime


class ExtractionHandler():
    def __init__(self):
        self.today = datetime.today().strftime('%m-%d-%y')


    @staticmethod
    def extract_ccm_data(pdf_file):
        """
        Extracts CCM relevant data from List of tuples with target data
        :param pdf_file:
        :return:
        """
        filename = os.path.basename(pdf_file)
        match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)-?\.pdf', filename)
        if match:
            doc_type_num = int(match.group(1))
            total_amount = float(match.group(2).replace(',', ''))
            return doc_type_num, total_amount
        return None, None

    @staticmethod
    def extract_lrd_data(pdf_file):
        """
        Extracts LRD relevant data from list of tuples
        :param pdf_file:
        :return:
        """
        match = re.match(r'LRD-(\d+)-.*\.pdf', pdf_file)
        if match:
            doc_type_num = match.group(1)
            return doc_type_num, None
        return None, None


    @staticmethod
    def extract_text_from_pdf_page(pdf_page):
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

    def extract_pdf_data(self, company_dir):
        """
        Extracts target data from filenames for calculation for post-processing
        :param company_dir: path to company name directory
        :return: Tuple (List, Int, List) where each List contains tuples of pre-extracted data relevant for CCM and LRD, respectively.
        """

        pdf_files = [f for f in os.listdir(company_dir) if f.endswith('.pdf')]
        logging.info(f'************************ pdf_files ******************** : {pdf_files}\n')
        pdf_data_ccm = []
        pdf_data_lrd = []
        total_amount = 0.00
        for pdf_file in pdf_files:
            if pdf_file.startswith('CCM'):
                doc_type_num_ccm, amount = self.extract_ccm_data(pdf_file)
                total_amount += amount
                total_amount = round(total_amount, 2)  # Round to two decimal places
                pdf_data_ccm.append((doc_type_num_ccm, self.today, total_amount, os.path.join(company_dir, pdf_file)))
            elif pdf_file.startswith('LRD'):
                doc_type_num_lrd, _ = self.extract_lrd_data(pdf_file)
                pdf_data_lrd.append((doc_type_num_lrd, self.today, _, os.path.join(company_dir, pdf_file)))
        pdf_data_ccm.sort(key=lambda x: x[0])
        logging.info(f'*********************************** pdf_data_ccm {pdf_data_ccm}\n')
        pdf_data_lrd.sort(key=lambda x: x[0])
        logging.info(f'*********************************** pdf_data_lrd {pdf_data_lrd}\n')

        return pdf_data_ccm, total_amount, pdf_data_lrd

    @staticmethod
    def extract_doc_type_and_total_target_amt(pattern, cur_page_text):
        """
        replaces deprecated `extract_info_from_text`
        :param pattern:
        :param cur_page_text:
        :return:
        """

        doc_type = pattern.split('-')[0]

        if doc_type is None:
            logging.warning(f'Could not find document type using pattern {pattern} in current text: {cur_page_text}')
            return None, None

        total_amount_matches = re.findall(r'-?[\d,]+\.\d+-?', cur_page_text)

        logging.info(f'\nGetting total_amount_matches: {total_amount_matches}\n')
        if total_amount_matches:
            total_target_amt = total_amount_matches[-1]
        else:
            total_target_amt = None

        return doc_type, total_target_amt
