import { error } from '@sveltejs/kit';
import { parseMarkdown } from '$lib/utils/markdownParser.js';

// Use glob import for all newsletter files
const newsletterFiles = import.meta.glob('/src/lib/data/newsletters/*.md', { query: '?raw', import: 'default' });

export async function load({ url, isPrerendering }) {
  try {
    // Default values for pagination
    let page = 1;
    let perPage = 10;

    // Only try to access searchParams if not prerendering
    if (!isPrerendering && url.searchParams) {
      page = parseInt(url.searchParams.get('page') || '1', 10);
      perPage = parseInt(url.searchParams.get('perPage') || '10', 10);
    }

    // Load all newsletter metadata
    const newsletters = await Promise.all(
      Object.entries(newsletterFiles).map(async ([path, loader]) => {
        const content = await loader();
        const { metadata } = await parseMarkdown(content);

        const file = path.split('/').pop();
        // Skip README.md file
        if (file === 'README.md') {
          return null;
        }

        const editionNumber = file.match(/\d+/)?.[0] || '0';

        return {
          slug: file.replace('.md', ''),
          title: metadata.title,
          date: metadata.date,
          description: metadata.description || metadata.excerpt || '',
          editionNumber: parseInt(editionNumber, 10)
        };
      })
    );

    // Filter out null entries (README.md) and sort by edition number
    const validNewsletters = newsletters.filter(n => n !== null);

    // Handle case where no newsletters exist
    if (validNewsletters.length === 0) {
      return {
        newsletters: [],
        latestNewsletter: {
          title: "No Newsletters Yet",
          date: new Date().toISOString().split('T')[0],
          content: "<p>There are no newsletters available yet. Check back soon!</p>",
          slug: "none"
        },
        pagination: {
          currentPage: 1,
          totalPages: 1,
          totalItems: 0,
          perPage
        }
      };
    }

    // Sort newsletters by edition number, descending (newest first)
    validNewsletters.sort((a, b) => b.editionNumber - a.editionNumber);

    // Calculate pagination
    const totalNewsletters = validNewsletters.length;
    const totalPages = Math.ceil(totalNewsletters / perPage);

    // Apply pagination
    const paginatedNewsletters = validNewsletters.slice((page - 1) * perPage, page * perPage);

    // Get the latest newsletter content
    const latestNewsletter = validNewsletters[0];
    if (latestNewsletter) {
      const path = Object.keys(newsletterFiles).find(p => p.endsWith(`/${latestNewsletter.slug}.md`));
      if (path) {
        const content = await newsletterFiles[path]();
        const { htmlContent } = await parseMarkdown(content);
        latestNewsletter.content = htmlContent;
      }
    }

    return {
      newsletters: paginatedNewsletters,
      latestNewsletter,
      pagination: {
        currentPage: page,
        totalPages,
        totalItems: totalNewsletters,
        perPage
      }
    };
  } catch (e) {
    console.error('Error loading newsletters:', e);
    throw error(500, 'Unable to load newsletters');
  }
}

// Disable prerendering for this page
export const prerender = false;