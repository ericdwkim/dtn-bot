import logging
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # If specific modules are too verbose, you can silence them here
    # logging.getLogger('specific_module').setLevel(logging.WARNING)
