#!/usr/bin/env node
/**
 * Script to create a new blog post from the template
 * Run with: node scripts/create-blog-post.js "Your Post Title"
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// Get command line arguments
const title = process.argv[2];

if (!title) {
  console.error('Please provide a blog post title as an argument.');
  console.error('Example: node scripts/create-blog-post.js "My New Blog Post"');
  process.exit(1);
}

// Generate slug from title
const slug = title
  .toLowerCase()
  .replace(/[^\w\s]/g, '')
  .replace(/\s+/g, '-');

// Get directory paths for ES modules
const __dirname = dirname(fileURLToPath(import.meta.url));
const templateDir = join(__dirname, '../src/lib/templates/blog-post-template');
const postsDir = join(__dirname, '../src/lib/data/blog-posts', slug);
const blogImagePath = join(__dirname, '../static/images/blog');

// Check if post already exists
if (existsSync(postsDir)) {
  console.error(`A blog post with the slug "${slug}" already exists.`);
  process.exit(1);
}

// Create new post directory and ensure the blog image directory exists
mkdirSync(postsDir, { recursive: true });
mkdirSync(blogImagePath, { recursive: true });

// Create a placeholder image file
const placeholderImagePath = join(blogImagePath, `${slug}.jpg`);
if (!existsSync(placeholderImagePath)) {
  // Create an empty placeholder image file
  writeFileSync(placeholderImagePath, '');
  console.log(`Created placeholder image at: ${placeholderImagePath}`);
}

// Read template files
const templateContent = readFileSync(join(templateDir, 'content.md'), 'utf8');
const templateIndex = readFileSync(join(templateDir, 'index.js'), 'utf8');

// Get current date
const currentDate = new Date().toISOString().split('T')[0];

// Replace placeholders in content.md
const newContent = templateContent
  .replace(/Title of Your Blog Post/g, title)
  .replace(/2023-01-01/g, currentDate)
  .replace(/Your Name/g, 'Christopher Tavolazzi') // Default author
  .replace(/A short excerpt of your blog post \(optional\)/g, `${title} - Learn more about this topic...`);

// Replace placeholders in index.js
const newIndex = templateIndex
  .replace(/Title of Your Blog Post/g, title)
  .replace(/2023-01-01/g, currentDate)
  .replace(/Your Name/g, 'Christopher Tavolazzi') // Default author
  .replace(/A short excerpt of your blog post \(optional\)/g, `${title} - Learn more about this topic...`)
  .replace(/your-post-slug/g, slug);

// Write the new files
writeFileSync(join(postsDir, 'content.md'), newContent);
writeFileSync(join(postsDir, 'index.js'), newIndex);

console.log(`Successfully created new blog post: ${title}`);
console.log(`Slug: ${slug}`);
console.log(`Files created at: ${postsDir}`);
console.log('');
console.log('Next steps:');
console.log(`1. Edit the content in: ${join(postsDir, 'content.md')}`);
console.log(`2. Update metadata in: ${join(postsDir, 'index.js')}`);
console.log(`3. Replace the placeholder image at: ${placeholderImagePath}`);