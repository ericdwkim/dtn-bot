def process_pdfs(self, regex_patterns,
             doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map, post_processing=False):


    try:

        # print(f'----------------------------- {file_path}')
        # print(f'Processing all single-page files....\n')
        single_pages_processed = process_pages(file_path,
                                               regex_patterns, is_multi_page=False)
        if single_pages_processed:
            print(f'Successfully finished processing all single-paged files\n')

        # print(f'Now processing all multi-page files....\n')
        multi_pages_processed = process_pages(file_path,
                                              regex_patterns, is_multi_page=True)
        if multi_pages_processed:
            print(f'Successfully finished processing all multi-paged files\n')

        # Conditional post processing only for EXXON CCMs and LRDs
        if single_pages_processed and multi_pages_processed and post_processing is True:
            # print(f'Post processing for EXXON CCMs & LRDs')
            output_path = self.file_path_mappings[self.doc_type][self.company_id]
            merge_rename_and_summate(output_path, doc_type_abbrv_to_doc_type_subdir_map, company_id_to_company_subdir_map)

        # Dynamic filesystem mgmt when post processing is False and
        elif single_pages_processed and multi_pages_processed and post_processing is False and is_last_day_of_month():
            end_of_month_operations(self.new_file_name)

        else:
            return single_pages_processed and multi_pages_processed

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return False
