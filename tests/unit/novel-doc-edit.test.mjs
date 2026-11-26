import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createBridge } from '../../src/lib/novel/bridge.js';
import { planEdit, pendingSuggestions, verifyEdit, findMatches, docParagraphs } from '../../src/lib/novel/docEdit.js';
import { bridgePage, bridgeMarkdown, bridgeHtml } from '../../src/lib/novel/bridgePage.js';

// A small Doc in the shape the Docs connector's read_doc returns.
const run = (content, style = {}, extra = {}) => ({ textRun: { content, textStyle: style, ...extra } });
const para = (runs, namedStyleType = 'NORMAL_TEXT') => ({ paragraph: { elements: runs, paragraphStyle: { namedStyleType } } });
function doc(paragraphs) {
  let index = 1;
  const content = paragraphs.map((p) => {
    const length = p.paragraph.elements.reduce((n, el) => n + el.textRun.content.length, 0);
    const out = { startIndex: index, endIndex: index + length, ...p };
    index += length;
    return out;
  });
  return { content: { documentId: 'doc-1', title: 'A manuscript', revisionId: 'rev-1', tabs: [{ documentTab: { body: { content } } }] } };
}
const book = () =>
  doc([
    para([run('Chapter 1: The Bar\n')], 'HEADING_1'),
    para([run('He ordered a beer. The beer was cold.\n')]),
    para([run('She said it was '), run('fine', { italic: true }), run(', and left.\n')]),
    para([run('Chapter 2: The Farm\n')], 'HEADING_1'),
    para([run('He ordered a beer again.\n')]),
    para([run('The old line. '), run('A new line.', {}, { suggestedInsertionIds: ['s1'] }), run('A cut line.', {}, { suggestedDeletionIds: ['s1'] }), run('\n')])
  ]);

test('a passage that appears once is planned as a suggestion', () => {
  const plan = planEdit(book(), { find: 'The beer was cold.', replace: 'The beer was warm.' });
  assert.equal(plan.ok, true);
  assert.equal(plan.where.section, 'Chapter 1: The Bar');
  assert.deepEqual(plan.request, {
    documentId: 'doc-1',
    writeControl: { writeMode: 'SUGGEST' },
    requests: [{ replaceAllText: { containsText: { text: 'The beer was cold.', matchCase: true }, replaceText: 'The beer was warm.' } }]
  });
  assert.equal(plan.document.readAtRevision, 'rev-1');
});

test('a direct edit is made only when asked for', () => {
  const plan = planEdit(book(), { find: 'The beer was cold.', replace: 'The beer was warm.', direct: true });
  assert.equal(plan.request.writeControl.writeMode, 'EDIT');
});

// Each refusal is shown firing. A refused plan carries no request to send.
const refusals = [
  ['words that appear twice', { find: 'He ordered a beer', replace: 'He ordered a water' }, /appear 2 times \(Chapter 1: The Bar; Chapter 2: The Farm\)/],
  ['words that are not in the Doc', { find: 'He ordered a whiskey', replace: 'x' }, /not in the Doc/],
  ['an em dash in the new words', { find: 'The beer was cold.', replace: 'The beer \u2014 cold.' }, /dash/],
  ['an en dash in the new words', { find: 'The beer was cold.', replace: 'Pages 1\u20132.' }, /dash/],
  ['new words the same as the old', { find: 'The beer was cold.', replace: 'The beer was cold.' }, /same as the old/],
  ['a match across two paragraphs', { find: 'cold.\nShe said', replace: 'x' }, /two paragraphs/],
  ['nothing to find', { find: '', replace: 'x' }, /Nothing to find/]
];
for (const [name, change, expected] of refusals) {
  test(`planEdit refuses ${name}`, () => {
    const plan = planEdit(book(), change);
    assert.equal(plan.ok, false);
    assert.equal(plan.request, null);
    assert.match(plan.problems.join('\n'), expected);
  });
}

