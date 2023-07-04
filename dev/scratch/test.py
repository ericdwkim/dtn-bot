from utils.pdf_processor import PdfProcessor
from utils.mappings_refactored import doc_type_abbrv_to_doc_type_subdir_map, doc_type_patterns, company_id_to_company_subdir_map
import re
#
processor = PdfProcessor()

# First, create a new dictionary where company names are keys and company IDs are values

# company_subdir_to_id_map = {v: k for k, v in company_id_to_company_subdir_map.items()}

# def get_company_id(company_name):
#     company_subdir_to_id_map = {v: k for k, v in company_id_to_company_subdir_map.items()}
#     print(company_subdir_to_id_map)

    # Remove the ID from the company_name (if it's present) for a clean match
    # clean_company_name = re.sub(r'\s*\[\d+\]$', '', company_name)
    # company_id = company_subdir_to_id_map.get(clean_company_name, None)
    #
    # return company_id


# get_company_id('EXXONMOBIL [10005]')


# def search_company(company_name):
#     # case insensitive search
#     company_name = company_name.lower()
#
#     # search and return value
#     for key, value in company_subdir_to_id_map.items():
#         if company_name in key.lower():
#             return value
#
#     # return None if not found
#     return None
#
# # testing function
# company_name = "T"
# print(search_company(company_name))
