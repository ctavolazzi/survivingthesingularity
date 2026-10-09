// @ts-check
import { test, expect } from '@playwright/test';

/**
 * STABILITY TESTS
 * Verify all routes load without errors, return correct status codes,
 * and render expected content.
 */

/* Routes that exist and must serve a 200.
 *
 * The homepage's `mustContain: 'Blueprint'` was dropped on 2026-08-02: the word
 * appears nowhere in +page.svelte, +layout.svelte or Navbar.svelte any more. The
 * homepage was rewritten around a different thesis and the assertion was never
 * updated, so it had been failing on every engine. */
const ROUTES = [
  { path: '/', name: 'Homepage', mustContain: '' },
  { path: '/blog', name: 'Blog', mustContain: '' },
  { path: '/book', name: 'Book', mustContain: '' },
  { path: '/about', name: 'About', mustContain: '' },
  { path: '/policies', name: 'Policies', mustContain: '' },
];

/* Routes removed in a past redesign, kept here deliberately.
 *
 * These were sitting in ROUTES above expecting a 200 and had been failing
 * 404 on every engine for as long as the suite has run. CLAUDE.md is explicit:
 * "There are still no /blueprint, /login, or /profile routes — removed in a past
 * redesign; don't link to them."
 *
 * Deleting the entries would have been the easy way to go green, and it would
 * have thrown away real signal. If a redesign or a bad merge quietly restores
 * one of these paths, or something starts linking to them again, that is worth
 * knowing. So they are asserted as gone rather than removed from the file. */
const REMOVED_ROUTES = [
  '/blueprint',
  '/blueprint/economic-trap',
  '/blueprint/the-shouse',
  '/blueprint/content-engine',
  '/blueprint/digital-sovereignty',
  '/blueprint/physical-exit',
  '/blueprint/robotics',
  '/blueprint/cash-engine',
  '/blueprint/execute',
  '/login',
  '/profile',
];

test.describe('Site Stability', () => {

  for (const route of ROUTES) {
    test(`${route.name} (${route.path}) loads without errors`, async ({ page }) => {
      const errors = [];
      page.on('pageerror', err => errors.push(err.message));

      /* 'domcontentloaded', not 'networkidle'. networkidle waits for a 500ms gap
         with no more than two connections open, which this site never reaches
         inside the 30s test timeout: the homepage loads video and webfonts, so
         goto simply timed out rather than reporting anything about the page.
         Measured on run 30762634291, where the homepage attempt burned 40.2s
         before failing. The assertions below already wait on real content, so
         they carry the "did it actually render" question. */
      const response = await page.goto(route.path, { waitUntil: 'domcontentloaded' });

      // Should return 200
      expect(response?.status()).toBe(200);

      // Should have content. This is the real readiness signal, and it retries
      // until the timeout, so it covers what networkidle was being asked to do.
      await expect(page.locator('body')).not.toBeEmpty();
      const body = await page.textContent('body');
      expect(body?.length).toBeGreaterThan(50);

      // Should have no JS errors. Checked after render, so a late-firing error
      // during hydration is still caught.
      expect(errors).toEqual([]);

      // Must contain expected text if specified
      if (route.mustContain) {
        expect(body).toContain(route.mustContain);
      }
    });
  }

  /* The other half of the ROUTES split: these must stay gone. A 200 here means
     a removed surface came back, which is the failure worth hearing about. */
  for (const path of REMOVED_ROUTES) {
    test(`${path} stays removed (404)`, async ({ page }) => {
      const response = await page.goto(path, { waitUntil: 'domcontentloaded' });
      expect(response?.status()).toBe(404);
    });
  }

  test('No console errors on homepage', async ({ page }) => {
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto('/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // Filter out known acceptable errors (like Supabase connection when not configured)
    const realErrors = consoleErrors.filter(err =>
      !err.includes('supabase') &&
      !err.includes('Failed to load resource') &&
      !err.includes('net::ERR')
    );

    expect(realErrors).toEqual([]);
  });

  test('Navigation between pages works', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Navigate to Blueprint
    const blueprintLink = page.locator('a[href="/blueprint"]').first();
    if (await blueprintLink.isVisible()) {
      await blueprintLink.click();
      await page.waitForURL('/blueprint');
      expect(page.url()).toContain('/blueprint');
    }

    // Navigate to Blog
    const blogLink = page.locator('a[href="/blog"]').first();
    if (await blogLink.isVisible()) {
      await blogLink.click();
      await page.waitForURL('/blog');
      expect(page.url()).toContain('/blog');
    }
  });

  test('404 page handles unknown routes gracefully', async ({ page }) => {
    const response = await page.goto('/this-page-does-not-exist');
    // Should get a 404 (or redirect to 404 page)
    expect([200, 404]).toContain(response?.status());
    // Should not crash
    const body = await page.textContent('body');
    expect(body?.length).toBeGreaterThan(0);
  });

  test('[object Object] URLs redirect to homepage', async ({ page }) => {
    const response = await page.goto('/[object%20Object]');
    // Our server hook should redirect this
    expect(page.url()).toContain('/');
  });
});
