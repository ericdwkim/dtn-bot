import os
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage
from utility import setup_driver, teardown_driver
# from pdf_handler import rename_and_move_pdf, rename_and_move_eft
from pdf_handler import rename_and_move_pdf, process_pdf

username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
def user_journey():
    driver = setup_driver()


    # Env vars for file hanlding
    # TODO: test on Windows with prod file paths
    file_name = 'messages'  # downloaded file is defaulted to filename `messages.pdf`
    dl_dir = r'/Users/ekim/Downloads'
    dest_dir_invoices = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/5-May'
    # dest_dir_draft_notices = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/CVR Supply & Training 12351'
    # cvr_supply_trading_company = 'CVR SUPPLY & TRADING, LLC'

    # ------------------------------------- TEST ------------------------------------------------------
    keyword_in_dl_file_name = 'messages'  # downloaded file is defaulted to filename `messages.pdf`
    download_dir = r'/Users/ekim/Downloads'


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

    # Parent directory to Draft Notices companies
    # draft_notices_parent_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts'

    try:
        # Visit site and login
        login_page = LoginPage(driver)
        login_page.visit_and_login(username, password)

        # DataConnect 1st Flow - Invoices
        data_connect = DataConnectPage(driver)
        data_connect.switch_tab_and_apply_filters()
        rename_and_move_pdf(file_name, dl_dir, dest_dir_invoices)

        # DataConnect 2nd Flow - Draft Notice
        data_connect.set_group_filter_to_draft_notice()
        # rename_and_move_eft(file_name, dl_dir, dest_dir_draft_notices, cvr_supply_trading_company)

        # Get full path to each companies' subdirectory as mapping
        # where {company_name: company_subdirectory}
        # # TODO: fix helper fn as CVR and US OIL not being mapped
        # company_name_to_company_subdir_mapping= get_target_directories(draft_notices_parent_dir, company_name_to_search_keyword_mapping)
        # print(f'company_name_to_company_subdir_mapping: {company_name_to_company_subdir_mapping}')


        # process_pdf(keyword_in_dl_file_name, company_name_to_subdir_full_path_mapping, download_dir, company_name_to_search_keyword_mapping)

        process_pdf(company_name_to_subdir_full_path_mapping,  company_name_to_search_keyword_mapping)



    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()