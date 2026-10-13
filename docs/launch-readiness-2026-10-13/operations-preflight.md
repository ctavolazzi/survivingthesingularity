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

# Rehearse the monitor against the isolated preview with its own token.
RECONCILE_ORIGIN="${PUBLIC_ORIGIN:?Set PUBLIC_ORIGIN to the isolated preview origin}" node scripts/check-payment-reconciliation.mjs

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

Use an **isolated Supabase project/database and private storage** for the preview,
with the required migrations, verified bundle and preview-only monitor token.
Test-mode Stripe does not isolate the application's database: ownership and
checkout reservations are keyed by email and edition without a mode partition.
Do not use production customer tables for rehearsal purchases or injected
database/provider failures. Use fresh test addresses and a controlled mailbox.

The monitor command above can rehearse the preview before merge. GitHub cannot
manually dispatch the new workflow until it exists on the default branch. After
merge, verify a manual production run and subsequent hourly runs, with the same
production token in hosting and the GitHub secret and working failure
notifications. Preview rehearsal does not establish production monitoring.

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
| Monitor | Preview command rehearsal passes before merge; after merge, production hosting/CI tokens match, manual and scheduled workflow runs succeed, and the failure notification destination works |
| Deployed site | Correct commit, `/sample` and downloads return current content; crawler guard passes against the actual domain |
| Social preview | Inspect the sample, offer and checklist links in intended social apps after deployment; refresh stale platform caches where supported |

Run `python3 scripts/check-social-previews.py --origin https://survivingthesingularity.com`
after deployment. It compares actual HTML, sitemap and preview bytes with this
checkout. It does not prove that every platform has refreshed its cached card.

The current [launch brief](audience-evidence-and-social-launch.md) provides an
honest preparation post and separate post-activation copy. Use the latter only
after the integration and deployed-site evidence exists. No social posts,
messages, ad campaigns or test purchases were sent during this review.

## Automatic Cloudflare deployment gate

The existing GitHub–Cloudflare Pages integration publishes `main`; a local
Cloudflare login is not required to trigger it. The release now runs
`scripts/check-hosted-deployment.mjs` from a build-only Vite plugin, before the
server compiles. This also covers a direct `vite build` command. The nested
client build does not repeat the provider checks.

The gate uses the build environment's existing credentials in place. It does not
export credentials, read customer rows, modify the database, upload files, create
payments or send email. It checks live provider configuration, required exposed
database columns/RPC arguments, bucket privacy and the downloaded ZIP's exact size
and SHA256. It does not need a copy of the private ZIP in the public repository.
Errors and logs use controlled messages without provider response bodies.

Cloudflare `main` builds must pass every check. Missing or unverifiable values
stop that build; a failed build leaves the previous deployment serving. Ordinary
local/GitHub builds skip hosted requests. Other Cloudflare branches fail closed
until an isolated preview policy is established. The production origin defaults
to `https://survivingthesingularity.com`; an explicit conflicting origin fails.

This gate can use configuration already present in Cloudflare even when the
local workspace has no credentials. Build-time availability is checked, not
assumed. A failed check requires fixing the hosted setup and retrying; there is
no bypass switch. The checks cannot prove migration function bodies or grants,
matching webhook signing secrets, actual checkout fulfillment, inbox arrival or
that runtime settings equal build settings. Preserve the separate evidence above
and verify deployed behavior before announcing that paid delivery is ready.

## Provider references

- [Stripe price retrieval](https://docs.stripe.com/api/prices/retrieve)
- [Stripe webhook endpoint listing](https://docs.stripe.com/api/webhook_endpoints/list)
- [Resend domain listing](https://resend.com/docs/api-reference/domains/list-domains)
- [Resend domain retrieval](https://resend.com/docs/api-reference/domains/get-domain)
- [Supabase API keys](https://supabase.com/docs/guides/api/api-keys)
- [PostgREST OpenAPI](https://docs.postgrest.org/en/stable/references/api/openapi.html)
