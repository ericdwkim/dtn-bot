import os
import shutil
import datetime
import PyPDF2

def rename_and_move_pdf(file_name, source_dir, target_dir):
    # Get today's date and format it as MM-DD-YY
    today = datetime.date.today().strftime('%m-%d-%y')

    # Find the downloaded PDF
    for file in os.listdir(source_dir):
        if file.endswith('.pdf') and file_name in file:  # Adjust this as needed to match your file
            source_file = os.path.join(source_dir, file)
            # Rename file
            destination_file = os.path.join(target_dir, f'{today}.pdf')
            # Move the file
            print(f'Moving {destination_file} to {target_dir}')
            shutil.move(source_file, destination_file)
            break  # If you're only expecting one such file, you can break the loop after the first one found


# TODO: 5) self.pdf_handler() with appropriate params specific to Draft Notice
"""
Creating new helper function specific to handling pdf saving, moving, renaming, etc.. for EFT/Draft Notices

Testing CVR Supply for file naming convention using `Total Draft` amount as part of filename as follows:

`EFT-1575-061623-23952.13`

1) read downloaded Draft Notice PDF file (aka EFT files)
    1a) use `dl_dir` path to open and read all of EFT files

2) search for "CVR SUPPLY & TRADING, LLC" -OR- just search for "Total Draft" and find value
    and turn it into a variable `tot_draft_amt` = 23952.13

            *** NEED CLARIFICATION ON THIS ***
                EDGE CASE HANDLING:  
                - what if "Total Draft" doesn't exist in any of the downloaded EFT files?
                - do we just skip? or just omit the Total Draft value as part of filename? 
                - does that file name convention above ONLY apply to "CVR SUPPLY & TRADING, LLC" files?
            *** NEED CLARIFICATION ON THIS ***

3) ONLY WITHIN THE PAGE THAT CONTAINS "Total Draft" string, search for EFT number at header section
and turn it into a variable; probably search for string "EFT-" including hyphen within the page
                `eft_num_that_contains_tot_draft_amt` = 1575
        OR just use the whole string as a variable "EFT-####" --> `eft_num`
                

4) string concat for filenaming convention:
    filename = `eft_num` + `-`todays_date` + '-' + `tot_draft_amt`.pdf
    
5) move `filename` to appropriate subdirectory from `dl_dir` to `dest_dir_draft_notices` according to convention

"""

def rename_and_move_eft(file_name, source_dir, target_dir):
    today = datetime.date.today().strftime('%m-%d-%y')
    for file in os.listdir(source_dir):
        if file.endswith('.pdf') and file_name in file:
            source_file = os.path.join(source_dir, file)

            # Read the PDF file
            with open(source_file, 'rb') as f:
                reader = PyPDF2.PdfFileReader(f)

                # Iterate through all the pages in the PDF
                for i in range(reader.getNumPages()):
                    page = reader.getPage(i)
                    text = page.extract_text()

                    # Check if the page contains the specific company name
                    if 'CVR SUPPLY & TRADING, LLC' in text:
                        # Extract the EFT number and the Total Draft Amount
                        eft_num = extract_eft_number(text)  # This function needs to be defined according to your needs
                        tot_draft_amt = extract_total_draft_amount(text)  # This function needs to be defined according to your needs

                        # Rename the file
                        new_file_name = f'{eft_num}-{today}-{tot_draft_amt}.pdf'
                        destination_file = os.path.join(target_dir, new_file_name)

                        # Move the file
                        print(f'Moving {source_file} to {destination_file}')
                        shutil.move(source_file, destination_file)
                        break

def extract_eft_number(text):
    # This function needs to be defined to extract the EFT number from the text
    # For example, if the EFT number is always at the start of the line and followed by a space:
    return text.split(' ')[0]

def extract_total_draft_amount(text):
    # This function needs to be defined to extract the Total Draft Amount from the text
    # For example, if the Total Draft Amount is always on a line that starts with "Total Draft Amount: ":
    for line in text.split('\n'):
        if line.startswith('Total Draft Amount: '):
            return line.split(': ')[1]
