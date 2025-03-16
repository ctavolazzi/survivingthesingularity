#!/bin/bash

# Script to convert src/lib/images to WebP format
# This script preserves the original files and creates WebP versions alongside them

# Set the quality for WebP conversion (0-100)
QUALITY=80

# Function to convert a single image
convert_image() {
  local input_file=$1
  local output_file="${input_file%.*}.webp"

  echo "Converting: $input_file to $output_file"

  # Check if the file is a PNG (might have transparency)
  if [[ $input_file == *.png ]]; then
    cwebp -q $QUALITY -alpha_q 100 "$input_file" -o "$output_file"
  else
    cwebp -q $QUALITY "$input_file" -o "$output_file"
  fi

  # Check if conversion was successful
  if [ $? -eq 0 ]; then
    echo "  ✓ Converted successfully"

    # Calculate and display size reduction
    original_size=$(du -h "$input_file" | cut -f1)
    new_size=$(du -h "$output_file" | cut -f1)
    echo "  ✓ Size: $original_size -> $new_size"
  else
    echo "  ✗ Conversion failed"
  fi
}

# Process src/lib/images directory
echo "Converting images in src/lib/images directory..."

# Convert images in src/lib/images
find src/lib/images -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | while read file; do
  # Skip svelte-welcome.webp which is already in WebP format
  if [[ "$file" != *"svelte-welcome"* ]]; then
    convert_image "$file"
  fi
done

echo "Conversion complete!"