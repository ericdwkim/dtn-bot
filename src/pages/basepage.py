import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.action = ActionChains(self.driver)

    def find_and_wait_for_src_to_be_clickable_and_target_to_be_visible(self, src_locator, target_locators, idx,
                                                                       locator_type=By.XPATH):
        source_element = None
        source_element_clickable = False
        target_element = None
        target_elements_visible = False

        try:
            source_element = self.driver.find_element(locator_type, src_locator)
            if source_element:
                target_elements = self.driver.find_elements(locator_type, target_locators)
                if target_elements and idx < len(target_elements):
                    target_element = target_elements[idx]
                else:
                    print(f"No target element found at idx {idx} or idx is out of range.")

            else:
                print(f"No source element found with locator: {src_locator}")

            source_element_clickable = self.wait_for_element_clickable(src_locator, locator_type)
            target_elements_visible = self.wait_for_presence_of_elements_located(target_locators, locator_type)

        except Exception as e:
            print(
                f"Error finding or waiting for source/target elements.\nSource locator: {src_locator}\nTarget locators: {target_locators}\nLocator type: {locator_type}\nError: {str(e)}")

        return source_element, source_element_clickable, target_element, target_elements_visible

    def find_element_drag_and_drop(self, src_locator, target_locator):

        source_element, source_element_clickable, target_element, target_element_clickable = self.find_and_wait_for_src_to_be_clickable_and_target_to_be_visible(src_locator, target_locator)

        # print(f'source_element: {source_element}\nsource_element_clickable: {source_element_clickable}\ntarget_element: {target_element}\ntarget_element_clickable: {target_element_clickable}')

        # Only if True, True, True, True, invoke drag_and_drop()
        if source_element and target_element and source_element_clickable and target_element_clickable:
            self.action.drag_and_drop(source_element, target_element).perform()
            time.sleep(10) # Wait for UI to update
            return True
        else:
            print("Source and/or Target element was not found and/or clickable")
            return False

    def find_element_and_click(self, locator ,locator_type=By.CSS_SELECTOR):
        """
        Finds element and clicks it using `WebElement.click()`
        :param locator:
        :param locator_type:
        :return: Tuple(bool, WebElement)
        """
        try:
            element = self.driver.find_element(locator_type, locator)
            element.click()
            return True, element
        except NoSuchElementException:
            print(f'Element {locator} was not found.')
            return False, None
        except Exception as e:
            print(f'Error occurred when trying to find and click element: {str(e)}')
            return False, None

    def find_element_and_click_and_send_keys(self, locator, keys_to_send):
        try:
            was_clicked, element_selector_clicked = self.find_element_and_click(locator)
            if was_clicked:
                element_selector_clicked.send_keys(keys_to_send)
                return True
            else:
                print(f'Failed to send keys to element: {locator}')
                return False
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False

    """
        @dev: find_element_and_click_perform() uses ActionChains
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
        """
        Checking for singular element to be intractable
        :param locator:
        :param locator_type:
        :param timeout:
        :return: bool
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((locator_type, locator))
            )
            # print(f'element: {locator} is clickable!')
            return True #If element is found within `timeout`
        except TimeoutException:
            print(f'Tried to wait for element: {locator} to be clickable using locator type: {locator_type}')
            return False

    def wait_for_presence_of_elements_located_then_click(self, locator, locator_type=By.CSS_SELECTOR, timeout=15):
        """
        :param locator:
        :param locator_type:
        :param timeout:
        :return: list of WebElements as `elements`
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((locator_type, locator))
            )
            # print(f'Element: {locator} was found')
            return elements
        except Exception as e:
            print(f'An error occurred trying to click filter button: {str(e)}')
            return None

    def wait_for_presence_of_elements_located(self, locator, locator_type=By.CSS_SELECTOR, timeout=30):
        """
        Checking for multiple elements to be visible
        will return list of WebElements to idx `WebElements[idx]`
        :param locator:
        :param locator_type:
        :param timeout:
        :return: BOOL
        TODO: NOTE,  presence_of_all_elements_located returns list of WebElements!!!!
        """

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((locator_type, locator))
            )
            return True
        except (NoSuchElementException, TimeoutException):
            print(f'Tried to check visibility of list WebElements: {locator} using locator type: {locator_type}')
            return False
    def wait_for_find_then_click(self, locator, locator_type=By.CSS_SELECTOR):
        """
        `wait_for_element()` + `find_element_and_click()`\n wrapper using `WebElement.click()`
        :param locator:
        :return: bool
        """
        try:
            is_element_present = self.wait_for_element(locator, locator_type)
            if is_element_present:
                element = self.find_element_and_click(locator, locator_type)
                # print(f'Successfully clicked on the element: {element}')
                return True
            else:
                print(f'Element "{locator}" was not present.')
                return False
        except NoSuchElementException:
            print(f'NoSuchElementException: The element "{locator}" was not found.')
            return False

    """
        @dev: wait_for_find_then_single_click() uses ActionChains.click().perform()
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
        @dev: retry_wait_for_single_click_perform() uses ActionChains.click()
    """
    def retry_wait_for_single_click_perform(self, locator, locator_type=By.CSS_SELECTOR, max_retries=5, retry_delay=1 ):
        retries = 0
        while retries < max_retries:
            try:
                # TODO: combine both functions into a single helper fn?
                print("Going to wait for it to be clickable")
                self.wait_for_element_clickable(locator, locator_type)
                print("Going to wait for it and then single click")
                self.wait_for_find_then_single_click(locator, locator_type)
                return True # Return True and exit fn if elm is found and clicked successfully
            except (NoSuchElementException, TimeoutException):
                print(f'Element (single ActionChains.click) with locator: {locator} not found. Retrying... (Attempt {retries+1}/{max_retries})')
                retries += 1
                time.sleep(retry_delay) # Delay before retrying
        else:
            # Executed if the loop completes without encountering a break statement (i.e., max_retries reached)
            print(f'Maximum number of retries reached. Element (single ActionChains.click) with locator: {locator}  not found.')
            return False  # Return False if element was not found after max_retries


    def retry_wait_find_then_click(self, locator, locator_type=By.CSS_SELECTOR, max_retries=5, retry_delay=1):
        """
        Retry wrapper for `wait_for_find_then_click()`
        :param locator:
        :param max_retries:
        :param retry_delay:
        :return: bool
        """
        retries = 0
        while retries < max_retries:
            try:
                element = self.wait_for_find_then_click(locator, locator_type)
                # print(f'Found element: {locator}')
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

