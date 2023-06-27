import os
import re
import datetime
import pikepdf

def cleanup_files(pdf_data):
    files_deleted = False
    for _, _, _, file_path in pdf_data:
        if os.path.exists(file_path):
            os.remove(file_path)
            files_deleted = True
    return files_deleted


def extract_ccm_data(pdf_file):
    match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', pdf_file)
    if match:
        regex_num = int(match.group(1))
        total_amount = float(match.group(2).replace(',', ''))
        return regex_num, total_amount
    return None, None


def extract_lrd_data(pdf_file):
    match = re.match(r'LRD-(\d+)-.*\.pdf', pdf_file)
    if match:
        regex_num = match.group(1)
        return regex_num, None
    return None, None


def extract_pdf_data(directory):
    today = datetime.date.today().strftime('%m-%d-%y')
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    pdf_data_ccm = []
    pdf_data_lrd = []
    total_amount = 0
    for pdf_file in pdf_files:
        if pdf_file.startswith('CCM'):
            regex_num_ccm, amount = extract_ccm_data(pdf_file)
            total_amount += amount
            pdf_data_ccm.append((regex_num_ccm, today, total_amount, os.path.join(directory, pdf_file)))
        elif pdf_file.startswith('LRD'):
            regex_num_lrd, _ = extract_lrd_data(pdf_file)
            pdf_data_lrd.append((regex_num_lrd, today, _, os.path.join(directory, pdf_file)))
    pdf_data_ccm.sort(key=lambda x: x[0])
    pdf_data_lrd.sort(key=lambda x: x[0])
    return pdf_data_ccm, total_amount, pdf_data_lrd

def check_file_exists(output_path):
    file_path = os.path.join(output_path)
    return os.path.isfile(file_path)


def merge_pdfs(pdf_data):
    merged_pdf = pikepdf.Pdf.new()
    for _, _, _, file_path in pdf_data:
        try:
            pdf = pikepdf.Pdf.open(file_path)
            merged_pdf.pages.extend(pdf.pages)
        except pikepdf.PdfError:
            return False
    return merged_pdf


def save_merged_pdf(directory, merged_pdf, total_amount_sum, file_prefix):
    today = datetime.date.today().strftime('%m-%d-%y')
    if file_prefix == 'CCM':
        new_file_name = f'{file_prefix}-{today}-{total_amount_sum}.pdf'
    else:  # LRD
        new_file_name = f'{today}-Loyalty.pdf'

    output_path = os.path.join(directory, new_file_name)
    try:
        merged_pdf.save(output_path)
        merged_pdf.close()
        print(f'{file_prefix} PDFs have been merged, renamed "{new_file_name}" and saved to: {output_path}')
        return True
    except Exception:
        return False

def merge_rename_and_summate(directory):
    pdf_data_ccm, total_amount_sum_ccm, pdf_data_lrd = extract_pdf_data(directory)

    merged_pdf_ccm = merge_pdfs(pdf_data_ccm)
    merged_ccm_pdf_is_saved = save_merged_pdf(directory, merged_pdf_ccm, total_amount_sum_ccm, 'CCM')
    if merged_pdf_ccm and merged_ccm_pdf_is_saved:
        cleanup_files(pdf_data_ccm)

    merged_pdf_lrd = merge_pdfs(pdf_data_lrd)
    merged_lrd_pdf_is_saved = save_merged_pdf(directory, merged_pdf_lrd, None, 'LRD')
    if merged_pdf_lrd and merged_lrd_pdf_is_saved:
        cleanup_files(pdf_data_lrd)
