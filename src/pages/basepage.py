from selenium import webdriver
from selenium.webdriver.common.by import By

# Environmental variables
username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
dtn_url = os.getenv('DTN_URL')

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = dtn_url
        self.password = password
        self.username = username

    def visit(self):
        self.driver.get(self.url)

    def login(self, username, password):
        # implementation of the login
        pass


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = dtn_url

    def visit(self):
        self.driver.get(self.url)

    def do_something(self):
        # interacting with elements, etc.
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
