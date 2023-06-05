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

        # Translated funnel header
        # self.wait_for_find_then_click('th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)')
        
        self.retry_wait_find_then_click(self.driver, "th.sorting:nth-child(7) > button:nth-child(1) > span:nth-child(2)", max_retries=5, retry_delay=2)

        # No draggable bar; double click to set
        no_drag_bar_wait = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[2]")))
        no_drag_bar= self.driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[2]")


        action = ActionChains(self.driver)
        action.double_click(no_drag_bar)
        action.double_click(WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div[2]/div[2]/ul/li[2]")))).perform()
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