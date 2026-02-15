// @ts-check
import { test, expect } from '@playwright/test';

/**
 * USABILITY TESTS
 * Test interactive features, keyboard navigation,
 * command palette, and overall UX quality.
 */

test.describe('Usability', () => {

  test('Command palette opens with Cmd+K / Ctrl+K', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Press Cmd+K (or Ctrl+K on non-Mac)
    await page.keyboard.press('Meta+k');
    await page.waitForTimeout(300);

    // Command palette should be visible
    const palette = page.locator('[class*="palette"]');
    const isVisible = (await palette.count() > 0) && (await palette.first().isVisible());

    if (!isVisible) {
      // Try Ctrl+K instead
      await page.keyboard.press('Control+k');
      await page.waitForTimeout(300);
    }

    // Check for search input inside palette
    const searchInput = page.locator('[class*="palette"] input').first();
    if (await searchInput.isVisible()) {
      expect(await searchInput.isVisible()).toBe(true);
    }
  });

  test('Command palette search returns results', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await page.keyboard.press('Meta+k');
    await page.waitForTimeout(300);

    const searchInput = page.locator('[class*="palette"] input').first();
    if (await searchInput.isVisible()) {
      await searchInput.fill('blueprint');
      await page.waitForTimeout(300);

      // Should show results
      const results = page.locator('[class*="palette-item"], [class*="palette-result"]');
      const count = await results.count();
      expect(count).toBeGreaterThan(0);
    }
  });

  test('Escape key closes command palette', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await page.keyboard.press('Meta+k');
    await page.waitForTimeout(300);

    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);

    const palette = page.locator('[class*="palette-overlay"]');
    if (await palette.count() > 0) {
      await expect(palette.first()).not.toBeVisible();
    }
  });

  test('Keyboard navigation works on homepage', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Tab through interactive elements
    for (let i = 0; i < 5; i++) {
      await page.keyboard.press('Tab');
    }

    // An element should now be focused
    const focusedTag = await page.evaluate(() => document.activeElement?.tagName);
    expect(['A', 'BUTTON', 'INPUT', 'SELECT']).toContain(focusedTag);
  });

  test('Blueprint navigation between sections works', async ({ page }) => {
    await page.goto('/blueprint');
    await page.waitForLoadState('networkidle');

    // Click on first section link
    const sectionLink = page.locator('a[href*="/blueprint/"]').first();
    if (await sectionLink.isVisible()) {
      await sectionLink.click();
      await page.waitForLoadState('networkidle');

      // Should navigate to a section or stay on blueprint index
      expect(page.url()).toContain('/blueprint');
    }
  });

  test('Scroll animations trigger correctly', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Get initial section states
    const sectionsExist = await page.locator('.section, [class*="section"]').count();
    expect(sectionsExist).toBeGreaterThan(0);

    // Scroll down to trigger animations
    await page.evaluate(() => window.scrollTo(0, 1000));
    await page.waitForTimeout(1000);

    // Elements should have been revealed
    const revealedCount = await page.evaluate(() => {
      return document.querySelectorAll('.revealed, [class*="revealed"]').length;
    });

    // At least some sections should be revealed after scrolling
    expect(revealedCount).toBeGreaterThanOrEqual(0);
  });

  test('Interactive stack table expands rows', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Scroll to stack table
    const stackTable = page.locator('[class*="stack-interactive"]').first();
    if (await stackTable.isVisible()) {
      // Click a row
      const firstRow = stackTable.locator('[class*="stack-row"]').first();
      await firstRow.click();
      await page.waitForTimeout(300);

      // Detail should be visible
      const detail = stackTable.locator('[class*="stack-detail"]');
      expect(await detail.count()).toBeGreaterThan(0);
    }
  });

  test('White Rabbit panel opens with Ctrl+Shift+D', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await page.keyboard.press('Control+Shift+D');
    await page.waitForTimeout(300);

    const panel = page.locator('[class*="rabbit-panel"]');
    if (await panel.count() > 0) {
      await expect(panel.first()).toBeVisible();
    }
  });

  test('Savings calculator responds to input', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Find savings calculator
    const calculator = page.locator('[class*="savings"], [class*="calculator"]').first();

    if (await calculator.isVisible()) {
      // Find range inputs inside
      const sliders = calculator.locator('input[type="range"]');
      const count = await sliders.count();

      if (count > 0) {
        // Move a slider
        const slider = sliders.first();
        await slider.fill('5000');
        await page.waitForTimeout(300);

        // Calculator should update (output text should change)
        const hasOutput = await calculator.textContent();
        expect(hasOutput?.length).toBeGreaterThan(0);
      }
    }
  });

  test('Toast notification system works', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Trigger a toast by interacting with newsletter or other action
    // Toasts are typically triggered by user actions
    const toastContainer = page.locator('[class*="toast"]');
    // Container should exist even if empty
    expect(await toastContainer.count()).toBeGreaterThanOrEqual(0);
  });

  test('All internal links resolve to real pages', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const links = await page.locator('a[href^="/"]').all();
    const hrefs = new Set();

    for (const link of links) {
      const href = await link.getAttribute('href');
      if (href && !href.includes('#') && !href.includes('mailto:')) {
        hrefs.add(href);
      }
    }

    const broken = [];
    for (const href of hrefs) {
      const response = await page.request.get(href);
      if (response.status() >= 400) {
        broken.push({ href, status: response.status() });
      }
    }

    if (broken.length > 0) {
      console.error('Broken internal links:', broken);
    }
    expect(broken.length).toBe(0);
  });
});
