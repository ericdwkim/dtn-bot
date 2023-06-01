from selenium import webdriver
from selenium.webdriver.common.by import By


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = 'http://www.example.com'

    def visit(self):
        self.driver.get(self.url)

    def do_something(self):
        # interacting with elements, etc.
        pass


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = 'http://www.example.com/login'

    def visit(self):
        self.driver.get(self.url)

    def login(self, username, password):
        # implementation of the login
        pass


# usage
driver = webdriver.Chrome()
home = HomePage(driver)
home.visit()
# do more with the home page

login = LoginPage(driver)
login.visit()
login.login('username', 'password')
# do more with the login page
