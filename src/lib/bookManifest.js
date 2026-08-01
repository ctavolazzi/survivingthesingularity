/**
 * BOOK MANIFEST RULES - the shared, runtime-agnostic half of "what the book is".
 *
 * WHY THIS FILE EXISTS
 *
 * Every rule for turning book.json into a name, a label, or an ordered file
 * list used to be written once per consumer. The download filename alone was
 * spelled out in four places: two route components building the href inline,
 * scripts/check-book-downloads.mjs asserting it, and static/_redirects
 * targeting it. On 2026-08-01 the PDF on /exclusive-friends-only 404'd in
 * production because the derived href and the shipped file disagreed - four
 * copies of one string with nothing holding them together.
 *
 * So the RULES live here and the LOADING stays with each caller. Every function
 * below is pure and takes the manifest as an argument: nothing here imports
 * book.json, touches the filesystem, or uses a Vite-only feature. That is what
 * lets the SvelteKit bundle (import book.json), a plain Node prebuild script
 * (readFileSync), and a test harness (a fixture object) all share one rule set
 * without a build step or a generated artifact between them.
 *
 * WHAT DOES *NOT* LIVE HERE
 *
 * scripts/sts.py owns the canonical cross-reference resolver, because it
 * resolves against the manuscript index (sections AND block ids) and raises on
 * a dangling pointer. This file mirrors the section-level half of that rule for
 * the website, which cannot call Python at build time. Those two are held
 * together by scripts/check-resolver-parity.mjs, not by hope - if the Python
 * and JS labels ever disagree, the build fails and names the section.
 */

/** The one place the shipped artifact filename is spelled. */
export const assetName = (version, ext) =>
  `Surviving-the-Singularity-v${version}.${ext}`;

/** The one place a public download URL is built. */
export const downloadHref = (version, ext) => `/downloads/${assetName(version, ext)}`;

/** Formats shipped for every version. Order is display order. */
export const DOWNLOAD_FORMATS = ['pdf', 'epub'];

/**
 * 'Chapter 1: The Event Horizon' -> 'Chapter 1'.
 *
 * Mirrors _section_label() in scripts/sts.py. book.json titles are
 * '<short name>: <descriptive tail>'; the short name is what prose actually
 * says ("as we saw in Chapter 1"), so that is what a generated label expands
 * to. Titles with no colon are used whole.
 */
export const shortLabel = title =>
  (title.includes(':') ? title.split(':')[0] : title).trim();

/**
 * A ref target is a section id ('chapter1') or a block id
 * ('sts.chapter1.b0003'); a block id carries its section in the middle segment.
 */
export const sectionIdFor = target => {
  const parts = target.split('.');
  return parts.length >= 3 && parts[0] === 'sts' ? parts[1] : target;
};

/** Generated label for a ref target, or null if it resolves to no section. */
export const labelFor = (manifest, target) => {
  const section = manifest.sections.find(s => s.id === sectionIdFor(target));
  return section ? shortLabel(section.title) : null;
};

/** [label](sts:target) - target is a section id or a full sts.<sec>.b<NNNN> id. */
export const STS_REF = /\[([^\]\n]*)\]\(sts:([A-Za-z0-9._-]+)\)/g;

/**
 * Expand every sts: cross-reference in `raw` to text.
 *
 * An empty label is generated from the manifest, so renumbering a chapter
 * rewrites every sentence that points at it instead of leaving prose that is
 * quietly wrong. A non-empty label is the author's phrasing and is left alone.
 *
 * `onDangling` decides what a pointer that resolves to nothing does. The
 * website passes the default (drop the marker) because a dangling ref is meant
 * to have been caught upstream by the EPUB build and `sts.py verify refs`;
 * rendering "](sts:..." at a reader is strictly worse than rendering nothing.
 * check-resolver-parity.mjs passes a collector instead, so the same rule can
 * report what it could not resolve rather than swallowing it.
 */
export function expandRefs(manifest, raw, onDangling = () => '') {
  if (!raw || !raw.includes('](sts:')) return raw;
  return raw.replace(STS_REF, (whole, label, target) => {
    if (label.trim()) return label;
    const generated = labelFor(manifest, target);
    return generated ?? onDangling(target, whole);
  });
}

/**
 * Section files in running order.
 *
 * `exclude` drops sections a given consumer cannot use - the EPUB build skips
 * the print-style index, which is generated for the PDF and meaningless in a
 * reflowable format. It is passed as data rather than grepped out downstream so
 * that renaming the file cannot silently stop excluding it.
 */
export const sectionFiles = (manifest, { exclude = [] } = {}) =>
  manifest.sections.map(s => s.file).filter(f => !exclude.includes(f));
