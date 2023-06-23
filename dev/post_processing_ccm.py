import os
import re
import datetime
import pikepdf

def delete_pdf_files(directory_path):
    files_deleted = False

    for file_name in os.listdir(directory_path):
        print(f'---- filename: {file_name}')
        if file_name.endswith('.pdf'):
            file_path = os.path.join(directory_path, file_name)
            os.remove(file_path)
            files_deleted = True

    return files_deleted


def post_processing(temp_dir):


    today = datetime.date.today().strftime('%m-%d-%y')
    # Get a list of all PDF files in the directory
    pdf_files = os.listdir(temp_dir)
    # print(pdf_files)
    # Create a list to store parsed information
    pdf_data = []
    # Loop through each PDF file and extract information
    for pdf_file in pdf_files:
        if pdf_file.endswith('.pdf'):
            file_path = os.path.join(temp_dir, pdf_file)
            # Extract information from the file name using regular expressions
            match = re.match(r'CCM-(\d+)-.*-(\d{1,3}(?:,\d{3})*\.\d+)\.pdf', pdf_file)
            if match:
                regex_num = int(match.group(1))
                total_credit_amt = float(match.group(2).replace(',', ''))
                today = datetime.date.today().strftime('%m-%d-%y')

                # Add extracted information to the list
                pdf_data.append((regex_num, today, total_credit_amt, file_path))


    # Sort the PDF data by regex_num
    pdf_data.sort(key=lambda x: x[0])


    # Sum the total_credit_amt and round to second decimal place
    total_credit_amt_sum = round(sum(item[2] for item in pdf_data), 2)


    # Merge the PDFs using pikepdf
    merged_pdf = pikepdf.Pdf.new()

    for _, _, _, file_path in pdf_data:
        pdf = pikepdf.Pdf.open(file_path)
        merged_pdf.pages.extend(pdf.pages)

    # Save the merged PDF with the new file name
    new_file_name = f'CCM-{pdf_data[0][0]}-{today}-{total_credit_amt_sum}.pdf'  # Use the first regex_num and today
    output_dir = temp_dir[:-5]
    output_path = os.path.join(output_dir, new_file_name)
    merged_pdf.save(output_path)

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


temp_dir = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL (10005)/temp'

post_processing(temp_dir)