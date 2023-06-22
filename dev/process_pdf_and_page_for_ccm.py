def create_and_save_pdf(pages, new_file_name, destination_dir):
    new_pdf = pikepdf.Pdf.new()
    new_pdf.pages.extend(pages)
    dest_dir_with_new_file_name = os.path.join(destination_dir, new_file_name)
    new_pdf.save(dest_dir_with_new_file_name)


def get_new_file_name_cc(today, total_credit_amt):
    new_file_name = f'{today}-{total_credit_amt}.pdf'
    print(f'new_file_name: {new_file_name}')
    return new_file_name

def extract_text_from_pdf_page(page):
    # Create a BytesIO buffer
    pdf_stream = io.BytesIO()

    # Write the page to the buffer
    with pikepdf.Pdf.new() as pdf:
        pdf.pages.append(page)
        pdf.save(pdf_stream)

    # Use pdfplumber to read the page from the buffer
    pdf_stream.seek(0)
    with pdfplumber.open(pdf_stream) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

    return text

def extract_info_from_text_cc(current_page_text, target_keywords):
    """Extract the specific information from a page"""

    # Extract total_credit
    total_credit_keyword = target_keywords[0]
    total_credit_matches = re.findall(r'([\d,]+\.\d+)', current_page_text)
    print(f'\nUsing total_credit_keyword: "{total_credit_keyword}"\nGetting total_credit_matches: {total_credit_matches}\n')
    if total_credit_matches:
        total_credit_amt = total_credit_matches[-1] # TODO: may only apply for VALERO and NOT exxon CCMs
    else:
        print(f"No matches for regular expression using keyword: {total_credit_keyword} in text:\n*****************************************************\n {current_page_text}\n*****************************************************\n")
        total_credit_amt = None

    today = datetime.date.today().strftime('%m-%d-%y')

    if total_credit_amt is None:
        return today, None

    return today, total_credit_amt


def process_page_cc(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

        # Handle single page CCM VALERO docs
        if re.search(r'CCM-\d+', current_page_text) and 'VALERO' in current_page_text and 'END MSG' in current_page_text:
            current_pages = [pdf.pages[page_num]]
            today, net_credit_amt = extract_info_from_text_cc(current_page_text, keywords)

            new_file_name = get_new_file_name_cc(today, net_credit_amt)
            destination_dir = company_name_to_company_subdir_mapping[company_name]
            create_and_save_pdf(current_pages, new_file_name, destination_dir)

            page_num += 1

            if page_num >= len(pdf.pages):
                break

        # Only multipage CCM VALERO docs only
        elif re.search(r'CCM-\d+', current_page_text) and 'VALERO' in current_page_text and 'END MSG' not in current_page_text:
            current_pages = []
            current_page_texts = []

            while 'END MSG' not in current_page_text and page_num < len(pdf.pages) - 1:
                current_pages.append(pdf.pages[page_num])
                current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
                current_page_texts.append(current_page_text)
                # Move cursor at multi-page (micro) level
                page_num += 1

                # If there aren't anymore pages, exit loop
                if page_num >= len(pdf.pages):
                    break

            current_page_text = "".join(current_page_texts)
            today, total_credit_amt = extract_info_from_text(current_page_text, keywords)

            new_file_name = get_new_file_name_cc(today, total_credit_amt)
            destination_dir = company_name_to_company_subdir_mapping[company_name]

            create_and_save_pdf(current_pages, new_file_name, destination_dir)

    return page_num


def process_pdf_cc(keyword_in_dl_file_name, company_name_to_company_subdir_mapping, download_dir, company_name_to_search_keyword_mapping):
    try:
        # Get all matching files
        full_path_to_downloaded_pdf = get_full_path_to_dl_dir(download_dir, keyword_in_dl_file_name)

        # Read original PDF from dls dir
        print(f'Processing file: {full_path_to_downloaded_pdf}')
        with pikepdf.open(full_path_to_downloaded_pdf) as pdf:
            page_num = 0  # Initialize page_num
            while page_num < len(pdf.pages):
                # Process pages and update the page number at original PDF (macro) level
                page_num = process_page_cc(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping)

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False
