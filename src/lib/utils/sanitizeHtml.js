import sanitize from 'sanitize-html';

// Parser-based sanitization works in browsers, Node, and Cloudflare Workers.
// Workers have no DOM: a DOMPurify browser build cannot sanitize server output.
// Keep this allowlist explicit. KaTeX emits HTML spans and occasionally static
// SVG paths; it does not need executable SVG, MathML, forms, or embedded pages.
const length = /^-?(?:\d+(?:\.\d+)?|\.\d+)(?:em|ex|px|%)?$/;
const positiveLength = /^(?:\d+(?:\.\d+)?|\.\d+)(?:em|ex|px|%)?$/;
const numericStyles = Object.fromEntries([
  'height', 'width', 'min-width', 'max-width', 'top', 'left',
  'margin-left', 'margin-right', 'margin-top', 'margin-bottom',
  'padding-left', 'padding-right', 'padding-top', 'padding-bottom',
  'vertical-align', 'border-bottom-width', 'font-size',
].map((property) => [property, [length]]));

export const markdownSanitizerOptions = {
  allowedTags: [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr',
    'blockquote', 'ul', 'ol', 'li', 'dl', 'dt', 'dd',
    'a', 'em', 'strong', 'b', 'i', 's', 'del', 'u', 'small',
    'sub', 'sup', 'code', 'pre', 'kbd', 'samp', 'mark',
    'div', 'span', 'aside', 'figure', 'figcaption', 'img',
    'table', 'caption', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
    'svg', 'path',
  ],
  allowedAttributes: {
    '*': ['class', 'title'],
    a: ['href', 'rel', { name: 'target', values: ['_blank', '_self'] }],
    img: ['src', 'alt', 'width', 'height', { name: 'loading', values: ['lazy', 'eager'] }, { name: 'decoding', values: ['async', 'sync', 'auto'] }],
    ol: ['start', 'reversed'],
    li: ['value'],
    th: ['colspan', 'rowspan', { name: 'align', values: ['left', 'center', 'right'] }, { name: 'scope', values: ['row', 'col', 'rowgroup', 'colgroup'] }],
    td: ['colspan', 'rowspan', { name: 'align', values: ['left', 'center', 'right'] }],
    span: ['style', { name: 'aria-hidden', values: ['true', 'false'] }],
    svg: ['xmlns', 'width', 'height', 'viewbox', 'preserveaspectratio'],
    path: ['d'],
  },
  allowedStyles: {
    span: { ...numericStyles, position: [/^relative$/] },
  },
  allowedSchemes: ['https', 'http', 'mailto'],
  allowedSchemesByTag: { img: ['https', 'http'] },
  allowProtocolRelative: false,
  disallowedTagsMode: 'discard',
  transformTags: {
    a(tagName, attributes) {
      if (attributes.target === '_blank') attributes.rel = 'noopener noreferrer';
      return { tagName, attribs: attributes };
    },
    svg(tagName, attributes) {
      // KaTeX's SVG is geometry only. In particular, no href/xlink:href,
      // namespaced HTML, animation, style, or event-handler attributes survive.
      if (attributes.xmlns !== 'http://www.w3.org/2000/svg') delete attributes.xmlns;
      for (const key of ['width', 'height']) {
        if (!positiveLength.test(attributes[key] ?? '')) delete attributes[key];
      }
      if (!/^-?[\d.]+(?:[ ,]+-?[\d.]+){3}$/.test(attributes.viewbox ?? '')) delete attributes.viewbox;
      if (!/^(?:xMin|xMid|xMax)(?:YMin|YMid|YMax)(?: (?:meet|slice))?$/.test(attributes.preserveaspectratio ?? '')) delete attributes.preserveaspectratio;
      return { tagName, attribs: attributes };
    },
    path(tagName, attributes) {
      if (!/^[MmLlHhVvCcSsQqTtAaZz\dEe.,+\-\s]+$/.test(attributes.d ?? '')) delete attributes.d;
      return { tagName, attribs: attributes };
    },
  },
};

/** Sanitize a rendered Markdown fragment without relying on a global DOM. */
export function sanitizeHtml(html) {
  return sanitize(html, markdownSanitizerOptions);
}
