import os
import re

import datetime
# lst = [1.263434, 2.7887773434, 2.232533434, 3.7897988434, 4.8565434, 6.37575434, 1.126444654654]
# total_amt = 0
# # print(total_amt)
#
#
# for num in lst:
#     total_amt += num
#
# total_amt = round(total_amt, 2)
# print(total_amt)
# print(type(total_amt))
# # print(total_amt)


# lst = [1.263434, 2.7887773434, 2.232533434, 3.7897988434, 4.8565434, 6.37575434, 1.126444654654]
# total_amt = 0
#
# for num in lst:
#     total_amt += num
#
# rounded_value = round(total_amt, 2)
# formatted_value = float("{:.2f}".format(rounded_value))
#
# print(formatted_value)
# print(type(formatted_value))

# from utils.post_processing import extract_ccm_data

directory =r'/Users/ekim/Downloads'
# file =r'/Users/ekim/Downloads/CCM-1234-06-28-23-1,234,567.89.pdf'


def extract_ccm_data(pdf_file):
    filename = os.path.basename(pdf_file)
    match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', filename)
    print(f'pdf_file: {filename}')
    if match:
        regex_num = int(match.group(1))
        total_amount = float(match.group(2).replace(',', ''))
        return regex_num, total_amount
    return None, None

# extract_ccm_data(file)





def someFunc(directory):
    today = datetime.date.today().strftime('%m-%d-%y')
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    print(f'directory: {directory}')
    pdf_data_ccm = []
    total_amount = 0.00
    for pdf_file in pdf_files:
        if pdf_file.startswith('CCM'):
            regex_num_ccm, amount = extract_ccm_data(pdf_file)
            print(f'amount: {amount}')
            total_amount += amount
            total_amount = round(total_amount, 2)  # Round to two decimal places
            total_amount = float("{:.2f}".format(total_amount)) # Include trailing zeros after decimal
            pdf_data_ccm.append((regex_num_ccm, today, total_amount, os.path.join(directory, pdf_file)))
            print(f'pdf_data_ccm: {pdf_data_ccm}')
            print(f'total_amount: {total_amount}')
    print(f'--------------total_amount: {total_amount}')
    return pdf_data_ccm, total_amount

someFunc(directory)
