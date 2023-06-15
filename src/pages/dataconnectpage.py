import time
from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, stop_after_attempt, wait_fixed

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


    def click_filter_header(self, filter_header_locator, locator_type=By.XPATH):
        """
            Clicks filter header at `filter_header_locator`\n
        :return: bool
        """
        # If filter header found and clicked, return True
        if self.wait_for_find_then_click(filter_header_locator, locator_type):
            print(f'Filter header: {filter_header_locator} was clicked!')
            return True
        else:
            print(f'Could not click filter header: {filter_header_locator} using locator type: {locator_type}')
            return False

    def click_filter_button_at_idx(self, filter_btn_elem_idx, wait_time=30):
        """
            Clicks `Filter` button at a specific filter_btn_elem_idx to confirm
        :param filter_btn_elem_idx: The idx of the filter button to be clicked
        :param wait_time: The time to wait for the element to be clickable
        :return:
        """
        try:

            filter_button_xpath_locator = "//span[@class='ui-button-text' and text()='Filter']"
            filter_button_elements = WebDriverWait(self.driver, timeout=30).until(
                EC.presence_of_all_elements_located((By.XPATH, filter_button_xpath_locator))
            )

            if filter_button_elements and filter_btn_elem_idx < len(filter_button_elements):
                # ensure desired filter button is clickable then click
                is_clickable = WebDriverWait(self.driver, timeout=60).until(
                    EC.element_to_be_clickable(filter_button_elements[filter_btn_elem_idx]))
                if is_clickable:
                    self.driver.execute_script("$(arguments[0]).click();", filter_button_elements[filter_btn_elem_idx])
                    time.sleep(wait_time)  # Wait for UI update
                    print(f"Filter button at idx {filter_btn_elem_idx} was clicked!")
                else:
                    print(f"Could not click Filter button at idx {filter_btn_elem_idx}")
            else:
                print(f"Filter buttons were not found or idx {filter_btn_elem_idx} is out of range!")
            return True

        except Exception as e:
            print(f'An error occurred trying to drag and drop from source to target element: {e}')
            return False

    def set_filter(self, filter_btn_elem_idx, filter_header_locator,  target_elem_idx, src_elem_idx=None, src_locator=None):
        """
        Click filter head @ `filter_header_locator`\n
        Drag `src_locator` elem and drop to `target_elements[target_elem_idx]` elem\n
        Click `Filter` button @ `filter_button_elements[filter_btn_elem_idx]` elem
        :param filter_header_locator:
        :param src_locator:
        :param target_elem_idx:
        :param filter_btn_elem_idx:
        :return: Tuple[bool, bool, bool]
        """
        filter_header_is_clicked = self.click_filter_header(filter_header_locator)
        if not filter_header_is_clicked:
            print("Filter header could not be clicked")
            return False, False, False

        # Translated `No` case
        if src_elem_idx is None:
            src_elem_dragged_and_dropped_to_target_elem = self.find_element_drag_and_drop(src_elem_idx, src_locator, target_elem_idx)
            if not src_elem_dragged_and_dropped_to_target_elem:
                print("Source element could not be dragged and dropped to target element")
                return True, False, False

        # Group `Invoice` case
        elif src_locator is None:
            src_elem_dragged_and_dropped_to_target_elem = self.find_element_drag_and_drop(src_elem_idx, src_locator, target_elem_idx)
            if not src_elem_dragged_and_dropped_to_target_elem:
                print("Source element could not be dragged and dropped to target element")
                return True, False, False


        filter_button_is_clicked = self.click_filter_button_at_idx(filter_btn_elem_idx)
        if not filter_button_is_clicked:
            print("Filter button could not be clicked")
            return True, True, False

        return True, True, True

    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def set_translated_filter_to_no(self):
        """
        set_filter wrapper specific to Translated filter to `No`
        :return: bool
        """

        filter_header_is_clicked, src_elem_dragged_and_dropped_to_target_elem, filter_button_is_clicked = self.set_filter(
            filter_btn_elem_idx=3,
            filter_header_locator=r'//*[@id="messageTable"]/thead/tr/th[7]/button',
            target_elem_idx=3,
            src_elem_idx=None,
            src_locator="//li[@title='No']"
        )
        if filter_header_is_clicked and src_elem_dragged_and_dropped_to_target_elem and filter_button_is_clicked:
            return True
        else:
            print(f'filter_header_is_clicked: {filter_header_is_clicked}\nsrc_elem_dragged_and_dropped_to_target_elem: {src_elem_dragged_and_dropped_to_target_elem}\nfilter_button_is_clicked: {filter_button_is_clicked}\n')
            return False

    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def set_group_filter_to_invoice(self):
        """
        set_filter wrapper specific to Group filter to `Invoice`
        :return: bool
        """

        filter_header_is_clicked, src_elem_dragged_and_dropped_to_target_elem, filter_button_is_clicked = self.set_filter(
            filter_btn_elem_idx=2,
            filter_header_locator=r'//*[@id="messageTable"]/thead/tr/th[5]/button/span[2]',
            target_elem_idx=1,
            src_elem_idx=None,
            src_locator="//li[@title='Invoice']",
        )
        if filter_header_is_clicked and src_elem_dragged_and_dropped_to_target_elem and filter_button_is_clicked:
            return True
        else:
            print(
                f'filter_header_is_clicked: {filter_header_is_clicked}\nsrc_elem_dragged_and_dropped_to_target_elem: {src_elem_dragged_and_dropped_to_target_elem}\nfilter_button_is_clicked: {filter_button_is_clicked}\n')

    def switch_tab_and_apply_filters(self):
        self.switch_tab()
        # self.set_date_filter()
        # self.set_translated_filter_to_no()
        self.set_group_filter_to_invoice()