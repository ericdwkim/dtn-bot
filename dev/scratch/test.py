# from utils.mappings_refactored import (doc_type_patterns, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)
# from utils.pdf_processor import PdfProcessor
#
#
#
# processor = PdfProcessor()
#
# processor.process_pdfs(post_processing=False)
#
#
#
doc_type_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}


for pattern in doc_type_patterns:
    print(pattern)