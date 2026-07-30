/**
 * The future-dated timestamp guard (plan item B-09).
 *
 * Pure logic, no server and no database, so it runs with:
 *   npx playwright test m-webhook-freshness --project=chromium
 *
 * Two things are being defended here and they pull in opposite directions, so
 * both get tested rather than just the headline one:
 *
 *   1. A timestamp past the future tolerance is REFUSED.
 *   2. Everything else is ALLOWED, because a hygiene guard that starts
 *      rejecting real webhooks is worse than the hole it closes.
 *
 * The sweep at the bottom is a mutation test. This guard fails silently in both
 * directions: a parser that always returned null would degrade open forever and
 * every "allowed" assertion above would still pass, and a comparison flipped to
 * always-reject would kill the money path while every "rejected" assertion still
 * passed. The sweep asserts the exact split, so neither mutation survives.
 */
import { test, expect } from '@playwright/test';
import {
  checkFreshness,
  parseSignatureTimestamp,
  FUTURE_TOLERANCE_SECONDS
} from '../../src/lib/server/webhookFreshness.js';

const NOW = 1_780_000_000;
const sig = (t) => `t=${t},v1=5257a869e7ecebeda32affa62cdca3fa51cad7e77a0e56ff536d0ce8e108d8bd`;

test.describe('reading the timestamp out of the header', () => {
  test('pulls t out of a real stripe-signature header', () => {
    // If this ever returns null the whole guard silently stops guarding, so it
    // is asserted against an exact value rather than just "not null".
    expect(parseSignatureTimestamp(sig(NOW))).toBe(NOW);
  });

  test('tolerates surrounding whitespace and extra schemes', () => {
    expect(parseSignatureTimestamp(` t=${NOW} , v1=abc , v0=def `)).toBe(NOW);
    expect(parseSignatureTimestamp(`v1=abc,t=${NOW}`)).toBe(NOW);
  });

  test('does not mistake another key ending in t for the timestamp', () => {
    // `st=` and `nonce_t=` both end in t and both must be ignored.
    expect(parseSignatureTimestamp('st=123,v1=abc')).toBeNull();
    expect(parseSignatureTimestamp('nonce_t=123,v1=abc')).toBeNull();
  });

  test('refuses to coerce a malformed value into a confident number', () => {
    // Every one of these is a case where Number() would have produced an
    // answer. `Number('')` is 0, which would read as January 1970 and sail
    // through the future check while being obvious nonsense.
    for (const bad of ['t=,v1=abc', 't=abc', 't=12.5', 't=1e9', 't= 12 3', 't=0x10', 't=NaN']) {
      expect(parseSignatureTimestamp(bad), bad).toBeNull();
    }
  });

  test('refuses an integer too large to be exact', () => {
    expect(parseSignatureTimestamp('t=99999999999999999999')).toBeNull();
  });

  test('returns null for anything that is not a string', () => {
    for (const bad of [undefined, null, 42, {}, []]) {
      expect(parseSignatureTimestamp(bad)).toBeNull();
    }
  });
});

test.describe('the future side is refused', () => {
  test('the reproduction case: 600s ahead is rejected', () => {
    // This is the exact condition measured at 200 on 2026-07-29 and the one
    // scripts/probe-stripe-webhook.mjs asserts over HTTP.
    const r = checkFreshness(sig(NOW + 600), NOW);
    expect(r.ok).toBe(false);
    expect(r.reason).toBe('future-dated');
    expect(r.skewSeconds).toBe(600);
    expect(r.degradesOpen).toBe(false);
  });

  test('exactly on the tolerance boundary is accepted, one second past it is not', () => {
    expect(checkFreshness(sig(NOW + FUTURE_TOLERANCE_SECONDS), NOW).ok).toBe(true);
    expect(checkFreshness(sig(NOW + FUTURE_TOLERANCE_SECONDS + 1), NOW).ok).toBe(false);
  });

  test('a wildly future timestamp, the unbounded-validity case, is rejected', () => {
    // A signature dated ten years out would otherwise never expire.
    expect(checkFreshness(sig(NOW + 315_360_000), NOW).ok).toBe(false);
  });
});

