from selenium.webdriver.common.by import By
from .basepage import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def enter_username(self, username):
        # username_field = self.driver.find_element(By.CSS_SELECTOR, '#username')
        # username_field.click()
        # username_field.send_keys(username)
        # TESTING ------------------------------------------------
        username_field = LoginPage.find_element_and_click('#username')
        username_field_submitted = LoginPage.find_element_and_click_and_send_keys(username)

    def enter_password(self, password):
        # password_field = LoginPage.find_element_and_click()
        # password_field = self.driver.find_element(By.CSS_SELECTOR, '.loginContent > form:nth-child(3) > div:nth-child(2) > input:nth-child(1)')
        # password_field.click()
        # password_field.send_keys(password)
        # TESTING ------------------------------------------------
        password_field = LoginPage.find_element_and_click('.loginContent > form:nth-child(3) > div:nth-child(2) > input:nth-child(1)')
        password_field_submitted = LoginPage.find_element_and_click_and_send_keys(password)

    def click_login_button(self):
        self.driver.find_element(By.CSS_SELECTOR, '.confirmButton').click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
