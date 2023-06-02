from selenium.webdriver.common.by import By
from .basePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def switch_tab(self, driver):
        dc_tab_wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')))

        db_tab_selector = self.driver.find_element(By.CSS_SELECTOR, '#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)').click()

    def set_date_filter(self):
        yesterday_date_selector = self.driver.find_element(By.CSS_SELECTOR, '#date > option:nth-child(2)').click()

    def set_translated_filter(self):
        translated_filter_wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)')))

        translated_filter_selector = self.driver.find_element(By.CSS_SELECTOR, 'th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)').click()