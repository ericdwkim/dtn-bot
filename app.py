import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Environmental variables
username = os.getenv('DTN_EMAIL_ADDRESS')
password = os.getenv('DTN_PASSWORD')
dtn_url = os.getenv('DTN_URL')

options = webdriver.ChromeOptions()
# options.add_argument('--headless=new')
options.add_argument('--start-maximized')
driver = uc.Chrome(use_subprocess=True, version_main=113, options=options)
driver.get(dtn_url)

# Login
usrname_txtbox_selector = driver.find_element(By.CSS_SELECTOR, '#username')
usrname_txtbox_selector.click()
usrname_txtbox_selector.send_keys(username)
pw_txtbox_selector = driver.find_element(By.CSS_SELECTOR, '.loginContent > form:nth-child(3) > div:nth-child(2) > input:nth-child(1)')
pw_txtbox_selector.click()
pw_txtbox_selector.send_keys(password)
login_btn_selector = driver.find_element(By.CSS_SELECTOR, '.confirmButton').click()

# Switch to `DataConnect` tab
dc_tab_wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')))
dc_tab_selector = driver.find_element(By.CSS_SELECTOR, '#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)').click()

# Set date to yesterday
yesterday_date_selector = driver.find_element(By.CSS_SELECTOR, '#date > option:nth-child(2)')
yesterday_date_selector.click()

# Apply Translated filter
translated_filter_wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)')))
translated_filter_selector = driver.find_element(By.CSS_SELECTOR, 'th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)')
translated_filter_selector.click()



n = 8
while n > 1:
    print('testing')
    n = n - 1