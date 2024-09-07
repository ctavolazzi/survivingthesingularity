import { error } from '@sveltejs/kit';
import { parseMarkdown } from '$lib/utils/markdownParser.js';

const newsletterFiles = import.meta.glob('/src/lib/data/newsletters/*.md', { query: '?raw', import: 'default' });

export async function load() {
  try {
    const newsletters = await Promise.all(
      Object.entries(newsletterFiles).map(async ([path, loader]) => {
        const content = await loader();
        const { metadata, htmlContent } = await parseMarkdown(content);
        
        const file = path.split('/').pop();
        const editionNumber = file.match(/\d+/)[0];
        
        return {
          slug: file.replace('.md', ''),
          title: metadata.title,
          date: metadata.date,
          description: metadata.description,
          content: htmlContent,
          editionNumber: parseInt(editionNumber, 10)
        };
      })
    );

    // Sort newsletters by edition number, descending
    newsletters.sort((a, b) => b.editionNumber - a.editionNumber);

    const latestNewsletter = newsletters[0];

    return { 
      newsletters,
      latestNewsletter
    };
  } catch (e) {
    console.error('Error loading newsletters:', e);
    throw error(500, 'Unable to load newsletters');
  }
}

export const prerender = true;