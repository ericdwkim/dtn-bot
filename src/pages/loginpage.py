import os
from selenium.webdriver.common.by import By
from .basepage import BasePage

# Environmental variables
dtn_url = os.getenv('DTN_URL')

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def visit(self):
        self.driver.get(dtn_url)

    def enter_username(self, username):
        username_field = self.driver.find_element(By.CSS_SELECTOR, '#username')
        username_field.click()
        username_field.send_keys(username)
        # username_field = self.find_element_and_click('#username')
        # username_field_submitted = self.find_element_and_click_and_send_keys('#username', username)

    def enter_password(self, password):
        password_field = self.driver.find_element(By.CSS_SELECTOR, '.loginContent > form:nth-child(3) > div:nth-child(2) > input:nth-child(1)')
        password_field.click()
        password_field.send_keys(password)
        # password_field = self.find_element_and_click('.loginContent > form:nth-child(3) > div:nth-child(2) > input:nth-child(1)')
        # password_field_submitted = self.find_element_and_click_and_send_keys('.loginContent > form:nth-child(3) > div:nth-child(2) > input:nth-child(1)', password)

    def click_login_button(self):
        self.driver.find_element(By.CSS_SELECTOR, '.confirmButton').click()
        # self.find_element_and_click('.confirmButton')

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

