import { expect, test } from '@playwright/test';
import { BOOK_ACCESS_PASSWORD } from '../../src/lib/bookAccessCode.js';

// Deliberately hostile browser conditions. Every external request and write
// is blocked unless a test installs its own local response. No email or charge.
async function isolate(context, baseURL) {
  const origin = new URL(baseURL).origin;
  if (!['localhost', '127.0.0.1', '[::1]'].includes(new URL(origin).hostname)) {
    throw new Error('Resilience tests require an isolated local server.');
  }
  await context.route('**/*', route => {
    const request = route.request();
    return new URL(request.url()).origin !== origin || !['GET', 'HEAD'].includes(request.method())
      ? route.abort() : route.continue();
  });
}

test.beforeEach(async ({ context, baseURL }) => {
  await isolate(context, baseURL);
});

async function privateStorage(context, mode) {
  await context.addInitScript(mode => {
    if (mode === 'denied') {
      for (const key of ['localStorage', 'sessionStorage']) {
        Object.defineProperty(window, key, { get() { throw new DOMException('Storage is disabled', 'SecurityError'); } });
      }
    } else {
      sessionStorage.setItem('sts:splash', 'seen');
      Storage.prototype.setItem = () => { throw new DOMException('Storage is full', 'QuotaExceededError'); };
      Storage.prototype.removeItem = () => { throw new DOMException('Storage is full', 'QuotaExceededError'); };
    }
  }, mode);
}

for (const mode of ['denied', 'write-failure']) {
  test(`pages and checklist unlock remain usable with ${mode} storage`, async ({ page, context }) => {
    await privateStorage(context, mode);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    for (const path of ['/', '/sample', '/early-access', '/book']) {
      await page.goto(path, { waitUntil: 'networkidle' });
      await expect(page.locator('h1').first()).not.toHaveText('Internal Error');
      await page.getByRole('button', { name: 'Open menu', exact: true }).click();
      await expect(page.getByRole('dialog', { name: 'Site menu' })).toBeVisible();
      await page.keyboard.press('Escape');
    }
    let signups = 0;
    await page.route('**/api/waitlist', route => { signups++; return route.fulfill({ status: 201, json: { ok: true } }); });
    await page.route('**/api/checklist-email', route => route.fulfill({ status: 503, json: { error: 'Email is temporarily unavailable.' } }));
    await page.goto('/checklist', { waitUntil: 'networkidle' });
    await expect(page.getByText('Browser storage is unavailable.', { exact: false })).toBeVisible();
    await page.locator('#check-title-01').click();
    await expect(page.locator('#check-01')).toBeChecked();
    const form = page.locator('form').filter({ has: page.getByRole('button', { name: 'Unlock Free', exact: true }) });
    await form.getByRole('textbox', { name: 'Email address', exact: true }).fill('reader@example.test');
    await form.getByRole('button', { name: 'Unlock Free', exact: true }).click();
    await expect(page.locator('input.cl-check-native')).toHaveCount(7);
    await expect(page.getByRole('alert')).toContainText('Email is temporarily unavailable');
    expect(signups).toBe(1);
    await page.goto('/book', { waitUntil: 'networkidle' });
    await page.getByLabel('Book access password', { exact: true }).fill(BOOK_ACCESS_PASSWORD);
    await page.getByRole('button', { name: 'Unlock', exact: true }).click();
    await page.getByRole('link', { name: /Read it straight through/ }).click();
    await expect(page.locator('.reader')).toHaveAttribute('data-size', 'medium');
    await page.getByRole('button', { name: 'Larger text', exact: true }).click();
    await expect(page.locator('.reader')).toHaveAttribute('data-size', 'large');
    expect(errors).toEqual([]);
  });
}

