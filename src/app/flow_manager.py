from src.app.drivers import BaseDriver, LoginPageDriver, DataConnectDriver
class FlowManager:
    def __init__(self):
        self.base_driver = BaseDriver()
        self.login_page_driver = LoginPageDriver()
        self.data_connect = DataConnectDriver()

    # @dev: what all flows should do in sequence regardless of what flow number assuming they are independently ran
    def start_flow(self):
        site_visited_and_logged_in = self.login_page_driver.visit_and_login()
        if not site_visited_and_logged_in:
            raise RuntimeError('Something went wrong1')

        tab_switched_to_data_connect = self.data_connect.switch_tab()
        if not tab_switched_to_data_connect:
            raise RuntimeError('Something went wrong2')

        # todo: not sure what changes will need to made, but it will be needed for all three flows, just different for third flow using `third_flow` bool
        date_filter_set = self.data_connect.set_date_filter()
        if not date_filter_set:
            raise RuntimeError('Something went wrong3')

        translated_set_to_no = self.data_connect.set_translated_filter_to_no()
        if not translated_set_to_no:
            raise RuntimeError('Something went wrong')


    def end_flow(self):
        self.base_driver.teardown_driver()
