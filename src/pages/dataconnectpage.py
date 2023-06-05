from .basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class DataConnectPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def switch_tab(self):
        self.wait_for_find_then_click('#header > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')

    def set_date_filter(self):
        self.find_element_and_click('#date > option:nth-child(2)')

    def set_translated_filter(self):
        action = ActionChains(self.driver)

        # Translated funnel header
        self.retry_wait_find_then_click("th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)")

        # self.wait_for_element(By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")

        # Execute JavaScript to set the property to 'No' value
        # script = """
        # var draggableBar = document.querySelector('.ui-state-default.ui-element.ui-draggable');
        # draggableBar.setAttribute('title', 'No');
        # """
        # self.driver.execute_script(script)


        # Check for widget visibility
        # self.check_element_visibility(By.CLASS_NAME, 'ui-dialog ui-widget ui-widget-content ui-corner-all ui-draggable')

        # Test clicking `Cancel` button on widget to see if any elm on widget can actually be interacted with
        # self.find_element_and_click("body > div:nth-child(13) > div.ui-multiselect.ui-helper-clearfix.ui-widget.ui-dialog-content.ui-widget-content > div.available.right-column > div > a")


        # Wait for list of draggable widget elements to be located
        lst_drag_elms = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'available connected-list')))
        draggable_no = lst_drag_elms[0]
        self.check_element_visibility(By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")
        print(f'------draggable_no: {draggable_no}')

        # no_drag_bar_test_wait = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")))
        # action.double_click(no_drag_bar_test).perform()



        # No draggable bar; double click to set
        # no_drag_bar_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")))
        # no_drag_bar= self.driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")

        #
        # action = ActionChains(self.driver)
        # action.double_click(WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[1][contains(., 'No')]")))).perform()
        #

        n = 3
        while n > 0:
            print('testing')
            n = n - 1
        # //li[@class='ui-state-default ui-element ui-draggable' and @title='No']
        # <li class="ui-state-default ui-element ui-draggable" title="No"><span class="ui-helper-hidden"></span>No<a href="#" class="action"><span class="ui-corner-all ui-icon ui-icon-plus"></span></a></li>


        # <p class="wrap button draggable" id="anonymous_element_1"><b class="icon" id="handler2"></b>Reports</p>

        # ActionChains(driver).double_click(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//p[@class='wrap button draggable' and @id='anonymous_element_1'][contains(., 'Reports')]")))).perform()

        # action.perform()
        print('no drag bar double clicked!')



        # Find and kill overlay
        # overlay_element = self.driver.find_element(By.XPATH, '//*[@id="cz_transBG"]')
        # JS to kill overlay
        # self.driver.execute_script("arguments[0].style.display = 'none';", overlay_elm)
        # Modify the z-index property using execute_script
        # self.driver.execute_script("arguments[0].style.zIndex = '0';", overlay_element)


        # Translated widget pop up box
        # self.wait_for_element('div.ui-dialog:nth-child(13)')
        # Wait for the span element to be clickable

        # no_plus_wait = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[2]/div[2]/ul/li[1]/a/span')))


        # `No` plus icon
        # self.find_element_and_click('li.ui-draggable:nth-child(1) > a:nth-child(2) > span:nth-child(1)')

        # Execute the click event using JavaScript
        # anchor_element = self.driver.find_element(By.CSS_SELECTOR, 'li.ui-draggable:nth-child(1)')
        # self.driver.execute_script("arguments[0].click();", anchor_element)

    # def switch_tab_and_apply_filters(self, driver):
    #     self.switch_tab(driver)
    #     self.set_date_filter()
    #     self.set_translated_filter(driver)