#!/bin/bash
# Run this ONCE after you have your Gumroad URL.
# Usage: ./LAUNCH.sh https://ctavolazzi.gumroad.com/l/your-product-id
#
# What it does:
#   1. Sets PURCHASE_URL in the book page (activates the buy button)
#   2. Commits that change on book-launch
#   3. Merges book-launch → main
#   4. Pushes main to GitHub

set -e

if [ -z "$1" ]; then
  echo "Usage: ./LAUNCH.sh <gumroad-url>"
  exit 1
fi

GUMROAD_URL="$1"

echo "Setting PURCHASE_URL to: $GUMROAD_URL"

# Swap the empty PURCHASE_URL constant
sed -i '' "s|const PURCHASE_URL = '';|const PURCHASE_URL = '$GUMROAD_URL';|" src/routes/book/+page.svelte

git add src/routes/book/+page.svelte
git commit -m "launch: set Gumroad URL — book is live"

git checkout main
git merge book-launch --no-edit

git push origin main

echo ""
echo "Done. Book is live."
echo "Gumroad: $GUMROAD_URL"
echo "Site: push complete — if Vercel/Cloudflare is wired to main, it deploys now."
