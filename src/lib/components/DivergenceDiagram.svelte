<script>
	import { onMount } from 'svelte';
	import InfoModal from '$lib/components/InfoModal.svelte';

	let wrap;
	let revealed = false;
	let activeCurve = null;

	const curveInfo = {
		old: {
			title: 'The Old Path: costs keep climbing',
			body: 'Housing, tuition, insurance, and general cost of living have outpaced wage growth for decades. The sourced stats above this chart (CPI, median home price) are the real-world anchors for this line.',
			links: [
				{ label: 'BLS Consumer Price Index', href: 'https://www.bls.gov/cpi/' },
				{ label: 'FRED Median Home Sale Price', href: 'https://fred.stlouisfed.org/series/MSPUS' },
			],
		},
		tools: {
			title: 'Capable Tools: costs keep collapsing',
			body: 'Utility-scale solar dropped roughly 85% from 2010 to 2023. Consumer GPUs now run serious local AI. Open-source robotics keeps getting cheaper. The inputs for an independent setup cost a fraction of what they did a decade ago.',
			links: [
				{ label: 'LBNL Utility-Scale Solar Report', href: 'https://emp.lbl.gov/utility-scale-solar' },
			],
		},
		gap: {
			title: 'The Gap: why timing matters',
			body: 'The vertical distance between the two lines is the opportunity: capable tools getting cheap while the conventional path gets expensive. The wider the gap, the more life you can buy back per dollar. Verify every number against current data before acting on any of it.',
			links: [],
		},
	};

	function openCurve(key) {
		activeCurve = key;
	}
	function labelKeydown(e, key) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			openCurve(key);
		}
	}

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						revealed = true;
						observer.disconnect();
					}
				});
			},
			{ threshold: 0.3 }
		);
		observer.observe(wrap);
		return () => observer.disconnect();
	});
</script>

<figure class="div-figure" bind:this={wrap} class:revealed>
	<svg viewBox="0 0 880 380" role="img" aria-label="Chart: the cost of the traditional path rises while the cost of capable tools collapses. Tap a label for sources.">
		<!-- grid -->
		<g stroke="rgba(148,163,184,0.08)" stroke-width="1">
			<line x1="70" y1="60" x2="830" y2="60" />
			<line x1="70" y1="130" x2="830" y2="130" />
			<line x1="70" y1="200" x2="830" y2="200" />
			<line x1="70" y1="270" x2="830" y2="270" />
		</g>
		<!-- axes -->
		<line x1="70" y1="30" x2="70" y2="300" stroke="rgba(148,163,184,0.3)" stroke-width="1" />
		<line x1="70" y1="300" x2="830" y2="300" stroke="rgba(148,163,184,0.3)" stroke-width="1" />

		<!-- x labels -->
		<g class="axis-label" text-anchor="middle">
			<text x="70" y="330">2010</text>
			<text x="260" y="330">2015</text>
			<text x="450" y="330">2020</text>
			<text x="640" y="330">2025</text>
			<text x="830" y="330">now</text>
		</g>
		<text x="34" y="170" class="axis-label" text-anchor="middle" transform="rotate(-90 34 170)">RELATIVE COST</text>

		<!-- the gap shading (tappable) -->
		<g
			class="gap-group"
			role="button"
			tabindex="0"
			aria-label="The gap between rising costs and collapsing tool prices. Tap for explanation."
			on:click={() => openCurve('gap')}
			on:keydown={(e) => labelKeydown(e, 'gap')}
		>
			<path
				class="gap-fill"
				d="M 450 178 C 580 150, 700 110, 830 72 L 830 252 C 700 236, 580 220, 450 196 Z"
				fill="rgba(245,158,11,0.08)"
			/>
			<g class="gap-note">
				<line x1="762" y1="86" x2="762" y2="240" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="3 4" />
				<polygon points="762,86 757,97 767,97" fill="#fbbf24" />
				<polygon points="762,240 757,229 767,229" fill="#fbbf24" />
				<text x="744" y="158" text-anchor="end" class="gap-text">THE GAP IS</text>
				<text x="744" y="176" text-anchor="end" class="gap-text">THE OPPORTUNITY</text>
				<text x="744" y="196" text-anchor="end" class="tap-glyph">ⓘ tap</text>
			</g>
		</g>

		<!-- traditional path: rising -->
		<path
			class="line line-danger"
			d="M 70 198 C 200 192, 340 188, 450 178 C 580 150, 700 110, 830 72"
			fill="none"
			stroke="#f87171"
			stroke-width="3"
		/>
		<!-- capable tools: collapsing -->
		<path
			class="line line-success"
			d="M 70 78 C 200 92, 330 130, 450 196 C 570 246, 700 250, 830 252"
			fill="none"
			stroke="#34d399"
			stroke-width="3"
		/>

		<!-- end dots -->
		<circle class="end-dot" cx="830" cy="72" r="6" fill="#f87171" />
		<circle class="end-dot" cx="830" cy="252" r="6" fill="#34d399" />

		<!-- line labels (tappable) -->
		<g
			class="line-label label-danger"
			role="button"
			tabindex="0"
			aria-label="The old path: housing, tuition, cost of living. Tap for sources."
			on:click={() => openCurve('old')}
			on:keydown={(e) => labelKeydown(e, 'old')}
		>
			<rect x="496" y="92" width="216" height="52" rx="6" fill="rgba(15,23,42,0.85)" stroke="rgba(248,113,113,0.4)" />
			<text x="512" y="114" fill="#f87171" class="label-main">THE OLD PATH ⓘ</text>
			<text x="512" y="134" fill="#fca5a5" class="label-sub">housing · tuition · living</text>
		</g>
		<g
			class="line-label label-success"
			role="button"
			tabindex="0"
			aria-label="Capable tools: solar, GPUs, open-source robots, AI. Tap for sources."
			on:click={() => openCurve('tools')}
			on:keydown={(e) => labelKeydown(e, 'tools')}
		>
			<rect x="496" y="242" width="226" height="52" rx="6" fill="rgba(15,23,42,0.85)" stroke="rgba(52,211,153,0.4)" />
			<text x="512" y="264" fill="#34d399" class="label-main">CAPABLE TOOLS ⓘ</text>
			<text x="512" y="284" fill="#6ee7b7" class="label-sub">solar · GPUs · robots · AI</text>
		</g>
	</svg>
	<figcaption>
		Stylized illustration, not plotted data. Directionally consistent with the sourced
		figures above. <span class="tap-hint">Tap a label for sources.</span>
	</figcaption>
