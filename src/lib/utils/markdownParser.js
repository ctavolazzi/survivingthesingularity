import { marked } from 'marked';
import matter from 'gray-matter';

/**
 * Parse markdown content and extract metadata, table of contents, and HTML content
 * @param {string} content - Raw markdown content
 * @returns {Object} - Object containing metadata, table of contents, and HTML content
 */
export async function parseMarkdown(content) {
  // Extract frontmatter metadata using gray-matter
  const { data: frontmatter, content: markdownContent } = matter(content);

  // Initialize metadata object
  const metadata = {
    ...frontmatter
  };

  // If title is not in frontmatter, try to extract from first h1
  if (!metadata.title) {
    const titleMatch = markdownContent.match(/^#\s+(.+)$/m);
    if (titleMatch) {
      metadata.title = titleMatch[1].trim();
    }
  }

  // If date is not in frontmatter, try to extract from h3 that looks like a date
  if (!metadata.date) {
    const dateMatch = markdownContent.match(/^###\s+(.+\d{4})$/m);
    if (dateMatch) {
      metadata.date = dateMatch[1].trim();
    }
  }

  // Generate table of contents
  const toc = [];
  const headingRegex = /^(##|###)\s+(.+)$/gm;
  let match;

  while ((match = headingRegex.exec(markdownContent)) !== null) {
    const level = match[1].length - 1; // ## is level 2, ### is level 3
    const text = match[2].trim();
    const id = text.toLowerCase().replace(/[^\w]+/g, '-');

    toc.push({
      level,
      text,
      id
    });
  }

  // Process custom components
  let processedContent = markdownContent.replace(
    /{{(\w+)}}/g,
    (_, componentName) => `<svelte:component this={${componentName}} />`
  );

  // Convert markdown to HTML
  const htmlContent = marked.parse(processedContent);

  return {
    metadata,
    toc,
    htmlContent
  };
}