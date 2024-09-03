import { readFile } from 'fs/promises';
import { join } from 'path';
import { error } from '@sveltejs/kit';

export async function load() {
  try {
    const bookPath = join(process.cwd(), 'src', 'lib', 'data', 'book', 'book.json');
    const bookContent = await readFile(bookPath, 'utf-8');
    const book = JSON.parse(bookContent);

    if (!book || !book.sections || book.sections.length === 0) {
      throw error(500, 'Book data is not available or malformed');
    }

    return { book };
  } catch (e) {
    console.error('Error loading book data:', e);
    throw error(500, 'Failed to load book data');
  }
}
