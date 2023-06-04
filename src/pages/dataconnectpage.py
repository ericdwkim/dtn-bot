from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def switch_tab(self):
        # self.wait_for_element('#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
        #
        # self.find_element_and_click('#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
        #
        self.wait_for_find_then_click('#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')

    def set_date_filter(self):
        self.find_element_and_click('#date > option:nth-child(2)')

    def set_translated_filter(self):

        # Translated funnel header
        self.wait_for_find_then_click('th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)')


        # Switch to iframe
        # self.driver.switch_to.frame('LifeLine_iframe')
        self.driver.switch_to.frame('cz-clean-room')
        # self.driver.switch_to.frame('LifeLine_iframe')
        # self.driver.switch_to.frame('LifeLine_iframe')
        # driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
        self.wait_for_find_then_click('li.ui-draggable:nth-child(1) > a:nth-child(2) > span:nth-child(1)')

        # self.find_element_and_click('ui-corner-all ui-icon ui-icon-plus', locator_type=By.CLASS_NAME)

    # def switch_tab_and_apply_filters(self, driver):
    #     self.switch_tab(driver)
    #     self.set_date_filter()
    #     self.set_translated_filter(driver)