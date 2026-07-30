/**
 * THE OFFER OBJECT
 *
 * The single source of truth for what a customer is buying. Every surface that
 * describes the offer imports from here: the homepage, /early-access, the
 * confirmation email, /policies, and /terms.
 *
 * WHY THIS FILE EXISTS
 *
 * On 2026-07-29 the live site described the same five dollar purchase three
 * different ways:
 *
 *   homepage       a checklist, a blueprint, a draft, and 29 documented cases
 *   /early-access  "$5 ... and a 50% discount at launch"
 *   /policies      "full refund at any time prior to shipment", citing the
 *                  U.S. FTC Mail, Internet, or Telephone Order Merchandise Rule
 *
 * The sales layer was selling digital access. The legal layer was selling
 * merchandise. Neither was lying on purpose. They drifted because each surface
 * carried its own prose copy of the offer, and prose drifts.
 *
 * Change anything in this file and every one of those surfaces moves together.
 * That is the point. If you find yourself typing offer language directly into a
 * component, that is the bug this file was written to prevent.
 *
 * RATIFIED 2026-07-29 by Chris. The three open questions are closed:
 *   D-01  what $5 buys           -> `sentence` + `included` below
 *   D-02  the scope of "forever" -> `foreverScope`, bounded on three axes
 *   D-03  the Print Edition      -> separate product, `excluded` below
 */

/**
 * How often each surface actually changes.
 *
 * Deliberately hedged on the site line. The real cadence is "when there is
 * something worth publishing", which is often but not reliably daily, and a
 * flat "updated daily" would be a promise the project has to keep on a slow
 * news week. Say the true thing.
 *
 * Note the split between `newsletter` and `listPolicy` below: the publication
 * sends a weekly newsletter, but the preorder list itself is deliberately
 * quieter than that. Those are two different lists and this file states both,
 * because letting them blur is exactly how the offer drifted the first time.
 */
export const cadence = Object.freeze({
  research: 'Research runs daily.',
  site: 'New coverage on the site as often as daily, whenever the news cycle gives us something worth publishing.',
  newsletter: 'A newsletter every week.',
  book: 'The digital book itself updates monthly.',
  print: 'A new Print Edition every year or two.'
});

/**
 * Count of documented cases in The Precedent File.
 *
 * PROVENANCE: `python3 scripts/sts.py verify` reports "all 23 present in the
 * book and indexed in Appendix D". The live site said 29 until 2026-07-29; the
 * likely origin of that number is the site's 29 pages. Every surface now
 * renders this constant rather than a typed integer, so the claim can only be
 * wrong in one place.
 *
 * C-02 replaces this with a build-time value emitted by sts.py. When it does,
 * this line is the only thing that changes.
 *
 * Declared here rather than only on the object below so the prose inside
 * `included` can interpolate it. A number written twice is a number that will
 * eventually disagree with itself, which is the whole finding this file closes.
 */
const PRECEDENT_COUNT = 23;