test('planEdit warns when the match would lose italics, or sits on a waiting suggestion', () => {
  const styled = planEdit(book(), { find: 'it was fine, and left', replace: 'it was all right, and left' });
  assert.equal(styled.ok, true);
  assert.match(styled.warnings.join('\n'), /italic/);
  const plain = planEdit(book(), { find: ', and left.', replace: ', and stayed.' });
  assert.deepEqual(plain.warnings, []);
  const stacked = planEdit(book(), { find: 'The old line.', replace: 'The older line.' });
  assert.match(stacked.warnings.join('\n'), /already has a suggestion/);
});

test('pendingSuggestions lists what is waiting, with its chapter', () => {
  assert.deepEqual(pendingSuggestions(book()), [
    { section: 'Chapter 2: The Farm', text: 'The old line. [+A new line.][-A cut line.]' }
  ]);
  // Control: a Doc with no suggestions lists none.
  assert.deepEqual(pendingSuggestions(doc([para([run('Plain.\n')])])), []);
});

test('verifyEdit tells a suggestion from accepted text, and from nothing', () => {
  assert.deepEqual(verifyEdit(book(), { replace: 'A new line.' }), { found: true, as: 'suggestion' });
  assert.deepEqual(verifyEdit(book(), { replace: 'The beer was cold.' }), { found: true, as: 'text' });
  assert.deepEqual(verifyEdit(book(), { replace: 'A line nobody wrote.' }), { found: false, as: null });
});

test('findMatches and docParagraphs read the Doc in order', () => {
  assert.equal(findMatches(book(), 'beer').length, 3);
  assert.deepEqual(docParagraphs(book()).map((p) => p.section), [
    'Chapter 1: The Bar', 'Chapter 1: The Bar', 'Chapter 1: The Bar', 'Chapter 2: The Farm', 'Chapter 2: The Farm', 'Chapter 2: The Farm'
  ]);
});

// ---- the bridge as a page

const root = new URL('../../src/lib/data/novel/', import.meta.url);
const load = (name) => JSON.parse(readFileSync(new URL(name, root), 'utf8'));
const page = () => {
  const protocol = load('bridge-protocol.json');
  const bridge = createBridge({ novel: load('novel.json'), compendium: load('compendium.json'), instances: load('instances.json') });
  return bridgePage(bridge, protocol, { code: protocol.code });
};

test('BRIDGE.md in the repository is what the data says today', () => {
  const onDisk = readFileSync(new URL('../../manuscript/novel/BRIDGE.md', import.meta.url), 'utf8');
  assert.equal(onDisk, bridgeMarkdown(page()) + '\n', 'run: node scripts/sts-bridge.mjs export md > manuscript/novel/BRIDGE.md');
});

test('the page names exactly one current copy and every editing step', () => {
  const p = page();
  assert.equal(p.copies.filter((c) => c.state === 'CURRENT').length, 1);
  assert.equal(p.current.title, 'StS v8 draft (Nov 26)');
  assert.ok(p.editing.length >= 6);
  const md = bridgeMarkdown(p);
  for (const step of p.editing) assert.ok(md.includes(step));
  assert.doesNotMatch(md, /[\u2013\u2014]/);
});

test('Doc ids appear in the Drive page only when they are passed in, and never in the repository page', () => {
  const p = page();
  const id = 'AbCdEfGhIjKlMnOpQrStUvWxYz0123456789_-abcdef';
  const html = bridgeHtml(p, { 'doc-revised-v3': id });
  assert.match(html, new RegExp(`docs\\.google\\.com/document/d/${id}/edit`));
  assert.doesNotMatch(bridgeHtml(p), /docs\.google\.com/);
  assert.doesNotMatch(bridgeMarkdown(p), /docs\.google\.com|[A-Za-z0-9_-]{40,}/);
  // Titles and roles are data, so they must be escaped.
  assert.doesNotMatch(bridgeHtml({ ...p, what: '<script>x</script>' }), /<script>/);
});
