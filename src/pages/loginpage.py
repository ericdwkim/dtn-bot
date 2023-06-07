import os
from selenium.webdriver.common.by import By
from .basepage import BasePage

# Environmental variables
dtn_url = os.getenv('DTN_URL')

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def visit(self):
        """
        Launch browser and navigate to URl
        :return: bool
        """
        try:
            self.driver.get(dtn_url)
            return True
        except Exception as e:
            print(f'An error occurred: {string(e)}')
            return False


    def enter_username(self, username):
        try:
            was_clicked = self.find_element_and_click_and_send_keys('#username', username)
            if was_clicked:
                return True
            else:
                return False
        except Exception as e:
            print(f'An error occurred: {string(e)}')
            return False


    def enter_password(self, password):
        try:
            was_clicked = self.find_element_and_click_and_send_keys('.loginContent > form:nth-child(3) > div:nth-child(2) > input:nth-child(1)', password)
            if was_clicked:
                return True
            else:
                return False
        except Exception as e:
            print(f'An error occurred: {string(e)}')
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
            print(f'An error ocurred: {string(e)}')
            return False

    def login(self, username, password):
        try:
            username_entered = self.enter_username(username)
            password_entered = self.enter_password(password)
            login_btn_clicked = self.click_login_button()
            if username_entered and password_entered and login_btn_clicked:
                return True
            else:
                return False
        except Exception as e:
            print(f'An error occurred: {string(e)}')
            return False

    def visit_and_login(self, username, password):
        try:
            if self.visit():
                print('Browser launched\nLoading site...')
                print('Logging in with provided credentials...')
                logged_in = self.login(username, password)
                if logged_in:
                    return True
                else:
                    print('Unable to log in with provided credentials')
                    return False
            else:
                print('Unable to launch and visit the site')
                return False
        except Exception as e:
            print('An error occurred:', str(e))
            return False

