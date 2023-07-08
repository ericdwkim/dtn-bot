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
    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def set_date_filter(self, date_locator='#date > option:nth-child(2)', third_flow=False):
        print(f'*********************date_locator1 ***********: {date_locator}')
        if third_flow:
            print(f'---------- testing -------------')
            date_locator = '#date > option:nth-child(1)'
        try:
            print(f'*********************date_locator2 ***********: {date_locator}')
            was_clicked, element_selector_clicked = self.find_element_and_click(date_locator)
            print(f'************ was_clicked , element_selector_clicked : {was_clicked}  {element_selector_clicked }')

            if was_clicked and element_selector_clicked:
                time.sleep(10)  # Wait for filter heads to load on DOM

                translated_filter_head_located = self.wait_for_presence_of_elements_located(
                    r'//*[@id="messageTable"]/thead/tr/th[7]/button', locator_type=By.XPATH)
                translated_filter_head_clickable = self.wait_for_element_clickable(
                    r'//*[@id="messageTable"]/thead/tr/th[7]/button', locator_type=By.XPATH)
                time.sleep(5)
                return True

            elif not was_clicked and not element_selector_clicked:
                print(f'Could not set date filter with retries. Reloading page....')
                reload_status = self.reload_page()
                # if successful reload, recursively call current function and continue with flow
                if reload_status:
                    print(f'Successfully reloaded page! Resetting date filter....')
                    time.sleep(30)
                    return self.set_date_filter(date_locator, third_flow)

                else:
                    print(f'Could not reload page. Something went wrong!')
                    return False

        except Exception as e:
            print(f'An error occurred trying to set date filter: {str(e)}')
            return False


    def reload_page(self, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.driver.refresh()
                return True
            except Exception as e:
                print(f"Error during refresh: {str(e)}. Attempt: {attempt + 1}")
                time.sleep(1)  # Wait for 1 second before the next attempt
        return False

    def click_filter_header(self, filter_header_locator, locator_type=By.XPATH):
        """
        Clicks filter header at `filter_header_locator`\n
        :return: bool
        """
        # If filter header found and clicked, return True
        if self.wait_for_find_then_click(filter_header_locator, locator_type):
            return True
        else:
            print(f'Could not click filter header: {filter_header_locator} using locator type: {locator_type}')
            return False

    def click_filter_button_at_idx(self, filter_btn_elem_idx, timeout=10):
        """
            Clicks `Filter` button at a specific filter_btn_elem_idx to confirm
        :param filter_btn_elem_idx: The idx of the filter button to be clicked
        :param timeout: The time to wait for the element to be clickable
        :return:
        """
        try:

            filter_button_xpath_locator = "//span[@class='ui-button-text' and text()='Filter']"
            filter_button_elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, filter_button_xpath_locator))
            )

            if filter_button_elements and filter_btn_elem_idx < len(filter_button_elements):
                # ensure desired filter button is clickable then click
                is_clickable = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(filter_button_elements[filter_btn_elem_idx]))
                if is_clickable:
                    self.driver.execute_script("$(arguments[0]).click();", filter_button_elements[filter_btn_elem_idx])
                    time.sleep(timeout)  # Wait for UI update
                    # print(f"Filter button at idx {filter_btn_elem_idx} was clicked!")
                else:
                    print(f"Could not click Filter button at idx {filter_btn_elem_idx}")
            else:
                print(f"Filter buttons were not found or idx {filter_btn_elem_idx} is out of range!")
            return True

        except Exception as e:
            print(f'An error occurred trying to drag and drop from source to target element: {e}')
            return False


    def reset_selected_group_filter(self):
        # list of webelements (4 total)
        remove_all_elements = self.driver.find_elements(By.XPATH, "//a[@class='remove-all' and text()='Remove all']")
        remove_all_element = remove_all_elements[1]  # desired `remove all` elem idx
        if remove_all_element:
            remove_all_element.click()  # remove `Notice` filter
            # print(f'Reset selected Group filter list')
            return True
        else:
            # print(f'Could not reset selected Group filter list')
            return False

    def click_checkbox(self):

        found_and_clicked = self.find_element_and_click("//*[@id='prMasterCheckbox2']", By.XPATH)
        if found_and_clicked:
            # print(f'Checkbox was found and clicked!')
            time.sleep(15)  # wait for UI to update
            return True
        else:
            print(f'Checkbox could not be found and clicked')
            return False

    def click_print_button(self):

        found_and_clicked = self.find_element_and_click("//*[@id='print_button']/span[2]", By.XPATH)
        if found_and_clicked:
            # print(f'Print button was found and clicked!')
            time.sleep(15)  # wait for UI to update
            return True
        else:
            print(f'Print button could not be found and clicked')
            return False

    def check_all_then_click_print(self):
        is_clicked = self.click_checkbox()
        if is_clicked:
            self.click_print_button()
            return True
        else:
            return False


    def set_filter(self, filter_btn_elem_idx, filter_header_locator,
                   target_elem_idx, src_locator, reset_selected=False):
        """
        Click filter head @ `filter_header_locator`\n
        Drag `src_locator` elem and drop to `target_elements[target_elem_idx]` elem\n
        Click `Filter` button @ `filter_button_elements[filter_btn_elem_idx]` elem
        :param reset_selected:
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

        # Group `Draft Notice` case requires resetting of selected list
        # to remove `Invoice` before selecting `Draft Notice`
        if filter_header_is_clicked and reset_selected is True:

            # Find `Remove all` and click to reset selected list on Filter widget
            self.reset_selected_group_filter()

        src_elem_dragged_and_dropped_to_target_elem = self.find_element_drag_and_drop(src_locator, target_elem_idx)
        if not src_elem_dragged_and_dropped_to_target_elem:
            print("Source element could not be dragged and dropped to target element")
            return True, False, False

        filter_button_is_clicked = self.click_filter_button_at_idx(filter_btn_elem_idx)
        if not filter_button_is_clicked:
            print("Filter button could not be clicked")
            return True, True, False

        if filter_button_is_clicked and reset_selected is True:
            # @dev: first checkbox click req'd
            checkbox_is_clicked = self.click_checkbox()
            checkbox_checked_and_print_button_clicked = self.check_all_then_click_print()
            if checkbox_is_clicked and checkbox_checked_and_print_button_clicked:
                print("Downloading Draft Notice PDF")
                time.sleep(30)  # wait for UI to update

        return True, True, True

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def set_translated_filter_to_no(self, third_flow):


        """
        set_filter wrapper specific to Translated filter to `No`
        :return: bool
        """

        # initialize req'd param
        date_locator = ''

        filter_header_is_clicked, src_elem_dragged_and_dropped_to_target_elem, \
            filter_button_is_clicked = self.set_filter(
            filter_btn_elem_idx=3,
            filter_header_locator=r'//*[@id="messageTable"]/thead/tr/th[7]/button',
            target_elem_idx=3,
            src_locator="//li[@title='No']"
        )
        if filter_header_is_clicked and src_elem_dragged_and_dropped_to_target_elem and filter_button_is_clicked:
            return True

        elif not filter_header_is_clicked and not src_elem_dragged_and_dropped_to_target_elem and not filter_button_is_clicked:
            print(f'Could not set Translated filter with retries. Please restart script.')
            # reload_status = self.reload_page()
            # time.sleep(15)
            #
            # if reload_status:
            #     print(f'Successfully reloaded page!')
            #     # Recall to set date to correct one
            #     reset_date_filter = self.set_date_filter(date_locator, third_flow)
            #     # Recursive call
            #     if reset_date_filter:
            #         return self.set_translated_filter_to_no(third_flow)
        else:
            print(f'filter_header_is_clicked: {filter_header_is_clicked}\nsrc_elem_dragged_and_dropped_to_target_elem: '
                  f'{src_elem_dragged_and_dropped_to_target_elem}'
                  f'\nfilter_button_is_clicked: {filter_button_is_clicked}\n')
            raise Exception("Failed to set Translated filter.")


    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def set_group_filter_to_invoice(self, third_flow=False):
        """
        set_filter wrapper specific to Group filter to `Invoice`
        :return: bool
        """
        # initialize req'd param
        date_locator = ''

        filter_header_is_clicked, src_elem_dragged_and_dropped_to_target_elem, \
            filter_button_is_clicked = self.set_filter(
            filter_btn_elem_idx=1,
            filter_header_locator=r'//*[@id="messageTable"]/thead/tr/th[5]/button/span[2]',
            target_elem_idx=1,
            src_locator="//li[@title='Invoice']",
        )
        if filter_header_is_clicked and src_elem_dragged_and_dropped_to_target_elem and filter_button_is_clicked:
            return True

        elif not filter_header_is_clicked and not src_elem_dragged_and_dropped_to_target_elem and not filter_button_is_clicked:
            print(f'Could not set group filter to invoice with retries. Please restart script.')
            # reload_status = self.reload_page()
            #
            # if reload_status:
            #     print(f'Successfully reloaded page!')
            #     # Recall to set date to correct one
            #     reset_date_filter = self.set_date_filter(date_locator, third_flow)
            #     # Recall to set translated filter
            #     reset_translated_filter = self.set_translated_filter_to_no(third_flow)
            #     # Recursive call
            #     if reset_date_filter and reset_translated_filter:
            #         return self.set_group_filter_to_invoice(third_flow)
        else:
            print(
                f'filter_header_is_clicked: {filter_header_is_clicked}\n'
                f'src_elem_dragged_and_dropped_to_target_elem: '
                f'{src_elem_dragged_and_dropped_to_target_elem}\nfilter_button_is_clicked: {filter_button_is_clicked}\n')
            raise Exception("Failed to set Group filter to Invoice")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def set_group_filter_to_draft_notice(self, third_flow=False):
        """
        set_filter wrapper specific to Group filter to Draft Notice
        :return: bool
        """

        # initialize req'd param
        date_locator = ''

        filter_header_is_clicked, src_elem_dragged_and_dropped_to_target_elem, \
            filter_button_is_clicked = self.set_filter(
            filter_btn_elem_idx=1,
            filter_header_locator=r'//*[@id="messageTable"]/thead/tr/th[5]/button/span[2]',
            target_elem_idx=1,
            src_locator="//li[@title='Draft Notice']",
            reset_selected=True
        )
        if filter_header_is_clicked and src_elem_dragged_and_dropped_to_target_elem and filter_button_is_clicked:
            return True

        elif not filter_header_is_clicked and not src_elem_dragged_and_dropped_to_target_elem and not filter_button_is_clicked:
            print(f'Could not set group filter to draft notice with retries. Please restart script.')
            # reload_status = self.reload_page()
            #
            # if reload_status:
            #     print(f'Successfully reloaded page!')
            #     # Recall to set date to correct one
            #     reset_date_filter = self.set_date_filter(date_locator, third_flow)
            #     # Recall to set translated filter
            #     reset_translated_filter = self.set_translated_filter_to_no(third_flow)
            #     # Recursive call
            #     if reset_date_filter and reset_translated_filter:
            #         return self.set_group_filter_to_draft_notice(third_flow)

        else:
            print(
                f'filter_header_is_clicked: {filter_header_is_clicked}\n'
                f'src_elem_dragged_and_dropped_to_target_elem: {src_elem_dragged_and_dropped_to_target_elem}'
                f'\nfilter_button_is_clicked: {filter_button_is_clicked}\n')
            raise Exception("Failed to set Group filter to Draft Notice")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def set_group_filter_to_credit_card(self, third_flow=True):
        """
        set_filter wrapper specific to Group filter to Credit Card
        :return: bool
        """
        # initialize req'd param
        date_locator = ''

        filter_header_is_clicked, src_elem_dragged_and_dropped_to_target_elem, \
            filter_button_is_clicked = self.set_filter(
            filter_btn_elem_idx=1,
            filter_header_locator=r'//*[@id="messageTable"]/thead/tr/th[5]/button/span[2]',
            target_elem_idx=1,
            src_locator="//li[@title='Credit Card']"
        )
        if filter_header_is_clicked and src_elem_dragged_and_dropped_to_target_elem and filter_button_is_clicked:
            return True

        elif not filter_header_is_clicked and not src_elem_dragged_and_dropped_to_target_elem and not filter_button_is_clicked:
            print(f'Could not set group filter to draft notice with retries. Please restart script.')
            # reload_status = self.reload_page()
            #
            # if reload_status:
            #     print(f'Successfully reloaded page!')
            #     # Recall to set date to correct one
            #     reset_date_filter = self.set_date_filter(date_locator, third_flow)
            #     # Recall to set translated filter
            #     reset_translated_filter = self.set_translated_filter_to_no(third_flow)
            #     # Recursive call
            #     if reset_date_filter and reset_translated_filter:
            #         return self.set_group_filter_to_credit_card(third_flow)

        else:
            print(
                f'filter_header_is_clicked: {filter_header_is_clicked}\n'
                f'src_elem_dragged_and_dropped_to_target_elem: {src_elem_dragged_and_dropped_to_target_elem}'
                f'\nfilter_button_is_clicked: {filter_button_is_clicked}\n')
            raise Exception("Failed to set Group filter to Credit Cards")


    def switch_tab_set_filters_and_download_invoices(self):
        if not self.switch_tab():
            return False


        if not self.set_date_filter():
            return False

        try:
            self.set_translated_filter_to_no(third_flow=False)
        except Exception as e:
            print(f"set_translated_filter_to_no failed with error: {str(e)}")
            return False

        try:
            self.set_group_filter_to_invoice(third_flow=False)
        except Exception as e:
            print(f'set_group_filter_to_invoice failed with error: {str(e)}')
            return False

        if not self.check_all_then_click_print():
            return False

        return True