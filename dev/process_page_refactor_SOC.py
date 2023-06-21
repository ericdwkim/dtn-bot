def create_and_save_pdf(pages, new_file_name, destination_dir):
    new_pdf = pikepdf.Pdf.new()
    new_pdf.pages.extend(pages)
    dest_dir_with_new_file_name = os.path.join(destination_dir, new_file_name)
    new_pdf.save(dest_dir_with_new_file_name)


def get_new_file_name(eft_num, today, total_draft_amt, company_name):
    if company_name == 'EXXONMOBIL':
        new_file_name = f'{eft_num}-{today}-({total_draft_amt}).pdf'
    else:
        new_file_name = f'{eft_num}-{today}-{total_draft_amt}.pdf'
    print(f'new_file_name: {new_file_name}')
    return new_file_name


def process_page(pdf, page_num, company_name_to_search_keyword_mapping, company_name_to_company_subdir_mapping):
    for company_name, keywords in company_name_to_search_keyword_mapping.items():
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

        if company_name in current_page_text and 'END MSG' in current_page_text:
            current_pages = [pdf.pages[page_num]]
            eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)

            new_file_name = get_new_file_name(eft_num, today, total_draft_amt, company_name)
            destination_dir = company_name_to_company_subdir_mapping[company_name]

            create_and_save_pdf(current_pages, new_file_name, destination_dir)

            page_num += 1

        elif company_name in current_page_text and 'END MSG' not in current_page_text:
            current_pages = []
            current_page_texts = []

            while 'END MSG' not in current_page_text and page_num < len(pdf.pages) - 1:
                current_pages.append(pdf.pages[page_num])
                current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
                current_page_texts.append(current_page_text)
                page_num += 1

            current_page_text = "".join(current_page_texts)
            eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)

            new_file_name = get_new_file_name(eft_num, today, total_draft_amt, company_name)
            destination_dir = company_name_to_company_subdir_mapping[company_name]

            create_and_save_pdf(current_pages, new_file_name, destination_dir)

    return page_num
