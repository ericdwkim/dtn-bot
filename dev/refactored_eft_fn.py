from PyPDF2 import PdfFileReader, PdfFileWriter

# The mapping dictionary
total_draft_amount_mapping = {
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


def process_pdf(file_path, source_dir, target_dir, mapping):
    """Process a PDF file, extract info from pages that contain target company and move to target dir"""
    with open(file_path, 'rb') as f:
        reader = PdfFileReader(f)

        for page_num in range(reader.getNumPages()):
            page = reader.getPage(page_num)
            text = page.extract_text()

            # Check each company
            for company, keyword in mapping.items():
                if company in text:
                    eft_num, today, total_draft = extract_info_from_page(page, keyword)
                    new_file_name = f'{eft_num}-{today}-{total_draft}.pdf' if company != 'EXXONMOBIL' else f'{eft_num}-{today}-({total_draft}).pdf'
                    destination_file = os.path.join(target_dir, company, new_file_name)

                    # Save the page to a new PDF
                    writer = PdfFileWriter()
                    writer.addPage(page)
                    with open(destination_file, 'wb') as output_pdf:
                        writer.write(output_pdf)

                    print(f'Moved page {page_num} to {destination_file}')
                    break  # If we found a match, no need to check the other companies


# Call the function
process_pdf('Path_to_your_PDF_file', dl_dir, dest_dir_draft_notices, total_draft_amount_mapping)
