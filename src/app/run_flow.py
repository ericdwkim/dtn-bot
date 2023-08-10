from src.app.flow_manager import FlowManager
from utils.pdf_processor import PdfProcessor
import logging
from utils.filesystem_manager import is_last_day_of_month, end_of_month_operations

def first_flow():
    flow_manager = FlowManager()
    processor = PdfProcessor()
    logging.info(f'\n---------------------------\nInitiating First Flow\n---------------------------\n')
    try:
        flow_manager.start_flow()

        group_filter_set_to_invoice =  flow_manager.data_connect_driver.set_group_filter_to_invoice()

        if not group_filter_set_to_invoice:
            logging.error('Could not set group filter to invoice')

        invoices_downloaded = flow_manager.data_connect_driver.data_connect_page.check_all_then_click_print()

        if not invoices_downloaded:
            logging.error('Could not download Invoices')

        invoices_renamed_and_filed_away = processor.rename_and_move_or_overwrite_invoices_pdf()

        if not invoices_renamed_and_filed_away:
            logging.error('Could not rename and file away invoices. Does the Invoices PDF exist?')

        # WIP - needs to create Sept dir in `Fuel Invoices/2023`
        elif invoices_renamed_and_filed_away and is_last_day_of_month():
            print(f'last day of the month\nPerforming end of month operations....')
            end_of_month_operations(processor.root_dir)
            print(f'done!---------------------------------')


    finally:
        flow_manager.end_flow()

first_flow()

# def second_flow():
#     flow_manager = FlowManager()
#     logging.info(f'\n---------------------------\nInitiating Second Flow\n---------------------------\n')
#
#     try:
#         flow_manager.start_flow()
#
#
#     finally:
#         flow_manager.end_flow()



# def third_flow():
#
#     # third flow specific logic
#     pass
#
#
#
# def run_flows():
#     # first , second, third flows execution wrapper for sequential runs
#     pass
#
