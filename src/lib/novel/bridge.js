// The bridge: one object that knows where the book lives and how its parts
// point at each other.
//
// It is built from three plain data files and has no imports, so the site, a
// script and a test can all make one and pass it around:
//
//   novel       src/lib/data/novel/novel.json        the sections, in reading order
//   compendium  src/lib/data/novel/compendium.json   topics and entries (people, places, ...)
//   instances   src/lib/data/novel/instances.json    every copy of the book and which version it holds
//
// The map is data, not code. A switch statement can only answer "given this
// name, what is it?". Kept as data, the same map also answers the questions
// that run the other way: what links here, which copies are behind, what is
// broken. The one switch that is left is in resolve(), where a reference is
// turned into the thing it names.
//
// Links inside entry text are written [[id]] or [[id|words to show]]. An id is
// an entry id, or carries its kind: [[section:chapter-0|Chapter 0]].

const LINK = /\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]/g;
const KINDS = ['entry', 'topic', 'section', 'instance'];

/** Split "kind:id" into its two halves. A bare id is an entry. */
export function parseRef(ref) {
  const text = String(ref ?? '').trim();
  const at = text.indexOf(':');
  if (at > 0 && KINDS.includes(text.slice(0, at))) {
    return { kind: text.slice(0, at), id: text.slice(at + 1) };
  }
  return { kind: 'entry', id: text };
}

/** Markdown from the reader's files, as plain paragraphs of words. */
export function plainParagraphs(markdown) {
  return String(markdown ?? '')
    .split(/\n\s*\n/)
    .map((p) => p.trim())
    .filter((p) => p && !p.startsWith('#') && !p.startsWith('![') && p !== '* * *')
    .map((p) => p.replace(/<[^>]+>/g, ''));
}

/**
 * @param {{novel: any, compendium: any, instances: any}} data
 */
