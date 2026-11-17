// Helpers shared by the two book sources: the novel ($lib/bookContent.js) and
// the archived nonfiction draft ($lib/archiveContent.js). Pure functions, no
// Vite globs, so either source can build the same section shapes.

export function extractTeaser(raw) {
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

export function countWords(raw) {
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

// Stable shape: { ...sectionFromJson, teaser, wordCount, readMinutes, inProgress }
export function describeSection(section, raw, inProgress = false) {
  const wordCount = countWords(raw);
  return {
    ...section,
    teaser: extractTeaser(raw),
    wordCount,
    readMinutes: Math.max(1, Math.ceil(wordCount / 250)),
    inProgress
  };
}
