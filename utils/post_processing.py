import os
import re
import datetime
import pikepdf

def delete_pdf_files(output_directory, merged_file_path):
    if not os.path.exists(merged_file_path):
        print("Merged file does not exist. Not deleting any files.")
        return False

    files_deleted = False
    for file_name in os.listdir(output_directory):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(output_directory, file_name)
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
    match = re.match(r'LRD-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', pdf_file)
    if match:
        regex_num = match.group(1)
        return regex_num, None
    return None, None


def extract_pdf_data(directory):
    today = datetime.date.today().strftime('%m-%d-%y')
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    pdf_data = []
    total_amount = 0
    for pdf_file in pdf_files:
        if 'CCM' in directory:
            regex_num, amount = extract_ccm_data(pdf_file)
            total_amount += amount
        else:  # LRD
            regex_num, _ = extract_lrd_data(pdf_file)
        pdf_data.append((regex_num, today, os.path.join(directory, pdf_file)))
    pdf_data.sort(key=lambda x: x[0])
    return pdf_data, total_amount

def check_file_exists(output_path):
    file_path = os.path.join(output_path)
    return os.path.isfile(file_path)


def merge_pdfs(pdf_data):
    merged_pdf = pikepdf.Pdf.new()
    for _, _, _, file_path in pdf_data:
        pdf = pikepdf.Pdf.open(file_path)
        merged_pdf.pages.extend(pdf.pages)
    return merged_pdf

def save_merged_pdf(directory, merged_pdf, total_amount_sum, file_prefix):
    today = datetime.date.today().strftime('%m-%d-%y')
    if file_prefix == 'CCM':
        new_file_name = f'{file_prefix}-{today}-{total_amount_sum}.pdf'
    else:  # LRD
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
    print(f'{file_prefix} PDFs have been merged, renamed "{new_file_name}" and saved to: {output_path}')


def process_directory(directory):
    pdf_data_ccm, total_amount_sum_ccm = extract_pdf_data(directory)
    merged_pdf_ccm = merge_pdfs(pdf_data_ccm)
    save_merged_pdf(directory, merged_pdf_ccm, total_amount_sum_ccm, 'CCM')

    pdf_data_lrd, _ = extract_pdf_data(directory)
    merged_pdf_lrd = merge_pdfs(pdf_data_lrd)
    save_merged_pdf(directory, merged_pdf_lrd, None, 'LRD')


# def merge_rename_and_summate(temp_dir):
#     ccm_temp_dir = os.path.join(temp_dir, "CCM")
#     lrd_temp_dir = os.path.join(temp_dir, "LRD")
#
#
#     # Move the files to their respective directories
#     for file in os.listdir(temp_dir):
#         if file.startswith("CCM"):
#             os.rename(os.path.join(temp_dir, file), os.path.join(ccm_temp_dir, file))
#         elif file.startswith("LRD"):
#             os.rename(os.path.join(temp_dir, file), os.path.join(lrd_temp_dir, file))
#
#     pdf_data_ccm, total_amount_sum_ccm = extract_pdf_data(ccm_temp_dir, 'CCM')
#     merged_pdf_ccm = merge_pdfs(pdf_data_ccm)
#     save_merged_pdf(ccm_temp_dir, merged_pdf_ccm, total_amount_sum_ccm, 'CCM')
#
#     pdf_data_lrd, _ = extract_pdf_data(lrd_temp_dir, 'LRD')
#
