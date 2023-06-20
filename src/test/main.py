import os
from pikepdf import Pdf
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage
from utility import setup_driver, teardown_driver
from pdf_handler import rename_and_move_pdf, process_pdf, get_full_path_to_dl_dir


username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
def user_journey():
    driver = setup_driver()


    # Directory paths
    # TODO: Update with Windows filepaths
    dest_dir_invoices = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/5-May'
    keyword_in_dl_file_name = 'messages'  # downloaded file is defaulted to filename `messages.pdf` on mac
    download_dir = r'/Users/ekim/Downloads'
    full_path_to_dl_dir = get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name)


    # The mapping dictionary for company name to list of keywords for tot_draft_amt, eft_num vars
    company_name_to_search_keyword_mapping = {
        'CVR SUPPLY & TRADING, LLC': ['Total Draft', 'EFT-\d+'],
        'EXXONMOBIL': ['TOTAL AMOUNT OF FUNDS TRANSFER', 'EFT-\d+'],
        'U.S. OIL COMPANY': ['TOTALS', 'EFT-\d+'],
        'VALERO': ['*** Net Amount ***', 'EFT-\d+'],
    }

    # Mapping for company name to subdir full path
    company_name_to_subdir_full_path_mapping = {
        'CVR SUPPLY & TRADING, LLC': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/CVR Supply & Trading 12351',

        'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/EXXONMOBIL [10005]',

        'U.S. OIL COMPANY': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/U S VENTURE - U S OIL COMPANY [12262]',

        'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/VALERO [10006]'
    }


    try:
        # Visit site and login
        login_page = LoginPage(driver)
        login_page.visit_and_login(username, password)

        # DataConnect 1st Flow - Invoices
        data_connect = DataConnectPage(driver)
        data_connect.switch_tab_and_apply_filters()
        rename_and_move_pdf(keyword_in_dl_file_name, download_dir, dest_dir_invoices)

        # DataConnect 2nd Flow - Draft Notice
        draft_notices_downloaded = data_connect.set_group_filter_to_draft_notice()

        # ~/Downloads/messages.pdf should only be
        # Draft Notices
        if draft_notices_downloaded:
            pdf = Pdf.open(full_path_to_dl_dir)

            process_pdf(keyword_in_dl_file_name, company_name_to_subdir_full_path_mapping, download_dir, company_name_to_search_keyword_mapping, pdf)



    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()