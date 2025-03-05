#!/usr/bin/env node

/**
 * Newsletter Creation Script
 *
 * This script creates a new newsletter edition file with the correct naming
 * and populated with the newsletter template.
 *
 * Usage:
 *   node create-newsletter.js "My Newsletter Title"
 *
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Get title from command line argument
const title = process.argv[2];

if (!title) {
  console.error('Please provide a newsletter title.');
  console.error('Usage: node create-newsletter.js "My Newsletter Title"');
  process.exit(1);
}

// Constants
const NEWSLETTERS_DIR = path.join(__dirname, '..', 'src', 'lib', 'data', 'newsletters');
const TEMPLATE_PATH = path.join(__dirname, '..', 'src', 'lib', 'components', 'NewsletterTemplate.md');

// Create newsletters directory if it doesn't exist
if (!fs.existsSync(NEWSLETTERS_DIR)) {
  fs.mkdirSync(NEWSLETTERS_DIR, { recursive: true });
}

// Get current date in YYYY-MM-DD format
const today = new Date().toISOString().split('T')[0];

// Find the highest edition number
const existingNewsletters = fs.readdirSync(NEWSLETTERS_DIR)
  .filter(file => file.startsWith('newsletter-edition-') && file.endsWith('.md'));

let highestEdition = 0;
existingNewsletters.forEach(file => {
  const match = file.match(/newsletter-edition-(\d+)\.md/);
  if (match && match[1]) {
    const edition = parseInt(match[1], 10);
    if (edition > highestEdition) {
      highestEdition = edition;
    }
  }
});

// New edition number with padding
const newEdition = highestEdition + 1;
const paddedEdition = String(newEdition).padStart(3, '0');

// Create new filename
const newFilename = `newsletter-edition-${paddedEdition}.md`;
const newFilePath = path.join(NEWSLETTERS_DIR, newFilename);

// Read template and replace placeholders
let template = fs.readFileSync(TEMPLATE_PATH, 'utf8');
template = template.replace('[Newsletter Title]', title);
template = template.replace('Newsletter Title Here', title);
template = template.replace('YYYY-MM-DD', today);
template = template.replace(/XXX/g, paddedEdition);

// Write new file
fs.writeFileSync(newFilePath, template);

console.log(`✅ Created new newsletter edition: ${newFilename}`);
console.log(`📝 Path: ${newFilePath}`);
console.log('');
console.log('What\'s next?');
console.log('1. Edit the file to add your content');
console.log('2. Run your dev server to preview: npm run dev');
console.log('3. Visit: http://localhost:5173/newsletter');
console.log('');

// Try to open the file in the default editor
try {
  if (process.platform === 'win32') {
    execSync(`start ${newFilePath}`);
  } else if (process.platform === 'darwin') {
    execSync(`open ${newFilePath}`);
  } else {
    execSync(`xdg-open ${newFilePath}`);
  }
} catch (error) {
  console.log(`You can open the file manually at: ${newFilePath}`);
}