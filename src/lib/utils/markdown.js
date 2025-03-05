import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync, readdirSync, readFileSync } from 'fs';
import { marked } from 'marked';
import { dev } from '$app/environment';

// Get directory path for ES modules
const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * Get the appropriate content directory path based on environment
 */
function getContentDirectory() {
  // Try different possible paths for blog posts
  const paths = [
    // Development path
    path.join(process.cwd(), 'src', 'lib', 'data', 'blog-posts'),
    // Build path in .svelte-kit
    path.join(process.cwd(), '.svelte-kit', 'output', 'server', 'chunks', 'lib', 'data', 'blog-posts'),
    // Fallback to relative path
    '../../lib/data/blog-posts'
  ];

  for (const p of paths) {
    try {
      if (fs.existsSync(p)) {
        console.log('Using content directory:', p);
        return p;
      }
    } catch (error) {
      // Ignore errors and try next path
    }
  }

  // Fallback to relative path
  console.log('Falling back to relative path for content directory');
  return '../../lib/data/blog-posts';
}

// Use contentDirectory function to determine the right path
const contentDirectory = getContentDirectory();

/**
 * Parse frontmatter from markdown content
 * Simple implementation that extracts YAML-like frontmatter between --- markers
 */
function parseFrontmatter(content) {
  const frontmatterRegex = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;
  const match = frontmatterRegex.exec(content);

  if (!match) {
    return {
      data: {},
      content
    };
  }

  const frontmatter = match[1];
  const markdown = match[2];

  // Parse frontmatter into object
  const data = {};
  frontmatter.split('\n').forEach(line => {
    const [key, ...valueParts] = line.split(':');
    if (key && valueParts.length > 0) {
      // Join value parts back with : in case the value itself contained colons
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
 * Get all blog posts with their metadata
 */
export function getAllPosts() {
  try {
    const posts = [];
    let directories;

    try {
      directories = readdirSync(contentDirectory)
        .filter(dir => !dir.startsWith('.') && existsSync(join(contentDirectory, dir, 'content.md')));
    } catch (err) {
      console.error(`Error reading content directory (${contentDirectory}):`, err);
      return [];
    }

    for (const dir of directories) {
      try {
        const contentPath = join(contentDirectory, dir, 'content.md');
        const content = readFileSync(contentPath, 'utf-8');
        const { metadata, markdown } = parseFrontmatter(content);

        if (metadata) {
          posts.push({
            ...metadata,
            slug: dir,
            excerpt: metadata.excerpt || markdown.substring(0, 150) + '...',
            content: markdown
          });
        }
      } catch (err) {
        console.error(`Error processing post ${dir}:`, err);
      }
    }

    // Sort posts by date in descending order
    return posts.sort((a, b) => new Date(b.date) - new Date(a.date));
  } catch (err) {
    console.error('Error getting all posts:', err);
    return [];
  }
}

/**
 * Get a single post by its slug
 */
export function getPostBySlug(slug) {
  try {
    const contentPath = join(contentDirectory, slug, 'content.md');

    if (!existsSync(contentPath)) {
      console.error(`Post not found: ${slug}`);
      return null;
    }

    const content = readFileSync(contentPath, 'utf-8');
    const { metadata, markdown } = parseFrontmatter(content);

    if (!metadata) {
      console.error(`Invalid metadata in post: ${slug}`);
      return null;
    }

    // Convert markdown to HTML
    const html = marked(markdown);

    return {
      ...metadata,
      slug,
      content: markdown,
      html
    };
  } catch (err) {
    console.error(`Error getting post by slug (${slug}):`, err);
    return null;
  }
}