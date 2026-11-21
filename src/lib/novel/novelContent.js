// The private reader for the novel (/novel). This is the revised v2
// manuscript, one Markdown file per section in $lib/data/novel, in the order
// novel.json gives. It is separate from the nonfiction draft in
// $lib/data/book and from the novel's working copy in manuscript/novel.
//
// The Markdown was converted from the Google Doc "Surviving the Singularity,
// Revised Manuscript v2" with its text unchanged. Italic and bold are written
// as <em> and <strong> so that no run of text can be misread as Markdown
// emphasis; scene breaks are `* * *`; each figure is an image followed by its
// italic caption paragraph.
import { Marked } from 'marked';
import { sanitizeHtml } from '$lib/utils/sanitizeHtml.js';
import novelJson from '$lib/data/novel/novel.json';

export const novel = novelJson;

const files = import.meta.glob('$lib/data/novel/*.md', { query: '?raw', import: 'default' });

/** @param {string} id */
export function findSection(id) {
  const index = novel.sections.findIndex((s) => s.id === id);
  if (index < 0) return null;
  return {
    index,
    section: novel.sections[index],
    prev: novel.sections[index - 1] ?? null,
    next: novel.sections[index + 1] ?? null
  };
}

/** @param {{file: string}} section */
export async function loadSectionMarkdown(section) {
  const load = files[`/src/lib/data/novel/${section.file}`];
  if (!load) throw new Error(`Missing novel file ${section.file}`);
  return load();
}

// Its own Marked instance: the book reader adds a KaTeX extension to the
// shared one, and this prose is full of dollar amounts.
const marked = new Marked({ gfm: true, breaks: false });

/** @param {string} source */
export function renderNovelMarkdown(source) {
  // The section title is drawn by the page itself.
  const body = source.replace(/^# .*\n+/, '');
  let html = sanitizeHtml(marked.parse(body));
  html = html.replace(/<img\b([^>]*?)\s*\/?>/g, '<img$1 width="960" height="768" loading="lazy" decoding="async">');
  return html.replace(
    /<p>\s*(<img\b[^>]*>)\s*<\/p>\s*<p>(<em>(?:(?!<\/p>)[\s\S])*?<\/em>)<\/p>/g,
    (_, image, caption) => `<figure class="novel-figure">${image}<figcaption>${caption}</figcaption></figure>`
  );
}

export function groupedSections() {
  const groups = [];
  for (const section of novel.sections) {
    const last = groups[groups.length - 1];
    if (last && last.label === section.group) last.items.push(section);
    else groups.push({ label: section.group, items: [section] });
  }
  return groups;
}
