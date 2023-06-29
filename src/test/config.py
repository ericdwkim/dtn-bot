import os
import platform
from subprocess import run

def setup_config():
    # Your configuration setup code here...
    run(["../scripts/delete_pdf_files.sh"], shell=True)
    print(f'===========================================================================================')


# main.py
# import config

# config.setup_config()

# The rest of your main script here...


setup_config()