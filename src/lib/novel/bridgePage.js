// The bridge written out as a page a person or a chat can read: Markdown for
// the repository (manuscript/novel/BRIDGE.md) and HTML for Google Drive.
//
// Both come from the same data, so they cannot disagree. Google Doc ids are
// never in the repository, which is public. Pass them in as `ids`
// ({instanceId or note title: docId}) when making the Drive page, where the
// links are private to the author's account.

const escapeHtml = (text) =>
  String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function stateOf(copy) {
  if (copy.current) return 'CURRENT';
  if (copy.stale) return 'stale copy';
  if (copy.behind === null) return 'unknown';
  if (copy.behind === 0) return 'up to date';
  if (copy.behind < 0) return 'next version';
  return `behind by ${copy.behind}`;
}

/** The page as plain data: a title and a list of sections. */
export function bridgePage(bridge, protocol, { code = null } = {}) {
  const roles = new Map(bridge.instances.map((c) => [c.id, c]));
  const copies = bridge.status().map((s) => ({
    id: s.id,
    title: s.title,
    kind: s.kind,
    holds: s.holds,
    state: stateOf(s),
    role: roles.get(s.id)?.role ?? ''
  }));
  const now = bridge.current();
  return {
    title: 'sts-bridge: read this first',
    asOf: bridge.asOf,
    what: protocol.what,
    current: now ? { id: now.id, title: now.title, role: now.role ?? '' } : null,
    copies,
    notes: (bridge.notes ?? []).map((n) => ({ title: n.title, what: n.what })),
    editing: protocol.editing,
    rules: protocol.rules,
    withCode: protocol.withCode,
    withoutCode: protocol.withoutCode,
    requestExample: protocol.requestExample,
    code
  };
}

export function bridgeMarkdown(page) {
  const out = [`# ${page.title}`, '', page.what, ''];
  out.push(`Recorded on ${page.asOf}. This page is written by \`node scripts/sts-bridge.mjs export md\`. Do not edit it by hand:`);
  out.push('change `src/lib/data/novel/instances.json` or `bridge-protocol.json` and export again.', '');
  out.push('## The book right now', '');
  out.push(page.current ? `**${page.current.title}** (a Google Doc). ${page.current.role}` : 'No copy is marked current.', '');
  out.push('## Every copy of the book', '', '| Holds | State | What | Where |', '|---|---|---|---|');
  for (const c of page.copies) out.push(`| ${c.holds} | ${c.state} | ${c.role} | ${c.title} |`);
  out.push('', 'Google Docs are named by title only, because this repository is public. Search Drive for the title.', '');
  out.push('## Notes about the book', '');
  for (const n of page.notes) out.push(`- **${n.title}.** ${n.what}`);
  out.push('', '## How to change the manuscript', '');
  page.editing.forEach((step, i) => out.push(`${i + 1}. ${step}`));
  out.push('', '## House rules', '');
  for (const rule of page.rules) out.push(`- ${rule}`);
  out.push('', '## If your chat can run code', '', '```bash');
  for (const line of page.withCode) out.push(line);
  out.push('```', '');
  out.push('`READ.json` is the saved result of the Docs connector\'s `read_doc` on the current manuscript. The', 'script never calls Google and never writes to the Doc. It checks your change and prints the request', 'for the connector\'s `update_doc`.', '');
  out.push('## If your chat cannot run code', '');
  page.withoutCode.forEach((step, i) => out.push(`${i + 1}. ${step}`));
  out.push('', '```json', JSON.stringify(page.requestExample, null, 2), '```', '');
  return out.join('\n');
}

export function bridgeHtml(page, ids = {}) {
  const e = escapeHtml;
  const link = (key, title) =>
    ids[key] ? `<a href="https://docs.google.com/document/d/${e(ids[key])}/edit">${e(title)}</a>` : e(title);
  const h = ['<html><body>', `<h1>${e(page.title)}</h1>`, `<p>${e(page.what)}</p>`];
  h.push(`<p><i>Recorded on ${e(page.asOf)}. Made from the bridge's data in the GitHub repository. If a copy is added or the current one changes, this page has to be made again.</i></p>`);
  h.push('<h2>The book right now</h2>');
  h.push(page.current ? `<p><b>${link(page.current.id, page.current.title)}</b>. ${e(page.current.role)}</p>` : '<p>No copy is marked current.</p>');
  h.push('<h2>Every copy of the book</h2>', '<ul>');
  for (const c of page.copies) {
    h.push(`<li><b>${e(c.state)}</b> (${e(c.holds)}): ${link(c.id, c.title)}. ${e(c.role)}</li>`);
  }
  h.push('</ul>', '<h2>Notes about the book</h2>', '<ul>');
  for (const n of page.notes) h.push(`<li>${link(n.title, n.title)}. ${e(n.what)}</li>`);
  h.push('</ul>', '<h2>How to change the manuscript</h2>', '<ol>');
  for (const step of page.editing) h.push(`<li>${e(step)}</li>`);
  h.push('</ol>', '<h2>House rules</h2>', '<ul>');
  for (const rule of page.rules) h.push(`<li>${e(rule)}</li>`);
  h.push('</ul>', '<h2>If your chat cannot run code</h2>', '<ol>');
  for (const step of page.withoutCode) h.push(`<li>${e(step)}</li>`);
  h.push('</ol>', '<p>The request looks like this:</p>', `<pre>${e(JSON.stringify(page.requestExample, null, 2))}</pre>`);
  h.push('<h2>If your chat can run code</h2>');
  if (page.code) {
    h.push(`<p>The code is in the GitHub repository ${e(page.code.repository)}, on the branch ${e(page.code.branch)}. ${e(page.code.note ?? '')}</p>`);
  }
  h.push('<ul>');
  for (const line of page.withCode) h.push(`<li><code>${e(line)}</code></li>`);
  h.push('</ul>', '</body></html>');
  return h.join('\n');
}
