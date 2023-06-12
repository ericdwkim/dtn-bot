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
        # If Translated filter found and clicked, return True
        if self.wait_for_find_then_click(r'//*[@id="messageTable"]/thead/tr/th[7]/button', locator_type=By.XPATH):
            print("Translated funnel header clicked!")
            return True
        else:
            print("1111111111")
            return False

    def drag_and_drop_for_translated(self):
        """
        Wrapper for clicking, drag/dropping, and confirming filter
            Clicks `Translated` filter funnel\n
            Drag and drops `No` draggable bar\n
            Clicks `Filter` button to confirm
        :return: bool
        """
        if self.click_translated_filter():
            self.find_element_drag_and_drop(src_locator="//li[@title='No']", target_locator="//ul[@class='selected connected-list ui-sortable']")
            print("Element was dragged and dropped!")
            return True
        else:
            print("222222222")
            return False
    def click_filter_to_confirm(self):

        if self.drag_and_drop_for_translated():

            filter_button_xpath_locator = "//span[@class='ui-button-text' and text()='Filter']" # fetch 3rd idx
            elements = WebDriverWait(self.driver, timeout=15).until(
                EC.presence_of_all_elements_located((By.XPATH, filter_button_xpath_locator))
            )

            if elements:
                print(f'elements: {elements}\nlength elements: {len(elements)}')
                # ensure desired filter button is clickable the try to click
                is_clickable = WebDriverWait(self.driver, timeout=60).until(
                    EC.element_to_be_clickable(elements[3]))
                if is_clickable:
                    # elements[3].click()
                    self.driver.execute_script("arguments[0].click();", elements[3])
                else:
                    print("Could not click element[3]")
                print("Filter buttons were found!")
            else:
                print("Filter buttons were not found!")

                """
                element.click() resulted in:
                   Error occurred when trying to find and click element: Message: element click intercepted: Element <button type="button" class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" aria-disabled="false">...</button> is not clickable at point (1063, 401). Other element would receive the click: <li class="ui-state-default ui-element" title="Yes">...</li>
                """

        else:
            print("3333333333")
            return False

    def set_translated_filter(self):
        # 1) click Translated filter head
        translated_is_clicked = self.click_translated_filter()
        # 2) drag and drop
        no_is_drag_dropped = self.drag_and_drop_for_translated()
        # 3) confirm
        translated_filter_is_confirmed = self.click_filter_to_confirm()

        return translated_is_clicked and no_is_drag_dropped and translated_filter_is_confirmed

    def switch_tab_and_apply_filters(self):
        self.switch_tab()
        self.set_date_filter()
        self.set_translated_filter() # Test - Refactored function without mappings
        # self.set_group_filter_to_invoice()