<script>
  import YouTubeVidBox from './YouTubeVidBox.svelte';

  export let title = "View more content like this";
  export let description = "Here are some more videos that dive deeper into AI and gaming";
  export let videos = [];
</script>

<div class="recommended-content-container">
  <h2 class="recommended-title">{title}</h2>
  <p class="recommended-description">{description}</p>
  <div class="video-container">
    {#each videos as video}
      <YouTubeVidBox videoId={video.id} title={video.title} />
    {/each}
  </div>
</div>

<style>
  .recommended-content-container {
    background-color: var(--color-bg-secondary);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-top: 2rem;
  }

  .recommended-title {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: var(--color-text-primary);
  }

  .recommended-description {
    font-size: 1rem;
    margin-bottom: 1rem;
    color: var(--color-text-secondary);
  }

  .video-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }

  @media (max-width: 768px) {
    .video-container {
      grid-template-columns: 1fr;
    }
  }
</style>
