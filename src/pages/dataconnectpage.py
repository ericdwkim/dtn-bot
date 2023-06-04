from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

        # Find and kill overlay
        overlay_element = self.driver.find_element(By.XPATH, '//*[@id="cz_transBG"]')
        # JS to kill overlay
        # self.driver.execute_script("arguments[0].style.display = 'none';", overlay_elm)
        # Modify the z-index property using execute_script
        self.driver.execute_script("arguments[0].style.zIndex = '0';", overlay_element)


        # Translated widget pop up box
        # self.wait_for_element('div.ui-dialog:nth-child(13)')
        # Wait for the span element to be clickable

        # no_plus_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[2]/div[2]/ul/li[1]/a/span')))

        no_plus_1 = self.driver.find_element('body')
        no_plus_2 = self.driver.find_element('div:nth-child(15)')
        no_plus_3 = self.driver.find_element('div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content')
        no_plus_4 = self.driver.find_element('div.available.right-column')
        no_plus_5 = self.driver.find_element('ul')
        no_plus_6 = self.driver.find_element('li:nth-child(1)')
        no_plus_6.click()

        # `No` plus icon
        # self.find_element_and_click('li.ui-draggable:nth-child(1) > a:nth-child(2) > span:nth-child(1)')

        # Execute the click event using JavaScript
        # anchor_element = self.driver.find_element(By.CSS_SELECTOR, 'li.ui-draggable:nth-child(1)')
        # self.driver.execute_script("arguments[0].click();", anchor_element)

    # def switch_tab_and_apply_filters(self, driver):
    #     self.switch_tab(driver)
    #     self.set_date_filter()
    #     self.set_translated_filter(driver)