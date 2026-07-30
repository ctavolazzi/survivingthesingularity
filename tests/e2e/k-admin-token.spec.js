/**
 * The admin bearer-token guard (supports B-06).
 *
 * This is the code between the open internet and a list of customer email
 * addresses with payment references attached, so it is tested for the failures
 * that actually happen to admin endpoints rather than the happy path.
 *
 * The headline case is the last one in the first block: an UNSET secret must not
 * authorise anybody. The classic way an admin endpoint ends up world-readable is
 * a comparison where "no secret configured" and "caller sent nothing" are both
 * falsy and therefore equal.
 */
import { test, expect } from '@playwright/test';
import {
  authorizeAdmin,
  constantTimeEqual,
  parseBearer,
  MIN_TOKEN_LENGTH
} from '../../src/lib/server/adminToken.js';

// 40 chars, comfortably over the minimum.
const GOOD = 'a'.repeat(20) + 'b'.repeat(20);

test.describe('fail shut on configuration problems', () => {
  test('an unset secret authorises nobody, even with no token supplied', () => {
    // THE bug this file exists to prevent: falsy secret vs falsy token.
    for (const secret of [undefined, null, '', '   ', '\t\n']) {
      for (const header of [undefined, null, '', 'Bearer ', `Bearer ${GOOD}`]) {
        const r = authorizeAdmin(header, secret);
        expect(r.ok, `secret=${JSON.stringify(secret)} header=${JSON.stringify(header)}`).toBe(false);
        expect(r.reason).toBe('not-configured');
        expect(r.status).toBe(503);
      }
    }
  });

  test('an empty token cannot match an empty secret', () => {
    expect(authorizeAdmin('Bearer ', '').ok).toBe(false);
  });

  test('a secret shorter than the minimum is refused rather than trusted', () => {
    for (const weak of ['admin', 'password', 'x', 'a'.repeat(MIN_TOKEN_LENGTH - 1)]) {
      const r = authorizeAdmin(`Bearer ${weak}`, weak);
      expect(r.ok, `weak=${weak}`).toBe(false);
      expect(r.reason).toBe('token-too-short');
      expect(r.status).toBe(503);
    }
  });

  test('a secret exactly at the minimum length is accepted', () => {
    const exact = 'c'.repeat(MIN_TOKEN_LENGTH);
    const r = authorizeAdmin(`Bearer ${exact}`, exact);
    expect(r.ok).toBe(true);
    expect(r.status).toBe(200);
  });

  test('not-configured is reported as 503, never 401', () => {
    // A 401 would tell an operator their token was wrong when the server has no
    // token at all, which is how an endpoint stays broken for weeks.
    expect(authorizeAdmin(`Bearer ${GOOD}`, '').status).toBe(503);
  });
});

test.describe('token matching', () => {
  test('the correct token is authorised', () => {
    const r = authorizeAdmin(`Bearer ${GOOD}`, GOOD);
    expect(r.ok).toBe(true);
    expect(r.reason).toBe('ok');
  });

  test('a wrong token of the same length is rejected', () => {
    const wrong = 'b'.repeat(20) + 'a'.repeat(20);
    expect(wrong.length).toBe(GOOD.length);
    const r = authorizeAdmin(`Bearer ${wrong}`, GOOD);
    expect(r.ok).toBe(false);
    expect(r.reason).toBe('bad-token');
    expect(r.status).toBe(401);
  });

  test('a token that is a prefix of the secret is rejected', () => {
    const r = authorizeAdmin(`Bearer ${GOOD.slice(0, -1)}`, GOOD);
    expect(r.ok).toBe(false);
    expect(r.reason).toBe('bad-token');
  });

  test('a token with the secret as a prefix is rejected', () => {
    expect(authorizeAdmin(`Bearer ${GOOD}x`, GOOD).ok).toBe(false);
  });

  test('a missing header is missing-token, distinct from bad-token', () => {
    const r = authorizeAdmin(null, GOOD);
    expect(r.ok).toBe(false);
    expect(r.reason).toBe('missing-token');
    expect(r.status).toBe(401);
  });

  test('matching is case sensitive on the token itself', () => {
    expect(authorizeAdmin(`Bearer ${GOOD.toUpperCase()}`, GOOD).ok).toBe(false);
  });
});

