<script>
  /**
   * Click-to-load YouTube facade.
   *
   * An eager YouTube embed costs ~1.1 MB of player script and styles per
   * video before anyone presses play. Measured 2026-08-04 on the homepage:
   * two eager embeds put 2.3 MB of youtube.com payload into a 2 MB page
   * weight budget and were the bulk of the e2e c-speed failure. The player
   * iframe also performs its own sub-navigations while it boots, which is
   * the prime suspect for WebKit's "interrupted by another navigation"
   * flake in d-device-compliance.
   *
   * So: render the thumbnail and a play control, and only create the real
   * iframe when the viewer asks for it. The click hands off to the player
   * with autoplay=1, so it is still one click to watch.
   */
  export let videoId;
  export let title;

  let playing = false;

  // hqdefault is ~20-60 KB and always exists; maxresdefault is ~270 KB and
  // 404s on some videos. The facade is a preview, not the product.
  $: thumb = `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;
</script>

{#if playing}
  <iframe
    src={`https://www.youtube.com/embed/${videoId}?autoplay=1`}
    {title}
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen
  ></iframe>
{:else}
  <button
    type="button"
    class="lite-yt"
    aria-label={`Play video: ${title}`}
    on:click={() => (playing = true)}
  >
    <img src={thumb} alt="" loading="lazy" decoding="async" />
    <span class="lite-yt-play" aria-hidden="true">
      <svg viewBox="0 0 68 48" width="68" height="48">
        <path
          d="M66.52 7.74a8 8 0 0 0-5.63-5.66C55.93.9 34 .9 34 .9s-21.93 0-26.89 1.18A8 8 0 0 0 1.48 7.74 83.2 83.2 0 0 0 .34 24a83.2 83.2 0 0 0 1.14 16.26 8 8 0 0 0 5.63 5.66C12.07 47.1 34 47.1 34 47.1s21.93 0 26.89-1.18a8 8 0 0 0 5.63-5.66A83.2 83.2 0 0 0 67.66 24a83.2 83.2 0 0 0-1.14-16.26z"
          fill="#f00"
        />
        <path d="M45 24 27 14v20" fill="#fff" />
      </svg>
    </span>
  </button>
{/if}

<style>
  /* Both fill the parent ratio box exactly the way the iframe rule in the
     consuming page does, so swapping facade for player moves nothing. */
  .lite-yt,
  iframe {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: none;
  }

  .lite-yt {
    display: block;
    padding: 0;
    margin: 0;
    background: #000;
    cursor: pointer;
  }

  .lite-yt img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .lite-yt-play {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.9;
    transition: opacity 0.15s ease, transform 0.15s ease;
  }

  .lite-yt:hover .lite-yt-play,
  .lite-yt:focus-visible .lite-yt-play {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.06);
  }

  .lite-yt:focus-visible {
    outline: 2px solid #f59e0b;
    outline-offset: -2px;
  }
</style>
