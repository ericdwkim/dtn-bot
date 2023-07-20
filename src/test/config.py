import os
import platform
from subprocess import run

def setup_config():

    # Run the shell script to delete PDF files from previous session
    # run(["../scripts/delete_for_accpt_test.sh"], shell=True)
    print(f'===========================================================================================')

    # Set environmental variables
    username = os.getenv('DTN_EMAIL_ADDRESS')
    password = os.getenv('DTN_PASSWORD')



setup_config()