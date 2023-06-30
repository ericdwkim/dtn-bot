import os
import datetime

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

def is_last_day_of_month():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow.day == 1

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def calculate_directory_path(file_prefix, company_id, filename, doc_type_abbrv_to_doc_type_map, company_id_to_company_subdir_map):
    print(f'Calculating directory path..............')
    # Extract the date from the filename
    # TODO: toggle this back on after testing
    filename_date = re.search(r'\d{2}-\d{2}-\d{2}', filename)
    # filename_date = datetime.date(2023, 12, 31)
    if filename_date:
        filename_date = datetime.datetime.strptime(filename_date.group(), '%m-%d-%y')
    else:
        return None  # Return None if date cannot be extracted from filename

    current_month = filename_date.strftime('%m-%b')
    current_year = filename_date.strftime('%Y')

    root_directory = None
    for key, value in doc_type_abbrv_to_doc_type_map.items():
        if isinstance(key, tuple):
            if file_prefix in key:
                root_directory = value
                break
        elif key == file_prefix:
            root_directory = value
            break

    if root_directory:
        company_directory = company_id_to_company_subdir_map.get(company_id, '')
        current_directory = os.path.join(root_directory, company_directory)
        year_dir = os.path.join(current_directory, current_year)

        create_directory(year_dir)  # This will not do anything if the directory already exists.

        month_dir = os.path.join(year_dir, current_month)
        month_dir = create_directory(month_dir)  # Create the month directory

        return month_dir

    # Return None if no appropriate directory could be found.
    return None

# TODO: wrap is_last_day_of_month() with this function since this operation should only be done if is_last_day_of_month() returns True
def end_of_month_operations(directory, filename):
    print(f'Today is the last day of the month\nConducting end of month operations.............')
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

