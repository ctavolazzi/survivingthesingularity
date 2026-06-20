<script>
	import { browser } from '$app/environment';
	import { evidenceCategories, resolveCategory, timeline, sources } from '$lib/data/evidence.js';
	import { toasts } from '$lib/stores/toasts.js';
	import YouTubeEmbed from '$lib/components/YouTubeEmbed.svelte';

	const categories = evidenceCategories.map(resolveCategory);

	const kindLabel = { paper: 'Paper', report: 'Report', article: 'Article' };

	// Totals for the header.
	const videoCount = categories.reduce((n, c) => n + c.videos.length, 0);
	const sourceCount = Object.keys(sources).length;

	let copied = false;

	const watchUrl = (id) => `https://www.youtube.com/watch?v=${id}`;

	// Build a clean, structured plaintext digest straight from the data, so the
	// copy keeps real links and reads well when pasted into any AI chat, far
	// smarter than scraping the rendered DOM.
	function buildPlaintext() {
		const pageUrl = browser ? window.location.href : 'https://survivingthesingularity.com/evidence';
		const out = [];
		out.push('SURVIVING THE SINGULARITY: THE EVIDENCE');
		out.push(`Source: ${pageUrl}`);
		out.push('');
		out.push(
			'We are already in the early stages of the Singularity. The question is no longer IF recursive self-improvement happens, but WHEN, and how fast. Below is the primary evidence: real demo footage and the papers and reports behind it. Watch it, read it, pull it apart.'
		);
		out.push('');

		out.push('== TIMELINE ==');
		for (const t of timeline) {
			out.push(`${t.year}  ${t.title}`);
			out.push(`        ${t.desc}`);
			const src = t.sourceId && sources[t.sourceId];
			if (src) out.push(`        Source: ${src.url}`);
		}
		out.push('');

		for (const cat of categories) {
			out.push(`== ${cat.title.toUpperCase()} (${cat.eyebrow}) ==`);
			out.push(cat.summary);
			if (cat.videos.length) {
				out.push('Watch:');
				for (const v of cat.videos) {
					out.push(`- ${v.title} (${v.channel})`);
					out.push(`  ${watchUrl(v.id)}`);
					out.push(`  ${v.blurb}`);
				}
			}
			if (cat.sources.length) {
				out.push('Read:');
				for (const s of cat.sources) {
					out.push(`- ${s.title} (${s.authors}, ${s.year}, ${s.venue})`);
					out.push(`  ${s.url}`);
					out.push(`  ${s.summary}`);
					out.push(`  Why it matters: ${s.why}`);
				}
			}
			out.push('');
		}

		out.push('== WHAT IT ADDS UP TO ==');
		out.push(
			'Intelligence, bodies, cheap tools, new substrates, and abundant energy are all bending upward at once, and AI is now helping build the hardware that runs the next AI. That feedback loop is recursive self-improvement.'
		);
		out.push('Soft takeoff: the transition plays out over years; institutions have time to adapt.');
		out.push('Hard takeoff: the transition happens in months or weeks once the loop closes; adaptation time collapses.');
		out.push('The evidence keeps pointing toward a hard takeoff. The move is to build independence before the curve goes vertical, not after.');
		out.push('');
		out.push(`---`);
		out.push(`Copied from Surviving the Singularity (${pageUrl}). Paste this into any AI chat to dig in.`);

		return out.join('\n');
	}

	async function copyEvidence() {
		if (!browser) return;
		try {
			await navigator.clipboard.writeText(buildPlaintext());
			copied = true;
			toasts.success('Evidence copied as plaintext. Paste it into any AI chat.');
			setTimeout(() => (copied = false), 3000);
		} catch (err) {
			toasts.error('Copy failed. Try selecting the page text manually.');
		}
	}
</script>

<svelte:head>
	<title>The Evidence | Surviving the Singularity</title>
	<meta
		name="description"
		content="The primary sources behind Surviving the Singularity: real demo footage and the papers and reports on AI, robotics, biocomputing, quantum, fusion, and space. Watch and read it yourself."
	/>
	<meta property="og:title" content="The Evidence | Surviving the Singularity" />
	<meta
		property="og:description"
		content="No forecasts you have to take on faith. Real footage and primary sources you can scrutinize, share, or drop into any AI chat."
	/>
