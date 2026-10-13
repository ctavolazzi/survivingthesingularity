import { expect, test, gotoReady } from './helpers/isolated-page.js';

/**
 * The checkout email gate shipped in commit 332fdfd.
 *
 * WHY THIS FILE EXISTS
 *
 * 332fdfd moved email collection off Stripe's hosted page and onto /early-access,
 * so the server can refuse a repeat purchase BEFORE a card is charged rather than
 * deduplicating a payment it has already taken. That gate is client-side markup,
 * which means curl cannot see it and a source grep cannot prove it still works.
 *
 * The previous round verified it with a throwaway script against a single browser
 * and then deleted the script, so it proved nothing the next day. This is the
 * committed replacement. It runs on all six device projects because the realistic
 * place for an input-gating regression to appear first is mobile Safari or the
 * tablet viewport, and no prior check touched either.
 *
 * These assertions deliberately need NO credentials. They exercise the gate, not
 * Stripe, so they are safe to run against a dev server with no .env and they
 * never create a checkout session or send mail.
 */

const PAGE = '/early-access';

/**
 * Load the page and wait until Svelte has actually hydrated.
 *
 * This is load-bearing, not politeness. The gate is driven by `bind:value` on
 * the email input, which needs a real `input` listener attached. Playwright's
 * fill() sets the DOM value and dispatches one input event; if it lands before
 * hydration, that single event is missed and `email` never updates, so the
 * button stays disabled forever and the test fails for a reason that has
 * nothing to do with the code under test. Writing this suite without the wait
 * produced exactly that false failure on 4 of 6 device projects.
 */
async function gotoHydrated(page) {
  await gotoReady(page, PAGE);
  const input = page.locator('#ea-email');
  const buy = page.locator('button.ea-buy-btn');
  await expect(input).toBeVisible();
  // Prove the binding is live before any test touches it.
  await expect(async () => {
    await input.fill('hydration@probe.test');
    await expect(buy).toBeEnabled({ timeout: 1000 });
  }).toPass({ timeout: 20_000 });
  await input.fill('');
  await expect(buy).toBeDisabled();
}

