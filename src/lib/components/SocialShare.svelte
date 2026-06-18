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
  function nativeShare() {
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

  // Social media share functions
  function shareOnFacebook() {
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(currentUrl)}`;
    window.open(shareUrl, '_blank', 'noopener,noreferrer');
  }

  function shareOnLinkedIn() {
    const shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(currentUrl)}`;
    window.open(shareUrl, '_blank', 'noopener,noreferrer');
  }

  function shareOnPinterest() {
    const shareUrl = `https://pinterest.com/pin/create/button/?url=${encodeURIComponent(currentUrl)}&media=${encodeURIComponent(image)}&description=${encodeURIComponent(title)}`;
    window.open(shareUrl, '_blank', 'noopener,noreferrer');
  }

  function shareOnInstagram() {
    // Instagram doesn't have a web sharing API
    // Best practice is to inform users to copy link and share manually
    alert('Instagram doesn\'t support direct sharing via web. Please copy the link and share manually.');
    copyToClipboard();
  }
</script>

<svelte:head>
  <!-- Open Graph tags for rich sharing previews -->
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={image.includes('?') ? image : `${image}?format=png`} />
  <meta property="og:url" content={currentUrl} />
  <meta property="og:type" content="article" />

  <!-- Twitter Card tags -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={image.includes('?') ? image : `${image}?format=png`} />
</svelte:head>

<div class="share-container">
  <!-- Native Share Button (visible on all devices) -->
  <button class="share-button share" on:click={nativeShare} aria-label="Share this article">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>
      <polyline points="16 6 12 2 8 6"></polyline>
      <line x1="12" y1="2" x2="12" y2="15"></line>
    </svg>
    <span>Share</span>
  </button>

  <!-- Social Media Share Buttons -->
  <div class="social-buttons">
    <!-- Facebook -->
    <button class="social-button facebook" on:click={shareOnFacebook} aria-label="Share on Facebook">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
        <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"></path>
      </svg>
    </button>

    <!-- LinkedIn -->
    <button class="social-button linkedin" on:click={shareOnLinkedIn} aria-label="Share on LinkedIn">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path>
      </svg>
    </button>

    <!-- Instagram -->
    <button class="social-button instagram" on:click={shareOnInstagram} aria-label="Share on Instagram">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
      </svg>
    </button>

    <!-- Pinterest -->
    <button class="social-button pinterest" on:click={shareOnPinterest} aria-label="Share on Pinterest">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 0C5.373 0 0 5.372 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738.098.119.112.224.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146 1.124.347 2.317.535 3.554.535 6.627 0 12-5.373 12-12 0-6.628-5.373-12-12-12z"/>
      </svg>
    </button>

    <!-- Copy Link -->
    <button class="social-button copy" on:click={copyToClipboard} aria-label="Copy Link">
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
      </svg>
    </button>
  </div>
</div>

<style>
  .share-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 0.75rem 0;
  }

  .share-button {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: transparent;
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 0.3rem 0.7rem;
    border-radius: 6px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    cursor: pointer;
    transition: color 0.15s ease, border-color 0.15s ease;
    white-space: nowrap;
  }

  .share-button:hover {
    color: #f59e0b;
    border-color: rgba(245, 158, 11, 0.35);
  }

  .social-buttons {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.25rem;
  }

  .social-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 6px;
    border: 1px solid rgba(148, 163, 184, 0.15);
    background: transparent;
    color: #475569;
    cursor: pointer;
    transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
  }

  .social-button:hover {
    color: #94a3b8;
    border-color: rgba(148, 163, 184, 0.35);
    background: rgba(148, 163, 184, 0.06);
  }

  .facebook:hover  { color: #1877F2; border-color: rgba(24, 119, 242, 0.4); }
  .linkedin:hover  { color: #0A66C2; border-color: rgba(10, 102, 194, 0.4); }
  .instagram:hover { color: #e6683c; border-color: rgba(230, 104, 60, 0.4); }
  .pinterest:hover { color: #E60023; border-color: rgba(230, 0, 35, 0.4); }
  .copy:hover      { color: #94a3b8; border-color: rgba(148, 163, 184, 0.4); }
</style>