import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# Environmental variables
username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
dtn_url = os.getenv('DTN_URL')

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = dtn_url

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def visit(self):
        self.driver.get(self.url)

    def login(self):
        self.username = username
        self.password = password

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # def do_something(self):
    #     # interacting with elements, etc.
    #     pass
