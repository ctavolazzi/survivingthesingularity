<script>
  import Spacer from '$lib/components/Spacer.svelte';
  import { onMount } from 'svelte';

  let navbarHeight = 0;
  let iframeHeight = 800;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
    
    // Add event listener for iframe messages
    window.addEventListener('message', (event) => {
      if (event.data.type === 'resize') {
        iframeHeight = event.data.height;
      }
    });
  });

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }
</script>

<div class="outer-container" style="padding-top: {navbarHeight}px">
  <div class="content-container">
    <h1>Get in touch:</h1>
    <p>We're here to help and answer any questions you might have. Please use the Mailchimp form below to get in touch with us.</p>
    <p>Your privacy is important to us. We will never share or sell your information.</p>
    
    <div class="form-wrapper">
      <iframe src="https://us19.list-manage.com/contact-form?u=79a060ac083c62360805246c1&form_id=c4630b003308d7c72c1d0479c30c9a64" title="Mailchimp contact form" style="height: {iframeHeight}px;"></iframe>
    </div>

    <div class="additional-info">
      <h2>Here are a few reasons you might want to reach out:</h2>
      <ul>
        <li>Questions about the book</li>
        <li>Questions about our projects or services</li>
        <li>Inquiries about collaborations or partnerships</li>
        <li>Feedback or suggestions</li>
      </ul>
      <p>Once you submit the form, we will get back to you as soon as possible.</p>
    </div>

    <button on:click={handleBackBook}>Back the Book on Kickstarter</button>
  </div>
</div>

<style>
  :global(body) {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: var(--color-text-primary);
    background-color: var(--color-bg-primary);
  }

  .outer-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    transition: padding-top 0.3s ease-in-out;
  }

  .content-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
    width: 100%;
  }

  .spacer-text {
    font-size: 1.5rem;
    font-weight: bold;
    background-color: var(--color-bg-secondary);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }

  h2 {
    font-size: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
  }

  p, li {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
  }

  .form-wrapper {
    margin: 2rem 0;
  }

  iframe {
    width: 100%;
    border: none;
    overflow: hidden;
  }

  ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 1rem;
  }

  li {
    margin-bottom: 0.5rem;
  }

  button {
    display: block;
    width: 100%;
    font-weight: bold;
    font-size: 1.25rem;
    background-color: var(--color-bg-secondary);
    border: 2px solid var(--color-text-primary);
    border-radius: 4px;
    padding: 1rem 0.5rem;
    margin-top: 2rem;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
    text-align: center;
    color: var(--color-text-primary);
  }

  button:hover {
    background-color: var(--color-bg-primary);
    color: var(--color-text-secondary);
  }
</style>