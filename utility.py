from selenium import webdriver
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def teardown_driver(driver):
    driver.quit()
    # Other cleanup code here...
