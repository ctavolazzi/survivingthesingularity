<script>
  import ContactForm from '$lib/components/ContactForm.svelte';
  import { fade, fly } from 'svelte/transition';
  import { onMount } from 'svelte';


  let navbarHeight = 0;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
  });
</script>

<svelte:head>
  <title>Contact | Surviving the Singularity</title>
</svelte:head>

<div class="main-content" style="padding-top: {navbarHeight}px">
  <h1 class="text-4xl font-bold mb-4 text-center" in:fly="{{ y: -50, duration: 1000 }}">Get in Touch</h1>
  <p class="subheadline" in:fade="{{ delay: 500, duration: 800 }}">We're here to listen, help, and connect</p>

  <div class="content-wrapper">
    <div class="form-container" in:fly="{{ x: -50, duration: 1000 }}">
      <h2>Send Us a Message</h2>
      <ContactForm />
    </div>

    <div class="info-container" in:fly="{{ x: 50, duration: 1000 }}">
      <h2>Why Reach Out?</h2>
      <ul class="contact-reasons">
        <li class="contact-reason">
          <span class="icon">📝</span>
          <div class="reason-content">
            <h3>Share your thoughts or feedback</h3>
            <p>We value your insights and opinions about our content, services, or any aspect of our platform.</p>
          </div>
        </li>
        <li class="contact-reason">
          <span class="icon">❓</span>
          <div class="reason-content">
            <h3>Ask us anything</h3>
            <p>Have questions about AI, the singularity, or our resources? We're happy to help clarify and provide information.</p>
          </div>
        </li>
        <li class="contact-reason">
          <span class="icon">💡</span>
          <div class="reason-content">
            <h3>Propose ideas or collaborations</h3>
            <p>Have a great idea or interested in working together? We're open to innovative partnerships and suggestions.</p>
          </div>
        </li>
        <li class="contact-reason">
          <span class="icon">🤝</span>
          <div class="reason-content">
            <h3>Connect with our team</h3>
            <p>Reach out to learn more about who we are and what we do. We're always happy to connect with like-minded individuals.</p>
          </div>
        </li>
        <li class="contact-reason">
          <span class="icon">🆘</span>
          <div class="reason-content">
            <h3>Get support or assistance</h3>
            <p>Need help with something specific? Let us know how we can assist you with our resources or services.</p>
          </div>
        </li>
      </ul>
    </div>
  </div>

  <div class="privacy-notice" in:fade={{ duration: 300, delay: 800 }}>
    We respect your privacy and only use your information to respond to your message.
  </div>
</div>

<style>
  .main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    transition: padding-top 0.3s ease-in-out;
    position: relative;
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

  .contact-reasons {
    list-style-type: none;
    padding: 0;
  }

  .contact-reason {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1.5rem;
    padding: 0;
    position: relative;
  }

  .icon {
    font-size: 1.5rem;
    margin-right: 1rem;
    flex-shrink: 0;
  }

  .reason-content {
    flex: 1;
  }

  .reason-content h3 {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--color-text-primary);
  }

  .reason-content p {
    font-size: 0.95rem;
    color: var(--color-text-secondary);
    line-height: 1.4;
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

  .privacy-notice {
    text-align: center;
    margin-top: 2rem;
    font-size: 0.7rem;
    color: var(--color-text-secondary);
    opacity: 0.6;
    letter-spacing: 0.02em;
  }

  .privacy-notice a {
    color: var(--color-accent);
    text-decoration: none;
    transition: all 0.2s ease;
    opacity: 0.7;
  }

  .privacy-notice a:hover {
    opacity: 1;
    text-decoration: underline;
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
  :global(.dark) .response-time {
    color: var(--color-text-primary-dark);
  }

  :global(.dark) .subheadline,
  :global(.dark) li,
  :global(.dark) .privacy-notice {
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

    .privacy-notice {
      font-size: 0.65rem;
      margin-top: 1.5rem;
    }
  }
</style>