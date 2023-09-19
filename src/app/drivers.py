import logging
import platform
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


    def visit_and_login(self):
        try:
            visit_and_login = self.login_page.visit_and_login()
            if not visit_and_login:
                return False
            else:
                return True
        except Exception as e:
            print(f'An error occurred trying to visit_and_login: {e}')



class DataConnectDriver:
    def __init__(self, base_driver):
        self.base_driver = base_driver
        self.data_connect_page = DataConnectPage(self.base_driver)


    def switch_tab(self):
        try:
            switch_tab = self.data_connect_page.switch_tab()
            if not switch_tab:
                logging.error('Could not switch tab')
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to switch tab to `Data Connect`: {e}')

    def set_date_filter(self, third_flow=False):
        try:
            set_date_filter = self.data_connect_page.set_date_filter(third_flow)
            if not set_date_filter:
                logging.error('Could not set date filter')
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to set date filter: {e}')

    def set_translated_filter_to_no(self):
        try:
            set_translated_filter_to_no = self.data_connect_page.set_translated_filter_to_no()
            if not set_translated_filter_to_no:
                logging.error('Could not set `Translated` filter to `No`')
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to set `Translated` filter to `No`: {e}')

    def set_group_filter_to_invoice(self):
        try:
            set_group_filter_to_invoice = self.data_connect_page.set_group_filter_to_invoice()
            if not set_group_filter_to_invoice:
                logging.error('Could not set `Group` filter to `Invoice`')
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to set `Group` filter to `Invoice`: {e}')

    def set_group_filter_to_draft_notice(self):
        try:
            set_group_filter_to_draft_notice = self.data_connect_page.set_group_filter_to_draft_notice()
            if not set_group_filter_to_draft_notice:
                logging.error('Could not set `Group` filter to `Draft Notice`')
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to set `Group` filter to `Draft Notice`: {e}')

    def set_group_filter_to_credit_card(self):
        try:
            set_group_filter_to_credit_card = self.data_connect_page.set_group_filter_to_credit_card()
            if not set_group_filter_to_credit_card:
                logging.error('Could not set `Group` filter to `Credit Card`')
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to set `Group` filter to `Credit Card`: {e}')

#
#     # todo: fill out with other required instance methods to be used in flow_manager.py
#
