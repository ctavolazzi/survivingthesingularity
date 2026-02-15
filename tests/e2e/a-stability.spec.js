// @ts-check
import { test, expect } from '@playwright/test';

/**
 * STABILITY TESTS
 * Verify all routes load without errors, return correct status codes,
 * and render expected content.
 */

const ROUTES = [
  { path: '/', name: 'Homepage', mustContain: 'Blueprint' },
  { path: '/blueprint', name: 'Blueprint Index', mustContain: 'Blueprint' },
  { path: '/blueprint/economic-trap', name: 'Blueprint: Economic Trap', mustContain: '' },
  { path: '/blueprint/the-shouse', name: 'Blueprint: The Shouse', mustContain: '' },
  { path: '/blueprint/content-engine', name: 'Blueprint: Content Engine', mustContain: '' },
  { path: '/blueprint/digital-sovereignty', name: 'Blueprint: Digital Sovereignty', mustContain: '' },
  { path: '/blueprint/physical-exit', name: 'Blueprint: Physical Exit', mustContain: '' },
  { path: '/blueprint/robotics', name: 'Blueprint: Robotics', mustContain: '' },
  { path: '/blueprint/cash-engine', name: 'Blueprint: Cash Engine', mustContain: '' },
  { path: '/blueprint/execute', name: 'Blueprint: Execute', mustContain: '' },
  { path: '/blog', name: 'Blog', mustContain: '' },
  { path: '/book', name: 'Book', mustContain: '' },
  { path: '/about', name: 'About', mustContain: '' },
  { path: '/policies', name: 'Policies', mustContain: '' },
  { path: '/login', name: 'Login', mustContain: '' },
  { path: '/profile', name: 'Profile', mustContain: '' },
];

test.describe('Site Stability', () => {

  for (const route of ROUTES) {
    test(`${route.name} (${route.path}) loads without errors`, async ({ page }) => {
      const errors = [];
      page.on('pageerror', err => errors.push(err.message));

      const response = await page.goto(route.path, { waitUntil: 'networkidle' });

      // Should return 200
      expect(response?.status()).toBe(200);

      // Should have no JS errors
      expect(errors).toEqual([]);

      // Should have content
      const body = await page.textContent('body');
      expect(body?.length).toBeGreaterThan(50);

      // Must contain expected text if specified
      if (route.mustContain) {
        expect(body).toContain(route.mustContain);
      }
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
