import os
import shutil
from datetime import datetime


def move_month_dir_to_year(parent_directory: str):
    # Define the current month and year in the appropriate format
    current_year = datetime.now().strftime('%Y')
    current_month = datetime.now().strftime('%m-%b')

    # Check if the month and year directories exist
    month_directory_path = os.path.join(parent_directory, current_month)
    year_directory_path = os.path.join(parent_directory, current_year)

    if os.path.exists(month_directory_path) and os.path.exists(year_directory_path):
        # If both exist, move the month's directory to the year's directory
        shutil.move(month_directory_path, year_directory_path)


def check_company_dirs(parent_directory: str):
    # List the names of the entries in the parent_directory
    entries = os.listdir(parent_directory)

    # Loop over the entries
    for entry in entries:
        # Define the current entry directory path
        current_entry_directory = os.path.join(parent_directory, entry)

        # If the entry is a directory
        if os.path.isdir(current_entry_directory):
            # Perform the move operation
            move_month_dir_to_year(current_entry_directory)


# Define the directories to check
directories_to_check = ['/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices', '/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts', '/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices']

# For each directory in the list of directories to check, execute the move_month_dir_to_year function
for directory in directories_to_check:
    # List the names of the entries in the directory
    entries = os.listdir(directory)

    # Loop over the entries
    for entry in entries:
        # Define the current entry directory path
        current_entry_directory = os.path.join(directory, entry)

        # If the entry is a directory
        if os.path.isdir(current_entry_directory):
            # Check the company directories
            check_company_dirs(current_entry_directory)
