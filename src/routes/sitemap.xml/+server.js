import { sections as blueprintSections } from '$lib/data/blueprint.js';
import { book } from '$lib/bookContent.js';

const SITE = 'https://survivingthesingularity.com';

// Discover every static page route at build time. Each key looks like
// '/src/routes/about/+page.svelte'; we strip the wrapper to get the URL path.
const pageModules = import.meta.glob('/src/routes/**/+page.svelte');

function routeToPath(file) {
  let p = file.replace('/src/routes', '').replace('/+page.svelte', '');
  if (p === '') p = '/';
  return p;
}

function buildUrls() {
  const paths = new Set();

  for (const file of Object.keys(pageModules)) {
    const p = routeToPath(file);
    // Skip dynamic routes ([param]) and private/group segments - dynamic
    // routes are expanded explicitly from their data below.
    if (p.includes('[') || p.includes('(')) continue;
    paths.add(p);
  }

  // Expand dynamic routes from their data sources.
  for (const s of blueprintSections) paths.add(`/blueprint/${s.slug}`);
  for (const s of book.sections) paths.add(`/book/${s.id}`);

  return [...paths].sort();
}

export async function GET() {
  const urls = buildUrls();
  const now = new Date().toISOString().slice(0, 10);

  const body =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    urls
      .map((p) => {
        const priority = p === '/' ? '1.0' : p.split('/').length <= 2 ? '0.8' : '0.6';
        return `  <url>\n    <loc>${SITE}${p}</loc>\n    <lastmod>${now}</lastmod>\n    <priority>${priority}</priority>\n  </url>`;
      })
      .join('\n') +
    `\n</urlset>\n`;

  return new Response(body, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'max-age=3600',
    },
  });
}
