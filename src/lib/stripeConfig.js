/** Presence/format only: proving the secret matches Stripe needs a signed event. */
export function isConfiguredStripeWebhookSecret(value) {
  return typeof value === 'string'
    && /^whsec_[A-Za-z0-9_-]{8,}$/.test(value)
    && !/placeholder|your[_-]|replace[_-]?|changeme|example|dummy|mock|x{8,}/i.test(value);
}
