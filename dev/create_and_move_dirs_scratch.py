import os
import datetime
import shutil

# Some global variable for the root directory.
root_directory = r'K:/DTN Reports'

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


def calculate_directory_path(file_prefix, company_name, last_day_of_month):
    today = datetime.date.today()
    current_month = today.strftime('%m-%b')
    current_year = today.strftime('%Y')

    if file_prefix == 'CCM':
        base_dir = os.path.join(root_directory, 'Credit Cards', company_name)
    elif file_prefix == 'ETF':
        base_dir = os.path.join(root_directory, 'Fuel Drafts', company_name)
    else:  # For Fuel Invoices
        base_dir = root_directory

    month_dir = os.path.join(base_dir, current_month)
    year_dir = os.path.join(base_dir, current_year)

    # Create year and month directories if they don't exist.
    month_dir = create_directory(month_dir)
    if last_day_of_month:
        # If it's the last day of the month, move the month to the year folder and create a new month folder.
        move_directory_to_another(month_dir, year_dir)
        next_month = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1).strftime('%m-%b')
        month_dir = create_directory(os.path.join(base_dir, next_month))
        if next_month == '01-Jan':
            # If it's January, create the next year folder.
            create_directory(os.path.join(base_dir, str(int(current_year) + 1)))

    return month_dir


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
