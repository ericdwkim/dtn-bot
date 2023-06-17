from PyPDF2 import PdfFileReader, PdfFileWriter

# The mapping dictionary
company_name_target_keyword_mapping = {
    'CVR SUPPLY & TRADING, LLC': 'Total Draft',
    'EXXONMOBIL': 'TOTAL AMOUNT OF FUNDS TRANSFER',
    'U.S. OIL COMPANY': 'TOTALS',
    'VALERO': '*** Net Amount ***',
}


def extract_info_from_page(page, target_keyword):
    """Extract the specific information from a page"""
    text = page.extract_text()
    lines = text.splitlines()
    eft_num_line = lines[1]
    eft_num = eft_num_line.split()[2]
    today = datetime.date.today().strftime('%m-%d-%y')

    total_draft_line = [line for line in lines if target_keyword in line][0]
    total_draft = re.findall(r'(\d+\.\d+)', total_draft_line)[0]

    return eft_num, today, total_draft


def process_pdf(file_name, source_dir, target_dir, mapping):

    # Create full file path where it gets downloaded
    file_path = os.path.join(source_dir, f"{file_name}.pdf")

    """Process a PDF file, extract info from pages that contain target company and move to target dir"""
    with open(file_path, 'rb') as f:
        reader = PdfFileReader(f)


        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            # Check each company
            for company, keyword in mapping.items():
                if company in text:
                    eft_num, today, total_draft = extract_info_from_page(page, keyword)
                    if company == 'EXXONMOBIL':
                        new_file_name = f'{eft_num}-{today}-({total_draft}).pdf'
                        # adds () to value
                        print(f'should be exxon: {company}')
                    else:
                        new_file_name = f'{eft_num}-{today}-{total_draft}.pdf'
                        print(f'-----------: {new_file_name}')
                    # destination_file = os.path.join(target_dir, company, new_file_name)

                    # Save the page to a new PDF
                    # writer = PdfFileWriter()
                    # writer.addPage(page)
                    # with open(destination_file, 'wb') as output_pdf:
                    #     writer.write(output_pdf)

                    # print(f'Moved page {page_num} to {destination_file}')
                    break  # If we found a match, no need to check the other companies



dest_dir_draft_notices = r'/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts'
# target_dir
dl_dir = r'/Users/ekim/Downloads'
# source_dir


# Call the function
process_pdf('Path_to_your_PDF_file', dl_dir, dest_dir_draft_notices, company_name_target_keyword_mapping)


