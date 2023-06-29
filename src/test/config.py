import os
import platform
from subprocess import run

def setup_config():

    # Run the shell script to delete PDF files from previous session
    # run(["../scripts/delete_pdf_files.sh"], shell=True)
    print(f'===========================================================================================')

    # Set environmental variables
    username = os.getenv('DTN_EMAIL_ADDRESS')
    password = os.getenv('DTN_PASSWORD')

    # Configuration setup code

# main.py
# import config

# config.setup_config()

# The rest of your main script here...


setup_config()