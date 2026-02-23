<script>
  export let alt = 'Image placeholder';
  export let aspect = '16/9';   // '16/9', '1/1', '4/3', '3/2', '21/9'
  export let caption = '';
  export let size = 'full';     // 'full', 'medium', 'small'
  export let type = 'photo';    // 'photo', 'chart', 'diagram', 'screenshot', 'infographic'

  const typeIcons = {
    photo: 'M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z M12 17a5 5 0 100-10 5 5 0 000 10z',
    chart: 'M18 20V10M12 20V4M6 20v-6',
    diagram: 'M12 2L2 7l10 5 10-5-10-5z M2 17l10 5 10-5 M2 12l10 5 10-5',
    screenshot: 'M2 3h20v14H2z M8 21h8 M12 17v4',
    infographic: 'M4 4h16v16H4z M9 9h6v6H9z M4 9h5 M15 9h5 M9 4v5 M9 15v5'
  };

  const sizeWidths = {
    full: '100%',
    medium: '66%',
    small: '50%'
  };
</script>

<figure class="placeholder" style="max-width: {sizeWidths[size]}">
  <div class="placeholder-frame" style="aspect-ratio: {aspect}">
    <div class="placeholder-x">
      <div class="x-line x-line-1"></div>
      <div class="x-line x-line-2"></div>
    </div>
    <div class="placeholder-content">
      <svg class="placeholder-icon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="{typeIcons[type] || typeIcons.photo}"/>
      </svg>
      <span class="placeholder-text">{alt}</span>
      <span class="placeholder-type">{type.toUpperCase()} — {aspect}</span>
    </div>
  </div>
  {#if caption}
    <figcaption class="placeholder-caption">{caption}</figcaption>
  {/if}
</figure>

<style>
  .placeholder {
    margin: 1.5rem auto;
  }

  .placeholder-frame {
    position: relative;
    background: rgba(15, 23, 42, 0.5);
    border: 1px dashed rgba(148, 163, 184, 0.15);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  .placeholder-x {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .x-line {
    position: absolute;
    background: rgba(148, 163, 184, 0.04);
    height: 1px;
    width: 141.4%;
    left: -20.7%;
    top: 50%;
    transform-origin: center;
  }

  .x-line-1 {
    transform: rotate(var(--x-angle, 33.69deg));
  }

  .x-line-2 {
    transform: rotate(calc(-1 * var(--x-angle, 33.69deg)));
  }

  .placeholder-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    z-index: 1;
    padding: 1rem;
    text-align: center;
  }

  .placeholder-icon {
    color: rgba(148, 163, 184, 0.2);
  }

  .placeholder-text {
    font-size: 0.78rem;
    color: #475569;
    max-width: 300px;
    line-height: 1.4;
  }

  .placeholder-type {
    font-size: 0.55rem;
    color: #334155;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
    font-weight: 600;
  }

  .placeholder-caption {
    margin-top: 0.5rem;
    font-size: 0.75rem;
    color: #475569;
    text-align: center;
    font-style: italic;
  }
</style>
