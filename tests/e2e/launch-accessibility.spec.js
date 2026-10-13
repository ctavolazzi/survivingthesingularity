import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { CONSENT_KEY, CONSENT_VERSION } from '../../src/lib/consent.js';
import { BOOK_ACCESS_PASSWORD } from '../../src/lib/bookAccessCode.js';

// All writes are intercepted locally. This suite never buys, subscribes, or
// sends email, and blocks third-party resources rather than depending on them.
test.beforeEach(async ({ page, baseURL }) => {
  if (!baseURL || !['localhost', '127.0.0.1', '[::1]'].includes(new URL(baseURL).hostname)) {
    throw new Error('Launch accessibility tests require a local server without service credentials.');
  }
  const origin = new URL(baseURL).origin;
  await page.addInitScript(() => sessionStorage.setItem('sts:splash', 'seen'));
  await page.route('**/*', (route) => {
    const request = route.request();
    if (new URL(request.url()).origin !== origin || !['GET', 'HEAD'].includes(request.method())) {
      return route.abort();
    }
    return route.continue();
  });
});

async function acceptNotice(page) {
  await page.addInitScript(({ key, version }) => {
    localStorage.setItem(key, JSON.stringify({ version, at: '2026-10-12T00:00:00Z' }));
  }, { key: CONSENT_KEY, version: CONSENT_VERSION });
}

test('menu receives focus, contains both tab directions, and restores its trigger', async ({ page }) => {
  await acceptNotice(page);
  await page.goto('/about', { waitUntil: 'networkidle' });
  const trigger = page.getByRole('button', { name: 'Open menu', exact: true });
  await trigger.focus();
  await page.keyboard.press('Enter');
  const dialog = page.getByRole('dialog', { name: 'Site menu' });
  await expect(dialog.getByRole('button', { name: 'Close menu' })).toBeFocused();
  await expect(page.locator('#main-content')).toHaveJSProperty('inert', true);
  await page.keyboard.press('Control+k');
  await expect(page.getByRole('dialog', { name: 'Command palette' })).toHaveCount(0);
  for (let i = 0; i < 14; i++) {
    await page.keyboard.press('Shift+Tab');
    await expect.poll(() => dialog.evaluate(el => el.contains(document.activeElement))).toBe(true);
  }
  for (let i = 0; i < 14; i++) {
    await page.keyboard.press('Tab');
    await expect.poll(() => dialog.evaluate(el => el.contains(document.activeElement))).toBe(true);
  }
  await page.keyboard.press('Escape');
  await expect(trigger).toBeFocused();
  await expect(page.locator('#main-content')).toHaveJSProperty('inert', false);
  // Reopening before the first tick completes must not leave two traps alive.
  await trigger.evaluate(button => {
    button.click();
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
    button.click();
  });
  await expect(dialog.getByRole('button', { name: 'Close menu' })).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(trigger).toBeFocused();
  await expect(page.locator('#main-content')).toHaveJSProperty('inert', false);
});

test('nested focus containment resumes the previous modal and preserves closed surfaces', async ({ page }) => {
  await acceptNotice(page);
  await page.route('**/__test__/modal-focus.js', route => route.fulfill({
    contentType: 'text/javascript',
    body: readFileSync(new URL('../../src/lib/modalFocus.js', import.meta.url), 'utf8')
  }));
  await page.goto('/about', { waitUntil: 'networkidle' });
  const result = await page.evaluate(async () => {
    const { containModalFocus } = await import('/__test__/modal-focus.js');
    const host = document.createElement('div');
    host.innerHTML = '<div id="fixture-a" tabindex="-1"><button id="fixture-first">First</button></div><div id="fixture-b" tabindex="-1"><button id="fixture-second">Second</button></div><div id="fixture-protected" inert><button>Unavailable</button></div>';
    document.body.append(host);
    const first = host.querySelector('#fixture-a');
    const second = host.querySelector('#fixture-b');
    const protectedNode = host.querySelector('#fixture-protected');
    const releaseFirst = containModalFocus(first);
    const releaseSecond = containModalFocus(second);
    const secondFocused = document.activeElement.id === 'fixture-second';
    releaseSecond();
    const resumedFirst = document.activeElement.id === 'fixture-first';
    const secondClosed = second.inert;
    releaseFirst();
    const originalProtected = protectedNode.inert;
    const releaseFirstAgain = containModalFocus(first);
    const releaseSecondAgain = containModalFocus(second);
    releaseFirstAgain();
    releaseSecondAgain();
    const closedOutOfOrder = first.inert && second.inert;
    host.remove();
    return { secondFocused, resumedFirst, secondClosed, originalProtected, closedOutOfOrder };
  });
  expect(result).toEqual({ secondFocused: true, resumedFirst: true, secondClosed: true, originalProtected: true, closedOutOfOrder: true });
  await expect(page.locator('#main-content')).toHaveJSProperty('inert', false);
});

