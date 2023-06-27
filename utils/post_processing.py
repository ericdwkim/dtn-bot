import os
import re
import datetime
import pikepdf

# TODO: 6-26-23 - test refactored driver function w/ LRD and CCM

def delete_pdf_files(directory_path):
    files_deleted = False

    for file_name in os.listdir(directory_path):
        print(f'filename: {file_name}')
        if file_name.endswith('.pdf'):
            file_path = os.path.join(directory_path, file_name)
            os.remove(file_path)
            files_deleted = True

    return files_deleted

def extract_pdf_data(temp_dir):
    today = datetime.date.today().strftime('%m-%d-%y')
    pdf_files = os.listdir(temp_dir)
    pdf_data_ccm = []
    pdf_data_lrd = []
    for pdf_file in pdf_files:
        if pdf_file.endswith('.pdf'):
            file_path = os.path.join(temp_dir, pdf_file)
            if pdf_file.startswith('CCM'):
                match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', pdf_file)
                if match:
                    regex_num = int(match.group(1))
                    total_credit_amt = float(match.group(2).replace(',', ''))
                    pdf_data_ccm.append((regex_num, today, total_credit_amt, file_path))
            elif pdf_file.startswith('LRD'):
                match = re.match(r'LRD-(\d+)-.*\.pdf', pdf_file)
                if match:
                    regex_num = match.group(1)
                    pdf_data_lrd.append((regex_num, today, file_path))
    pdf_data_ccm.sort(key=lambda x: x[0])
    pdf_data_lrd.sort(key=lambda x: x[0])
    total_credit_amt_sum = round(sum(item[2] for item in pdf_data_ccm), 2)
    return pdf_data_ccm, total_credit_amt_sum, pdf_data_lrd

def check_file_exists(output_path):
    file_path = os.path.join(output_path)
    return os.path.isfile(file_path)


def merge_pdfs(pdf_data):
    merged_pdf = pikepdf.Pdf.new()
    for _, _, _, file_path in pdf_data:
        pdf = pikepdf.Pdf.open(file_path)
        merged_pdf.pages.extend(pdf.pages)
    return merged_pdf

def save_merged_pdf(temp_dir, merged_pdf, total_credit_amt_sum, file_prefix):
    today = datetime.date.today().strftime('%m-%d-%y')
    new_file_name = ''
    if file_prefix == 'CCM':
        new_file_name = f'{file_prefix}-{today}-{total_credit_amt_sum}.pdf'
    elif file_prefix == 'LRD':
        new_file_name = f'{today}-Loyalty.pdf'
    output_dir = temp_dir[:-5]
    output_path = os.path.join(output_dir, new_file_name)
    merged_pdf.save(output_path)
    merged_pdf.close()
    merged_file_exists = check_file_exists(output_path)
    if merged_file_exists:
        if file_prefix == 'CCM':
            print(f'EXXON CCM PDFs have been merged, renamed "{new_file_name}" and moved to: {output_path}\nDeleting temporary PDF files in {temp_dir}')
        elif file_prefix == 'LRD':
            print(f'Loyalty PDFs have been merged and saved as "{new_file_name}" to: {output_path}\nDeleting temporary PDF files in {temp_dir}')
        temp_files_deleted = delete_pdf_files(temp_dir)
        if temp_files_deleted:
            print('Temporary PDF files have been deleted.')
        else:
            print('Temporary PDF files were not deleted.')
    else:
        print('Failed to save the merged PDF.')

    merged_pdf.close()

def merge_rename_and_summate(temp_dir):
    pdf_data_ccm, total_credit_amt_sum_ccm, pdf_data_lrd = extract_pdf_data(temp_dir)

    merged_pdf_ccm = merge_pdfs(pdf_data_ccm)
    save_merged_pdf(temp_dir, merged_pdf_ccm, total_credit_amt_sum_ccm, 'CCM')

    merged_pdf_lrd = merge_pdfs(pdf_data_lrd)
    save_merged_pdf(temp_dir, merged_pdf_lrd, None, 'LRD')