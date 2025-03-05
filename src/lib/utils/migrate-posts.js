/**
 * Utility to migrate blog posts from the old format (flat .md files in src/content/blog)
 * to the new format (content.md files in subdirectories of src/lib/data/blog-posts)
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// Get directory paths for ES modules
const __dirname = dirname(fileURLToPath(import.meta.url));
const oldContentDirectory = join(__dirname, '../../content/blog');
const newContentDirectory = join(__dirname, '../../lib/data/blog-posts');

/**
 * Parse frontmatter from markdown content
 */
function parseFrontmatter(content) {
  const frontmatterRegex = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;
  const match = frontmatterRegex.exec(content);

  if (!match) {
    return { data: {}, content };
  }

  const frontmatter = match[1];
  const markdown = match[2];

  // Parse frontmatter into object
  const data = {};
  frontmatter.split('\n').forEach(line => {
    const [key, ...valueParts] = line.split(':');
    if (key && valueParts.length > 0) {
      let value = valueParts.join(':').trim();

      // Remove quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.substring(1, value.length - 1);
      }

      data[key.trim()] = value;
    }
  });

  return { data, content: markdown };
}

/**
 * Migrate blog posts from old format to new format
 */
export function migrateOldPosts() {
  if (!existsSync(oldContentDirectory)) {
    console.log('Old content directory does not exist:', oldContentDirectory);
    return;
  }

  // Ensure the blog images directory exists
  const imagesDirectory = join(__dirname, '../../../static/images/blog');
  if (!existsSync(imagesDirectory)) {
    mkdirSync(imagesDirectory, { recursive: true });
    console.log('Created images directory:', imagesDirectory);
  }

  // Get all .md files in the old directory
  const files = readdirSync(oldContentDirectory)
    .filter(file => file.endsWith('.md'));

  if (files.length === 0) {
    console.log('No markdown files found in old directory:', oldContentDirectory);
    return;
  }

  // Process each file
  for (const file of files) {
    try {
      const oldFilePath = join(oldContentDirectory, file);
      const slug = file.replace('.md', '');
      const newDirPath = join(newContentDirectory, slug);

      // Create directory if it doesn't exist
      if (!existsSync(newDirPath)) {
        mkdirSync(newDirPath, { recursive: true });
      }

      // Read the old file
      const fileContent = readFileSync(oldFilePath, 'utf8');
      const { data, content } = parseFrontmatter(fileContent);

      // Write content.md
      const contentPath = join(newDirPath, 'content.md');
      writeFileSync(contentPath, fileContent);
      console.log(`Created content file: ${contentPath}`);

      // Create a placeholder image file if needed
      const imageFileName = `${slug}.jpg`;
      const imagePath = join(imagesDirectory, imageFileName);
      if (!existsSync(imagePath)) {
        // Create an empty placeholder image
        writeFileSync(imagePath, '');
        console.log(`Created placeholder image: ${imagePath}`);
      }

      // Create index.js with the correct path to content.md
      const indexContent = `// Auto-generated from migrated post
import content from './content.md?raw';

export const post = {
  title: ${JSON.stringify(data.title || slug)},
  date: ${JSON.stringify(data.date || new Date().toISOString().split('T')[0])},
  author: ${JSON.stringify(data.author || 'Anonymous')},
  authorAvatar: null, // Set to null explicitly to avoid 404 errors
  excerpt: ${JSON.stringify((data.excerpt || content.substring(0, 150).replace(/[\n\r"]/g, ' ')).trim() + '...')},
  imageUrl: ${JSON.stringify(data.image || data.imageUrl || `/images/blog/${slug}.jpg`)},
  tags: ${JSON.stringify(data.tags ? data.tags.split(',').map(tag => tag.trim()) : [])},
  content,
  slug: ${JSON.stringify(slug)}
};
`;
      const indexPath = join(newDirPath, 'index.js');
      writeFileSync(indexPath, indexContent);
      console.log(`Created index file: ${indexPath}`);

      console.log(`Successfully migrated post: ${slug}`);
    } catch (error) {
      console.error(`Error migrating post ${file}:`, error);
    }
  }

  // Update the blogPosts.js index file
  updateBlogPostsIndex();
}

/**
 * Update the blogPosts.js index file with all available posts
 */
function updateBlogPostsIndex() {
  try {
    // Skip if the directory doesn't exist yet
    if (!existsSync(newContentDirectory)) {
      return;
    }

    // Get all subdirectories in the blog posts directory
    const directories = readdirSync(newContentDirectory, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .map(dirent => dirent.name);

    // Generate the blogPosts.js file
    const imports = directories.map(dir => `import { post as ${dir.replace(/-/g, '_')} } from './${dir}/index.js';`).join('\n');
    const postsArray = `export const blogPosts = [${directories.map(dir => dir.replace(/-/g, '_')).join(', ')}];`;

    const content = `/**
 * This file is auto-generated by the migration script.
 * It imports all blog posts and exports them as an array.
 */

${imports}

${postsArray}
`;

    const indexPath = join(newContentDirectory, 'blogPosts.js');
    writeFileSync(indexPath, content);
    console.log(`Updated blog posts index at: ${indexPath}`);
  } catch (error) {
    console.error('Error updating blog posts index:', error);
  }
}

// Run the migration if this file is executed directly
if (import.meta.url === import.meta.main) {
  migrateOldPosts();
}