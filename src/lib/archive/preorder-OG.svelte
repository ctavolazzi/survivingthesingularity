<script>
    import PreorderButton from '$lib/components/PreorderButton.svelte';
    import { onMount } from 'svelte';
    import Spacer from '$lib/components/Spacer.svelte';
    import BookCoverModal from '$lib/components/BookCoverModal.svelte';
    import CountdownTimer from '$lib/components/CountdownTimer.svelte';

    let pageTitle = "Preorder 'Surviving the Singularity'";
    let isModalOpen = false;

    // Set the offer end date to November 8th, 2024
    const offerEndDate = new Date('2024-11-08T23:59:59');

    onMount(() => {
      document.title = pageTitle;
    });
</script>

<svelte:head>
  <title>{pageTitle}</title>
  <meta name="description" content="Preorder 'Surviving the Singularity' and prepare your future for technological marvels.">
</svelte:head>

<Spacer height="50px" />

<div class="preorder-page">
  <h1 class="font-bold">{pageTitle}</h1>
  <p class="subtitle">Secure your copy and prepare for the future of AI and technology now</p>
  
  <BookCoverModal 
    isOpen={isModalOpen} 
    on:open={() => isModalOpen = true} 
    on:close={() => isModalOpen = false} 
  />
  
  <div class="cta-container">
    <PreorderButton />
  </div>
  
  <div class="lto-container">
    <CountdownTimer 
      countdownText="Pre-order Discount Ends In:" 
      endDate={offerEndDate}
    />
  </div>
  
  <div class="additional-info">
    <h2>Why Preorder?</h2>
    <ul>
      <li>Be among the first to receive the book</li>
      <li>Get exclusive early access to bonus content</li>
      <li>Support the author and the important message of the book</li>
      <li>Prepare yourself for the rapidly approaching technological singularity</li>
    </ul>
  </div>
</div>

<style>
  .preorder-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
    text-align: center;
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--text-primary);
  }

  .subtitle {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: var(--text-secondary);
  }

  .cta-container {
    margin-bottom: 1rem;
  }

  .lto-container {
    margin-bottom: 2rem;
  }

  .additional-info {
    margin-top: 3rem;
    text-align: left;
  }

  h2 {
    font-size: 1.8rem;
    margin-bottom: 1rem;
    color: var(--text-primary);
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
  }

  li::before {
    content: "✓ ";
    color: var(--text-accent);
    font-weight: bold;
    margin-right: 0.5rem;
  }

  :global(.dark) {
    --text-primary: #f7fafc;
    --text-secondary: #e2e8f0;
    --text-accent: #fbd38d;
  }
</style>