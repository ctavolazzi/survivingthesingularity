import { error } from '@sveltejs/kit';

// The novel reader opens from a private link, /novel/<key>/, instead of a
// password. Only the SHA-256 of the key lives in this public repository, so
// the link itself can't be read out of the code. A wrong key is a plain 404,
// the same as any page that doesn't exist.
const KEY_SHA256 = '5bdd0d7de6edad119b6d5c44a6c5ac8e86d4900883f5f38de5bb0effef789284';

export const prerender = false;

async function sha256Hex(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function load({ params, setHeaders }) {
  if ((await sha256Hex(params.key)) !== KEY_SHA256) throw error(404, 'Not found');
  setHeaders({ 'x-robots-tag': 'noindex, nofollow', 'cache-control': 'private, no-store' });
  return { base: `/novel/${params.key}` };
}
