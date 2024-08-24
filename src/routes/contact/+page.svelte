<script>
  import ContactForm from '$lib/components/ContactForm.svelte';

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }
</script>

<div class="outer-container">
  <div class="content-container">
    <h1>Get in Touch</h1>
    <p>We're here to help and answer any questions you might have. Please use the form below to get in touch with us.</p>
    <p>Your privacy is important to us. We will never share or sell your information.</p>
    
    <div class="form-wrapper">
      <ContactForm />
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
  </div>
</div>

<style>
  .outer-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    padding-top: 2rem;
  }

  .content-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem;
    width: 100%;
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    color: var(--color-text-primary);
    text-align: center;
    font-weight: 700;
  }

  h2 {
    font-size: 1.75rem;
    margin-top: 2.5rem;
    margin-bottom: 1.25rem;
    color: var(--color-text-primary);
  }

  p, li {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
    line-height: 1.6;
  }

  .form-wrapper {
    margin: 2.5rem 0;
  }

  ul {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin-bottom: 1.5rem;
  }

  li {
    margin-bottom: 0.75rem;
  }

  button {
    display: block;
    width: 100%;
    font-weight: bold;
    font-size: 1.25rem;
    background-color: var(--color-bg-secondary);
    border: 2px solid var(--color-text-primary);
    border-radius: 8px;
    padding: 1rem 0.5rem;
    margin-top: 2.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease, transform 0.3s ease;
    text-align: center;
    color: var(--color-text-primary);
  }

  button:hover {
    background-color: var(--color-bg-primary);
    color: var(--color-text-secondary);
    transform: translateY(-2px);
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 2rem;
    }

    h2 {
      font-size: 1.5rem;
    }

    button {
      font-size: 1.1rem;
    }
  }
</style>