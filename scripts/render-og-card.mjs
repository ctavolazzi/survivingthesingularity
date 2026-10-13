// Render the existing HTML card at an exact CSS viewport. Chrome's screenshot
// CLI uses an outer window size and can clip the bottom at newer browser sizes.
import { chromium } from '@playwright/test';
import { pathToFileURL } from 'node:url';

const [source, output] = process.argv.slice(2);
if (!source || !output) throw new Error('Usage: node scripts/render-og-card.mjs <html> <png>');
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 2 });
  await page.route(/^https?:/, (route) => route.abort());
  await page.goto(pathToFileURL(source).href);
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((image) => image.decode()));
    if (document.fonts.status !== 'loaded') throw new Error('Card fonts did not load');
    for (const element of document.querySelectorAll('.eyebrow, h1, p, .chiprow, .cover img')) {
      const box = element.getBoundingClientRect();
      if (box.top < 0 || box.left < 0 || box.bottom > innerHeight || box.right > innerWidth) {
        throw new Error(`Card content clips: ${element.className || element.tagName}`);
      }
    }
  });
  await page.screenshot({ path: output });
} finally {
  await browser.close();
}
