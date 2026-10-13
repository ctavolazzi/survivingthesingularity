import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import test from 'node:test';
import { load as loadBlog } from '../../src/routes/blog/+page.server.js';

const root = new URL('../../', import.meta.url);
const sitemap = readFileSync(new URL('static/sitemap.xml', root), 'utf8');
const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map((match) => new URL(match[1]));

test('the static sitemap is the sole owner and contains only existing public routes', () => {
  for (const extension of ['js', 'ts']) {
    assert.equal(existsSync(new URL(`src/routes/sitemap.xml/+server.${extension}`, root)), false);
  }
  assert.ok(urls.length > 0);
  assert.equal(new Set(urls.map(String)).size, urls.length, 'duplicate canonical URLs');
  for (const url of urls) {
    assert.equal(url.origin, 'https://survivingthesingularity.com');
    assert.equal(url.search, '');
    assert.equal(url.hash, '');
    const route = url.pathname === '/' ? '' : url.pathname;
    assert.equal(existsSync(new URL(`src/routes${route}/+page.svelte`, root)), true, `missing route: ${url.pathname}`);
    assert.doesNotMatch(url.pathname, /^\/(book|read|optional|exclusive-friends-only|unsubscribe|api)(\/|$)/);
    assert.notEqual(url.pathname, '/early-access/success');
    assert.notEqual(url.pathname, '/launch');
  }
  assert.ok(urls.some((url) => url.pathname === '/sample'), 'the open sample must be discoverable');
  assert.doesNotMatch(sitemap, /<lastmod>/, 'omit invented dates; add dates only with verified content metadata');
});

test('every published blog post is discoverable in the sitemap', async () => {
  const paths = new Set(urls.map((url) => url.pathname));
  const { posts } = await loadBlog();
  for (const post of posts) assert.ok(paths.has(post.route), `missing published post: ${post.route}`);
});