</figure>

<InfoModal
	open={activeCurve !== null}
	title={activeCurve ? curveInfo[activeCurve].title : ''}
	on:close={() => (activeCurve = null)}
>
	{#if activeCurve}
		<p>{curveInfo[activeCurve].body}</p>
		{#if curveInfo[activeCurve].links.length}
			<ul>
				{#each curveInfo[activeCurve].links as link}
					<li><a href={link.href} target="_blank" rel="noopener noreferrer">{link.label} ↗</a></li>
				{/each}
			</ul>
		{/if}
	{/if}
</InfoModal>

<style>
	.div-figure {
		margin: 3rem 0 2.5rem;
		padding: 2rem 1.5rem 1.25rem;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: var(--radius-md);
		opacity: 0;
		transform: translateY(24px);
		transition: opacity 0.9s ease, transform 0.9s ease;
	}
	.div-figure.revealed {
		opacity: 1;
		transform: none;
	}
	svg {
		display: block;
		width: 100%;
		height: auto;
	}
	.axis-label,
	.axis-label text {
		font-family: var(--font-mono);
		font-size: 13px;
		fill: #cbd5e1;
	}
	.label-main {
		font-family: var(--font-mono);
		font-size: 14px;
		font-weight: 700;
		letter-spacing: 0.06em;
	}
	.label-sub {
		font-family: var(--font-mono);
		font-size: 11.5px;
	}
	.gap-text {
		font-family: var(--font-mono);
		font-size: 14px;
		font-weight: 700;
		letter-spacing: 0.06em;
		fill: #fbbf24;
	}
	.tap-glyph {
		font-family: var(--font-mono);
		font-size: 11px;
		fill: rgba(251, 191, 36, 0.75);
	}
	.line-label,
	.gap-group {
		cursor: pointer;
		outline: none;
	}
	.line-label rect {
		transition: stroke 0.2s, filter 0.2s;
	}
	.line-label:hover rect,
	.line-label:focus-visible rect {
		filter: brightness(1.35);
	}
	.gap-group:hover .gap-fill,
	.gap-group:focus-visible .gap-fill {
		fill: rgba(245, 158, 11, 0.14);
	}
	.line {
		stroke-dasharray: 900;
		stroke-dashoffset: 900;
		transition: stroke-dashoffset 2s ease 0.3s;
	}
	.revealed .line { stroke-dashoffset: 0; }
	.gap-fill,
	.end-dot,
	.gap-note,
	.line-label {
		opacity: 0;
		transition: opacity 0.8s ease 1.6s;
	}
	.revealed .gap-fill,
	.revealed .end-dot,
	.revealed .gap-note,
	.revealed .line-label {
		opacity: 1;
	}
	figcaption {
		margin-top: 0.9rem;
		font-family: var(--font-mono);
		font-size: 0.78rem;
		line-height: 1.6;
		color: #cbd5e1;
		text-align: center;
	}
	.tap-hint {
		color: var(--color-primary-light);
	}
	/* mobile: 880-unit viewBox shrinks hard on phones — bump user-unit sizes */
	@media (max-width: 640px) {
		.div-figure { padding: 1.25rem 0.75rem 1rem; }
		.axis-label,
		.axis-label text { font-size: 19px; }
		.label-main { font-size: 18px; }
		.label-sub { font-size: 15px; }
		.gap-text { font-size: 19px; }
		.tap-glyph { font-size: 15px; }
		figcaption { font-size: 0.85rem; }
	}
	@media (prefers-reduced-motion: reduce) {
		.div-figure, .line, .gap-fill, .end-dot, .gap-note, .line-label {
			transition: none;
			opacity: 1;
			stroke-dashoffset: 0;
		}
	}
</style>
