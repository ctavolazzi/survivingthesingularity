import katex from 'katex';

// KaTeX support for the book renderer, deliberately narrower than the stock
// marked-katex extension.
//
// WHY THE PATTERN IS RESTRICTED: the manuscript carries 24 dollar AMOUNTS
// ($25,000, $150, $211, $10,000, $40) in the same chapters that carry math.
// 15-chapter13.md has $25,000 three times and six equations. A default
// `$...$` inline rule will eventually swallow the prose between two prices
// and render it as math. Today no two prices share a line, so nothing
// collides yet - that makes it a latent bug, not a current one, and it is
// exactly the kind of thing that surfaces after a later edit joins two
// paragraphs.
//
// The rule: an inline span may only OPEN on a letter or a TeX backslash, and
// may not CLOSE immediately before a digit. Every price in the book opens on
// a digit, so no price can start a span. Every math span in the book opens on
// a letter ($Q$, $k-1$, $e(t)$, $Q = 4$), so none of them are lost.
// Display math has no such ambiguity and uses plain $$...$$.

const INLINE_MATH = /^\$([A-Za-z\\][^$\n]{0,80}?)\$(?!\d)/;
const BLOCK_MATH = /^\$\$([\s\S]{1,600}?)\$\$(?:\n|$)/;

// Degrade to the source text with the delimiters stripped, which is exactly
// what the unconverted chapters already look like on the page. A KaTeX parse
// error must never reach the reader as raw TeX or as KaTeX's red error string.
function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function render(tex, displayMode) {
  try {
    return katex.renderToString(tex, {
      displayMode,
      throwOnError: true,
      strict: false,
      output: 'html'
    });
  } catch (error) {
    if (typeof console !== 'undefined' && console.warn) {
      console.warn(`[katex] falling back to plain text for: ${tex}`, error?.message);
    }
    const fallback = escapeHtml(tex.trim());
    return displayMode
      ? `<span class="math-fallback math-fallback-display">${fallback}</span>`
      : `<span class="math-fallback">${fallback}</span>`;
  }
}

export const katexExtension = {
  extensions: [
    {
      name: 'mathBlock',
      level: 'block',
      start(src) {
        return src.indexOf('$$');
      },
      tokenizer(src) {
        const match = BLOCK_MATH.exec(src);
        if (!match) return undefined;
        return { type: 'mathBlock', raw: match[0], text: match[1].trim() };
      },
      renderer(token) {
        return render(token.text, true);
      }
    },
    {
      name: 'mathInline',
      level: 'inline',
      start(src) {
        // Only wake the tokenizer on a `$` that could legally open a span,
        // so prices never even enter the hot path.
        const match = /\$[A-Za-z\\]/.exec(src);
        return match ? match.index : undefined;
      },
      tokenizer(src) {
        const match = INLINE_MATH.exec(src);
        if (!match) return undefined;
        return { type: 'mathInline', raw: match[0], text: match[1].trim() };
      },
      renderer(token) {
        return render(token.text, false);
      }
    }
  ]
};
