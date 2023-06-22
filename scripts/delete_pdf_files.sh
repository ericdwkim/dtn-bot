#!/bin/bash

# List of directories to search for PDF files
directories=(

  "/Users/ekim/Downloads"

  "/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/CVR Supply & Trading 12351"
  "/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Invoices/5-May"
  "/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/VALERO [10006]"
  "/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/EXXONMOBIL [10005]"
  "/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Fuel Drafts/U S VENTURE - U S OIL COMPANY [12262]"

  '/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/CVR Supply & Trading 12351'
  '/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/EXXONMOBIL [10005]'
  '/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/U S VENTURE - U S OIL COMPANY [12262]'
  '/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/VALERO [10006]'
  '/Users/ekim/workspace/txb/mock/K-Drive/DTN Reports/Credit Cards/DK TRADING [12293]'
)

# Iterate through each directory
for dir in "${directories[@]}"; do
  # Check if the directory exists
  if [ -d "$dir" ]; then
    echo "Searching for PDF files in $dir..."

    # Find and delete PDF files within the directory
    find "$dir" -type f -name "*.pdf" -delete

    echo "Deleted PDF files in $dir"
  else
    echo "Directory $dir does not exist."
  fi
done

