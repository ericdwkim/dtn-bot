import os
from datetime import datetime, timedelta
from utils.mappings import doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map

def check_file_exists(output_path):
    """
    :param output_path:
    :return: bool
    """
    file_path = os.path.join(output_path)
    return os.path.isfile(file_path)

def move_directory_to_another(src_dir, dst_dir):
    """
    Files away from src_dir to dst_dir for management
    :param src_dir:
    :param dst_dir:
    :return: None
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    shutil.move(src_dir, dst_dir)

def cleanup_files(pdf_data):
    """
    Given a list of tuples. Loop and delete all file_path files in the 4th element of each tuple
    :param pdf_data:
    :return: bool
    """
    files_deleted = False
    for _, _, _, file_path in pdf_data:
        if os.path.exists(file_path):
            os.remove(file_path)
            files_deleted = True
    return files_deleted
# TODO: consider creating a wrapper func for `is_last_day_of_month` then `end_of_month_operations`

def is_last_day_of_month():
    """
    Relative to today's date, it checks if tomorrow's date would be the start of a new month,\n
    if so, then it will return True indicating that today is the last day of the month
    :return: bool
    """
    # today = datetime.today()  # @today
    today = datetime.strptime('08-31-23', '%m-%d-%y')  # testing purposes for `today` as `datetime`


    tomorrow = today + timedelta(days=1)
    return tomorrow.day == 1

def create_directory(directory):
    """
    Checks if `directory` path exists, if not, it creates `directory`
    :param directory: year or month directory
    :return: Any
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

#TODO (WIP): refactor to not require company_dir param, but take assign_file_path_mappings output as `company_dir` instance to concat dynamic cur or next yr/next_month dirs
def end_of_month_operations(company_dir=None):
    """
    Creates the new month and new year directories if it is the last day of the month
    :param company_dir: defaulted to None
    :return: None
    """
    # Handles INV case
    if company_dir is None:
        # set company_dir as Fuel Invoices document type dir; prevents new dirs from being generated in bot script's working dir.
        company_dir = doc_type_abbrv_to_doc_type_subdir_map['INV']

    # Get today's date
    # today = datetime.strptime(datetime.today().strftime('%m-%d-%y'), '%m-%d-%y')  # @today
    today = datetime.strptime('08-31-23', '%m-%d-%y')  # testing purposes for `today` as `datetime`


    current_year = today.strftime('%Y')
    next_month = (today.replace(day=1) + timedelta(days=32)).replace(day=1).strftime('%m-%b')
    next_year = str(int(current_year) + 1) if next_month == '01-Jan' else current_year

    # If it's December, create the next year's directory and the next month's directory inside it
    if next_month == '01-Jan':
        os.makedirs(os.path.join(company_dir, next_year, next_month), exist_ok=True)

    else:  # If not December, just create the next month's directory inside the current year's directory
        os.makedirs(os.path.join(company_dir, current_year, next_month), exist_ok=True)

def cur_month_and_year_from_today():
    """
    Helper function to calculate current month and current year relative to today's date
    :return: Tuple(cur_month, cur_yr)
    """
    # today = datetime.today().strftime('%m-%d-%y')  # @today # todo: turn filesystem_manager.py into OOP to be able to `self.today` ?
    today = '08-31-23'

    current_month = datetime.strptime(today, '%m-%d-%y').strftime('%m-%b')
    current_year = datetime.strptime(today, '%m-%d-%y').strftime('%Y')

    return current_month, current_year

# @dev: renamed `get_root_directory` to `get_doc_type_dir`
# TODO: rename func and associated vars as it only returns type of document in full `Credit Credits`, not the directory up to doc_type as suggested `K:/DTN Reports/Credit Cards`
def get_doc_type_dir(doc_type):
    """
    Given a file prefix, it unpacks the root_directory mapping to return doc_type matching root directory aka the document type directory path
    :param doc_type:
    :return: str | None
    """
    for key, value in doc_type_abbrv_to_doc_type_subdir_map.items():
        if (isinstance(key, tuple) and doc_type in key) or key == doc_type:
            return value
    return None

def create_and_return_directory_path(doc_type_dir, current_year, current_month):
    """
    Given the root dir (aka document type dir), cur_yr, cur_month,\n
    it returns the final output path `month_dir` which is constructed appropriately based on current date
    :param doc_type_dir:
    :param current_year:
    :param current_month:
    :return: `month_dir` final output path to save PDFs to
    """
    year_dir = os.path.join(doc_type_dir, current_year)
    create_directory(year_dir)

    month_dir = os.path.join(year_dir, current_month)
    create_directory(month_dir)

    return month_dir

def construct_month_dir_from_doc_type(doc_type, company_id=None, company_dir=None):
    """
    Given the doc_type as minimum param, it returns the constructed final output path\ndepending on document type
    :param doc_type:
    :param company_id:
    :param company_dir:
    :return:
    """
    # Extract month and year from helper
    current_month, current_year = cur_month_and_year_from_today()

    # Determine root directory; #todo: rename var to doc_type_full ? b/c not a directory!
    doc_type_dir = get_doc_type_dir(doc_type)

    # If root directory not found, raise exception
    # todo: update as it is no longer a root directory, just document type in full aka `Fuel Invoices`
    if not doc_type_dir:
        raise ValueError(f"No root directory found for document type '{doc_type}'")

    # Handle EFT and CMB cases and non-exxon CCM files
    if (doc_type == 'EFT' or doc_type == 'CMB' or doc_type == 'CCM') and company_id is None and company_dir:
        doc_type_dir = company_dir # todo: change var name;; doesn't make sense to say that company directory is now doc type directory. if anything, it is now the new "root" directory /doc_type/company; NOTE: called the same var to only have a single return instead of having three separate returns

    # If a company_id was provided, update root directory to include company subdirectory; CCM or LRD
    elif doc_type_dir and company_id:
        company_directory = company_id_to_company_subdir_map.get(company_id, '')
        doc_type_dir = os.path.join(doc_type_dir, company_directory)

    # Create and return path to the relevant year and month directories
    # @dev: for INV doc_type, it only needs to return `Fuel Invoices/YYYY/MM-MMM`
    return create_and_return_directory_path(doc_type_dir, current_year, current_month)


def construct_month_dir_from_company_dir(company_dir):

    # Extract cur_yr and cur_month
    cur_month, cur_yr = cur_month_and_year_from_today()

    # Construct month directory
    month_dir = create_and_return_directory_path(company_dir, cur_yr, cur_month)

    return month_dir


