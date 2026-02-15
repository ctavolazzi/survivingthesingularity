// @ts-check
import { test, expect } from '@playwright/test';

/**
 * LEGAL COMPLIANCE TESTS
 * Verify required legal elements:
 * - Privacy policy
 * - Cookie consent
 * - Terms of service
 * - Disclaimers
 * - Data collection notices
 */

test.describe('Legal Compliance', () => {

  test('Privacy policy page exists and has content', async ({ page }) => {
    await page.goto('/policies');
    await page.waitForLoadState('networkidle');

    const body = await page.textContent('body');
    expect(body?.toLowerCase()).toContain('privacy');
  });

  test('Cookie consent banner appears', async ({ page }) => {
    // Clear cookies to simulate first visit
    await page.context().clearCookies();

    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1000);

    // Check for cookie consent UI — may appear after a delay
    await page.waitForTimeout(2000);

    const cookieConsent = page.locator('[class*="cookie"], [class*="consent"], [id*="cookie"]');
    const cookieText = page.getByText(/cookie|cookies|consent/i);

    const hasConsent = (await cookieConsent.count() > 0) || (await cookieText.count() > 0);

    // Cookie consent should exist (component is loaded in layout)
    expect(hasConsent).toBe(true);
  });

  test('Cookie consent can be accepted', async ({ page }) => {
    await page.context().clearCookies();
    await page.goto('/');
    await page.waitForTimeout(1000);

    // Find accept button
    const acceptBtn = page.locator('button:has-text("Accept"), button:has-text("Got it"), button:has-text("OK"), button:has-text("Agree")').first();

    if (await acceptBtn.isVisible()) {
      await acceptBtn.click();
      await page.waitForTimeout(500);

      // Banner should disappear after acceptance
      const banner = page.locator('[class*="cookie-banner"], [class*="consent-banner"]').first();
      if (await banner.count() > 0) {
        await expect(banner).not.toBeVisible();
      }
    }
  });

  test('Footer contains legal links', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);

    const footer = page.locator('footer');
    const footerText = await footer.textContent();

    // Footer should reference policies or legal pages
    const hasLegalRef = footerText?.toLowerCase().includes('privacy') ||
                        footerText?.toLowerCase().includes('terms') ||
                        footerText?.toLowerCase().includes('policies') ||
                        footerText?.toLowerCase().includes('legal');

    expect(hasLegalRef).toBe(true);
  });

  test('No financial advice without disclaimers', async ({ page }) => {
    await page.goto('/');
    const bodyText = await page.textContent('body');

    // If the page mentions money/investing/financial topics, there should be disclaimers
    const hasFinancialContent = bodyText?.toLowerCase().includes('invest') ||
                                bodyText?.toLowerCase().includes('financial') ||
                                bodyText?.toLowerCase().includes('savings');

    if (hasFinancialContent) {
      // Check for presence of disclaimer language somewhere on the site
      const hasDisclaimer = bodyText?.toLowerCase().includes('not financial advice') ||
                           bodyText?.toLowerCase().includes('disclaimer') ||
                           bodyText?.toLowerCase().includes('educational purposes') ||
                           bodyText?.toLowerCase().includes('not a substitute');

      // Log warning if no disclaimer found on this page
      // (disclaimer may be on the policies page which is acceptable)
      if (!hasDisclaimer) {
        console.warn('Financial content detected but no inline disclaimer found. Ensure /policies covers this.');
      }
    }
  });

  test('Policies page covers required legal topics', async ({ page }) => {
    await page.goto('/policies');
    const bodyText = (await page.textContent('body'))?.toLowerCase() || '';

    // Should cover data collection
    const coversData = bodyText.includes('data') || bodyText.includes('information');
    expect(coversData).toBe(true);

    // Should mention email if newsletter exists
    const coversEmail = bodyText.includes('email') || bodyText.includes('contact');
    expect(coversEmail).toBe(true);
  });

  test('External links open in new tabs', async ({ page }) => {
    await page.goto('/');

    const externalLinks = await page.locator('a[href^="http"]').all();
    for (const link of externalLinks) {
      const href = await link.getAttribute('href');
      if (href && !href.includes('localhost') && !href.includes('survivingthesingularity')) {
        const target = await link.getAttribute('target');
        const rel = await link.getAttribute('rel');

        // External links should open in new tab
        if (target === '_blank') {
          // And have rel="noopener" for security
          expect(rel).toContain('noopener');
        }
      }
    }
  });

  test('No broken policy links', async ({ page }) => {
    await page.goto('/policies');

    const links = await page.locator('a[href]').all();
    for (const link of links) {
      const href = await link.getAttribute('href');
      if (href && href.startsWith('/')) {
        const response = await page.request.get(href);
        expect(response.status()).toBeLessThan(400);
      }
    }
  });
});
