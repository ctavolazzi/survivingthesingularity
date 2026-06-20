<script>
	// Lightweight, privacy-friendly, lazy-loaded YouTube embed.
	// Shows the video thumbnail first; only loads the iframe on click,
	// so the page stays fast and no YouTube cookies are set until the
	// visitor actually presses play.
	export let videoId;
	export let title = 'YouTube video';
	export let caption = '';
	export let credit = '';

	let playing = false;

	$: thumb = `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;
	$: embedSrc = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0`;
</script>

<figure class="yt-embed">
	<div class="yt-frame">
		{#if playing}
			<iframe
				src={embedSrc}
				{title}
				frameborder="0"
				allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
				referrerpolicy="strict-origin-when-cross-origin"
				allowfullscreen
			></iframe>
		{:else}
			<button class="yt-poster" type="button" on:click={() => (playing = true)} aria-label={`Play: ${title}`}>
				<img src={thumb} alt={title} loading="lazy" />
				<span class="yt-play" aria-hidden="true">
					<svg width="68" height="48" viewBox="0 0 68 48">
						<path class="yt-play-bg" d="M66.52 7.74c-.78-2.93-2.49-5.41-5.42-6.19C55.79.13 34 0 34 0S12.21.13 6.9 1.55c-2.93.78-4.63 3.26-5.42 6.19C.06 13.05 0 24 0 24s.06 10.95 1.48 16.26c.78 2.93 2.49 5.41 5.42 6.19C12.21 47.87 34 48 34 48s21.79-.13 27.1-1.55c2.93-.78 4.64-3.26 5.42-6.19C67.94 34.95 68 24 68 24s-.06-10.95-1.48-16.26z"/>
						<path d="M 45,24 27,14 27,34" fill="#fff"/>
					</svg>
				</span>
			</button>
		{/if}
	</div>
	{#if caption || credit}
		<figcaption class="yt-caption">
			{#if caption}<span class="yt-caption-text">{caption}</span>{/if}
			{#if credit}<span class="yt-credit">{credit}</span>{/if}
		</figcaption>
	{/if}
</figure>

<style>
	.yt-embed {
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: 0.65rem;
	}

	.yt-frame {
		position: relative;
		aspect-ratio: 16 / 9;
		width: 100%;
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		overflow: hidden;
		background: #000;
	}

	.yt-frame iframe {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		border: 0;
	}

	.yt-poster {
		position: absolute;
		inset: 0;
		padding: 0;
		border: 0;
		cursor: pointer;
		background: #000;
		display: block;
		width: 100%;
		height: 100%;
	}

	.yt-poster img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.4s ease, opacity 0.3s ease;
		opacity: 0.92;
	}

	.yt-poster:hover img,
	.yt-poster:focus-visible img {
		transform: scale(1.04);
		opacity: 1;
	}

	.yt-play {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		transition: transform 0.2s ease;
	}

	.yt-play .yt-play-bg {
		fill: #212121;
		fill-opacity: 0.8;
		transition: fill 0.2s ease, fill-opacity 0.2s ease;
	}

	.yt-poster:hover .yt-play-bg,
	.yt-poster:focus-visible .yt-play-bg {
		fill: var(--color-primary);
		fill-opacity: 1;
	}

	.yt-poster:hover .yt-play,
	.yt-poster:focus-visible .yt-play {
		transform: translate(-50%, -50%) scale(1.08);
	}

	.yt-caption {
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
		font-size: 0.9rem;
		line-height: 1.4;
	}

	.yt-caption-text {
		color: var(--color-text-primary);
		font-weight: 600;
	}

	.yt-credit {
		color: var(--color-text-muted);
		font-family: var(--font-mono);
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.04em;
	}
</style>
