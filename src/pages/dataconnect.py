from selenium.webdriver.common.by import By
from .basePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def switch_tab(self, driver):
        wait_for_dc_tab = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')))

        db_tab_selector = self.driver.find_element(By.CSS_SELECTOR, '#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)').click()

