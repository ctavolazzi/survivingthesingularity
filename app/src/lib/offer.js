/**
 * THE OFFER OBJECT
 *
 * This is the single source of truth for what a customer is buying. Every
 * surface that describes the offer imports from here: the hero, the offer
 * table, the closing call to action, and the refund policy.
 *
 * Why this file exists.
 *
 * On 2026-07-29 the live site described the same five dollar purchase three
 * different ways:
 *
 *   homepage       "one payment, everything now, plus 50% off at launch"
 *   /early-access  "$5 today ... an exclusive link at 50% off"
 *   /policies      "full refund at any time prior to shipment", citing the
 *                  FTC Mail, Internet, or Telephone Order Merchandise Rule
 *
 * The sales layer was selling access. The legal layer was selling merchandise.
 * Neither was lying on purpose. They drifted because each surface carried its
 * own prose copy of the offer, and prose drifts.
 *
 * Change anything in this file and every one of those surfaces moves together.
 * That is the point. If you find yourself typing offer language directly into
 * a component, that is the bug this file was written to prevent.
 */

export const offer = Object.freeze({
  price: '$5',
  priceCents: 500,
  cadence: 'once',

  /**
   * The load-bearing sentence. Rendered verbatim in the hero and in the close.
   * It is deliberately one sentence group and not a bullet list, because a
   * bullet list is where qualifiers hide.
   *
   * STATUS: recommended default, awaiting ratification. The two alternatives
   * considered are recorded in the design document, section 2:
   *   A. keep the 50% launch coupon (lowest change cost, weakest promise)
   *   B. include a physical copy (strongest offer, not a $5 product)
   */
  sentence:
    'Five dollars, once. You get the book as it is being written, The Precedent ' +
    'File, and every update forever. When the finished book ships, the digital ' +
    'edition is yours at no additional cost.',

  included: Object.freeze([
    Object.freeze({
      title: 'The book as it is being written.',
      detail: 'All 30 sections, readable now, updated as they change.'
    }),
    Object.freeze({
      title: 'The Precedent File.',
      detail: '23 documented cases, every source cited, delivered to your inbox.'
    }),
    Object.freeze({
      title: 'The Singularity Readiness Checklist.',
      detail: 'The short version you can act on this week.'
    }),
    Object.freeze({
      title: 'Every update forever.',
      detail:
        'Including the finished digital edition when the book ships, at no ' +
        'additional cost.'
    })
  ]),

  /**
   * Stated as plainly as the included list, in the same table, at the same
   * size. Saying what five dollars does not buy is worth more trust than any
   * adjective in the list above it.
   */
  excluded: Object.freeze([
    Object.freeze({
      title: 'Not included: a printed copy.',
      detail:
        'Physical is a separate product at a real price, and it is not ready. ' +
        'Anyone selling you a hardback for five dollars is selling you a ' +
        'shipping delay.'
    })
  ]),

  /**
   * "Forever" is an unbounded obligation, so it gets a bounded definition,
   * rendered on the page rather than buried in terms.
   */
  foreverScope:
    'As long as this book is maintained, every revision, new section, and ' +
    'correction reaches you at no additional cost, by email and on this site. ' +
    'If the project ever stops, you keep everything already delivered and the ' +
    'archive stays readable. That is the whole promise. There is no tier above ' +
    'it and nothing else to buy.',

  /**
   * The single flag the refund policy branches on.
   *
   * When this is false, no merchandise is shipped, so the FTC Merchandise Rule
   * thirty day clock never starts and /policies must not contain a shipment
   * clause. Flip it to true and the policy page grows the shipment language
   * back automatically. That coupling is the entire reason this flag lives in
   * the offer object rather than in the policy copy.
   */
  shipsPhysicalGoods: false,

  refund: Object.freeze({
    windowDays: 30,
    contact: 'hello@survivingthesingularity.com',
    subjectLine: 'Refund request'
  })
});

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
      `the subject line "${offer.refund.subjectLine}". The U.S. FTC Mail, ` +
      'Internet, or Telephone Order Merchandise Rule and any other applicable ' +
      'consumer-protection laws govern over anything stated on this page.'
    );
  }

  return (
    'This purchase is digital access and delivers immediately. Nothing is ' +
    'shipped, so no shipment date applies. You may request a full refund ' +
    `within ${offer.refund.windowDays} days, for any reason or no reason, by ` +
    `emailing ${offer.refund.contact} from the address used to place the ` +
    `order with the subject line "${offer.refund.subjectLine}". Refunds are ` +
    'processed to the original payment method. Applicable consumer-protection ' +
    'law governs over anything stated on this page.'
  );
}
