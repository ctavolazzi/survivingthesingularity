// @ts-check
import { test as baseTest, expect } from '@playwright/test';
import { CONSENT_KEY, CONSENT_VERSION } from '../../../src/lib/consent.js';

export { expect };

/* Block browser requests to remote services and unmocked local APIs. Start the
   local SSR server without service credentials: browser routing cannot control
   server-side fetches or APIRequestContext. Test-specific page.route mocks take
   precedence. Consent and splash seeds leave checklist state untouched. */
export const test = baseTest.extend({
  serviceWorkers: 'block',
  page: async ({ page, baseURL }, use) => {
    if (!baseURL) throw new Error('Isolated browser tests require a local baseURL.');
    const base = new URL(baseURL);
    if (!['http:', 'https:'].includes(base.protocol) ||
        !['localhost', '127.0.0.1', '[::1]', 'host.docker.internal'].includes(base.hostname)) {
      throw new Error('Isolated browser tests only allow a local development server.');
    }

    await page.context().route('**/*', route => {
      const url = new URL(route.request().url());
      if (!['http:', 'https:'].includes(url.protocol)) return route.continue();
      if (url.origin !== base.origin) return route.abort('blockedbyclient');
      if (url.pathname.startsWith('/api/')) {
        return route.fulfill({
          status: 503,
          contentType: 'application/json',
          body: JSON.stringify({ error: 'API disabled in this browser test.' }),
        });
      }
      return route.continue();
    });

    await page.context().addInitScript(({ consentKey, consentVersion }) => {
      localStorage.setItem(consentKey, JSON.stringify({
        version: consentVersion,
        at: '2026-10-10T00:00:00.000Z',
      }));
      sessionStorage.setItem('sts:splash', 'seen');
    }, { consentKey: CONSENT_KEY, consentVersion: CONSENT_VERSION });
    await use(page);
  },
});

/** @param {import('@playwright/test').Page} page */
export async function waitForReady(page) {
  await page.waitForLoadState('domcontentloaded');
  // CSS can hide the SSR overlay before hydration. Only onMount removes it.
  // The removed /signup and /auth/* routes omit this component altogether.
  await expect(page.locator('[data-sts-splash]')).toHaveCount(0, { timeout: 15000 });
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {string} path
 */
export async function gotoReady(page, path) {
  const response = await page.goto(path, { waitUntil: 'domcontentloaded' });
  await waitForReady(page);
  return response;
}

/** @param {import('@playwright/test').Page} page */
export async function reloadReady(page) {
  const response = await page.reload({ waitUntil: 'domcontentloaded' });
  await waitForReady(page);
  return response;
}