test.describe('everything else is allowed, on purpose', () => {
  test('the past is left entirely to Stripe tolerance', () => {
    // Deliberately NOT enforced here. Two expiry windows that can drift apart
    // is worse than one, and the second is the one nobody remembers exists.
    for (const back of [1, 600, 86_400, 315_360_000]) {
      const r = checkFreshness(sig(NOW - back), NOW);
      expect(r.ok, `${back}s in the past`).toBe(true);
      expect(r.reason).toBe('ok');
      expect(r.skewSeconds).toBe(-back);
    }
  });

  test('an unreadable header degrades OPEN and says so', () => {
    // Failing shut here would reject every real webhook the day Stripe changes
    // its header format. `degradesOpen` is what stops that being read as a pass.
    for (const bad of ['v1=abc', 't=abc', '', undefined, null]) {
      const r = checkFreshness(bad, NOW);
      expect(r.ok, JSON.stringify(bad)).toBe(true);
      expect(r.reason).toBe('no-timestamp');
      expect(r.degradesOpen).toBe(true);
      expect(r.skewSeconds).toBeNull();
    }
  });

  test('a broken clock on our side degrades OPEN rather than rejecting traffic', () => {
    for (const clock of [NaN, Infinity, -Infinity]) {
      const r = checkFreshness(sig(NOW + 600), clock);
      expect(r.ok, String(clock)).toBe(true);
      expect(r.degradesOpen).toBe(true);
    }
  });

  test('a valid in-window timestamp is a clean pass, not a degrade', () => {
    const r = checkFreshness(sig(NOW + 2), NOW);
    expect(r).toEqual({ ok: true, reason: 'ok', degradesOpen: false, skewSeconds: 2 });
  });
});

test.describe('mutation guard: the split is exact, so neither always-answer survives', () => {
  test('a sweep of offsets rejects precisely the ones past tolerance', () => {
    const offsets = [-86_400, -600, -1, 0, 1, 299, 300, 301, 600, 86_400];
    const rejected = offsets.filter((o) => !checkFreshness(sig(NOW + o), NOW).ok);

    // Printed rather than only asserted. A checker that can pass while measuring
    // nothing eventually does, so the denominator goes in the output.
    console.log(`swept ${offsets.length} offsets, rejected ${rejected.length}: ${rejected.join(', ')}`);

    expect(offsets.length).toBe(10);
    expect(rejected).toEqual([301, 600, 86_400]);
  });

  test('the sweep is sensitive to the comparison, so it cannot pass vacuously', () => {
    /**
     * The two mutations that would otherwise survive, driven through the
     * tolerance parameter rather than by hand-editing the module. Doing it this
     * way means the sensitivity proof is committed and re-runs forever, instead
     * of being something a past session claims to have done once.
     *
     *   tolerance Infinity   stands in for a guard that never rejects
     *   tolerance -Infinity  stands in for a guard that rejects everything
     *
     * If the real run above ever matched either of these counts, the assertion
     * would be measuring nothing.
     */
    const offsets = [-86_400, -600, -1, 0, 1, 299, 300, 301, 600, 86_400];
    const count = (tol) => offsets.filter((o) => !checkFreshness(sig(NOW + o), NOW, tol).ok).length;

    const neverRejects = count(Infinity);
    const alwaysRejects = count(-Infinity);
    const real = count(FUTURE_TOLERANCE_SECONDS);

    console.log(`sensitivity: never=${neverRejects}, always=${alwaysRejects}, real=${real} of ${offsets.length}`);

    expect(neverRejects).toBe(0);
    expect(alwaysRejects).toBe(offsets.length);
    expect(real).toBe(3);
  });
});
