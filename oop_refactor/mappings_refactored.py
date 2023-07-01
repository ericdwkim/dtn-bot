import os

# First, define the common parts of the paths
base_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports'

# Define the mapping from company id to company directory
company_id_to_subdir_mapping = {
    '10006': 'VALERO [10006]',
    '10005': 'EXXONMOBIL [10005]',
    # More companies here...
}

# Define the mapping from document type to its respective directory under the base directory
doc_type_to_subdir_mapping = {
    ('CCM', 'LRD'): 'Credit Cards',
    'EFT': 'Fuel Drafts',
    'INV': 'Fuel Invoices',
}

# Now you can create a mapping of document type to company ID to file path
file_path_mappings = {
    doc_type: {
        company_id: os.path.join(base_dir, subdir, company_dir)
        for company_id, company_dir in company_id_to_subdir_mapping.items()
    }
    for doc_type, subdir in doc_type_to_subdir_mapping.items()
}

# Other important file paths and constants
other_file_paths = {
    'download_dir': r'/Users/ekim/Downloads',
    # 'dest_dir_invoices': os.path.join(base_dir, 'Fuel Invoices'),
    'keyword_in_dl_file_name': 'messages'
}

company_names = ['VALERO', 'CONCORD FIRST DATA RETRIEVAL', 'EXXONMOBIL', 'U.S. OIL COMPANY', 'DK Trading & Supply',
                 'CVR SUPPLY & TRADING, LLC']

regex_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}
