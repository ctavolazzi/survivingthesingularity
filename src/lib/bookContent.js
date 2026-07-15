import bookJson from '$lib/data/book/book.json';

export const book = bookJson;

// Lazy loader - returns a function per chapter that fetches markdown on demand.
// Preserves the original surface used by /book/[sectionId] routes.
export const sections = Object.fromEntries(
  book.sections.map(section => [
    section.id,
    import.meta.glob('$lib/data/book/*.md', { query: '?raw', import: 'default' })[`/src/lib/data/book/${section.file}`]
  ])
);

// Eager loader - all markdown loaded synchronously at build time so the
// /book landing page can render rich chapter cards (teaser + read time) without
// an async wait per card. Bundles ~all chapter prose into the page; tradeoff
// is page weight, but markdown compresses well and there's no waterfall.
const eagerMarkdown = import.meta.glob('$lib/data/book/*.md', { query: '?raw', import: 'default', eager: true });

function extractTeaser(raw) {
  if (!raw) return '';
  // Strip YAML frontmatter if present
  let body = raw.startsWith('---') ? raw.replace(/^---[\s\S]*?---\s*/, '') : raw;
  // Remove leading H1/H2 headings (chapter titles)
  body = body.replace(/^#{1,2}\s+.+\n+/m, '');
  // Find first prose paragraph that isn't a heading, list, blockquote, or fence
  const paragraphs = body.split(/\n\s*\n/);
  for (const p of paragraphs) {
    const trimmed = p.trim();
    if (!trimmed) continue;
    if (/^#{1,6}\s/.test(trimmed)) continue;       // headings
    if (/^[-*+]\s/.test(trimmed)) continue;        // unordered list
    if (/^\d+\.\s/.test(trimmed)) continue;        // ordered list
    if (/^>/.test(trimmed)) continue;              // blockquote
    if (/^```/.test(trimmed)) continue;            // code fence
    if (/^!\[/.test(trimmed)) continue;            // standalone image
    // Strip inline markdown for clean teaser text
    const clean = trimmed
      .replace(/\*\*([^*]+)\*\*/g, '$1')
      .replace(/\*([^*]+)\*/g, '$1')
      .replace(/_([^_]+)_/g, '$1')
      .replace(/`([^`]+)`/g, '$1')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/\s+/g, ' ')
      .trim();
    return clean.length > 220 ? clean.slice(0, 217).trimEnd() + '…' : clean;
  }
  return '';
}

function countWords(raw) {
  if (!raw) return 0;
  const text = raw
    .replace(/^---[\s\S]*?---\s*/, '')   // frontmatter
    .replace(/```[\s\S]*?```/g, '')      // code blocks
    .replace(/`[^`]+`/g, '')             // inline code
    .replace(/!\[[^\]]*\]\([^)]+\)/g, '') // images
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // links → label
    .replace(/[#>*_\-]/g, ' ');
  const matches = text.match(/\b[\w’'-]+\b/g);
  return matches ? matches.length : 0;
}

// Narrative chapters (chapterN + the conclusion) get an ongoing pass that
// weaves a recurring throughline into the material (see ELIJAH-PROTOCOL.md).
// Front/back matter (preface, introduction, appendices) were never in scope
// for that pass, so they're excluded from the "in progress" check below
// rather than being flagged as unfinished.
const NARRATIVE_SECTION = /^(chapter\d+|conclusion)$/;

// Chapter metadata enriched with teaser + word count + read time.
// Stable shape: { ...sectionFromJson, teaser, wordCount, readMinutes, inProgress }
export const sectionsWithMeta = book.sections.map(section => {
  const raw = eagerMarkdown[`/src/lib/data/book/${section.file}`] || '';
  const wordCount = countWords(raw);
  const inProgress = NARRATIVE_SECTION.test(section.id) && !raw.includes('Elijah');
  return {
    ...section,
    teaser: extractTeaser(raw),
    wordCount,
    readMinutes: Math.max(1, Math.ceil(wordCount / 250)),
    inProgress
  };
});

// Convenience: just the numbered chapters (excludes front/back matter),
// useful for chapter-card grids on the /book landing page.
export const chaptersWithMeta = sectionsWithMeta.filter(s => /^chapter\d+$/.test(s.id));
