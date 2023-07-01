# from config import setup_config
import os
from subprocess import run
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage
from utils.pdf_processor import PdfProcessor
from utility import setup_driver, teardown_driver
from utils.mappings_refactored import (company_names,
                      regex_patterns, doc_type_abbrv_to_doc_type_dir_map, company_id_to_company_subdir_map)


def user_journey():

    # Run the shell script to delete PDF files from previous session
    run(["../scripts/delete_pdf_files.sh"], shell=True)
    print(f'===========================================================================================')

    # Set environmental variables
    username = os.getenv('DTN_EMAIL_ADDRESS')
    password = os.getenv('DTN_PASSWORD')

    driver = setup_driver()

    try:
        # Visit site and login
        login_page = LoginPage(driver)
        login_page.visit_and_login(username, password)

        # DataConnect 1st Flow - Invoices
        data_connect = DataConnectPage(driver)
        data_connect.switch_tab_set_filters_and_download_invoices()
        PdfProcessor.rename_and_delete_pdf()

        # DataConnect 2nd Flow - Draft Notice
        group_filter_set_to_draft_notice = data_connect.set_group_filter_to_draft_notice()
        if not group_filter_set_to_draft_notice:
            return
        draft_notices_processed_and_filed = PdfProcessor.process_pdfs()
        if not draft_notices_processed_and_filed:
            return

        print(f'draft_notices_processed_and_filed: {draft_notices_processed_and_filed}')
        # DataConnect 3rd Flow - Credit Cards
        if draft_notices_processed_and_filed:
            original_eft_messages_pdf_is_deleted = rename_and_delete_pdf(full_path_to_downloaded_pdf)

            print(f'original_eft_messages_pdf_is_deleted: {original_eft_messages_pdf_is_deleted}')
        # Switch date from yesterday's to today's
        date_set_to_today = data_connect.set_date_filter('#date > option:nth-child(1)')
        if not date_set_to_today:
            return

        # Reset Translated to No
        translated_set_to_no = data_connect.set_translated_filter_to_no()
        print(f'translated_set_to_no: {translated_set_to_no}')
        if not translated_set_to_no:
            return

        # Set Group filter to CC
        group_filter_set_to_credit_card = data_connect.set_group_filter_to_credit_card()
        print(f'group_filter_set_to_credit_card: {group_filter_set_to_credit_card}')
        if not group_filter_set_to_credit_card:
            return

        # Download CC PDF
        ccm_files_downloaded = data_connect.check_all_then_click_print()
        print(f'ccm_files_downloaded: {ccm_files_downloaded}')
        if not ccm_files_downloaded:
            return

        # CCM, LRD files
        ccm_files_processed = process_pdfs(full_path_to_downloaded_pdf,
                                           company_name_to_subdir_full_path_mapping_credit_cards, company_names,
                                           regex_patterns, doc_type_abbrv_to_doc_type_dir_map,
                                           company_id_to_company_subdir_map, post_processing=True)
        if ccm_files_processed:
            # original_ccm_messages_pdf_is_deleted = rename_and_delete_pdf(full_path_to_downloaded_pdf)
            # print(f'Finished! original_ccm_messages_pdf_is_deleted: {original_ccm_messages_pdf_is_deleted}')
            print(f'*********************************** SUCCESS *****************************************************')

    finally:
        teardown_driver(driver)


if __name__ == '__main__':
    user_journey()

"""

# Usage:
processor = PdfProcessor("example.pdf")
processor.rename_and_delete_pdf()

"""