from selenium import webdriver

def setup_driver():
    driver = webdriver.Chrome()
    # Other setup code here...
    return driver

def teardown_driver(driver):
    driver.quit()
    # Other cleanup code here...
