from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selenium.webdriver.common.action_chains import ActionChains

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.action = ActionChains(self.driver)

    def find_element_and_click(self, locator ,locator_type=By.CSS_SELECTOR):
        element_selector = self.driver.find_element(locator_type, locator)
        element_selector.click()
        return element_selector

    def find_element_and_click_and_send_keys(self, locator, keys_to_send):
        element_selector_clicked = self.find_element_and_click(locator)
        element_selector_clicked.send_keys(keys_to_send)


    def find_element_and_double_click(self, locator, locator_type=By.XPATH):
        element = self.driver.find_element(locator_type, locator)
        self.action.move_to_element(element).double_click(element).perform()


    def wait_for_page_to_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element(self, locator, locator_type=By.CSS_SELECTOR, timeout=15):
        element_wait = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((locator_type, locator))
        )
        return element_wait
    def wait_for_element_clickable(self, locator, locator_type=By.CSS_SELECTOR, timeout=15):
        element_wait = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((locator_type, locator))
        )
        return element_wait

    def wait_for_find_then_click(self, locator):
        self.wait_for_element(locator)
        element_selector_clicked = self.find_element_and_click(locator)
        return element_selector_clicked

    def wait_for_find_then_double_click(self, locator, locator_type=By.XPATH):
        self.wait_for_element(locator, locator_type)
        element_selector_double_clicked = self.find_element_and_double_click(locator, locator_type)
        return element_selector_double_clicked

    def wait_for_find_click_then_send_keys(self, locator, keys_to_send):
        element_selector_clicked = self.wait_for_find_then_click(locator)
        # self.find_element_and_click_and_send_keys(locator, keys_to_send)
        element_selector_clicked.send_keys(keys_to_send)

    def retry_wait_find_then_click(self, locator, max_retries=5, retry_delay=1):
        retries = 0
        while retries < max_retries:
            try:
                element = self.wait_for_find_then_click(locator)
                break  # Break out of the loop if element is found and clicked successfully
            except (NoSuchElementException, TimeoutException):
                print(f"Element not found. Retrying... (Attempt {retries+1}/{max_retries})")
                retries += 1
                time.sleep(retry_delay)  # Delay before retrying
        else:
            # Executed if the loop completes without encountering a break statement (i.e., max_retries reached)
            print("Maximum number of retries reached. Element not found.")

    def retry_wait_find_then_double_click(self, locator, locator_type=By.XPATH , max_retries=5, retry_delay=1):
        retries = 0
        while retries < max_retries:
            try:
                element = self.wait_for_find_then_double_click(locator, locator_type)
                break  # Break out of the loop if element is found and clicked successfully
            except (NoSuchElementException, TimeoutException):
                print(f"Element not found. Retrying... (Attempt {retries+1}/{max_retries})")
                retries += 1
                time.sleep(retry_delay)  # Delay before retrying
        else:
            # Executed if the loop completes without encountering a break statement (i.e., max_retries reached)
            print("Maximum number of retries reached. Element not found.")


    def check_element_visibility(self, locator ,locator_type=By.CSS_SELECTOR):
        element = self.driver.find_element(locator_type, locator)
        if element.is_displayed():
            print("Element is visible")
        else:
            print("Element is not visible")
