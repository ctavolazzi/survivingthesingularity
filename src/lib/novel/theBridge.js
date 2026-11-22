// The bridge, made from this site's own data. Import it on the server:
//
//   import { bridge, sectionTexts } from '$lib/novel/theBridge.js';
//
// bridge.js says what it can do. Keep this file out of client code, so the
// whole compendium and the map of copies are not shipped to every browser.
import novel from '$lib/data/novel/novel.json';
import compendium from '$lib/data/novel/compendium.json';
import instances from '$lib/data/novel/instances.json';
import { createBridge } from './bridge.js';
import { loadSectionMarkdown } from './novelContent.js';

export const bridge = createBridge({ novel, compendium, instances });

let texts;

/** {sectionId: markdown} for every section the reader holds. Read once. */
export function sectionTexts() {
  texts ??= Promise.all(
    novel.sections.map(async (section) => [section.id, await loadSectionMarkdown(section)])
  ).then(Object.fromEntries);
  return texts;
}
