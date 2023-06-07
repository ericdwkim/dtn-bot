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
        login_page.visit_and_login(username, password)

        # DataConnect navigation
        # data_connect = DataConnectPage(driver)
        # data_connect.switch_tab_and_apply_filters()

        # perform actions on pages...
    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()