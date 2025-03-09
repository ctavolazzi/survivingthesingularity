<script>
  import { darkMode } from '$lib/stores/darkMode';
  import StSFreeGuideImage from '$lib/images/StSFreeGuide.png';

  let isDownloading = false;
  let buttonText = "Download FREE Checklist PDF";

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

  function handleJoinSkool() {
    window.open('https://www.skool.com/surviving-the-singularity-9297', '_blank');
  }

  function handleReadSample() {
    window.location.href = 'https://survivingthesingularity.com/sample';
  }
</script>

<div class="main-content">
  <div class="content-container">
    <div class="card bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4">Download Singularity Checklist</h1>
      <p class="intro text-xl text-gray-700 dark:text-gray-300 mb-6">Prepare for the future with our comprehensive guide.</p>
      <img src={StSFreeGuideImage} alt="Surviving the Singularity Free Guide" class="w-full mb-4 rounded-lg shadow-md" loading="lazy" \>
      <button on:click={downloadSamplePDF} 
        class="big-button bg-blue-500 hover:bg-blue-600 dark:bg-blue-700 dark:hover:bg-blue-800 text-white w-full" 
        class:downloading={isDownloading} 
        disabled={isDownloading}>
          {isDownloading ? 'Downloading...' : buttonText}
        <span class="button-icon">{isDownloading ? '⟳' : '↓'}</span>
      </button>
      <div class="description text-gray-700 dark:text-gray-300 mb-8">
        <br>
        <p class="mb-4">Our Singularity Checklist is a carefully curated PDF resource designed to help you:</p>
        <div class="bullet-points-container">
          <ul>
            <li>Understand key concepts related to technological singularity</li>
            <li>Identify potential challenges and opportunities in a rapidly changing world</li>
            <li>Develop strategies to adapt and thrive in the face of exponential technological growth</li>
          </ul>
        </div>
        <p>Download now and take the first step towards future-proofing your life and career.</p>
      </div>
      <div class="button-container">
        <button class="big-button" on:click={handleReadSample}>
          Read a Sample
        </button>
        <button class="big-button" on:click={handleJoinSkool}>
          Join the Skool Community
        </button>
      </div>
    </div>
  </div>
</div>

<style>
  .main-content {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding-top: 1rem;
    padding: 2rem;
  }

  .content-container {
    max-width: 800px;
    text-align: center;
    margin-top: 0.5rem;
  }

  h1 {
    font-size: 2rem;
    margin-top: 0;
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

  .bullet-points-container {
    width: 80%;
    margin: 0 auto;
  }

  ul {
    list-style-type: none;
    padding-left: 0;
    margin-bottom: 1rem;
    text-align: left;
  }

  li {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.5rem;
    font-weight: bold;
    text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.2);
  }

  li::before {
    content: "•";
    margin-right: 0.5em;
    flex-shrink: 0;
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