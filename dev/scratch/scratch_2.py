from utils.mappings_refactored import (doc_type_patterns, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)
from utils.pdf_processor import PdfProcessor
#
# def get_company_names():
#     company_names = []
#     for company_dir in company_id_to_company_subdir_map.values():
#         # Slice the string to remove the company id and brackets
#         company_name = company_dir.split('[')[0].strip()
#         company_names.append(company_name)
#     return company_names
#
#
# def get_company_name(self):
#     # print(f'++++++++++++++++++++ {company_names}')
#     for company_name in company_names:
#         # print(f'++++++++++++++++++++ {company_name}')
#         if company_name in self.page_text:
#             self.company_name = company_name
#             print(f'self.company_name: {self.company_name}|\nself.page_text: {self.page_text}')
#             # return company_name
#     # Return None if no company name is found in the page_text
#     return None
#
# def get_company_id(self):
#     for company_id, company_dir in company_id_to_company_subdir_map.items():
#         if company_name == company_dir.split('[')[0].strip():
#             return company_id
#     return None
# #
# def get_pattern(self):
#     for pattern in doc_type_patterns:
#         if re.search(pattern, self.page_text, re.IGNORECASE):
#             self.pattern = pattern
#     return None





# company_names = get_company_names()
# # print(company_names)
#
# for company_name in company_names:
#     print(company_name)



processor = PdfProcessor()

output  = processor.file_path_mappings['EFT']['100005']
print(output)

# processor.process_pdfs(post_processing=False)