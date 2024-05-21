<script context="module">
  export async function load({ url }) {
    const sessionId = url.searchParams.get('session_id');
    return { sessionId };
  }
</script>

<script>
  import { onMount } from 'svelte';
  export let sessionId;

  // Logic to verify the session and provide the download link
  let downloadLink = '';

  async function verifyPayment() {
    const response = await fetch(`/verify-payment?session_id=${sessionId}`);
    if (response.ok) {
      const { link } = await response.json();
      downloadLink = link;
    } else {
      console.error('Failed to verify payment');
    }
  }

  onMount(verifyPayment);
</script>

<div class="thank-you">
  <h1>Thank You for Your Purchase!</h1>
  {#if downloadLink}
    <a href={downloadLink} download="Surviving_the_Singularity.pdf">Download Your Book</a>
  {/if}
</div>

<style>
  .thank-you {
    text-align: center;
    margin-top: 2rem;
  }

  a {
    display: inline-block;
    margin-top: 1rem;
    padding: 1rem 2rem;
    background-color: #333;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s ease;
  }

  a:hover {
    background-color: #555;
  }
</style>


