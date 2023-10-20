import logging, platform
from src.utils.log_config import handle_errors
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage

class BaseDriver:
    def __init__(self, headless=False):
        self.headless = headless
        self.setup_driver()

    def setup_driver(self):
        logging.info('Initializing BaseDriver...')
        options = self._get_chrome_options()
        # @dev: for unit testing
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        os_type = platform.system()
        chromedriver_executable_path = self._get_chromedriver_executable_path(os_type)

        self.driver = webdriver.Chrome(
            service=Service(executable_path=chromedriver_executable_path),
            options=options
        )

        logging.info(
            f'Using operating system: "{os_type}".\nConstructing chromedriver instance using executable_path: "{chromedriver_executable_path}"'
        )

    def _get_chrome_options(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless=new')
        else:
            options.add_argument('--start-maximized')
        return options

    def _get_chromedriver_executable_path(self, os_type):
        return '/opt/homebrew/bin/chromedriver' if os_type == 'Darwin' else 'C:\\Users\\ekima\\AppData\\Local\\anaconda3\\envs\\bots\\Lib\\site-packages\\seleniumbase\\drivers\\chromedriver.exe'

    def teardown_driver(self):
        self.driver.quit()

class LoginPageDriver:
    def __init__(self, base_driver):
        self.base_driver = base_driver
        self.login_page = LoginPage(self.base_driver)

    @handle_errors
    def visit_and_login(self):
        return self.login_page.visit_and_login()

class DataConnectDriver:
    def __init__(self, base_driver):
        self.base_driver = base_driver
        self.data_connect_page = DataConnectPage(self.base_driver)

    @handle_errors
    def switch_tab(self):
        return self.data_connect_page.switch_tab()

    @handle_errors
    def set_date_filter(self, third_flow=False):
        return self.data_connect_page.set_date_filter(third_flow)

    @handle_errors
    def set_translated_filter_to_no(self):
        return self.data_connect_page.set_translated_filter_to_no()

    @handle_errors
    def set_group_filter_to_invoice(self):
        return self.data_connect_page.set_group_filter_to_invoice()

    @handle_errors
    def set_group_filter_to_draft_notice(self):
        return self.data_connect_page.set_group_filter_to_draft_notice()

    @handle_errors
    def set_group_filter_to_credit_card(self):
        return self.data_connect_page.set_group_filter_to_credit_card()
