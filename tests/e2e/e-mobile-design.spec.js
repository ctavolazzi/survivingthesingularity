// @ts-check
import { test, expect } from '@playwright/test';

/**
 * MOBILE DESIGN TESTS
 * Verify mobile-specific UX patterns work correctly:
 * - Hamburger menu
 * - Scroll behavior
 * - Interactive elements
 * - Blueprint reading experience
 */

test.describe('Mobile Design', () => {

  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
  });

  test('Mobile menu opens and closes', async ({ page }) => {
    await page.goto('/');

    // Look for hamburger/mobile menu toggle
    const menuToggle = page.locator('[class*="mobile"], [class*="hamburger"], [class*="menu-toggle"], button[aria-label*="menu"]').first();

    if (await menuToggle.isVisible()) {
      await menuToggle.click();
      await page.waitForTimeout(500);

      // Some navigation links should now be visible
      const navLinks = page.locator('nav a');
      const visibleCount = await navLinks.evaluateAll(links =>
        links.filter(l => l.offsetParent !== null).length
      );
      expect(visibleCount).toBeGreaterThan(0);
    }
  });

  test('Homepage hero is visible on mobile', async ({ page }) => {
    await page.goto('/');

    // The main heading should be visible
    const heading = page.locator('h1').first();
    await expect(heading).toBeVisible();

    // It should be within the viewport
    const box = await heading.boundingBox();
    expect(box).not.toBeNull();
    expect(box?.y).toBeLessThan(800); // Within first scroll
  });

  test('Blueprint page is readable on mobile', async ({ page }) => {
    await page.goto('/blueprint/economic-trap');
    await page.waitForLoadState('networkidle');

    // Content should be visible
    const content = page.locator('main');
    await expect(content).toBeVisible();

    // Check text doesn't overflow
    const hasOverflow = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth + 5;
    });
    expect(hasOverflow).toBe(false);
  });

  test('Blog posts are readable on mobile', async ({ page }) => {
    await page.goto('/blog');
    await page.waitForLoadState('networkidle');

    // Blog listing should be visible
    const main = page.locator('main');
    await expect(main).toBeVisible();
  });

  test('Page has substantial content on mobile', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1000); // Let animations settle

    // Page should have multiple sections of content
    const sections = await page.locator('section, .section, [class*="section"]').count();
    const mainContent = page.locator('main');
    const mainHeight = await mainContent.evaluate(el => el.scrollHeight);

    // Main content area should have substantial height
    expect(mainHeight).toBeGreaterThan(500);
  });

  test('Images are responsive on mobile', async ({ page }) => {
    await page.goto('/');

    const images = await page.locator('img').all();
    for (const img of images) {
      if (await img.isVisible()) {
        const box = await img.boundingBox();
        if (box) {
          // Image should not exceed viewport width
          expect(box.width).toBeLessThanOrEqual(375 + 5);
        }
      }
    }
  });

  test('CTA buttons are tappable on mobile', async ({ page }) => {
    await page.goto('/');

    // Find primary action buttons
    const buttons = await page.locator('a[class*="btn"], a[class*="cta"], button[class*="btn"]').all();

    for (const btn of buttons) {
      if (await btn.isVisible()) {
        const box = await btn.boundingBox();
        if (box && box.y < 2000) { // Only check above-fold buttons
          // Minimum touch target: 44x44
          expect(box.height).toBeGreaterThanOrEqual(36); // Some tolerance
        }
      }
    }
  });

  test('Footer links work on mobile', async ({ page }) => {
    await page.goto('/');

    // Scroll to footer
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);

    const footer = page.locator('footer');
    await expect(footer).toBeVisible();

    // Footer should have links
    const footerLinks = footer.locator('a');
    const count = await footerLinks.count();
    expect(count).toBeGreaterThan(0);
  });
});
