<script>
  import { fade, fly } from 'svelte/transition';
  import { elasticOut } from 'svelte/easing';
  import NewsletterSection from '../NewsletterSection.svelte';
  import { darkMode } from '$lib/stores/darkMode';

  export let metadata = {
    title: '',
    date: '',
    edition: '',
    description: ''
  };
</script>

<!-- This is a template for creating newsletter editions using the modular component approach -->
<!-- When creating a new newsletter, copy this file and customize the content -->

<div class="newsletter" class:dark={$darkMode}>
  <!-- Header Section -->
  <header class="newsletter-header" in:fly={{ y: 20, duration: 500, easing: elasticOut }}>
    <div class="edition-badge">Edition #{metadata.edition}</div>
    <h1>{metadata.title}</h1>
    <div class="metadata">
      <time datetime={metadata.date}>{new Date(metadata.date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })}</time>
      <div class="reading-time">~10 min read</div>
    </div>
    <p class="intro">
      {metadata.description || 'Welcome to this edition of the Surviving the Singularity newsletter.'}
    </p>
  </header>

  <!-- Table of Contents -->
  <nav class="table-of-contents" in:fade={{ duration: 300, delay: 200 }}>
    <h2>In This Edition</h2>
    <ul>
      <li><a href="#this-week">This Week in AI</a></li>
      <li><a href="#main-topic">Main Topic</a></li>
      <li><a href="#resources">Resources & Tools</a></li>
      <li><a href="#community">Community Spotlight</a></li>
      <li><a href="#tip">Practical Tip</a></li>
    </ul>
  </nav>

  <!-- Main Content -->
  <div class="content" in:fade={{ duration: 300, delay: 400 }}>
    <slot></slot>
  </div>

  <!-- Social Share -->
  <div class="social-share" in:fade={{ duration: 300, delay: 500 }}>
    <h3>Share this newsletter</h3>
    <div class="share-buttons">
      <button class="share-button twitter">
        <span class="icon">𝕏</span>
        Share on X
      </button>
      <button class="share-button linkedin">
        <span class="icon">in</span>
        Share on LinkedIn
      </button>
    </div>
  </div>

  <!-- Footer -->
  <footer class="newsletter-footer" in:fade={{ duration: 300, delay: 600 }}>
    <div class="footer-content">
      <div class="author">
        <img src="/images/avatar.jpg" alt="Author" class="author-avatar" />
        <div class="author-info">
          <span class="author-name">Christopher Tavolazzi</span>
          <span class="author-title">Chief Singularity Survivalist</span>
        </div>
      </div>
      <div class="newsletter-cta">
        <h3>Stay Updated</h3>
        <p>Get weekly insights on thriving in the age of AI.</p>
        <slot name="newsletter-signup"></slot>
      </div>
    </div>
  </footer>
</div>

<style>
  .newsletter {
    --primary-color: #3b82f6;
    --secondary-color: #9333ea;
    --text-primary: #1a1a1a;
    --text-secondary: #4b5563;
    --bg-primary: #ffffff;
    --bg-secondary: #f9fafb;
    --border-color: #e5e7eb;

    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    font-family: system-ui, -apple-system, sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
  }

  .newsletter.dark {
    --text-primary: #f3f4f6;
    --text-secondary: #9ca3af;
    --bg-primary: #111827;
    --bg-secondary: #1f2937;
    --border-color: #374151;
  }

  .newsletter-header {
    text-align: center;
    margin-bottom: 3rem;
  }

  .edition-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border-radius: 9999px;
    font-weight: 600;
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  h1 {
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1.2;
    margin: 0 0 1rem 0;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.025em;
  }

  .metadata {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
  }

  .reading-time {
    display: flex;
    align-items: center;
  }

  .reading-time::before {
    content: "•";
    margin-right: 1rem;
  }

  .intro {
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 42rem;
    margin: 0 auto;
  }

  .table-of-contents {
    background: var(--bg-secondary);
    border-radius: 1rem;
    padding: 1.5rem 2rem;
    margin-bottom: 3rem;
  }

  .table-of-contents h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text-primary);
  }

  .table-of-contents ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .table-of-contents a {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.875rem;
    transition: all 0.2s ease;
  }

  .table-of-contents a:hover {
    color: var(--primary-color);
  }

  .social-share {
    margin: 3rem 0;
    text-align: center;
  }

  .social-share h3 {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text-primary);
  }

  .share-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }

  .share-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: 1px solid var(--border-color);
    border-radius: 9999px;
    background: var(--bg-primary);
    color: var(--text-primary);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .share-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .newsletter-footer {
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
  }

  .footer-content {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 2rem;
    align-items: start;
  }

  .author {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .author-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
  }

  .author-info {
    display: flex;
    flex-direction: column;
  }

  .author-name {
    font-weight: 600;
    color: var(--text-primary);
  }

  .author-title {
    font-size: 0.875rem;
    color: var(--text-secondary);
  }

  .newsletter-cta {
    background: var(--bg-secondary);
    padding: 1.5rem;
    border-radius: 1rem;
  }

  .newsletter-cta h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
  }

  .newsletter-cta p {
    color: var(--text-secondary);
    margin-bottom: 1rem;
  }

  @media (max-width: 768px) {
    .newsletter {
      padding: 1.5rem;
    }

    h1 {
      font-size: 2rem;
    }

    .footer-content {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    .table-of-contents ul {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 480px) {
    .newsletter {
      padding: 1rem;
    }

    h1 {
      font-size: 1.75rem;
    }

    .metadata {
      flex-direction: column;
      gap: 0.5rem;
    }

    .reading-time::before {
      display: none;
    }

    .share-buttons {
      flex-direction: column;
    }
  }
</style>
