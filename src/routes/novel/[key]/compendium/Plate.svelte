<script>
  // The picture slot for an entry. Give an entry
  // "image": {"src": "...", "alt": "...", "credit": "..."} in compendium.json
  // and the picture is shown. With no picture it draws a small plate with the
  // entry's initials, so the page never has a large empty box on it.
  export let name = '';
  /** @type {{src: string, alt?: string, credit?: string} | null} */
  export let image = null;
  /** @type {'small' | 'large'} */
  export let size = 'small';

  $: initials = name
    .replace(/^The\s+/i, '')
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0].toUpperCase())
    .join('');
</script>

{#if image?.src}
  <figure class="picture {size}" class:pixel={image.pixelArt}>
    <img src={image.src} alt={image.alt ?? ''} loading="lazy" decoding="async" />
    {#if image.credit}<figcaption>{image.credit}</figcaption>{/if}
  </figure>
{:else}
  <div class="plate" aria-hidden="true">{initials}</div>
{/if}

<style>
  .plate {
    flex: none;
    width: 76px;
    height: 76px;
    display: grid;
    place-items: center;
    border-radius: 14px;
    background: var(--panel, var(--card));
    border: 1px solid var(--rule);
    color: var(--accent);
    font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
    font-size: 30px;
    line-height: 1;
    letter-spacing: 0.02em;
  }
  @media (max-width: 520px) {
    .plate { width: 56px; height: 56px; border-radius: 12px; font-size: 22px; }
  }
  .picture { margin: 0; width: 100%; }
  .picture img {
    display: block;
    width: 100%;
    max-height: 420px;
    object-fit: cover;
    border-radius: 14px;
    border: 1px solid var(--rule);
  }
  /* Pixel art is drawn at its true size, scaled up in whole steps with hard edges. */
  .picture.pixel { max-width: 320px; }
  .picture.pixel img { width: 320px; max-width: 100%; height: auto; max-height: none; aspect-ratio: 1; object-fit: contain; image-rendering: pixelated; }
  .picture figcaption { margin-top: 8px; font-size: 14px; color: var(--soft, var(--muted)); }
</style>
