/**
 * Check locally knowable prerequisites for selling an emailed digital product.
 * This does not verify a Resend credential, domain ownership or inbox delivery;
 * the deployment preflight and a real test purchase must establish those.
 * Keep this pure so checkout and the deployment preflight use the same rules.
 */
export function validatePurchaseEmailConfig(env = {}) {
  const key = typeof env.RESEND_API_KEY === 'string' ? env.RESEND_API_KEY : '';
  if (!/^re_[A-Za-z0-9_-]{8,}$/.test(key)
      || /placeholder|your[_-]|replace[_-]?me|changeme|example|dummy|mock|x{8,}/i.test(key)) {
    return { ok: false, error: 'RESEND_API_KEY is missing, malformed or a placeholder' };
  }

  const rawFrom = typeof env.EMAIL_FROM === 'string' ? env.EMAIL_FROM : '';
  const from = rawFrom.trim();
  // One sender only. Reject header injection before parsing a display name.
  if (!from || from.length > 320 || /[\r\n,;]/.test(rawFrom)) {
    return { ok: false, error: 'EMAIL_FROM must identify one configured production sender' };
  }
  const named = from.match(/^([^<>]+)<([^<>]+)>$/);
  const address = (named ? named[2].trim() : from).toLowerCase();
  const parts = address.split('@');
  const local = parts[0];
  const domain = parts[1] || '';
  const labels = domain.split('.');
  if (parts.length !== 2 || address.length > 254 || local.length > 64
      || !/^[a-z0-9_%+.-]+$/.test(local) || local.startsWith('.')
      || local.endsWith('.') || local.includes('..') || labels.length < 2
      || labels.some((label) => !/^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(label))
      || !/^[a-z]{2,}$/.test(labels.at(-1))) {
    return { ok: false, error: 'EMAIL_FROM is not a valid sender address' };
  }
  const unavailableDomains = ['resend.dev', 'example.com', 'example.net', 'example.org', 'yourdomain.com'];
  if (unavailableDomains.some((reserved) => domain === reserved || domain.endsWith(`.${reserved}`))
      || /\.(test|invalid|localhost|local|example)$/.test(domain)) {
    return { ok: false, error: 'EMAIL_FROM must use your production sending domain, not a test or placeholder domain' };
  }
  return { ok: true, senderDomain: domain };
}

/** PUBLIC_ values must come from SvelteKit's public environment at runtime. */
export function validateEmailLinkOrigin(env = {}) {
  try {
    const url = new URL(env.PUBLIC_BASE_URL || 'https://survivingthesingularity.com');
    if (url.protocol === 'https:' && !url.username && !url.password && url.pathname === '/' && !url.search && !url.hash) {
      return { ok: true, origin: url.origin };
    }
  } catch { /* Return only the controlled diagnostic below, never input. */ }
  return { ok: false, error: 'PUBLIC_BASE_URL must be an HTTPS site origin.' };
}
