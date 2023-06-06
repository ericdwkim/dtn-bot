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

        # Translated funnel header
        if self.retry_wait_find_then_click("th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)"):
            print("Translated funnel header clicked!")
        else:
            print("Translated funnel NOT clicked!")

        """
        locators: locator types for `No` draggable bar in the following order CSS_SELECTOR, cust_XPATH, XPATH. 
        Setting Translated to `No` with drag & drop
        """
        # Locator types for `No` draggable bar in the following order CSS_SELECTOR, cust_XPATH, XPATH.
        locators = [
            "body > div:nth-child(15) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.available.right-column > ul > li:nth-child(1)",
            "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]",
            "/html/body/div[8]/div[2]/div[2]/ul/li[1]"
        ]
        # `selected connected-list ui-sortable` class
        target_locator = "body > div:nth-child(13) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.selected > ul"

        for locator in locators:
            try:
                self.find_element_drag_and_drop(locator_src=locator, locator_target=target_locator)
                time.sleep(30) # Wait for UI update
                # If the drag and drop was successful, you can break out of the loop.
                break
            except Exception as e:
                print(f"Drag and drop failed with locator {locator}. Error: {e}")
                # You may continue to next locator

        #
        # """
        # Setting Translated to `No` with doubleclick
        # """
        # for locator in locators:
        #     if self.retry_wait_find_then_double_click(locator):
        #         print(f' No drag bar double clicked using locator: {locator}')
        #         break
        # else:
        #     print("No drag bar NOT double clicked")
        #
        # time.sleep(60)  # Required to update UI


        # Confirm filter setting by clicking `Filter` button on widget
        # if self.retry_wait_for_single_click_perform( "body > div:nth-child(13) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1) > span", locator_type=By.CSS_SELECTOR):
        #     print("Filter button clicked!")
        # else:
        #     print("Filter button NOT clicked!")
        #
        # time.sleep(30)

        # filter_btn_wait = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[10]/div[3]/div/button[1]/span")))
        # filter_btn= self.driver.find_element(By.XPATH, "/html/body/div[10]/div[3]/div/button[1]/span")
        #
        # # Check if the element is displayed
        # if filter_btn.is_displayed():
        #     print("Element is displayed")
        # else:
        #     print("Element is not displayed")
        #
        # # Check if the element is enabled
        # if filter_btn.is_enabled():
        #     print("Element is enabled")
        # else:
        #     print("Element is disabled")


    # def switch_tab_and_apply_filters(self, driver):
    #     self.switch_tab(driver)
    #     self.set_date_filter()
    #     self.set_translated_filter(driver)