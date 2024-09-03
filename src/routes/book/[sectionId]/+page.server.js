import { error } from '@sveltejs/kit';
import { book, sections } from '$lib/bookContent';

export async function load({ params }) {
  try {
    const section = book.sections.find(s => s.id === params.sectionId);
    if (!section) {
      throw error(404, 'Section not found');
    }

    const contentLoader = sections[section.id];
    if (!contentLoader) {
      throw error(404, 'Content not found');
    }

    const content = await contentLoader();

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
