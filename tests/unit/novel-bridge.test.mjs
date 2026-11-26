import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createBridge, parseRef, plainParagraphs } from '../../src/lib/novel/bridge.js';

const root = new URL('../../src/lib/data/novel/', import.meta.url);
const load = (name) => JSON.parse(readFileSync(new URL(name, root), 'utf8'));
const data = () => ({
  novel: load('novel.json'),
  compendium: load('compendium.json'),
  instances: load('instances.json')
});
const clone = (value) => JSON.parse(JSON.stringify(value));
const texts = (novel) =>
  Object.fromEntries(novel.sections.map((s) => [s.id, readFileSync(new URL(s.file, root), 'utf8')]));

test('the map on disk holds together', () => {
  assert.deepEqual(createBridge(data()).check(), []);
});

test('every topic has an entry and every entry links to another', () => {
  const bridge = createBridge(data());
  for (const topic of bridge.tree()) assert.ok(topic.entries.length >= 1, topic.id);
  for (const entry of bridge.entries) {
    const others = bridge.linksFrom(entry.id).filter((ref) => ref.startsWith('entry:'));
    assert.ok(others.length >= 1, `${entry.id} links to no other entry`);
    assert.ok(bridge.backlinks(entry.id).length >= 1, `nothing links to ${entry.id}`);
  }
});

// Each check is shown going red on a map with that one fault put in.
const faults = [
  ['a link to an entry that does not exist', (d) => d.compendium.entries[0].body.push('See [[nobody-here]].'), /nobody-here/],
  ['a link to a section that does not exist', (d) => d.compendium.entries[0].body.push('[[section:chapter-99|Chapter 99]]'), /chapter-99/],
  ['an entry in a topic that does not exist', (d) => (d.compendium.entries[1].topic = 'weather'), /weather/],
  ['a topic with no entries', (d) => d.compendium.topics.push({ id: 'songs', name: 'Songs' }), /has no entries/],
  ['an id used twice', (d) => d.compendium.entries.push(clone(d.compendium.entries[2])), /used twice/],
  ['a find pattern that is not valid', (d) => (d.compendium.entries[2].find = '(Fisher'), /find pattern/],
  ['an em dash in an entry', (d) => (d.compendium.entries[3].summary += ' \u2014 and so on'), /dash/],
  ['an entry that links to itself', (d) => d.compendium.entries[4].body.push('[[the-co-op]]'), /links to itself/],
  ['an entry with no text', (d) => (d.compendium.entries[5].body = []), /has no text/],
  ['two copies marked current', (d) => (d.instances.instances[0].current = true), /2 copies are marked current/],
  ['no copy marked current', (d) => d.instances.instances.forEach((c) => delete c.current), /0 copies are marked current/],
  ['a copy made from one that is not in the map', (d) => (d.instances.instances[1].from = 'doc-lost'), /doc-lost/],
  ['a copy holding a version that is not listed', (d) => (d.instances.instances[5].holds = 'v9'), /v9/]
];
for (const [name, breakIt, expected] of faults) {
  test(`check() reports ${name}`, () => {
    const broken = data();
    breakIt(broken);
    const said = createBridge(broken).check().map((p) => `${p.where}: ${p.what}`).join('\n');
    assert.match(said, expected);
  });
}

test('resolve() names the thing a reference points at', () => {
  const bridge = createBridge(data());
  assert.equal(bridge.resolve('the-fisher').title, 'The Fisher');
  assert.equal(bridge.resolve('entry:the-fisher').kind, 'entry');
  assert.equal(bridge.resolve('topic:items').title, 'Items');
  assert.equal(bridge.resolve('section:chapter-0').title, 'Chapter 0: The Demonstration');
  assert.equal(bridge.resolve('instance:site-reader').item.holds, 'v2');
  assert.equal(bridge.resolve('entry:nobody-here'), null);
  assert.deepEqual(parseRef('chapter-0'), { kind: 'entry', id: 'chapter-0' });
});

