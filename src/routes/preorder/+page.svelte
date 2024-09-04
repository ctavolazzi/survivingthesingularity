<script>
    import PreorderButton from '$lib/components/PreorderButton.svelte';
    import { onMount } from 'svelte';
    import Spacer from '$lib/components/Spacer.svelte';
  
    let pageTitle = "Preorder 'Surviving the Singularity'";
  
    onMount(() => {
      document.title = pageTitle;
    });
</script>

<svelte:head>
  <title>{pageTitle}</title>
  <meta name="description" content="Preorder 'Surviving the Singularity' and prepare for the future of AI and technology.">
</svelte:head>

<Spacer height="50px" />

<div class="preorder-page">
  <h1>{pageTitle}</h1>
  <p class="subtitle">Secure your copy and prepare for the future of AI and technology</p>
  
  <PreorderButton />
  
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

  /* These variables should match your global CSS */
  :global(:root) {
    --text-primary: #2d3748;
    --text-secondary: #4a5568;
    --text-accent: #ed8936;
  }

  :global(.dark) {
    --text-primary: #f7fafc;
    --text-secondary: #e2e8f0;
    --text-accent: #fbd38d;
  }
</style>