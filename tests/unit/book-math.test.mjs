import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { Marked } from 'marked';
import { sanitizeHtml } from '../../src/lib/utils/sanitizeHtml.js';
import { katexExtension } from '../../src/lib/utils/katexExtension.js';

const markdown = new Marked(katexExtension);
const render = text => sanitizeHtml(markdown.parse(text));
test('math renders without consuming prices in neighboring prose', () => {
  const html = render('Compare $25,000 with $150. For $Q = 4$, keep both prices.');
  assert.match(html, /\$25,000/);
  assert.match(html, /\$150/);
  assert.match(html, /class="katex"/);
  assert.doesNotMatch(html, /math-fallback|katex-error/);
});
test('current manuscript equations still render with the updated math dependency', () => {
  const root = new URL('../../src/lib/data/book/', import.meta.url);
  const book = JSON.parse(readFileSync(new URL('book.json', root), 'utf8'));
  let equations = 0;
  for (const section of book.sections) {
    const html = render(readFileSync(new URL(section.file, root), 'utf8'));
    assert.doesNotMatch(html, /class="(?:math-fallback|katex-error)/, section.file);
    equations += [...html.matchAll(/class="katex"/g)].length;
  }
  assert.ok(equations >= 6, 'The manuscript equations must remain rendered');
});
