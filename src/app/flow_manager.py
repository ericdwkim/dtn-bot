from src.app.drivers import BaseDriver, LoginPageDriver, DataConnectDriver
class FlowManager:
    def __init__(self):
        # @dev: subclass drivers have and use base_driver
        self.base_driver = BaseDriver()
        self.login_page_driver = LoginPageDriver(self.base_driver)
        self.data_connect_driver = DataConnectDriver(self.base_driver)

    # @dev: what all flows should do in sequence regardless of what flow number assuming they are independently ran
    def start_flow(self):
        try:
            site_visited_and_logged_in = self.login_page_driver.visit_and_login()
            if not site_visited_and_logged_in:
                raise RuntimeError('site_visited_and_logged_in returned false')
            else:
                print(f'logged in successfully!')

            tab_switched_to_data_connect = self.data_connect_driver.switch_tab()
            if not tab_switched_to_data_connect:
                raise RuntimeError('tab_switched_to_data_connect returned false')


            # todo: not sure what changes will need to made, but it will be needed for all three flows, just different for third flow using `third_flow` bool
            date_filter_set = self.data_connect_driver.set_date_filter()
            if not date_filter_set:
                raise RuntimeError('Something went wrong3')

            translated_set_to_no = self.data_connect_driver.set_translated_filter_to_no()
            if not translated_set_to_no:
                raise RuntimeError('Something went wrong')
        except Exception as e:
            print(f'An error occurred trying to start_flow: {e}')

    def end_flow(self):
        self.base_driver.teardown_driver()


"""
# TODO: test implementation in `end_flow()`
        # todo: clean up via `rename_and_delete_pdf()`?


    # TODO: test implementation in `end_flow()`
    # def rename_and_delete_pdf(self):
    #     file_deleted = False
    #     if os.path.exists(self.file_path):
    #         with pikepdf.open(self.file_path) as pdf:
    #             if len(pdf.pages) > 0:
    #                 first_page = self.extractor.extract_text_from_pdf_page(pdf.pages[0])
    #
    #                 if re.search(r'EFT-\d+', first_page) or re.search(r'CCM-\d+ | CMD-\d+', first_page):
    #                     if re.search(r'EFT-\d+', first_page):
    #                         self.new_file_name = f'EFT-{self.today}-TO-BE-DELETED.pdf'
    #                     else:
    #                         self.new_file_name = f'CCM-{self.today}-TO-BE-DELETED.pdf'
    #
    #                     file_directory = os.path.dirname(self.file_path)
    #                     new_file_path = os.path.join(file_directory, self.new_file_name)
    #
    #                     print(f"Renaming file: {self.file_path} to {new_file_path}")
    #                     os.rename(self.file_path, new_file_path)
    #                     file_deleted = True
    #                     print("File renamed successfully.")
    #                     sleep(3)
    #
    #                     if os.path.exists(new_file_path):
    #                         print(f"Deleting file: {new_file_path}")
    #                         os.remove(new_file_path)
    #                         print("File deleted successfully.")
    #
    #             return file_deleted

"""