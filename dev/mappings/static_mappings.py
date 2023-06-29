# Directory paths
dest_dir_invoices = r'K:/DTN Reports/Fuel Invoices/5-May'
keyword_in_dl_file_name = 'messages'  # downloaded file is defaulted to filename `messages.pdf` on mac
download_dir = r'/Users/cgonzales/Downloads'

company_names = ['VALERO', 'CONCORD FIRST DATA RETRIEVAL', 'EXXONMOBIL', 'U.S. OIL COMPANY', 'DK Trading & Supply',
                 'CVR SUPPLY & TRADING, LLC']

regex_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}

# Mapping for company name to Fuel Drafts subdir full path
company_name_to_subdir_full_path_mapping_fuel_drafts = {
    'CVR SUPPLY & TRADING, LLC': r'K:/DTN Reports/Fuel Drafts/CVR Supply & Trading 12351',

    'EXXONMOBIL': r'K:/DTN Reports/Fuel Drafts/EXXONMOBIL (10005)',

    'U.S. OIL COMPANY': r'K:/DTN Reports/Fuel Drafts/U S VENTURE - U S OIL COMPANY [12262]',

    'VALERO': r'K:/DTN Reports/Fuel Drafts/VALERO [10006]',

    'DK Trading & Supply': r'K:/DTN Reports/Fuel Drafts/DK TRADING [12293]'
}

# Mapping for company name to Credit Cards subdir full path
company_name_to_subdir_full_path_mapping_credit_cards = {

    'VALERO': r'K:/DTN Reports/Credit Cards/Valero (10006)',

    'CONCORD FIRST DATA RETRIEVAL': r'K:/DTN Reports/Credit Cards/First Data',

    'EXXONMOBIL': r'K:/DTN Reports/Credit Cards/EXXONMOBIL (10005)'

}
