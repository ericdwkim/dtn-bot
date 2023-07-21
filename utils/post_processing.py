import os
import re
import datetime
import pikepdf
import shutil
from .mappings import company_id_to_company_subdir_map, root_directory_mapping

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


def extract_ccm_data(pdf_file):
    """
    Extracts CCM relevant data from List of tuples with target data
    :param pdf_file:
    :return:
    """
    filename = os.path.basename(pdf_file)
    match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', filename)
    if match:
        regex_num = int(match.group(1))
        total_amount = float(match.group(2).replace(',', ''))
        return regex_num, total_amount
    return None, None


def extract_lrd_data(pdf_file):
    """
    Extracts LRD relevant data from list of tuples
    :param pdf_file:
    :return:
    """
    match = re.match(r'LRD-(\d+)-.*\.pdf', pdf_file)
    if match:
        regex_num = match.group(1)
        return regex_num, None
    return None, None


def extract_pdf_data(company_dir):
    """
    Extracts target data from filenames for calculation for post-processing
    :param company_dir: path to company name directory
    :return: Tuple (List, Int, List) where each List contains tuples of pre-extracted data relevant for CCM and LRD, respectively.
    """
    today = datetime.today().strftime('%m-%d-%y')
    pdf_files = [f for f in os.listdir(company_dir) if f.endswith('.pdf')]
    print(f'************************ pdf_files ******************** : {pdf_files}\n')
    pdf_data_ccm = []
    pdf_data_lrd = []
    total_amount = 0.00
    for pdf_file in pdf_files:
        if pdf_file.startswith('CCM'):
            regex_num_ccm, amount = extract_ccm_data(pdf_file)
            total_amount += amount
            total_amount = round(total_amount, 2)  # Round to two decimal places
            pdf_data_ccm.append((regex_num_ccm, today, total_amount, os.path.join(company_dir, pdf_file)))
        elif pdf_file.startswith('LRD'):
            regex_num_lrd, _ = extract_lrd_data(pdf_file)
            pdf_data_lrd.append((regex_num_lrd, today, _, os.path.join(company_dir, pdf_file)))
    pdf_data_ccm.sort(key=lambda x: x[0])
    print(f'*********************************** pdf_data_ccm {pdf_data_ccm}\n')
    pdf_data_lrd.sort(key=lambda x: x[0])
    print(f'*********************************** pdf_data_lrd {pdf_data_lrd}\n')

    return pdf_data_ccm, total_amount, pdf_data_lrd
def check_file_exists(output_path):
    """
    :param output_path:
    :return: bool
    """
    file_path = os.path.join(output_path)
    return os.path.isfile(file_path)

def is_last_day_of_month():
    """
    Relative to today's date, it checks if tomorrow's date would be the start of a new month,\n
    if so, then it will return True indicating that today is the last day of the month
    :return: bool
    """
    today = datetime.date.today()

    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow.day == 1

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

