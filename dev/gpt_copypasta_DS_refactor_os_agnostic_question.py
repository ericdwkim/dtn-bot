"""

"""

"""

Given the following mappings, how to best create a config mapping to encapsulate both filepaths to allow for OS agnostic `data_file` to be passed in as filepath parameter in functions that process, move, save, or delete based on provided filepath parameter.

1. Mapping for Mac for "Fuel Drafts" document type

# Mapping for company name to Fuel Drafts subdir full path
company_name_to_subdir_full_path_mapping_fuel_drafts = {
    'CVR SUPPLY & TRADING, LLC': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/CVR Supply & Trading 12351',

    'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/EXXONMOBIL (10005)',

    'U.S. OIL COMPANY': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/U S VENTURE - U S OIL COMPANY [12262]',

    'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/VALERO [10006]',

    'DK Trading & Supply': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/DK TRADING [12293]'
    
    # rest of the companies and their filepaths
}

2. Mapping for Mac for "Credit Cards" document type

# Mapping for company name to Credit Cards subdir full path
company_name_to_subdir_full_path_mapping_credit_cards = {

    'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/Valero (10006)',

    'CONCORD FIRST DATA RETRIEVAL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/First Data',

    'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)'

}


3. Static variable on Mac for "Fuel Invoices" document type. No mapping was created for this as there was no need to separate by company name.

destination_directory_filepath_for_fuel_invoices = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/


-------------------------------------------

1. Mapping for Windows for "Fuel Drafts" document type

# Mapping for company name to Fuel Drafts subdir full path
company_name_to_subdir_full_path_mapping_fuel_drafts = {
   
    'CVR SUPPLY & TRADING, LLC': r'K:/DTN Reports/Fuel Drafts/CVR Supply & Trading 12351/7-July',
    'EXXONMOBIL': r'K:/DTN Reports/Fuel Drafts/EXXONMOBIL [10005]/7-July',
    'U.S. OIL COMPANY': r'K:/DTN Reports/Fuel Drafts/U S VENTURE - U S OIL COMPANY [12262]/7-July',
    'VALERO': r'K:/DTN Reports/Fuel Drafts/VALERO [10006]/7-July',
    'DK Trading & Supply': r'K:/DTN Reports/Fuel Drafts/DK TRADING [12293]/7-July'
    
    # rest of the companies and their filepaths

}


2. Mapping for Windows for "Credit Cards" document type

# Mapping for company name to Credit Cards subdir full path
company_name_to_subdir_full_path_mapping_credit_cards = {

    'VALERO': r'K:/DTN Reports/Credit Cards/Valero (10006)/7-July',

    'CONCORD FIRST DATA RETRIEVAL': r'K:/DTN Reports/Credit Cards/First Data/7-July',

    'EXXONMOBIL': r'K:/DTN Reports/Credit Cards/EXXONMOBIL (10005)/7-July',

    'P66': r'K:/DTN Reports/Credit Cards/P66/7-July'

}

3. Static variable for Windows for "Fuel Invoices" document type. 

destination_directory_filepath_for_fuel_invoices = r'K:/DTN Reports/Fuel Invoices/6-June'

----------------------------------------------------------
Miscellaneous filepaths that are frequently used in current codebase that may/may not be better to include as part of this new schema:

download_directory_path_windows = download_dir = r'/Users/cgonzales/Downloads'

download_directory_path_mac = directory =r'/Users/ekim/Downloads'
-----------------------------------------------------------
Other important data structures frequently used in current codebase that may/may not be better to include as part of this new schema:

company_names = ['VALERO', 'CONCORD FIRST DATA RETRIEVAL', 'EXXONMOBIL', 'U.S. OIL COMPANY', 'DK Trading & Supply',
                 'CVR SUPPLY & TRADING, LLC']

regex_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}

--------------------------------------------------------
Template for configuration file to achieve OS agnostic data structure
```
import os
import platform

# A configuration dictionary to store paths
config = {
    "data_dir": "",
    "log_dir": "",
    "temp_dir": ""
}


# Get the current operating system
os_type = platform.system()
# print(os_type) # "Darwin" was printed on Mac. "Windows was printed out on Windows machine. 


if os_type == 'Windows':
    config["data_dir"] = "C:\\path\\to\\data\\dir"
    config["log_dir"] = "C:\\path\\to\\log\\dir"
    config["temp_dir"] = "C:\\path\\to\\temp\\dir"

else:  # Assume Unix-based system (like MacOS or Linux)
    config["data_dir"] = "/path/to/data/dir"
    config["log_dir"] = "/path/to/log/dir"
    config["temp_dir"] = "/path/to/temp/dir"


# Now you can use these paths in your code
data_file = os.path.join(config["data_dir"], "mydata.txt")

# Suppose you have a function that requires a file path
def process_data(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    # do something with data...
    pass

# You can now call this function with the correct file path,
# regardless of the operating system.
process_data(data_file)
```














"""


"""































"""