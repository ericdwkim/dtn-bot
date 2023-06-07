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

    """
    src_locators - mapping for source elements
    target_locators - mapping for target element(s)
    source_element - elem to drag
    target_element - elem to drop onto
    """

    def find_element_drag_and_drop(self, src_locators, src_locator_key, target_locators, target_locator_key):
        src_locator_type, src_locators_list = src_locators[src_locator_key]
        target_locator_type, target_locators_list = target_locators[target_locator_key]

        for src_locator in src_locators_list:
            for target_locator in target_locators_list:
                try:
                    source_element = self.driver.find_element(src_locator_type, src_locator)
                    target_element = self.driver.find_element(target_locator_type, target_locator)
                    self.action.drag_and_drop(source_element, target_element).perform()
                    return True  # Drag and drop successful
                except Exception as e:
                    print(f"Drag and drop failed.\nSource locator key: {src_locator_key} |\nSource locator: {src_locator}\nTarget locator key: {target_locator_key} |\nTarget locator: {target_locator}.\n Error: {e}")
        return False  # Drag and drop failed

    """
    find_element_and_click() uses WebElement.click()
    NOTE: some fns require `element_selector` to be returned, such as WebElement.send_keys()
    Will need to come back and refactor... 
    """
    def find_element_and_click(self, locator ,locator_type=By.CSS_SELECTOR):
        element_selector = self.driver.find_element(locator_type, locator)
        element_selector.click()
        return element_selector

    def find_element_and_click_and_send_keys(self, locator, keys_to_send):
        element_selector_clicked = self.find_element_and_click(locator)
        element_selector_clicked.send_keys(keys_to_send)

    """
    find_element_and_click_perform() uses ActionChains
    """
    def find_element_and_click_perform(self, locator, locator_type=By.CSS_SELECTOR):
        element = self.driver.find_element(locator_type, locator)
        self.action.move_to_element(element).click(element).perform()

    def find_element_and_double_click(self, locator, locator_type=By.XPATH):
        element = self.driver.find_element(locator_type, locator)
        self.action.move_to_element(element).double_click(element).perform()

    def wait_for_page_to_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def wait_for_element(self, locator, locator_type=By.CSS_SELECTOR, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((locator_type, locator))
            )
            return True # If element is found within `timeout`
        except TimeoutException:
            return False # If exception raised

    def wait_for_element_clickable(self, locator, locator_type=By.CSS_SELECTOR, timeout=30):
        element_wait = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((locator_type, locator))
        )
        return element_wait

    """
    wait_for_find_then_click() uses WebElement.click()
    """
    def wait_for_find_then_click(self, locator):
        try:
            is_element_present = self.wait_for_element(locator)
            if is_element_present:
                element = self.find_element_and_click(locator)
                # print(f'Successfully clicked on the element: {element}')
                return True
            else:
                print(f'Element was not present using locator:  {locator}.')
                return False
        except NoSuchElementException:
            print(f'NoSuchElementException: The element was not found using locator: {locator}.')
            return False

    """
    wait_for_find_then_single_click() uses ActionChains.click().perform()
    """
    def wait_for_find_then_single_click(self, locator, locator_type=By.CSS_SELECTOR):
        self.wait_for_element(locator)
        self.find_element_and_click_perform(locator, locator_type)


    def wait_for_find_then_double_click(self, locator, locator_type=By.XPATH):
        self.wait_for_element_clickable(locator, locator_type)
        element_selector_double_clicked = self.find_element_and_double_click(locator, locator_type)
        return element_selector_double_clicked

    def wait_for_find_click_then_send_keys(self, locator, keys_to_send):
        element_selector_clicked = self.wait_for_find_then_click(locator)
        # self.find_element_and_click_and_send_keys(locator, keys_to_send)
        element_selector_clicked.send_keys(keys_to_send)

    """
    retry_wait_for_single_click_perform() uses ActionChains.click()
    
    """
    def retry_wait_for_single_click_perform(self, locator, locator_type=By.CSS_SELECTOR, max_retries=5, retry_delay=1 ):
        retries = 0
        while retries < max_retries:
            try:
                element = self.wait_for_find_then_single_click(locator, locator_type)
                return True # Return True and exit fn if elm is found and clicked successfully
            except (NoSuchElementException, TimeoutException):
                print(f'Element (single ActionChains.click) with locator: {locator} not found. Retrying... (Attempt {retries+1}/{max_retries})')
                retries += 1
                time.sleep(retry_delay) # Delay before retrying
        else:
            # Executed if the loop completes without encountering a break statement (i.e., max_retries reached)
            print(f'Maximum number of retries reached. Element (single ActionChains.click) with locator: {locator}  not found.')
            return False  # Return False if element was not found after max_retries


    """
    retry_wait_find_then_click() uses WebElement.click()

    """

    def retry_wait_find_then_click(self, locator, max_retries=5, retry_delay=1):
        retries = 0
        while retries < max_retries:
            try:
                element = self.wait_for_find_then_click(locator)
                return True  # Return True and exit the function if element is found and clicked successfully
            except (NoSuchElementException, TimeoutException):
                print(f'Element (single click) with locator: {locator} not found. Retrying... (Attempt {retries+1}/{max_retries})')
                retries += 1
                time.sleep(retry_delay)  # Delay before retrying
        else:
            # Executed if the loop completes without encountering a break statement (i.e., max_retries reached)
            print(f'Maximum number of retries reached. Element (single click) with locator: {locator}  not found.')
            return False  # Return False if element was not found after max_retries

    def retry_wait_find_then_double_click(self, locator, locator_type=By.XPATH , max_retries=5, retry_delay=1):
        retries = 0
        while retries < max_retries:
            try:
                element = self.wait_for_find_then_double_click(locator, locator_type)
                return True  # Return True and exit the function if element is found and clicked successfully
            except (NoSuchElementException, TimeoutException):
                print(f'Element (double click) with locator: {locator} not found. Retrying... (Attempt {retries+1}/{max_retries})')
                retries += 1
                time.sleep(retry_delay)  # Delay before retrying
        else:
            # Executed if the loop completes without encountering a break statement (i.e., max_retries reached)
            print(f'Maximum number of retries reached. Element (double click) with locator: {locator}  not found.')
            return False  # Return False if element was not found after max_retries



    def check_element_visibility(self, locator ,locator_type=By.CSS_SELECTOR):
        element = self.driver.find_element(locator_type, locator)
        if element.is_displayed():
            print("Element is visible")
        else:
            print("Element is not visible")
