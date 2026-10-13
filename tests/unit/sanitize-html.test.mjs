import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Marked } from 'marked';
import { sanitizeHtml } from '../../src/lib/utils/sanitizeHtml.js';
import { katexExtension } from '../../src/lib/utils/katexExtension.js';

test('Markdown sanitization works without a browser DOM', () => {
  assert.equal(typeof globalThis.window, 'undefined');
  assert.equal(typeof globalThis.document, 'undefined');
  assert.equal(sanitizeHtml('<p>Hello <strong>reader</strong>.</p>'), '<p>Hello <strong>reader</strong>.</p>');
});

test('manuscript asides, tables, images, and accessible math attributes survive', () => {
  const html = sanitizeHtml('<aside class="numbers"><h3>Numbers</h3><table><thead><tr><th align="right" scope="col">Cost</th></tr></thead><tbody><tr><td colspan="2">$150</td></tr></tbody></table><img src="/book_images/diagram.png" alt="A diagram" width="400" height="250" loading="lazy" decoding="async"><span class="katex-html" aria-hidden="true">x</span></aside>');
  assert.match(html, /<aside class="numbers">/);
  assert.match(html, /<th align="right" scope="col">Cost<\/th>/);
  assert.match(html, /<td colspan="2">\$150<\/td>/);
  assert.match(html, /src="\/book_images\/diagram.png" alt="A diagram" width="400" height="250" loading="lazy" decoding="async"/);
  assert.match(html, /<span class="katex-html" aria-hidden="true">x<\/span>/);
});

test('active HTML and attributes are removed while ordinary text remains', () => {
  const html = sanitizeHtml('<p id="location" onclick="alert(1)">Read this.</p><script>alert(1)</script><style>body{display:none}</style><iframe src="https://evil.test"></iframe><object data="https://evil.test"></object><form action="https://evil.test"><input name="email"></form><img src="/safe.png" onerror="alert(1)">');
  assert.equal(html, '<p>Read this.</p><img src="/safe.png" />');
});

test('encoded unsafe URLs cannot become anchor or image destinations', () => {
  const unsafeUrls = [
    'javascript:alert(1)', 'jAvAsCrIpT:alert(1)', 'java&#x73;cript:alert(1)',
    'java&#x09;script:alert(1)', 'java&#10;script:alert(1)', 'java&#13;script:alert(1)',
    'data:text/html;base64,PHNjcmlwdD4=', 'vbscript:msgbox(1)', '//evil.test/image.png',
  ];
  for (const url of unsafeUrls) {
    const html = sanitizeHtml(`<a href="${url}">Link</a><img src="${url}">`);
    assert.doesNotMatch(html, /(?:href|src)=/, url);
  }
  assert.equal(sanitizeHtml('<a href="/sample">Sample</a><a href="https://example.com">Source</a><a href="mailto:hello@example.com">Email</a>'), '<a href="/sample">Sample</a><a href="https://example.com">Source</a><a href="mailto:hello@example.com">Email</a>');
  assert.equal(sanitizeHtml('<img src="mailto:hello@example.com">'), '<img />');
});

test('new-tab links receive safe relationship attributes', () => {
  assert.equal(sanitizeHtml('<a href="https://example.com" target="_blank" rel="opener">Source</a>'), '<a href="https://example.com" target="_blank" rel="noopener noreferrer">Source</a>');
});

test('only numerical KaTeX positioning styles survive', () => {
  const html = sanitizeHtml('<span style="height:1.2em;vertical-align:-0.2em;position:relative;left:0em;background:url(javascript:alert(1));behavior:url(evil);color:red;transform:translateX(1px)" onmouseover="alert(1)">x</span><span style="position:fixed;top:0;z-index:99999;width:expression(alert(1))">y</span>');
  assert.match(html, /style="height:1.2em;vertical-align:-0.2em;position:relative;left:0em"/);
  assert.doesNotMatch(html, /background|behavior|color|transform|onmouseover|fixed|z-index|expression|url\(/i);
});

test('KaTeX stretching geometry survives without active SVG or MathML', () => {
  const markdown = new Marked(katexExtension);
  const html = sanitizeHtml(markdown.parse('$\\sqrt{x} + \\overbrace{a+b}^{c} + \\frac{x}{y}$'));
  assert.match(html, /class="katex"/);
  assert.match(html, /<svg[^>]+viewbox="[0-9 ]+"[^>]+preserveaspectratio="xMinYMin slice"/);
  assert.match(html, /<path d="M[\s\S]+?<\/path>/);
  assert.match(html, /border-bottom-width:0.04em/);
  const malicious = sanitizeHtml('<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><foreignObject><script>alert(1)</script></foreignObject><use href="https://evil.test/x.svg#x"></use><animate attributeName="href" values="javascript:alert(1)"></animate><path d="M0 0L1 1" onclick="alert(1)" xlink:href="javascript:alert(1)"></path></svg><math><mtext><img src="x" onerror="alert(1)"></mtext></math>');
  assert.match(malicious, /<path d="M0 0L1 1"><\/path>/);
  assert.doesNotMatch(malicious, /foreignObject|script|<use|animate|onload|onclick|onerror|href|<math/i);
});

test('malformed namespace markup remains inert after sanitization', () => {
  const payloads = [
    ['<svg><p><style><img src=x onerror=alert(1)></style></p></svg>', '<svg><p></p></svg>'],
    ['<math><mtext><table><mglyph><style><!--</style><img title="--><img src=x onerror=alert(1)>">', '<table><img title="--&gt;&lt;img src=x onerror=alert(1)&gt;" /></table>'],
    ['<svg></p><style><a id="</style><img src=x onerror=alert(1)>">', '<svg><p></p></svg>'],
  ];
  for (const [payload, expected] of payloads) {
    const html = sanitizeHtml(payload);
    assert.equal(html, expected, 'Payload text must stay escaped inside attributes');
    assert.equal(sanitizeHtml(html), html, 'Reparsing must not introduce active markup');
  }
});
