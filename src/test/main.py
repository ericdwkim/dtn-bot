import os
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage
from utility import setup_driver, teardown_driver

username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
def user_journey():
    driver = setup_driver()

    try:
        # Visit site and login
        login_page = LoginPage(driver)
        # login_page.enter_username()
        login_page.visit()
        login_page.login(username, password)

        # DataConnect navigation
        # data_connect = DataConnectPage(driver)
        # data_connect.switch_tab()
        # data_connect.set_date_filter()
        # data_connect.set_translated_filter(driver)

        # perform actions on pages...
    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()