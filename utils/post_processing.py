import os
import re
import datetime
import pikepdf

# TODO: 6-26-23 - test refactored driver function

# TODO: need to fix this logic to 1) check if all appropriate multi AND single page pdfs are ready for post processing and located in temp_dir
# TODO: this will be dependent on each original PDF. REMEMBER, this is specific to exxon 'TOTAL DISTRIBUTOR' calculation



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
    pdf_data = []
    for pdf_file in pdf_files:
        if pdf_file.endswith('.pdf'):
            file_path = os.path.join(temp_dir, pdf_file)
            match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', pdf_file)
            if match:
                regex_num = int(match.group(1))
                total_credit_amt = float(match.group(2).replace(',', ''))
                pdf_data.append((regex_num, today, total_credit_amt, file_path))
    pdf_data.sort(key=lambda x: x[0])
    total_credit_amt_sum = round(sum(item[2] for item in pdf_data), 2)
    return pdf_data, total_credit_amt_sum

def merge_pdfs(pdf_data):
    merged_pdf = pikepdf.Pdf.new()
    for _, _, _, file_path in pdf_data:
        pdf = pikepdf.Pdf.open(file_path)
        merged_pdf.pages.extend(pdf.pages)
    return merged_pdf

def save_merged_pdf(temp_dir, merged_pdf, total_credit_amt_sum):
    today = datetime.date.today().strftime('%m-%d-%y')
    new_file_name = f'CCM-{today}-{total_credit_amt_sum}.pdf'
    output_dir = temp_dir[:-5]
    output_path = os.path.join(output_dir, new_file_name)
    merged_pdf.save(output_path)
    merged_pdf.close()
    if os.path.exists(output_path):
        print(f'PDFs have been merged, renamed, and moved to: {output_path}')
        temp_files_deleted = delete_pdf_files(temp_dir)
        if temp_files_deleted:
            print('Temporary PDF files have been deleted.')
        else:
            print('Failed to delete temporary PDF files.')
    else:
        print('Failed to save the merged PDF.')

    merged_pdf.close()

def merge_rename_and_summate(temp_dir):
    pdf_data, total_credit_amt_sum = extract_pdf_data(temp_dir)
    merged_pdf = merge_pdfs(pdf_data)
    save_merged_pdf(temp_dir, merged_pdf, total_credit_amt_sum)
