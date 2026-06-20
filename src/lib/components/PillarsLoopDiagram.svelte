<script>
	import { onMount } from 'svelte';
	import InfoModal from '$lib/components/InfoModal.svelte';

	let wrap;
	let revealed = false;
	let activePillar = null;

	const pillarInfo = {
		tools: {
			title: '01: Learn the Tools',
			color: '#f59e0b',
			body: 'Teach yourself to use modern AI. The real leverage is not a subscription. It is understanding these tools well enough to build new ways of getting your needs met.',
			feeds: 'Feeds the loop: the AI skills you build here are what run the machines in pillar 02.',
			href: '/blueprint/local-ai',
		},
		robotics: {
			title: '02: Open-Source Robotics',
			color: '#3b82f6',
			body: 'Automate food production with FarmBot and workshop tasks with open-source robots. Secure your own calories and labor.',
			feeds: 'Feeds the loop: automated production is what makes the low-overhead homestead in pillar 03 viable.',
			href: '/blueprint/robotics',
		},
		exit: {
			title: '03: The Physical Exit',
			color: '#10b981',
			body: 'Rural land, a shouse workshop, and a digital cash engine. Crush overhead and buy back decades of your life.',
			feeds: 'Feeds the loop: crushed overhead buys back the time you need to keep learning in pillar 01.',
			href: '/blueprint/physical-exit',
		},
	};

	function openPillar(key) {
		activePillar = key;
	}
	function nodeKeydown(e, key) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			openPillar(key);
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

<figure class="loop-figure" bind:this={wrap} class:revealed>
	<svg viewBox="0 0 560 500" role="img" aria-label="Diagram: the three pillars reinforce each other in a loop around material independence. Tap a pillar for details.">
		<!-- orbit ring -->
		<circle cx="280" cy="250" r="158" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1" />
		<circle class="orbit-flow" cx="280" cy="250" r="158" fill="none" stroke="rgba(245,158,11,0.45)" stroke-width="1.5" />

		<!-- center -->
		<circle cx="280" cy="250" r="66" fill="rgba(30,41,59,0.65)" stroke="rgba(148,163,184,0.25)" stroke-width="1" />
		<text x="280" y="242" text-anchor="middle" class="center-label">MATERIAL</text>
		<text x="280" y="262" text-anchor="middle" class="center-label">INDEPENDENCE</text>

		<!-- reinforcement edges -->
		<g class="edges" fill="none" stroke-width="1.5">
			<path class="edge" d="M 322 94 C 392 140, 420 210, 430 290" stroke="rgba(245,158,11,0.55)" />
			<path class="edge" d="M 380 352 C 330 382, 230 382, 180 352" stroke="rgba(59,130,246,0.55)" />
			<path class="edge" d="M 130 290 C 140 210, 168 140, 238 94" stroke="rgba(16,185,129,0.55)" />
		</g>
		<g fill="rgba(203,213,225,0.85)">
			<polygon points="430,290 424,278 437,279" />
			<polygon points="180,352 193,350 187,361" />
			<polygon points="238,94 235,107 246,103" />
		</g>

		<!-- edge annotations -->
		<text x="452" y="184" text-anchor="middle" class="edge-label">AI skills run<tspan x="452" dy="16">the machines</tspan></text>
		<text x="280" y="416" text-anchor="middle" class="edge-label">automation feeds<tspan x="280" dy="16">the homestead</tspan></text>
		<text x="104" y="184" text-anchor="middle" class="edge-label">low overhead buys<tspan x="104" dy="16">time to learn</tspan></text>

		<!-- pillar 1: Learn the Tools (top) -->
		<g
			class="node node-1"
			role="button"
			tabindex="0"
			aria-label="Pillar 1: Learn the Tools. Tap for details."
			on:click={() => openPillar('tools')}
			on:keydown={(e) => nodeKeydown(e, 'tools')}
		>
			<circle class="node-hit" cx="280" cy="72" r="54" />
			<circle class="node-ring" cx="280" cy="72" r="48" fill="#0f172a" stroke="#f59e0b" stroke-width="2" />
			<text x="280" y="64" text-anchor="middle" class="node-num" fill="#fbbf24">01</text>
			<text x="280" y="82" text-anchor="middle" class="node-name">TOOLS</text>
			<text x="280" y="99" text-anchor="middle" class="node-tap" fill="#fbbf24">ⓘ</text>
		</g>

		<!-- pillar 2: Robotics (bottom right) -->
		<g
			class="node node-2"
			role="button"
			tabindex="0"
			aria-label="Pillar 2: Open-Source Robotics. Tap for details."
			on:click={() => openPillar('robotics')}
			on:keydown={(e) => nodeKeydown(e, 'robotics')}
		>
			<circle class="node-hit" cx="427" cy="340" r="54" />
			<circle class="node-ring" cx="427" cy="340" r="48" fill="#0f172a" stroke="#3b82f6" stroke-width="2" />
			<text x="427" y="332" text-anchor="middle" class="node-num" fill="#60a5fa">02</text>
			<text x="427" y="350" text-anchor="middle" class="node-name">ROBOTS</text>
			<text x="427" y="367" text-anchor="middle" class="node-tap" fill="#60a5fa">ⓘ</text>
		</g>

		<!-- pillar 3: Physical Exit (bottom left) -->
		<g
			class="node node-3"
			role="button"
			tabindex="0"
			aria-label="Pillar 3: The Physical Exit. Tap for details."
			on:click={() => openPillar('exit')}
			on:keydown={(e) => nodeKeydown(e, 'exit')}
		>
			<circle class="node-hit" cx="133" cy="340" r="54" />
			<circle class="node-ring" cx="133" cy="340" r="48" fill="#0f172a" stroke="#10b981" stroke-width="2" />
			<text x="133" y="332" text-anchor="middle" class="node-num" fill="#34d399">03</text>
			<text x="133" y="350" text-anchor="middle" class="node-name">EXIT</text>
			<text x="133" y="367" text-anchor="middle" class="node-tap" fill="#34d399">ⓘ</text>
		</g>
	</svg>
	<figcaption>
		The reinforcing loop: each pillar's output is the next one's input.
		<span class="tap-hint">Tap a pillar to see how.</span>
	</figcaption>
