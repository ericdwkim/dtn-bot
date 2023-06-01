from ..pages import HomePage, LoginPage
from ..pages.utility import setup_driver, teardown_driver

def user_journey():
    driver = setup_driver()

    try:
        # Go to login page and login
        login_page = LoginPage(driver)
        login_page.visit()

        #
        home_page = HomePage(driver)
        home_page.visit()

        # perform actions on pages...
    finally:
        teardown_driver(driver)