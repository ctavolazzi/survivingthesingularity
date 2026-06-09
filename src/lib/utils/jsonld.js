/**
 * Safely serialize a JSON-LD object for inline injection into a
 * <script type="application/ld+json"> tag.
 *
 * JSON.stringify alone is NOT safe inside <script>: a value containing
 * "</script>" breaks out of the tag and enables script injection. We escape
 * the angle brackets (and ampersand) so the payload can never close the tag.
 * Content is parsed as JSON-LD, not eval'd, so U+2028/U+2029 are irrelevant.
 *
 * @param {Record<string, unknown>} data
 * @returns {string} escaped JSON string safe to drop between script tags
 */
export function jsonLd(data) {
  return JSON.stringify(data)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/&/g, '\\u0026');
}
