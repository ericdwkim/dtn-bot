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

    def find_and_wait_for_elem_to_be_clickable(self, locator, locator_type):
        """
        wait_for_presence_of_elements_located and wait_for_element_clickable wrapper
        :param locator:
        :param locator_type:
        :return:
        """
        try:
            element_located = self.wait_for_presence_of_elements_located(locator, locator_type)
            element_clickable = self.wait_for_element_clickable(locator, locator_type)
            return element_located, element_clickable
        except Exception as e:
            print(f'An error occurred trying to locate and click element: {str(e)}')
            return None, None

    def find_and_wait_for_src_elem_to_be_clickable_and_target_elems_to_be_present(self, src_locator, target_elem_idx, target_locator="//ul[@class='selected connected-list ui-sortable']", locator_type=By.XPATH):
        """
        Find and wait for single source WebElement to be clickable\n
        Find and wait for multiple target WebElements to be present on DOM
        :param src_locator:
        :param target_elem_idx:
        :param target_locator:
        :param locator_type:
        :return: Tuple(WebElement, bool, WebElement, bool)
        """
        source_element = None
        src_element_is_clickable_and_present = False
        target_element = None
        target_elements_present = False

        try:
            source_element = self.driver.find_element(locator_type, src_locator)
            target_elements = self.driver.find_elements(locator_type, target_locator)

            # if a single WebElement from source_locator was found and a list of WebElements
            # from target_locator were found, and if the idx for target element is less than the total length of the list of WebElements from target_locator, then assign
            # that specific WebElement to `target_element` per `target_elem_idx`
            if source_element and target_elements and target_elem_idx < len(target_elements):
                target_element = target_elements[target_elem_idx]

            else:
                print(f'Could not find source WebElement: {src_locator}\nand/or target WebElements: target_locator[{target_elem_idx}]')

            src_element_is_clickable = self.wait_for_element_clickable(src_locator, locator_type)
            src_element_is_present = self.wait_for_presence_of_elements_located(src_locator, locator_type)
            src_element_is_clickable_and_present = src_element_is_clickable and src_element_is_present
            target_elements_present =  self.wait_for_presence_of_elements_located(target_locator, locator_type)

        except Exception as e:
            print(
                f"Error finding or waiting for source/target elements.\nSource locator: {src_locator}\nTarget locator: {target_locator}\nLocator type: {locator_type}\nError {str(e)}")

        return source_element, src_element_is_clickable_and_present, target_element, target_elements_present

    def find_element_drag_and_drop(self, src_locator, target_elem_idx):
        """
        Find element by src_locator string, drag elem and drop to target element by index target_elem_idx
        :param src_locator:
        :param target_elem_idx:
        :return: bool
        """

        source_element, src_element_is_clickable_and_present, target_element, target_elements_present = self.find_and_wait_for_src_elem_to_be_clickable_and_target_elems_to_be_present(
            src_locator, target_elem_idx)

        if source_element and target_element and src_element_is_clickable_and_present and target_elements_present:
            self.action.drag_and_drop(source_element, target_element).perform()
            time.sleep(10)  # Wait for UI to update
            return True

        # @dev: Handles edge case when either Draft Notices or Credit Cards are unavailable for set date; if so, continue to next flow
        elif source_element and target_element and not src_element_is_clickable_and_present and not target_elements_present and (
                (src_locator == r"//li[@title='Draft Notice']") or (src_locator == r"//li[@title='Credit Card']")):
            print(f'Unable to wait for src elem: {src_locator} to be found and interactable\nAre there Draft Notices or Credit Cards for set date?\nProceeding with the script...')
            return True

        else:
            print(f'Source and/or Target element was not found and/or not present\nsrc_locator: {src_locator} | target_elem_idx: {target_elem_idx}')
            return False


    def find_element_and_click(self, locator, locator_type=By.CSS_SELECTOR):
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
        """
        Find element by locator string, click on element, and send keys
        :param locator:
        :param keys_to_send:
        :return: bool
        """
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

    def find_element_and_click_perform(self, locator, locator_type=By.CSS_SELECTOR):
        """
        Finds element by locator string using locator_type. Uses ActionChains to click() and perform()
        :param locator:
        :param locator_type:
        :return: bool
        """
        element = self.driver.find_element(locator_type, locator)
        if element:
            self.action.move_to_element(element).click(element).perform()
            return True
        else:
            print(f'Could not locate element: {locator}')
            return False


    def wait_for_element(self, locator, locator_type=By.CSS_SELECTOR, timeout=30):
        """
        Waits for element by locator string using locator_type with a timeout
        :param locator:
        :param locator_type:
        :param timeout:
        :return: bool
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((locator_type, locator))
            )
            return True # If element is found within `timeout`
        except TimeoutException:
            return False # If exception raised

    def wait_for_element_clickable(self, mark, locator_type=None, timeout=30):
        """
        Checking for singular element to be interactable
        :param mark:
        :param locator_type:
        :param timeout:
        :return: bool
        """

        try:
            # Check if 'mark' is a WebElement
            if self.is_web_element(mark):
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(mark)
                )
            # If 'mark' is not a WebElement, then it is assumed to be a locator
            else:
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((locator_type, mark))
                )

            # print(f'element: {mark} is clickable!')
            return True  # If element is found within `timeout`
        except TimeoutException:
            print(f'Tried to wait for element: {mark} to be clickable')
            return False

    @staticmethod
    def is_web_element(obj):
        """
        Checks for common attributes/methods a WebElement instance has, such as `tag_name`\nas a workaround since `WebElement` is not a directly importable class in Selenium module. There is no direct way to check if an obj is a WebElement via isintance() method.
        :param obj:
        :return: bool
        """
        return hasattr(obj, "tag_name")

    def wait_for_presence_of_elements_located(self, locator, locator_type=By.CSS_SELECTOR, timeout=30):
        """
        Checking for multiple elements to be visible
        will return list of WebElements to idx `WebElements[idx]`
        :param locator:
        :param locator_type:
        :param timeout:
        :return: bool
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
        :param locator_type: default to CSS SELECTOR
        :param locator: locator string for element to wait and click
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