import time
from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        # source locators are the possible locator type, locator string combinations specific to the `No` draggable bar
        src_locators = {
            "CSS_SELECTOR_KEY": (By.CSS_SELECTOR, [
                "body > div:nth-child(15) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.available.right-column > ul > li:nth-child(1)"]),
            "XPATH_KEY": (By.XPATH, ["/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]",
                                 "/html/body/div[8]/div[2]/div[2]/ul/li[1]"]),
        }

        # target locators is the are the possible locator type, locator string combinations specific to the droppable element
        # NOTE: to add other locator types, just create new KEY w/ tup value

        target_locators = {
            # `selected connected-list ui-sortable` class
            'CSS_SELECTOR_KEY': (By.CSS_SELECTOR,
                               ["body > div:nth-child(13) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.selected > ul"])
        }


        for src_locator_key in ['CSS_SELECTOR_KEY', 'XPATH_KEY']:  # Loop over keys of source locators
            if self.find_element_drag_and_drop(src_locators, src_locator_key, target_locators, 'CSS_SELECTOR_KEY'):
                print(f'Drag and drop successful with locator {src_locator_key}')
                time.sleep(30)  # Wait for UI update
                break
            else:
                print(f'Drag and drop failed with locator {src_locator_key}')

        # TODO: Refactor current setup as drag & drop works!!!!
        """
        FYI: 
            Drag and drop failed with locator CSS_SELECTOR_KEY
            Drag and drop successful with locator XPATH_KEY
        might be worth just going w/ XPATH_KEY but redundancy code is still useful?
        """
        # TODO: consider changing ds since locator key literals are identical both source and target; will have to remove unneeded dict_key and replace with By.locator_type ?
        # locator_keys = ['CSS_SELECTOR_KEY', 'XPATH_KEY']
        # for locator_key in locator_keys:  # Loop over locator keys
        #     if self.find_element_drag_and_drop(src_locators, locator_key, target_locators, locator_key):
        #         print(f'Drag and drop successful with locator {locator_key}')
        #         time.sleep(30)  # Wait for UI update
        #         break
        #     else:
        #         print(f'Drag and drop failed with locator {locator_key}')
        # -----------------------------------------------------------------------

        # Confirm filter setting by clicking `Filter` button on widget
        if self.retry_wait_for_single_click_perform( "body > div:nth-child(13) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1) > span", locator_type=By.CSS_SELECTOR):
            print("Filter button clicked!")
        else:
            print("Filter button NOT clicked!")

        time.sleep(30)

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