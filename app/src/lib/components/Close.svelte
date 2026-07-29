<script>
  import { offer } from '$lib/offer.js';
  import BuyButton from './BuyButton.svelte';
</script>

<!-- No countdown, no seat counter, no "only N left". The waitlist currently
     holds 9 people. A counter reading "6 of 500 claimed" is negative social
     proof in a box with a border around it. -->
<section class="close">
  <div class="wrap wrap-narrow">
    <h2 class="close-h">
      If a robot grows your food and builds your house,<br />
      why are you renting survival?
    </h2>
    <p class="close-offer">{offer.sentence}</p>
    <BuyButton size="lg" />
  </div>
</section>

<style>
  .close {
    padding: clamp(72px, 11vw, 132px) 0;
    border-top: 1px solid var(--border);
    text-align: center;
  }
  .close-h {
    font: 600 clamp(25px, 4.4vw, 44px)/1.18 var(--serif);
    letter-spacing: -0.025em;
    margin: 0 0 24px;
    text-wrap: balance;
  }
  .close-offer {
    font-size: 17px;
    color: var(--text-2);
    max-width: 58ch;
    margin: 0 auto 32px;
  }
</style>
