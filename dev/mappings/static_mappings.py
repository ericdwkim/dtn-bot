# TODO: STATIC MAPPING OF ALL COMPANIES THAT RETRIEVE PDFS FROM WEB APP FOR THE MONTH OF JULY ONLY

# Directory paths
dest_dir_invoices = r'K:/DTN Reports/Fuel Invoices/6-June'
keyword_in_dl_file_name = 'messages'
download_dir = r'/Users/cgonzales/Downloads'

company_names = ['VALERO', 'CONCORD FIRST DATA RETRIEVAL', 'EXXONMOBIL', 'U.S. OIL COMPANY', 'DK Trading & Supply',
                 'CVR SUPPLY & TRADING, LLC']

regex_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}

# Mapping for company name to Fuel Drafts subdir full path
company_name_to_subdir_full_path_mapping_fuel_drafts = {
    'COFFEYVILLE': r'K:/DTN Reports/Fuel Drafts/COFFEYVILLE [10482]/7-July',
    'FRONTIER': r'K:/DTN Reports/Fuel Drafts/FRONTIER [10351]/7-July',
    'FUEL MASTERS': r'K:/DTN Reports/Fuel Drafts/FUEL MASTERS [10350]/7-July',
    'JUNIPER': r'K:/DTN Reports/Fuel Drafts/JUNIPER [11465]/7-July',
    'LA LOMITA': r'K:/DTN Reports/Fuel Drafts/LA LOMITA [12123]/7-July',
    'MANSFIELD OIL': r'K:/DTN Reports/Fuel Drafts/MANSFIELD OIL [11480]/7-July',
    'MOTIVA': r'K:/DTN Reports/Fuel Drafts/MOTIVA [10420]/7-July',
    'OFFEN PETROLEUM': r'K:/DTN Reports/Fuel Drafts/OFFEN PETROLEUM [12170]/7-July',
    'PHILLIPS': r'K:/DTN Reports/Fuel Drafts/PHILLIPS [10007]/7-July',
    'SEIFS': r'K:/DTN Reports/Fuel Drafts/SEIFS [11293]/7-July',
    'SUNOCO': r'K:/DTN Reports/Fuel Drafts/SUNOCO [11613]/7-July',
    'TTE': r'K:/DTN Reports/Fuel Drafts/TEXAS TRANSEASTERN [10280]/7-July', # TEXAS TRANSEASTERN
    'WINTERS OIL': r'K:/DTN Reports/Fuel Drafts/WINTERS OIL [10778]/7-July',
    'CVR SUPPLY & TRADING, LLC': r'K:/DTN Reports/Fuel Drafts/CVR Supply & Trading 12351/7-July',
    'EXXONMOBIL': r'K:/DTN Reports/Fuel Drafts/EXXONMOBIL [10005]/7-July',
    'U.S. OIL COMPANY': r'K:/DTN Reports/Fuel Drafts/U S VENTURE - U S OIL COMPANY [12262]/7-July',
    'VALERO': r'K:/DTN Reports/Fuel Drafts/VALERO [10006]/7-July',
    'DK Trading & Supply': r'K:/DTN Reports/Fuel Drafts/DK TRADING [12293]/7-July'
}

# Mapping for company name to Credit Cards subdir full path
company_name_to_subdir_full_path_mapping_credit_cards = {

    'VALERO': r'K:/DTN Reports/Credit Cards/Valero (10006)/7-July',

    'CONCORD FIRST DATA RETRIEVAL': r'K:/DTN Reports/Credit Cards/First Data/7-July',

    'EXXONMOBIL': r'K:/DTN Reports/Credit Cards/EXXONMOBIL (10005)/7-July',

    'P66': r'K:/DTN Reports/Credit Cards/P66/7-July'

}



