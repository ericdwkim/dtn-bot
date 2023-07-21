#!/bin/bash

# Directory to search for PDF files
directory="/Users/ekim/Downloads"

# Check if the directory exists
if [ -d "$directory" ]; then
  echo "Searching for PDF files in $directory and its subdirectories..."

  # Find and delete PDF files within the directory and its subdirectories
  find "$directory" -type f -name "*.pdf" -delete

  echo "Deleted PDF files in $directory and its subdirectories"
else
  echo "Directory $directory does not exist."
fi
