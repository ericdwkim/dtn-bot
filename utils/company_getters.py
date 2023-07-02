from utils.mappings_refactored import company_id_to_company_subdir_map


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
@classmethod
def get_company_id(company_name):
    for id, subdir in company_id_to_company_subdir_map.items():
        if company_name == subdir.split('[')[0].strip():
            return id
    return None
@classmethod
def get_company_name(page_text):

    if company_name in page_text:





    company_names = []
    for company_dir in company_id_to_company_subdir_map.values():
        # Slice the string to remove the company id and brackets
        company_name = company_dir.split('[')[0].strip()
        company_names.append(company_name)
    return company_names

