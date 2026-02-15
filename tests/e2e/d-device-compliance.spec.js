// @ts-check
import { test, expect } from '@playwright/test';

/**
 * DEVICE COMPLIANCE TESTS
 * Verify the site works across different screen sizes,
 * viewport dimensions, and device capabilities.
 */

const VIEWPORTS = [
  { name: 'iPhone SE', width: 375, height: 667 },
  { name: 'iPhone 14 Pro', width: 393, height: 852 },
  { name: 'Samsung Galaxy S21', width: 360, height: 800 },
  { name: 'iPad Mini', width: 768, height: 1024 },
  { name: 'iPad Pro', width: 1024, height: 1366 },
  { name: 'Laptop', width: 1366, height: 768 },
  { name: 'Desktop', width: 1920, height: 1080 },
  { name: 'Ultrawide', width: 2560, height: 1080 },
];

test.describe('Device Compliance', () => {

  for (const viewport of VIEWPORTS) {
    test(`Homepage renders on ${viewport.name} (${viewport.width}x${viewport.height})`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('/');
      await page.waitForLoadState('networkidle');

      // Should have visible content
      const body = await page.locator('body');
      await expect(body).toBeVisible();

      // No horizontal overflow
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
      expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 5); // 5px tolerance
    });
  }

  for (const viewport of VIEWPORTS) {
    test(`Blueprint page renders on ${viewport.name}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('/blueprint');
      await page.waitForLoadState('networkidle');

      const body = await page.locator('body');
      await expect(body).toBeVisible();

      // No horizontal overflow
      const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
      const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
      expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 5);
    });
  }

  test('Text is readable at minimum font size', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Check that body text isn't too small
    const fontSizes = await page.evaluate(() => {
      const textElements = document.querySelectorAll('p, span, li, a, h1, h2, h3');
      const sizes = [];
      textElements.forEach(el => {
        const style = window.getComputedStyle(el);
        const size = parseFloat(style.fontSize);
        if (el.textContent?.trim() && size > 0) {
          sizes.push(size);
        }
      });
      return sizes;
    });

    // No text should be smaller than 10px on mobile
    const tooSmall = fontSizes.filter(s => s < 10);
    if (tooSmall.length > 0) {
      console.warn(`Found ${tooSmall.length} elements with font-size < 10px`);
    }
    // Allow some very small elements (badges, labels) but majority should be readable
    expect(tooSmall.length).toBeLessThan(fontSizes.length * 0.15);
  });

  test('Touch targets are large enough on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    const smallTargets = await page.evaluate(() => {
      const clickables = document.querySelectorAll('a, button, input, select, [role="button"]');
      const issues = [];
      clickables.forEach(el => {
        const rect = el.getBoundingClientRect();
        // Only check visible elements
        if (rect.width > 0 && rect.height > 0 && rect.top < window.innerHeight) {
          if (rect.width < 44 || rect.height < 44) {
            issues.push({
              tag: el.tagName,
              text: el.textContent?.slice(0, 30),
              width: rect.width.toFixed(0),
              height: rect.height.toFixed(0)
            });
          }
        }
      });
      return issues;
    });

    if (smallTargets.length > 0) {
      console.warn('Small touch targets found:', smallTargets.slice(0, 10));
    }
    // Some small targets are acceptable (icon buttons, etc.)
    // But flag if there are too many
    expect(smallTargets.length).toBeLessThan(20);
  });

  test('Navbar is visible on all screen sizes', async ({ page }) => {
    for (const viewport of VIEWPORTS) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('/');

      const nav = page.locator('nav').first();
      await expect(nav).toBeVisible();
    }
  });

  test('No content cut off on small screens', async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 568 }); // iPhone 5/SE size
    await page.goto('/');

    // Check for overflow
    const hasOverflow = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth + 5;
    });

    expect(hasOverflow).toBe(false);
  });
});
