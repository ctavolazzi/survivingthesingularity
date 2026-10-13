export const SITE_URL = 'https://survivingthesingularity.com';

// Share the permanent page address, not a visitor's campaign query, access
// token or reading position. This works during SSR and after client navigation.
export function canonicalShareUrl(pathname) {
  const path = new URL(pathname, SITE_URL).pathname.replace(/\/+$/, '') || '/';
  return SITE_URL + path;
}
