#!/bin/bash

input_dir="domain_name"

#Iterate through each file in the input directory
for file in "$input_dir"/*; do
    if [[ -f "$file" ]]; then
        echo "Processing $file"

        # Call nslookup script
        ./nslookup "$file" &
    fi
done

echo "All files processed."
