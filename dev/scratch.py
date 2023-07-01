from utils.pdf_processor import  PdfProcessor


dl_dir = PdfProcessor.download_dir
file_path = dl_dir + '/messages.pdf'

print(file_path)

"""

So we would need something like this function to dynamically get all the required params dynamically and with this we can create our class instance PdfProcessor for each instance level


def someGreatFunction():
    current_page_text = extract_text_from_pdf_page(pdf.pages[page_num])
    for company_name in company_names:
        # Handles CCM, CMB, LRD multi page docs
        if company_name in current_page_text
            for pattern in regex_patterns:
                regex_num, self.today, self.total_target_amt = extract_info_from_text(current_page_text, pattern)


        self.doc_type = doc_type --> `pattern` variable dynamically fetched from inner loop 
        
        self.company_id = company_id --> `company_id` variable dynamically fetched from outer loop by using `company_name` and `company_id_to_company_subdir_map` (search company_name in value to fetch company_id)

        self.total_target_amt = total_target_amt --> `total_target_amt` variable dynamically fetched from `extract_info_from_text(current_page_text, pattern)` where `pattern` would be `self.doc_type` 
        
        
        

"""
