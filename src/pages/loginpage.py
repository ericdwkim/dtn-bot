import os
from selenium.webdriver.common.by import By
from .basepage import BasePage


class LoginPage(BasePage):
    def __init__(self, base_driver):
        super().__init__(base_driver)
        self.url = os.getenv('DTN_URL')
        self.username = os.getenv('DTN_EMAIL_ADDRESS')
        self.password = os.getenv('DTN_PASSWORD')

    def visit(self):
        """
        Launch browser and navigate to URl
        :return: bool
        """
        try:
            self.driver.get(self.url)
            return True
        except Exception as e:
            print(f'Browser could not be launched\nAn error occurred: {str(e)} ')
            return False


    def enter_username(self):
        try:
            was_clicked = self.find_element_and_click_and_send_keys('#username', self.username)
            if was_clicked:
                return True
            else:
                return False
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False


    def enter_password(self):
        try:
            was_clicked = self.find_element_and_click_and_send_keys('.loginContent > form:nth-child(3) > div:nth-child(2) > input:nth-child(1)', self.password)
            if was_clicked:
                return True
            else:
                return False
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False
    def click_login_button(self):
        """
        find_element)_ + click() wrapper
        :return: bool
        """
        try:
            was_clicked, element_selector_clicked = self.find_element_and_click('.confirmButton')
            if was_clicked:
                return True
            else:
                return False
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False

    def login(self):
        try:
            username_entered = self.enter_username()
            password_entered = self.enter_password()
            login_btn_clicked = self.click_login_button()
            if username_entered and password_entered and login_btn_clicked:
                return True
            else:
                print(f'Could not login with provided credentials')
                return False
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False

    def visit_and_login(self):
        try:
            if not self.visit():
                return False
            if not self.login():
                return False
            else:
                print('Browser launched!')
                return True
        except Exception as e:
            print(f'exception: {e}')
