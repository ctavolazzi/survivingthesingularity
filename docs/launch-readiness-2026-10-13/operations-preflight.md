# Deployment preflight and release evidence

The launch preflight checks the configuration supplied to its process. It does
not inspect Cloudflare's stored secrets or turn a local pass into permission to
announce that checkout works. No production credentials are configured in this
workspace; the current environment therefore cannot pass the configuration gate.

## Read-only commands

Supply values through the intended environment's secret store or an existing
private environment file outside the repository. The script does not load `.env`
automatically. Never paste credential values into an issue, PR or this document.

```sh
# No network: check configuration and the reviewed bundle fingerprint.
npm run check:launch

# Explicit read-only service checks with test-mode credentials.
npm run check:launch -- --services --mode=test

# Read-only verification of the production configuration and provider records.
npm run check:launch -- --services --mode=live

# Independently compare the private storage object with the local reviewed ZIP.
# Default is verification only; uploading requires the explicit --upload option.
node scripts/deploy-book-bundle.mjs
```

`PUBLIC_ORIGIN` identifies the intended site for preflight webhook matching.
`PUBLIC_BASE_URL` controls customer email links and must match that origin. Use
the intended HTTPS preview origin and test-mode keys together for the rehearsal;
use `https://survivingthesingularity.com` and live-mode keys for the production
configuration check. See [`.env.example`](../../.env.example) for the variable
contract, and [the rollout](../payment-reliability-rollout.md) for migration and
fulfillment details.

Configuration checks cover the standard Stripe price ID, key mode, webhook
secrets, production sender, Supabase service credentials, exact bundle
fingerprint and reconciliation token. `--services` adds bounded GET requests
for the actual USD 5.00 one-time price, enabled Stripe webhook/events, verified
Resend sending domain and exposed Supabase RPC schema. It creates no sessions,
payments, emails, database rows or storage objects. Provider bodies and secrets
are omitted from its report. An unverified service check produces a nonzero exit.

A sending-only Resend key may lack domain-read permission. A 403 leaves domain
verification unverified; verify it in the provider dashboard instead of
broadening the production sending key just to obtain a green script result.
Stripe restricted keys are also supported; insufficient inspection permissions
leave those checks unverified and require dashboard evidence, not a broader key.
Schema discovery proves that RPC paths are exposed, not that migration 017's
semantics, permissions or concurrent behavior are correct. The disposable
Postgres integration test covers the checked-in SQL; verify the hosted migration
separately.

## Evidence required before the purchase announcement

Record the candidate commit and intended environment with each observation.
Keep customer addresses, session IDs, secrets and private signed links out of
public evidence. Record results and sanitized references instead.

| Check | Evidence to retain |
| --- | --- |
| Database | Migration 017 applied after prerequisites; hosted RPCs and permissions verified; backup and rollback available |
| Private bundle | Reviewed manifest, successful remote byte comparison and private bucket status |
| Test purchase | Correct test price; authentic signed checkout event; exactly one purchase; provider acceptance ID and actual inbox receipt |
| Buyer access | Receipt opens the intended environment; current ZIP extracts; PDF/EPUB open; access code and return-link recovery work |
| Failure recovery | Provider failure remains retryable; replay does not duplicate fulfillment; two concurrent checkout tabs do not create two independently payable purchases |
| Consent and email | Optional marketing remains unchecked; welcome/unsubscribe links target the intended environment; delivery-event webhook recorded |
| Monitor | Hosting and CI tokens match; manual reconciliation succeeds; failure notification destination works |
| Deployed site | Correct commit, `/sample` and downloads return current content; crawler guard passes against the actual domain |
| Social preview | Inspect the sample, offer and checklist links in intended social apps after deployment; refresh stale platform caches where supported |

Run `python3 scripts/check-social-previews.py --origin https://survivingthesingularity.com`
after deployment. It compares actual HTML, sitemap and preview bytes with this
checkout. It does not prove that every platform has refreshed its cached card.

The current [launch brief](audience-evidence-and-social-launch.md) provides an
honest preparation post and separate post-activation copy. Use the latter only
after the integration and deployed-site evidence exists. No social posts,
messages, ad campaigns or test purchases were sent during this review.

## Provider references

- [Stripe price retrieval](https://docs.stripe.com/api/prices/retrieve)
- [Stripe webhook endpoint listing](https://docs.stripe.com/api/webhook_endpoints/list)
- [Resend domain listing](https://resend.com/docs/api-reference/domains/list-domains)
- [Resend domain retrieval](https://resend.com/docs/api-reference/domains/get-domain)
- [Supabase API keys](https://supabase.com/docs/guides/api/api-keys)
- [PostgREST OpenAPI](https://docs.postgrest.org/en/stable/references/api/openapi.html)
