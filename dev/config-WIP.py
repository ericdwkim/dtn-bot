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

    # Determine the OS
    os_type = platform.system()

    # Set the base directory according to local machine's OS
    # if os_type == 'Windows':
    #     regex_pattern_to_document_type_root_directory_map = {
            # ('CCM') # TODO: use actual regex syntax pattern as key? does that work?

        # }




# main.py
# import config

# config.setup_config()

# The rest of your main script here...


setup_config()


"""
The `file_path_mappings` variable is essentially a three-level deep dictionary which allows us to directly map from a document's regular expression pattern and a company's ID to the corresponding file path.

The structure of the dictionary is as follows:

```python
file_path_mappings = {
    regex_pattern: {
        company_id: corresponding_file_path,
        ...
    },
    ...
}
```

This structure allows you to easily and quickly lookup the correct file path given the regex pattern and the company ID. This is particularly useful as it ensures you only need to reference these two key details (regex pattern and company ID) when working with your data, rather than having to manually piece together parts of the path yourself.

To explain the construction of `file_path_mappings`:

1. `for regex_pattern, root_dir in regex_pattern_to_document_type_root_directory_mapping.items()`: This outer loop iterates over each key-value pair in your regex pattern to root directory mapping. The key is the regex pattern and the value is the root directory path.

2. `for company_id, subdir in company_id_to_subdir_mapping.items()`: This inner loop iterates over each key-value pair in your company ID to subdirectory mapping. The key is the company ID and the value is the subdirectory.

3. `os.path.join(root_dir, subdir)`: This joins together the root directory and the subdirectory to form the full file path.

4. `{company_id: os.path.join(root_dir, subdir) for company_id, subdir in company_id_to_subdir_mapping.items()}`: This forms a new dictionary where the key is the company ID and the value is the full file path.

5. `{regex_pattern: {...} for regex_pattern, root_dir in ...}`: Finally, this forms the outer dictionary where the key is the regex pattern and the value is the dictionary created in step 4.

The reason for using this nested mapping data structure is because it provides a clear and direct way to get from a document's regex pattern and a company's ID to the required file path. It encapsulates all the information we need into one variable which makes it easy to manage and reference throughout the code. The use of built-in Python data structures and functions like dictionaries and `os.path.join()` also ensures that this approach is efficient and OS-agnostic.



------------------------------------------
The time complexity of constructing the `file_path_mappings` dictionary is mainly determined by the two nested loops. If `n` is the number of items in the `regex_pattern_to_document_type_root_directory_mapping` dictionary and `m` is the number of items in the `company_id_to_subdir_mapping` dictionary, then the overall time complexity would be O(n*m) because for each item in the `regex_pattern_to_document_type_root_directory_mapping` dictionary, you are iterating over each item in the `company_id_to_subdir_mapping` dictionary. This is a typical time complexity when you have nested loops.

However, once the `file_path_mappings` dictionary has been constructed, looking up a file path given a regex pattern and a company ID is very efficient. In a Python dictionary, these lookup operations are generally O(1), or constant time complexity, which means it takes the same amount of time regardless of the size of the dictionary.

Therefore, although constructing the `file_path_mappings` dictionary might take some time if the input dictionaries are large, it's a cost that you pay only once. After the construction, all subsequent lookups are very efficient.
"""