import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { marked } from 'marked';

// Get directory path for ES modules
const __dirname = dirname(fileURLToPath(import.meta.url));
const contentDirectory = join(__dirname, '../../lib/data/blog-posts');

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
 * Get all blog posts with metadata
 */
export function getAllPosts() {
  try {
    // Look for subdirectories with content.md files instead of direct .md files
    const postDirs = readdirSync(contentDirectory, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .map(dirent => dirent.name);

    return postDirs
      .map(dir => {
        try {
          const contentPath = join(contentDirectory, dir, 'content.md');
          if (!existsSync(contentPath)) return null;

          const fileContent = readFileSync(contentPath, 'utf8');
          // Import the post data from the index.js file
          const indexPath = join(contentDirectory, dir, 'index.js');
          const slug = dir; // Use directory name as slug

          // If we don't have access to dynamic imports, we can at least return basic content
          return {
            slug,
            content: fileContent,
            excerpt: fileContent.substring(0, 200).replace(/[#*[\]_]/g, '') + '...',
            // These would normally come from index.js but we can't import it directly here
            // Add any metadata that might be available in the frontmatter
            ...(parseFrontmatter(fileContent).data || {})
          };
        } catch (error) {
          console.error(`Error processing post directory ${dir}:`, error);
          return null;
        }
      })
      .filter(post => post !== null)
      .sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));
  } catch (error) {
    console.error('Error loading blog posts:', error);
    return [];
  }
}

/**
 * Get a single post by slug
 */
export function getPostBySlug(slug) {
  try {
    const postDir = join(contentDirectory, slug);
    const contentPath = join(postDir, 'content.md');

    if (!existsSync(contentPath)) {
      return null;
    }

    const fileContent = readFileSync(contentPath, 'utf8');
    const { data, content } = parseFrontmatter(fileContent);
    const htmlContent = marked(content);

    return {
      ...data,
      slug,
      content: htmlContent,
      rawContent: content
    };
  } catch (error) {
    console.error(`Error loading post ${slug}:`, error);
    return null;
  }
}