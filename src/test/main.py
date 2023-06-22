import os
import time
from pikepdf import Pdf
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage
from utility import setup_driver, teardown_driver
from pdf_handler import rename_and_move_pdf, process_pdf, get_full_path_to_dl_dir
from dev.process_pdf_and_page_for_ccm import process_pdf_cc
import subprocess

# Run the shell script to delete PDF files from previous session
subprocess.run(["../scripts/delete_pdf_files.sh"], shell=True)
print(f'===========================================================================================')


username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
def user_journey():
    driver = setup_driver()


    # Directory paths
    # TODO: Update with Windows filepaths
    dest_dir_invoices = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/5-May'
    keyword_in_dl_file_name = 'messages'  # downloaded file is defaulted to filename `messages.pdf` on mac
    download_dir = r'/Users/ekim/Downloads'
    full_path_to_downloaded_pdf = get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name)


    # The mapping dictionary for company name to list of keywords for tot_draft_amt, eft_num vars
    company_name_to_search_keyword_mapping = {
        'CVR SUPPLY & TRADING, LLC': ['Total Draft', 'EFT-\d+'],
        'EXXONMOBIL': ['TOTAL AMOUNT OF FUNDS TRANSFER', 'EFT-\d+'],
        'U.S. OIL COMPANY': ['TOTALS', 'EFT-\d+'],
        'VALERO': ['*** Net Amount ***', 'EFT-\d+'],
        'DK Trading & Supply': ['TOTAL DRAFT AMOUNT', 'EFT-\d+']
    }

    company_name_to_search_keyword_mapping_credit_cards = {
        'VALERO': ['-NET CREDIT 51000', 'CCM-\d+']
    }

    # Mapping for company name to Fuel Drafts subdir full path
    company_name_to_subdir_full_path_mapping_fuel_drafts = {
        'CVR SUPPLY & TRADING, LLC': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/CVR Supply & Trading 12351',

        'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/EXXONMOBIL [10005]',

        'U.S. OIL COMPANY': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/U S VENTURE - U S OIL COMPANY [12262]',

        'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/VALERO [10006]',
        
        'DK Trading & Supply': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/DK TRADING [12293]'
    }

    # Mapping for company name to Credit Cards subdir full path
    company_name_to_subdir_full_path_mapping_credit_cards = {

        'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/VALERO [10006]'

    }

    try:
        # Visit site and login
        login_page = LoginPage(driver)
        login_page.visit_and_login(username, password)

        # DataConnect 1st Flow - Invoices
        data_connect = DataConnectPage(driver)
        data_connect.switch_tab_set_filters_and_download_invoices()
        rename_and_move_pdf(keyword_in_dl_file_name, download_dir, dest_dir_invoices)

        # DataConnect 2nd Flow - Draft Notice
        # TODO: if set date has no draft notices (aka draft notice bar not found) then just skip draft notices and continue to 3rd Flow)
        group_filter_set_to_draft_notice = data_connect.set_group_filter_to_draft_notice()
        if not group_filter_set_to_draft_notice:
            return
        draft_notices_processed_and_filed = process_pdf(keyword_in_dl_file_name, company_name_to_subdir_full_path_mapping_fuel_drafts, download_dir, company_name_to_search_keyword_mapping)
        if not draft_notices_processed_and_filed:
            return

        # DataConnect 3rd Flow - Credit Cards
        # if os.path.exists(full_path_to_downloaded_pdf):
        #     try:
        #         os.remove(full_path_to_downloaded_pdf)
        #         print(f'The original Draft Notices PDF File located in: {full_path_to_downloaded_pdf} has been deleted successfully.')
        #     except OSError as e:
        #         print(f"Error deleting file: {str(e)}")
        # else:
        #     print("File does not exist. Cannot proceed.")
        #     return False
        #
        # # Switch date from yesterday's to today's
        # date_set_to_today = data_connect.set_date_filter('#date > option:nth-child(1)')
        # if not date_set_to_today:
        #     return
        #
        # # Reset Translated to No
        # # TODO: this doesn't work for some reason in Test #2
        # translated_set_to_no = data_connect.set_translated_filter_to_no()
        # print(f'translated_set_to_no: {translated_set_to_no}')
        # if not translated_set_to_no:
        #     return
        #
        # # Set Group filter to CC
        # group_filter_set_to_credit_card = data_connect.set_group_filter_to_credit_card()
        # print(f'group_filter_set_to_credit_card: {group_filter_set_to_credit_card}')
        # if not group_filter_set_to_credit_card:
        #     return
        #
        # # Download CC PDF
        # ccm_files_downloaded = data_connect.check_all_then_click_print()
        # print(f'ccm_files_downloaded: {ccm_files_downloaded}')
        # if not ccm_files_downloaded:
        #     return
        #
        # # Process CCM VALERO PDFs only
        # valero_ccm_processed_and_filed = process_pdf_cc(keyword_in_dl_file_name, company_name_to_subdir_full_path_mapping_credit_cards, download_dir, company_name_to_search_keyword_mapping_credit_cards)
        #
        # print(f'valero_ccm_processed_and_filed: {valero_ccm_processed_and_filed}')



    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()