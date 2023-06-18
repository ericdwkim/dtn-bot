# Print button saves to:
# C:/Users/cgonzales/Downloads/messages%20-%202023-05-17T063646.793.pdf

# misc path
#  This PC / nt1data (\\fileserver\data) (K:) / DTN Reports / Credit Cards / First Data

# 1st flow (Translated = No ; Group = Invoice) File system PATH to save to
#  This PC / nt1data (\\fileserver\data) (K:) / DTN Reports / Fuel Invoices / 5-May



"""
"""
"""
File system structure:

This PC
|_ nt1data (\\fileserver\data) (K:)
  |______________ DTN Reports
                |______________ Credit Cards         
                |______________ Fuel Drafts                                
                |______________ Fuel Invoices
                                |______________ 5-May
                                |______________ 2020
                                |______________ 2021
                                |______________ 2022
                                |______________ 2023
                                                
"""

"""
chat jippity prompt copypasta
_______________________________
Given the following file system structure:

File system structure:

This PC
|_ nt1data (\\fileserver\data) (K:)
  |______________ DTN Reports
                |______________ Credit Cards         
                |______________ Fuel Drafts                                
                |______________ Fuel Invoices
                                |______________ 5-May
                                |______________ 2020
                                |______________ 2021
                                |______________ 2022
                                |______________ 2023
              

And the default download directory path:

 C:/Users/cgonzales/Downloads/messages%20-%202023-05-17T063646.793.pdf

Using python, how to do the following:

1) Find the downloaded PDF in default download directory
2) Rename file as just today's date in `MM-DD-YY.pdf` format
3) Move the file from the downloads directory into appropriate subdirectory:
`This PC / nt1data (\\fileserver\data) (K:) / DTN Reports / Fuel Invoices / 5-May`


"""

# TODO: improvement functionality idea; this prevents having to hard code each and every `target_company`
"""
1) extract target company from first line that preceeds after `text` (typically the first "word" of each `text` (aka pdf file). 
2) turn target company name into variable for each respective file (ETF-#### for company X --> `company_name_etf`)
3) use company_name_etf to search through filesystem one level up, that is, a method to search all subdirs within `/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts` since all company names with their company id are listed in this directory 
4) 

"""

""" 
            *** Draft Notice - Notes ***

    - keyword string search in pdfs
        "Total Draft" for EXXON files only
        "TOTALS" for U.S. OIL COMPANY files only
        etc... 

    Questions for clarification:
    - does this naming convention ONLY apply to EFT/Draft Notice files?
    - is the () or not for values only convention for values that end with `-`?
    - why were the last three ETF files skipped and not saved in the recording? is this important or is it alright to just also save them in their respective dirs as well?

    - NEED: under "Draft Notice" directory, I need the list of all company names and their company id numbers
        - create mapping of company_id: company_name (or just company names as an array
        - use mapping or array to search ETF files for company_name as string instead of having each company name variable initalized in main.py


Refactoring rename_and_move_etf() to be reuseable for all ETF files:

 note: exxonmobil filenames' etf_num values will be wrapped in (); can add logic by `if eft_num[:-1] == '-'` as they all end in a hyphen 
    Key - the company_name
    Value - the keywords to search in document to extract eft_num
    
    
    eft_companies = ['CVR SUPPLY & TRADING, LLC', 'EXXONMOBIL']
    
    OR 
    
    total_draft_amount_mapping: 
    [
    { 'CVR SUPPLY & TRADING, LLC': 'Total Draft' }, 
    { 'EXXONMOBIL': 'TOTAL AMOUNT OF FUNDS TRANSFER' },
    { 'U.S. OIL COMPANY': 'TOTALS' },
    { 'VALERO': '*** Net Amount ***' },
    
    ]

    { 'VALERO': '*** Net Amount ***' },



need to add if current month directory doesn't exist in filesystem, then create directory and place file in directory; also create additional appropriate new subdirs if necessary (ie: new companies, etc..)



Improvement / feature idea:
- download Invoice, Draft Notice, etc... and instead of leaving it to be saved as default `messages.pdf`
 (at least on mac), rename the defaults to concat what type of file `messages_invoice.pdf` which can be another check to ensure
 a `messages_invoice.pdf` does not get moved to a draft notice directory.



keyword_in_dl_file_name --> 'messages` = substring that is contained in originally downloaded PDF (invoice, draft notices, credit cards, etc...)
company_name_to_target_subdir_mapping --> `company_subdir_mapping` = {company_name: company_subdirectory} 
    allows us to search for each companies' respective subdir in (~/DTN Reports/Fuel Drafts)
    to then turn each companies' full subdir path into a variable as `destination_dir` (or previously as `dest_dir` for short. 




"""