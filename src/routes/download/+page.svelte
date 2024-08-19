<script>
  import { darkMode } from '$lib/stores/darkMode';
  let isDownloading = false;

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

<div class="main-content">
  <div class="content-container">
    <div class="card bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Download Singularity Checklist</h1>
      <p class="intro text-xl text-gray-700 dark:text-gray-300 mb-6">Prepare for the future with our comprehensive guide.</p>
      <div class="description text-gray-700 dark:text-gray-300 mb-8">
        <p class="mb-4">Our Singularity Checklist is a carefully curated PDF resource designed to help you:</p>
        <ul class="list-disc list-inside mb-4">
          <li>Understand key concepts related to technological singularity</li>
          <li>Identify potential challenges and opportunities in a rapidly changing world</li>
          <li>Develop strategies to adapt and thrive in the face of exponential technological growth</li>
        </ul>
        <p>Download now and take the first step towards future-proofing your life and career.</p>
      </div>
      <button on:click={downloadSamplePDF} 
              class="big-button bg-blue-500 hover:bg-blue-600 dark:bg-blue-700 dark:hover:bg-blue-800 text-white w-full" 
              class:downloading={isDownloading} 
              disabled={isDownloading}>
        {isDownloading ? 'Downloading...' : 'Download Checklist PDF'}
        <span class="button-icon">{isDownloading ? '⟳' : '↓'}</span>
      </button>
    </div>
  </div>
</div>

<style>
  .main-content {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
  }

  .content-container {
    max-width: 800px;
    text-align: center;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .intro {
    font-size: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .description p,
  li {
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  ul {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
    list-style-type: disc;
  }

  .button-container {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin: 1rem 0;
  }

  .big-button {
    flex: 1;
    font-weight: 600;
    font-size: 1.1rem;
    background-color: #ffffff;
    border: 1px solid #2c3e50;
    border-radius: 6px;
    color: #2c3e50;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .big-button:hover {
    background-color: #f8f9fa;
    border-color: #34495e;
    color: #34495e;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transform: translateY(-2px);
  }

  :global(.dark) .big-button {
    background-color: #2c3e50;
    color: #ffffff;
    border-color: #34495e;
  }

  :global(.dark) .big-button:hover {
    background-color: #34495e;
    border-color: #4a6785;
    color: #ffffff;
  }

  .button-icon {
    margin-left: 8px;
    font-size: 1.2rem;
  }

  .downloading .button-icon {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    100% { transform: rotate(360deg); }
  }

  .big-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  /* .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  } */
</style>