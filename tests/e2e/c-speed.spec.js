// @ts-check
import { test, expect } from '@playwright/test';

/**
 * SPEED / PERFORMANCE TESTS
 * Verify pages load within acceptable timeframes,
 * measure key performance metrics.
 */

test.describe('Performance', () => {

  test('Homepage loads under 3 seconds', async ({ page }) => {
    const start = Date.now();
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    const loadTime = Date.now() - start;

    expect(loadTime).toBeLessThan(3000);
    console.log(`Homepage load time: ${loadTime}ms`);
  });

  test('Blueprint index loads under 3 seconds', async ({ page }) => {
    const start = Date.now();
    await page.goto('/blueprint', { waitUntil: 'domcontentloaded' });
    const loadTime = Date.now() - start;

    expect(loadTime).toBeLessThan(3000);
    console.log(`Blueprint load time: ${loadTime}ms`);
  });

  test('Blueprint section loads under 3 seconds', async ({ page }) => {
    const start = Date.now();
    await page.goto('/blueprint/economic-trap', { waitUntil: 'domcontentloaded' });
    const loadTime = Date.now() - start;

    expect(loadTime).toBeLessThan(3000);
    console.log(`Blueprint section load time: ${loadTime}ms`);
  });

  test('Blog page loads under 3 seconds', async ({ page }) => {
    const start = Date.now();
    await page.goto('/blog', { waitUntil: 'domcontentloaded' });
    const loadTime = Date.now() - start;

    expect(loadTime).toBeLessThan(3000);
    console.log(`Blog load time: ${loadTime}ms`);
  });

  test('No images larger than 500KB', async ({ page }) => {
    const largeAssets = [];

    page.on('response', response => {
      const contentType = response.headers()['content-type'] || '';
      const contentLength = parseInt(response.headers()['content-length'] || '0');

      if (contentType.startsWith('image/') && contentLength > 500 * 1024) {
        largeAssets.push({
          url: response.url(),
          size: `${(contentLength / 1024).toFixed(0)}KB`,
          type: contentType
        });
      }
    });

    await page.goto('/', { waitUntil: 'networkidle' });

    if (largeAssets.length > 0) {
      console.warn('Large images found:', largeAssets);
    }
    expect(largeAssets.length).toBe(0);
  });

  test('No blocking requests over 5 seconds', async ({ page }) => {
    const slowRequests = [];

    page.on('requestfinished', async request => {
      const timing = request.timing();
      const totalTime = timing.responseEnd;

      if (totalTime > 5000) {
        slowRequests.push({
          url: request.url(),
          time: `${totalTime.toFixed(0)}ms`,
          method: request.method()
        });
      }
    });

    await page.goto('/', { waitUntil: 'networkidle' });

    if (slowRequests.length > 0) {
      console.warn('Slow requests:', slowRequests);
    }
    expect(slowRequests.length).toBe(0);
  });

  test('Page navigation is fast (under 2 seconds)', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const start = Date.now();
    await page.goto('/blueprint');
    await page.waitForLoadState('domcontentloaded');
    const navTime = Date.now() - start;

    expect(navTime).toBeLessThan(2000);
    console.log(`Navigation time (/ -> /blueprint): ${navTime}ms`);
  });

  test('Total page weight is reasonable (under 2MB)', async ({ page }) => {
    let totalBytes = 0;

    page.on('response', response => {
      const contentLength = parseInt(response.headers()['content-length'] || '0');
      totalBytes += contentLength;
    });

    await page.goto('/', { waitUntil: 'networkidle' });

    const totalKB = totalBytes / 1024;
    const totalMB = totalKB / 1024;
    console.log(`Total page weight: ${totalKB.toFixed(0)}KB (${totalMB.toFixed(2)}MB)`);

    expect(totalMB).toBeLessThan(2);
  });

  test('First Contentful Paint metrics', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });

    const fcp = await page.evaluate(() => {
      return new Promise((resolve) => {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const fcpEntry = entries.find(e => e.name === 'first-contentful-paint');
          if (fcpEntry) {
            resolve(fcpEntry.startTime);
          }
        });
        observer.observe({ entryTypes: ['paint'] });

        // Fallback if FCP already happened
        const existing = performance.getEntriesByName('first-contentful-paint');
        if (existing.length > 0) {
          resolve(existing[0].startTime);
        }

        // Timeout fallback
        setTimeout(() => resolve(-1), 5000);
      });
    });

    if (fcp > 0) {
      console.log(`First Contentful Paint: ${fcp}ms`);
      expect(fcp).toBeLessThan(2500);
    }
  });
});
