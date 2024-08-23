<script>
  import { marked } from 'marked';
  import sampleContent from '$lib/data/sample.md?raw';
  import ContactForm from '$lib/components/ContactForm.svelte';
  import Divider from '$lib/components/Divider.svelte';
  import StSBookImage from '$lib/images/default-blog-image.png';


  function joinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }

  function backOnKickstarter() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  const parsedContent = marked(sampleContent);
</script>

<svelte:head>
  <title>Surviving the Singularity: Sample</title>
</svelte:head>

<main class="container mx-auto px-4 py-8 max-w-3xl">
  <!-- <h1 class="text-4xl font-bold mb-8 text-center">Surviving the Singularity</h1> -->

  <img src={StSBookImage} alt="Surviving the Singularity" class="StS-book-image mb-8" />

  <h1 class="text-1xl font-bold mb-8 text-center">You are reading a sample of "Surviving the Singularity" - a workbook for processing the confusion and anxiety associated with the age of advanced AI and robotics.</h1>

  <div class="content-warning mb-8">
    <p><strong>Content Warning:</strong> Do not read this text if you have ever suffered from derealization or depersonalization.</p>
  </div>

  <div class="content">
    {@html parsedContent}
  </div>

  <Divider />

  <section class="text-center mt-16 mb-12">
    <h2 class="text-3xl font-bold mb-4">Thank you for reading!</h2>
    <p class="text-xl mb-8">If you want to support this work, please consider joining the Skool community or supporting the book on Kickstarter.</p>

    <div class="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
      <button on:click={joinSkool} class="action-button">
        Join Skool Community
      </button>
      <button on:click={backOnKickstarter} class="action-button">
        Back on Kickstarter
      </button>
    </div>
  </section>

  <Divider />

  <section class="mt-16">
    <h2 class="text-3xl font-bold mb-8 text-center">Get in Touch</h2>
    <p class="text-center mb-8">Like what you just read? If you have any questions or feedback, please contact us.</p>
    <ContactForm />
  </section>
</main>

<style>
  :global(body) {
    background-color: #f8f9fa;
    color: #333;
  }

  main {
    background-color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
  }

  .action-button {
    font-weight: bold;
    background-color: #FF9933;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.1s ease;
    font-size: 1rem;
    border-radius: 5px;
  }

  .action-button:hover {
    background-color: #FF8000;
    transform: translateY(-2px);
  }

  .content :global(h2) {
    font-size: 2rem;
    color: #333;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #FF9933;
    padding-bottom: 0.5rem;
  }

  .content :global(p) {
    margin-bottom: 1.5rem;
    line-height: 1.8;
    font-size: 1.1rem;
  }

  .content :global(h2:first-of-type) {
    margin-top: 0;
  }

  @media (max-width: 640px) {
    .content :global(h2) {
      font-size: 1.75rem;
    }

    .content :global(p) {
      font-size: 1rem;
    }

    .action-button {
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
    }
  }

  :global(.dark) body {
    background-color: #1a202c;
    color: #e2e8f0;
  }

  :global(.dark) main {
    background-color: #2d3748;
  }

  :global(.dark) .action-button {
    background-color: #FF9933;
    color: #1a202c;
  }

  :global(.dark) .action-button:hover {
    background-color: #FF8000;
  }

  :global(.dark) .content :global(h2) {
    color: #e2e8f0;
    border-bottom-color: #FF9933;
  }

  .content-warning {
    border-left: 4px solid #FF9933;
    padding: 0.5rem 1rem;
    background-color: rgba(255, 153, 51, 0.1);
    font-style: italic;
  }

  .content-warning p {
    margin: 0;
    font-size: 0.9rem;
    color: #666;
  }

  :global(.dark) .content-warning {
    background-color: rgba(255, 153, 51, 0.2);
  }

  :global(.dark) .content-warning p {
    color: #b0b0b0;
  }

  .StS-book-image {
    display: block;
    margin: 1rem auto;
    max-width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
</style>