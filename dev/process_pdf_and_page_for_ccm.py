def process_page_cc(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

        # Handle single page CCM docs
        if re.search(r'CCM-\d+', current_page_text) and company_name in current_page_text and 'END MSG' in current_page_text:
            current_pages = [pdf.pages[page_num]]



        # Only single page docs only
        if re.search(r'EFT-\d+', current_page_text) and company_name in current_page_text and 'END MSG' in current_page_text:
            current_pages = [pdf.pages[page_num]]
            eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)

            new_file_name = get_new_file_name(eft_num, today, total_draft_amt, company_name)
            destination_dir = company_name_to_company_subdir_mapping[company_name]

            create_and_save_pdf(current_pages, new_file_name, destination_dir)

            # Move cursor at single page (micro) level
            page_num += 1

            # If there aren't anymore pages, exit loop
            if page_num >= len(pdf.pages):
                break

        # Only multipage EFT docs only
        elif re.search(r'EFT-\d+', current_page_text) and company_name in current_page_text and 'END MSG' not in current_page_text:
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
            eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)

            new_file_name = get_new_file_name(eft_num, today, total_draft_amt, company_name)
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
                page_num = process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping)

            # If all pages processed without errors, return True
            return True
    except Exception as e:
        # If any error occurred, print it and return False
        print(f'An unexpected error occurred: {str(e)}')
        return False
