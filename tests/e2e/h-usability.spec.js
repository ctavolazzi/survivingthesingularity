// @ts-check
import { test, expect, gotoReady } from './helpers/isolated-page.js';

// These assertions require current, visible behavior. A missing feature must
// fail its check instead of conditionally bypassing the assertion.
test.describe('Usability', () => {
  for (const shortcut of ['Meta+k', 'Control+k']) {
    test(`Command palette opens and focuses search with ${shortcut}`, async ({ page }) => {
      await gotoReady(page, '/');
      await page.keyboard.press(shortcut);
      await expect(page.getByRole('dialog', { name: 'Command palette' })).toBeVisible();
      await expect(page.getByPlaceholder('Search pages...')).toBeFocused();
    });
  }

  test('Command palette filters current pages and reports no matches', async ({ page }) => {
    await gotoReady(page, '/');
    await page.keyboard.press('Control+k');
    const dialog = page.getByRole('dialog', { name: 'Command palette' });
    await expect(dialog).toBeVisible();
    const search = dialog.getByPlaceholder('Search pages...');
    await search.fill('blog');
    await expect(dialog.locator('.palette-item')).toHaveCount(1);
    await expect(dialog.locator('.palette-item-title')).toHaveText('Blog');
    await search.fill('no-matching-page-xyz');
    await expect(dialog.locator('.palette-item')).toHaveCount(0);
    await expect(dialog.locator('.palette-empty')).toContainText('No results');
  });

  test('Escape closes an open command palette', async ({ page }) => {
    await gotoReady(page, '/');
    await page.keyboard.press('Control+k');
    const dialog = page.getByRole('dialog', { name: 'Command palette' });
    await expect(dialog).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(dialog).toHaveCount(0);
  });

  test('Command palette keyboard selection navigates to Blog', async ({ page }) => {
    await gotoReady(page, '/');
    await page.keyboard.press('Control+k');
    await page.getByPlaceholder('Search pages...').fill('blog');
    await expect(page.locator('.palette-item-title')).toHaveText('Blog');
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(/\/blog$/);
    await expect(page.getByRole('dialog', { name: 'Command palette' })).toHaveCount(0);
    await expect(page.locator('main h1')).toBeVisible();
  });

  test('First interactive keyboard stop skips navigation and focuses main content', async ({ page, browserName }) => {
    await gotoReady(page, '/');
    await page.keyboard.press('Tab');
    // Firefox focuses the scrollable body before its first interactive child.
    // This also occurs in plain HTML with the site's overflow/height rules.
    if (browserName === 'firefox' && await page.locator('body').evaluate(el => el === document.activeElement)) {
      await expect(page.locator('body')).toHaveCSS('overflow-y', 'auto');
      await page.keyboard.press('Tab');
    }
    await expect(page.locator('a[href="#main-content"]')).toBeFocused();
    await page.keyboard.press('Enter');
    await expect(page.locator('#main-content')).toBeFocused();
  });

  test('Scrolling reveals the final call to action', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    await gotoReady(page, '/');
    const callToAction = page.locator('.cta-inner.reveal');
    await expect(callToAction).toHaveCount(1);
    await expect(callToAction).not.toHaveClass(/\bvisible\b/);
    await callToAction.scrollIntoViewIfNeeded();
    await expect(callToAction).toHaveClass(/\bvisible\b/);
    await expect(callToAction).toHaveCSS('opacity', '1');
  });

  test('Thank-you dialog opens and its close control works', async ({ page }) => {
    await gotoReady(page, '/');
    await page.getByRole('button', { name: /Thank you for being here/ }).click();
    const dialog = page.getByRole('dialog', { name: 'Thank You', exact: true });
    await expect(dialog).toBeVisible();
    await dialog.getByRole('button', { name: 'Close dialog', exact: true }).click();
    await expect(dialog).toHaveCount(0);
  });

  test('Homepage exposes current navigation and internal links resolve', async ({ page }) => {
    await gotoReady(page, '/');
    const hrefs = await page.locator('a[href^="/"]').evaluateAll(links =>
      [...new Set(links.map(link => link.getAttribute('href')).filter(Boolean))]
    );
    for (const required of ['/book', '/blog', '/early-access', '/checklist', '/about']) {
      expect(hrefs).toContain(required);
    }
    for (const href of hrefs) {
      if (!href || href.startsWith('//')) continue;
      const origin = new URL(page.url()).origin;
      let target = new URL(href, origin);
      for (let hop = 0; hop < 6; hop++) {
        // APIRequestContext bypasses browser routing. Validate each redirect
        // before making another request, including its origin and API path.
        expect(target.origin).toBe(origin);
        expect(target.pathname).not.toMatch(/^\/api(?:\/|$)/);
        const response = await page.request.get(target.href, { maxRedirects: 0 });
        if ([301, 302, 303, 307, 308].includes(response.status())) {
          expect(hop, `${href} redirects too many times`).toBeLessThan(5);
          const location = response.headers().location;
          expect(location, `${href} redirect needs a destination`).toBeTruthy();
          target = new URL(location, target);
        } else {
          expect(response.ok(), `${href} must resolve (${response.status()})`).toBe(true);
          break;
        }
      }
    }
  });
});