test.describe('early-access checkout email gate', () => {
  test.beforeEach(async ({ page }) => {
    await gotoHydrated(page);
  });

  test('the email field is present and precedes the primary buy button', async ({ page }) => {
    const input = page.locator('#ea-email');
    await expect(input).toBeVisible();
    await expect(input).toHaveAttribute('type', 'email');
    await expect(input).toHaveAttribute('autocomplete', 'email');
  });

  test('the primary buy button is disabled until a valid address is typed', async ({ page }) => {
    const input = page.locator('#ea-email');
    const buy = page.locator('button.ea-buy-btn');

    await expect(buy).toBeDisabled();

    await input.fill('not-an-email');
    await expect(buy).toBeDisabled();

    await input.fill('someone@');
    await expect(buy).toBeDisabled();

    await input.fill('someone@example.com');
    await expect(buy).toBeEnabled();

    // Clearing it must close the gate again, not leave the button hot.
    await input.fill('');
    await expect(buy).toBeDisabled();
  });

  test('an empty checkout attempt never reaches the network', async ({ page }) => {
    const calls = [];
    await page.route('**/api/stripe-checkout', (route) => {
      calls.push(route.request().url());
      route.abort();
    });

    const bottom = page.locator('button.ea-bottom-btn');
    await expect(bottom).toBeDisabled();
    await bottom.scrollIntoViewIfNeeded();
    const box = await bottom.boundingBox();
    expect(box).not.toBeNull();
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
    await page.waitForTimeout(400);

    expect(calls, 'no session may be created without an address').toHaveLength(0);
  });

  test('the bottom buy button uses the same valid-email gate as the primary button', async ({ page }) => {
    const input = page.locator('#ea-email');
    const bottom = page.locator('button.ea-bottom-btn');
    await expect(bottom).toBeDisabled();
    await input.fill('not-an-email');
    await expect(bottom).toBeDisabled();
    await input.fill('reader@example.invalid');
    await expect(bottom).toBeEnabled();
    await input.fill('');
    await expect(bottom).toBeDisabled();
  });

  // The old expected-failure asserted an invalid-email error several screens
  // away. Both buttons now reject invalid email before submission, and a real
  // checkout failure must be visible beside whichever button was used.
  test('bottom-button checkout errors render where the customer can see them', async ({ page }) => {
    await page.route('**/api/stripe-checkout', route => route.fulfill({
      status: 503,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'Checkout is temporarily unavailable. Please try again shortly.' }),
    }));
    await page.locator('#ea-email').fill('reader@example.invalid');
    const bottom = page.locator('button.ea-bottom-btn');
    await bottom.scrollIntoViewIfNeeded();
    await bottom.click();

    const err = page.locator('p.ea-checkout-error.ea-bottom-error');
    await expect(err).toContainText('temporarily unavailable');
    await expect(bottom).toBeEnabled();
    const errBox = await err.boundingBox();
    const btnBox = await bottom.boundingBox();
    expect(errBox, 'error paragraph must have a layout box').not.toBeNull();
    expect(btnBox, 'bottom button must have a layout box').not.toBeNull();

    const gapPx = Math.abs(btnBox.y - errBox.y);
    const viewportH = page.viewportSize()?.height ?? 720;
    expect(gapPx, `error must be near its button in a ${viewportH}px viewport`).toBeLessThan(viewportH);
  });

  test('a valid address in the field enables the primary path end to end', async ({ page }) => {
    let posted = null;
    await page.route('**/api/stripe-checkout', async (route) => {
      posted = route.request().postDataJSON();
      // Answer as the server would for a brand-new address, without touching Stripe.
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ url: 'about:blank#stubbed-checkout' }),
      });
    });

    await page.locator('#ea-email').fill('ctavolazzi+pwgate@gmail.com');
    await page.locator('button.ea-buy-btn').click();
    await page.waitForTimeout(600);

    expect(posted, 'the gate must forward a body').not.toBeNull();
    expect(posted.email, 'the typed address must reach the server, lowercased and trimmed')
      .toBe('ctavolazzi+pwgate@gmail.com');
    expect(posted.edition_type).toBe('standard');
  });

  test('the already-owned refusal reads as good news, not an error', async ({ page }) => {
    await page.route('**/api/stripe-checkout', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ already_owned: true, resent: true, reason: 'sent' }),
      });
    });

    await page.locator('#ea-email').fill('ctavolazzi+pwowned@gmail.com');
    await page.locator('button.ea-buy-btn').click();

    await expect(page.locator('p.ea-owned-note:not(.ea-bottom-error)')).toContainText('You already have this one');
    // It must NOT be presented in the error slot.
    await expect(page.locator('p.ea-checkout-error')).toHaveCount(0);
  });

  test('a cooldown refusal does not promise an email that was not sent', async ({ page }) => {
    await page.route('**/api/stripe-checkout', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ already_owned: true, resent: false, reason: 'cooldown' }),
      });
    });

    await page.locator('#ea-email').fill('ctavolazzi+pwcool@gmail.com');
    await page.locator('button.ea-buy-btn').click();

    const note = page.locator('p.ea-owned-note:not(.ea-bottom-error)');
    await expect(note).toContainText('very recently');
    await expect(note).not.toContainText('We have re-sent');
  });

  test('a 503 fail-closed answer surfaces as an error, not a silent no-op', async ({ page }) => {
    await page.route('**/api/stripe-checkout', async (route) => {
      await route.fulfill({
        status: 503,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Checkout is temporarily unavailable. Please try again shortly.' }),
      });
    });

    await page.locator('#ea-email').fill('ctavolazzi+pw503@gmail.com');
    await page.locator('button.ea-buy-btn').click();

    await expect(page.locator('p.ea-checkout-error:not(.ea-bottom-error)')).toContainText('temporarily unavailable');
    // The button must come back so the customer can retry.
    await expect(page.locator('button.ea-buy-btn')).toBeEnabled();
  });
});
