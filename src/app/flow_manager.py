import logging, time
from src.app.drivers import BaseDriver, LoginPageDriver, DataConnectDriver
class FlowManager:
    def __init__(self, headless=False):
        # @dev: subclass drivers have and use base_driver
        self.base_driver = BaseDriver(headless=headless)
        self.login_page_driver = LoginPageDriver(self.base_driver)
        self.data_connect_driver = DataConnectDriver(self.base_driver)

    # @dev: what all flows should do in sequence regardless of what flow number assuming they are independently ran
    def start_flow(self, third_flow=False):
        try:
            site_visited_and_logged_in = self.login_page_driver.visit_and_login()
            if not site_visited_and_logged_in:
                raise RuntimeError('site_visited_and_logged_in returned false')
            else:
                logging.info('Logged in to DataConnect Successfully')

            tab_switched_to_data_connect = self.data_connect_driver.switch_tab()
            if not tab_switched_to_data_connect:
                raise RuntimeError('tab_switched_to_data_connect returned false')
            time.sleep(15)  # Wait for DOM to load switched tab

            date_filter_set = self.data_connect_driver.set_date_filter(third_flow)
            if not date_filter_set:
                raise RuntimeError('Something went wrong3')

            translated_set_to_no = self.data_connect_driver.set_translated_filter_to_no()
            if not translated_set_to_no:
                raise RuntimeError('Something went wrong')
        except Exception as e:
            logging.exception(f'An error occurred trying to start_flow: {e}')

    def end_flow(self):
        try:
            logging.info('Tearing down ChromeDriver. Placeholder')
            # self.base_driver.teardown_driver()  # todo: renable after deving
        except Exception as e:
            logging.exception(f'An error occurred trying to tear down ChromeDriver: {e}')