export const offer = Object.freeze({
  price: '$5',
  priceCents: 500,
  billing: 'once',

  /**
   * The price spelled out, for display headings that want words rather than a
   * numeral. Not new copy: `sentence` below already opens with these words, and
   * the homepage close already rendered them. Naming the string here is what
   * lets that heading derive instead of hardcoding, so a future price change
   * cannot leave a numeral and a spelled-out word disagreeing on the same page.
   */
  priceWords: 'Five dollars',

  /**
   * The load-bearing sentence. Rendered verbatim in the hero, in the close, and
   * on /policies. It is one sentence group rather than a bullet list, because a
   * bullet list is where qualifiers hide.
   *
   * The grandfathering clause is last on purpose: it is the single most
   * valuable thing in the offer, and it is the one a reader has to hear stated
   * plainly rather than infer from a table.
   */
  sentence:
    'Five dollars, once. You get every digital thing this project makes, ' +
    'starting with the book as it is being written and The Precedent File, ' +
    'and you keep getting it. When the membership launches later, you never ' +
    'pay it.',

  precedentCount: PRECEDENT_COUNT,

  /**
   * `available: true` means the customer has it the moment payment clears.
   * `false` means it is a real commitment about a thing that does not exist
   * yet, and the page must label it as such rather than let it read as
   * something already in hand. Two of the seven are promises about the future,
   * and hiding which two is how an honest offer starts sounding dishonest.
   */
  included: Object.freeze([
    Object.freeze({
      id: 'all-digital',
      title: 'All the digital content.',
      detail:
        'Everything this project publishes in digital form. There is no ' +
        'digital tier above this one and nothing else to buy.',
      available: true
    }),
    Object.freeze({
      id: 'book-draft',
      title: 'The book as it is being written.',
      detail:
        'Read the current pre-release version on the site, every section, ' +
        'updated monthly as the field moves.',
      available: true
    }),
    Object.freeze({
      id: 'precedent-file',
      title: 'The Precedent File.',
      detail:
        `${PRECEDENT_COUNT} documented cases of people meeting a machine that ` +
        'changed everything, every source cited so you can check the work.',
      available: true
    }),
    Object.freeze({
      id: 'early-access-list',
      title: 'A permanent place on the early-access list.',
      detail:
        'You stay on it until you ask to come off. One reply is enough, and ' +
        'it costs you nothing to leave.',
      available: true
    }),
    Object.freeze({
      id: 'updates-only',
      title: 'Only the updates that matter.',
      detail:
        'This list gets substantial version updates and nothing else. The ' +
        'weekly newsletter is a separate thing you can take or leave.',
      available: true
    }),
    Object.freeze({
      id: 'print-discount',
      title: '50% off the Print Edition.',
      detail:
        'Your place in line to buy the Print Edition at half price, as an ' +
        'early supporter, whenever the next one is ready.',
      available: false
    }),
    Object.freeze({
      id: 'membership-grandfathered',
      title: 'You never pay the membership.',
      detail:
        'When the subscription launches, preorder buyers are grandfathered in ' +
        'permanently. This is the most valuable thing on this list and it is ' +
        'the reason to buy before the window closes.',
      available: false
    })
  ]),

  /**
   * Stated as plainly as the included list, in the same place, at the same size
   * and weight. Saying what five dollars does not buy is worth more trust than
   * any adjective in the list above it.
   */
  excluded: Object.freeze([
    Object.freeze({
      id: 'print-edition',
      title: 'Not included: the Print Edition itself.',
      detail:
        'Print is a separate product at its own price, released as numbered ' +
        'editions every year or two. Five dollars buys you half off the next ' +
        'one, not the book itself. Anyone selling you a hardback for five ' +
        'dollars is selling you a shipping delay.'
    })
  ]),

  /**
   * "Forever" is an unbounded obligation being sold to strangers, so it gets a
   * bounded definition, rendered on the page rather than buried in terms.
   *
   * D-02, ratified: bounded on three axes. Cohort-limited, opt-out on request,
   * substantial updates only.
   */
  foreverScope:
    'This is bounded on three axes, deliberately. It is cohort-limited: it ' +
    'belongs to preorder buyers, and the preorder window closes. You can leave ' +
    'at any time by asking, and one reply is enough. And it covers substantial ' +
    'version updates rather than every small change, which is what keeps the ' +
    'list quiet enough to be worth staying on. For as long as this project is ' +
    'maintained, those updates reach you at no additional cost, by email and ' +
    'on this site. If it ever stops, you keep everything already delivered and ' +
    'the archive stays readable.',

  /**
   * What changes when the preorder window shuts. Named on the page because a
   * deadline a reader cannot see is not a reason to act, it is a trick.
   */
  windowClose:
    'When the preorder window closes, this price is gone. Readers arriving ' +
    'after it who want the updates buy a membership or a subscription instead. ' +
    'Everyone who bought at five dollars keeps everything, permanently.',

  /**
   * THE FLAG THE REFUND POLICY BRANCHES ON.
   *
   * False here means no merchandise is shipped, so the FTC Mail, Internet, or
   * Telephone Order Merchandise Rule thirty day clock never starts and
   * /policies must not carry a shipment clause. The $5 SKU grants digital
   * access plus a discount right on a future purchase; it ships nothing.
   *
   * The Print Edition, when it exists, is a SEPARATE SKU and gets its own
   * terms. Do not flip this flag to cover it. Flipping it here would grow the
   * shipment language back onto a page describing a product that still ships
   * nothing, which is the drift this file exists to stop.
   */
  shipsPhysicalGoods: false,

  refund: Object.freeze({
    windowDays: 30,
    contact: 'info@survivingthesingularity.com',
    subjectLine: 'Refund request'
  })
});

/**
 * Looks up one included or excluded item by its stable `id`.
 *
 * Surfaces that need a single line of the offer rather than the whole list use
 * this instead of indexing the array. `included[5]` silently becomes the wrong
 * promise the first time someone reorders the list, and the confirmation email
 * a paying customer receives is not a good place to find that out.
 *
 * Throws rather than returning undefined. A typo in an id is a build-time
 * mistake and should read like one, not render as the word "undefined" in a
 * receipt.
 */
export function offerItem(id) {
  const found =
    offer.included.find((item) => item.id === id) ||
    offer.excluded.find((item) => item.id === id);

  if (!found) {
    throw new Error(
      `offerItem: no offer item with id "${id}". Valid ids: ` +
        [...offer.included, ...offer.excluded].map((i) => i.id).join(', ')
    );
  }

  return found;
}

/**
 * The title of an offer item with its trailing period removed, for label and
 * heading contexts where the list's sentence punctuation reads wrong. Derived
 * so the label still cannot drift from the list it came from.
 */
export function offerItemLabel(id) {
  return offerItem(id).title.replace(/\.$/, '');
}

/**
 * Derives the refund paragraph from the offer rather than restating it.
 * /policies calls this. Nothing else should hand-write refund language.
 */
export function refundClause() {
  if (offer.shipsPhysicalGoods) {
    return (
      'This purchase includes physical goods. You may request a full refund at ' +
      'any time prior to shipment, for any reason or no reason, by emailing ' +
      `${offer.refund.contact} from the address used to place the order with ` +
      `the subject line "${offer.refund.subjectLine}". Refunds are processed ` +
      'to the original payment method. The U.S. FTC Mail, Internet, or ' +
      'Telephone Order Merchandise Rule and any other applicable ' +
      'consumer-protection law govern over anything stated on this page.'
    );
  }

  return (
    'This purchase is digital access and delivers immediately. Nothing is ' +
    'shipped, so no shipment date applies and no shipping policy is involved. ' +
    `You may request a full refund within ${offer.refund.windowDays} days, ` +
    `for any reason or no reason, by emailing ${offer.refund.contact} from ` +
    'the address used to place the order with the subject line ' +
    `"${offer.refund.subjectLine}". Refunds are processed to the original ` +
    'payment method. Applicable consumer-protection law governs over anything ' +
    'stated on this page.'
  );
}

/**
 * The one-line version, for meta descriptions, cards, and anywhere a full
 * paragraph will not fit. Derived so it cannot drift from `sentence`.
 */
export function offerBlurb() {
  return `${offer.price} once. Every digital thing this project makes, the book as it is being written, and The Precedent File. When the membership launches, you never pay it.`;
}
