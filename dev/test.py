from utils.pdf_handler import process_pdfs, rename_and_move_pdf, get_full_path_to_dl_dir, rename_and_delete_pdf
from utils.mappings import (dest_dir_invoices, keyword_in_dl_file_name, download_dir, company_names,
                      regex_patterns, company_name_to_subdir_full_path_mapping_fuel_drafts,
                      company_name_to_subdir_full_path_mapping_credit_cards, root_directory_mapping, company_id_to_company_subdir_map,)


full_path_to_downloaded_pdf = r'/Users/ekim/Downloads/messages.pdf'


# CCM, LRD files
ccm_files_processed = process_pdfs(full_path_to_downloaded_pdf, company_name_to_subdir_full_path_mapping_credit_cards,
                                   company_names, regex_patterns, root_directory_mapping, company_id_to_company_subdir_map, post_processing=True)
if ccm_files_processed:
    # original_ccm_messages_pdf_is_deleted = rename_and_delete_pdf(full_path_to_downloaded_pdf)
    # print(f'Finished! original_ccm_messages_pdf_is_deleted: {original_ccm_messages_pdf_is_deleted}')
    print(f'*********************************** SUCCESS *****************************************************')