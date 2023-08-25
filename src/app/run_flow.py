import argparse
import logging
# from subprocess import run
from src.app.flow_manager import FlowManager
from utils.pdf_processor import PdfProcessor


# todo: keeps trying to save in working dir `src` so it creates new Fuel Invoices/yyyy/mm
def first_flow(flow_manager, processor):
    logging.info(f'\n---------------------------\nInitiating First Flow\n---------------------------\n')
    try:
        # flow_manager.start_flow()

        group_filter_set_to_invoice =  flow_manager.data_connect_driver.set_group_filter_to_invoice()

        if not group_filter_set_to_invoice:
            logging.error('Could not set group filter to invoice')

        invoices_downloaded = flow_manager.data_connect_driver.data_connect_page.check_all_then_click_print()

        if not invoices_downloaded:
            logging.error('Could not download Invoices')

        invoices_renamed_and_filed_away = processor.rename_and_move_or_overwrite_invoices_pdf()

        if not invoices_renamed_and_filed_away:
            logging.error('Could not rename and file away invoices. Does the Invoices PDF exist?')

        elif invoices_renamed_and_filed_away and processor.is_last_day_of_month():
            processor.month_and_year_handler(first_flow=True)

        logging.info(f'\n---------------------------\nCommencing First Flow\n---------------------------\n')


    except Exception as e:
        logging.info(f'an error: {e}')



    # finally:
    #     invoices_renamed_and_filed_away = processor.rename_and_move_or_overwrite_invoices_pdf()
    #
    #     if not invoices_renamed_and_filed_away:
    #         logging.error('Could not rename and file away invoices. Does the Invoices PDF exist?')
    #
    #     elif invoices_renamed_and_filed_away and processor.is_last_day_of_month():
    #         processor.month_and_year_handler(first_flow=True)
    #
    #     flow_manager.end_flow()
    #
    #     logging.info(f'\n---------------------------\nCommencing First Flow\n---------------------------\n')



def second_flow(flow_manager, processor):
    logging.info(f'\n---------------------------\nInitiating Second Flow\n---------------------------\n')

    try:
        # flow_manager.start_flow()
        group_filter_set_to_draft_notice = flow_manager.data_connect_driver.set_group_filter_to_draft_notice()
        logging.info(f'group_filter_set_to_draft_notice: {group_filter_set_to_draft_notice}')

        if not group_filter_set_to_draft_notice:
            logging.error('Could not set group filter to Draft Notice during second_flow')

        draft_notices_processed_and_filed = processor.process_pages()

        if not draft_notices_processed_and_filed:
            logging.error('Could not rename and file away Draft Notices. Do the notices PDF exist?')

        elif draft_notices_processed_and_filed and processor.is_last_day_of_month():
            processor.month_and_year_handler()


    except Exception as e:
        logging.info(f'an error: {e}')



    # finally:
    #     # TODO:
    #     #processor.rename_and_delete_pdf()
    #     flow_manager.end_flow()
    #     logging.info('END OF SECOND__FLOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')



def third_flow(flow_manager, processor):
    logging.info('running third flow....')

    # third flow specific logic
    pass


# @dev: call w/o args if wish to run all three flows in sequential order using the same ChromeDriver instance todo: will need to refactor flow funcs to conditionally `start_flow` and `end_flow` depending on whether it is to be ran in sequential order (only one `start_flow` and `end_flow` necessary OR individually (currently as is)
def run_flows(flow_manager, processor, flows):
    # Setup session
    flow_manager.start_flow()

    for flow in flows:
        logging.info(f'Running flow: {flow}')
        flow(flow_manager, processor)   # Execute all flow(s)

    # Terminate session
    flow_manager.end_flow()


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

    flows_to_run = []
    if not args.skipFlow1:
        flows_to_run.append(first_flow)
    if not args.skipFlow2:
        flows_to_run.append(second_flow)
    if not args.skipFlow3:
        flows_to_run.append(third_flow)

    # Delete all PDFs in Downloads directory
    # run(["../scripts/clean_slate.sh"], shell=True)
    # print(f'===========================================================================================')

    run_flows(flow_manager, processor, flows_to_run)
    logging.info(f'\n---------------------------\nCommencing All Flows\n---------------------------\n')
