import argparse
import logging
from src.app.flow_manager import FlowManager
from utils.pdf_processor import PdfProcessor



def first_flow(flow_manager, processor):
    logging.info(f'\n---------------------------\nInitiating First Flow\n---------------------------\n')
    try:
        flow_manager.start_flow()

        group_filter_set_to_invoice =  flow_manager.data_connect_driver.set_group_filter_to_invoice()

        if not group_filter_set_to_invoice:
            logging.error('Could not set group filter to invoice')

        invoices_downloaded = flow_manager.data_connect_driver.data_connect_page.check_all_then_click_print()

        if not invoices_downloaded:
            logging.error('Could not download Invoices')


    finally:
        invoices_renamed_and_filed_away = processor.rename_and_move_or_overwrite_invoices_pdf()

        if not invoices_renamed_and_filed_away:
            logging.error('Could not rename and file away invoices. Does the Invoices PDF exist?')

        elif invoices_renamed_and_filed_away and processor.is_last_day_of_month():
            processor.month_and_year_handler(first_flow=True)

        flow_manager.end_flow()

        logging.info(f'\n---------------------------\nCommencing First Flow\n---------------------------\n')



def second_flow(flow_manager, processor):
    logging.info(f'\n---------------------------\nInitiating Second Flow\n---------------------------\n')

    try:
        flow_manager.start_flow()
        # TODO WIP - does not select all prior tp clicking print
        group_filter_set_to_draft_notice = flow_manager.data_connect_driver.set_group_filter_to_draft_notice()

        if not group_filter_set_to_draft_notice:
            logging.error('Could not set group filter to Draft Notice during second_flow')

        draft_notices_processed_and_filed = processor.process_pages()

        if not draft_notices_processed_and_filed:
            logging.error('Could not download Draft Notices')



    finally:
        # TODO:
        #processor.rename_and_delete_pdf()
        flow_manager.end_flow()
        logging.info('END OF SECOND__FLOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')



def third_flow(flow_manager, processor):
    logging.info('running third flow....')

    # third flow specific logic
    pass


# @dev: call w/o args if wish to run all three flows in sequential order using the same ChromeDriver instance todo: will need to refactor flow funcs to conditionally `start_flow` and `end_flow` depending on whether it is to be ran in sequential order (only one `start_flow` and `end_flow` necessary OR individually (currently as is)
def run_flows(flow_manager, processor, args):
    if not args.skipFlow1:
        first_flow(flow_manager, processor)
    if not args.skipFlow2:
        second_flow(flow_manager, processor)
    if not args.skipFlow3:
        third_flow(flow_manager, processor)

#todo: if wish to call individual flows, will need to ensure each flow calls its own `start_flow` and `end_flow`



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DTN Bot V2')
    parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
    parser.add_argument('--skipFlow1', required=False, action='store_true', help='Skip the first flow')
    parser.add_argument('--skipFlow2', required=False, action='store_true', help='Skip the second flow')
    parser.add_argument('--skipFlow3', required=False, action='store_true', help='Skip the third flow')
    args = parser.parse_args()

    flow_manager = FlowManager(headless=args.headless)
    processor = PdfProcessor()

    # Delete all PDFs in Downloads directory
    run(["../scripts/clean_slate.sh"], shell=True)
    print(f'===========================================================================================')

    run_flows(flow_manager, processor, args)
    logging.info(f'\n---------------------------\nCommencing All Flows\n---------------------------\n')