</svelte:head>

<article class="evidence">
	<!-- HERO -->
	<header class="ev-hero">
		<p class="ev-eyebrow">The receipts</p>
		<h1 class="ev-title">The Evidence</h1>
		<p class="ev-lede">
			Everything on this site is downstream of things you can watch or read yourself. No forecasts
			you have to take on faith. Below is the footage and the primary sources: {videoCount} demos and
			{sourceCount} papers and reports, organized by theme. Watch it, read it, pull it apart.
		</p>
		<div class="ev-hero-actions">
			<button class="ev-copy-btn" class:ev-copied={copied} type="button" on:click={copyEvidence}>
				{#if copied}
					<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
					Copied as plaintext
				{:else}
					<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
					Copy page for chat
				{/if}
			</button>
			<span class="ev-hero-hint">Clean plaintext with every link intact. Paste it into any AI chat to start a conversation.</span>
		</div>
	</header>

	<!-- TIMELINE -->
	<section class="ev-section" aria-labelledby="ev-timeline-h">
		<div class="ev-section-head">
			<h2 id="ev-timeline-h" class="ev-h2">The timeline</h2>
			<p class="ev-section-desc">
				What already happened, what is happening now, and the dates the people building it have put
				on the record.
			</p>
		</div>

		<ol class="ev-timeline">
			{#each timeline as item}
				<li class="ev-tl-item ev-tl-{item.status}">
					<span class="ev-tl-year">{item.year}</span>
					<div class="ev-tl-body">
						<h3 class="ev-tl-title">{item.title}</h3>
						<p class="ev-tl-desc">{item.desc}</p>
						{#if item.sourceId && sources[item.sourceId]}
							<a class="ev-tl-source" href={sources[item.sourceId].url} target="_blank" rel="noopener noreferrer">
								Source: {sources[item.sourceId].venue}
							</a>
						{/if}
					</div>
				</li>
			{/each}
		</ol>
	</section>

	<!-- THEMED CATEGORIES -->
	{#each categories as cat}
		<section class="ev-section" id={cat.id} aria-labelledby={`ev-${cat.id}-h`}>
			<div class="ev-section-head">
				<p class="ev-cat-eyebrow">{cat.eyebrow}</p>
				<h2 id={`ev-${cat.id}-h`} class="ev-h2">{cat.title}</h2>
				<p class="ev-section-desc">{cat.summary}</p>
			</div>

			{#if cat.videos.length}
				<div class="ev-video-grid">
					{#each cat.videos as v}
						<YouTubeEmbed
							videoId={v.id}
							title={v.title}
							caption={v.blurb}
							credit={v.channel}
						/>
					{/each}
				</div>
			{/if}

			{#if cat.sources.length}
				<div class="ev-source-list">
					{#each cat.sources as s}
						<a class="ev-source-card ev-kind-{s.kind}" href={s.url} target="_blank" rel="noopener noreferrer">
							<div class="ev-source-top">
								<span class="ev-source-kind">{kindLabel[s.kind] || 'Source'}</span>
								<span class="ev-source-year">{s.year}</span>
							</div>
							<h3 class="ev-source-title">{s.title}</h3>
							<p class="ev-source-meta">{s.authors} · {s.venue}</p>
							<p class="ev-source-summary">{s.summary}</p>
							<p class="ev-source-why"><strong>Why it matters:</strong> {s.why}</p>
							<span class="ev-source-link">
								Open source
								<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7"/><path d="M7 7h10v10"/></svg>
							</span>
						</a>
					{/each}
				</div>
			{/if}
		</section>
	{/each}

	<!-- SYNTHESIS / TAKEOFF -->
	<section class="ev-section ev-takeoff" id="takeoff" aria-labelledby="ev-takeoff-h">
		<div class="ev-section-head">
			<p class="ev-cat-eyebrow">What it adds up to</p>
			<h2 id="ev-takeoff-h" class="ev-h2">We are already in the early stages</h2>
			<p class="ev-section-desc">
				Pull back from any single demo and the pattern is hard to miss. Intelligence, bodies, cheap
				tools, new substrates, and abundant energy are all bending upward at once, and AI is now
				helping build the very hardware that runs the next AI. That feedback loop has a name:
				<strong>recursive self-improvement</strong>. The point where machines improve themselves
				faster than we can, at scale, indefinitely.
			</p>
		</div>

		<p class="ev-takeoff-claim">
			The question is no longer <em>if</em> recursive self-improvement happens. It is <em>when</em>, and
			how fast.
		</p>

		<div class="ev-scenarios">
			<div class="ev-scenario ev-scenario-soft">
				<span class="ev-scenario-tag">Scenario A</span>
				<h3 class="ev-scenario-title">Soft takeoff</h3>
				<p class="ev-scenario-desc">
					The transition plays out over years. Capability compounds gradually, society and
					institutions have time to adapt, and the change feels like a steep but climbable ramp.
				</p>
			</div>
			<div class="ev-scenario ev-scenario-hard">
				<span class="ev-scenario-tag">Scenario B</span>
				<h3 class="ev-scenario-title">Hard takeoff</h3>
				<p class="ev-scenario-desc">
					The transition happens in months or weeks once the loop closes. Capability goes near-vertical,
					adaptation time collapses, and most people only notice after the world has already changed.
				</p>
			</div>
		</div>

		<p class="ev-takeoff-note">
			The evidence above keeps pointing the same direction: a hard takeoff looks increasingly likely.
			That is not a reason to panic. It is a reason to build your independence <em>before</em> the curve
			goes vertical, not after.
		</p>
	</section>

	<!-- CLOSING / HOW TO USE -->
	<section class="ev-section ev-closing" aria-labelledby="ev-use-h">
		<h2 id="ev-use-h" class="ev-h2">How to use this page</h2>
		<ul class="ev-use-list">
			<li><strong>Skeptical?</strong> Good. Every claim links to its source. Check them.</li>
			<li><strong>Want to share it?</strong> Send the link. It is one page, no signup, no paywall.</li>
			<li><strong>Talking to an AI?</strong> Hit "Copy page for chat" up top, paste it in, and ask it whatever you want.</li>
			<li><strong>Think something is missing or wrong?</strong> That is the point. The list is meant to be argued with.</li>
		</ul>
		<div class="ev-cta-row">
			<a href="/why" class="ev-btn ev-btn-primary">Why this matters now</a>
			<a href="/blueprint" class="ev-btn ev-btn-secondary">What to do about it</a>
		</div>
	</section>
</article>

<style>
	.evidence {
		max-width: var(--max-width, 1100px);
		margin: 0 auto;
		padding: 4rem var(--container-padding, 1.5rem) 6rem;
	}

	/* Hero */
	.ev-hero {
		text-align: center;
		max-width: 760px;
		margin: 0 auto 4rem;
	}

	.ev-eyebrow {
		font-family: var(--font-mono);
		font-size: 0.8rem;
		letter-spacing: 0.18em;
		text-transform: uppercase;
		color: var(--color-primary);
		margin: 0 0 0.75rem;
	}

	.ev-title {
		font-size: clamp(2.5rem, 6vw, 4rem);
		font-weight: 800;
		line-height: 1.05;
		margin: 0 0 1.25rem;
		color: var(--color-text-primary);
		letter-spacing: -0.02em;
	}

	.ev-lede {
		font-size: 1.15rem;
		line-height: 1.7;
		color: var(--color-text-secondary);
		margin: 0 0 2rem;
	}

	.ev-hero-actions {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.6rem;
	}

	.ev-copy-btn {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		font-family: var(--font-primary);
		font-weight: 700;
		font-size: 0.95rem;
		color: #020617;
		background: var(--color-primary);
		border: none;
		border-radius: var(--radius-sm);
		padding: 0.8rem 1.4rem;
		cursor: pointer;
		transition: transform 0.15s ease, background 0.2s ease;
	}

	.ev-copy-btn:hover {
		transform: translateY(-2px);
		background: var(--color-primary-light);
	}

	.ev-copy-btn.ev-copied {
		background: var(--color-success);
		color: #fff;
	}

	.ev-hero-hint {
		font-size: 0.85rem;
		color: var(--color-text-muted);
		font-family: var(--font-mono);
		max-width: 44ch;
	}

	/* Sections */
	.ev-section {
		margin: 0 auto 4.5rem;
		max-width: 960px;
		scroll-margin-top: 90px;
	}

	.ev-section-head {
		margin-bottom: 2rem;
		border-top: 1px solid var(--color-border);
		padding-top: 2rem;
	}

	.ev-cat-eyebrow {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		letter-spacing: 0.16em;
		text-transform: uppercase;
		color: var(--color-primary);
		margin: 0 0 0.5rem;
	}

	.ev-h2 {
		font-size: clamp(1.6rem, 3.5vw, 2.2rem);
		font-weight: 800;
		margin: 0 0 0.65rem;
		color: var(--color-text-primary);
		letter-spacing: -0.01em;
	}

	.ev-section-desc {
		font-size: 1.05rem;
		line-height: 1.65;
		color: var(--color-text-secondary);
		margin: 0;
		max-width: 70ch;
	}

	/* Timeline */
	.ev-timeline {
		list-style: none;
		margin: 0;
		padding: 0;
		position: relative;
	}

	.ev-timeline::before {
		content: '';
		position: absolute;
		left: 7px;
		top: 6px;
		bottom: 6px;
		width: 2px;
		background: var(--color-border);
	}

	.ev-tl-item {
		position: relative;
		display: grid;
		grid-template-columns: 5.5rem 1fr;
		gap: 1rem;
		padding: 0 0 1.75rem 1.75rem;
	}

	.ev-tl-item::before {
		content: '';
		position: absolute;
		left: 0;
		top: 6px;
		width: 16px;
		height: 16px;
		border-radius: 50%;
		background: var(--color-bg-primary);
		border: 2px solid var(--color-border-hover);
	}

	.ev-tl-past::before { border-color: var(--color-secondary); }
	.ev-tl-now::before {
		border-color: var(--color-primary);
		background: var(--color-primary);
		box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.2);
	}
	.ev-tl-future::before {
		border-style: dashed;
		border-color: var(--color-text-muted);
	}

	.ev-tl-year {
		font-family: var(--font-mono);
		font-weight: 700;
		font-size: 0.95rem;
		color: var(--color-text-primary);
		padding-top: 2px;
	}

	.ev-tl-future .ev-tl-year { color: var(--color-text-muted); }

	.ev-tl-title {
		font-size: 1.05rem;
		font-weight: 700;
		margin: 0 0 0.25rem;
		color: var(--color-text-primary);
	}

	.ev-tl-desc {
		font-size: 0.95rem;
		line-height: 1.55;
		color: var(--color-text-secondary);
		margin: 0 0 0.4rem;
	}

	.ev-tl-source {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--color-primary);
		text-decoration: none;
	}

	.ev-tl-source:hover { text-decoration: underline; }

	/* Video grid */
	.ev-video-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
		gap: 1.5rem;
		margin-bottom: 2rem;
	}

	/* Source cards */
	.ev-source-list {
		display: grid;
		gap: 1rem;
	}

	.ev-source-card {
		display: block;
		text-decoration: none;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-left: 3px solid var(--color-secondary);
		border-radius: var(--radius-md);
		padding: 1.5rem;
		transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease;
	}

	.ev-source-card:hover {
		background: var(--color-surface-hover);
		border-color: var(--color-border-hover);
		border-left-color: var(--color-primary);
		transform: translateY(-2px);
	}

	.ev-kind-paper { border-left-color: var(--color-secondary); }
	.ev-kind-report { border-left-color: var(--color-primary); }
	.ev-kind-article { border-left-color: #10b981; }

	.ev-source-top {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.6rem;
	}

	.ev-source-kind {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--color-text-muted);
		border: 1px solid var(--color-border);
		border-radius: 999px;
		padding: 0.15rem 0.6rem;
	}

	.ev-source-year {
		font-family: var(--font-mono);
		font-size: 0.85rem;
		font-weight: 700;
		color: var(--color-text-primary);
	}

	.ev-source-title {
		font-size: 1.15rem;
		font-weight: 700;
		margin: 0 0 0.3rem;
		color: var(--color-text-primary);
		line-height: 1.35;
	}

	.ev-source-meta {
		font-family: var(--font-mono);
		font-size: 0.78rem;
		color: var(--color-text-muted);
		margin: 0 0 0.9rem;
	}

	.ev-source-summary {
		font-size: 0.97rem;
		line-height: 1.6;
		color: var(--color-text-secondary);
		margin: 0 0 0.75rem;
	}

	.ev-source-why {
		font-size: 0.95rem;
		line-height: 1.6;
		color: var(--color-text-primary);
		margin: 0 0 1rem;
	}

	.ev-source-why strong { color: var(--color-primary); }

	.ev-source-link {
		display: inline-flex;
		align-items: center;
		gap: 0.4rem;
		font-family: var(--font-mono);
		font-size: 0.82rem;
		font-weight: 600;
		color: var(--color-primary);
	}

	/* Takeoff / synthesis */
	.ev-takeoff-claim {
		font-size: clamp(1.3rem, 3vw, 1.7rem);
		font-weight: 700;
		line-height: 1.4;
		color: var(--color-text-primary);
		text-align: center;
		max-width: 50ch;
		margin: 0 auto 2.5rem;
	}

	.ev-takeoff-claim em {
		color: var(--color-primary);
		font-style: normal;
	}

	.ev-scenarios {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 1.25rem;
		margin-bottom: 2rem;
	}

	.ev-scenario {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		padding: 1.5rem;
	}

	.ev-scenario-soft { border-top: 3px solid var(--color-secondary); }
	.ev-scenario-hard { border-top: 3px solid var(--color-primary); }

	.ev-scenario-tag {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: var(--color-text-muted);
	}

	.ev-scenario-title {
		font-size: 1.3rem;
		font-weight: 800;
		margin: 0.35rem 0 0.6rem;
		color: var(--color-text-primary);
	}

	.ev-scenario-desc {
		font-size: 0.97rem;
		line-height: 1.6;
		color: var(--color-text-secondary);
		margin: 0;
	}

	.ev-takeoff-note {
		font-size: 1.05rem;
		line-height: 1.7;
		color: var(--color-text-secondary);
		max-width: 65ch;
		margin: 0 auto;
		text-align: center;
	}

	.ev-takeoff-note em {
		color: var(--color-primary);
		font-style: normal;
		font-weight: 600;
	}

	/* Closing */
	.ev-closing {
		text-align: center;
		max-width: 720px;
	}

	.ev-use-list {
		list-style: none;
		padding: 0;
		margin: 1.5rem 0 2.5rem;
		text-align: left;
		display: grid;
		gap: 0.85rem;
	}

	.ev-use-list li {
		font-size: 1rem;
		line-height: 1.6;
		color: var(--color-text-secondary);
		padding-left: 1.5rem;
		position: relative;
	}

	.ev-use-list li::before {
		content: '→';
		position: absolute;
		left: 0;
		color: var(--color-primary);
		font-weight: 700;
	}

	.ev-use-list strong { color: var(--color-text-primary); }

	.ev-cta-row {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
	}

	.ev-btn {
		display: inline-flex;
		align-items: center;
		padding: 0.85rem 1.6rem;
		border-radius: var(--radius-sm);
		font-weight: 700;
		text-decoration: none;
		font-size: 0.95rem;
		transition: transform 0.15s ease, background 0.2s ease;
	}

	.ev-btn:hover { transform: translateY(-2px); }

	.ev-btn-primary {
		background: var(--color-primary);
		color: #020617;
	}

	.ev-btn-secondary {
		background: transparent;
		color: var(--color-text-primary);
		border: 1px solid var(--color-border-hover);
	}

	@media (max-width: 540px) {
		.ev-tl-item {
			grid-template-columns: 4.5rem 1fr;
			gap: 0.6rem;
		}
	}
</style>
