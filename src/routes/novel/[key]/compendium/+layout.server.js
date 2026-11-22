import { bridge } from '$lib/novel/theBridge.js';

export async function load({ parent }) {
  // The novel layout checks the private key; nothing loads until it has passed.
  const { base } = await parent();
  return {
    base,
    tree: bridge.tree().map((topic) => ({
      id: topic.id,
      name: topic.name,
      mark: topic.mark,
      blurb: topic.blurb,
      entries: topic.entries.map((entry) => ({
        id: entry.id,
        name: entry.name,
        summary: entry.summary,
        href: bridge.href(entry.id, base)
      }))
    }))
  };
}
