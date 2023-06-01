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
# options.add_argument('--start-maximized')
driver = uc.Chrome(use_subprocess=True, version_main=113, options=options)
