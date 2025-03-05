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

        // Skip README.md file
        if (file === 'README.md') {
          return null;
        }

        const editionNumber = file.match(/\d+/)?.[0] || '0';

        return {
          slug: file.replace('.md', ''),
          title: metadata.title,
          date: metadata.date,
          description: metadata.description,
          editionNumber: parseInt(editionNumber, 10)
        };
      })
    );

    // Filter out null entries and sort
    const validNewsletters = allNewsletters.filter(n => n !== null);
    validNewsletters.sort((a, b) => b.editionNumber - a.editionNumber);

    // Find the path that ends with the slug
    const filePath = Object.keys(newsletterFiles).find(path => path.endsWith(`/${slug}.md`));

    if (!filePath) {
      console.error(`Newsletter file not found for slug: ${slug}`);
      throw error(404, 'Newsletter not found');
    }

    const newsletterLoader = newsletterFiles[filePath];
    const content = await newsletterLoader();
    const { metadata, htmlContent } = await parseMarkdown(content);

    return {
      newsletter: {
        slug,
        title: metadata.title,
        date: metadata.date,
        content: htmlContent
      },
      allNewsletters: validNewsletters
    };
  } catch (e) {
    console.error(`Error loading newsletter ${slug}:`, e);
    throw error(404, 'Newsletter not found');
  }
}