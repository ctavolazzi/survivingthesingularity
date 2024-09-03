import { readFile } from 'fs/promises';
import { join } from 'path';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
  try {
    const bookPath = join(process.cwd(), 'src', 'lib', 'data', 'book', 'book.json');
    const bookContent = await readFile(bookPath, 'utf-8');
    const book = JSON.parse(bookContent);

    const section = book.sections.find(s => s.id === params.sectionId);
    if (!section) {
      throw error(404, 'Section not found');
    }

    const contentPath = join(process.cwd(), 'src', 'lib', 'data', 'book', section.file);
    const content = await readFile(contentPath, 'utf-8');

    return {
      book,
      section,
      content
    };
  } catch (e) {
    console.error('Error loading section:', e);
    throw error(500, 'Failed to load section');
  }
}
