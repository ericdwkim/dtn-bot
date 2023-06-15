import os
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage
from utility import setup_driver, teardown_driver
from pdf_handler import rename_and_move_pdf

username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
def user_journey():
    driver = setup_driver()


    # Env vars for file hanlding
    file_name = 'messages'  # downloaded file is defaulted to filename `messages.pdf`
    dl_dir = r'/Users/ekim/Downloads'
    dest_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/5-May'


    try:
        # Visit site and login
        login_page = LoginPage(driver)
        login_page.visit_and_login(username, password)

        # DataConnect 1st Flow - Invoices
        data_connect = DataConnectPage(driver)
        data_connect.switch_tab_and_apply_filters()
        rename_and_move_pdf(file_name, dl_dir, dest_dir)

        # DataConnect 2nd Flow - Draft Notice
        data_connect.click_checkbox() # Uncheck checkbox
        data_connect.set_group_filter_to_draft_notice()



        # perform actions on pages...
    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()