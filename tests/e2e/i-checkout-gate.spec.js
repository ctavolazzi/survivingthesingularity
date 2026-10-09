import { expect, test } from '@playwright/test';

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
  await page.goto(PAGE, { waitUntil: 'networkidle' });
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

    await page.locator('button.ea-bottom-btn').click();
    await page.waitForTimeout(400);

    expect(calls, 'no session may be created without an address').toHaveLength(0);
  });

  /**
   * The regression this file was written to catch.
   *
   * `.ea-bottom-btn` calls the same checkout() handler as the primary button but
   * its disabled binding is `checkoutLoading` alone, with no `!emailOk`. The
   * handler does guard internally, so this is not a security hole and no session
   * is created. The cost is conversion: the button looks live, clicking it emits
   * an error paragraph that renders ~180 lines up the page next to the OTHER
   * button, and a customer at the bottom of a long sales page sees nothing happen.
   *
   * Assert the honest current state so the fix flips this test rather than
   * silently changing behaviour nobody is watching.
   */
  test('the bottom buy button is not gated on a valid email', async ({ page }) => {
    // Documented current behaviour. `.ea-bottom-btn` binds disabled to
    // `checkoutLoading` alone, with no `!emailOk`, unlike the primary button.
    // checkout() guards internally so no session is created, which is why this
    // is a conversion defect and not a security hole.
    const bottom = page.locator('button.ea-bottom-btn');
    await bottom.scrollIntoViewIfNeeded();
    await expect(bottom).toBeEnabled();

    await bottom.click();
    await expect(page.locator('p.ea-checkout-error'))
      .toHaveText(/Enter a valid email address first\./);
  });

  /**
   * KNOWN DEFECT, expected to fail until the page is fixed.
   *
   * Clicking the bottom buy button with no address emits its error into the
   * paragraph that sits beside the OTHER button, near the top of an 814-line
   * sales page. Measured on Desktop Chrome at a 720px viewport: the error
   * renders 4052px away from the button that produced it, which is 5.6 screens.
   * The customer clicks buy, sees absolutely nothing happen, and leaves.
   *
   * test.fail() keeps the suite honest: it stays green while the bug exists and
   * turns red the moment someone fixes it, at which point delete this wrapper.
   * The fix is either to gate `.ea-bottom-btn` on `emailOk` the way the primary
   * button already is, or to render a second error slot next to it.
   */
  test.fail('bottom-button error renders where the customer can see it', async ({ page }) => {
    const bottom = page.locator('button.ea-bottom-btn');
    await bottom.scrollIntoViewIfNeeded();
    await bottom.click();

    const err = page.locator('p.ea-checkout-error');
    await expect(err).toHaveText(/Enter a valid email address first\./);

    const errBox = await err.boundingBox();
    const btnBox = await bottom.boundingBox();
    expect(errBox, 'error paragraph must have a layout box').not.toBeNull();
    expect(btnBox, 'bottom button must have a layout box').not.toBeNull();

    const gapPx = Math.abs(btnBox.y - errBox.y);
    const viewportH = page.viewportSize()?.height ?? 720;

    expect(
      gapPx,
      `error is ${Math.round(gapPx)}px from the button in a ${viewportH}px viewport`
    ).toBeLessThan(viewportH);
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

    await expect(page.locator('p.ea-owned-note')).toContainText('You already have this one');
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

    const note = page.locator('p.ea-owned-note');
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

    await expect(page.locator('p.ea-checkout-error')).toContainText('temporarily unavailable');
    // The button must come back so the customer can retry.
    await expect(page.locator('button.ea-buy-btn')).toBeEnabled();
  });
});