test.describe('bearer header parsing', () => {
  test('the scheme is case insensitive, the token is not touched', () => {
    for (const scheme of ['Bearer', 'bearer', 'BEARER', 'BeArEr']) {
      expect(parseBearer(`${scheme} abc`), scheme).toBe('abc');
    }
  });

  test('extra whitespace around the token is tolerated', () => {
    expect(parseBearer('Bearer   abc  ')).toBe('abc');
    expect(parseBearer('  Bearer\tabc  ')).toBe('abc');
  });

  test('a non-bearer scheme yields nothing', () => {
    for (const h of ['Basic abc', 'Token abc', 'abc', 'Bearerabc']) {
      expect(parseBearer(h), h).toBe(null);
    }
  });

  test('a bearer scheme with no token yields nothing', () => {
    for (const h of ['Bearer', 'Bearer ', 'Bearer    ', 'Bearer\t']) {
      expect(parseBearer(h), JSON.stringify(h)).toBe(null);
    }
  });

  test('non-string input yields nothing rather than throwing', () => {
    for (const h of [null, undefined, 42, {}, []]) {
      expect(parseBearer(h)).toBe(null);
    }
  });
});

test.describe('constant time comparison correctness', () => {
  test('equal strings compare equal', () => {
    expect(constantTimeEqual('abc', 'abc')).toBe(true);
    expect(constantTimeEqual('', '')).toBe(true);
    expect(constantTimeEqual(GOOD, GOOD)).toBe(true);
  });

  test('different strings compare unequal', () => {
    expect(constantTimeEqual('abc', 'abd')).toBe(false);
    expect(constantTimeEqual('abc', 'ABC')).toBe(false);
  });

  test('different lengths compare unequal, including prefixes', () => {
    expect(constantTimeEqual('abc', 'ab')).toBe(false);
    expect(constantTimeEqual('ab', 'abc')).toBe(false);
    expect(constantTimeEqual('', 'a')).toBe(false);
    expect(constantTimeEqual('a', '')).toBe(false);
  });

  test('a trailing NUL cannot be used to pad to equality', () => {
    // charCodeAt past the end of a string is read as 0, so a string ending
    // in a REAL 0 byte must still not compare equal to the shorter string it
    // pads. If it did, the length guard would be bypassable by appending NULs.
    // Written as an escape, not a literal byte: a raw 0x00 in source makes
    // every text tool treat this file as binary, which is how grep -c silently
    // returned nothing for it during verification.
    expect(constantTimeEqual('abc', 'abc\u0000')).toBe(false);
    expect(constantTimeEqual('abc\u0000', 'abc')).toBe(false);
    expect(constantTimeEqual('abc\u0000', 'abc\u0000')).toBe(true);
  });

  test('null and undefined are treated as empty, not as wildcards', () => {
    expect(constantTimeEqual(null, undefined)).toBe(true);
    expect(constantTimeEqual(null, 'a')).toBe(false);
    expect(constantTimeEqual('a', undefined)).toBe(false);
  });

  test('multibyte characters compare correctly', () => {
    expect(constantTimeEqual('héllo', 'héllo')).toBe(true);
    expect(constantTimeEqual('héllo', 'hello')).toBe(false);
  });

  test('every position is compared, not just the first mismatch', () => {
    // A comparison that returned on first difference would still get these
    // right; this asserts correctness at the last byte specifically, which is
    // the position a truncated loop would miss.
    const a = 'x'.repeat(64) + '0';
    const b = 'x'.repeat(64) + '1';
    expect(constantTimeEqual(a, b)).toBe(false);
  });
});
