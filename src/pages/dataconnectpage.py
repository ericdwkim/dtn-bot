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

        filter_button_css_locator = "body > div:nth-child(13) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1) > span"

        try:
            if self.retry_wait_for_single_click_perform(filter_button_css_locator,                locator_type=By.CSS_SELECTOR):
                # print("Filter button clicked!")
                time.sleep(10) # update UI
                return True
            else:
                print("Could not click the filter button")
                return False
        except Exception as e:
            print(f'An error occurred trying to click filter button: {str(e)}')
            return False


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
                # ul draggable element copied
                <ul class="available connected-list" style="height: 172px;"><li class="ui-state-default ui-element ui-draggable" title="No"><span class="ui-helper-hidden"></span>No<a href="#" class="action"><span class="ui-corner-all ui-icon ui-icon-plus"></span></a></li><li class="ui-state-default ui-element ui-draggable" title="Yes"><span class="ui-helper-hidden"></span>Yes<a href="#" class="action"><span class="ui-corner-all ui-icon ui-icon-plus"></span></a></li></ul>
                
                # draggable element copied
                <li class="ui-state-default ui-element ui-draggable" title="No"><span class="ui-helper-hidden"></span>No<a href="#" class="action"><span class="ui-corner-all ui-icon ui-icon-plus"></span></a></li>
                
                # xpath syntax for drilling down to draggable No element
                //ul[@class='available connected-list']//li[@class='ui-state-default ui-element ui-draggable']//span[@class='ui-helper-hidden']//[a[@class='action']//span[@class='ui-corner-all ui-icon ui-icon-plus'][contains(., 'No')]
                
                or
                
                # xpath syntax accessing draggable No element directly 
                //li[@class='ui-state-default ui-element ui-draggable']
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