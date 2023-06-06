from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def switch_tab(self):
        self.wait_for_find_then_click('#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')

    def set_date_filter(self):
        self.find_element_and_click('#date > option:nth-child(2)')

    def set_translated_filter(self):
        action = ActionChains(self.driver)

        # Translated funnel header
        self.retry_wait_find_then_click("th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)")

        # Set Translated to `No`
        self.retry_wait_find_then_double_click("/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")
        print("No drag bar double clicked!")

        # Click `filter` on widget to refresh current page to validate if Translated is all Nos
        self.retry_wait_find_then_double_click("/html/body/div[10]/div[3]/div/button[1]/span")


        filter_btn_wait = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[10]/div[3]/div/button[1]/span")))
        filter_btn= self.driver.find_element(By.XPATH, "/html/body/div[10]/div[3]/div/button[1]/span")

        Check if the element is displayed
        if filter_btn.is_displayed():
            print("Element is displayed")
        else:
            print("Element is not displayed")

        # Check if the element is enabled
        if filter_btn.is_enabled():
            print("Element is enabled")
        else:
            print("Element is disabled")


        # self.wait_for_element_clickable(By.XPATH, "/html/body/div[10]/div[3]/div/button[1]")
        # self.find_element_and_click(By.XPATH, "/html/body/div[10]/div[3]/div/button[1]")
        #



    # def switch_tab_and_apply_filters(self, driver):
    #     self.switch_tab(driver)
    #     self.set_date_filter()
    #     self.set_translated_filter(driver)