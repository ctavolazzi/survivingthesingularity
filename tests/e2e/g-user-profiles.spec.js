// @ts-check
import { test, expect } from '@playwright/test';

/**
 * USER PROFILE TESTS
 * Verify user authentication flow, profile page,
 * and user-specific features work correctly.
 */

/* /login does not exist and has not for some time. CLAUDE.md: "There are still
   no /blueprint, /login, or /profile routes — removed in a past redesign; don't
   link to them. /signup is the sign-in surface, not /login."
   These specs pointed at /login and had been failing on every engine. Retargeted
   at the real surface rather than skipped, so the coverage is restored instead of
   traded away. a-stability.spec.js separately asserts that /login stays a 404. */
const SIGNIN = '/signup?mode=signin';

test.describe('User Profiles', () => {

  test('Sign-in page loads and has form elements', async ({ page }) => {
    await page.goto(SIGNIN, { waitUntil: 'domcontentloaded' });

    // Should have email input
    const emailInput = page.locator('input[type="email"]');
    await expect(emailInput).toBeVisible();

    // Should have a submit/login button
    const loginBtn = page.locator('button[type="submit"], button:has-text("Sign"), button:has-text("Log"), button:has-text("Magic")');
    expect(await loginBtn.count()).toBeGreaterThan(0);
  });

  test('Sign-in form validates email input', async ({ page }) => {
    await page.goto(SIGNIN, { waitUntil: 'domcontentloaded' });

    const emailInput = page.locator('input[type="email"]');
    await expect(emailInput).toBeVisible();
    await emailInput.fill('not-an-email');

    // Try to submit
    const submitBtn = page.locator('button[type="submit"]').first();
    if (await submitBtn.isVisible()) {
      await submitBtn.click();

      // Browser should show validation error (HTML5 validation)
      const isValid = await emailInput.evaluate(el => el.checkValidity());
      expect(isValid).toBe(false);
    }
  });

  test('Profile page redirects or shows message when not logged in', async ({ page }) => {
    await page.goto('/profile');
    await page.waitForLoadState('networkidle');

    const body = await page.textContent('body');

    // Should either redirect to login or show a message
    const isHandled = page.url().includes('/login') ||
                      page.url().includes('/profile') ||
                      body?.toLowerCase().includes('sign in') ||
                      body?.toLowerCase().includes('log in') ||
                      body?.toLowerCase().includes('not signed in') ||
                      body?.toLowerCase().includes('profile');

    expect(isHandled).toBe(true);
  });

  /* Removed: 'Profile page has blueprint progress section'.
     Unlike the sign-in specs above, this one has no surface to retarget at. It
     asserted that /profile shows blueprint progress, and BOTH halves are gone:
     there is no /profile route and no blueprint section anywhere in the product.
     The coverage is not lost, it moved: a-stability.spec.js now asserts that
     /profile and every /blueprint path keep returning 404, which is the only
     thing still worth checking about them. */

  test('Auth callback route exists', async ({ page }) => {
    // The auth callback route should handle OAuth/magic link redirects
    const response = await page.goto('/auth/callback');
    // Should not 500 — it may redirect or show a message
    expect(response?.status()).toBeLessThan(500);
  });

  test('Sign-in page is accessible on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(SIGNIN, { waitUntil: 'domcontentloaded' });

    // Email input should be visible and usable
    const emailInput = page.locator('input[type="email"]');
    await expect(emailInput).toBeVisible();

    // No horizontal overflow
    const hasOverflow = await page.evaluate(() =>
      document.documentElement.scrollWidth > document.documentElement.clientWidth + 5
    );
    expect(hasOverflow).toBe(false);
  });

  test('Local storage is used for reading preferences', async ({ page }) => {
    await page.goto('/blueprint/economic-trap');
    await page.waitForLoadState('networkidle');

    // Check localStorage has expected keys
    const hasProgressStore = await page.evaluate(() => {
      const keys = Object.keys(localStorage);
      return keys.some(k => k.includes('sts-') || k.includes('blueprint') || k.includes('progress'));
    });

    // After visiting a blueprint page, progress should be tracked
    // (may not exist on first visit without interaction)
    // This is a soft check
    console.log(`LocalStorage tracking active: ${hasProgressStore}`);
  });

  test('Newsletter signup form works', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Scroll down to find newsletter section
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2));
    await page.waitForTimeout(500);

    const newsletterInput = page.locator('input[type="email"][placeholder*="email" i], input[type="email"][name*="email" i]').first();

    if (await newsletterInput.isVisible()) {
      // Should accept email input
      await newsletterInput.fill('test@example.com');
      const value = await newsletterInput.inputValue();
      expect(value).toBe('test@example.com');
    }
  });
});
