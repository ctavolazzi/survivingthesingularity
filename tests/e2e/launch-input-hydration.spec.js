import { expect, test } from '@playwright/test';
import { CONSENT_KEY, CONSENT_VERSION } from '../../src/lib/consent.js';
import { BOOK_ACCESS_PASSWORD } from '../../src/lib/bookAccessCode.js';

test.beforeEach(async ({ page, baseURL }) => {
  const origin = new URL(baseURL).origin;
  if (!['localhost', '127.0.0.1', '[::1]'].includes(new URL(origin).hostname)) {
    throw new Error('Hydration tests require a credential-free local server.');
  }
  await page.addInitScript(({ key, version }) => {
    sessionStorage.setItem('sts:splash', 'seen');
    localStorage.setItem(key, JSON.stringify({ version, at: '2026-10-13T00:00:00Z' }));
  }, { key: CONSENT_KEY, version: CONSENT_VERSION });
  await page.route('**/*', route => {
    const request = route.request();
    if (new URL(request.url()).origin !== origin || !['GET', 'HEAD'].includes(request.method())) return route.abort();
    return route.continue();
  });
});

async function holdScripts(page, baseURL) {
  let release;
  let count = 0;
  const ready = new Promise(resolve => { release = resolve; });
  await page.route('**/*', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (url.origin === new URL(baseURL).origin && request.resourceType() === 'script' && url.pathname !== '/splash-gate.js') {
      count++;
      await ready;
    }
    return route.fallback();
  });
  return { release, count: () => count };
}

for (const path of ['/book', '/read']) {
  test(`${path} preserves a password entered before hydration and reads later autofill on submit`, async ({ page, baseURL }) => {
    const scripts = await holdScripts(page, baseURL);
    try {
      await page.goto(path, { waitUntil: 'commit' });
      const input = page.getByLabel('Book access password', { exact: true });
      const unlock = page.getByRole('button', { name: 'Unlock', exact: true });
      await input.fill('incorrect-before-scripts');
      await expect(input).toHaveValue('incorrect-before-scripts');
      await expect(unlock).toBeDisabled();
      expect(scripts.count()).toBeGreaterThan(0);
      scripts.release();
      await expect(unlock).toBeEnabled();
      await expect(input).toHaveValue('incorrect-before-scripts');
      await unlock.click();
      await expect(page.getByRole('alert')).toHaveText('Incorrect password.');
      await expect(input).toHaveValue('incorrect-before-scripts');
      await input.evaluate(element => { element.value = ''; element.dispatchEvent(new Event('change', { bubbles: true })); });
      await expect(unlock).toBeDisabled();
      await input.evaluate(element => { element.value = 'changed'; element.dispatchEvent(new Event('change', { bubbles: true })); });
      await expect(unlock).toBeEnabled();
      await input.evaluate((element, password) => { element.value = password; }, BOOK_ACCESS_PASSWORD);
      await input.press('Enter');
      await expect(input).toHaveCount(0);
      await expect(page.locator(path === '/book' ? '.book-page' : '.reader')).toBeVisible();
    } finally { scripts.release(); }
  });
}

for (const consent of [false, true]) {
  test(`checklist preserves pre-hydration email, honeypot and explicit consent=${consent}`, async ({ page, baseURL }) => {
    const scripts = await holdScripts(page, baseURL);
    const submitted = [];
    await page.route('**/api/waitlist', route => {
      submitted.push(route.request().postDataJSON());
      return route.fulfill({ status: 503, json: { error: 'Signup is temporarily unavailable.' } });
    });
    try {
      await page.goto('/checklist', { waitUntil: 'commit' });
      const unlock = page.getByRole('button', { name: 'Unlock Free', exact: true });
      const form = page.locator('form').filter({ has: unlock });
      const email = form.getByRole('textbox', { name: 'Email address', exact: true });
      const checkbox = page.getByRole('checkbox', { name: 'Also send me Signal Dispatches and book release news (optional)', exact: true });
      await expect(checkbox).not.toBeChecked();
      await email.fill('before-scripts@example.test');
      await checkbox.setChecked(consent);
      await form.locator('input.hp-field').evaluate(element => { element.value = 'preserve-antibot-field'; });
      await expect(unlock).toBeDisabled();
      expect(scripts.count()).toBeGreaterThan(0);
      scripts.release();
      await expect(unlock).toBeEnabled();
      await expect(email).toHaveValue('before-scripts@example.test');
      await expect(checkbox).toBeChecked({ checked: consent });
      await unlock.click();
      await expect(page.getByRole('alert')).toHaveText('Signup is temporarily unavailable.');
      expect(submitted[0]).toMatchObject({ email: 'before-scripts@example.test', newsletter_consent: consent, book_release_consent: consent, _hp: 'preserve-antibot-field' });
      await expect(email).toHaveValue('before-scripts@example.test');
      // Both ordinary change events and an autofill that emits no event are
      // read correctly, without turning optional updates on implicitly.
      await email.evaluate(element => { element.value = ''; element.dispatchEvent(new Event('change', { bubbles: true })); });
      await expect(unlock).toBeDisabled();
      await email.evaluate(element => { element.value = 'changed@example.test'; element.dispatchEvent(new Event('change', { bubbles: true })); });
      await expect(unlock).toBeEnabled();
      await checkbox.setChecked(!consent);
      await email.evaluate(element => { element.value = 'autofilled@example.test'; });
      await form.locator('input.hp-field').evaluate(element => { element.value = ''; });
      await email.press('Enter');
      await expect.poll(() => submitted.length).toBe(2);
      expect(submitted[1]).toMatchObject({ email: 'autofilled@example.test', newsletter_consent: !consent, book_release_consent: !consent, _hp: '' });
      await expect(unlock).toBeEnabled();
      await checkbox.evaluate((element, checked) => { element.checked = checked; }, consent);
      await email.press('Enter');
      await expect.poll(() => submitted.length).toBe(3);
      expect(submitted[2]).toMatchObject({ newsletter_consent: consent, book_release_consent: consent });
    } finally { scripts.release(); }
  });
}

test('restoring the checklist unlock does not submit signup or resend notes', async ({ page }) => {
  const writes = [];
  await page.route('**/api/**', route => {
    if (!['GET', 'HEAD'].includes(route.request().method())) writes.push(route.request().url());
    return route.abort();
  });
  await page.addInitScript(() => {
    localStorage.setItem('sts_unlock_checklist', '1');
    localStorage.setItem('sts_unlock_checklist_email', 'returning@example.test');
  });
  await page.goto('/checklist', { waitUntil: 'networkidle' });
  await expect(page.locator('input.cl-check-native')).toHaveCount(7);
  await expect(page.getByRole('button', { name: 'Unlock Free', exact: true })).toHaveCount(0);
  expect(writes).toEqual([]);
});
