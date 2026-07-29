<script>
  import { say } from '$lib/toast.svelte.js';
  import { offer } from '$lib/offer.js';

  /** @type {{ size?: 'sm' | 'md' | 'lg', class?: string }} */
  let { size = 'md', class: extra = '' } = $props();

  // Deliberately inert. Wiring a demo build to a real Stripe key is how test
  // charges end up in a real ledger, so this says what it is and stops.
  function onclick() {
    say(
      `Demo build. Checkout is not wired, on purpose. In production this opens Stripe at ${offer.price}.00.`
    );
  }
</script>

<button
  class="btn btn-primary {size === 'sm' ? 'btn-sm' : ''} {size === 'lg' ? 'btn-lg' : ''} {extra}"
  {onclick}
>
  Get in for {offer.price}
</button>
