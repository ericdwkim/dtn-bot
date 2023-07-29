from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# test
def setup_driver():
    """
    Sets up driver instance with preferred options.
    :return: `driver` of WebDriver class
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    # options.add_argument('--start-maximized')
    # @dev: 7/28/23 - Selenium Manager (selenium==4.10.0) includes ChromeDriver upgrade. Deprecated ChromeDriverManager due to v114 cap
    # https://stackoverflow.com/questions/76724939/there-is-no-such-driver-by-url-https-chromedriver-storage-googleapis-com-lates
    driver = webdriver.Chrome(service=Service(executable_path='./chromedriver.exe'), options=options)
    return driver

def teardown_driver(driver):
    """
    Breaks down and closes driver instance
    :param driver:
    :return: None
    """
    driver.quit()
