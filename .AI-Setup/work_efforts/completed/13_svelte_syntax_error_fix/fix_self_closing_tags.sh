#!/bin/bash

# fix_self_closing_tags.sh
# This script finds and fixes incorrectly escaped self-closing tags in Svelte files
# Created as part of work effort 13: Svelte Syntax Error Fix

echo "🔍 Starting to scan for Svelte files with incorrectly escaped self-closing tags..."

# Directories to search in
DIRS_TO_SEARCH=(
  "src"
  "src/lib"
  "src/routes"
  "src/lib/components"
)

# Directories to exclude (optional)
DIRS_TO_EXCLUDE=(
  "node_modules"
  ".svelte-kit"
  "build"
)

# Track files fixed
FILES_FIXED=0
TOTAL_FIXES=0

# Create a backup directory
BACKUP_DIR="work_efforts/13_svelte_syntax_error_fix/backups/$(date +"%Y%m%d_%H%M%S")"
mkdir -p "$BACKUP_DIR"
echo "📁 Backup directory created: $BACKUP_DIR"

# Function to fix a file
fix_file() {
  local file=$1
  local original_content
  local new_content
  local fixes=0

  # Check if the file contains the pattern before reading it
  if grep -q "\/\\\>" "$file"; then
    # Create a backup of the original file
    cp "$file" "$BACKUP_DIR/$(basename "$file").bak"

    # Read file content
    original_content=$(cat "$file")

    # Replace the incorrect pattern with the correct one
    new_content=$(echo "$original_content" | sed 's/\/\\\>/\/>/g')

    # Count how many fixes were made
    fixes=$(echo "$original_content" | grep -o "\/\\\>" | wc -l)
    fixes=$(echo "$fixes" | tr -d '[:space:]')

    # Write the new content back to the file
    echo "$new_content" > "$file"

    echo "✅ Fixed $fixes issue(s) in: $file"
    ((FILES_FIXED++))
    ((TOTAL_FIXES+=fixes))
  fi
}

# Process all Svelte files in the project (using find with proper exclusions)
echo "🔎 Scanning all Svelte files in the project..."
find_cmd="find . -type f -name \"*.svelte\""

# Add exclusion patterns
for dir in "${DIRS_TO_EXCLUDE[@]}"; do
  find_cmd="$find_cmd -not -path \"*/$dir/*\""
done

# Run the find command and process each file
while IFS= read -r file; do
  fix_file "$file"
done < <(eval "$find_cmd")

echo "============================"
echo "🎉 Fixed $TOTAL_FIXES issue(s) in $FILES_FIXED file(s)"
echo "📁 Backups saved to: $BACKUP_DIR"
echo "============================"

# If no files were fixed, remove the empty backup directory
if [ "$FILES_FIXED" -eq 0 ]; then
  rmdir "$BACKUP_DIR"
  echo "No files needed fixing. Removed empty backup directory."
fi

echo "✨ Done!"