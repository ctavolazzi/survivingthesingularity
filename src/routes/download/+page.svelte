<script>
  function downloadSamplePDF() {
    const pdfUrl = '/Singularity-checklist.pdf';
    const link = document.createElement('a');
    link.href = pdfUrl;
    link.download = 'Singularity-checklist.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
</script>

<main>
  <h1>Download Singularity Checklist</h1>
  <p>Click the button below to download our free Singularity Checklist PDF.</p>
  <button on:click={downloadSamplePDF}>Download Checklist PDF</button>
</main>

<style>
  main {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
  }

  h1 {
    margin-bottom: 20px;
  }

  button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
  }

  button:hover {
    background-color: #45a049;
  }
</style>