export function createBridge({ novel, compendium, instances }) {
  const sections = novel?.sections ?? [];
  const topics = compendium?.topics ?? [];
  const entries = compendium?.entries ?? [];
  const copies = instances?.instances ?? [];
  const order = instances?.versions ?? [];

  const byId = (list) => new Map(list.map((item) => [item.id, item]));
  const sectionMap = byId(sections);
  const topicMap = byId(topics);
  const entryMap = byId(entries);
  const copyMap = byId(copies);

  /** The thing a reference names, or null. This is the switch. */
  function resolve(ref) {
    const { kind, id } = parseRef(ref);
    let item = null;
    let title = '';
    switch (kind) {
      case 'entry':
        item = entryMap.get(id) ?? null;
        title = item?.name ?? '';
        break;
      case 'topic':
        item = topicMap.get(id) ?? null;
        title = item?.name ?? '';
        break;
      case 'section':
        item = sectionMap.get(id) ?? null;
        title = item?.title ?? '';
        break;
      case 'instance':
        item = copyMap.get(id) ?? null;
        title = item?.title ?? item?.path ?? '';
        break;
    }
    return item ? { kind, id, title, item } : null;
  }

  /** Where a reference opens on the site. `base` is the private reader's root. */
  function href(ref, base = '') {
    const { kind, id } = parseRef(ref);
    switch (kind) {
      case 'entry':
        return `${base}/compendium/${id}`;
      case 'topic':
        return `${base}/compendium#topic-${id}`;
      case 'section':
        return `${base}/${id}`;
      default:
        return null;
    }
  }

  /**
   * Entry text as pieces the page can draw without trusting any HTML:
   * {text} for words, {text, ref, kind, id, href, missing} for a link.
   */
  function tokens(text, base = '') {
    const out = [];
    const source = String(text ?? '');
    let last = 0;
    for (const m of source.matchAll(LINK)) {
      if (m.index > last) out.push({ text: source.slice(last, m.index) });
      const found = resolve(m[1]);
      const { kind, id } = parseRef(m[1]);
      out.push({
        text: m[2] ?? found?.title ?? id,
        ref: `${kind}:${id}`,
        kind,
        id,
        href: found ? href(m[1], base) : null,
        missing: !found
      });
      last = m.index + m[0].length;
    }
    if (last < source.length) out.push({ text: source.slice(last) });
    return out;
  }

  /** Every string in an entry that can hold a link. */
  function linkTexts(entry) {
    return [
      entry.summary ?? '',
      ...(entry.body ?? []),
      ...(entry.facts ?? []).map((f) => f.value ?? ''),
      ...(entry.quotes ?? []).map((q) => q.from ?? '')
    ];
  }

  /** The references an entry makes, once each, in the order they appear. */
  function linksFrom(entryId) {
    const entry = entryMap.get(entryId);
    if (!entry) return [];
    const seen = new Set();
    for (const text of linkTexts(entry)) {
      for (const m of text.matchAll(LINK)) {
        const { kind, id } = parseRef(m[1]);
        seen.add(`${kind}:${id}`);
      }
    }
    return [...seen];
  }

  /** The entries that link to this one. */
  function backlinks(entryId) {
    return entries.filter((e) => e.id !== entryId && linksFrom(e.id).includes(`entry:${entryId}`));
  }

  /** Topics in order, each with its entries sorted by name. */
  function tree() {
    return topics.map((topic) => ({
      ...topic,
      entries: entries
        .filter((e) => e.topic === topic.id)
        .sort((a, b) => a.name.localeCompare(b.name))
    }));
  }

  /**
   * Where an entry is named in the book. `texts` is {sectionId: markdown},
   * the reader's own files, so the answer is about the copy the site holds.
   * A paragraph counts when it matches the entry's `find` pattern. It misses
   * scenes where someone is present and not named.
   */
  function appearances(entryId, texts) {
    const entry = entryMap.get(entryId);
    if (!entry?.find) return [];
    const pattern = new RegExp(entry.find);
    const out = [];
    for (const section of sections) {
      const count = plainParagraphs(texts?.[section.id]).filter((p) => pattern.test(p)).length;
      if (count) out.push({ id: section.id, title: section.title, group: section.group, paragraphs: count });
    }
    return out;
  }

  /** The copy of the manuscript that is the book right now. */
  function current() {
    return copies.find((c) => c.current) ?? null;
  }

  /**
   * Every copy of the book and how far it is behind the current one.
   * `behind` is counted in versions from the `holds` label written in
   * instances.json. It is what was recorded on the file's `asOf` date, not a
   * fresh measurement. null means the copy's version is not in the list.
   */
  function status() {
    const now = current();
    const top = now ? order.indexOf(now.holds) : -1;
    return copies.map((c) => {
      const at = order.indexOf(c.holds);
      const behind = top < 0 || at < 0 ? null : top - at;
      // `stale` marks a copy that carries the current version's name but was
      // made before that version's latest edits.
      return { id: c.id, kind: c.kind, title: c.title ?? c.path, holds: c.holds, current: Boolean(c.current), behind, stale: Boolean(c.stale) };
    });
  }

  /** Everything wrong with the map. An empty list means it holds together. */
  function check() {
    const problems = [];
    const say = (where, what) => problems.push({ where, what });
    const dupes = (list, kind) => {
      const seen = new Set();
      for (const item of list) {
        if (seen.has(item.id)) say(`${kind}:${item.id}`, 'this id is used twice');
        seen.add(item.id);
      }
    };
    dupes(topics, 'topic');
    dupes(entries, 'entry');
    dupes(copies, 'instance');
    dupes(sections, 'section');

    for (const topic of topics) {
      if (!entries.some((e) => e.topic === topic.id)) say(`topic:${topic.id}`, 'has no entries');
    }
    for (const entry of entries) {
      const where = `entry:${entry.id}`;
      if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(entry.id ?? '')) say(where, 'the id must be lowercase words joined by hyphens');
      if (!topicMap.has(entry.topic)) say(where, `topic "${entry.topic}" does not exist`);
      if (!entry.name) say(where, 'has no name');
      if (!entry.summary) say(where, 'has no summary');
      if (!entry.body?.length) say(where, 'has no text');
      if (entry.find) {
        try {
          new RegExp(entry.find);
        } catch {
          say(where, `the find pattern is not valid: ${entry.find}`);
        }
      }
      for (const ref of linksFrom(entry.id)) {
        if (!resolve(ref)) say(where, `links to ${ref}, which does not exist`);
        if (ref === `entry:${entry.id}`) say(where, 'links to itself');
      }
      if (/[\u2013\u2014]/.test(linkTexts(entry).join(' ') + entry.name)) say(where, 'has an en dash or em dash');
    }

    const live = copies.filter((c) => c.current);
    if (copies.length && live.length !== 1) say('instances', `${live.length} copies are marked current; there must be exactly one`);
    for (const copy of copies) {
      const where = `instance:${copy.id}`;
      if (copy.from && !copyMap.has(copy.from)) say(where, `was made from "${copy.from}", which is not in the map`);
      if (!order.includes(copy.holds)) say(where, `holds "${copy.holds}", which is not in the list of versions`);
    }
    return problems;
  }

  return {
    novel,
    topics,
    entries,
    sections,
    instances: copies,
    notes: instances?.notes ?? [],
    versions: order,
    asOf: instances?.asOf ?? null,
    section: (id) => sectionMap.get(id) ?? null,
    topic: (id) => topicMap.get(id) ?? null,
    entry: (id) => entryMap.get(id) ?? null,
    instance: (id) => copyMap.get(id) ?? null,
    resolve,
    href,
    tokens,
    linksFrom,
    backlinks,
    tree,
    appearances,
    current,
    status,
    check
  };
}
