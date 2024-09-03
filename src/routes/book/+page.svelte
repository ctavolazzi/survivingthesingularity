<script>
  import { fade } from 'svelte/transition';
  import TableOfContents from '$lib/components/TableOfContents.svelte';
  import coverImage from '$lib/images/Surviving-the-Singularity-Cover.png';

  export let data;
</script>

<svelte:head>
  <title>Surviving the Singularity - Book Preview</title>
  <meta name="description" content="Preview the first draft of 'Surviving the Singularity' and join our community of future-ready individuals.">
</svelte:head>

<section class="book-cover">
  <img src={coverImage} alt="Surviving the Singularity Book Cover" loading="eager">
</section>

<section class="disclaimer" in:fade="{{ duration: 1000, delay: 600 }}">
  <h1>First Draft Disclaimer</h1>
  <p>
    Welcome, brave explorer of the future! You're about to dive into the raw, unfiltered first draft of "Surviving the Singularity." 
    This version is offered on a trial, as-is basis. Expect typos, plot holes, and remember:
  </p>
  <p class="text-center"><strong>If any of the jokes don't compute, I didn't write them. All the unfunny jokes were AI generated 👍</strong></p>
  <p>
    Your feedback is crucial for our survival! If you spot any glitches in the matrix (or just have thoughts to share), 
    please transmit a signal to <a href="https://solo.to/thecoffeejesus" target="_blank" rel="noopener noreferrer">@thecoffeejesus</a> on any social media platform.
  </p>
  <p>Together, we can make this book as singularity-proof as possible!</p>
</section>

<section class="table-of-contents">
  <h2>Table of Contents</h2>
  <TableOfContents sections={data.book.sections} />
</section>

<style>
  .book-cover {
    text-align: center;
    margin-bottom: 3rem;
  }

  .book-cover img {
    max-width: 100%;
    height: auto;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
  }

  .disclaimer {
    background-color: #ffffff;
    border-left: 4px solid #ff7708;
    padding: 1.5rem;
    margin-bottom: 3rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 0.5rem;
  }

  .disclaimer h1 {
    font-family: 'Orbitron', sans-serif;
    color: #ff7708;
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }

  .disclaimer p {
    margin-bottom: 1rem;
    line-height: 1.6;
  }

  .disclaimer a {
    color: #ff7708;
    text-decoration: none;
    font-weight: bold;
    transition: all 0.3s ease;
  }

  .disclaimer a:hover {
    color: #ff9933;
    text-decoration: underline;
  }

  h2 {
    font-family: 'Orbitron', sans-serif;
    color: #ff7708;
    margin-bottom: 1rem;
    font-size: 1.3rem;
  }

  /* Dark mode styles */
  :global(.dark) .disclaimer {
    background-color: #2d3748;
    border-left-color: #ff9933;
  }

  :global(.dark) .disclaimer h1,
  :global(.dark) h2 {
    color: #ff9933;
  }

  :global(.dark) .disclaimer a {
    color: #ff9933;
  }

  :global(.dark) .disclaimer a:hover {
    color: #ffb366;
  }
</style>
