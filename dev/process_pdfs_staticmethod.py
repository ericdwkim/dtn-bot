@staticmethod
def process_pdfs(pdf_files, regex_patterns, doc_type_abbrv_to_doc_type_subdir_map,
                 company_id_to_company_subdir_map, post_processing=False):

    # Get company_names from the helper function
    company_names = get_company_names(company_id_to_company_subdir_map)

    for pdf_file in pdf_files:
        pdf = Pdf.open(pdf_file)

        for page_num in range(len(pdf.pages)):
            current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])

            for company_name in company_names:
                if company_name in current_page_text:
                    # Get the company_id from the mapping
                    company_id = get_company_id(company_name)  # Use your helper function to get the company id

                    for pattern in regex_patterns:
                        if re.search(pattern, current_page_text, re.IGNORECASE):
                            # The pattern is the doc_type
                            doc_type = pattern

                            # Extract the other info
                            regex_num, today, total_target_amt = extract_info_from_text(current_page_text, pattern)

                            # Now we have all the info we need to create a PdfProcessor instance
                            processor = PdfProcessor(pdf_file, doc_type, company_id, total_target_amt)

                            # Use the processor to process the PDF
                            if 'END MSG' in current_page_text:
                                processor.process_single_page(pdf, page_num, company_names, regex_patterns)
                            else:
                                page_num = processor.process_multi_page(pdf, page_num, company_names, regex_patterns)
