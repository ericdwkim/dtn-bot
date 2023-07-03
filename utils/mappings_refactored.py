# Mapping from company id to company directory
company_id_to_company_subdir_map = {
    '10482': 'COFFEYVILLE [10482]',
    '12351': 'CVR Supply & Trading [12351]',
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

# Mapping from document type to its respective directory under the root directory
doc_type_abbrv_to_doc_type_subdir_map = {
    'CCM': 'Credit Cards',
    'LRD': 'Credit Cards',
    'EFT': 'Fuel Drafts',
    'INV': 'Fuel Invoices',
}


# company_names = ['VALERO', 'CONCORD FIRST DATA RETRIEVAL', 'EXXONMOBIL', 'U.S. OIL COMPANY', 'DK Trading & Supply',
#                  'CVR SUPPLY & TRADING, LLC', 'COFFEYVILLE', 'FLINT HILLS', 'FRONTIER',  'FUEL MASTERS', 'JUNIPER', 'LA LOMITA', 'MANSFIELD OIL', 'MERITUM - PICO', 'MOTIVA', 'OFFEN PETROLEUM', 'PHILLIPS', 'SEIFS', 'SUNOCO', 'TEXAS TRANSEASTERN', 'WINTERS OIL']

regex_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}
