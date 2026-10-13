import { book, sections } from '$lib/bookContent.js';
import { renderMarkdown } from '$lib/utils/bookMarkdown.js';

// The public sample always comes from the same canonical source as the reader.
export const prerender = true;
export async function load() {
  const ids = ['introduction', 'how-to-use'];
  return {
    version: book.version,
    excerpts: await Promise.all(ids.map(async (id) => ({
      id,
      title: book.sections.find((section) => section.id === id).title,
      html: renderMarkdown(await sections[id]()).replace(/<(\/?)h([1-5])\b/g, (_, close, level) => `<${close}h${Number(level) + 1}`)
    })))
  };
}
