from utils.mappings_refactored import (doc_type_patterns, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)
def get_company_names():
    company_names = []
    for company_dir in company_id_to_company_subdir_map.values():
        # Slice the string to remove the company id and brackets
        company_name = company_dir.split('[')[0].strip()
        company_names.append(company_name)
    return company_names


def get_company_name(page_text):
    company_names = get_company_names()
    for company_name in company_names:
        if company_name in page_text:
            return company_name
    # Return None if no company name is found in the page_text
    return None

text = 'VALERO ASDF;AKDJS;SDFKS;AJF;DSAJ'

comp_name = get_company_name(text)
print(comp_name)


# def get_page_text(self, pdf_data):
#     company_names = get_company_names(company_id_to_company_subdir_map)
#     # Extract main large pdf
#     page_text = extract_text_from_pdf_page(pdf_data.pages[self.page_num])
#     for company_name in company_names:
#         for pattern in regex_patterns:
#             if re.search(pattern, page_text, re.IGNORECASE):
#                 # conditional for multi "mini" pdfs
#                 if company_name in page_text and 'END MSG' not in page_text:
#                     self.process_multi_page(pdf_data, page_text, pattern)
#                 # conditional for single "mini" pdfs
#                 else:
#                     self.process_single_page(pdf_data, page_text, pattern)
#
#     # return the text for each instance of pdf_data
#     return page_text
