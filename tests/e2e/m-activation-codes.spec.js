/**
 * The activation-code generator and its normalizer.
 *
 * An activation code is a bearer credential: whoever holds the string gets an
 * account and the paid book behind it. So this file tests the properties that
 * make it safe to hand one to a stranger, not the happy path of generating one.
 *
 * The three that matter, in the order they would hurt:
 *
 *   1. ENTROPY. A generator that quietly draws from a smaller space than it
 *      claims is not a visible bug - every code still looks fine. The uniformity
 *      and uniqueness blocks below are what would notice.
 *
 *   2. ROUND TRIP. normalize(generate()) must reproduce exactly the string that
 *      was hashed at mint time. If it does not, valid codes are rejected and the
 *      failure looks like "the customer typed it wrong", which is the single
 *      hardest kind of bug to get reported accurately.
 *
 *   3. HASH AGREEMENT. Every accepted spelling of one code - lowercase, spaced,
 *      with O for 0 - must hash to the same digest. This is the property that
 *      makes typo repair work end to end rather than only in the normalizer.
 *
 * Pure module, no database: it imports activationCodeCrypto.js directly, the way
 * k-admin-token.spec.js imports adminToken.js.
 */
import { test, expect } from '@playwright/test';
import {
  ALPHABET,
  CODE_LENGTH,
  generateActivationCode,
  normalizeActivationCode,
  formatActivationCode,
  hashActivationCode,
  activationErrorText,
} from '../../src/lib/server/activationCodeCrypto.js';

test.describe('shape', () => {
  test('generated codes are three groups of four, dash separated', () => {
    for (let i = 0; i < 200; i++) {
      expect(generateActivationCode()).toMatch(/^[0-9A-Z]{4}-[0-9A-Z]{4}-[0-9A-Z]{4}$/);
    }
  });

  test('the alphabet excludes every confusable letter', () => {
    // The whole point of Crockford's alphabet. If someone "helpfully" restores
    // the full A-Z, codes stop surviving a phone call and this catches it.
    for (const forbidden of ['I', 'L', 'O', 'U']) {
      expect(ALPHABET.includes(forbidden), `${forbidden} must not be in the alphabet`).toBe(false);
    }
    expect(ALPHABET.length).toBe(32);
    expect(new Set(ALPHABET).size, 'alphabet must have no duplicate symbols').toBe(32);
  });

  test('formatActivationCode is the exact inverse of stripping the dashes', () => {
    const code = generateActivationCode();
    const canonical = normalizeActivationCode(code);
    expect(formatActivationCode(canonical)).toBe(code);
  });
});

test.describe('entropy', () => {
  /**
   * A biased generator still produces codes that look right, so shape tests
   * cannot see this. 4000 codes x 12 symbols = 48000 draws over 32 symbols,
   * so each symbol is expected ~1500 times with sd ~38. The +/-20% band is
   * about eight standard deviations - wide enough never to flake, narrow
   * enough to catch a generator drawing from a truncated alphabet (which would
   * leave symbols at zero) or skewed by a modulo mistake.
   */
  test('every symbol appears, at roughly the expected rate', () => {
    const SAMPLES = 4000;
    const counts = new Map([...ALPHABET].map((c) => [c, 0]));

    for (let i = 0; i < SAMPLES; i++) {
      for (const ch of normalizeActivationCode(generateActivationCode())) {
        counts.set(ch, counts.get(ch) + 1);
      }
    }

    const expected = (SAMPLES * CODE_LENGTH) / ALPHABET.length;
    for (const [symbol, n] of counts) {
      expect(n, `symbol ${symbol} never appeared`).toBeGreaterThan(0);
      expect(n, `symbol ${symbol} appeared ${n} times, expected ~${expected}`)
        .toBeGreaterThan(expected * 0.8);
      expect(n, `symbol ${symbol} appeared ${n} times, expected ~${expected}`)
        .toBeLessThan(expected * 1.2);
    }
  });

  test('10000 codes are all distinct', () => {
    // At 60 bits a collision in 10k draws is ~1 in 10^10. A repeat here means
    // the generator is not drawing from the space it claims - a seeded PRNG, a
    // reused buffer, or getRandomValues silently returning zeros.
    const seen = new Set();
    for (let i = 0; i < 10000; i++) seen.add(generateActivationCode());
    expect(seen.size).toBe(10000);
  });

  test('codes are not all-zeros, which is what a dead CSPRNG returns', () => {
    // Uint8Array starts zero filled. If getRandomValues were ever a no-op the
    // mask would map every byte to ALPHABET[0] and produce "0000-0000-0000"
    // forever, which the uniqueness test above would catch only as a set of
    // size 1 - this names the actual failure.
    const dead = ALPHABET[0].repeat(CODE_LENGTH);
    for (let i = 0; i < 50; i++) {
      expect(normalizeActivationCode(generateActivationCode())).not.toBe(dead);
    }
  });
});

