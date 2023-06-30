import os
import re
import datetime
import pikepdf
import shutil


company_id_to_subdir_mapping = {
    '10482': 'COFFEYVILLE [10482]',
    '12351': 'CVR Supply & Trading 12351',
    '12293': 'DK TRADING [12293]',
    '10005': 'EXXONMOBIL [10005]',
    '11177': 'FLINT HILLS [11177]',
    '10351': 'FRONTIER [10351]',
    '10350': 'FUEL MASTERS [10350]',
    '11465': 'JUNIPER [11465]',
    '12123': 'LA LOMITA [12123]',
    '11480': 'MANSFIELD OIL [11480]',
    '11096': 'MERITUM - PICO [11096]',
    '10420': 'MOTIVA [10420]',
    '12170': 'OFFEN PETROLEUM [12170]',
    '10007': 'PHILLIPS [10007]',
    '11293': 'SEIFS [11293]',
    '11613': 'SUNOCO [11613]',
    '10280': 'TEXAS TRANSEASTERN [10280]',
    '12262': 'U S VENTURE - U S OIL COMPANY [12262]',
    '10006': 'VALERO [10006]',
    '10778': 'WINTERS OIL [10778]',
}

def cleanup_files(pdf_data):
    """

    :param pdf_data:
    :return:
    """
    files_deleted = False
    for _, _, _, file_path in pdf_data:
        if os.path.exists(file_path):
            os.remove(file_path)
            files_deleted = True
    return files_deleted


def extract_ccm_data(pdf_file):
    filename = os.path.basename(pdf_file)
    match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', filename)
    if match:
        regex_num = int(match.group(1))
        total_amount = float(match.group(2).replace(',', ''))
        return regex_num, total_amount
    return None, None


def extract_lrd_data(pdf_file):
    match = re.match(r'LRD-(\d+)-.*\.pdf', pdf_file)
    if match:
        regex_num = match.group(1)
        return regex_num, None
    return None, None


def extract_pdf_data(directory):
    today = datetime.date.today().strftime('%m-%d-%y')
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    pdf_data_ccm = []
    pdf_data_lrd = []
    total_amount = 0.00
    for pdf_file in pdf_files:
        if pdf_file.startswith('CCM'):
            regex_num_ccm, amount = extract_ccm_data(pdf_file)
            total_amount += amount
            total_amount = round(total_amount, 2)  # Round to two decimal places
            pdf_data_ccm.append((regex_num_ccm, today, total_amount, os.path.join(directory, pdf_file)))
        elif pdf_file.startswith('LRD'):
            regex_num_lrd, _ = extract_lrd_data(pdf_file)
            pdf_data_lrd.append((regex_num_lrd, today, _, os.path.join(directory, pdf_file)))
    pdf_data_ccm.sort(key=lambda x: x[0])
    pdf_data_lrd.sort(key=lambda x: x[0])
    return pdf_data_ccm, total_amount, pdf_data_lrd

def check_file_exists(output_path):
    file_path = os.path.join(output_path)
    return os.path.isfile(file_path)
def is_last_day_of_month():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow.day == 1

