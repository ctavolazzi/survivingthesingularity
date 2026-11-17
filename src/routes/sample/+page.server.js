import { book, sections } from '$lib/bookContent.js';
import { renderMarkdown } from '$lib/utils/bookMarkdown.js';

// The public sample always comes from the same canonical source as the reader.
export const prerender = true;
export async function load() {
  // The free sample is the Author's Note and the first chapter of the novel.
  const ids = ['authors-note', 'chapter0'];
  return {
    version: book.version,
    edition: book.edition,
    excerpts: await Promise.all(ids.map(async (id) => ({
      id,
      title: book.sections.find((section) => section.id === id).title,
      html: renderMarkdown(await sections[id]()).replace(/<(\/?)h([1-5])\b/g, (_, close, level) => `<${close}h${Number(level) + 1}`)
    })))
  };
}