test('decline dialog contains focus and returns to terms without reloading', async ({ page }) => {
  await page.goto('/about', { waitUntil: 'networkidle' });
  const decline = page.getByRole('button', { name: 'I do not agree to the terms' });
  await decline.click();
  const dialog = page.getByRole('alertdialog', { name: 'Review the terms' });
  const review = dialog.getByRole('button', { name: 'Return to terms' });
  await expect(review).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(review).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(review).toBeFocused();
  await expect(page.locator('#main-content')).toHaveJSProperty('inert', true);
  await page.keyboard.press('Escape');
  await expect(decline).toBeFocused();
  await expect(page.locator('#main-content')).toHaveJSProperty('inert', false);
});

test('information dialog traps focus and restores its opener', async ({ page }) => {
  await acceptNotice(page);
  await page.goto('/about', { waitUntil: 'networkidle' });
  const opener = page.getByRole('button', { name: /Thank you for being here/ });
  await opener.click();
  const dialog = page.getByRole('dialog', { name: 'Thank You', exact: true });
  const close = dialog.getByRole('button', { name: 'Close dialog', exact: true });
  await expect(close).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(close).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(close).toBeFocused();
  await expect(page.locator('#main-content')).toHaveJSProperty('inert', true);
  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  await expect(opener).toBeFocused();
  await expect(page.locator('#main-content')).toHaveJSProperty('inert', false);
});

