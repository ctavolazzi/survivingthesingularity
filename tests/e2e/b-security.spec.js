// @ts-check
import { test, expect } from '@playwright/test';

/**
 * SECURITY TESTS
 * Check for common web security issues:
 * - XSS vectors
 * - Open redirects
 * - Sensitive data exposure
 * - Security headers
 * - Cookie security
 * - Input sanitization
 */

test.describe('Security', () => {

  test('No sensitive data in HTML source', async ({ page }) => {
    await page.goto('/');
    const html = await page.content();

    // Should not contain API keys, tokens, or secrets
    expect(html).not.toMatch(/sk[-_][a-zA-Z0-9]{20,}/);  // Stripe-like keys
    expect(html).not.toMatch(/eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}/);  // JWTs (require longer segments)
    expect(html.toLowerCase()).not.toMatch(/api[_-]?key\s*[:=]\s*["'][^"']{20,}/);
    expect(html.toLowerCase()).not.toMatch(/secret[_-]?key\s*[:=]\s*["'][^"']{20,}/);
  });

  test('No sensitive data in blueprint pages', async ({ page }) => {
    await page.goto('/blueprint/economic-trap');
    const html = await page.content();
    expect(html).not.toMatch(/sk[-_][a-zA-Z0-9]{20,}/);
    expect(html).not.toMatch(/eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+/);
  });

  test('XSS attempt in URL path is neutralized', async ({ page }) => {
    // Attempt script injection via URL
    const response = await page.goto('/<script>alert(1)</script>');
    const html = await page.content();
    // Should not execute or reflect the script
    expect(html).not.toContain('<script>alert(1)</script>');
  });

  test('XSS attempt in query params is neutralized', async ({ page }) => {
    await page.goto('/?q=<script>alert(1)</script>');
    const html = await page.content();
    expect(html).not.toContain('<script>alert(1)</script>');
  });

  test('No open redirect vulnerability', async ({ page }) => {
    // Try common open redirect patterns via query param
    await page.goto('/?redirect=https://evil.com');
    // Should not have been redirected to external domain
    const hostname = new URL(page.url()).hostname;
    expect(hostname).toBe('localhost');
  });

  test('Cookie security flags', async ({ page }) => {
    await page.goto('/');
    const cookies = await page.context().cookies();

    for (const cookie of cookies) {
      // If there are cookies, they should have secure attributes
      if (cookie.name.includes('session') || cookie.name.includes('auth')) {
        expect(cookie.httpOnly).toBe(true);
        // SameSite should be set
        expect(['Strict', 'Lax', 'None']).toContain(cookie.sameSite);
      }
    }
  });

  test('No directory listing exposed', async ({ page }) => {
    const response = await page.goto('/src/');
    // Should not show directory listing — may 404 or show app shell
    const body = await page.textContent('body');
    expect(body).not.toContain('Index of');
    // Source files should not be directly accessible
    expect(body).not.toMatch(/\.svelte\b.*\.svelte\b/); // Multiple .svelte files = directory listing
  });

  test('Environment variables not exposed to client', async ({ page }) => {
    await page.goto('/');
    const html = await page.content();

    // Private env vars should never appear in client HTML
    expect(html).not.toContain('SUPABASE_SERVICE_ROLE');
    expect(html).not.toContain('DATABASE_URL');
    expect(html).not.toContain('PRIVATE_');
  });

  test('Login page does not expose auth details in URL', async ({ page }) => {
    await page.goto('/login');
    // Should not have tokens/codes in URL on initial load
    expect(page.url()).not.toMatch(/token=|code=|key=/);
  });

  test('Forms have CSRF-like protection (no direct POST to external)', async ({ page }) => {
    await page.goto('/');
    const forms = await page.locator('form').all();

    for (const form of forms) {
      const action = await form.getAttribute('action');
      // Forms should not post directly to external URLs
      if (action) {
        expect(action).not.toMatch(/^https?:\/\/(?!localhost)/);
      }
    }
  });
});
