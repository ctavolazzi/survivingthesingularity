import { sceneCatalog } from './catalog.js';

// The ordinary image/caption is the publication source and the no-script
// fallback. Unknown or malformed markers never remove manuscript content.
const PAIRED_FIGURE = /^<!--\s*interactive:([a-z0-9-]+)\s*-->[ \t]*\r?\n\s*\n?!\[([^\]\n]*)\]\((\/book-images\/[^)\s]+)\)[ \t]*\r?\n\s*\n?\*([^\n]+)\*[ \t]*(?=\r?\n|$)/gm;

export function splitBookFigures(raw = '') {
  const segments = [];
  let position = 0;
  for (const match of raw.matchAll(PAIRED_FIGURE)) {
    const [block, id, alt, src, caption] = match;
    if (!sceneCatalog[id] || src !== `/book-images/${sceneCatalog[id].file}`) continue;
    if (match.index > position) segments.push({ type: 'markdown', raw: raw.slice(position, match.index) });
    segments.push({ type: 'scene', id, alt, src, caption });
    position = match.index + block.length;
  }
  if (position < raw.length) segments.push({ type: 'markdown', raw: raw.slice(position) });
  return segments;
}
