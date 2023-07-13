import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import

class BaseDriver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # TODO: argument flag to toggle b/w headless or maximized; less repo changes/commits
        # options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def teardown_driver(self):
        self.driver.quit()


class LoginPageDriver(BaseDriver):
    def __init__(self):
        super().__init__()
        self.login_page = LoginPage(BaseDriver)

        login_page.visit_and_login()

    def visit_and_login(self):
        try:
            # implementation of visit_and_login
            return True
        except Exception as e:
            logging.error('Failed to visit and login: %s', e)
            return False


class DataConnectDriver(BaseDriver):
    def __init__(self):
        super().__init__()

    def switch_tab(self):
        try:
            # implementation of switch_tab
            return True
        except Exception as e:
            logging.error('Failed to switch tab: %s', e)
            return False


def visit_login_and_switch_tab_to_data_connect(username, password):
    try:
        loginDriver = LoginPageDriver(username, password)
        siteVisitedAndLoggedIn = loginDriver.visit_and_login()
        if not siteVisitedAndLoggedIn:
            raise RuntimeError('Something went wrong')

        dataConnect = DataConnectDriver()
        tabSwitchedToDataConnect = dataConnect.switch_tab()
        if not tabSwitchedToDataConnect:
            raise RuntimeError('Something went wrong')

    except Exception as e:
        logging.error('Something went wrong: %s', e)
        return False

    finally:
        loginDriver.teardown_driver()
        dataConnect.teardown_driver()
