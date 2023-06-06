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
        Setting Translated to `No` with drag & drop
        """
        # source locators are the possible locator type, locator string
        # specific to the `No` draggable bar
        
        src_locators = {
            "CSS_SELECTOR_KEY": (By.CSS_SELECTOR, [
                "body > div:nth-child(15) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.available.right-column > ul > li:nth-child(1)"]),
            "XPATH__KEY": (By.XPATH, ["/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]",
                                 "/html/body/div[8]/div[2]/div[2]/ul/li[1]"]),
        }

        # `selected connected-list ui-sortable` class as target element to drop
        # target locators is the one locator type, locator string specific to drop area for source element
        # to add other locator types, just create new KEY w/ tup value

        target_locators = {

            'CSS_SELECTOR_KEY': (By.CSS_SELECTOR,
                               ["body > div:nth-child(13) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.selected > ul"])
        }
        for locator_key in src_locators:
            try:
                self.find_element_drag_and_drop(locator_dict=src_locators, locator_key_src= src_locator_key, )

        for locator_key in locators:
            try:
                self.find_element_drag_and_drop(no_bar_locators, locator_key, target_locator_key)
                time.sleep(30)  # Wait for UI update
                # If the drag and drop was successful, you can break out of the loop.
                break
            except Exception as e:
                print(f"Drag and drop failed with locator {locator_key}. Error: {e}")
                # You may continue to next locator

        """
        Setting Translated to `No` with doubleclick
        """
        # locators as mapping
        # locators = {
        #     By.CSS_SELECTOR: "body > div:nth-child(15) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.available.right-column > ul > li:nth-child(1)",
        #     By.XPATH: ["/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]",
        #                "/html/body/div[8]/div[2]/div[2]/ul/li[1]"],
        # }

        # for locator_type, locator_values in locators.items():
        #     for locator in locator_values:
        #         if self.retry_wait_find_then_double_click(locator, locator_type):
        #             print(f' No drag bar double clicked using locator: {locator}')
        #             break
        #     else:
        #         continue
        #     break
        # else:
        #     print("No drag bar NOT double clicked")
        #
        # time.sleep(60)  # Required to update UI
        #
        #
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