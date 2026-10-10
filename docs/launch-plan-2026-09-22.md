# Launch plan: take real money, then publish from the book

**Date:** 2026-09-22
**Status:** planning, nothing executed yet
**Two tracks, run in parallel.** Track A turns the $5 preorder back on. Track B turns
the book's 23 precedents into a video slate. Filming does not wait on Track A, but
**the videos' call to action does**: `/book` is password-gated and the password comes
with the preorder, so until Track A is done there is nothing a viewer can buy or read.
Until then, point videos at `/ledger`, the free Precedent Ledger (all 23 cases, unlocked with
an email), so every video grows the list today.

---

## Track A: re-cutover to live Stripe

Source of truth for the detail is `STRIPE-GO-LIVE.md` ("Re-cutover checklist"). This
section only splits it by **who can do each step**, because most of it lives in
dashboards the repo cannot reach.

### A1. CT, Stripe dashboard in live mode (about 30 minutes)

- [ ] **Step 0.** Open `price_1To6muCYoTMkQm81rXG6QagG` and confirm it reads $5.00 USD
      one-time. Then open the Author's Edition price `price_1TogztCYoTMkQm81Nfv3uJ20`
      and write down its amount. If it is $9, the July overcharge is fully explained.
- [ ] **Step 1.** Payments, live mode, 2026-07-13 to 2026-07-26. Record the count of
      successful payments. The Supabase backup suggests zero, but only this screen is
      authoritative.
- [ ] **Step 3.** Developers, Webhooks, add endpoint
      `https://survivingthesingularity.com/api/webhooks/stripe` with
      `checkout.session.completed` and `checkout.session.async_payment_succeeded`.
      Copy the **live** `whsec_...`. The one in production today is the test-mode one
      and will reject every live event.
- [ ] **Step 5.** Create coupon 50% off, duration once, then promotion code
      `PREORDER50`. It only exists in test mode today.

### A2. CT, Supabase SQL editor (about 15 minutes)

- [ ] **Step 4.** Run whatever migrations are pending. `STRIPE-GO-LIVE.md` names
      `002`, `008`, `009`, `010`, but `sql/` now also holds `011_email_deliveries`,
      `012_lockdown_public_grants` and `013_checkout_durability`, written after that
      list. Get the real list with `python3 scripts/sts.py schema` on a machine that
      has the Supabase keys in `.env` (this session does not), and paste the output of
      `sts schema --bundle`. `002` matters most: without it the mailing list has no
      working unsubscribe.

### A3. CT, Cloudflare env vars, one sitting

- [ ] **Step 2.** Set `STRIPE_SECRET_KEY` (live), `STRIPE_PRICE_ID_STANDARD`,
      `STRIPE_WEBHOOK_SECRET` (the live one from A1), and keep `STRIPE_PRICE_ID`
      pointed at the **$5** price so the fallback cannot charge a different amount.
      Leave `STRIPE_PRICE_ID_AUTHORS` unset unless the Author's Edition should be
      sellable.

### A4. Claude, in the repo, same change as A3

- [ ] Flip `EXPECTED_MODE` from `test` to `live` in `.github/workflows/stripe-guard.yml`.
      This must land together with the key swap, not before (it would alarm daily on a
      test-mode site) and not after (it would stay silent through a rollback).
- [ ] Run `python3 scripts/sts.py stripe --live`. It must print `mode live`, webhook
      **VERIFIED** (a signed event returning 200, not merely a 400), and no price drift.

### A5. CT, one real purchase

- [ ] Buy one Standard Edition with a real card. Confirm: the download email arrives,
      the admin alert reaches `admin@johnnyautoseed.com`, a `preorders` row exists, and
      the session id starts with `cs_live_`. Refund it afterwards if you like.

### Decisions only CT can make

1. **Does the Author's Edition sell at launch?** Current answer in the doc is no
   (Standard only). Leaving `STRIPE_PRICE_ID_AUTHORS` unset keeps that path closed.
2. **Is $5 still the price?** Every page says $5 plus 50% off at launch. Changing it
   later means touching the six places on `/early-access` and the social meta.

**Total CT time: roughly an hour, in one sitting.** A1 and A2 can happen in any order.
A3 and A4 must happen together. A5 closes it.

---

## Track B: the precedent video slate

Every precedent is a self-contained story of 400 to 1,300 words, already sourced in
Appendix B and traced on `/factcheck`. Each one follows the same arc: a technology
arrives, respectable people are sure about it, they are wrong in an instructive way,
and the book says what that means for AI. That is a video format.

### The format (same for every episode)

| Part | Length | What happens |
|---|---|---|
| Cold open | 0:00 to 0:15 | The single most surprising fact, stated flat. No intro, no logo. |
| The story | about 4 to 6 min | The precedent as written, told in your voice, not read. |
| The turn | about 1 to 2 min | "Here is why this is happening again right now." Pulled from the chapter the precedent sits in. |
| The ask | 0:20 | "This is one of 23 cases in the book. $5 preorders it and you get the current draft right away." Link to `/early-access`. Until Track A is done, point to `/ledger` instead. |

