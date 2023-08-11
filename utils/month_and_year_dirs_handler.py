import logging

#TDOO WIP: delete the matching functiosn from here in filesystem_manager and migrate to pdf_processor.py
# NOTE: some other functions in filesystem_manager currently rely on some of thees functions, so they may need to be refactored/moved as well.
def cur_month_and_year_from_today(self):
    current_month = self.today.strftime('%m-%b')
    current_year = self.today.strftime('%Y')
    return current_year, current_month


@staticmethod
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    else:
        logging.error('Directory already exists!')
    return directory

def create_and_return_directory_path(self, parent_dir, year, month):
    year_dir = os.path.join(parent_dir, year)
    self.create_directory(year_dir)

    month_dir = os.path.join(year_dir, month)
    self.create_directory(month_dir)

    return month_dir

def is_last_day_of_month(self):
    tomorrow = self.today + timedelta(days=1)
    return tomorrow.day == 1

# @dev: previously called `end_of_month_operations`
def get_year_and_month(self):
    # throw away current_month as not needed in this function
    current_year, _ = self.cur_month_and_year_from_today()
    next_month = (self.today.replace(day=1) + timedelta(days=32)).replace(day=1).strftime('%m-%b')
    next_year = str(int(current_year) + 1) if next_month == '01-Jan' else current_year
    return (next_year, next_month) if next_month == '01-Jan' else (current_year, next_month)

# @dev: previously called `wrapper` during dev
def end_of_month_operations(self, parent_dir):
    next_or_cur_year, next_month = self.get_year_and_month()
    month_dir = self.create_and_return_directory_path(parent_dir, next_or_cur_year, next_month)
    target_output_path = os.path.join(self.root_dir, month_dir)
    self.create_directory(target_output_path)

def month_and_year_handler(self, first_flow=False):
    try:
        if self.is_last_day_of_month():
            parent_dir = get_doc_type_dir('INV') if first_flow else self.company_dir
            self.end_of_month_operations(parent_dir)
        else:
            print('Not the last day of the month.')
    except Exception as e:
        print(f'Exception: {e}')
