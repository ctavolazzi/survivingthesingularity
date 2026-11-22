#!/usr/bin/env node
// The bridge from the command line. Run from anywhere in the repository.
//
//   node scripts/sts-bridge.mjs status                 every copy of the book and which one is the book right now
//   node scripts/sts-bridge.mjs check                  everything wrong with the map (exit 1 if anything)
//   node scripts/sts-bridge.mjs where <name>           what a name is, what it links to, where it appears
//   node scripts/sts-bridge.mjs edit READ.json --find "old words" --replace "new words" [--direct]
//                                                      check one change and print the request to send
//   node scripts/sts-bridge.mjs suggestions READ.json  the suggestions waiting in the Doc, by chapter
//   node scripts/sts-bridge.mjs verify READ.json --replace "new words"
//                                                      after sending: is the change in the Doc
//   node scripts/sts-bridge.mjs quotes TEXT.txt        is every quotation in the compendium in this text
//   node scripts/sts-bridge.mjs export md|html [--ids FILE]
//                                                      the bridge as a page, for the repository or for Drive
//
// <name> is an entry (elijah-madrone), a chapter (chapter-9) or a copy (site-reader).
// READ.json is a saved result of the Docs connector's read_doc on the manuscript.
// This script reads files. It never calls Google and never writes to a Doc.
import { readFileSync } from 'node:fs';
import { createBridge } from '../src/lib/novel/bridge.js';
import { planEdit, pendingSuggestions, verifyEdit, docIdentity } from '../src/lib/novel/docEdit.js';
import { bridgePage, bridgeMarkdown, bridgeHtml } from '../src/lib/novel/bridgePage.js';

const root = new URL('../src/lib/data/novel/', import.meta.url);
const load = (name) => JSON.parse(readFileSync(new URL(name, root), 'utf8'));
const novel = load('novel.json');
const compendium = load('compendium.json');
const protocol = load('bridge-protocol.json');
const bridge = createBridge({ novel, compendium, instances: load('instances.json') });
const texts = () => Object.fromEntries(novel.sections.map((s) => [s.id, readFileSync(new URL(s.file, root), 'utf8')]));

const [command, ...rest] = process.argv.slice(2);
const flag = (name) => {
  const at = rest.indexOf(`--${name}`);
  return at >= 0 ? rest[at + 1] : undefined;
};
const has = (name) => rest.includes(`--${name}`);
const first = rest.find((a, i) => !a.startsWith('--') && !(rest[i - 1] ?? '').match(/^--(find|replace|ids)$/));
const readJson = (file) => JSON.parse(readFileSync(file, 'utf8'));

function status() {
  const now = bridge.current();
  console.log(`As recorded on ${bridge.asOf}. The book right now: ${now?.title ?? 'not set'} (${now?.holds ?? '?'})\n`);
  for (const copy of bridgePage(bridge, protocol).copies) {
    console.log(`  ${copy.holds.padEnd(11)} ${copy.state.padEnd(13)} ${copy.kind.padEnd(11)} ${copy.title}`);
  }
  return 0;
}

function check() {
  const problems = bridge.check();
  for (const p of problems) console.log(`${p.where}: ${p.what}`);
  console.log(problems.length ? `\n${problems.length} problems.` : `The map holds together: ${bridge.topics.length} topics, ${bridge.entries.length} entries, ${bridge.instances.length} copies of the book.`);
  return problems.length ? 1 : 0;
}

function where(ref) {
  // A bare name is tried as an entry first, then as each other kind.
  const found = ['', 'topic:', 'section:', 'instance:'].map((kind) => bridge.resolve(kind + (ref ?? ''))).find(Boolean);
  if (!found) {
    console.log(`Nothing is called "${ref}".`);
    return 1;
  }
  console.log(`${found.kind}: ${found.title}`);
  if (found.kind === 'entry') {
    console.log(`  topic:        ${found.item.topic}`);
    console.log(`  links to:     ${bridge.linksFrom(found.id).join(', ') || 'nothing'}`);
    console.log(`  linked from:  ${bridge.backlinks(found.id).map((e) => e.id).join(', ') || 'nothing'}`);
    const seen = bridge.appearances(found.id, texts());
    console.log(`  in the book:  ${seen.reduce((n, a) => n + a.paragraphs, 0)} paragraphs in ${seen.length} sections of the site's copy`);
    for (const a of seen) console.log(`      ${String(a.paragraphs).padStart(4)}  ${a.title}`);
  } else if (found.kind === 'instance') {
    for (const key of ['holds', 'from', 'path', 'role', 'tool', 'checked']) {
      if (found.item[key]) console.log(`  ${(key + ':').padEnd(9)} ${found.item[key]}`);
    }
  } else if (found.kind === 'topic') {
    for (const entry of bridge.tree().find((t) => t.id === found.id).entries) console.log(`  ${entry.id}`);
  } else {
    console.log(`  file: src/lib/data/novel/${found.item.file}   words: ${found.item.words}`);
  }
  return 0;
}

