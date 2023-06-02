from ..pages.basepage import HomePage, LoginPage
from utility import setup_driver, teardown_driver

def user_journey():
    driver = setup_driver()

    try:
        # Go to login page and login
        login_page = LoginPage(driver)
        login_page.visit()
        login_page.login()

        # DataConnect tab
        data_connect = DataConnectPage(driver)

        # Memory allocation check for identical WebDriver instance being shared b/w pages
        # print(f'LoginPage driver instance: {type(login_page.driver)}')
        # print(f'HomePage driver instance: {type(home_page.driver)}')

        # perform actions on pages...
    finally:
        teardown_driver(driver)

if __name__ == '__main__':
    user_journey()