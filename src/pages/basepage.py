import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Environmental variables
username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
dtn_url = os.getenv('DTN_URL')

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = dtn_url
        self.username = username
        self.password = password

    def wait_for_page_to_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element(self, locator, locator_type=By.CSS_SELECTOR, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((locator_type, locator))
        )
        return element

    def find_element_and_click(self, locator ,locator_type=By.CSS_SELECTOR):
        element_selector = self.driver.find_element(locator_type, locator)
        element_selector_clicked = element_selector.click()
        return element_selector_clicked

    def find_element_and_click_and_send_keys(self, locator, keys_to_send, locator_type=By.CSS_SELECTOR):
        element_selector_clicked = find_element_and_click(locator_type, locator)
        element_selector_clicked.send_keys(keys_to_send)

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