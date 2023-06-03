from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def wait_for_page_to_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element(self, locator, locator_type=By.CSS_SELECTOR, timeout=10):
        element_wait = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((locator_type, locator))
        )
        return element_wait

    def find_element_and_click(self, locator ,locator_type=By.CSS_SELECTOR):
        element_selector = self.driver.find_element(locator_type, locator)
        element_selector.click()
        return element_selector

    def find_element_and_click_and_send_keys(self, locator, keys_to_send):
        element_selector_clicked = self.driver.find_element_and_click(locator)
        element_selector_clicked.send_keys(keys_to_send)

