import os
import re
from datetime import datetime
import pikepdf
import shutil
from utils.filesystem_manager import end_of_month_operations, construct_month_dir_from_doc_type, is_last_day_of_month, cleanup_files

# TODO: move all `extract_` helpers to extraction_handler.py as class `PDFExtractor` instance method
def extract_ccm_data(pdf_file):
    """
    Extracts CCM relevant data from List of tuples with target data
    :param pdf_file:
    :return:
    """
    filename = os.path.basename(pdf_file)
    match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', filename)
    if match:
        doc_type_num = int(match.group(1))
        total_amount = float(match.group(2).replace(',', ''))
        return doc_type_num, total_amount
    return None, None


def extract_lrd_data(pdf_file):
    """
    Extracts LRD relevant data from list of tuples
    :param pdf_file:
    :return:
    """
    match = re.match(r'LRD-(\d+)-.*\.pdf', pdf_file)
    if match:
        doc_type_num = match.group(1)
        return doc_type_num, None
    return None, None


def extract_pdf_data(company_dir):
    """
    Extracts target data from filenames for calculation for post-processing
    :param company_dir: path to company name directory
    :return: Tuple (List, Int, List) where each List contains tuples of pre-extracted data relevant for CCM and LRD, respectively.
    """
    today = datetime.today().strftime('%m-%d-%y')  # @today
    # today = '07-23-23'

    pdf_files = [f for f in os.listdir(company_dir) if f.endswith('.pdf')]
    print(f'************************ pdf_files ******************** : {pdf_files}\n')
    pdf_data_ccm = []
    pdf_data_lrd = []
    total_amount = 0.00
    for pdf_file in pdf_files:
        if pdf_file.startswith('CCM'):
            doc_type_num_ccm, amount = extract_ccm_data(pdf_file)
            total_amount += amount
            total_amount = round(total_amount, 2)  # Round to two decimal places
            pdf_data_ccm.append((doc_type_num_ccm, today, total_amount, os.path.join(company_dir, pdf_file)))
        elif pdf_file.startswith('LRD'):
            doc_type_num_lrd, _ = extract_lrd_data(pdf_file)
            pdf_data_lrd.append((doc_type_num_lrd, today, _, os.path.join(company_dir, pdf_file)))
    pdf_data_ccm.sort(key=lambda x: x[0])
    print(f'*********************************** pdf_data_ccm {pdf_data_ccm}\n')
    pdf_data_lrd.sort(key=lambda x: x[0])
    print(f'*********************************** pdf_data_lrd {pdf_data_lrd}\n')

    return pdf_data_ccm, total_amount, pdf_data_lrd

# TODO: class PDFPostProcessorMerger that inherits from class PDFExtractor (extraction_handler.py); call post processing relevant extraction methods via an instance of PDFPostProcessorMerger object, such as: `post_procecssor_merger = PDFPostProcessorMerger()` then `post_procecssor_merger.extract_pdf_data()`
# TODO: PDFPostProcessorMerger with class attribute `self.new_pdf = pikepdf.Pdf.new()` to be used within class easily as it is commonly used in other areas such as `create_and_save_pdf`; similar to `today` instance, we don't want to repeat this and be able to just use `self.new_pdf` in order to `self.new_pdf.pages.extend(self.page_objs) for `create_and_save_pdf_refactored`
def merge_pdfs(pdf_data):
    """
    Merges PDFs by fetching 4th element in tuple `file_path` by looping, opening each file_path\nand creating them as pikePDF pages to combine and merge them all into a single PDF object
    :param pdf_data:
    :return: `merged_pdf` a pikePDF object | None
    """
    merged_pdf = pikepdf.Pdf.new()
    for _, _, _, file_path in pdf_data:
        try:
            pdf = pikepdf.Pdf.open(file_path)
            merged_pdf.pages.extend(pdf.pages)
        except pikepdf.PdfError:
            return False
    return merged_pdf

def save_merged_pdf(file_prefix, merged_pdf, total_amount_sum, company_id):
    """
    Saves pre-merged pike PDF object with constructed filename dependent on doc type with provided target data.
    :param file_prefix: CCM or LRD ; only these for post-processing
    :param merged_pdf:
    :param total_amount_sum:
    :param company_id:
    :return: Bool
    """
    today = datetime.today().strftime('%m-%d-%y')  # @today
    # today = '07-23-23'

    if file_prefix == 'CCM':
        new_file_name = f'{file_prefix}-{today}-{total_amount_sum}.pdf'
    else:
        new_file_name = f'{today}-Loyalty.pdf'

    month_directory = construct_month_dir_from_doc_type(file_prefix, company_id)
    output_path = os.path.join(month_directory, new_file_name)

    try:
        merged_pdf.save(output_path)
        merged_pdf.close()
        print(f'{file_prefix} PDFs have been merged, renamed "{new_file_name}" and saved to: {output_path}')
        return True
    except Exception:
        return False


def merge_rename_and_summate(company_dir):
    """
    Main post-processing wrapper function. Accounts for end of month operations if last day of the month.
    :param company_dir: path to company name directory
    :return: None
    """
    pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = extract_pdf_data(company_dir)
    print(
        f'********************* pdf_data_ccm: {pdf_data_ccm}\n total_amount_sum_ccm: {total_amount_sum_ccm}\n *********** pdf_data_lrd {pdf_data_lrd}  ')

    merged_pdf_ccm = merge_pdfs(pdf_data_ccm)
    merged_ccm_pdf_is_saved = save_merged_pdf('CCM', merged_pdf_ccm, total_amount_sum_ccm, '10005')
    print(f'merged_pdf_ccm / merged_ccm_pdf_is_saved: {merged_pdf_ccm} / {merged_ccm_pdf_is_saved}')
    # Clean up pre-merged PDFs in EXXON company_dir; loops through file_path (4th elem in tuple) to delete
    cleanup_files(pdf_data_ccm)
    # PDFs were merged, saved w/ new filename. If it is currently the last day of the month, then perform end of month filesystem management
    if merged_pdf_ccm and merged_ccm_pdf_is_saved and is_last_day_of_month():
        end_of_month_operations(company_dir)

    merged_pdf_lrd = merge_pdfs(pdf_data_lrd)
    merged_lrd_pdf_is_saved = save_merged_pdf('LRD', merged_pdf_lrd, None, '10005')
    # Clean up pre-merged PDFs in EXXON company_dir; loops through file_path (4th elem in tuple) to delete
    cleanup_files(pdf_data_lrd)
    # PDFs were merged, saved w/ new filename. If it is currently the last day of the month, then perform end of month filesystem management
    if merged_pdf_lrd and merged_lrd_pdf_is_saved and is_last_day_of_month():
        end_of_month_operations(company_dir)
