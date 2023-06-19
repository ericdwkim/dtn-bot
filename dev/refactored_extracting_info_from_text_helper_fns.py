# total_draft_line = [line for line in lines if target_keyword in line]
# if total_draft_line:
#     total_draft = re.findall(r'(\d+\.\d+)', total_draft_line[0])
#     if total_draft:
#         total_draft = total_draft[0]
#     else:
#         print(f"Couldn't find a matching draft total on page {page_num} for company {company_name}.")
#         total_draft = None
# else:
#     print(f"Couldn't find the keyword '{target_keyword}' on page {page_num} for company {company_name}.")
#     total_draft = None
#
#
#
# for line in lines:
#     if "Total Draft" in line:
#     total_draft_lines = line
#
#

# Initialize today's date as global var
today = datetime.date.today().strftime('%m-%d-%y')

def extract_info_from_text(text):
    """Extract the specific information from a page"""
    # Split the text into a list of lines
    lines = text.split('\n')
    return lines


def get_eft_num():
    lines = extract_info_from_text()
    eft_num_line = lines[1] # EFT-#### typically on 2nd line
    eft_num = eft_num_line.split()[2] # EFT-#### typically third word
    return eft_num


def get_total_draft(lines, target_keyword):
    """Get the total draft from the lines that contain the target keyword"""
    total_draft_lines = [line for line in lines if target_keyword in line]
    if not total_draft_lines:
        print(f"No lines found with keyword: {target_keyword}")
        return None

    total_draft_line = total_draft_lines[0]
    total_draft_matches = re.findall(r'(\d+\.\d+)', total_draft_line)
    if not total_draft_matches:
        print(f"No matches for regular expression in line: {total_draft_line}")
        return None

    total_draft = total_draft_matches[0]
    return total_draft


"""
# process_page()

text = ' '.join(viewer.canvas.strings)
lines = extract_info_from_text(text)

eft_num, today = get_eft_and_date(lines)
total_draft = get_total_draft(lines, keyword)

# If any of the extracted values is None, continue to next company
if eft_num is None or today is None or total_draft is None:
    continue
    
"""

import re


def extract_info_from_text(text, target_keywords):
    """Extract the specific information from a page"""

    # Extract total_draft
    total_draft_keyword = target_keywords[0]
    total_draft_matches = re.findall(r'(\d+\.\d+)', text)
    if not total_draft_matches:
        print(f"No matches for regular expression in text: {total_draft_keyword}")
        return None, None, None
    total_draft = total_draft_matches[0]

    # Extract EFT number
    eft_num_keyword = target_keywords[1]  # Assuming keyword is something like 'EFT-'
    eft_num_pattern = eft_num_keyword.replace('*', '\d+')  # Replace '*' with regex pattern for any digit
    eft_num_matches = re.findall(eft_num_pattern, text)
    if not eft_num_matches:
        print(f"No matches for regular expression in text: {eft_num_pattern}")
        return None, None, None
    eft_num = eft_num_matches[0]

    today = datetime.date.today().strftime('%m-%d-%y')

    return eft_num, today, total_draft
