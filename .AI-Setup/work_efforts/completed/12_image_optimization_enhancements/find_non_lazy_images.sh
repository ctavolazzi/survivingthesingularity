#!/bin/bash

# This script searches for <img> tags in the codebase that don't have the loading="lazy" attribute
# It excludes node_modules and build directories

echo "Searching for <img> tags without lazy loading..."

# Define search patterns
img_pattern='<img[^>]*>'
lazy_pattern='loading="lazy"'

# Find all Svelte files
files=$(find src -type f -name "*.svelte" -not -path "*/node_modules/*" -not -path "*/.svelte-kit/*" -not -path "*/build/*")

# Create a log file
log_file="work_efforts/12_image_optimization_enhancements/non_lazy_images.txt"
echo "Images without lazy loading ($(date))" > "$log_file"
echo "==================================" >> "$log_file"

# Counter for images found
count=0

# Process each file
for file in $files; do
  # Extract all img tags
  img_tags=$(grep -o "$img_pattern" "$file" || true)

  if [ -n "$img_tags" ]; then
    # Check each img tag for missing lazy loading
    while IFS= read -r img_tag; do
      if [[ ! "$img_tag" =~ $lazy_pattern ]]; then
        echo "File: $file" >> "$log_file"
        echo "Tag: $img_tag" >> "$log_file"
        echo "-------------------" >> "$log_file"
        ((count++))
      fi
    done <<< "$img_tags"
  fi
done

echo "Found $count images without lazy loading."
echo "Results saved to $log_file"