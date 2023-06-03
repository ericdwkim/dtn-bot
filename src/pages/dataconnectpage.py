from selenium.webdriver.common.by import By
from .basePage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # TODO: refactor function w/ wait_for_page_to_load() and/or wait_for_element()

    # def switch_tab(self):
    #     dc_tab_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')))
    #
    #     db_tab_selector = self.driver.find_element(By.CSS_SELECTOR, '#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)').click()

    def set_date_filter(self):
        yesterday_date_selector = self.driver.find_element(By.CSS_SELECTOR, '#date > option:nth-child(2)').click()

    def set_translated_filter(self):
        translated_filter_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)')))

        # Opening translated pop-up modal
        translated_filter_selector = self.driver.find_element(By.CSS_SELECTOR, 'th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)').click()

        # Wait for pop-up modal element
        # div.ui-dialog:nth-child(15)

        # Adjust translated to `No`
        # li.ui-draggable:nth-child(1) > a:nth-child(2) > span:nth-child(1)

    # def switch_tab_and_apply_filters(self, driver):
    #     self.switch_tab(driver)
    #     self.set_date_filter()
    #     self.set_translated_filter(driver)