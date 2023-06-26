# import re
# import pdfplumber
#
# def check_pdf_for_pattern(pdf_file_path, regex_pattern):
#     with pdfplumber.open(pdf_file_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             # if re.match(r'CBK-\s*\d+', regex_pattern, re.IGNORECASE):
#             #     return True
#             if re.search(regex_pattern, text, re.IGNORECASE):
#                 print(text)
#                 return True
#     return False
#
# pdf_file_path = '/Users/ekim/workspace/txb/docs/ccm_full.pdf'
# regex_pattern = r'CBK-\s*\d+'
#
# pattern_found = check_pdf_for_pattern(pdf_file_path, regex_pattern)
# if pattern_found:
#     print("The pattern was found in the PDF.")
# else:
#     print("The pattern was not found in the PDF.")
#
# # import re
# # import pdfplumber
# #
# # def check_pdf_for_pattern(pdf_file_path, regex_pattern):
# #     with pdfplumber.open(pdf_file_path) as pdf:
# #         for page in pdf.pages:
# #             text = page.extract_text()
# #             if re.search(regex_pattern, text):
# #                 return True
# #     return False
# #
# # pdf_file_path = '/Users/ekim/workspace/txb/docs/ccm_full.pdf'
# # regex_pattern = r'CBK-\d+'
# #
# # pattern_found = check_pdf_for_pattern(pdf_file_path, regex_pattern)
# # if pattern_found:
# #     print("The pattern was found in the PDF.")
# # else:
# #     print("The pattern was not found in the PDF.")
