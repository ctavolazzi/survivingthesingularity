import bookJson from '$lib/data/book/book.json';

export const book = bookJson;

export const sections = Object.fromEntries(
  book.sections.map(section => [
    section.id,
    import.meta.glob('$lib/data/book/*.md', { as: 'raw' })[`/src/lib/data/book/${section.file}`]
  ])
);