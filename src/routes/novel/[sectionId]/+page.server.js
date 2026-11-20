import { error } from '@sveltejs/kit';
import { findSection, loadSectionMarkdown, renderNovelMarkdown, novel } from '$lib/novel/novelContent.js';

export async function load({ params }) {
  const found = findSection(params.sectionId);
  if (!found) throw error(404, 'Not found');
  const html = renderNovelMarkdown(await loadSectionMarkdown(found.section));
  return {
    section: found.section,
    prev: found.prev,
    next: found.next,
    position: found.index + 1,
    total: novel.sections.length,
    html
  };
}
