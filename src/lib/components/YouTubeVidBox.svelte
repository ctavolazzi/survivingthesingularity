<script>
  export let videoId;
  export let title = "Video";
  export let description = "";
</script>

<div class="video-card">
  <h3 class="video-title">{title}</h3>
  {#if description}
    <p class="video-description">{description}</p>
  {/if}
  <div class="video-container">
    <iframe
      width="560"
      height="315"
      src="https://www.youtube.com/embed/{videoId}"
      title={title}
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
    ></iframe>
  </div>
</div>

<style>
  .video-card {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .video-title {
    font-size: 1.25rem;
    font-weight: bold;
    padding: 1rem 1rem 0.5rem;
    margin: 0;
    color: var(--color-text-primary);
  }

  .video-description {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    color: var(--color-text-secondary);
  }

  .video-container {
    position: relative;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
    height: 0;
    overflow: hidden;
  }

  .video-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  :global(.dark) .video-card {
    background-color: #2c3e50;
    border-color: #34495e;
  }

  :global(.dark) .video-title {
    color: #ecf0f1;
  }

  :global(.dark) .video-description {
    color: #bdc3c7;
  }
</style>
