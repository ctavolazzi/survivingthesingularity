<script>
  export let url = '';
  export let title = '';
  export let description = '';
  export let image = '';

  // Get current URL if not provided
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  let currentUrl = '';
  let shareSupported = false;

  onMount(() => {
    // Use provided URL or get current URL from browser
    currentUrl = url || window.location.href;

    // Check if Web Share API is supported
    shareSupported = !!navigator.share;
  });

  // Share function using Web Share API
  function share() {
    if (navigator.share) {
      navigator.share({
        title: title,
        text: description,
        url: currentUrl,
      })
      .catch((error) => console.error('Error sharing:', error));
    } else {
      // Fallback - copy to clipboard
      copyToClipboard();
    }
  }

  function copyToClipboard() {
    navigator.clipboard.writeText(currentUrl)
      .then(() => {
        alert('Link copied to clipboard!');
      })
      .catch(err => {
        console.error('Failed to copy: ', err);
      });
  }
</script>

<svelte:head>
  <!-- Open Graph tags for rich sharing previews -->
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={image} />
  <meta property="og:url" content={currentUrl} />
  <meta property="og:type" content="article" />

  <!-- Twitter Card tags -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={image} />
</svelte:head>

<div class="share-container">
  <button class="share-button" on:click={share} aria-label="Share this article">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>
      <polyline points="16 6 12 2 8 6"></polyline>
      <line x1="12" y1="2" x2="12" y2="15"></line>
    </svg>
    <span>Share</span>
  </button>
</div>

<style>
  .share-container {
    display: flex;
    margin: 1rem 0;
  }

  .share-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background-color: var(--color-primary, #f97316);
    color: white;
    font-weight: 500;
    padding: 0.5rem 1.25rem;
    border-radius: 0.375rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    font-size: 0.95rem;
  }

  .share-button:hover {
    background-color: var(--color-primary-dark, #ea580c);
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Dark mode adjustment */
  :global(.dark) .share-button {
    background-color: var(--color-primary-dark, #f97316);
  }

  :global(.dark) .share-button:hover {
    background-color: var(--color-primary-hover-dark, #ea580c);
  }

  /* Responsive design */
  @media (max-width: 640px) {
    .share-button {
      font-size: 0.9rem;
      padding: 0.5rem 1rem;
    }
  }
</style>