// Is this read the copy the map calls current? Titles are all the repository knows.
function sameAsCurrent(read) {
  const now = bridge.current();
  const { title } = docIdentity(read);
  return { now, title, same: Boolean(now && title && now.title === title) };
}

function edit() {
  if (!first || flag('find') === undefined || flag('replace') === undefined) {
    console.log('Usage: edit READ.json --find "old words" --replace "new words" [--direct]');
    return 1;
  }
  const read = readJson(first);
  const plan = planEdit(read, { find: flag('find'), replace: flag('replace'), direct: has('direct') });
  const { now, title, same } = sameAsCurrent(read);
  console.error(`Doc:      ${title}`);
  if (!same) console.error(`WARNING:  the map says the book right now is "${now?.title ?? 'not set'}". This read is of a different Doc.`);
  if (plan.where) console.error(`Where:    ${plan.where.section || 'before the first heading'}`);
  for (const p of plan.problems) console.error(`PROBLEM:  ${p}`);
  for (const w of plan.warnings) console.error(`WARNING:  ${w}`);
  if (!plan.ok) {
    console.error('\nNot sent. Nothing was changed.');
    return 1;
  }
  console.error(`Mode:     ${plan.request.writeControl.writeMode === 'SUGGEST' ? 'a suggestion the author can accept or reject' : 'A DIRECT EDIT. Only with the author\'s say-so.'}`);
  console.error('\nSend this with the Docs connector\'s update_doc, then read the Doc again and run `verify`:\n');
  console.log(JSON.stringify(plan.request, null, 2));
  return 0;
}

function suggestions() {
  if (!first) {
    console.log('Usage: suggestions READ.json');
    return 1;
  }
  const read = readJson(first);
  const waiting = pendingSuggestions(read);
  console.log(`${docIdentity(read).title}: ${waiting.length} paragraphs with a suggestion waiting. [+new words] [-removed words]\n`);
  let section = null;
  for (const s of waiting) {
    if (s.section !== section) console.log(`${s.section || 'Before the first heading'}`);
    section = s.section;
    console.log(`  ${s.text.length > 400 ? s.text.slice(0, 400) + '...' : s.text}`);
  }
  return 0;
}

function verify() {
  if (!first || flag('replace') === undefined) {
    console.log('Usage: verify READ.json --replace "new words"');
    return 1;
  }
  const result = verifyEdit(readJson(first), { replace: flag('replace') });
  if (!result.found) console.log('NOT FOUND. The new words are not in this read of the Doc.');
  else console.log(result.as === 'suggestion' ? 'Found, as a suggestion waiting on the author.' : 'Found, as text in the Doc (not a suggestion).');
  return result.found ? 0 : 1;
}

function quotes(file) {
  if (!file) {
    console.log('Give the manuscript as a plain text file.');
    return 1;
  }
  const tidy = (s) => s.replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ');
  const book = tidy(readFileSync(file, 'utf8'));
  let checked = 0;
  let missing = 0;
  for (const entry of compendium.entries) {
    const strings = [entry.summary, ...(entry.body ?? []), ...(entry.facts ?? []).map((f) => f.value), ...(entry.quotes ?? []).map((q) => q.from)];
    const quoted = (entry.quotes ?? []).map((q) => q.text);
    for (const s of strings) for (const m of s.matchAll(/"([^"]+)"/g)) quoted.push(m[1]);
    for (const q of quoted) {
      checked += 1;
      // A quotation may close on its own full stop or comma where the book's sentence runs on.
      if (!book.includes(tidy(q).replace(/[.,]$/, ''))) {
        missing += 1;
        console.log(`NOT IN THE TEXT  ${entry.id}: ${q}`);
      }
    }
  }
  console.log(`${checked} quotations checked, ${missing} not found.`);
  return missing ? 1 : 0;
}

function exportPage(format) {
  const page = bridgePage(bridge, protocol, { code: protocol.code ?? null });
  if (format === 'md') console.log(bridgeMarkdown(page));
  else if (format === 'html') console.log(bridgeHtml(page, flag('ids') ? readJson(flag('ids')) : {}));
  else {
    console.log('Usage: export md | export html [--ids FILE]');
    return 1;
  }
  return 0;
}

switch (command) {
  case 'status':
    process.exit(status());
  case 'check':
    process.exit(check());
  case 'where':
    process.exit(where(first));
  case 'edit':
    process.exit(edit());
  case 'suggestions':
    process.exit(suggestions());
  case 'verify':
    process.exit(verify());
  case 'quotes':
    process.exit(quotes(first));
  case 'export':
    process.exit(exportPage(first));
  default:
    console.log(readFileSync(new URL(import.meta.url), 'utf8').split('\n').slice(1, 19).map((l) => l.replace(/^\/\/ ?/, '')).join('\n'));
    process.exit(command ? 1 : 0);
}
