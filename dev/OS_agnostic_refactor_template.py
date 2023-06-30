import os
import platform

# Determine the operating system
os_type = platform.system()

# Set the base directory according to the operating system
if os_type == 'Windows':
    regex_pattern_to_document_type_root_directory_mapping = {
        ('CCM', 'LRD'): r'K:/DTN Reports/Credit Cards/',
        'EFT': r'K:/DTN Reports/Fuel Drafts/',
        'INV': r'K:/DTN Reports/Fuel Invoices/',
    }
    download_dir = r'/Users/cgonzales/Downloads'
else:  # Assume Unix-based system (like MacOS or Linux)
    regex_pattern_to_document_type_root_directory_mapping = {
        ('CCM', 'LRD'): r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/',
        'EFT': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/',
        'INV': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/',
    }
    download_dir = r'/Users/ekim/Downloads'

company_id_to_subdir_mapping = {
    '10482': 'COFFEYVILLE [10482]',
    '12351': 'CVR Supply & Trading 12351',
    # rest of the companies and their IDs
}

# Now you can create a mapping of regex pattern to document type to company ID to file path
file_path_mappings = {
    regex_pattern: {
        company_id: os.path.join(root_dir, subdir)
        for company_id, subdir in company_id_to_subdir_mapping.items()
    }
    for regex_pattern, root_dir in regex_pattern_to_document_type_root_directory_mapping.items()
}

# Other important file paths
other_file_paths = {
    'download_dir': download_dir
}


# Suppose you have a function that requires a file path
def process_data(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    # do something with data...
    pass

# Call this function with the correct file path, regardless of the operating system.
regex_pattern = 'EFT'
company_id = '12351'
file_path = file_path_mappings[regex_pattern][company_id]
process_data(file_path)
