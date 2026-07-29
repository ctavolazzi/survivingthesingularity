<script>
  import { offer } from '$lib/offer.js';
  import BuyButton from './BuyButton.svelte';
</script>

<section class="band band-alt" id="offer">
  <div class="wrap wrap-narrow">
    <p class="kicker">The offer</p>
    <h2 class="sec-h2">What five dollars buys.</h2>

    <ul class="incl" aria-label="Included">
      {#each offer.included as item}
        <li>
          <span class="tick" aria-hidden="true"></span>
          <div><b>{item.title}</b> {item.detail}</div>
        </li>
      {/each}
    </ul>

    <!-- Same table, same size, same weight. Saying plainly what five dollars
         does not buy is worth more trust than any adjective above it. -->
    <ul class="excl" aria-label="Not included">
      {#each offer.excluded as item}
        <li>
          <span class="cross" aria-hidden="true"></span>
          <div><b>{item.title}</b> {item.detail}</div>
        </li>
      {/each}
    </ul>

    <div class="scope">
      <p class="scope-h">What "forever" actually means</p>
      <p>{offer.foreverScope}</p>
      <p class="scope-link">
        The refund terms derive from this same offer.
        <a href="/policies">Read the policy</a>.
      </p>
    </div>

    <div class="offer-cta"><BuyButton size="lg" /></div>
  </div>
</section>

<style>
  .incl,
  .excl {
    list-style: none;
    margin: 0 0 14px;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: var(--r);
    overflow: hidden;
  }
  .excl { margin-bottom: 32px; }

  .incl li,
  .excl li {
    background: var(--bg);
    padding: 18px 20px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
    font-size: 16px;
    color: var(--text-2);
  }
  .excl li { background: var(--surface-2); }

  .incl b,
  .excl b {
    color: var(--text);
    font-weight: 600;
    display: block;
    margin-bottom: 2px;
  }

  .tick,
  .cross {
    flex: 0 0 auto;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin-top: 2px;
    position: relative;
  }
  .tick { background: rgba(74, 222, 128, 0.14); }
  .tick::after {
    content: '';
    position: absolute;
    left: 6px;
    top: 4px;
    width: 5px;
    height: 10px;
    border: solid var(--ok);
    border-width: 0 2px 2px 0;
    transform: rotate(42deg);
  }
  .cross { background: var(--surface-3); }
  .cross::before,
  .cross::after {
    content: '';
    position: absolute;
    left: 5px;
    top: 9px;
    width: 10px;
    height: 2px;
    background: var(--no);
  }
  .cross::before { transform: rotate(45deg); }
  .cross::after { transform: rotate(-45deg); }

  .scope {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--border-2);
    border-radius: 0 var(--r) var(--r) 0;
    padding: 20px 22px;
    margin-bottom: 32px;
  }
  .scope-h {
    font: 600 13px/1 var(--mono);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-3);
    margin: 0 0 12px;
  }
  .scope p {
    font-size: 15.5px;
    line-height: 1.7;
    color: var(--text-2);
    margin: 0;
  }
  .scope p.scope-link {
    margin-top: 12px;
    font-size: 14px;
    color: var(--text-3);
  }
  .scope a { color: var(--accent); }

  .offer-cta { display: flex; justify-content: flex-start; }
</style>