test.describe('normalization round trip', () => {
  test('normalize(generate()) is stable and strips only the dashes', () => {
    for (let i = 0; i < 200; i++) {
      const display = generateActivationCode();
      const canonical = normalizeActivationCode(display);
      expect(canonical).toBe(display.replace(/-/g, ''));
      expect(canonical).toHaveLength(CODE_LENGTH);
      // Idempotent: normalizing an already-canonical code changes nothing.
      expect(normalizeActivationCode(canonical)).toBe(canonical);
    }
  });

  test('presentation differences all collapse to one canonical string', () => {
    const canonical = normalizeActivationCode(generateActivationCode());
    const grouped = formatActivationCode(canonical);

    const spellings = [
      grouped,
      grouped.toLowerCase(),
      grouped.replace(/-/g, ' '),
      grouped.replace(/-/g, ''),
      `  ${grouped}  `,
      grouped.replace(/-/g, '​'), // zero-width space, survives HTML paste
      grouped.replace(/-/g, ' '), // non-breaking space, from a PDF
      grouped.split('').join(' '),
    ];

    for (const spelling of spellings) {
      expect(normalizeActivationCode(spelling), `spelling: ${JSON.stringify(spelling)}`)
        .toBe(canonical);
    }
  });

  test('confusable glyphs are repaired the way a human would have meant them', () => {
    // Build a code containing the digits people mistype, then hand back the
    // letter forms and require the original.
    const canonical = '01234567890V'.slice(0, CODE_LENGTH);
    expect(canonical).toHaveLength(CODE_LENGTH);

    expect(normalizeActivationCode('O1234567890V')).toBe(canonical); // O -> 0
    expect(normalizeActivationCode('0I234567890V')).toBe(canonical); // I -> 1
    expect(normalizeActivationCode('0L234567890V')).toBe(canonical); // L -> 1
    expect(normalizeActivationCode('01234567890U')).toBe(canonical); // U -> V
    expect(normalizeActivationCode('oi234567890u')).toBe(canonical); // all at once, lowercase
  });
});

test.describe('normalization rejects what is not a code', () => {
  test('wrong lengths are refused', () => {
    const canonical = normalizeActivationCode(generateActivationCode());
    expect(normalizeActivationCode(canonical.slice(0, -1))).toBeNull();
    expect(normalizeActivationCode(canonical + '7')).toBeNull();
    expect(normalizeActivationCode('')).toBeNull();
  });

  test('non-strings are refused rather than coerced', () => {
    // A JSON body can carry any of these. Coercing an object to "[object
    // Object]" and then measuring its length is how type confusion starts.
    for (const junk of [null, undefined, 42, {}, [], true, Symbol('x')]) {
      expect(normalizeActivationCode(/** @type {any} */ (junk))).toBeNull();
    }
  });

  test('symbols outside the alphabet are refused', () => {
    // Twelve characters, right length, wrong contents - so this can only be
    // caught by the alphabet check rather than the length check.
    expect(normalizeActivationCode('!@#$%^&*()_+')).toBeNull();
  });
});

test.describe('hashing', () => {
  test('a digest is 64 lowercase hex characters', async () => {
    const digest = await hashActivationCode(normalizeActivationCode(generateActivationCode()));
    expect(digest).toMatch(/^[0-9a-f]{64}$/);
  });

  test('known-answer test against the SHA-256 of a fixed string', async () => {
    // Pinned so a future "optimization" that changes the encoding, the digest,
    // or the hex conversion invalidates every code already in the database
    // loudly here rather than silently in production.
    // Cross-checked against a different SHA-256 implementation rather than
    // recorded from this one, which would only prove the code agrees with
    // itself:  printf 'ABCDEFGHJKMN' | shasum -a 256
    expect(await hashActivationCode('ABCDEFGHJKMN')).toBe(
      'f798776cb4d1e5975b47ed94fcc91314bc8d5c6935ff56b33c03b08c52356818'
    );
  });

  test('every accepted spelling of one code hashes identically', async () => {
    // The property that makes typo repair real. Normalization could be correct
    // while the hash path bypassed it, and codes would work only when typed
    // perfectly.
    const canonical = normalizeActivationCode(generateActivationCode());
    const grouped = formatActivationCode(canonical);

    const expected = await hashActivationCode(canonical);
    for (const spelling of [grouped, grouped.toLowerCase(), `  ${grouped} `]) {
      expect(await hashActivationCode(normalizeActivationCode(spelling))).toBe(expected);
    }
  });

  test('different codes hash differently', async () => {
    const a = normalizeActivationCode(generateActivationCode());
    const b = normalizeActivationCode(generateActivationCode());
    expect(await hashActivationCode(a)).not.toBe(await hashActivationCode(b));
  });
});

test.describe('error copy gives nothing away', () => {
  test('an unknown code and a malformed code read identically', () => {
    // Distinguishing "no such code" from "not a code" is a free enumeration
    // oracle and helps a real user not at all.
    expect(activationErrorText('not_found')).toBe(activationErrorText('nonsense-reason'));
  });

  test('every reason produces a sentence, never undefined', () => {
    for (const reason of ['not_found', 'expired', 'revoked', 'exhausted', 'unavailable']) {
      expect(activationErrorText(reason), reason).toMatch(/\S/);
    }
  });
});
