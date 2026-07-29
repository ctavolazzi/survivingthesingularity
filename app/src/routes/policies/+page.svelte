<script>
  import { offer, refundClause } from '$lib/offer.js';

  // Nothing on this page restates the offer in prose. Every clause below reads
  // from the same frozen object the hero and the offer table read from.
  //
  // This is the demonstration. On the live site, the sales pages say $5 buys
  // access and a discount, while this page says a refund is available "prior to
  // shipment" under the FTC Merchandise Rule. Two surfaces, two different
  // transactions, because each one carried its own prose copy of the offer.
  //
  // Flip `shipsPhysicalGoods` in src/lib/offer.js and watch the shipment
  // language appear here and the excluded row change on the homepage, together,
  // from one edit.
</script>

<svelte:head>
  <title>Policies · Surviving the Singularity</title>
</svelte:head>

<section class="band">
  <div class="wrap wrap-narrow">
    <p class="kicker">Policies</p>
    <h1 class="sec-h2">What you bought, and how to get your money back.</h1>

    <div class="derived-flag">
      Every clause on this page is generated from the same offer object the
      sales pages use. It cannot drift from them.
    </div>

    <h2 class="h" id="what">What this purchase is</h2>
    <p>{offer.sentence}</p>

    <h3 class="h3">Included</h3>
    <ul class="plain">
      {#each offer.included as item}
        <li><b>{item.title}</b> {item.detail}</li>
      {/each}
    </ul>

    <h3 class="h3">Not included</h3>
    <ul class="plain">
      {#each offer.excluded as item}
        <li><b>{item.title}</b> {item.detail}</li>
      {/each}
    </ul>

    <h2 class="h" id="refunds">Refunds</h2>
    <p>{refundClause()}</p>

    {#if !offer.shipsPhysicalGoods}
      <p class="aside">
        This offer ships no physical goods, so no shipment date applies and the
        thirty day merchandise clock never starts. If that ever changes, this
        paragraph changes with it, automatically.
      </p>
    {/if}

    <h2 class="h" id="terms">The scope of "forever"</h2>
    <p>{offer.foreverScope}</p>

    <p class="back"><a href="/">Back to the site</a></p>
  </div>
</section>

<style>
  .derived-flag {
    background: var(--accent-dim);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: var(--r);
    padding: 14px 18px;
    font: 400 13.5px/1.55 var(--mono);
    color: var(--accent-hi);
    margin: 0 0 40px;
  }

  .h {
    font: 600 22px/1.25 var(--serif);
    letter-spacing: -0.01em;
    margin: 40px 0 14px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
  }
  .h3 {
    font: 600 13px/1 var(--mono);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-3);
    margin: 26px 0 12px;
  }

  p {
    font-size: 16.5px;
    line-height: 1.72;
    color: var(--text-2);
    max-width: 70ch;
    margin: 0 0 16px;
  }

  .aside {
    border-left: 3px solid var(--border-2);
    background: var(--surface-2);
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    font-size: 15px;
    color: var(--text-3);
  }

  .plain {
    list-style: none;
    margin: 0 0 8px;
    padding: 0;
  }
  .plain li {
    font-size: 16px;
    line-height: 1.65;
    color: var(--text-2);
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    max-width: 70ch;
  }
  .plain b { color: var(--text); display: block; }

  .back { margin-top: 40px; }
  .back a { color: var(--accent); }
</style>
