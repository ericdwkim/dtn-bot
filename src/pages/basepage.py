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

    # TODO: Abstracted function for WebDriverWait use cases
    # def wait_for_page_to_load(self, timeout=10):
    #     WebDriverWait(self.driver, timeout).until(
    #         lambda driver: driver.execute_script("return document.readyState") == "complete"
    #     )

# def wait_for_element(self, locator, locator_type=By.ID, timeout=10):
#     element = WebDriverWait(self.driver, timeout).until(
#         EC.presence_of_element_located((locator_type, locator))
#     )
#     return element

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def visit(self):
        self.driver.get(self.url)

    def login(self):
        self.username = username
        self.password = password

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # def switch_tab(self):
    #     self.driver
# TODO: use abstracted wait function like so
# element = DataConnectPage.wait_for_element("my_element_id")