def move_directory_to_another(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    shutil.move(src_dir, dst_dir)

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def end_of_month_operations(directory, filename):
    """
    Create the new month and year directories at the end of the month.
    """
    # Extract the date from the filename
    filename_date = re.search(r'\d{2}-\d{2}-\d{2}', filename)
    if filename_date:
        filename_date = datetime.datetime.strptime(filename_date.group(), '%m-%d-%y')
    else:
        return  # Return if date cannot be extracted from filename

    current_year = filename_date.strftime('%Y')
    next_month = (filename_date.replace(day=1) + datetime.timedelta(days=32)).replace(day=1).strftime('%m-%b')
    next_year = str(int(current_year) + 1) if next_month == '01-Jan' else current_year

    # If it's December, create the next year's directory and the next month's directory inside it
    if next_month == '01-Jan':
        os.makedirs(os.path.join(directory, next_year, next_month), exist_ok=True)
    else:  # If not December, just create the next month's directory inside the current year's directory
        os.makedirs(os.path.join(directory, current_year, next_month), exist_ok=True)


def calculate_directory_path(file_prefix, company_id, filename):
    # Extract the date from the filename
    # TODO: toggle this back on after testing
    # filename_date = re.search(r'\d{2}-\d{2}-\d{2}', filename)
    filename_date = datetime.date(2023, 12, 31)
    # if filename_date:
    #     filename_date = datetime.datetime.strptime(filename_date.group(), '%m-%d-%y')
    # else:
    #     return None  # Return None if date cannot be extracted from filename

    current_month = filename_date.strftime('%m-%b')
    current_year = filename_date.strftime('%Y')

    root_directory_mapping = {
        ('CCM', 'LRD'): r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/',
        'EFT': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/',
        'INV': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/',
    }
    root_directory = None
    for key, value in root_directory_mapping.items():
        if isinstance(key, tuple):
            if file_prefix in key:
                root_directory = value
                break
        elif key == file_prefix:
            root_directory = value
            break

    if root_directory:
        company_directory = company_id_to_subdir_mapping.get(company_id, '')
        current_directory = os.path.join(root_directory, company_directory)
        year_dir = os.path.join(current_directory, current_year)

        create_directory(year_dir)  # This will not do anything if the directory already exists.

        month_dir = os.path.join(year_dir, current_month)
        month_dir = create_directory(month_dir)  # Create the month directory

        return month_dir

    # Return None if no appropriate directory could be found.
    return None


def merge_pdfs(pdf_data):
    merged_pdf = pikepdf.Pdf.new()
    for _, _, _, file_path in pdf_data:
        try:
            pdf = pikepdf.Pdf.open(file_path)
            merged_pdf.pages.extend(pdf.pages)
        except pikepdf.PdfError:
            return False
    return merged_pdf



def save_merged_pdf(file_prefix, merged_pdf, total_amount_sum, company_id):
    # TODO: toggle this back on after testing
    today = datetime.date(2023, 12, 31).strftime('%m-%d-%y')
    # today = datetime.date.today().strftime('%m-%d-%y')
    if file_prefix == 'CCM':
        new_file_name = f'{file_prefix}-{today}-{total_amount_sum}.pdf'
    else:
        new_file_name = f'{today}-Loyalty.pdf'

    month_directory = calculate_directory_path(file_prefix, company_id, new_file_name)
    print(f'----------------------------------------- {month_directory} -----------------------------')
    output_path = os.path.join(month_directory, new_file_name)

    try:
        merged_pdf.save(output_path)
        merged_pdf.close()
        print(f'{file_prefix} PDFs have been merged, renamed "{new_file_name}" and saved to: {output_path}')
        return True, new_file_name
    except Exception:
        return False, None


def merge_rename_and_summate(directory):
    pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = extract_pdf_data(directory)

    merged_pdf_ccm = merge_pdfs(pdf_data_ccm)
    merged_ccm_pdf_is_saved, filename = save_merged_pdf('CCM', merged_pdf_ccm, total_amount_sum_ccm, '10005')
    print(f'merged_pdf_ccm / merged_ccm_pdf_is_saved: {merged_pdf_ccm} / {merged_ccm_pdf_is_saved}')
    # PDFs were merged, saved, and renamed with a new filename and it is currently the last day of the month, then perform end of month filesystem management
    if merged_pdf_ccm and merged_ccm_pdf_is_saved  and filename and is_last_day_of_month():

        end_of_month_operations(directory, filename)
        cleanup_files(pdf_data_ccm)

    # if it is not the last day
    else:
        # cleanup_files(pdf_data_ccm)
        print(f'dont delete plz')

    merged_pdf_lrd = merge_pdfs(pdf_data_lrd)
    merged_lrd_pdf_is_saved, filename = save_merged_pdf('LRD', merged_pdf_lrd, None, '10005')

    if merged_pdf_lrd and merged_lrd_pdf_is_saved and filename:

        end_of_month_operations(directory, filename)
        cleanup_files(pdf_data_lrd)

    else:
        cleanup_files(pdf_data_lrd)
        print(f'dont delete plz')
