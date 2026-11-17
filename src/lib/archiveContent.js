import archiveJson from '$lib/data/book/book.json';
import { expandRefs as expandRefsRule } from '$lib/bookManifest.js';
import { describeSection } from '$lib/bookContentShared.js';

// THE ARCHIVED NONFICTION DRAFT (v0.11.0).
//
// Before the book became a novel, preorder buyers were delivered this draft,
// and the offer told them: "you keep everything already delivered and the
// archive stays readable." /archive is that promise. The source directory
// (src/lib/data/book/) and its publication pipeline are unchanged; the
// downloads in static/downloads/ still match its book.json, which
// scripts/check-book-downloads.mjs keeps asserting.
//
// Only /archive imports this module. Do not import it from the novel's
// readers: it bundles the whole draft eagerly.
export const archiveBook = archiveJson;

const expandRefs = raw => expandRefsRule(archiveBook, raw);

const eagerMarkdown = import.meta.glob('$lib/data/book/*.md', { query: '?raw', import: 'default', eager: true });

export const archiveSections = archiveBook.sections.map(section => {
  const raw = expandRefs(eagerMarkdown[`/src/lib/data/book/${section.file}`] || '');
  return { ...describeSection(section, raw), raw };
});

// The bonus file earlier buyers were delivered with that draft. Frozen build
// output (see src/lib/data/archive/README.md). YAML front matter is dropped:
// it was written for the PDF build, not for a page.
const extras = import.meta.glob('$lib/data/archive/*.md', { query: '?raw', import: 'default', eager: true });
const body = raw => (raw || '').replace(/^---[\s\S]*?---\s*/, '');
export const archiveExtras = [
  { id: 'precedent-file', title: 'The Precedent File', file: 'The-Precedent-File.md' },
  { id: 'precedent-sources', title: 'The Precedent File: sources and citations', file: 'Sources-and-Citations.md' }
].map(extra => {
  const raw = body(extras[`/src/lib/data/archive/${extra.file}`]);
  return { ...describeSection(extra, raw), raw };
});
