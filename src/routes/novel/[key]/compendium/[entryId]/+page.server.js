import { error } from '@sveltejs/kit';
import { bridge, sectionTexts } from '$lib/novel/theBridge.js';

export async function load({ params, parent }) {
  // The novel layout checks the private key; nothing loads until it has passed.
  const { base } = await parent();
  const entry = bridge.entry(params.entryId);
  if (!entry) throw error(404, 'Not found');
  const topic = bridge.topic(entry.topic);
  const tokens = (text) => bridge.tokens(text, base);
  const card = (e) => ({ id: e.id, name: e.name, summary: e.summary, href: bridge.href(e.id, base) });

  const linked = bridge
    .linksFrom(entry.id)
    .map((ref) => bridge.resolve(ref))
    .filter((found) => found?.kind === 'entry')
    .map((found) => card(found.item));

  return {
    entry: {
      id: entry.id,
      name: entry.name,
      summary: tokens(entry.summary),
      image: entry.image ?? null,
      facts: (entry.facts ?? []).map((fact) => ({ label: fact.label, value: tokens(fact.value) })),
      body: (entry.body ?? []).map(tokens),
      quotes: (entry.quotes ?? []).map((quote) => ({ text: quote.text, from: tokens(quote.from) }))
    },
    topic: { id: topic.id, name: topic.name, mark: topic.mark },
    linked,
    mentionedIn: bridge.backlinks(entry.id).map(card),
    appearances: bridge
      .appearances(entry.id, await sectionTexts())
      .map((a) => ({ ...a, href: bridge.href(`section:${a.id}`, base) }))
  };
}