def create_directory(directory):
    """
    Checks if `directory` path exists, if not, it creates `directory`
    :param directory: year or month directory
    :return: Any
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


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
    today = datetime.datetime.strptime(datetime.date.today().strftime('%m-%d-%y'), '%m-%d-%y')

    current_year = today.strftime('%Y')
    next_month = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1).strftime('%m-%b')
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
    today = datetime.today().strftime('%m-%d-%y')
    current_month = datetime.datetime.strptime(today, '%m-%d-%y').strftime('%m-%b')
    current_year = datetime.datetime.strptime(today, '%m-%d-%y').strftime('%Y')

    return current_month, current_year

def get_root_directory(file_prefix):
    """
    Given a file prefix, it unpacks the root_directory mapping to return file_prefix matching root directory aka the document type directory path
    :param file_prefix:
    :return: str | None
    """
    for key, value in root_directory_mapping.items():
        if (isinstance(key, tuple) and file_prefix in key) or key == file_prefix:
            return value
    return None


def create_and_return_directory_path(root_directory, current_year, current_month):
    """
    Given the root dir (aka document type dir), cur_yr, cur_month,\n
    it returns the final output path `month_dir` which is constructed appropriately based on current date
    :param root_directory:
    :param current_year:
    :param current_month:
    :return: `month_dir` final output path to save PDFs to
    """
    year_dir = os.path.join(root_directory, current_year)
    create_directory(year_dir)

    month_dir = os.path.join(year_dir, current_month)
    create_directory(month_dir)

    return month_dir
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

def merge_pdfs(pdf_data):
    """
    Merges PDFs by fetching 4th element in tuple `file_path` by looping, opening each file_path\nand creating them as pikePDF pages to combine and merge them all into a single PDF object
    :param pdf_data:
    :return: `merged_pdf` a pikePDF object | None
    """
    merged_pdf = pikepdf.Pdf.new()
    for _, _, _, file_path in pdf_data:
        try:
            pdf = pikepdf.Pdf.open(file_path)
            merged_pdf.pages.extend(pdf.pages)
        except pikepdf.PdfError:
            return False
    return merged_pdf



def save_merged_pdf(file_prefix, merged_pdf, total_amount_sum, company_id):
    """
    Saves pre-merged pike PDF object with constructed filename dependent on doc type with provided target data.
    :param file_prefix: CCM or LRD ; only these for post-processing
    :param merged_pdf:
    :param total_amount_sum:
    :param company_id:
    :return: Bool
    """
    today = datetime.today().strftime('%m-%d-%y')
    if file_prefix == 'CCM':
        new_file_name = f'{file_prefix}-{today}-{total_amount_sum}.pdf'
    else:
        new_file_name = f'{today}-Loyalty.pdf'

    month_directory = calculate_directory_path(file_prefix, company_id)
    output_path = os.path.join(month_directory, new_file_name)

    try:
        merged_pdf.save(output_path)
        merged_pdf.close()
        print(f'{file_prefix} PDFs have been merged, renamed "{new_file_name}" and saved to: {output_path}')
        return True
    except Exception:
        return False


def merge_rename_and_summate(company_dir):
    """
    Main post-processing wrapper function. Accounts for end of month operations if last day of the month.
    :param company_dir: path to company name directory
    :return: None
    """
    pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = extract_pdf_data(company_dir)
    print(
        f'********************* pdf_data_ccm: {pdf_data_ccm}\n total_amount_sum_ccm: {total_amount_sum_ccm}\n *********** pdf_data_lrd {pdf_data_lrd}  ')

    merged_pdf_ccm = merge_pdfs(pdf_data_ccm)
    merged_ccm_pdf_is_saved = save_merged_pdf('CCM', merged_pdf_ccm, total_amount_sum_ccm, '10005')
    print(f'merged_pdf_ccm / merged_ccm_pdf_is_saved: {merged_pdf_ccm} / {merged_ccm_pdf_is_saved}')
    # Clean up pre-merged PDFs in EXXON company_dir; loops through file_path (4th elem in tuple) to delete
    cleanup_files(pdf_data_ccm)
    # PDFs were merged, saved w/ new filename. If it is currently the last day of the month, then perform end of month filesystem management
    if merged_pdf_ccm and merged_ccm_pdf_is_saved and is_last_day_of_month():
        end_of_month_operations(company_dir)

    merged_pdf_lrd = merge_pdfs(pdf_data_lrd)
    merged_lrd_pdf_is_saved = save_merged_pdf('LRD', merged_pdf_lrd, None, '10005')
    # Clean up pre-merged PDFs in EXXON company_dir; loops through file_path (4th elem in tuple) to delete
    cleanup_files(pdf_data_lrd)
    # PDFs were merged, saved w/ new filename. If it is currently the last day of the month, then perform end of month filesystem management
    if merged_pdf_lrd and merged_lrd_pdf_is_saved and is_last_day_of_month():
        end_of_month_operations(company_dir)
