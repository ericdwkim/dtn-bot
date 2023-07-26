import os
import re
import datetime
import pikepdf
import shutil
from utils.filesystem_manager import end_of_month_operations, calculate_directory_path, is_last_day_of_month, cleanup_files



def extract_ccm_data(pdf_file):
    filename = os.path.basename(pdf_file)
    match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', filename)
    if match:
        doc_type_num = int(match.group(1))
        total_amount = float(match.group(2).replace(',', ''))
        return doc_type_num, total_amount
    return None, None


def extract_lrd_data(pdf_file):
    match = re.match(r'LRD-(\d+)-.*\.pdf', pdf_file)
    if match:
        doc_type_num = match.group(1)
        return doc_type_num, None
    return None, None


def extract_pdf_data(directory):
    today = datetime.date.today().strftime('%m-%d-%y')
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    pdf_data_ccm = []
    pdf_data_lrd = []
    total_amount = 0.00
    for pdf_file in pdf_files:
        if pdf_file.startswith('CCM'):
            doc_type_num_ccm, amount = extract_ccm_data(pdf_file)
            total_amount += amount
            total_amount = round(total_amount, 2)  # Round to two decimal places
            pdf_data_ccm.append((doc_type_num_ccm, today, total_amount, os.path.join(directory, pdf_file)))
        elif pdf_file.startswith('LRD'):
            doc_type_num_lrd, _ = extract_lrd_data(pdf_file)
            pdf_data_lrd.append((doc_type_num_lrd, today, _, os.path.join(directory, pdf_file)))
    pdf_data_ccm.sort(key=lambda x: x[0])
    pdf_data_lrd.sort(key=lambda x: x[0])
    return pdf_data_ccm, total_amount, pdf_data_lrd


def merge_pdfs(pdf_data):
    merged_pdf = pikepdf.Pdf.new()
    for _, _, _, file_path in pdf_data:
        try:
            pdf = pikepdf.Pdf.open(file_path)
            merged_pdf.pages.extend(pdf.pages)
        except pikepdf.PdfError:
            return False
    return merged_pdf



def save_merged_pdf(file_prefix, merged_pdf, total_amount_sum, company_id, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map):
    # TODO: toggle this back on after testing
    # today = datetime.date(2023, 12, 31).strftime('%m-%d-%y')
    today = datetime.date.today().strftime('%m-%d-%y')
    if file_prefix == 'CCM':
        new_file_name = f'{file_prefix}-{today}-{total_amount_sum}.pdf'
    else:
        new_file_name = f'{today}-Loyalty.pdf'

    month_directory = calculate_directory_path(file_prefix, company_id, new_file_name, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)
    print(f'----------------------------------------- {month_directory} -----------------------------')
    output_path = os.path.join(month_directory, new_file_name)

    try:
        merged_pdf.save(output_path)
        merged_pdf.close()
        print(f'{file_prefix} PDFs have been merged, renamed "{new_file_name}" and saved to: {output_path}')
        return True, new_file_name
    except Exception:
        return False, None


def merge_rename_and_summate(directory, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map):
    pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = extract_pdf_data(directory)

    merged_pdf_ccm = merge_pdfs(pdf_data_ccm)
    # @dev: Hardcoded to '10005' == Exxon
    merged_ccm_pdf_is_saved, filename = save_merged_pdf('CCM', merged_pdf_ccm, total_amount_sum_ccm, '10005', doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)
    # print(f'merged_pdf_ccm / merged_ccm_pdf_is_saved: {merged_pdf_ccm} / {merged_ccm_pdf_is_saved}')
    # PDFs were merged, saved, and renamed with a new filename and it is currently the last day of the month, then perform end of month filesystem management
    if merged_pdf_ccm and merged_ccm_pdf_is_saved and filename and is_last_day_of_month():
        print(f'CCM PDFs have been merged and saved!')
        end_of_month_operations(directory, filename)
        cleanup_files(pdf_data_ccm)

    # if it is not the last day
    else:
        # TODO: toggle back to clean up
        cleanup_files(pdf_data_ccm)
        # print(f'dont delete plz')

    merged_pdf_lrd = merge_pdfs(pdf_data_lrd)
    # @dev: Hardcoded to '10005' == Exxon
    merged_lrd_pdf_is_saved, filename = save_merged_pdf('LRD', merged_pdf_lrd, None, '10005', doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)

    if merged_pdf_lrd and merged_lrd_pdf_is_saved and filename:

        end_of_month_operations(directory, filename)
        cleanup_files(pdf_data_lrd)

    else:
        # TODO: toggle back to clean up
        cleanup_files(pdf_data_lrd)
        # print(f'dont delete plz')
