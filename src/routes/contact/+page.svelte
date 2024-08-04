<script>
  // import BottomNav from '../../components/BottomNav.svelte';
  function handleBackBook() {
    window.location.href = 'https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook';
  }
</script>

<div class="outer-container flex flex-col min-h-screen">
  <div class="form-wrapper flex-grow flex justify-center items-center p-0">
    <iframe src="https://us19.list-manage.com/contact-form?u=79a060ac083c62360805246c1&form_id=c4630b003308d7c72c1d0479c30c9a64" class="w-full h-full" style="border:0; height: 950px; overflow:hidden;" title="Mailchimp contact form"></iframe>
  </div>
</div>

<!-- Add the title and description inside the container for better alignment -->
<!-- Add the title and description inside the container for better alignment -->
<div class="text-container text-center p-4">
  <h1 class="form-title text-2xl font-semibold mb-6">Get in touch:</h1>
  <p>We're here to help and answer any questions you might have. Please use the Mailchimp form above to get in touch with us.</p>
  <p>Your privacy is important to us. We will never share or sell your information.</p>
  <br>
  <p><strong>Here are a few reasons you might want to reach out:</strong></p>
  <br>
  <ul class="list-disc list-inside text-left mb-6">
    <li>Questions about the book</li>
    <li>Questions about our projects or services</li>
    <li>Inquiries about collaborations or partnerships</li>
    <li>Feedback or suggestions</li>
  </ul>
  <p>Once you submit the form, we will get back to you as soon as possible.</p>
  <button class="buy-button block w-full mt-4" on:click={handleBackBook}>Back the Book on Kickstarter</button>
</div>

<!-- <BottomNav /> -->

<style>
  .outer-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .form-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-grow: 1;
    padding: 0;
    width: 100%;
    height: 100%;
  }

  iframe {
    width: 100%;
    height: 100%;
    min-height: 100vh; /* Ensure minimum height fills the viewport */
    border: none; /* Remove border */
    overflow: hidden; /* Hide overflow */
  }

  .text-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-top: 1rem;
  }

  .form-title {
    margin-bottom: 1rem;
  }

	.buy-button {
      font-weight: bold;
	    font-size: 1.5rem;
      background-color: #f8f9fa;
      border: 2px solid #000000;
      border-radius: 4px;
      padding: 1rem 1rem;
      cursor: pointer;
      transition: background-color 0.3s ease;
      text-align: center;
    }

    .buy-button:hover {
      background-color: #e2e6ea;
    }
</style>
