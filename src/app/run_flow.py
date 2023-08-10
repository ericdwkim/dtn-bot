from src.app.flow_manager import FlowManager
import logging

def first_flow():
    flow_manager = FlowManager()
    logging.info(f'\n---------------------------\nInitiating First Flow\n---------------------------\n')
    try:
        flow_manager.start_flow()
        # first flow specific logic
        group_filter_set_to_invoice =  flow_manager.data_connect_driver.set_group_filter_to_invoice()

        if not group_filter_set_to_invoice:
            logging.error('Could not set group filter to invoice')

        else:
            invoices_downloaded = flow_manager.data_connect_driver.data_connect_page.check_all_then_click_print()

    finally:
        flow_manager.end_flow()


first_flow()

# def second_flow():
#     flow_manager = FlowManager()
#
#     try:
#         flow_manager.start_flow()
#         # ... Rest of second_flow logic ...
#     finally:
#         flow_manager.end_flow()
#
#
#
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
