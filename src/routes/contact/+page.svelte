<script>
  import ContactForm from '$lib/components/ContactForm.svelte';
  import { fade, fly } from 'svelte/transition';
  import { onMount } from 'svelte';

  let navbarHeight = 0;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
  });
</script>

<div class="main-content" style="padding-top: {navbarHeight}px">
  <h1 in:fly="{{ y: -50, duration: 1000 }}">Get in Touch</h1>
  <p class="subheadline" in:fade="{{ delay: 500, duration: 800 }}">We're here to listen, help, and connect</p>
  
  <div class="content-wrapper">
    <div class="form-container" in:fly="{{ x: -50, duration: 1000 }}">
      <h2>Send Us a Message</h2>
      <ContactForm />
    </div>
    
    <div class="info-container" in:fly="{{ x: 50, duration: 1000 }}">
      <h2>Why Reach Out?</h2>
      <ul>
        <li>📝 Share your thoughts or feedback</li>
        <li>❓ Ask us anything</li>
        <li>💡 Propose ideas or collaborations</li>
        <li>🤝 Connect with our team</li>
        <li>🆘 Get support or assistance</li>
      </ul>
      <p class="response-time">We aim to respond to all messages within 1 business day.</p>
    </div>
  </div>

  <div class="privacy-note">
    <h3>Your Privacy Matters</h3>
    <p>We respect your privacy and will only use your information to respond to your message. For more details, please see our Privacy Policy.</p>
  </div>
</div>

<style>
  .main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    transition: padding-top 0.3s ease-in-out;
  }

  h1 {
    font-size: 3rem;
    text-align: center;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
  }

  .subheadline {
    font-size: 1.5rem;
    text-align: center;
    margin-bottom: 2rem;
    opacity: 0.8;
    color: var(--color-text-secondary);
  }

  .content-wrapper {
    display: flex;
    gap: 2rem;
  }

  .form-container, .info-container {
    flex: 1;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    background-color: var(--color-bg-secondary);
  }

  h2 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid var(--color-border);
    padding-bottom: 0.5rem;
    color: var(--color-text-primary);
  }

  ul {
    list-style-type: none;
    padding-left: 0;
  }

  li {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    padding-left: 2rem;
    position: relative;
    color: var(--color-text-secondary);
  }

  li::before {
    content: attr(data-icon);
    position: absolute;
    left: 0;
    font-size: 1.5rem;
  }

  .response-time {
    font-weight: bold;
    margin: 1.5rem 0;
    font-size: 1.1rem;
    text-align: center;
    background: var(--color-bg-accent);
    padding: 0.8rem;
    border-radius: 8px;
    color: var(--color-text-primary);
  }

  .privacy-note {
    text-align: center;
    margin-top: 2rem;
    padding: 1rem;
    background-color: var(--color-bg-accent);
    border-radius: 8px;
  }

  .privacy-note h3 {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
    color: var(--color-text-primary);
  }

  .privacy-note p {
    color: var(--color-text-secondary);
  }

  /* Dark mode styles */
  :global(.dark) .main-content {
    background-color: var(--color-bg-primary);
  }

  :global(.dark) .form-container,
  :global(.dark) .info-container {
    background-color: var(--color-bg-secondary);
  }

  :global(.dark) h1,
  :global(.dark) h2,
  :global(.dark) .response-time,
  :global(.dark) .privacy-note h3 {
    color: var(--color-text-primary-dark);
  }

  :global(.dark) .subheadline,
  :global(.dark) li,
  :global(.dark) .privacy-note p {
    color: var(--color-text-secondary-dark);
  }

  /* Responsive styles */
  @media (max-width: 768px) {
    .content-wrapper {
      flex-direction: column;
    }

    h1 {
      font-size: 2.5rem;
    }

    .subheadline {
      font-size: 1.2rem;
    }

    h2 {
      font-size: 1.8rem;
    }
  }
</style>