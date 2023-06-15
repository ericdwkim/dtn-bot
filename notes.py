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