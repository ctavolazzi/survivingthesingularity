<script>
  import StSFreeGuideImage from '$lib/images/StSFreeGuide.png';

  let isDownloading = false;
  let buttonText = "Get Your FREE Checklist";

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
      <img src={StSFreeGuideImage} alt="Surviving the Singularity Free Guide" class="w-full mb-4 rounded-lg shadow-md">
      <button on:click={downloadSamplePDF} 
        class="big-button gradient-button text-white w-full" 
        class:downloading={isDownloading} 
        disabled={isDownloading}>
        {isDownloading ? 'Downloading...' : buttonText}
        <span class="button-icon">{isDownloading ? '⟳' : '↓'}</span>
      </button>
    </div>
  </div>
</div>

<style>
  .main-content {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding: 2rem;
  }

  .content-container {
    max-width: 800px;
    text-align: center;
  }

  .card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .big-button {
    font-weight: 600;
    font-size: 1.1rem;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .gradient-button {
    background: linear-gradient(135deg, #ff8a00, #ff5100);
    border: none;
    color: white;
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
</style>