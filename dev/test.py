from utils.mappings_refactored import (regex_patterns, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)
from utils.pdf_processor import PdfProcessor
from utils.mappings_refactored import company_id_to_company_subdir_map

dl_dir = PdfProcessor.download_dir
file_path = dl_dir + '/etf_full.pdf'



PdfProcessor.process_pdfs(file_path, regex_patterns, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)