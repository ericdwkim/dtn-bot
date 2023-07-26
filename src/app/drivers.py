import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage

class BaseDriver:
    def __init__(self):
        print(f'Creating new basedriver instance')
        options = webdriver.ChromeOptions()
        # TODO: argument flag to toggle b/w headless or maximized; less repo changes/commits
        # options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
                return False
            else:
                return True
        except Exception as e:
            print(f'An error occurred trying to switch_tab: {e}')
    def set_date_filter(self):
        set_date_filter = self.data_connect_page.set_date_filter()

    def set_translated_filter_to_no(self):
        self.data_connect_page.set_translated_filter_to_no()

    def set_group_filter_to_invoice(self):
        self.data_connect_page.set_group_filter_to_invoice()

#
#     # todo: fill out with required instance methods to be used in flow_manager.py
#
