from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def setup_driver():
    """
    Sets up driver instance with preferred options.
    :return: `driver` of WebDriver class
    """
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def teardown_driver(driver):
    """
    Breaks down and closes driver instance
    :param driver:
    :return: None
    """
    driver.quit()
