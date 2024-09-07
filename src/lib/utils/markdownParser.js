// src/lib/utils/markdownParser.js
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkHtml from 'remark-html';
import { visit } from 'unist-util-visit';
import slugify from 'slugify'; // Add this import

// Custom plugin to handle our component placeholders
function customComponentPlugin() {
  return (tree) => {
    visit(tree, 'paragraph', (node) => {
      if (node.children.length === 1 && node.children[0].type === 'text') {
        const text = node.children[0].value;
        if (text === '{{NewsletterSignup}}') {
          node.type = 'html';
          node.value = '<svelte:component this={NewsletterSignup} />';
        } else if (text === '{{SkoolGroup}}') {
          node.type = 'html';
          node.value = '<svelte:component this={SkoolGroup} />';
        }
      }
    });
  };
}

// Add this new plugin
function tableOfContentsPlugin() {
  return (tree, file) => {
    const toc = [];
    visit(tree, 'heading', (node) => {
      if (node.depth === 2 || node.depth === 3) {
        const text = node.children.map(n => n.value).join('');
        const id = slugify(text, { lower: true });
        toc.push({ id, text, level: node.depth });
        node.data = node.data || {};
        node.data.hProperties = node.data.hProperties || {};
        node.data.hProperties.id = id;
      }
    });
    file.data.toc = toc;
  };
}

// Add this new plugin
function footnoteLinksPlugin() {
  return (tree) => {
    visit(tree, 'link', (node) => {
      // Check if the link text matches a footnote pattern (e.g., [1], [2], etc.)
      if (node.children.length === 1 && 
          node.children[0].type === 'text' && 
          /^\[\d+\]$/.test(node.children[0].value)) {
        // Add properties to open link in new tab
        node.data = node.data || {};
        node.data.hProperties = node.data.hProperties || {};
        node.data.hProperties.target = '_blank';
        node.data.hProperties.rel = 'noopener noreferrer';
      }
    });
  };
}

export async function parseMarkdown(content) {
  try {
    const lines = content.split('\n');
    let title = '';
    let date = '';
    let editionNumber = '';
    let description = '';

    // Extract title, edition number, date, and description
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (line.startsWith('# ')) {
        title = line.substring(2);
      } else if (line.startsWith('## Issue #')) {
        editionNumber = line.split('#')[2].trim();
      } else if (line.startsWith('### Date:')) {
        date = line.substring(9).trim(); // Remove "### Date: " prefix
      } else if (line.startsWith('#### Description:')) {
        description = line.substring(17).trim(); // Remove "#### Description: " prefix
        break; // Stop after finding the description
      }
    }

    const metadata = { title, date, editionNumber, description };

    // Parse the content and generate HTML
    const file = await unified()
      .use(remarkParse)
      .use(tableOfContentsPlugin)
      .use(customComponentPlugin)
      .use(footnoteLinksPlugin)
      .use(remarkHtml, { sanitize: false }) // Disable sanitization to allow custom attributes
      .process(content);

    return { 
      metadata, 
      htmlContent: file.toString(),
      toc: file.data.toc
    };
  } catch (error) {
    console.error('Error parsing markdown:', error);
    return {
      metadata: { title: 'Error', date: '', editionNumber: '', description: '' },
      htmlContent: '<p>There was an error parsing this newsletter. Please try again later.</p>',
      toc: []
    };
  }
}