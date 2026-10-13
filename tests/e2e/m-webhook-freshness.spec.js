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
    // If this ever stops returning the value the whole guard silently stops
    // guarding, so it is asserted against an exact number, not just "not null".
    expect(parseSignatureTimestamp(sig(NOW))).toEqual({ present: true, seconds: NOW });
  });

  test('tolerates surrounding whitespace, a leading +, and extra schemes', () => {
    expect(parseSignatureTimestamp(` t=${NOW} , v1=abc , v0=def `).seconds).toBe(NOW);
    expect(parseSignatureTimestamp(`v1=abc,t=${NOW}`).seconds).toBe(NOW);
    expect(parseSignatureTimestamp(`t=+${NOW},v1=abc`).seconds).toBe(NOW);
  });

  test('does not mistake another key ending in t for the timestamp', () => {
    // `st=` and `nonce_t=` both end in t and both must be ignored. These report
    // ABSENT, not malformed, because no `t` key was present at all.
    expect(parseSignatureTimestamp('st=123,v1=abc')).toEqual({ present: false, seconds: null });
    expect(parseSignatureTimestamp('nonce_t=123,v1=abc')).toEqual({ present: false, seconds: null });
  });

  test('reports a present-but-unreadable t as PRESENT, which is what fails it shut', () => {
    // Every one of these is a case where a coercion would have produced an
    // answer: `Number('')` is 0, and stripe-node's own `parseInt('123abc')` is
    // 123. Reporting present:true is the entire fix for the bypass, because
    // present:false would degrade open and let the crafted header through.
    for (const bad of ['t=,v1=abc', 't=abc', 't=12.5', 't=1e9', 't= 12 3', 't=0x10', 't=NaN', 't=123abc']) {
      expect(parseSignatureTimestamp(bad), bad).toEqual({ present: true, seconds: null });
    }
  });

  test('refuses an integer too large to be exact, and still reports it present', () => {
    expect(parseSignatureTimestamp('t=99999999999999999999')).toEqual({ present: true, seconds: null });
  });

  test('reports absent for anything that is not a string', () => {
    for (const bad of [undefined, null, 42, {}, []]) {
      expect(parseSignatureTimestamp(bad)).toEqual({ present: false, seconds: null });
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

test.describe('the malformed-timestamp bypass, regression', () => {
  /**
   * THE BUG THIS BLOCK EXISTS FOR, measured over HTTP before it was fixed:
   * `t=abc` and `t=` both returned 200 with a valid signature, defeating this
   * guard AND Stripe's own tolerance at the same time.
   *
   * stripe-node's `parseHeader` runs `parseInt(kv[1], 10)` with no validity
   * check, and `makeHMACContent` signs the parsed value back as
   * `${details.timestamp}.${payload}`. So `t=abc` becomes the literal string
   * "NaN", an attacker signs over "NaN.{body}", and the tolerance test becomes
   * `NaN > 300`, which is false. The payload then had no time bound at all.
   */
  test('a present-but-unparseable t is REFUSED, not waved through', () => {
    for (const crafted of ['t=abc,v1=sig', 't=,v1=sig', 't=NaN,v1=sig', 't=123abc,v1=sig', 't=0x10,v1=sig']) {
      const r = checkFreshness(crafted, NOW);
      expect(r.ok, crafted).toBe(false);
      expect(r.reason, crafted).toBe('malformed-timestamp');
      expect(r.degradesOpen, crafted).toBe(false);
    }
  });

  test('malformed and absent are different verdicts, which is the whole fix', () => {
    // If these two ever collapse back to the same answer, the bypass is back.
    const malformed = checkFreshness('t=abc,v1=sig', NOW);
    const absent = checkFreshness('v1=sig', NOW);

    expect(malformed.ok).toBe(false);
    expect(absent.ok).toBe(true);
    expect(malformed.reason).not.toBe(absent.reason);
  });

  test('a malformed t is refused no matter what the clock says', () => {
    // Refusal must not depend on skew, since skew is unknowable here.
    for (const clock of [NOW, NOW - 1_000_000, NOW + 1_000_000, NaN]) {
      expect(checkFreshness('t=abc,v1=sig', clock).ok, String(clock)).toBe(false);
    }
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

  test('an ABSENT t degrades OPEN and says so', () => {
    // Failing shut here would reject every real webhook the day Stripe changes
    // its header format. `degradesOpen` is what stops that being read as a pass.
    // Unreachable in practice: with no `t`, stripe-node defaults to -1 and its
    // own tolerance rejects that as ancient before this code ever runs.
    for (const bad of ['v1=abc', '', undefined, null]) {
      const r = checkFreshness(bad, NOW);
      expect(r.ok, JSON.stringify(bad)).toBe(true);
      expect(r.reason).toBe('no-timestamp');
      expect(r.degradesOpen).toBe(true);
      expect(r.skewSeconds).toBeNull();
    }
  });

  test('a broken clock degrades OPEN under its OWN reason code', () => {
    // Not folded into no-timestamp. A log line naming the wrong cause is how the
    // constructEventAsync bug cost someone a long night.
    for (const clock of [NaN, Infinity, -Infinity]) {
      const r = checkFreshness(sig(NOW + 600), clock);
      expect(r.ok, String(clock)).toBe(true);
      expect(r.reason).toBe('unusable-clock');
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
