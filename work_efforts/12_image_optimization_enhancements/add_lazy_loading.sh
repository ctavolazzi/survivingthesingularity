#!/bin/bash

# This script adds loading="lazy" attribute to <img> tags that don't have it
# It automatically skips images that should be loaded eagerly (above the fold)

echo "Adding lazy loading attribute to images..."

# Define patterns for images that should NOT be lazy loaded (critical above-the-fold images)
# These are images like logos, hero images, or other critical content
critical_patterns=(
  "navbar.*logo"
  "hero"
  "loading=\"eager\""
  "cover.*loading"
)

# Read from the non-lazy images log
log_file="work_efforts/12_image_optimization_enhancements/non_lazy_images.txt"
temp_file="work_efforts/12_image_optimization_enhancements/temp_modified_files.txt"
modified_files=()

> "$temp_file" # Clear the temp file

# Process the log file
while IFS= read -r line; do
  if [[ "$line" == "File: "* ]]; then
    file="${line#File: }"
    current_file="$file"
  elif [[ "$line" == "Tag: "* ]]; then
    img_tag="${line#Tag: }"

    # Skip if this is a critical image that shouldn't be lazy-loaded
    skip=false
    for pattern in "${critical_patterns[@]}"; do
      if [[ "$img_tag" =~ $pattern ]]; then
        echo "Skipping critical image in $current_file: $img_tag"
        skip=true
        break
      fi
    done

    if [ "$skip" = false ]; then
      # Prepare the replacement - add loading="lazy" attribute before the closing >
      if [[ "$img_tag" == *"/>" ]]; then
        # Self-closing tag
        new_tag="${img_tag/\/>/ loading=\"lazy\" \/\>}"
      else
        # Regular tag
        new_tag="${img_tag/\>/ loading=\"lazy\" \>}"
      fi

      # Escape special characters for sed
      img_tag_escaped=$(echo "$img_tag" | sed 's/[\/&]/\\&/g')
      new_tag_escaped=$(echo "$new_tag" | sed 's/[\/&]/\\&/g')

      # Check if file has been modified already
      if [[ ! " ${modified_files[*]} " =~ " ${current_file} " ]]; then
        # Create a backup of the file
        cp "$current_file" "${current_file}.bak"
        modified_files+=("$current_file")
        echo "$current_file" >> "$temp_file"
      fi

      # Replace the tag in the file
      sed -i.tmp "s/$img_tag_escaped/$new_tag_escaped/g" "$current_file"

      echo "Added lazy loading to image in $current_file"
    fi
  fi
done < "$log_file"

# Clean up temporary files
find . -name "*.tmp" -delete

echo "Lazy loading has been added to images in the following files:"
cat "$temp_file"
echo "Backup files with .bak extension have been created."