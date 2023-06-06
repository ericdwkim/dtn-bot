import time
from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def switch_tab(self):
        print('Switching to DataConnect tab')
        self.wait_for_find_then_click('#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')

    def set_date_filter(self):
        print('Applying date filter to yesterday')
        self.find_element_and_click('#date > option:nth-child(2)')

    def set_translated_filter(self):
        print('Applying Translated filter to `No`')

        """
        #TODO
        :return: None
        """

        """
        1) Click `Translated` filter funnel column header
        """
        if self.retry_wait_find_then_click("th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)"):
            print("Translated funnel header clicked!")
        else:
            print("Translated funnel NOT clicked!")

        """
        2) Drag and drop `No` bar to set 
        """
        # source locators are the possible locator type, locator string combinations specific to the `No` draggable bar
        src_locators = {
            "XPATH_KEY": (By.XPATH, ["/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]",
                                 "/html/body/div[8]/div[2]/div[2]/ul/li[1]"]),
            "CSS_SELECTOR_KEY": (By.CSS_SELECTOR, [
                "body > div:nth-child(15) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.available.right-column > ul > li:nth-child(1)"])
        }

        # target locators is the are the possible locator type, locator string combinations specific to the droppable element
        # NOTE: to add other locator types, just create new KEY w/ tup value
        target_locators = {
            # `selected connected-list ui-sortable` class
            'CSS_SELECTOR_KEY': (By.CSS_SELECTOR,
                               ["body > div:nth-child(13) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.selected > ul"])
        }

        # Loop over keys of source locators
        for src_locator_key in ['XPATH_KEY', 'CSS_SELECTOR_KEY']:
            if self.find_element_drag_and_drop(src_locators, src_locator_key, target_locators, 'CSS_SELECTOR_KEY'):
                print(f'Drag and drop successful with locator {src_locator_key}')
                time.sleep(30)  # Wait for UI update
                break
            else:
                print(f'Drag and drop failed with locator {src_locator_key}')


        """
        3) Click `Filter` button to confirm setting
        """
        if self.retry_wait_for_single_click_perform( "body > div:nth-child(13) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1) > span", locator_type=By.CSS_SELECTOR):
            print("Filter button clicked!")
        else:
            print("Filter button NOT clicked!")

        time.sleep(30)

    def set_group_filter(self):
        print('Applying group filter to Invoice')

        """
         logic to set filter to `Invoice` only
        """

        print('Applying group filter to Draft Notice')

        """
         logic to set filter to `Draft Notice` only
        """

    def switch_tab_and_apply_filters(self):
        self.switch_tab()
        self.set_date_filter()
        self.set_translated_filter()
        self.set_group_filter()