for (const stored of ['not json', 'null', '"saved text"', '{"01":{"checked":42,"notes":100}}', '{"01":{"checked":"false","notes":{"bad":true}},"__proto__":{"checked":true}}']) {
  test(`malformed stored preferences recover without false checklist progress: ${stored.slice(0, 25)}`, async ({ page, context }) => {
    await context.addInitScript(stored => {
      sessionStorage.setItem('sts:splash', 'seen');
      localStorage.setItem('sts_checklist_progress', stored);
      localStorage.setItem('sts:consent', 'not json');
      localStorage.setItem('sts_audience', 'unknown');
      localStorage.setItem('sts:reading-position:v1', 'null');
      localStorage.setItem('sts_book_last_read', '<script>alert(1)</script>');
    }, stored);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('/checklist', { waitUntil: 'networkidle' });
    await expect(page.locator('#check-01')).not.toBeChecked();
    await page.locator('#check-title-01').click();
    await expect(page.locator('#check-01')).toBeChecked();
    await page.reload({ waitUntil: 'networkidle' });
    // The init fixture runs on every document; restoring malformed data stays safe.
    await expect(page.locator('#check-01')).not.toBeChecked();
    expect(errors).toEqual([]);
  });
}

test('no-JavaScript visitors can read the sample and get a checkout explanation', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  await isolate(context, baseURL);
  const page = await context.newPage();
  try {
    await page.goto(baseURL + '/sample');
    await expect(page.getByRole('heading', { name: 'Start with the book.', exact: true })).toBeVisible();
    await expect(page.locator('#how-to-use')).toContainText('How to Use This Book');
    await page.goto(baseURL + '/early-access');
    const fallback = page.locator('noscript p').filter({ hasText: 'Checkout needs JavaScript' });
    await expect(fallback).toBeVisible();
    await expect(fallback.getByRole('link', { name: 'read the free sample', exact: true })).toHaveAttribute('href', '/sample');
    await expect(fallback.getByRole('link', { name: 'contact us for help with your purchase', exact: true })).toHaveAttribute('href', /^mailto:/);
  } finally { await context.close(); }
});

test('a checkout timeout restores controls and directs ambiguous retries to the same email', async ({ page, context }) => {
  await context.addInitScript(() => sessionStorage.setItem('sts:splash', 'seen'));
  await page.clock.install();
  let attempts = 0;
  await page.route('**/api/stripe-checkout', route => {
    attempts++;
    if (attempts === 1) return new Promise(() => {});
    return route.fulfill({ status: 503, json: { error: 'Checkout is temporarily unavailable.' } });
  });
  await page.goto('/early-access', { waitUntil: 'networkidle' });
  await page.locator('#ea-email').fill('reader@example.test');
  const buy = page.locator('button.ea-buy-btn');
  await buy.click();
  await expect(buy).toBeDisabled();
  await expect.poll(() => attempts).toBe(1);
  await page.clock.fastForward(30_100);
  await expect(page.getByRole('alert')).toContainText('could not confirm its status');
  await expect(page.getByRole('alert')).toContainText('same email address');
  await expect(buy).toBeEnabled();
  await expect(page.locator('#ea-email')).toHaveValue('reader@example.test');
  await buy.click();
  await expect(page.getByRole('alert')).toContainText('temporarily unavailable');
  await expect(buy).toBeEnabled();
  expect(attempts).toBe(2);
});

test('network failures and malformed gateway responses leave a recoverable checkout', async ({ page, context }) => {
  await context.addInitScript(() => sessionStorage.setItem('sts:splash', 'seen'));
  let attempts = 0;
  await page.route('**/api/stripe-checkout', route => {
    attempts++;
    if (attempts === 1) return route.abort('failed');
    return route.fulfill({ status: 502, contentType: 'text/html', body: '<h1>Bad gateway</h1>' });
  });
  await page.goto('/early-access', { waitUntil: 'networkidle' });
  await page.locator('#ea-email').fill('reader@example.test');
  const buy = page.locator('button.ea-buy-btn');
  await buy.click();
  await expect(page.getByRole('alert')).toContainText('Connection interrupted');
  await expect(buy).toBeEnabled();
  await buy.click();
  await expect(page.getByRole('alert')).toContainText('Could not start checkout');
  await expect(buy).toBeEnabled();
  await expect(page.locator('#ea-email')).toHaveValue('reader@example.test');
});

