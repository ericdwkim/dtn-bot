from selenium import webdriver

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    driver = uc.Chrome(use_subprocess=True, version_main=113, options=options)
    return driver

def teardown_driver(driver):
    driver.quit()
    # Other cleanup code here...
