import bookJson from '$lib/data/novel/book.json';
import { expandRefs as expandRefsRule } from '$lib/bookManifest.js';
import { describeSection } from '$lib/bookContentShared.js';

// THE BOOK IS THE NOVEL (2026-11-17).
//
// "Surviving the Singularity" became a novel. Its canonical source is
// src/lib/data/novel/: book.json sets the order of the Markdown beside it.
// Those files were built from the author's PDF ("final rough draft", 258
// pages); book.json records that provenance.
//
// The earlier nonfiction draft (v0.11.0) is NOT deleted. It stays, untouched,
// in src/lib/data/book/ with its whole publication pipeline, and is served to
// earlier buyers at /archive through $lib/archiveContent.js. Keep the two
// sources in separate modules: this one is imported by /book, /read and
// /sample, and must not drag the 109,000-word archive into their bundles.
export const book = bookJson;

// Internal cross-references ([](sts:chapter1)) are a feature of the archived
// draft. The novel has none, but the expansion stays so a pointer added later
// resolves against the novel's own manifest instead of rendering raw.
export const expandRefs = raw => expandRefsRule(book, raw);

// Lazy loader: one function per section that fetches its markdown on demand.
const lazyMarkdown = import.meta.glob('$lib/data/novel/*.md', { query: '?raw', import: 'default' });

export const sections = Object.fromEntries(
  book.sections.map(section => [
    section.id,
    async () => expandRefs(await lazyMarkdown[`/src/lib/data/novel/${section.file}`]())
  ])
);

// Eager loader: all markdown at build time so the /book landing page can show
// word counts without a wait per card, and /read can render one long scroll.
const eagerMarkdown = import.meta.glob('$lib/data/novel/*.md', { query: '?raw', import: 'default', eager: true });

const rawFor = section => expandRefs(eagerMarkdown[`/src/lib/data/novel/${section.file}`] || '');

// The novel is a finished draft: no section is flagged "under construction".
export const sectionsWithMeta = book.sections.map(section => describeSection(section, rawFor(section)));

// Just the numbered chapters (no front matter, act pages, interludes or afterword).
export const chaptersWithMeta = sectionsWithMeta.filter(s => /^chapter\d+$/.test(s.id));

// Same shape plus the raw markdown body, for the continuous reader (/read).
export const sectionsWithBody = sectionsWithMeta.map(section => ({
  ...section,
  raw: rawFor(section)
}));