test('public sample renders both excerpts and the guide works without an access form', async ({ page }) => {
  await acceptNotice(page);
  await page.goto('/sample', { waitUntil: 'networkidle' });
  await expect(page.getByRole('heading', { name: 'Start with the book.', exact: true })).toBeVisible();
  await expect(page.locator('#introduction')).toContainText(/introduction/i);
  await expect(page.getByLabel('Book access password', { exact: true })).toHaveCount(0);
  const guide = page.getByRole('navigation', { name: 'Sample sections' }).getByRole('link', { name: 'How to Use This Book', exact: true });
  await guide.click();
  await expect(page).toHaveURL(/\/sample#how-to-use$/);
  await expect(page.locator('#how-to-use')).toContainText('How to Use This Book');
  await expect(page.getByRole('link', { name: /See the \$5 book offer/ })).toHaveAttribute('href', '/early-access');
});

test('all checklist steps are named and clickable; unlocking does not opt into marketing', async ({ page }) => {
  await acceptNotice(page);
  let signup;
  await page.route('**/api/waitlist', (route) => {
    signup = route.request().postDataJSON();
    return route.fulfill({ status: 201, json: { ok: true } });
  });
  await page.route('**/api/checklist-email', (route) => route.fulfill({ status: 503, json: { error: 'Email is temporarily unavailable.' } }));
  await page.goto('/checklist', { waitUntil: 'networkidle' });
  const marketing = page.getByRole('checkbox', { name: /Also send me Signal Dispatches/ });
  await expect(marketing).not.toBeChecked();
  await page.locator('#check-title-01').click();
  await expect(page.getByRole('checkbox', { name: 'Understand what is actually happening', exact: true })).toBeChecked();
  const unlockForm = page.locator('form').filter({ has: page.getByRole('button', { name: 'Unlock Free', exact: true }) });
  await unlockForm.getByRole('textbox', { name: 'Email address', exact: true }).fill('reader@example.test');
  await page.getByRole('button', { name: 'Unlock Free', exact: true }).click();
  await expect(page.locator('input.cl-check-native')).toHaveCount(7);
  expect(signup.newsletter_consent).toBe(false);
  expect(signup.book_release_consent).toBe(false);
  for (const checkbox of await page.locator('input.cl-check-native').all()) {
    await expect(checkbox).toHaveAccessibleName(/\S/);
  }
  await page.locator('#check-title-07').click();
  await expect(page.locator('#check-07')).toBeChecked();
  await page.locator('#check-07').focus();
  await page.keyboard.press('Space');
  await expect(page.locator('#check-07')).not.toBeChecked();
  await expect(page.getByRole('alert')).toContainText('Email is temporarily unavailable');
  await expect(page.getByRole('heading', { name: /on their way/ })).toHaveCount(0);
});

test('checkout errors expose alert semantics, preserve the address, and allow retry', async ({ page }) => {
  await acceptNotice(page);
  await page.route('**/api/stripe-checkout', (route) => route.fulfill({ status: 503, json: { error: 'Checkout is temporarily unavailable.' } }));
  await page.goto('/early-access', { waitUntil: 'networkidle' });
  const buy = page.locator('button.ea-buy-btn');
  await expect(buy).toBeDisabled();
  await page.locator('#ea-email').fill('reader@example.test');
  await buy.click();
  await expect(page.getByRole('alert')).toContainText('Checkout is temporarily unavailable');
  await expect(page.locator('#ea-email')).toHaveValue('reader@example.test');
  await expect(buy).toBeEnabled();
});

test('book gate has a persistent label, a public sample, and recoverable invalid input', async ({ page }) => {
  await acceptNotice(page);
  await page.goto('/book', { waitUntil: 'networkidle' });
  const password = page.getByLabel('Book access password', { exact: true });
  await expect(password).toBeVisible();
  await expect(page.getByRole('link', { name: 'Read the free sample & reading guide', exact: true })).toHaveAttribute('href', '/sample');
  await password.fill('incorrect');
  await page.getByRole('button', { name: 'Unlock', exact: true }).click();
  await expect(page.getByRole('alert')).toHaveText('Incorrect password.');
  await expect(password).toHaveAttribute('aria-invalid', 'true');
  await expect(password).toHaveValue('incorrect');
});

test('unlocked readers can open the continuous book, resize text, and jump to a chapter', async ({ page }) => {
  await acceptNotice(page);
  await page.goto('/book', { waitUntil: 'networkidle' });
  await page.getByLabel('Book access password', { exact: true }).fill(BOOK_ACCESS_PASSWORD);
  await page.getByRole('button', { name: 'Unlock', exact: true }).click();
  await page.getByRole('link', { name: /Read it straight through/ }).click();
  await expect(page).toHaveURL(/\/read$/);
  await expect(page.getByRole('progressbar', { name: 'Reading progress' })).toBeVisible();
  await expect(page.locator('.reader')).toHaveAttribute('data-size', 'medium');
  await page.getByRole('button', { name: 'Larger text', exact: true }).click();
  await expect(page.locator('.reader')).toHaveAttribute('data-size', 'large');
  await page.getByRole('button', { name: 'Chapters', exact: true }).click();
  const chapters = page.getByRole('dialog', { name: 'Chapters', exact: true });
  await expect(chapters.getByRole('button', { name: 'Close chapter list' })).toBeFocused();
  await chapters.getByRole('button', { name: /Chapter 1: The Event Horizon/ }).click();
  await expect(page.locator('#s-chapter1').locator('h1, h2').first()).toBeFocused();
  await expect(chapters).not.toBeVisible();
});
