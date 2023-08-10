from src.app.flow_manager import FlowManager
from src.app.drivers import DataConnectDriver
from src.pages import DataConnectPage
import logging

def first_flow():
    flow_manager = FlowManager()
    data_connect_page = DataConnectDriver()
    logging.info(f'\n---------------------------\nInitiating First Flow\n---------------------------\n')
    try:
        flow_manager.start_flow()
        # first flow specific logic
        group_filter_set_to_invoice = data_connect_page.set_group_filter_to_invoice()
        if not group_filter_set_to_invoice:
            logging.error('Could not set group filter to invoice')



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
