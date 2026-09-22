import { marked } from 'marked';
import { book, expandRefs } from '$lib/bookContent.js';

// The Precedent Ledger: every "## Precedent P-NN: Title (Place, Years)" section
// in the book, pulled from the book source at build time. There is no copy of
// the precedents anywhere else, so a fix in src/lib/data/book/ reaches this page
// on the next build, the same as it reaches /book, the EPUB and the PDFs.
const raw = import.meta.glob('$lib/data/book/*.md', { query: '?raw', import: 'default', eager: true });

const HEADING = /^## Precedent (P-(\d+)): (.+?)(?: \(([^)]+)\))?\s*$/;

function extractPrecedents(markdown, section) {
  const lines = markdown.split('\n');
  const found = [];
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(HEADING);
    if (!m) continue;
    const body = [];
    for (let j = i + 1; j < lines.length; j++) {
      // A precedent runs until the next heading of level 1 or 2, or a rule.
      if (/^#{1,2} /.test(lines[j]) || /^---\s*$/.test(lines[j])) break;
      body.push(lines[j]);
    }
    const text = expandRefs(body.join('\n').trim());
    found.push({
      id: m[1],
      n: Number(m[2]),
      title: m[3],
      where: m[4] ?? '',
      chapter: section.title,
      sectionId: section.id,
      html: marked.parse(text),
      words: text.split(/\s+/).filter(Boolean).length,
    });
  }
  return found;
}

export function load() {
  const precedents = book.sections
    .flatMap((section) => {
      const md = raw[`/src/lib/data/book/${section.file}`];
      return md ? extractPrecedents(md, section) : [];
    })
    .sort((a, b) => a.n - b.n);

  return { precedents, version: book.version };
}
