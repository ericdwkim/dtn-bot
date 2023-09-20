import argparse
import logging
# from subprocess import run
from src.app.flow_manager import FlowManager
from utils.pdf_processor import PdfProcessor


# todo: keeps trying to save in working dir `src` so it creates new Fuel Invoices/yyyy/mm; need it to save it in downloads dir as from and overwrite/save to target dir
def first_flow(flow_manager, processor):
    try:

        group_filter_set_to_invoice =  flow_manager.data_connect_driver.set_group_filter_to_invoice()

        if not group_filter_set_to_invoice:
            logging.error('Could not set group filter to invoice')

        invoices_renamed_and_filed_away = processor.rename_and_move_or_overwrite_invoices_pdf()

        if not invoices_renamed_and_filed_away:
            logging.error('Could not rename and file away invoices. Does the Invoices PDF exist?')

        elif invoices_renamed_and_filed_away and processor.is_last_day_of_month():
            processor.month_and_year_handler(first_flow=True)

    except Exception as e:
        logging.info(f'An unexpected error has occurred during first_flow: {e}')



def second_flow(flow_manager, processor):

    try:
        group_filter_set_to_draft_notice = flow_manager.data_connect_driver.set_group_filter_to_draft_notice()
        logging.info(f'group_filter_set_to_draft_notice: {group_filter_set_to_draft_notice}')

        if not group_filter_set_to_draft_notice:
            logging.error('Could not set group filter to Draft Notice during second_flow')


        draft_notices_processed_and_filed = processor.process_pages()

        if not draft_notices_processed_and_filed:
            logging.error('Could not rename and file away Draft Notices. Do the notices PDF exist?')

        elif draft_notices_processed_and_filed and processor.is_last_day_of_month():
            processor.month_and_year_handler(first_flow=False)

    except Exception as e:
        logging.info(f'An unexpected error has occurred during second_flow: {e}')


def third_flow(flow_manager, processor):

    try:
        group_filter_set_to_credit_card = flow_manager.data_connect_driver.set_group_filter_to_credit_card()
        logging.info(f'group_filter_to_credit_card: {group_filter_set_to_credit_card}')

        if not group_filter_set_to_credit_card:
            logging.error('Could not set group filter to Credit Card during third_flow')

        ccms_processed_and_filed = processor.process_pages()

        if not ccms_processed_and_filed:
            logging.error('Could not rename and file away CCMs')
        elif ccms_processed_and_filed and processor.is_last_day_of_month():
            processor.month_and_year_handler(first_flow=False)

    except Exception as e:
        logging.info(f'An unexpected error has occurred during third_flow: {e}')


def run_flows(flow_manager, processor, flows):
    num_flows = len(flows)

    for i, (flow_func, flow_name) in enumerate(flows):
        logging.info(f'\n---------------------------\nInitiating Flow: {flow_name}\n---------------------------\n')

        # Only start the flow at the beginning of the list of flows.
        if i == 0:
            if flow_name == 'third_flow':
                flow_manager.start_flow(third_flow=True)
            else:
                flow_manager.start_flow(third_flow=False)

        flow_func(flow_manager, processor)  # Execute flows

        if flow_name in ['second_flow', 'third_flow']:
            original_pdf_deleted = processor.rename_and_delete_pdf()
            logging.info(f'original_pdf_deleted: {original_pdf_deleted}')

        logging.info(f'\n---------------------------\nCommencing Flow: {flow_name}\n---------------------------\n')

        # Only end the flow if it's the last one in the list of flows.
        if i == num_flows - 1:
            flow_manager.end_flow()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DTN Bot V2')
    parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
    parser.add_argument('--skipFlow1', required=False, action='store_true', help='Skip the first flow')
    parser.add_argument('--skipFlow2', required=False, action='store_true', help='Skip the second flow')
    parser.add_argument('--skipFlow3', required=False, action='store_true', help='Skip the third flow')
    args = parser.parse_args()

    flow_manager = FlowManager(headless=args.headless)
    processor = PdfProcessor()

    flows_to_run = []
    if not args.skipFlow1:
        flows_to_run.append((first_flow, 'first_flow'))
    if not args.skipFlow2:
        flows_to_run.append((second_flow, 'second_flow'))
    if not args.skipFlow3:
        flows_to_run.append((third_flow, 'third_flow'))

    # Delete all PDFs in Downloads directory
    # run(["../scripts/clean_slate.sh"], shell=True)
    # print(f'===========================================================================================')

    run_flows(flow_manager, processor, flows_to_run)
    logging.info(f'\n---------------------------\nCommencing All Flows\n---------------------------\n')