test('href() opens entries, topics and sections under the private reader', () => {
  const bridge = createBridge(data());
  assert.equal(bridge.href('the-fisher', '/novel/k'), '/novel/k/compendium/the-fisher');
  assert.equal(bridge.href('topic:items', '/novel/k'), '/novel/k/compendium#topic-items');
  assert.equal(bridge.href('section:chapter-5', '/novel/k'), '/novel/k/chapter-5');
  assert.equal(bridge.href('instance:site-reader', '/novel/k'), null);
});

test('tokens() turns [[links]] into pieces and marks the missing ones', () => {
  const bridge = createBridge(data());
  const pieces = bridge.tokens('At [[the-bear-flag|the bar]], see [[the-fisher]] and [[nobody-here]].', '/novel/k');
  assert.deepEqual(pieces.map((p) => p.text), ['At ', 'the bar', ', see ', 'The Fisher', ' and ', 'nobody-here', '.']);
  assert.equal(pieces[1].href, '/novel/k/compendium/the-bear-flag');
  assert.equal(pieces[3].missing, false);
  assert.equal(pieces[5].missing, true);
  assert.equal(pieces[5].href, null);
});

test('backlinks() finds the entries that point at one', () => {
  const bridge = createBridge(data());
  const names = bridge.backlinks('the-fisher').map((e) => e.id).sort();
  assert.deepEqual(names, ['elijah-madrone', 'the-co-op']);
});

test('appearances() counts paragraphs in the reader’s own files, in reading order', () => {
  const d = data();
  const bridge = createBridge(d);
  const all = texts(d.novel);
  const fisher = bridge.appearances('the-fisher', all);
  assert.ok(fisher.length >= 5);
  assert.equal(fisher[0].id, 'chapter-5', 'the Fisher is first named in chapter 5');
  const order = d.novel.sections.map((s) => s.id);
  const places = fisher.map((a) => order.indexOf(a.id));
  assert.deepEqual(places, [...places].sort((a, b) => a - b));
  // Control: a pattern that is in no chapter finds nothing, and headings and captions are not counted.
  const none = clone(d);
  none.compendium.entries[2].find = 'Zzyzx Road';
  assert.deepEqual(createBridge(none).appearances('the-fisher', all), []);
  assert.deepEqual(plainParagraphs('# The Fisher\n\n![The Fisher](/x.webp)\n\n* * *\n\nA <em>stove</em>.'), ['A stove.']);
});

test('each "First seen" fact names the section where the entry is first named', () => {
  const d = data();
  const bridge = createBridge(d);
  const all = texts(d.novel);
  for (const entry of bridge.entries) {
    const fact = (entry.facts ?? []).find((f) => f.label === 'First seen');
    if (!fact) continue;
    const said = /\[\[section:([^\]|]+)/.exec(fact.value)?.[1];
    // The story, not the Author's Note or the appendix, which name people too.
    const inStory = bridge.appearances(entry.id, all).filter((a) => !/matter$/.test(a.group));
    assert.equal(said, inStory[0]?.id, entry.id);
  }
});

test('status() says which copy is the book and how far each other copy is behind', () => {
  const bridge = createBridge(data());
  assert.equal(bridge.current().id, 'doc-v6-draft');
  const byId = Object.fromEntries(bridge.status().map((s) => [s.id, s]));
  assert.equal(byId['doc-v6-draft'].behind, 0);
  assert.equal(byId['doc-v5-draft'].behind, 1);
  assert.equal(byId['doc-v4-final-draft'].behind, 2);
  assert.equal(byId['doc-revised-v3'].behind, 3);
  assert.equal(byId['site-reader'].behind, 4);
  assert.equal(byId['repo-manuscript'].behind, 7);
  // The scaffold describes version 4, two versions before the book.
  assert.equal(byId['doc-v4-scaffold'].behind, 2);
});

test('no Google Doc id is written into the map', () => {
  const raw = readFileSync(new URL('instances.json', root), 'utf8') + readFileSync(new URL('compendium.json', root), 'utf8');
  assert.doesNotMatch(raw, /[A-Za-z0-9_-]{40,}/, 'a Drive id is about 44 characters; this repository is public');
  assert.doesNotMatch(raw, /docs\.google\.com/);
});
