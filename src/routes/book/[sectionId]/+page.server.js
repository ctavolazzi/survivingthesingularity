import { error, isHttpError } from '@sveltejs/kit';
import { book, sections } from '$lib/bookContent';

export async function load({ params }) {
  const section = book.sections.find(s => s.id === params.sectionId);
  if (!section) {
    throw error(404, 'Section not found');
  }

  const contentLoader = sections[section.id];
  if (!contentLoader) {
    throw error(404, 'Content not found');
  }

  try {
    const content = await contentLoader();
    return {
      book,
      section,
      content
    };
  } catch (e) {
    // A deliberate 404 above is thrown outside this try, so it never lands
    // here; guard against re-wrapping an HttpError anyway in case that
    // changes. Only genuine markdown-load failures should ever hit this.
    if (isHttpError(e)) throw e;
    console.error('Error loading section content:', e);
    throw error(500, 'Failed to load section');
  }
}