**Plus one Short per episode:** the cold open and the punchline, under 60 seconds,
posted a few days before the long version to test the hook.

### Film first (strongest hooks, closest to what people are anxious about now)

| # | Precedent | Cold open (from the text) | Why it goes first |
|---|---|---|---|
| 1 | **P-03 One Million Years, Give or Take** (ch1) | Oct 9, 1903: the New York Times says a flying machine could take "one million to ten million years." Sixty-nine days later the Wright Flyer flew. | Shortest, sharpest, Short-native. Ideal first test of the format. |
| 2 | **P-10 The Robot in the Orchestra Pit** (ch7) | In 1906 the most recorded musician alive, John Philip Sousa, warned recorded music would make the vocal cord go the way of the tail. | The longest and deepest case (1,305 words), maps directly onto AI and creative work, and carries the 1929 and 1930 union ads as visuals you can show on camera. |
| 3 | **P-17 The Graveyard of the Unconvinced** (ch14) | 1975: a 24-year-old Kodak engineer builds the first digital camera. Management: "That's cute, but don't tell anyone about it." | Four companies in one episode. Pair it with P-18 (Fujifilm) as the "and here's who survived" ending. |
| 4 | **P-07 The Horse's Last Ledger** (ch5) | The word "horsepower" was a sales tool James Watt invented to price the horse in its own currency. | The book's cleanest labor-automation analogy, and the one viewers will argue about in the comments. |
| 5 | **P-19 Twenty Million Gardens** (ch15) | By 1944, backyard Victory Gardens grew about 40% of the fresh vegetables Americans ate. | The hopeful one. It is also the bridge to Johnny Autoseed without putting the company in the book. |

### Then, in any order

| Precedent | Cold open |
|---|---|
| P-01 The Reading Rage (preface) | In the 1790s, doctors diagnosed "reading fever" in young women. The dangerous technology was the novel. |
| P-02 The Toy at the Fair (ch0) | At the 1876 Centennial, the judges nearly skipped Bell's telephone. Everyone came to see a steam engine. |
| P-04 The Red Flag (ch2) | Britain made a man walk ahead of every car waving a red flag. The speed limits it came with lasted 31 years. |
| P-05 The Fleet That Sailed Home Forever (ch3) | In 1433 China had the most powerful navy on Earth. Then it lost a budget fight and let the ships rot. |
| P-06 The Great Demotion (ch4) | Copernicus moved Earth off the center of the universe. Everyone was sure meaning would collapse. People kept making breakfast. |
| P-08 The Grain Trap (ch6) | The first farmers were shorter, sicker and worked longer than the foragers before them. |
| P-09 The Frame-Breakers (ch7) | The Luddites were right about everything and still lost. Natural lead-in to P-10. |
| P-11 Torches of Freedom (ch8) | In 1929 a PR man sold cigarettes to women by staging a "freedom" march for the cameras. |
| P-12 The Year the Bronze Stopped (ch9) | Around 1177 BC the first global supply chain failed in a cascade, and a civilization went dark. |
| P-13 The Abbot's Confession (ch10) | In 1492 an abbot wrote a book attacking the printing press. Then he had it printed. |
| P-14 The Quartz Heresy (ch11) | The Swiss dismissed the quartz watch. Two-thirds of their watch jobs were gone in 15 years. |
| P-15 One Hundred Sixty Acres (ch12) | The Homestead Act passed in the middle of the Civil War. The people who filed during the chaos held title after. |
| P-16 The House That Came by Mail (ch13) | For 34 years you could order a house from the Sears catalog. Thousands are still standing. |
| P-18 The Mirror Twin (ch14) | Fujifilm faced Kodak's exact extinction event and lived. Use as P-17's ending or its own short. |
| P-20 Seventy-Nine Pages (ch16) | A failed tax officer with a printing press changed a continent's mind in 79 pages. |
| P-21 Access to Tools (ch17) | Three words on a 1968 catalog cover led to both the commune and the personal computer. |
| P-22 The Apocalypse That Ran On Time (ch18) | Y2K was real. The world spent about $300 billion so that nothing happened. |
| P-23 The Passing Fad (conclusion) | 1995, Newsweek: "The Internet? Bah!" A good series finale. |

### What Claude can produce per episode, on request

- A talking-points script (not a word-for-word read) built from the precedent and its
  chapter's turn, in the book's voice.
- The list of sources for that precedent from Appendix B, so every on-screen claim is
  checkable.
- A title and thumbnail-text shortlist, and the Short's cut points.
- Visuals already in the book that can go on screen (figures in `art-catalog.json`,
  and `credits.json` for rights).

### Open question for CT

**Which channel posts these?** The sites link both `@thecoffeejesus` and
`@johnnyautoseed`. The book is CT's own work and deliberately carries no Johnny
Autoseed branding, which points at `@thecoffeejesus`.

---

## What happens next, in order

1. CT answers the two Track A decisions and the channel question.
2. Claude writes the P-03 script and Short cut points (Track B, episode 1).
3. CT does A1 and A2 whenever there is an hour free; Claude does A4 the same sitting as A3.
4. Film P-03. Post the Short first, the long version a few days later.
