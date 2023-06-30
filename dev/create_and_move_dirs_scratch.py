import os
import datetime
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

# file_prefix INV is only needed for conditional logic. it is not used for actual file renaming
root_directory_mapping = {
    ('CCM-\s*\d+', 'LRD-\s*\d+'): r'K:/DTN Reports/Credit Cards/',
    'EFT-\s*\d+': r'K:/DTN Reports/Fuel Drafts/',
    'INV': r'K:/DTN Reports/Fuel Invoices/',
}


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


def calculate_directory_path(file_prefix, company_id, last_day_of_month):
    today = datetime.date.today()
    current_month = today.strftime('%m-%b')
    current_year = today.strftime('%Y')



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
        company_directory = company_id_to_subdir_mapping.get(company_id, '')  # Use the mapping to get company directory
        current_directory = os.path.join(root_directory, company_directory)

        month_dir = os.path.join(current_directory, current_month)
        year_dir = os.path.join(current_directory, current_year)

        # Create year and month directories if they don't exist.
        month_dir = create_directory(month_dir)
        if last_day_of_month:
            # If it's the last day of the month, move the month to the year folder and create a new month folder.
            move_directory_to_another(month_dir, year_dir)
            next_month = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1).strftime('%m-%b')
            month_dir = create_directory(os.path.join(current_directory, next_month))
            if last_day_of_month:
                # If it's the last day of the month, move the month to the year folder.
                move_directory_to_another(month_dir, year_dir)
                next_month = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1).strftime('%m-%b')
                if next_month == '01-Jan':
                    # If it's January, create the next year folder.
                    create_directory(os.path.join(current_directory, str(int(current_year) + 1)))
                # Always create the directory for next_month, whether it's January or not.
                month_dir = create_directory(os.path.join(current_directory, next_month))

        # This is the directory to save the file to.
        return month_dir

    # Return None if no appropriate directory could be found.
    return None


def create_and_save_pdf(pages, new_file_name, file_prefix, company_name):
    try:
        new_pdf = pikepdf.Pdf.new()
        new_pdf.pages.extend(pages)

        last_day_of_month = is_last_day_of_month()
        destination_dir = calculate_directory_path(file_prefix, company_name, last_day_of_month)
        dest_dir_with_new_file_name = os.path.join(destination_dir, new_file_name)

        new_pdf.save(dest_dir_with_new_file_name)
        return True
    except Exception as e:
        print(f"Error occurred while creating and saving PDF: {str(e)}")
        return False


def save_merged_pdf(file_prefix, merged_pdf, total_amount_sum, company_name):
    today = datetime.date.today().strftime('%m-%d-%y')
    if file_prefix == 'CCM':
        new_file_name = f'{file_prefix}-{today}-{total_amount_sum}.pdf'
    else:  # LRD
        new_file_name = f'{today}-Loyalty.pdf'

    last_day_of_month = is_last_day_of_month()
    directory = calculate_directory_path(file_prefix, company_name, last_day_of_month)
    output_path = os.path.join(directory, new_file_name)

    try:
        merged_pdf.save(output_path)
        merged_pdf.close()
        print(f'{file_prefix} PDFs have been merged, renamed "{new_file_name}" and saved to: {output_path}')
        return True
    except Exception:
        return False
