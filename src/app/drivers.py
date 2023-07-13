import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from ..pages.loginpage import LoginPage
from ..pages.dataconnectpage import DataConnectPage

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
        self.login_page = LoginPage(self)


    def visit_and_login(self):
        self.login_page.visit_and_login()


class DataConnectDriver(BaseDriver):
    def __init__(self):
        super().__init__()
        self.data_connect_page = DataConnectPage(self)


    def switch_tab(self):
        self.data_connect_page.switch_tab()

    def set_date_filter(self):
        self.data_connect_page.set_date_filter()

    def set_translated_filter_to_no(self):
        self.data_connect_page.set_translated_filter_to_no()

    def set_group_filter_to_invoice(self):
        self.data_connect_page.set_group_filter_to_invoice()


    # todo: fill out with required instance methods to be used in flow_manager.py

