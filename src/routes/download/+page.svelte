<script>
  import { onMount } from 'svelte';
  let isDownloading = false;
  let isDarkMode = false;

  onMount(() => {
    isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  async function downloadSamplePDF() {
    isDownloading = true;
    const pdfUrl = '/Singularity-checklist.pdf';
    const link = document.createElement('a');
    link.href = pdfUrl;
    link.download = 'Singularity-checklist.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate download time
    isDownloading = false;
  }
</script>

<div class="outer-container" class:dark-mode={isDarkMode}>
  <main class="content-container">
    <h1>Download Singularity Checklist</h1>
    <p>Click the button below to download our free Singularity Checklist PDF.</p>
    <button on:click={downloadSamplePDF} class="cta-button" class:downloading={isDownloading} disabled={isDownloading}>
      <span class="button-text">{isDownloading ? 'Downloading...' : 'Download Checklist PDF'}</span>
      <span class="button-icon">{isDownloading ? '⟳' : '↓'}</span>
      <div class="button-flash"></div>
    </button>
  </main>
</div>

<style>
  .outer-container {
    --color-bg-primary: #ffffff;
    --color-bg-secondary: #f0f0f0;
    --color-text-primary: #333333;
    --color-text-secondary: #666666;
    --color-accent: #3498db;
    --color-accent-hover: #2980b9;
    --color-flash: rgba(52, 152, 219, 0.3);
  }

  .dark-mode {
    --color-bg-primary: #2c3e50;
    --color-bg-secondary: #34495e;
    --color-text-primary: #ecf0f1;
    --color-text-secondary: #bdc3c7;
    --color-accent: #3498db;
    --color-accent-hover: #2980b9;
    --color-flash: rgba(52, 152, 219, 0.3);
  }

  .content-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    text-align: center;
    background-color: var(--color-bg-primary);
    color: var(--color-text-primary);
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--color-accent);
  }

  p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    color: var(--color-text-secondary);
  }

  .cta-button {
    position: relative;
    background-color: var(--color-accent);
    border: none;
    padding: 12px 24px;
    color: var(--color-bg-primary);
    font-size: 1.1rem;
    font-weight: bold;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.3s ease;
    overflow: hidden;
    border-radius: 5px;
  }

  .cta-button:hover {
    background-color: var(--color-accent-hover);
  }

  .button-text, .button-icon {
    position: relative;
    z-index: 2;
  }

  .button-icon {
    margin-left: 10px;
    font-size: 1.2rem;
  }

  .downloading .button-icon {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    100% { transform: rotate(360deg); }
  }

  .button-flash {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, var(--color-flash) 0%, transparent 70%);
    transform: scale(0);
    opacity: 0;
    z-index: 1;
  }

  .cta-button:hover .button-flash {
    animation: flash 1.5s infinite;
  }

  @keyframes flash {
    0% {
      transform: scale(0);
      opacity: 0;
    }
    30% {
      transform: scale(0);
      opacity: 0.5;
    }
    100% {
      transform: scale(3);
      opacity: 0;
    }
  }

  .cta-button:disabled {
    cursor: not-allowed;
    opacity: 0.7;
  }
</style>