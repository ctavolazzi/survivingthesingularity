<script>
  import { browser } from '$app/environment';
  import { addToast } from '$lib/stores/toasts.js';

  let copied = false;
  let copying = false;

  async function copyPageText() {
    if (!browser || copying) return;
    copying = true;

    try {
      // Get main content, excluding nav, footer, and utility components
      const main = document.querySelector('main');
      if (!main) {
        addToast('No content found to copy', 'error');
        copying = false;
        return;
      }

      // Clone the main element to avoid modifying the DOM
      const clone = main.cloneNode(true);

      // Remove elements we don't want in the copy
      const removeSelectors = [
        'nav', 'footer', '[class*="toast"]', '[class*="cookie"]',
        '[class*="rabbit"]', '[class*="palette"]', '[class*="floating-nav"]',
        '[class*="copy-page"]', 'button', 'input', 'select', 'textarea',
        'svg', '[class*="btn"]', 'style', 'script', '[class*="loading"]'
      ];

      removeSelectors.forEach(sel => {
        clone.querySelectorAll(sel).forEach(el => el.remove());
      });

      // Get clean text
      let text = clone.textContent || '';

      // Clean up whitespace: collapse multiple newlines, trim lines
      text = text
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)
        .join('\n')
        .replace(/\n{3,}/g, '\n\n');

      // Add source attribution
      const pageTitle = document.title || 'Surviving the Singularity';
      const pageUrl = window.location.href;
      text = `--- ${pageTitle} ---\nSource: ${pageUrl}\n\n${text}\n\n---\nCopied from Surviving the Singularity (${pageUrl})`;

      await navigator.clipboard.writeText(text);

      copied = true;
      addToast('Page text copied to clipboard', 'success');

      setTimeout(() => {
        copied = false;
      }, 3000);
    } catch (err) {
      addToast('Failed to copy — try selecting text manually', 'error');
    }

    copying = false;
  }
</script>

<button
  class="copy-page-btn"
  class:copy-page-copied={copied}
  on:click={copyPageText}
  title="Copy page text to clipboard — paste into your AI chatbot"
  aria-label="Copy page text to clipboard"
>
  {#if copied}
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
    <span class="copy-label">Copied</span>
  {:else}
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
    </svg>
    <span class="copy-label">Copy for AI</span>
  {/if}
</button>

<style>
  .copy-page-btn {
    position: fixed;
    bottom: 4rem;
    right: 1rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 0.85rem;
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 10px;
    color: #64748b;
    cursor: pointer;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    z-index: 90;
    transition: all 0.2s;
    backdrop-filter: blur(8px);
    white-space: nowrap;
  }

  .copy-page-btn:hover {
    color: #f59e0b;
    border-color: rgba(245, 158, 11, 0.25);
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  }

  .copy-page-copied {
    color: #10b981;
    border-color: rgba(16, 185, 129, 0.25);
  }

  .copy-label {
    letter-spacing: 0.03em;
  }

  @media (max-width: 640px) {
    .copy-page-btn {
      bottom: 4rem;
      right: 0.5rem;
      padding: 0.45rem 0.65rem;
    }

    .copy-label {
      display: none;
    }
  }
</style>
