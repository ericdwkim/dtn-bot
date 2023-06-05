from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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

        # Test - if no drag bar is found, we can rule out shadow DOM theory
        no_drag_bar_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")))
        no_drag_bar= self.driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")
        # print(no_drag_bar) # Output: <undetected_chromedriver.webelement.WebElement (session="df60cc274c09168cc66110a295349da3", element="DED5601AAF35631FB1BE6B3616B4539A_element_232")>

        # Check if the element is displayed
        if no_drag_bar.is_displayed():
            print("Element is displayed")
        else:
            print("Element is not displayed")

        # Check if the element is enabled
        if no_drag_bar.is_enabled():
            print("Element is enabled")
        else:
            print("Element is disabled")

        # Test - both check return True; displayed & enabled


    # def switch_tab_and_apply_filters(self, driver):
    #     self.switch_tab(driver)
    #     self.set_date_filter()
    #     self.set_translated_filter(driver)