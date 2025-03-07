#!/usr/bin/env node

/**
 * Newsletter Creation Script
 *
 * This script creates a new newsletter edition component file with the correct naming
 * and populated with the newsletter template.
 *
 * Usage:
 *   node scripts/create-newsletter.js "My Newsletter Title"
 *
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

// Get the current file's directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Get title from command line argument
const title = process.argv[2];

if (!title) {
  console.error('Please provide a newsletter title.');
  console.error('Usage: node scripts/create-newsletter.js "My Newsletter Title"');
  process.exit(1);
}

// Constants
const COMPONENT_DIR = path.join(__dirname, '..', 'src', 'lib', 'components', 'newsletters');
const DATA_FILE = path.join(__dirname, '..', 'src', 'lib', 'data', 'newsletterData.js');
const TEMPLATE_PATH = path.join(__dirname, '..', 'src', 'lib', 'components', 'newsletters', 'NewsletterTemplate.svelte');

// Create newsletter components directory if it doesn't exist
if (!fs.existsSync(COMPONENT_DIR)) {
  fs.mkdirSync(COMPONENT_DIR, { recursive: true });
}

// Get current date in YYYY-MM-DD format
const today = new Date();
const formattedDate = today.toLocaleDateString('en-US', {
  month: 'long',
  day: 'numeric',
  year: 'numeric'
});

// Read the newsletter data file to find the highest edition number
let newsletterData = fs.readFileSync(DATA_FILE, 'utf8');
const editionMatch = newsletterData.match(/editionNumber: (\d+)/g);
let highestEdition = 0;

if (editionMatch) {
  editionMatch.forEach(match => {
    const edition = parseInt(match.replace('editionNumber: ', ''), 10);
    if (edition > highestEdition) {
      highestEdition = edition;
    }
  });
}

// New edition number with padding
const newEdition = highestEdition + 1;
const paddedEdition = String(newEdition).padStart(3, '0');

// Create new filename
const slug = `newsletter-edition-${paddedEdition}`;
const newFilename = `NewsletterEdition${paddedEdition}.svelte`;
const newFilePath = path.join(COMPONENT_DIR, newFilename);

// Read template and replace placeholders
let template = fs.readFileSync(TEMPLATE_PATH, 'utf8');
template = template.replace(/\[Newsletter Title\]/g, title);
template = template.replace(/#XXX/g, `#${newEdition}`);

// Write new component file
fs.writeFileSync(newFilePath, template);

// Update the newsletterData.js file
const newNewsletterEntry = `
  {
    slug: '${slug}',
    title: '${title}',
    date: '${formattedDate}',
    description: 'A brief summary of this newsletter edition.',
    editionNumber: ${newEdition}
  },`;

// Insert the new entry at the beginning of the newsletters array
const updatedNewsletterData = newsletterData.replace(
  /export const newsletters = \[/,
  `export const newsletters = [${newNewsletterEntry}`
);

// Write the updated data back to the file
fs.writeFileSync(DATA_FILE, updatedNewsletterData);

// Update the newsletterLoader.js file to import the new component
const loaderPath = path.join(__dirname, '..', 'src', 'lib', 'utils', 'newsletterLoader.js');
let loaderContent = fs.readFileSync(loaderPath, 'utf8');

// Add import statement
const importStatement = `import NewsletterEdition${paddedEdition} from '$lib/components/newsletters/NewsletterEdition${paddedEdition}.svelte';`;
loaderContent = loaderContent.replace(
  /\/\/ Import all newsletter components/,
  `// Import all newsletter components\n${importStatement}`
);

// Add component to mapping
const componentMapping = `  '${slug}': NewsletterEdition${paddedEdition},`;
loaderContent = loaderContent.replace(
  /const newsletterComponents = {/,
  `const newsletterComponents = {\n${componentMapping}`
);

// Write the updated loader back to the file
fs.writeFileSync(loaderPath, loaderContent);

console.log(`✅ Created new newsletter edition: ${newFilename}`);
console.log(`✅ Updated newsletter data in ${DATA_FILE}`);
console.log(`✅ Updated newsletter loader in ${loaderPath}`);
console.log(`📝 Component Path: ${newFilePath}`);
console.log('');
console.log('What\'s next?');
console.log('1. Edit the component file to add your content');
console.log('2. Update the description in the newsletterData.js file');
console.log('3. Run your dev server to preview: npm run dev');
console.log('4. Visit: http://localhost:5173/newsletter');
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