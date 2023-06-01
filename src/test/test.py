from pages import HomePage, LoginPage
from utility import setup_driver, teardown_driver

driver = setup_driver()

try:
    home_page = HomePage(driver)
    home_page.visit()

    login_page = LoginPage(driver)
    login_page.visit()
    # perform actions on pages...
finally:
    teardown_driver(driver)