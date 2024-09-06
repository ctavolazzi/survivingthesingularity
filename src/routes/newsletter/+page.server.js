import { readdirSync, readFileSync } from 'fs';
import { join } from 'path';
import { parseMarkdown } from '$lib/utils/markdownParser.js';

export async function load() {
  try {
    const newsletterDir = '/Users/ctavolazzi/Code/survivingthesingularity/src/lib/data/newsletters';
    const files = readdirSync(newsletterDir);

    if (files.length === 0) {
      console.log('No newsletter files found');
      return { latestNewsletter: null };
    }

    // Sort files by edition number
    const sortedFiles = files.sort((a, b) => {
      const editionA = parseInt(a.match(/\d+/)[0]);
      const editionB = parseInt(b.match(/\d+/)[0]);
      return editionB - editionA;
    });

    // Get the latest newsletter
    const latestNewsletter = sortedFiles[0];
    const latestNewsletterPath = join(newsletterDir, latestNewsletter);

    // Read and parse the latest newsletter
    const content = readFileSync(latestNewsletterPath, 'utf-8');
    const parsedContent = await parseMarkdown(content);

    return {
      latestNewsletter: {
        filename: latestNewsletter,
        content: parsedContent
      }
    };
  } catch (error) {
    console.error('Error loading newsletter:', error);
    return {
      latestNewsletter: null,
      error: 'Failed to load newsletter'
    };
  }
}