import { marked } from 'marked';
import DOMPurify from 'isomorphic-dompurify';
import { katexExtension } from './katexExtension.js';
import imageDimensions from '../data/book/image-dimensions.json';
import visuals from '../data/book/visuals.json';

// Configure once per module, including when a route reuses its component.
marked.use(katexExtension);
const layouts = new Set(['diagram', 'cutout-left', 'cutout-right', 'inset']);
const basename = (src) => src.split(/[?#]/)[0].split('/').pop();

export function renderMarkdown(source) {
  let html = DOMPurify.sanitize(marked(source));
  html = html.replace(/<img\b[^>]*>/g, (tag) => {
    const src = tag.match(/\bsrc="([^"]+)"/)?.[1];
    if (!src) return tag;
    const file = basename(src);
    const dimensions = visuals.images[file]?.pixels || imageDimensions[file];
    const width = Array.isArray(dimensions) ? dimensions[0] : dimensions?.width;
    const height = Array.isArray(dimensions) ? dimensions[1] : dimensions?.height;
    let attrs = ' loading="lazy" decoding="async"';
    if (width > 0 && height > 0) attrs += ` width="${Number(width)}" height="${Number(height)}"`;
    return tag.replace(/\s(?:width|height|loading|decoding)="[^"]*"/g, '').replace(/\s*\/?>(?=$)/, `${attrs}>`);
  });
  // Only standalone, registered images become editorial figures. Captions remain
  // actual manuscript text; alt text remains on the image for assistive readers.
  return html.replace(/<p>\s*(<img\b[^>]*>)\s*<\/p>(?:\s*<p>(<em>(?:(?!<\/p>)[\s\S])*?<\/em>)<\/p>)?/g, (block, image, caption) => {
    const file = basename(image.match(/\bsrc="([^"]+)"/)?.[1] || '');
    const visual = visuals.images[file];
    if (!visual || !layouts.has(visual.layout)) return block;
    return `<figure class="book-figure figure-${visual.layout}">${image}${caption ? `<figcaption>${caption}</figcaption>` : ''}</figure>`;
  });
}
