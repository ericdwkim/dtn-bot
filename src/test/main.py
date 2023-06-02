from ..pages.basepage import DataConnectPage, LoginPage
from utility import setup_driver, teardown_driver

def user_journey():
    driver = setup_driver()

    try:
        # Visit site and login
        login_page = LoginPage(driver)
        login_page.visit()
        login_page.login()

        # DataConnect navigation
        data_connect = DataConnectPage(driver)
        data_connect.switch_tab(driver)
        data_connect.set_date_filter()
        data_connect.set_translated_filter(driver)

        # perform actions on pages...
    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()