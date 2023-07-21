#!/bin/bash

# List of directories to search for PDF files
directories=(
  "/Users/ekim/Downloads"
)

# Iterate through each directory
for dir in "${directories[@]}"; do
  # Check if the directory exists
  if [ -d "$dir" ]; then
    echo "Searching for PDF files in $dir and its subdirectories..."

    # Find and delete PDF files within the directory and its subdirectories
    find "$dir" -type f -name "*.pdf" -delete

    echo "Deleted PDF files in $dir and its subdirectories"
  else
    echo "Directory $dir does not exist."
  fi
done
