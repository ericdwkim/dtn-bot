import os
from subprocess import run
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage
from utility import setup_driver, teardown_driver
from utils.pdf_handler import process_pdfs, rename_and_move_pdf, get_full_path_to_dl_dir, rename_and_delete_pdf
import subprocess
from utils.post_processing import is_last_day_of_month, end_of_month_operations
from utils.mappings import (keyword_in_dl_file_name, download_dir, company_names,
                      regex_patterns, company_name_to_subdir_full_path_mapping_fuel_drafts,
                      company_name_to_subdir_full_path_mapping_credit_cards)

# Run the shell script to delete PDF files from previous session
# run(["../scripts/delete_pdf_files.sh"], shell=True)
# print(f'===========================================================================================')

# Set environmental variables
username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')

def user_journey():
    driver = setup_driver()

    full_path_to_downloaded_pdf = get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name)

    try:
        # Visit site and login
        login_page = LoginPage(driver)
        login_page.visit_and_login(username, password)

        """
        # DataConnect 1st Flow - Invoices
        """

        data_connect = DataConnectPage(driver)
        data_connect.switch_tab_set_filters_and_download_invoices()
        invoices_renamed_and_filed_away = rename_and_move_pdf(keyword_in_dl_file_name, download_dir)
        if invoices_renamed_and_filed_away and is_last_day_of_month():
            end_of_month_operations()


        """
        # DataConnect 2nd Flow - Draft Notice
        """
        print(f'*********************** STARTING 2nd FLOW ***********************')

        group_filter_set_to_draft_notice = data_connect.set_group_filter_to_draft_notice()
        if not group_filter_set_to_draft_notice:
            return
        print(f'*********************** group_filter_set_to_draft_notice *********************** {group_filter_set_to_draft_notice}')

        draft_notices_processed_and_filed = process_pdfs(full_path_to_downloaded_pdf, company_name_to_subdir_full_path_mapping_fuel_drafts, company_names, regex_patterns, post_processing=False)
        if not draft_notices_processed_and_filed:
            print(
                f'*********************** draft_notices_processed_and_filed *********************** {draft_notices_processed_and_filed}')
            return

        print(f'draft_notices_processed_and_filed: {draft_notices_processed_and_filed}')

        """
        # DataConnect 3rd Flow - Credit Cards
        """

        if draft_notices_processed_and_filed:
            original_eft_messages_pdf_is_deleted = rename_and_delete_pdf(full_path_to_downloaded_pdf)

            print(f'original_eft_messages_pdf_is_deleted: {original_eft_messages_pdf_is_deleted}')
        # Switch date from yesterday's to today's
        print(f'STARTING 3RD FLOW ***********************')
        date_set_to_today = data_connect.set_date_filter(third_flow=True)
        if not date_set_to_today:
            return
        print(f'date_set_to_today *********************** {date_set_to_today}')


        # Reset Translated to No
        translated_set_to_no = data_connect.set_translated_filter_to_no(third_flow=True)
        print(f'translated_set_to_no: {translated_set_to_no}')
        if not translated_set_to_no:
            return
        print(f'translated_set_to_no *********************** {translated_set_to_no}')

        # Set Group filter to CC
        group_filter_set_to_credit_card = data_connect.set_group_filter_to_credit_card()
        print(f'group_filter_set_to_credit_card: {group_filter_set_to_credit_card}')
        if not group_filter_set_to_credit_card:
            return
        print(f'group_filter_set_to_credit_card *********************** {group_filter_set_to_credit_card}')

        # Download CC PDF
        ccm_files_downloaded = data_connect.check_all_then_click_print()
        print(f'ccm_files_downloaded: {ccm_files_downloaded}')
        if not ccm_files_downloaded:
            return
        print(f'ccm_files_downloaded *********************** {ccm_files_downloaded}')

        # CCM, LRD files
        ccm_files_processed = process_pdfs(full_path_to_downloaded_pdf, company_name_to_subdir_full_path_mapping_credit_cards, company_names, regex_patterns, post_processing=True)
        print(f'**********************  ccm_files_processed: {ccm_files_processed} ***********************')
        if ccm_files_processed:
            original_ccm_messages_pdf_is_deleted = rename_and_delete_pdf(full_path_to_downloaded_pdf)
            print(f'Finished! original_ccm_messages_pdf_is_deleted: {original_ccm_messages_pdf_is_deleted}')

    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()

