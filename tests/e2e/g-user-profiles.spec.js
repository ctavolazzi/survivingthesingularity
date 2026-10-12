// @ts-check
import { test, expect, gotoReady, reloadReady } from './helpers/isolated-page.js';

/* Accounts were removed by CT's ruling on 2026-08-04. See the header of
   src/hooks.server.js. Purchase identity is the email used at checkout;
   checklist progress is local to the browser. Keep the historical filename
   while checking that contract, rather than restoring a removed sign-in page.
   External requests are blocked and API calls are intercepted by the shared
   fixture, including automatic checklist email. */
const READER_EMAIL = 'reader@example.test';
const ACCOUNT_CONTROLS = 'input[type="password"], a[href^="/signup"], a[href^="/login"], a[href^="/profile"], a[href^="/auth/"]';

test.describe('Purchase email and no accounts', () => {
  for (const path of ['/signup', '/signup?mode=signin', '/profile', '/auth/callback']) {
    test(`${path} stays removed without an account form`, async ({ page }) => {
      const response = await gotoReady(page, path);
      expect(response?.status()).toBe(404);
      await expect(page.locator(ACCOUNT_CONTROLS)).toHaveCount(0);
    });
  }

  test('Preorder validates the purchase email at both buy buttons', async ({ page }) => {
    await gotoReady(page, '/early-access');
    const email = page.locator('#ea-email');
    const bottomEmail = page.locator('#ea-email-bottom');
    const buttons = page.locator('.ea-buy-btn, .ea-bottom-btn');
    await expect(email).toBeVisible();
    await expect(buttons).toHaveCount(2);
    for (const button of await buttons.all()) await expect(button).toBeDisabled();

    await email.fill('not-an-email');
    await expect(bottomEmail).toHaveValue('not-an-email');
    for (const button of await buttons.all()) await expect(button).toBeDisabled();

    await email.fill(READER_EMAIL);
    await expect(bottomEmail).toHaveValue(READER_EMAIL);
    for (const button of await buttons.all()) await expect(button).toBeEnabled();
    await expect(page.locator(ACCOUNT_CONTROLS)).toHaveCount(0);
  });

  test('An existing buyer recovers the link by purchase email without signing in', async ({ page }) => {
    await page.route('**/api/stripe-checkout', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ already_owned: true, resent: true }),
    }));
    await gotoReady(page, '/early-access');
    await page.locator('#ea-email').fill(` ${READER_EMAIL} `);
    const request = page.waitForRequest(req =>
      req.method() === 'POST' && new URL(req.url()).pathname === '/api/stripe-checkout'
    );
    await page.locator('.ea-buy-btn').click();
    expect((await request).postDataJSON()).toEqual({ edition_type: 'standard', email: READER_EMAIL });
    await expect(page.locator('.ea-owned-note').first()).toContainText('re-sent your download link');
    await expect(page).toHaveURL(/\/early-access$/);
    await expect(page.locator(ACCOUNT_CONTROLS)).toHaveCount(0);
  });

  test('Purchase email is usable on mobile without horizontal overflow', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await gotoReady(page, '/early-access');
    const email = page.locator('#ea-email');
    await expect(email).toBeVisible();
    await email.fill(READER_EMAIL);
    await expect(email).toHaveValue(READER_EMAIL);
    await expect(page.locator('.ea-buy-btn')).toBeEnabled();
    // overflow-x:hidden can hide clipped controls from scrollWidth. Measure
    // the actual purchase controls as well as the document overflow below.
    for (const control of [email, page.locator('.ea-buy-btn')]) {
      const box = await control.boundingBox();
      expect(box).not.toBeNull();
      expect(box.x).toBeGreaterThanOrEqual(0);
      expect(box.x + box.width).toBeLessThanOrEqual(375);
    }
    expect(await page.evaluate(() =>
      document.documentElement.scrollWidth > document.documentElement.clientWidth + 5
    )).toBe(false);
  });

  test('Checklist progress and notes survive reload without an account', async ({ page }) => {
    await gotoReady(page, '/checklist');
    const checkbox = page.locator('#check-01');
    const notes = page.locator('#notes-01');
    await expect(notes).toBeVisible();
    await page.locator('label[for="check-01"]').click();
    await expect(checkbox).toBeChecked();
    await notes.fill('Compare one local food project this week.');
    await expect.poll(() => page.evaluate(() =>
      JSON.parse(localStorage.getItem('sts_checklist_progress') || '{}')['01']
    )).toEqual({ checked: true, notes: 'Compare one local food project this week.' });

    await reloadReady(page);
    await expect(checkbox).toBeChecked();
    await expect(notes).toHaveValue('Compare one local food project this week.');
    await expect(page.locator(ACCOUNT_CONTROLS)).toHaveCount(0);
  });

  test('Free checklist unlock respects email consent and persists without signing in', async ({ page }) => {
    await page.route('**/api/waitlist', route => route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({ success: true }),
    }));
    await page.route('**/api/checklist-email', route => route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ success: true }),
    }));
    await gotoReady(page, '/checklist');
    const email = page.locator('.gate-form').getByRole('textbox', { name: 'Email address', exact: true });
    await expect(email).toBeVisible();
    await expect(page.locator('.cl-list-gated')).toHaveCount(0);
    await email.fill(READER_EMAIL);
    await page.locator('.gate-consent input').uncheck();
    const request = page.waitForRequest(req =>
      req.method() === 'POST' && new URL(req.url()).pathname === '/api/waitlist'
    );
    await page.getByRole('button', { name: 'Unlock Free', exact: true }).click();
    expect((await request).postDataJSON()).toEqual({
      email: READER_EMAIL,
      source: 'checklist',
      newsletter_consent: false,
      book_release_consent: false,
      _hp: '',
    });
    await expect(page.locator('.cl-list-gated')).toBeVisible();
    await expect(page.locator('.cl-list-gated input[type="checkbox"]')).toHaveCount(4);
    await reloadReady(page);
    await expect(page.locator('.cl-list-gated')).toBeVisible();
    await expect(email).toHaveCount(0);
    await expect(page.locator(ACCOUNT_CONTROLS)).toHaveCount(0);
  });
});
