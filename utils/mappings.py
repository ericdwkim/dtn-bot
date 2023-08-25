# Mapping from company id to company directory
# @dev: last two are made up company_ids
company_id_to_company_subdir_map = {
    '10482': 'COFFEYVILLE [10482]',
    '12351': 'CVR SUPPLY & TRADING [12351]',
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
    '12262': 'U.S. OIL COMPANY [12262]',
    '10006': 'VALERO [10006]',
    '10778': 'WINTERS OIL [10778]',
    '11111': 'CONCORD FIRST DATA RETRIEVAL [11111]',
    '22222': 'P66 [22222]',
    '33333': 'GLOBAL COMPANIES LLC [33333]'

}

# Mapping from document type to its respective directory under the root directory
doc_type_short_to_doc_type_full_map = {
    ('CCM', 'LRD', 'CBK', 'RBK', 'CMB'): 'Credit Cards',
    'EFT': 'Fuel Drafts',
    'INV': 'Fuel Invoices',
}

# company_names = ['COFFEYVILLE', 'CVR SUPPLY & TRADING', 'DK TRADING', 'EXXONMOBIL', 'FLINT HILLS', 'FRONTIER', 'FUEL MASTERS',
#  'JUNIPER', 'LA LOMITA', 'MANSFIELD OIL', 'MERITUM - PICO', 'MOTIVA', 'OFFEN PETROLEUM', 'PHILLIPS', 'SEIFS', 'SUNOCO',
#  'TEXAS TRANSEASTERN', 'U.S. OIL COMPANY', 'VALERO', 'WINTERS OIL', 'CONCORD FIRST DATA RETRIEVAL', 'P66',
#  'GLOBAL COMPANIES LLC']


doc_type_patterns = {'EFT-\s*\d+', 'CMB-\s*\d+', 'CCM-\s*\d+', 'RTV-\s*\d+', 'CBK-\s*\d+', 'LRD-\s*\d+'}
