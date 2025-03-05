import { marked } from 'marked';
import { dev } from '$app/environment';

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
 * This version uses the pre-processed blog posts from blogPosts.js
 */
export function getAllPosts() {
  try {
    // In a Cloudflare environment, we'll rely on the pre-processed blog posts
    // This function will be called by the dynamic import in +page.server.js
    return []; // Return empty array - the actual posts will be loaded via loadBlogPosts()
  } catch (err) {
    console.error('Error getting all posts:', err);
    return [];
  }
}

/**
 * Get a single post by its slug
 * This version uses the pre-processed blog posts from blogPosts.js
 */
export function getPostBySlug(slug) {
  try {
    // In a Cloudflare environment, we'll rely on the pre-processed blog posts
    // This function will be called by the dynamic import in +page.server.js
    return null; // Return null - the actual post will be loaded via the imported posts
  } catch (err) {
    console.error(`Error getting post by slug (${slug}):`, err);
    return null;
  }
}