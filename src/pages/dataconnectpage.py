import time
from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def switch_tab(self):
        """
        Switches from default `Markets` to `DataConnect` tab
        :return: bool
        """
        try:
            is_element_clicked = self.wait_for_find_then_click('#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
            if is_element_clicked:
                print('Switched to DataConnect tab')
                return True
            else:
                # print('Failed to switch to DataConnect tab.')
                return False
        except Exception as e:
            print(f'An error occurred trying to switch to DataConnect tab: {str(e)}')
            return False

    def set_date_filter(self):
        """
        Sets `Date` filter to yesterday
        :return: bool
        """
        try:
            was_clicked, element_selector_clicked = self.find_element_and_click('#date > option:nth-child(2)')
            if was_clicked:
                # print('Date filter set to yesterday')
                return True
            else:
                # print('Date filter could not be set to yesterday')
                return False
        except Exception as e:
            print(f'An error occurred trying to set date to yesterday: {str(e)}')
            return False

    def click_filter_to_confirm(self):



        filter_button_xpath_locator = "//span[@class='ui-button-text' and text()='Filter']" # fetch 3rd idx
        elements = WebDriverWait(self.driver, timeout=15).until(
            EC.presence_of_all_elements_located((By.XPATH, filter_button_xpath_locator))
        )
        # loop through all filter buttons and click each one
        for element in elements:
            element.click()

        # print(f'elements: {elements}')
        # print(f' length elements: {len(elements)}')
        # element = elements[3]
        # print(f'element: {element}')

        # is_clickable = self.wait_for_element_clickable(By.XPATH, filter_button_xpath_locator)
        # if is_clickable:
        #     # element.click()
        #     self.action.click(element).perform()
        # else:
        #     print("Unable to interact")

        # try:
        #     filter_btns = self.wait_for_presence_of_elements_located_then_click(By.XPATH, filter_button_xpath_locator)
        #     if filter_btns: # if filter button WebElements returned
        #         filter_btn = filter_btns[3] # access 3rd idx filter button
        #         filter_btn.click() # Confirm filter
        #         return True
        #     else:
        #         print(f'Could not locate Filter buttons')
        #         return False
        # except Exception as e:
        #     print(f'An error occurred trying to locate presence of list WebElements: {e}')
        #     return False

    def set_translated_filter(self):
        """
        Wrapper for clicking, drag/dropping, and confirming filter
            Clicks `Translated` filter funnel\n
            Drag and drops `No` draggable bar\n
            Clicks `Filter` button to confirm
        :return: bool
        """

        try:
            # If Translated filter found and clicked, return True
            if self.retry_wait_find_then_click(r'//*[@id="messageTable"]/thead/tr/th[7]/button', locator_type=By.XPATH):
                # print("Translated funnel header clicked!")

                dragged_and_dropped_no_bar = self.find_element_drag_and_drop(src_locator="//li[@title='No']",
                                                                             target_locator="//ul[@class='selected connected-list ui-sortable']")

                """
                # filter button full element copied
                <span class="ui-button-text">Filter</span>
                
                # xpath syntax to directly access filter button using latest working syntax
                //span[@class='ui-button-text']
               
                """
                if dragged_and_dropped_no_bar:
                    self.click_filter_to_confirm()
                    return True
                else:
                    print("Could not drag and no drop bar")
                    return False
            else:
                print("Could not wait, find, and click Translated filter.")
                return False

        except Exception as e:
            print(f'An error occurred trying to apply Translated filter: {str(e)}')
            return False

    # TODO: if checks for each function call to ensure each fn is called successfully before running the next function --> this requires all nested function calls to also return bools.
    def switch_tab_and_apply_filters(self):
        self.switch_tab()
        self.set_date_filter()
        self.set_translated_filter() # Test - Refactored function without mappings
        # self.set_group_filter_to_invoice()