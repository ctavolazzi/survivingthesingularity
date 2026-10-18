# Surviving the Singularity: strategy brief

*A book: a food-first field manual for living through fast AI change.*

Strategy brief, October 18, 2026 · Stage: draft sold as a $5 preorder · survivingthesingularity.com · 99,172 words, 35 sections

> **Positioning.** For working adults who use AI but feel the ground shifting, Surviving the Singularity is the food-first field manual that turns AI anxiety into household and neighborhood actions you can try this month, unlike AI-at-work guides (Mollick) or long-range forecasts (Kurzweil).

**The call.** Sell the book to unsettled AI users first. Verify checkout end to end, put a date on the $5 preorder, then move to a $9.99 ebook and a $19.99 paperback. Build a list the book owns instead of borrowing the author’s other channels.

## Where it stands today

| Area | Today | Source |
|---|---|---|
| Manuscript | v0.11.0: Chapters 0 to 19 plus 8 appendices, 99,172 words, a 416-page reading PDF. | RELEASES.md, src/lib/data/book/book.json |
| Launch | v0.11 merged October 13 (PRs #31 and #32). | git log |
| Offer | $5 once: the draft (PDF, EPUB, online), The Precedent File (31 cases), future digital editions, half off a later print edition, 30-day refund. | src/lib/offer.js |
| Free entry points | /sample, /checklist, /signals (60 research items, updated by a bot) and 13 blog posts, the latest from July 17. | src/routes/blog/+page.server.js |
| Traction | Unknown: no sales analytics, conversion data or reader interviews exist yet. | docs/launch-readiness-2026-10-13/ |

## Market

Practical “adapt to AI” trade nonfiction, read by adults who feel AI changing their work and want something to do about it at home.

- **$6.0B**: US adult nonfiction publisher revenue, 2025 (trade overall $21.7B). Source: [AAP StatShot (search result)](https://publishers.org/news/aap-statshot-annual-report-publishing-revenues-totaled-33-4-billion-for-calendar-year-2025/)
- **71%**: US adults who expect AI to mean fewer jobs over 20 years. Source: [Pew Research, 2026 (search result)](https://www.pewresearch.org/short-reads/2026/08/18/young-adults-in-the-us-are-increasingly-wary-of-ai/)
- **18%**: US employees who think AI will likely eliminate their job within 5 years, up from 15%. Source: [Gallup, Q1 2026 (search result)](https://www.gallup.com/workplace/704225/rising-adoption-spurs-workforce-changes.aspx)

A reliable preorder conversion benchmark for self-published nonfiction was not found.

## Audience segments

Five reader segments, drawn from the book’s own routing table. Unsettled AI users come first: the largest measured group, and the one the book already routes first.

### Unsettled AI users (beachhead), fit 5 of 5

- **Who:** Workers whose tasks just changed because of AI.
- **Size:** 18% of US employees expect AI to take their job within 5 years (Gallup).
- **Job to be done:** Get more choices before they need them.
- **Pains:** No time; distrust of prepper hype.
- **Uses today:** Free newsletters, Co-Intelligence.
- **Will pay:** $5 is untested; comparable books list at $19 to $35.
- **Reach them:** Newsletters, podcasts, the free checklist.

The book routes them first (Chapters 6, 7, 11 and 19).

### Makers and builders, fit 4 of 5

- **Who:** Growers and repairers who want a real system to test.
- **Size:** Unknown.
- **Job to be done:** Try a working setup, not a theory.
- **Pains:** Hype without parts lists.
- **Uses today:** YouTube builds, forums.
- **Will pay:** Unknown.
- **Reach them:** Maker video, solarpunk communities.

Chapters 9, 13 and 17 fit; overlaps a sister company’s audience.

### Existing followers, fit 4 of 5

- **Who:** People who already follow the author.
- **Size:** Unknown; real purchases came in summer 2026.
- **Job to be done:** Support the work and read it properly.
- **Pains:** Mistaking the draft for the finished book.
- **Uses today:** The author’s free posts.
- **Will pay:** Proven by early charges; count unknown.
- **Reach them:** The author’s channels.

Warm, but a channel more than a market.

### Parents, fit 3 of 5

- **Who:** Parents planning for their kids’ futures.
- **Size:** Unknown.
- **Job to be done:** A household plan they can start.
- **Pains:** Overwhelm.
- **Uses today:** Parenting media.
- **Will pay:** Unknown.
- **Reach them:** Parent newsletters and podcasts.

Chapters 8 and 14 fit; the voice can read as abrasive.

### Organizers, educators, book clubs, fit 3 of 5

- **Who:** People who run a group or a local pilot.
- **Size:** Unknown.
- **Job to be done:** Run a discussion or a project from the book.
- **Pains:** Reputation risk; sourcing.
- **Uses today:** Mollick, Suleyman.
- **Will pay:** Higher budgets, no evidence yet.
- **Reach them:** Libraries, co-ops.

Appendices A and H fit; a slow buying cycle.

**Why this beachhead:** It is the largest measured group, the free sample and checklist fit the half hour it has, and it can be reached without leaning on the author’s other brands.

## Competitive landscape

| Alternative | Price | Strength | Weakness | How we differ |
|---|---|---|---|---|
| Co-Existence, Ethan Mollick | $32 hardcover | Credible; owns “AI at work”. Out October 20. | Not about household provision. | Food, tools and neighbors. |
| Co-Intelligence, Ethan Mollick | $30 hardcover | Bestselling practical guide. | Work-centric. | Life outside the job. |
| Futureproof, Kevin Roose | $19 paperback | “Rules for humans” framing. | Predates generative AI. | Current, with dated forecasts. |
| The Singularity Is Nearer, Ray Kurzweil | $35 hardcover, $20 paperback | Owns the title concept. | Optimistic and abstract. | Practical; the forecast is labeled personal. |
| Superagency, Reid Hoffman | $32 hardcover | Optimistic authority. | An elite viewpoint. | Ground-level and cooperative. |

## Value proposition and offer

- **For unsettled AI users:** Something changed at work. In 30 minutes, take one task inventory and one household step, without land, a quit or a subscription. $5 for the whole route, with a 30-day refund.
- **For existing followers:** The draft you watched being written, delivered properly, with future digital editions included and half off print. Promises written once in offer.js and shown the same everywhere.

### Pricing ladder

| Step | Tier | Price | What | Benchmark | Status |
|---|---|---|---|---|---|
| 1 | Preorder | $5 | Until a dated close; January 31 suggested. | Today’s offer. | Live |
| 2 | Ebook | $9.99 | After the preorder closes, on at least one retailer. | Kindle’s 70% royalty band is $2.99 to $12.99; nonfiction commonly $9.99 to $14.99. | Proposed |
| 3 | Paperback | $19.99 | With an ISBN; preorder buyers get half off. | Futureproof $19, Kurzweil paperback $20. | Proposed |
| 4 | Ebook plus print | $24.99 | Bundle. | The two prices less a small discount. | Proposed |
| 5 | Talks | Set after 3 requests | Use the free Appendix H guide until then. | No evidence of demand yet. | Proposed |

## Go to market

1. **Newsletter.** Substack says 5% to 10% of free readers convert; independent estimates sit near 3%. **First move:** Send the drafted launch post linking to /sample.
2. **Podcast guesting.** 58% of Americans 12 and up listen monthly; most bestselling authors guest on shows. **First move:** Pitch 10 AI-and-work and homesteading shows with the “the part I care most about is dinner” hook.
3. **Short video.** Reaches unsettled workers where they scroll. **First move:** Record the outline already drafted in the audience doc, ending on /sample.

## Plan

### Next 90 days

| Date | Milestone | Target |
|---|---|---|
| 2026-10-24 | Checkout verified | 1 live test purchase delivered and refunded |
| 2026-11-15 | Readers heard | 5 recorded reader conversations |
| 2026-12-15 | Podcast run | 10 pitches sent, 3 episodes recorded |
| 2027-01-15 | Preorders | 100 paid preorders |
| 2027-01-31 | Preorder closes | Ebook listed on 1 retailer at $9.99 |

### 12-month goals

- 1,000 paid digital copies by October 31, 2027.
- A print edition with an ISBN.
- 3,000 subscribers on a list the book owns.

## KPIs

| Metric | How to measure | Target |
|---|---|---|
| Net paid copies a week | Stripe payments minus refunds. | Baseline in November |
| Refund rate within 30 days | Stripe. | Under 5% |
| Delivery integrity | Reconciliation count stays at 0 and runs stay green. | 100% green |
| Signups by source | The source column of the waitlist table. | Baseline in November |
| Sample to paid conversion | Privacy-respecting analytics; tracking tags are not carried into payments yet. | Set after analytics |

## Risks

| Risk | Level | Mitigation |
|---|---|---|
| Open-ended promises: membership, print date and preorder close are undefined | High | Set dates or retire the promises in offer.js. |
| No exclusivity: the manuscript and files are public | Medium | Sell delivery and updates honestly; check retailer rules on freely available text. |
| Drift: off-thesis posts dilute the food-first message as Co-Existence lands | Low | Post on thesis. |

## Untangling

The book has its own site and checkout, but its readers, alerts and links still run through the author’s other ventures.

### What ties it to other projects today

- The personal site’s preorder form writes to this book’s signup list instead of linking here.
- Admin alerts go to a johnnyautoseed.com address; the newsletter, Ko-fi and YouTube links are the author’s personal accounts.
- Johnny Autoseed LLC appears on the homepage and /about; the book is promoted on three other sites.
- Chapter 13 and the FarmBot posts overlap Johnny Autoseed’s subject.
- The author’s time, split across at least five projects.

### Steps to stand alone

1. Replace the personal site’s form with a link to /early-access.
2. Route alerts to a survivingthesingularity.com address.
3. Start a list or newsletter section the book owns.
4. Keep one “about the author” link; mention Johnny Autoseed as disclosure, not a pitch.
5. Block a fixed weekly time for the book.

## Decisions for the owner

1. The preorder close date.
2. Define the membership, or drop the promise.
3. Print date, price and ISBN.
4. Which legal entity sells the book; the roadmap says “the LLC” without naming it.
5. A separate newsletter, or not.
6. Keep the manuscript openly licensed?
7. Retail distribution, or direct sales only?
8. Keep /signals and off-thesis posts?

## Sources

1. [AAP StatShot 2025](https://publishers.org/news/aap-statshot-annual-report-publishing-revenues-totaled-33-4-billion-for-calendar-year-2025/): Nonfiction and trade revenue
2. [Pew Research: young adults wary of AI](https://www.pewresearch.org/short-reads/2026/08/18/young-adults-in-the-us-are-increasingly-wary-of-ai/): 71% expect fewer jobs; 52% more concerned than excited
3. [Gallup: rising AI adoption](https://www.gallup.com/workplace/704225/rising-adoption-spurs-workforce-changes.aspx): 18% expect job loss within 5 years
4. [Kindle Direct Publishing royalties](https://kdp.amazon.com/en_US/help/topic/G200634560): 70% royalty price band
5. [Cambric: pricing a self-published book](https://cambric.pub/blog/how-to-price-your-self-published-book): Nonfiction ebook price range
6. [Substack conversion rates](https://www.reallygoodbusinessideas.com/p/substack-average-paid-subscriber-conversion-rate): Free to paid conversion
7. [PPC Land: 58% listen to podcasts](https://ppc.land/58-of-americans-now-listen-to-podcasts-monthly-a-record/): Podcast reach
8. [Author Media: bestselling authors on podcasts](https://www.authormedia.com/90-precent-of-usa-today-bestselling-authors-have-a-podcast-presence): Guesting pattern
9. [Co-Existence listing](https://bulkbookstore.com/co-existence-9798217181391): Price and release date
10. [Co-Intelligence listing](https://www.bookstores.com/browse/books/9780593716717): Price
11. [Futureproof listing](https://beta.thriftbooks.com/w/futureproof-9-rules-for-machine-age-humans_kevin-roose/24401369): Price
12. [The Singularity Is Nearer listing](https://www.harvard.com/book/9780399562785): Price
13. [Superagency listing](https://www.simonandschuster.com/books/Superagency/Reid-Hoffman/9798893310108): Price

---

*Prepared October 18, 2026 from the survivingthesingularity repo and web research. Page fetches were blocked during research, so every web figure comes from search results, and the live site was not checked; verify a figure before quoting it. Prices marked Proposed and the plan are recommendations. This is the public edition: internal operational detail is kept in a private copy.*
