import os
import time
from pikepdf import Pdf
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage
from utility import setup_driver, teardown_driver
from pdf_handler import rename_and_move_pdf, process_pdf, get_full_path_to_dl_dir
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
        'CVR SUPPLY & TRADING, LLC': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/CVR Supply & Trading 12351',
        'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL [10005]',
        'U.S. OIL COMPANY': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/U S VENTURE - U S OIL COMPANY [12262]',
        'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/VALERO [10006]',
        'DK Trading & Supply': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/DK TRADING [12293]'
    }

    company_name_to_search_keyword_mapping_credit_cards = {
        'CVR SUPPLY & TRADING, LLC': 'RTV-\d+',
        'EXXONMOBIL': 'RTV-\d+',
        'U.S. OIL COMPANY': 'RTV-\d+',
        'VALERO': 'RTV-\d+',
        'DK Trading & Supply': 'RTV-\d+'
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
        group_filter_set_to_draft_notice = data_connect.set_group_filter_to_draft_notice()
        if not group_filter_set_to_draft_notice:
            return

        draft_notices_processed_and_filed = process_pdf(keyword_in_dl_file_name, company_name_to_subdir_full_path_mapping_fuel_drafts, download_dir, company_name_to_search_keyword_mapping)

        if not draft_notices_processed_and_filed:
            return



        # DataConnect 3rd Flow - Credit Cards
        if os.path.exists(full_path_to_downloaded_pdf):
            try:
                os.remove(full_path_to_downloaded_pdf)
                print("File deleted successfully.")
            except OSError as e:
                print(f"Error deleting file: {str(e)}")
        else:
            print("File does not exist. Cannot proceed.")
            return False

        # Switch date from yesterday's to today's
        date_set_to_today = data_connect.set_date_filter()

        # Wait for UI to update date change
        time.sleep(45)
        if not date_set_to_today:
            return

        # Reset Translated to No
        translated_set_to_no = data_connect.set_translated_filter_to_no()
        if not translated_set_to_no:
            return

        group_filter_set_to_credit_card = data_connect.set_group_filter_to_credit_card()
        if not group_filter_set_to_credit_card:
            return

        print_button_clicked = data_connect.click_print_button()
        if not print_button_clicked:
            return

        # process_pdf(keyword_in_dl_file_name, company_name_to_subdir_full_path_mapping_credit_cards, download_dir, company_name_to_search_keyword_mapping_credit_cards)





    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()