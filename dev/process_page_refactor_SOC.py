for company_name, keywords in company_name_to_search_keyword_mapping.items():
    # handle single page condition
    if company_name in current_page_text and 'END MSG' in current_page_text:
        # keep track of pdf objs to create new pdf obj
        current_pages.append(pdf.pages[page_num])
        # extract text from single page
        current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
        # extract target vars from text
        eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)
        print(f'\neft_num: {eft_num} | today: {today}  | total_draft_amt: {total_draft_amt}\n')

        # In case there's an outlier page, just skip to next page
        if eft_num is None or total_draft_amt is None:
            continue

        # Naming convention
        if company_name == 'EXXONMOBIL':
            new_file_name = f'{eft_num}-{today}-({total_draft_amt}).pdf'
            print(f'new_file_name: {new_file_name}')
        else:
            new_file_name = f'{eft_num}-{today}-{total_draft_amt}.pdf'
            print(f'new_file_name: {new_file_name}')

        # Create new pdf obj
        new_pdf = pikepdf.Pdf.new()

        # Append pikepdf Pdf obj as new pdf obj
        new_pdf.pages.extend(current_pages)

        # Fetch subdir path based on company name
        destination_dir = company_name_to_company_subdir_mapping[company_name]
        # print(f'destination_dir: {destination_dir}')

        # Absolute path to subdir for company name
        dest_dir_with_new_file_name = os.path.join(destination_dir, new_file_name)

        # Save new pdf obj to absolute subdir path
        new_pdf.save(dest_dir_with_new_file_name)

        # Move cursor to next page
        page_num += 1

        # Update start index for next document
        start_idx = page_num



        while company_name in current_page_text and 'END MSG' not in current_page_text and page_num < len(
                pdf.pages) - 1:
            page_num += 1
            # Keep track of pages for multi-page doc
            # list of pikepdf.Page objects; [pikepdf.Page1, pikepdf.Page2, etc...]
            current_pages.append(pdf.pages[page_num])
            print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! current_pages: {current_pages}')

            # Extract text for all subsequent page(s)
            current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

            # Keep track of texts for multi-page doc
            current_page_texts.append(current_page_text)
            print(f'---------------------------- current_page_texts: {current_page_texts}')

            # Combine all page text strings into a single string
            current_page_text = "".join(current_page_texts)
            # @dev: if multi-page doc, `current_page_text` should now be
            # all texts from all pages as single string to be passed into
            # extraction function
            print(f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n current_page_text: {current_page_text}')

        eft_num, today, total_draft_amt = extract_info_from_text(current_page_text, keywords)
        print(f'\neft_num: {eft_num} | today: {today}  | total_draft_amt: {total_draft_amt}\n')
