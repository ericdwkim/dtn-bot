from drivers import LoginPageDriver, DataConnectDriver
class FlowManager:
    def __init__(self):
        self.base_driver = BaseDriver()
        self.login_driver = LoginPageDriver(self.base_driver)
        self.data_connect = DataConnectDriver(self.base_driver)

    def start_flow(self):
        site_visited_and_logged_in = self.login_driver.visit_and_login()
        if not site_visited_and_logged_in:
            raise RuntimeError('Something went wrong')

        tab_switched_to_data_connect = self.data_connect.switch_tab()
        if not tab_switched_to_data_connect:
            raise RuntimeError('Something went wrong')

    def end_flow(self):
        self.base_driver.teardown_driver()
