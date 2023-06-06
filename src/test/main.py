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
        login_page.visit()
        print('Launching browser and visiting site')
        login_page.login(username, password)
        print('Logging in....')

        # DataConnect navigation
        data_connect = DataConnectPage(driver)
        data_connect.switch_tab()
        print('Switching from home to DataConnect tab')
        # data_connect.set_date_filter()
        # print('Setting date filter to yesterday')
        data_connect.set_translated_filter()
        # data_connect.set_filters()

        # perform actions on pages...
    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()