# Social previews, links and accessibility review

Reviewed 13 October 2026. This is evidence for the release candidate; the production site still needs the deployment and external-service checks in the main handoff.

## Social sharing fixes

- The free `/sample` previously had no Open Graph or Twitter Card metadata. It now has a complete, server-rendered preview and a [dedicated card](../../static/images/og/sample.png).
- Most blog pages emitted three overlapping metadata sets, including empty `og:url` values from share controls that only discovered the URL after mounting. Each page now owns one metadata set; repeated share controls add no head tags. All 13 articles use the site's landscape blog card rather than relative portrait images or remotely hosted pictures.
- The [offer card](../../static/images/og/early-access.png) now distinguishes digital delivery from the separately sold, half-price first Print Edition. The [evidence card](../../static/images/og/factcheck.png) now describes historical checks and their limits instead of promising to trace every claim. The [checklist card](../../static/images/og/checklist.png) promises seven practical steps without an AGI deadline.
- The card renderer now uses an exact 1200 × 630 CSS viewport at 2× scale, local embedded fonts, waits for images/fonts, and rejects clipped content. A newer Chrome screenshot CLI had clipped the bottom of the old render path. All four reviewed cards are PNGs at 2400 × 1260, about 1.1 MB each.
- The blog layout's unverified `@survivingthesingularity` X account attribution was removed. It was not a valid X handle.

The [Open Graph protocol](https://ogp.me/) identifies title, type, image and canonical URL as the basic properties. The new HTTP guard checks those and the associated Twitter fields in actual crawler-visible HTML, rather than relying on component-source searches:

```sh
npm run build
npm run test:cloudflare
# Or, against an already running candidate:
python3 scripts/check-social-previews.py --origin http://127.0.0.1:8788
```

The Cloudflare check invokes this guard inside its isolated local Worker. It checks all 25 sitemap pages, including the dynamic offer page, with campaign parameters present: one nonempty metadata set, clean canonical and share URL, indexability, first-party HTTPS images, correct MIME/signature/dimensions, and image bytes matching the reviewed checkout. HTTP redirects fail the check. The actual run result belongs in the main validation log; this document does not substitute a source audit for that run.

`python3 scripts/sts.py og --json` also passed its source-level check for all 25 public routes. Browser validation confirmed that copying an article link strips campaign parameters and fragments, updates to the correct article after two client navigations, and that the sample's purchase link reaches the offer page.

## Launch links and attribution

Use `/sample` for readers who need to judge the book first, and `/early-access` when the post explicitly describes the current digital draft and the $5 preorder. The product is still described as a current draft/preorder; posting a print-book launch announcement would promise a different product.

Incoming UTM parameters remain on the entry URL, but ordinary internal links do not carry them into checkout, and the site does not store channel-to-purchase attribution. A tagged social link does not establish which channel produced a purchase. No additional tracking was introduced.

At review time, read-only requests to the production site showed `/sample` returning 404, and the live offer card still contained the old discount wording. `/images/og/factcheck.png` also returned 404. These are concrete deployment differences, not claims that the candidate is already live. After deployment, run the HTTP guard against the public origin and inspect the actual post composer or [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/) before posting; platform caches can retain old previews.

## Outbound links and support

The focused audit covered outbound links on the homepage, sample, offer, checklist, about and policies, plus the Discord invite. Of 25 HTTP probes, 20 returned 200 with matching destinations. Five were inconclusive: Substack and YouTube were blocked by the execution proxy; LinkedIn returned 999; FAO and the UN returned 403. These responses do not establish dead links.

The homepage's Goldman Sachs, Mercer, Grace et al. and LeRobot destinations were fetched and read. They match the corrected descriptions: potentially exposed full-time-equivalent work; executives' expected 1–20% headcount reductions; and the survey's 10%/2027 versus 50%/2047 estimates. The sample's Stanford PDF, CDFA, CFPB, Princeton, California Courts and Oxfam references resolved to the named documents or institutions. This spot check does not certify every statement in the book.

The Discord invite resolved to **Surviving the Singularity**, channel **rules**, with no expiry reported by Discord's public invite response. No account was joined. Support addresses are syntactically valid; the site domain publishes Cloudflare mail-routing MX records. That does not prove the `info@survivingthesingularity.com` forwarding rule or inbox works. Test receipt and support-mail delivery during production verification. Four launch-page YouTube videos could not be independently checked through the blocked YouTube endpoint; their click-to-load behavior is separate from video availability/content.

## Accessibility evidence

An isolated Chromium DOM audit used axe-core 4.14 outside the repository, with third-party requests and all HTTP writes blocked. It covered `/`, `/sample`, `/early-access`, `/checklist`, `/policies` and the unlocked `/book` at both 390 px and 1440 px widths: **12 scans, zero reported violations, zero page errors** after the fixes below.

The shared footer skipped heading levels using `h4` for its three navigation groups; these are now `h2` with the same classes. The unlocked book index had no `h1`; its existing title now supplies one with the same typography and margins. An early scan during the book's 400 ms fade produced transient contrast results; the final scan waited for full opacity, and the stable elements passed.

The audit also produced incomplete results requiring human judgment, including contrast over pseudo-elements/obscured backgrounds and the checklist's multiple-label pattern. The menu's invalid `aside`/`dialog` combination was changed to `div role="dialog"`. A separate check of the **built site with the menu open at 390 × 844** reported zero violations and page errors, and explicitly passed the allowed-role, dialog-name and hidden-focus checks. Three menu descriptions still needed manual contrast judgment because axe reported overlapping backgrounds; they were visually inspected. Zero automatically reported violations is not full WCAG or screen-reader certification. Real screen-reader use, social-app browsers, platform preview rendering and inbox delivery remain distinct checks.

Local evidence from this session is under `/workspace/review/`: `social-generated-heads-before.json`, `social-live-heads-before.json`, `social-live-assets-before.json`, `social-primary-link-results.json`, `social-video-mail-probes.json`, `share-browser.log`, `axe-launch/results.json` and `axe-launch/open-menu-built.json`. No social post, email, payment or production configuration was changed by these checks.
