import os
import platform

# A configuration dictionary to store paths
config = {
    "data_dir": "",
    "log_dir": "",
    "temp_dir": ""
}

# Get the current operating system
os_type = platform.system()

# print(os_type) # Darwin on M1



if os_type == 'Windows':
    config["data_dir"] = "C:\\path\\to\\data\\dir"
    config["log_dir"] = "C:\\path\\to\\log\\dir"
    config["temp_dir"] = "C:\\path\\to\\temp\\dir"
else:  # Assume Unix-based system (like MacOS or Linux)
    config["data_dir"] = "/path/to/data/dir"
    config["log_dir"] = "/path/to/log/dir"
    config["temp_dir"] = "/path/to/temp/dir"

# Now you can use these paths in your code
data_file = os.path.join(config["data_dir"], "mydata.txt")

# Suppose you have a function that requires a file path
def process_data(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    # do something with data...
    pass

# You can now call this function with the correct file path,
# regardless of the operating system.
process_data(data_file)