</figure>

<InfoModal
	open={activePillar !== null}
	title={activePillar ? pillarInfo[activePillar].title : ''}
	on:close={() => (activePillar = null)}
>
	{#if activePillar}
		<p>{pillarInfo[activePillar].body}</p>
		<p><em>{pillarInfo[activePillar].feeds}</em></p>
		<a class="modal-cta" href={pillarInfo[activePillar].href}>
			Read the chapter
			<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M3 7H11M11 7L8 4M11 7L8 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
		</a>
	{/if}
</InfoModal>

<style>
	.loop-figure {
		margin: 3rem auto 0;
		max-width: 560px;
		opacity: 0;
		transform: translateY(24px);
		transition: opacity 0.9s ease, transform 0.9s ease;
	}
	.loop-figure.revealed {
		opacity: 1;
		transform: none;
	}
	svg {
		display: block;
		width: 100%;
		height: auto;
	}
	.center-label {
		font-family: var(--font-mono);
		font-size: 13px;
		font-weight: 600;
		letter-spacing: 0.12em;
		fill: var(--color-text-primary);
	}
	.node-num {
		font-family: var(--font-mono);
		font-size: 15px;
		font-weight: 700;
		letter-spacing: 0.08em;
	}
	.node-name {
		font-family: var(--font-mono);
		font-size: 12.5px;
		font-weight: 600;
		letter-spacing: 0.14em;
		fill: #f1f5f9;
	}
	.node-tap {
		font-size: 13px;
		opacity: 0.8;
	}
	.edge-label {
		font-family: var(--font-mono);
		font-size: 12.5px;
		fill: #cbd5e1;
	}
	.node {
		opacity: 0;
		transition: opacity 0.7s ease;
		cursor: pointer;
		outline: none;
	}
	.node-hit {
		fill: transparent;
	}
	.node-ring {
		transition: filter 0.25s ease, stroke-width 0.25s ease;
	}
	.node:hover .node-ring,
	.node:focus-visible .node-ring {
		stroke-width: 3;
		filter: drop-shadow(0 0 12px currentColor);
	}
	.node-1 .node-ring { color: rgba(245, 158, 11, 0.7); }
	.node-2 .node-ring { color: rgba(59, 130, 246, 0.7); }
	.node-3 .node-ring { color: rgba(16, 185, 129, 0.7); }
	.revealed .node-1 { opacity: 1; transition-delay: 0.15s; }
	.revealed .node-2 { opacity: 1; transition-delay: 0.35s; }
	.revealed .node-3 { opacity: 1; transition-delay: 0.55s; }
	.edge {
		stroke-dasharray: 400;
		stroke-dashoffset: 400;
		transition: stroke-dashoffset 1.6s ease 0.7s;
	}
	.revealed .edge { stroke-dashoffset: 0; }
	.orbit-flow {
		stroke-dasharray: 5 9;
		animation: orbit-flow 1.6s linear infinite;
	}
	@keyframes orbit-flow {
		to { stroke-dashoffset: -14; }
	}
	figcaption {
		margin-top: 1rem;
		text-align: center;
		font-family: var(--font-mono);
		font-size: 0.8rem;
		line-height: 1.6;
		color: #cbd5e1;
	}
	.tap-hint {
		color: var(--color-primary-light);
	}
	/* mobile: SVG scales down ~0.6x, so bump user-unit font sizes to compensate */
	@media (max-width: 640px) {
		.center-label { font-size: 16px; }
		.node-num { font-size: 19px; }
		.node-name { font-size: 15px; }
		.node-tap { font-size: 16px; }
		.edge-label { font-size: 16px; }
		figcaption { font-size: 0.85rem; }
	}
	@media (prefers-reduced-motion: reduce) {
		.loop-figure, .node, .edge { transition: none; opacity: 1; stroke-dashoffset: 0; }
		.orbit-flow { animation: none; }
	}
</style>
