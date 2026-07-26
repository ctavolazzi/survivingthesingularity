<script>
  // The book cover, one component so every surface that shows the book shows
  // the same art at the same fidelity. Assets are kept in sync with the book's
  // own cover by `sts.py cover --sync`, so this never drifts from the printed
  // edition - point it at the optimized derivatives and it follows along.

  /** Rendered width. Any CSS length; the aspect ratio is locked to the art. */
  export let width = '220px';
  /** Amber halo behind the cover. Off for small inline uses. */
  export let glow = true;
  /** Slight tilt, so it reads as an object rather than a flat image. */
  export let tilt = false;
  /** Lazy by default; pass "eager" when it's above the fold. */
  export let loading = 'lazy';
  export let alt = 'Surviving the Singularity book cover';
</script>

<div class="cover-wrap" class:has-glow={glow} class:is-tilted={tilt} style="--cover-w: {width};">
  {#if glow}<div class="cover-glow" aria-hidden="true"></div>{/if}
  <picture>
    <source
      type="image/webp"
      srcset="/images/optimized/surviving_the_singularity_cover_400.webp 400w,
              /images/optimized/surviving_the_singularity_cover_800.webp 800w,
              /images/optimized/surviving_the_singularity_cover_1200.webp 1200w"
      sizes="{width}"
    />
    <img
      src="/images/surviving_the_singularity_cover_1200.png"
      srcset="/images/optimized/surviving_the_singularity_cover_400.png 400w,
              /images/optimized/surviving_the_singularity_cover_800.png 800w,
              /images/optimized/surviving_the_singularity_cover_1200.png 1200w"
      sizes="{width}"
      {alt}
      {loading}
      decoding="async"
      width="1410"
      height="2056"
      class="cover-img"
    />
  </picture>
</div>

<style>
  .cover-wrap {
    position: relative;
    width: var(--cover-w);
    max-width: 100%;
    flex-shrink: 0;
    line-height: 0;
  }

  .cover-glow {
    position: absolute;
    inset: -14%;
    background: radial-gradient(ellipse at center, rgba(245, 158, 11, 0.26) 0%, rgba(245, 158, 11, 0.06) 45%, transparent 72%);
    filter: blur(6px);
    pointer-events: none;
  }

  .cover-img {
    position: relative;
    width: 100%;
    height: auto;
    display: block;
    border-radius: 6px;
    box-shadow:
      0 18px 40px rgba(0, 0, 0, 0.55),
      0 0 0 1px rgba(245, 158, 11, 0.22);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }

  .is-tilted .cover-img {
    transform: rotate(-1.8deg);
  }

  .cover-wrap:hover .cover-img {
    transform: rotate(0deg) translateY(-3px);
    box-shadow:
      0 24px 52px rgba(0, 0, 0, 0.6),
      0 0 0 1px rgba(245, 158, 11, 0.38);
  }

  @media (prefers-reduced-motion: reduce) {
    .cover-img,
    .is-tilted .cover-img,
    .cover-wrap:hover .cover-img { transition: none; transform: none; }
  }
</style>
