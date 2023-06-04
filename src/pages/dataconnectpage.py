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
        # Translated widget pop up box
        self.wait_for_element('div.ui-dialog:nth-child(13)')

        # Locate anchor element
        # anchor_elm = self.driver.find_element(By.XPATH,
        #                                  '/html/body/div[8]/div[2]/div[2]/ul/li[1]/a')
        # Wait for the span element to be clickable
        # wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-icon-plus')))
        # span_elm = self.driver.find_element(By.CLASS_NAME, 'ui-icon-plus')

        # Find the span element with the desired class
        # span_element = self.driver.find_element(By.XPATH, '//span[@class="ui-corner-all ui-icon ui-icon-plus"]')

        # Wait for anchor element to be
        # wait = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'action')))

        # Find the anchor element with the desired CSS selector
        anchor_element = self.driver.find_element(By.CSS_SELECTOR, 'li.ui-draggable:nth-child(1)')

        # Execute the click event using JavaScript
        self.driver.execute_script("arguments[0].click();", anchor_element)

        # Perform the hover action on the span element
        # actions = ActionChains(self.driver)
        # actions.move_to_element(span_element).perform()

        # anchor_element.click()

        # No plus icon
        # self.find_element_and_click('li.ui-draggable:nth-child(1) > a:nth-child(2) > span:nth-child(1)')


    # def switch_tab_and_apply_filters(self, driver):
    #     self.switch_tab(driver)
    #     self.set_date_filter()
    #     self.set_translated_filter(driver)