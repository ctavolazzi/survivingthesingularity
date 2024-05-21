<script>
  import Navbar from '../../components/Navbar.svelte';
  import BottomNav from '../../components/BottomNav.svelte';
  import { loadStripe } from '@stripe/stripe-js';
  import { onMount } from 'svelte';
  import { PUBLIC_STRIPE_KEY_TEST, PUBLIC_STRIPE_KEY_LIVE } from '$env/static/public';
  import Spacer from '../../components/Spacer.svelte';
  import MailchimpSignup from '../../components/MailchimpSignup.svelte';
  import { goto } from '$app/navigation';

  let stripe = null;
  let elements = null;
  let paymentElement = null;
  let clientSecret = '';
  let loading = false; // Added this line to define the 'loading' variable

  onMount(async () => {
    stripe = await loadStripe(PUBLIC_STRIPE_KEY_TEST);
    console.log('Stripe loaded:', stripe);
  });

  async function handleBuyBook() {
    console.log('handleBuyBook called');
    loading = true;

    const response = await fetch('/create-payment-intent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ amount: 2000, currency: 'usd' })
    });
    const data = await response.json();
    console.log('Payment Intent Response:', data);
    clientSecret = data.clientSecret;
    console.log('Client Secret:', clientSecret);

    // Create and mount the payment element only when clientSecret is available
    if (clientSecret) {
      elements = stripe.elements({ clientSecret });
      paymentElement = elements.create('payment');
      paymentElement.mount('#payment-element');
    }

    loading = false;
  }

  async function submitPayment(event) {
    event.preventDefault();
    console.log('submitPayment called');

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/thank-you`,
      },
    });

    if (error) {
      console.error('Payment Error:', error.message);
    } else {
      console.log('Payment successful');
      // Redirect to the thank-you page
      goto('/thank-you');
    }
  }
</script>

<Navbar />

<div class="container">
  <div class="content">
    <h1 class="title">What is this all about?</h1>
    <p class="description">
      Are you ready for a future where AI outpaces human intelligence, where your kids' tech-savvy isn't just about mastering the latest app, but surviving in a world that looks more like The Matrix and Blade Runner had a mutant baby with the Terminator?
    </p>
    <p class="description">
      This book isn't just about understanding technology; it's about preparing you and your family for the rapid changes ahead.
    </p>
    <p class="description">
      What will you do when machines can think, feel, and even outsmart us? How will you protect your family in a world where the lines between human and machine are increasingly blurred? "Surviving the Singularity" provides the insights and strategies to help you navigate the cognitive dissonance ahead as you learn to survive AND thrive in this new era.
    </p>

    <div class="button-group">
      <button class="sample-button" on:click={() => window.open('https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit?usp=sharing', '_blank')}>
        Read a Sample
      </button>
      <button class="buy-button" on:click={handleBuyBook} disabled={loading}>
        {#if loading}
          Loading...
        {:else}
          Buy the Book
        {/if}
      </button>
    </div>

    {#if clientSecret}
      <form on:submit|preventDefault={submitPayment}>
        <div id="payment-element"><!-- Payment Element will be mounted here --></div>
        <button type="submit">Pay</button>
      </form>
    {/if}


    <div class="additional-content">
      <div class="section">
        <h2 class="section-title">Our Mission</h2>
        <p class="section-description">
          Our mission is to help you understand the Singularity and its impact on our lives. Join our community of forward-thinkers, researchers, and innovators to navigate the challenges and opportunities of this rapidly changing world.
        </p>
      </div>

      <div class="section">
        <h2 class="section-title">Stay Updated</h2>
        <p class="section-description">
          Subscribe to our newsletter for regular updates, insights, and exclusive content about the technological Singularity.
        </p>
        <MailchimpSignup />
      </div>
      <p class="section-description">
        "Surviving the Singularity" is sponsored by AIECO, a humanity-focused organization.
      </p>
    </div>
  </div>
</div>

<!-- Spacer for bottom navigation -->
<Spacer height="4rem"/>

<BottomNav />

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    color: #333;
  }

  .content {
    text-align: left;
  }

  .title {
    font-size: 3rem;
    margin-bottom: 2rem;
  }

  .description {
    font-size: 1.2rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  .button-group {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .sample-button, .buy-button {
    padding: 1rem 2rem;
    background-color: #333;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1.2rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .sample-button:hover, .buy-button:hover {
    background-color: #555;
  }

  .additional-content {
    margin-top: 3rem;
  }

  .section-title {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .section-description {
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }
</style>
