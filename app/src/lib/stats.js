/**
 * DERIVED STATS
 *
 * Every number that appears on the sales page carries the artifact it came
 * from. The `source` field is not decoration and it is not a tooltip. It is
 * rendered on the page, under the number, in mono.
 *
 * Why this file exists.
 *
 * On 2026-07-29 the live homepage said "The Precedent File: 29 documented
 * cases". The book contains 23, P-01 through P-23. The project's own harness
 * says so:
 *
 *   $ python3 scripts/sts.py verify
 *     precedents  P-01..P-23 ledger integrity
 *       OK     all 23 present in the book and indexed in Appendix D
 *
 * The likeliest origin of the 29 is that the site has 29 pages. That is exactly
 * the kind of collision hardcoding produces, on the one asset whose entire
 * pitch is that a reader can check the work.
 *
 * The rule this file enforces: if a number cannot be derived, it does not go on
 * the page.
 *
 * MVP STATUS: these are literals with their provenance recorded alongside. In
 * production they are emitted at build time by scripts/sts.py, which already
 * computes every one of them. See `PRODUCTION_WIRING` at the bottom.
 */

/** @typedef {{ key: string, value: string, label: string, source: string, measuredOn: string }} Stat */

/** @type {readonly Stat[]} */
export const stats = Object.freeze([
  Object.freeze({
    key: 'precedents',
    value: '23',
    label: 'documented precedents',
    source: 'counted from the book source',
    measuredOn: '2026-07-29'
  }),
  Object.freeze({
    key: 'words',
    value: '90,623',
    label: 'words, across 30 sections',
    source: 'measured by the build harness',
    measuredOn: '2026-07-29'
  }),
  Object.freeze({
    key: 'sources',
    value: '186',
    label: 'sources in Works Cited',
    source: 'link-checked, 1 currently dead',
    measuredOn: '2026-07-29'
  }),
  Object.freeze({
    key: 'price',
    value: '$5',
    label: 'once, then nothing',
    source: 'the only price on this site',
    measuredOn: '2026-07-29'
  })
]);

/** The eyebrow line above the headline. Composed, not typed. */
export const eyebrow = `${stat('words').value} words. ${stat('precedents').value} precedents. Last revised 27 July 2026.`;

/**
 * @param {string} key
 * @returns {Stat}
 */
export function stat(key) {
  const found = stats.find((s) => s.key === key);
  if (!found) throw new Error(`unknown stat: ${key}`);
  return found;
}

/**
 * PRODUCTION_WIRING
 *
 * Replacing the literals above is a small job because the harness already
 * produces all four numbers. At build time:
 *
 *   precedents  rg -c '^## Precedent P-[0-9]+' src/lib/data/book/*.md
 *   words       python3 scripts/sts.py status   (book: N words)
 *   sources     python3 scripts/sts.py verify --links
 *   sections    manuscript-index.json length
 *
 * Write the result to src/lib/stats.generated.json in a prebuild step and have
 * this module read it. The `source` strings stay hand-written, because the
 * provenance of a number is a claim about method and a script cannot make it.
 */
