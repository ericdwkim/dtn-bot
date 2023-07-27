import os
import pikepdf
from extraction_handler import PDFExtractor
from pdf_processor import PdfProcessor

# extractor = PDFExtractor()
#
# # print(extractor)
#
# file_path = r'/Users/ekim/Downloads/messages.pdf'
#
#
# def get_cur_text():
#     if os.path.exists(file_path):
#         pdf = pikepdf.open(file_path)  # Open the PDF file
#         if len(pdf.pages) > 0:
#             cur_pg_text = extractor.extract_text_from_pdf_page(pdf.pages[0])
#             return cur_pg_text
#
#
# cur_text = get_cur_text()
#
# doc_type, tot_tar_amt = extractor.extract_doc_type_and_total_target_amt('CMB-\s*\d+', cur_text)
#
# print(f'doc_type: {doc_type}, tot_tar_amt: {tot_tar_amt}')

processor = PdfProcessor()

tar_file = processor.get_pdf_file_path()
print(tar_file)

# for company_name in PdfProcessor.get_company_names():
#     print(company_name)