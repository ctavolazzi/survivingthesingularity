import { sections } from '$lib/bookContent.js';
import { renderMarkdown } from '$lib/utils/bookMarkdown.js';

// The homepage is fully static content - prerender it so the launch spike is
// absorbed by the CDN edge instead of invoking a serverless function per view.
export const prerender = true;

// THE EXCERPT ON THE HOMEPAGE IS CUT FROM THE BOOK AT BUILD TIME.
//
// A sales page that retypes a passage will drift from the manuscript the first
// time the author revises it. So the passage is not typed here: it is the text
// of Chapter 0 between two anchors, the toast scene. If a revision moves or
// rewrites either anchor, the build fails and names the anchor, and someone
// picks a new passage on purpose.
const EXCERPT = Object.freeze({
  section: 'chapter0',
  from: '“Got into it. Brother. We live in it.”',
  to: 'Three glasses up, catching the neon.'
});

export async function load() {
  const raw = await sections[EXCERPT.section]();
  const start = raw.indexOf(EXCERPT.from);
  const end = raw.indexOf(EXCERPT.to, start);
  if (start < 0) throw new Error(`Homepage excerpt: start anchor not found in ${EXCERPT.section}: ${EXCERPT.from}`);
  if (end < 0) throw new Error(`Homepage excerpt: end anchor not found in ${EXCERPT.section}: ${EXCERPT.to}`);
  return { excerptHtml: renderMarkdown(raw.slice(start, end + EXCERPT.to.length)) };
}
