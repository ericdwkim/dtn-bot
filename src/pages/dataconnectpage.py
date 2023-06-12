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

    def click_translated_filter(self):
        """
            Clicks `Translated` filter funnel\n
        :return:
        """
        # If Translated filter found and clicked, return True
        if self.wait_for_find_then_click(r'//*[@id="messageTable"]/thead/tr/th[7]/button', locator_type=By.XPATH):
            print("Translated funnel header clicked!")
            return True
        else:
            print("Could not wait, find, and then click Translated filter btn")
            return False

    def drag_and_drop_for_translated(self, src_locator, target_elem_idx):
        """
            Drag and drops `No` draggable bar\n
        :return: bool
        """
        if self.click_translated_filter:
            self.find_element_drag_and_drop(src_locator, target_elem_idx)
            print("Element was dragged and dropped!")
            return True
        else:
            print("Could not click translated filter")
            return False

    def click_filter_at_index(self, idx, wait_time=30):
        """
            Clicks `Filter` button at a specific idx to confirm
        :param idx: The idx of the filter button to be clicked
        :param wait_time: The time to wait for the element to be clickable
        :return:
        """

        if self.drag_and_drop_for_translated:

            filter_button_xpath_locator = "//span[@class='ui-button-text' and text()='Filter']"
            elements = WebDriverWait(self.driver, timeout=30).until(
                EC.presence_of_all_elements_located((By.XPATH, filter_button_xpath_locator))
            )

            if elements and idx < len(elements):
                # ensure desired filter button is clickable then click
                is_clickable = WebDriverWait(self.driver, timeout=60).until(
                    EC.element_to_be_clickable(elements[idx]))
                if is_clickable:
                    self.driver.execute_script("$(arguments[0]).click();", elements[idx])
                    time.sleep(wait_time)  # Wait for UI update
                    print(f"Filter button at idx {idx} was clicked!")
                else:
                    print(f"Could not click Filter button at idx {idx}")
            else:
                print(f"Filter buttons were not found or idx {idx} is out of range!")

        else:
            print("Could not drag and drop from source to target elm")
            return False

# TODO: make this reusable
    def set_translated_filter(self):
        # 1) click Translated filter head
        translated_is_clicked = self.click_translated_filter()
        # 2) drag and drop
        no_is_drag_dropped = self.drag_and_drop_for_translated()
        """
        TEST - REFACTORING OF FUNCTIONS
        src_locator = "//li[@title='No']"
        target_locator="//ul[@class='selected connected-list ui-sortable']"
        target_elem_idx = 3
        """
        # 3) confirm
        translated_filter_is_confirmed = self.click_filter_at_index(3)

        return translated_is_clicked and no_is_drag_dropped and translated_filter_is_confirmed


    def set_filter(self, filter_header_locator, src_locator, target_locator):

    # def click_group_filter(self):
    #     # If Group filter found and clicked, return True
    #     if self.wait_for_find_then_click(r'//*[@id="messageTable"]/thead/tr/th[5]/button/span[2]', locator_type=By.XPATH):
    #         print("Group filter clicked!")
    #         return True
    #     else:
    #         print("Could not wait, find, and then click Group filter btn")
    #         return False
    #
    # def drag_and_drop_for_group(self):
    #     """
    #     Wrapper for clicking, drag/dropping, and confirming filter
    #         Clicks `Group` filter funnel\n
    #         Drag and drops `No` draggable bar\n
    #         Clicks `Filter` button to confirm
    #     :return: bool
    #     """
    #     if self.click_translated_filter:
    #         self.find_element_drag_and_drop(src_locator="//li[@title='No']", target_locator="//ul[@class='selected connected-list ui-sortable']")
    #         print("Element was dragged and dropped!")
    #         return True
    #     else:
    #         print("Could not click translated filter")
    #         return False


    def switch_tab_and_apply_filters(self):
        self.switch_tab()
        self.set_date_filter()
        self.set_translated_filter()
        # self.set_group_filter_to_invoice()