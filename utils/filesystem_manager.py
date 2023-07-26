import os
from datetime import datetime, timedelta
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


# TODO: if this fn returns true, then just call end_of_month_operations() ?
def is_last_day_of_month():
    """
    Relative to today's date, it checks if tomorrow's date would be the start of a new month,\n
    if so, then it will return True indicating that today is the last day of the month
    :return: bool
    """
    today = datetime.today()  # @today
    # today = datetime.strptime('07-23-23', '%m-%d-%y')  # testing purposes for `today` as `datetime`


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


def calculate_directory_path(file_prefix, company_id=None, company_dir=None):
    """
    Given the file_prefix as minimum param, it returns the constructed final output path\ndepending on document type
    :param file_prefix:
    :param company_id:
    :param company_dir:
    :return:
    """
    # Extract month and year from helper
    current_month, current_year = cur_month_and_year_from_today()

    # Determine root directory
    root_directory = get_root_directory(file_prefix)

    # If root directory not found, raise exception
    if not root_directory:
        raise ValueError(f"No root directory found for file prefix '{file_prefix}'")

    # Handle EFT and CMB cases and non-exxon CCM files
    if (file_prefix == 'EFT' or file_prefix == 'CMB' or file_prefix == 'CCM') and company_id is None and company_dir:
        root_directory = company_dir

    # If a company_id was provided, update root directory to include company subdirectory; CCM or LRD
    elif root_directory and company_id:
        company_directory = company_id_to_company_subdir_map.get(company_id, '')
        root_directory = os.path.join(root_directory, company_directory)

    # Create and return path to the relevant year and month directories
    return create_and_return_directory_path(root_directory, current_year, current_month)

# TODO: wrap is_last_day_of_month() with this function since this operation should only be done if is_last_day_of_month() returns True
def end_of_month_operations(company_dir=None):
    """
    Creates the new month and new year directories if it is the last day of the month
    :param company_dir: defaulted to None
    :return: None
    """
    # Handles INV case
    if company_dir is None:
        # set company_dir as Fuel Invoices document type dir; prevents new dirs from being generated in bot script's working dir.
        company_dir = root_directory_mapping['INV']

    # Get today's date
    today = datetime.strptime(datetime.today().strftime('%m-%d-%y'), '%m-%d-%y')  # @today
    # today = datetime.strptime('07-23-23', '%m-%d-%y')  # testing purposes for `today` as `datetime`


    current_year = today.strftime('%Y')
    next_month = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1).strftime('%m-%b')
    next_year = str(int(current_year) + 1) if next_month == '01-Jan' else current_year

    # If it's December, create the next year's directory and the next month's directory inside it
    if next_month == '01-Jan':
        os.makedirs(os.path.join(company_dir, next_year, next_month), exist_ok=True)

    else:  # If not December, just create the next month's directory inside the current year's directory
        os.makedirs(os.path.join(company_dir, current_year, next_month), exist_ok=True)
