/**
 * Registry of interactive "explorable" widgets that can be embedded inline
 * in book chapters. A chapter markdown file drops a marker on its own line:
 *
 *   [[interactive:local-grid-sizer]]
 *
 * and src/routes/book/[sectionId]/+page.svelte splits the raw markdown on
 * that marker and renders the matching component from this map at that
 * exact point in the chapter. To add a new explorable: build the component,
 * import it here, add one entry. Nothing else needs to change.
 */
import LocalGridSizer from './LocalGridSizer.svelte';

export const interactiveRegistry = {
  'local-grid-sizer': LocalGridSizer
};
