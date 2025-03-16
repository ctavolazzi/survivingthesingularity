#!/bin/bash

# cleanup_redundant_images.sh
# This script removes redundantly generated images from the optimization process
# that have multiple size indicators (e.g., image_800_400_200.png)

echo "🔍 Starting cleanup of redundant image variants..."

# Directory where optimized images are stored
OPTIMIZED_DIR="static/images/optimized"

# Create a backup directory
BACKUP_DIR="work_efforts/12_image_optimization_enhancements/deleted_images_backup/$(date +"%Y%m%d_%H%M%S")"
mkdir -p "$BACKUP_DIR"
echo "📁 Backup directory created: $BACKUP_DIR"

# Track files deleted
FILES_DELETED=0
SPACE_SAVED=0

# Function to convert bytes to human-readable format
function human_readable_size() {
  local size=$1
  local units=("B" "KB" "MB" "GB" "TB")
  local unit=0

  while (( size > 1024 )); do
    size=$(( size / 1024 ))
    (( unit++ ))
  done

  echo "$size ${units[$unit]}"
}

# Function to get file size in bytes
function get_file_size() {
  stat -f %z "$1" 2>/dev/null || stat --format="%s" "$1" 2>/dev/null
}

# Function to delete redundant image files
function delete_redundant_images() {
  # Find files with multiple size indicators (more than one underscore followed by numbers)
  while IFS= read -r file; do
    # Skip if file doesn't exist (might have been deleted already)
    [ ! -f "$file" ] && continue

    # Extract filename
    filename=$(basename "$file")

    # Count number of size patterns (like _400, _800, etc.)
    size_patterns=$(echo "$filename" | grep -o "_[0-9]\+" | wc -l)

    # If the file has more than one size pattern, it's redundant
    if [ "$size_patterns" -gt 1 ]; then
      # Get file size before deleting
      file_size=$(get_file_size "$file")

      # Copy to backup before deleting
      cp "$file" "$BACKUP_DIR/"

      # Delete the file
      rm "$file"

      echo "🗑️  Deleted: $file ($(human_readable_size $file_size))"
      ((FILES_DELETED++))
      ((SPACE_SAVED+=file_size))
    fi
  done < <(find "$OPTIMIZED_DIR" -type f)
}

# Run the cleanup
if [ -d "$OPTIMIZED_DIR" ]; then
  delete_redundant_images

  echo "============================"
  echo "🎉 Deleted $FILES_DELETED redundant image files"
  echo "💾 Space saved: $(human_readable_size $SPACE_SAVED)"
  echo "📁 Backups saved to: $BACKUP_DIR"
  echo "============================"
else
  echo "❌ Optimized images directory not found: $OPTIMIZED_DIR"
fi

echo "✨ Cleanup complete!"