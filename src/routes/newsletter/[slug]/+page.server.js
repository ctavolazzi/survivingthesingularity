import { error } from '@sveltejs/kit';
import { parseMarkdown } from '$lib/utils/markdownParser.js';

const newsletterFiles = import.meta.glob('/src/lib/data/newsletters/*.md', { query: '?raw', import: 'default' });

export async function load({ params }) {
  const { slug } = params;

  try {
    const allNewsletters = await Promise.all(
      Object.entries(newsletterFiles).map(async ([path, loader]) => {
        const content = await loader();
        const { metadata } = await parseMarkdown(content);
        const file = path.split('/').pop();
        const editionNumber = file.match(/\d+/)[0];
        
        return {
          slug: file.replace('.md', ''),
          title: metadata.title,
          date: metadata.date,
          description: metadata.description,
          editionNumber: parseInt(editionNumber, 10)
        };
      })
    );

    allNewsletters.sort((a, b) => b.editionNumber - a.editionNumber);

    const newsletterLoader = newsletterFiles[`/src/lib/data/newsletters/${slug}.md`];
    if (!newsletterLoader) {
      throw error(404, 'Newsletter not found');
    }

    const content = await newsletterLoader();
    const { metadata, htmlContent } = await parseMarkdown(content);
    
    return {
      newsletter: {
        slug,
        title: metadata.title,
        date: metadata.date,
        content: htmlContent
      },
      allNewsletters
    };
  } catch (e) {
    console.error(`Error loading newsletter ${slug}:`, e);
    throw error(404, 'Newsletter not found');
  }
}