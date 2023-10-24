import logging


class CustomFormatter(logging.Formatter):
    GREEN = "\033[0;32m"
    YELLOW = "\E[33;47m"
    RED = "\033[1;31m"
    RESET = "\033[0;0m"

    FORMATS = {
        logging.DEBUG: GREEN + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.INFO: GREEN + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.WARNING: YELLOW + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.ERROR: RED + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.CRITICAL: RED + "%(asctime)s - %(levelname)s - %(message)s" + RESET
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


# @dev: removing existing handler before establishing new handler; prevents duplicate logs with `INFO.root:`
def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

# @dev: decorator to centralize error handling for all functions
def handle_errors(func):
    def catch_and_log(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.exception(f'An error occurred in {func.__name__}: {e}')
            return False
    return catch_and_log

# @dev: format logging output of list of pdf files in easy to read format
def pdf_files_logger(pdf_files):
    if len(pdf_files) == 0:
        logging.info(f'\nThere are no files in the current iteration.\n')
        return
    for idx, pdf_file in enumerate(pdf_files):
        logging.info(f'\nNumber of files: {len(pdf_files)} files.\nFile #{idx+1}: {pdf_file}\n')

# todo: needs fixing...
# def total_amt_matches_logger(total_amount_matches):
#     if len(total_amount_matches) == 0:
#         logging.info(f'\nThere are no matches for total amounts in the current iteration.\n')
#         return
#     for idx, amt_match in total_amount_matches:
#         while idx == 0:
#             logging.info(f'\nNumber of total amount matches: {len(total_amount_matches)}.\nLast (3) Matches: {total_amount_matches[-3:]}\n')
