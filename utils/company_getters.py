# from utils.mappings_refactored import company_id_to_company_subdir_map
#
# @classmethod
# def get_company_id(company_name):
#     for id, subdir in company_id_to_company_subdir_map.items():
#         if company_name == subdir.split('[')[0].strip():
#             return id
#     return None
# @classmethod
# def get_company_name(page_text):
#
#     if company_name in page_text:
#
#
#
#
#
#     company_names = []
#     for company_dir in company_id_to_company_subdir_map.values():
#         # Slice the string to remove the company id and brackets
#         company_name = company_dir.split('[')[0].strip()
#         company_names.append(company_name)
#     return company_names
#
