#!/bin/bash

# Script to convert PNG and JPG images to WebP format
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

# Create log directory if it doesn't exist
mkdir -p logs

# Start log file
LOG_FILE="logs/conversion_$(date +%Y%m%d_%H%M%S).log"
echo "WebP Conversion Log - $(date)" > $LOG_FILE
echo "=================================" >> $LOG_FILE

# Process static directory images
echo "Converting images in static directory..."
echo "Converting images in static directory..." >> $LOG_FILE

# Convert PNG images in static root
find static -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | while read file; do
  convert_image "$file"
  echo "Converted: $file" >> $LOG_FILE
done

# Convert images in static/images
find static/images -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | while read file; do
  convert_image "$file"
  echo "Converted: $file" >> $LOG_FILE
done

# Convert images in static/future-projections
find static/future-projections -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | while read file; do
  convert_image "$file"
  echo "Converted: $file" >> $LOG_FILE
done

echo "Conversion complete! See $LOG_FILE for details."