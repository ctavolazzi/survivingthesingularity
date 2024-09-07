import { error } from '@sveltejs/kit';
import { readdir, readFile } from 'fs/promises';
import { join } from 'path';
import { parseMarkdown } from '$lib/utils/markdownParser.js';

export async function load({ params }) {
  const { slug } = params;
  const newsletterDir = join(process.cwd(), 'src', 'lib', 'data', 'newsletters');

  try {
    const files = await readdir(newsletterDir);
    const allNewsletters = await Promise.all(
      files
        .filter(file => file.endsWith('.md'))
        .map(async file => {
          const content = await readFile(join(newsletterDir, file), 'utf-8');
          const { metadata } = await parseMarkdown(content);
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

    const filePath = join(newsletterDir, `${slug}.md`);
    const content = await readFile(filePath, 'utf-8');
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