# Directory paths
dest_dir_invoices = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/6-June'
keyword_in_dl_file_name = 'messages'  # downloaded file is defaulted to filename `messages.pdf` on mac
download_dir = r'/Users/ekim/Downloads'

company_names = ['VALERO', 'CONCORD FIRST DATA RETRIEVAL', 'EXXONMOBIL', 'U.S. OIL COMPANY', 'DK Trading & Supply',
                 'CVR SUPPLY & TRADING, LLC']

regex_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}

# Mapping for company name to Fuel Drafts subdir full path
company_name_to_subdir_full_path_mapping_fuel_drafts = {
    'CVR SUPPLY & TRADING, LLC': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/CVR Supply & Trading 12351',

    'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/EXXONMOBIL (10005)',

    'U.S. OIL COMPANY': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/U S VENTURE - U S OIL COMPANY [12262]',

    'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/VALERO [10006]',

    'DK Trading & Supply': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/DK TRADING [12293]',

    'CONCORD FIRST DATA RETRIEVAL': r'/Users/ekima/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/First Data',

}

# Mapping for company name to Credit Cards subdir full path
company_name_to_subdir_full_path_mapping_credit_cards = {

    'VALERO': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/Valero [10006]',

    'CONCORD FIRST DATA RETRIEVAL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/First Data',

    'EXXONMOBIL': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL [10005]',

    'U.S. OIL COMPANY': r'/Users/ekima/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/U S VENTURE - U S OIL COMPANY [12262]'

}


company_id_to_company_subdir_map = {
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

doc_type_abbrv_to_doc_type_dir_map = {
    ('CCM', 'LRD'): r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/',
    'EFT': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/',
    'INV': r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/',
}