test('320px pages reflow with doubled root text and reduced motion', async ({ page, context }) => {
  await context.addInitScript(() => sessionStorage.setItem('sts:splash', 'seen'));
  await page.setViewportSize({ width: 320, height: 740 });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  for (const path of ['/', '/sample', '/early-access', '/checklist', '/book']) {
    await page.goto(path, { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: 'html { font-size: 200% !important; }' });
    const overflow = await page.locator('main').evaluate(main => [...main.querySelectorAll('*')].filter(node => {
      if (node.children.length || node.closest('[aria-hidden="true"]')) return false;
      const box = node.getBoundingClientRect();
      const style = getComputedStyle(node);
      if (!box.width || !box.height || style.visibility === 'hidden' || style.display === 'none') return false;
      // A horizontally scrollable data table remains an intentional two-axis
      // surface. It must fit the page; its cells may extend inside that scroller.
      for (let parent = node.parentElement; parent && parent !== main; parent = parent.parentElement) {
        const css = getComputedStyle(parent);
        const rect = parent.getBoundingClientRect();
        if (['auto', 'scroll'].includes(css.overflowX) && rect.right <= innerWidth + 2 && rect.left >= -2) return false;
      }
      return box.right > innerWidth + 2 || box.left < -2;
    }).map(node => ({ tag: node.tagName, text: node.textContent?.slice(0, 60) })));
    expect(overflow, path).toEqual([]);
    await expect.poll(() => page.evaluate(() => document.getAnimations().filter(animation => animation.playState === 'running').length)).toBe(0);
  }
});

test('a tagged social link survives sample navigation, back, forward and reload', async ({ page, context }) => {
  await context.addInitScript(() => sessionStorage.setItem('sts:splash', 'seen'));
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/sample?utm_source=instagram&utm_medium=social&utm_campaign=book-launch#how-to-use', { waitUntil: 'networkidle' });
  await expect(page.locator('#how-to-use')).toContainText('How to Use This Book');
  await page.getByRole('link', { name: /See the \$5 book offer/ }).click();
  await expect(page).toHaveURL(/\/early-access$/);
  await page.goBack({ waitUntil: 'networkidle' });
  await expect(page).toHaveURL(/utm_campaign=book-launch#how-to-use$/);
  await expect(page.locator('#how-to-use')).toContainText('How to Use This Book');
  await page.goForward({ waitUntil: 'networkidle' });
  await expect(page).toHaveURL(/\/early-access$/);
  await page.reload({ waitUntil: 'networkidle' });
  await expect(page.locator('#ea-email')).toBeVisible();
  await expect(page.locator('button.ea-buy-btn')).toBeDisabled();
  expect(errors).toEqual([]);
});

test('a superseded hash-focus callback cannot rewrite the next history entry', async ({ page, context }) => {
  await context.addInitScript(() => {
    sessionStorage.setItem('sts:splash', 'seen');
    const nativeTimeout = window.setTimeout.bind(window);
    window.__deferredHashFocus = [];
    window.setTimeout = (callback, delay, ...args) => {
      // Hold only Kit's deferred fragment-focus workaround, not the app's
      // timers. Releasing it after forward navigation deterministically
      // reproduces the real WebKit race observed in the full launch suite.
      if (typeof callback === 'function' && callback.toString().includes('location.replace(')
          && callback.toString().includes('history.replaceState(')) {
        window.__deferredHashFocus.push(() => callback(...args));
        return nativeTimeout(() => {}, 0);
      }
      return nativeTimeout(callback, delay, ...args);
    };
  });
  await page.goto('/sample?utm_source=instagram#how-to-use', { waitUntil: 'networkidle' });
  await page.getByRole('link', { name: /See the \$5 book offer/ }).click();
  await expect(page.locator('#ea-email')).toBeVisible();
  await page.goBack({ waitUntil: 'networkidle' });
  await expect(page.locator('#how-to-use')).toContainText('How to Use This Book');
  await expect.poll(() => page.evaluate(() => window.__deferredHashFocus.length)).toBe(1);
  await page.goForward({ waitUntil: 'networkidle' });
  await expect(page).toHaveURL(/\/early-access$/);
  await expect(page.locator('#ea-email')).toBeVisible();
  await page.evaluate(() => window.__deferredHashFocus.splice(0).forEach(release => release()));
  await expect(page).toHaveURL(/\/early-access$/);
  await expect(page.locator('#ea-email')).toBeVisible();
  await page.reload({ waitUntil: 'networkidle' });
  await expect(page).toHaveURL(/\/early-access$/);
  await expect(page.locator('#ea-email')).toBeVisible();
});
