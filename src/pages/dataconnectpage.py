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
            print(f'An error occurred: {str(e)}')
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
            print(f'An error occurred: {str(e)}')
            return False

    def set_translated_filter(self):
        """
        Clicks `Translated` filter funnel\n
        Drag and drops `No` draggable bar\n
        Click `Filter` button to confirm
        :return: bool
        """

        try:
            # If filter found and clicked, return True
            if self.retry_wait_find_then_click("th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)"):
                # print("Translated funnel header clicked!")

                # source locators are the possible (locator type, locator string) combinations specific to the `No` draggable bar
                src_locators = {
                    "XPATH_KEY": (By.XPATH, ["/html/body/div[8]/div[2]/div[2]/ul/li[1]",
                                             "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]"]),
                    "CSS_SELECTOR_KEY": (By.CSS_SELECTOR, [
                        "body > div:nth-child(15) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.available.right-column > ul > li:nth-child(1)"])
                }

                # target locators is the are the possible locator type, locator string combinations specific to the droppable element
                # NOTE: to add other locator types, just create new KEY w/ tup value
                target_locators = {
                    # `selected connected-list ui-sortable` class
                    'CSS_SELECTOR_KEY': (By.CSS_SELECTOR,
                                         [
                                             "body > div:nth-child(13) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.selected > ul"])
                }

                # Loop over keys of source locators; drag & drop for filtering
                for src_locator_key in ['XPATH_KEY', 'CSS_SELECTOR_KEY']:
                    try:
                        if self.find_element_drag_and_drop(src_locators, src_locator_key, target_locators, 'CSS_SELECTOR_KEY'):
                            # print(f'Drag and drop successful with locator {src_locator_key}')
                            time.sleep(30)  # Wait for UI update

                            # Click `Filter` to confirm
                            try:
                                if self.retry_wait_for_single_click_perform(
                                        "body > div:nth-child(13) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1) > span",
                                        locator_type=By.CSS_SELECTOR):
                                    print("Filter button clicked!")
                                    return True
                                    # time.sleep(30)  # UI update
                                else:
                                    print("Could not click Filter button")
                                    return False
                            except Exception as e:
                                print(f'An error occurred trying to click Filter button: {str(e)}')
                                return False

                            return True
                        else:
                            # print(f'Drag and drop failed with locator {src_locator_key}')
                            return False
                    except Exception as e:
                        print(f'An error occurred trying to find_element_drag_and_drop : {str(e)}')
                        return False

                print("Successfully applied Translated filter ")
                return True

            else:
                print("Could not apply Translated filter.")
                return False

        except Exception as e:
            print(f'An error occurred when trying to apply Translated filter: {str(e)}')
            return False

    def set_group_filter_to_invoice(self):
        print('Applying group filter to Invoice')

        """
        1) Click `Group` filter funnel column header
        """
        if self.retry_wait_find_then_click("#messageTable > thead > tr > th:nth-child(5) > button > span.ui-button-text"):
            print("Group funnel header clicked!")
        else:
            print("Group funnel NOT clicked!")

        src_locators = {
            "XPATH_KEY": (By.XPATH, ["/html/body/div[6]/div[2]/div[2]/ul/li[3][contains(., 'Invoice')]",
                                     "/html/body/div[6]/div[2]/div[2]/ul/li[3]"]),
            "CSS_SELECTOR_KEY": (By.CSS_SELECTOR, ["body > div:nth-child(13) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.available.right-column > ul > li.ui-state-default.ui-element.ui-draggable"])
        }

        target_locators = {
            "CSS_SELECTOR_KEY": (By.CSS_SELECTOR, ["body > div:nth-child(13) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.selected > ul"])

        }

        """
        2) Drag and drop `Invoice` bar to set 
        """
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


    # def set_group_filter_to_draft_notice(self):
    #     print('Applying group filter to Draft Notice')
    #
    #     """
    #     1) Click `Group` filter funnel column header
    #     """
    #     if self.retry_wait_find_then_click(locator_string):
    #         print("Group funnel header clicked!")
    #     else:
    #         print("Group funnel NOT clicked!")


    # TODO: if checks for each function call to ensure each fn is called successfully before running the next function --> this requires all nested function calls to also return bools.
    def switch_tab_and_apply_filters(self):
        self.switch_tab()
        self.set_date_filter()
        self.set_translated_filter()
        # self.set_group_filter_to_invoice()