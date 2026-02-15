<script>
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { sections } from '$lib/data/blueprint.js';
	import { blueprintProgress } from '$lib/stores/progress.js';
	import SavingsCalculator from '$lib/components/SavingsCalculator.svelte';
	import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
	import StackConfigurator from '$lib/components/StackConfigurator.svelte';
	import IndependenceCountdown from '$lib/components/IndependenceCountdown.svelte';
	import FloatingNav from '$lib/components/FloatingNav.svelte';
	import LiveDashboard from '$lib/components/LiveDashboard.svelte';
	import InteractiveStackTable from '$lib/components/InteractiveStackTable.svelte';
	import UrgencyBanner from '$lib/components/UrgencyBanner.svelte';

	const homeSections = [
		{ id: 'brief', label: 'The Brief' },
		{ id: 'situation', label: 'Situation' },
		{ id: 'plan', label: 'The Plan' },
		{ id: 'steps', label: '4 Steps' },
		{ id: 'costs', label: 'Costs' },
		{ id: 'stack', label: 'The Stack' },
		{ id: 'calculator', label: 'Calculator' },
		{ id: 'timeline', label: 'Timeline' },
		{ id: 'chapters', label: 'Blueprint' },
		{ id: 'act', label: 'Act Now' },
	];

	let heroVisible = false;

	function observe(node) {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						entry.target.classList.add('revealed');
						observer.unobserve(entry.target);
					}
				});
			},
			{ threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
		);
		observer.observe(node);
		return { destroy: () => observer.disconnect() };
	}

	function countUp(node, { target, duration = 1600, prefix = '', suffix = '' }) {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						observer.unobserve(entry.target);
						const start = performance.now();
						const numericTarget = parseFloat(target.replace(/[^0-9.]/g, ''));
						function tick(now) {
							const elapsed = now - start;
							const progress = Math.min(elapsed / duration, 1);
							const eased = 1 - Math.pow(1 - progress, 4);
							const current = Math.round(numericTarget * eased);
							node.textContent = prefix + current.toLocaleString() + suffix;
							if (progress < 1) requestAnimationFrame(tick);
							else node.textContent = prefix + target + suffix;
						}
						requestAnimationFrame(tick);
					}
				});
			},
			{ threshold: 0.5 }
		);
		observer.observe(node);
		return { destroy: () => observer.disconnect() };
	}

	function stagger(node, { delay = 80 } = {}) {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						const children = node.children;
						for (let i = 0; i < children.length; i++) {
							children[i].style.transitionDelay = `${i * delay}ms`;
							children[i].classList.add('stagger-in');
						}
						observer.unobserve(entry.target);
					}
				});
			},
			{ threshold: 0.05 }
		);
		observer.observe(node);
		return { destroy: () => observer.disconnect() };
	}

	const chapters = sections.map((s) => ({
		num: s.number,
		title: s.title,
		desc: s.subtitle,
		slug: s.slug,
	}));

	onMount(() => { heroVisible = true; });

	$: progress = $blueprintProgress;
	$: completedCount = Object.values(progress).filter((v) => v.readAt).length;
	$: progressPercent = Math.round((completedCount / chapters.length) * 100);
</script>

<svelte:head>
	<title>Surviving the Singularity — The Blueprint</title>
	<meta name="description" content="A practical blueprint for building real independence. 4 steps, under $150K. Land, shelter, digital income, and local AI — a better path forward." />
	<meta property="og:type" content="website" />
	<meta property="og:title" content="Surviving the Singularity — The Blueprint" />
	<meta property="og:description" content="A practical blueprint for material independence. 4 steps. Under $150K. There's a better way to build your future." />
	<meta name="twitter:card" content="summary_large_image" />
	{@html `<script type="application/ld+json">${JSON.stringify({
		"@context": "https://schema.org",
		"@type": "WebSite",
		"name": "Surviving the Singularity",
		"url": "https://survivingthesingularity.com",
		"description": "A technical blueprint for material independence before AI changes everything."
	})}</script>`}
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
</svelte:head>

<div class="page">
	<FloatingNav sections={homeSections} />
	<UrgencyBanner />

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE BRIEF — This is not a sales page.          -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="hero" id="brief">
		<div class="hero-bg">
			<div class="hero-grid"></div>
			<div class="hero-glow"></div>
		</div>

		{#if heroVisible}
			<div class="hero-content" in:fade={{ duration: 600, delay: 100 }}>
				<div class="hero-classification">
					<span class="classification-dot"></span>
					A PRACTICAL BLUEPRINT FOR WHAT COMES NEXT
				</div>

				<h1 class="hero-title">
					There's a better way<br/>to build your future.
				</h1>

				<p class="hero-subtitle">
					The old playbook — mortgage, career ladder, retire at 65 — was designed for a world that no longer
					exists. AI is rewriting every industry. Housing costs are out of control. But inside that disruption
					is an opportunity most people haven't seen yet.
				</p>

				<p class="hero-question">
					What if you could build <em>real independence</em> for under $150K?
				</p>

				<div class="hero-answer">
					<div class="answer-bar"></div>
					<div class="answer-content">
						<p class="answer-text">
							Buy land. Build a shop. Start a YouTube channel and film everything you make.
							Run your own AI locally. Grow food. Teach your kids to be
							<strong>builders</strong> — not just employees. This is the blueprint.
						</p>
						<p class="answer-cost">
							Total cost: <strong>under $150K</strong>. In some cases, <strong>under $30K</strong>.
						</p>
					</div>
				</div>

				<div class="hero-actions">
					<a href="/blueprint" class="btn-primary">
						Read the Full Blueprint
						<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
					</a>
					<a href="#plan" class="btn-secondary">
						See the 4 Steps
					</a>
				</div>

				{#if completedCount > 0}
					<div class="hero-progress" in:fade={{ delay: 500, duration: 400 }}>
						<div class="progress-bar-bg">
							<div class="progress-bar-fill" style="width: {progressPercent}%"></div>
						</div>
						<span class="progress-label">{completedCount}/{chapters.length} chapters read</span>
					</div>
				{/if}
			</div>
		{/if}
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- SITUATION REPORT — The numbers.                -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section" id="situation" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">01</span>
				<div>
					<h2 class="section-title">The Reality Check</h2>
					<p class="section-desc">The numbers that explain why the old path doesn't work — and why a new one is possible.</p>
				</div>
			</div>

			<div class="stats-grid" use:stagger>
				<div class="stat-card stagger-item stat-danger">
					<span class="stat-number" use:countUp={{ target: '25', suffix: '%' }}>0%</span>
					<span class="stat-label">Dollar purchasing power lost since 2020</span>
				</div>
				<div class="stat-card stagger-item stat-danger">
					<span class="stat-number" use:countUp={{ target: '500', prefix: '$', suffix: 'K' }}>$0K</span>
					<span class="stat-label">Median U.S. home price</span>
				</div>
				<div class="stat-card stagger-item stat-danger">
					<span class="stat-number" use:countUp={{ target: '30', suffix: ' years' }}>0 years</span>
					<span class="stat-label">Standard mortgage commitment</span>
				</div>
				<div class="stat-card stagger-item stat-warning">
					<span class="stat-number" use:countUp={{ target: '51', suffix: '%' }}>0%</span>
					<span class="stat-label">Of all U.S. wealth held by Boomers. You have 10.7%.</span>
				</div>
			</div>

			<div class="situation-block">
				<p>
					A 30-year mortgage on a $500K house means you pay <strong>$1.1 million</strong> total.
					For a structure you leave empty 10 hours a day. Meanwhile, your dollar buys 25% less than
					it did six years ago, and housing inventory is at historic lows.
				</p>
				<p>
					But the same technology disrupting old industries is also creating new leverage.
					A YouTube channel costs $0 to start. Rural land is $5K-$30K. Open-source AI runs on a
					$2K GPU. The tools for independence have never been more accessible.
				</p>
				<p class="situation-punchline">
					The old path is broken. But a better one exists — and it's cheaper than you think.
				</p>
			</div>

			<LiveDashboard />
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE PLAN — 4 steps. That's it.                 -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section section-emphasis" id="plan" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">02</span>
				<div>
					<h2 class="section-title">The Plan</h2>
					<p class="section-desc">Four steps. No fluff. No course to buy. This is a technical specification for a different life.</p>
				</div>
			</div>

			<div class="plan-statement">
				<p class="plan-headline">Adaptability is the new currency.</p>
				<p class="plan-sub">The people who thrive in what's coming won't be the ones with the best degrees or biggest 401Ks. They'll be the ones who can <em>build things</em>, <em>learn fast</em>, and <em>teach others</em>. This blueprint shows you how.</p>
			</div>
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE 4 STEPS — The core of everything.          -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section" id="steps" use:observe>
		<div class="section-inner">
			<div class="steps-grid" use:stagger={{ delay: 150 }}>

				<div class="step-card stagger-item">
					<div class="step-header">
						<span class="step-num">01</span>
						<div class="step-cost">
							<span class="cost-label">Est. cost</span>
							<span class="cost-value">$0</span>
						</div>
					</div>
					<h3 class="step-title">Start a YouTube Channel</h3>
					<p class="step-body">
						This is your economic engine. Film everything you learn, build, and figure out. The
						<strong>One-Hour Rule</strong>: anything that took you more than an hour to learn is
						worth a video. Faceless channels work. Sponsorships fund your build. Donations replace
						your need for venture capital. Your phone is the only equipment you need to start.
					</p>
					<div class="step-tags">
						<span class="step-tag">Revenue: $2K–$20K/mo at scale</span>
						<span class="step-tag">Faceless channels viable</span>
					</div>
					<a href="/blueprint/content-engine" class="step-link">Read the full chapter &rarr;</a>
				</div>

				<div class="step-card stagger-item">
					<div class="step-header">
						<span class="step-num">02</span>
						<div class="step-cost">
							<span class="cost-label">Est. cost</span>
							<span class="cost-value">$5K–$30K</span>
						</div>
					</div>
					<h3 class="step-title">Buy Land</h3>
					<p class="step-body">
						Rural land in the U.S. can be acquired for <strong>$5,000–$30,000</strong> per acre in
						areas with minimal building restrictions. Title 25 "Owner-Built Housing" provisions let
						you build without a general contractor. Butte County, CA — 1-acre parcels for under $15K.
						This is your sovereignty. The foundation of everything else.
					</p>
					<div class="step-tags">
						<span class="step-tag">Title 25 Owner-Built</span>
						<span class="step-tag">No contractor required</span>
					</div>
					<a href="/blueprint/physical-exit" class="step-link">Read the full chapter &rarr;</a>
				</div>

				<div class="step-card stagger-item">
					<div class="step-header">
						<span class="step-num">03</span>
						<div class="step-cost">
							<span class="cost-label">Est. cost</span>
							<span class="cost-value">$25K–$100K</span>
						</div>
					</div>
					<h3 class="step-title">Build a Shop</h3>
					<p class="step-body">
						Not a house — a <strong>shouse</strong>. Shop first, shelter second. A 40×60 red iron
						steel building costs $25–$43/sq ft. The living space inside is a $8,000 partition. Compare
						that to a $500K mortgage. Your shop is your production facility. Your living quarters are
						an efficient afterthought. Flip the domestic hierarchy.
					</p>
					<div class="step-tags">
						<span class="step-tag">$8K living space inside</span>
						<span class="step-tag">Steel > wood frame</span>
					</div>
					<a href="/blueprint/the-shouse" class="step-link">Read the full chapter &rarr;</a>
				</div>

				<div class="step-card stagger-item">
					<div class="step-header">
						<span class="step-num">04</span>
						<div class="step-cost">
							<span class="cost-label">Est. cost</span>
							<span class="cost-value">$2K–$15K</span>
						</div>
					</div>
					<h3 class="step-title">Build, Film, Automate, Teach</h3>
					<p class="step-body">
						Now use the shop. Film your builds for YouTube. Buy tools that make you more autonomous:
						<strong>FarmBot</strong> grows your food. A <strong>$2K GPU</strong> runs local AI that
						nobody controls but you. <strong>Mobile Aloha</strong> automates physical tasks. Do science
						at home. Discover things. Make a living being curious.
						Then teach your kids to do all of it.
					</p>
					<div class="step-tags">
						<span class="step-tag">FarmBot XL: food autonomy</span>
						<span class="step-tag">RTX 5090 + Llama 4: AI sovereignty</span>
					</div>
					<a href="/blueprint/robotics" class="step-link">Read the full chapter &rarr;</a>
				</div>

			</div>

			<div class="steps-total">
				<div class="total-line"></div>
				<div class="total-content">
					<span class="total-label">Total estimated cost</span>
					<span class="total-range">$30,000 – $150,000</span>
					<span class="total-compare">vs. $1.1M for a traditional mortgage</span>
				</div>
				<div class="total-line"></div>
			</div>
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE STACK — What replaces what.                -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section" id="stack" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">03</span>
				<div>
					<h2 class="section-title">The Replacement Stack</h2>
					<p class="section-desc">Every layer of the system that extracts from you — replaced with something you own. Click any row for details.</p>
				</div>
			</div>

			<InteractiveStackTable />
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- CALCULATOR — Run your numbers.                 -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section section-dark" id="calculator" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">04</span>
				<div>
					<h2 class="section-title">Run Your Numbers</h2>
					<p class="section-desc">Input your current housing cost. See what you save with the shouse strategy. This is not theoretical.</p>
				</div>
			</div>
			<SavingsCalculator />
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- YOUR PATH — Personalized configurator.         -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section" id="path" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">05</span>
				<div>
					<h2 class="section-title">Your Path</h2>
					<p class="section-desc">Answer four questions. Get a personalized reading order based on your situation, skills, and goals.</p>
				</div>
			</div>
			<StackConfigurator />
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- TIMELINE — When do you hit independence?        -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section section-dark" id="timeline" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">06</span>
				<div>
					<h2 class="section-title">Your Timeline</h2>
					<p class="section-desc">Input your numbers. See when you reach independence — and how much faster the shouse strategy gets you there.</p>
				</div>
			</div>
			<IndependenceCountdown />
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE FULL BLUEPRINT — 8 chapters.               -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section" id="chapters" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">07</span>
				<div>
					<h2 class="section-title">The Full Blueprint</h2>
					<p class="section-desc">Eight chapters. Every layer of the exit strategy. From the economic analysis to your first week of action.</p>
				</div>
			</div>

			{#if completedCount > 0}
				<div class="chapters-progress">
					<div class="cp-bar-bg">
						<div class="cp-bar-fill" style="width: {progressPercent}%"></div>
					</div>
					<span class="cp-text">{completedCount} of {chapters.length} complete</span>
				</div>
			{/if}

			<div class="chapters-list" use:stagger={{ delay: 60 }}>
				{#each chapters as chapter}
					<a href="/blueprint/{chapter.slug}" class="chapter-row stagger-item" class:chapter-done={progress[chapter.slug]?.readAt}>
						<span class="chapter-num-box" class:chapter-num-done={progress[chapter.slug]?.readAt}>
							{#if progress[chapter.slug]?.readAt}
								<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
							{:else}
								{chapter.num}
							{/if}
						</span>
						<div class="chapter-info">
							<h3 class="chapter-title">{chapter.title}</h3>
							<p class="chapter-desc">{chapter.desc}</p>
						</div>
						<svg class="chapter-arrow" width="18" height="18" viewBox="0 0 18 18" fill="none">
							<path d="M4 9H14M14 9L10 5M14 9L10 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</a>
				{/each}
			</div>
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- ACT NOW — This is not optional.                -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section section-cta" id="act" use:observe>
		<div class="section-inner cta-inner">
			<div class="cta-border"></div>
			<p class="cta-eyebrow">Final directive</p>
			<h2 class="cta-title">
				Real security is not found in status.<br/>
				It is found in solar panels, seeds in the soil,<br/>
				and a human voice on a digital network.
			</h2>
			<p class="cta-body">
				Put yourself through life with your own two hands. Teach your kids the same.
				The window for preparation is measured in years, not decades.
				This blueprint is free. The only cost is action.
			</p>
			<div class="cta-actions">
				<a href="/blueprint" class="btn-primary btn-large">
					Read the Full Blueprint
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
				</a>
				<a href="/book" class="btn-secondary">Read the Book</a>
			</div>

			<div class="cta-newsletter">
				<p class="cta-newsletter-label">Get notified when new chapters drop</p>
				<NewsletterSignup />
			</div>
		</div>
	</section>
</div>

<style>
	/* ═══════════════════════════ */
	/* PAGE & GLOBAL              */
	/* ═══════════════════════════ */
	.page { display: flex; flex-direction: column; }

	.section > .section-inner {
		opacity: 0;
		transform: translateY(24px);
		transition: opacity 0.6s ease, transform 0.6s ease;
	}
	.section.revealed > .section-inner,
	.section:global(.revealed) > .section-inner {
		opacity: 1;
		transform: translateY(0);
	}
	.stagger-item {
		opacity: 0;
		transform: translateY(12px);
		transition: opacity 0.4s ease, transform 0.4s ease;
	}
	:global(.stagger-in) {
		opacity: 1 !important;
		transform: translateY(0) !important;
	}

	/* ═══════════════════════════ */
	/* HERO                       */
	/* ═══════════════════════════ */
	.hero {
		position: relative;
		min-height: 90vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 6rem 2rem 4rem;
		overflow: hidden;
	}

	.hero-bg {
		position: absolute;
		inset: 0;
		background: #020617;
	}

	.hero-grid {
		position: absolute;
		inset: 0;
		background-image:
			linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
			linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
		background-size: 80px 80px;
	}

	.hero-glow {
		position: absolute;
		width: 800px;
		height: 800px;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(239, 68, 68, 0.06), transparent 70%);
		top: -300px;
		right: -200px;
		filter: blur(80px);
	}

	.hero-content {
		position: relative;
		z-index: 2;
		max-width: 860px;
	}

	.hero-classification {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.65rem;
		font-weight: 700;
		color: #ef4444;
		text-transform: uppercase;
		letter-spacing: 0.15em;
		font-family: 'JetBrains Mono', monospace;
		margin-bottom: 2rem;
		padding: 0.4rem 0.8rem;
		background: rgba(239, 68, 68, 0.06);
		border: 1px solid rgba(239, 68, 68, 0.12);
		border-radius: 6px;
	}

	.classification-dot {
		width: 5px;
		height: 5px;
		border-radius: 50%;
		background: #ef4444;
		animation: blink 2s ease-in-out infinite;
	}

	@keyframes blink {
		0%, 100% { opacity: 0.3; }
		50% { opacity: 1; }
	}

	.hero-title {
		font-size: clamp(2rem, 5.5vw, 3.5rem);
		font-weight: 900;
		color: #fafafa;
		line-height: 1.15;
		margin: 0 0 1.5rem 0;
		letter-spacing: -0.04em;
	}

	.hero-subtitle {
		font-size: 1.05rem;
		color: #71717a;
		line-height: 1.75;
		margin: 0 0 1.5rem 0;
		max-width: 700px;
	}

	.hero-question {
		font-size: 1.4rem;
		font-weight: 700;
		color: #fafafa;
		margin: 0 0 1.5rem 0;
	}

	.hero-question em {
		color: #f59e0b;
		font-style: italic;
	}

	.hero-answer {
		display: flex;
		gap: 1rem;
		margin-bottom: 2.5rem;
		padding: 1.5rem;
		background: rgba(245, 158, 11, 0.04);
		border: 1px solid rgba(245, 158, 11, 0.1);
		border-radius: 12px;
	}

	.answer-bar {
		width: 3px;
		background: linear-gradient(180deg, #f59e0b, #f97316);
		border-radius: 2px;
		flex-shrink: 0;
	}

	.answer-text {
		font-size: 1rem;
		color: #d4d4d8;
		line-height: 1.7;
		margin: 0 0 0.75rem 0;
	}

	.answer-text strong {
		color: #fafafa;
		font-weight: 700;
	}

	.answer-cost {
		font-size: 0.9rem;
		color: #a1a1aa;
		margin: 0;
		font-family: 'JetBrains Mono', monospace;
	}

	.answer-cost strong {
		color: #10b981;
		font-weight: 700;
	}

	.hero-actions {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.hero-progress {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-top: 2rem;
	}

	.progress-bar-bg {
		width: 120px;
		height: 4px;
		background: rgba(255, 255, 255, 0.08);
		border-radius: 2px;
		overflow: hidden;
	}

	.progress-bar-fill {
		height: 100%;
		background: linear-gradient(90deg, #f59e0b, #10b981);
		border-radius: 2px;
		transition: width 0.8s ease;
	}

	.progress-label {
		font-size: 0.72rem;
		color: #52525b;
		font-family: 'JetBrains Mono', monospace;
	}

	/* ═══════════════════════════ */
	/* BUTTONS                    */
	/* ═══════════════════════════ */
	.btn-primary {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.85rem 2rem;
		border-radius: 8px;
		font-weight: 700;
		font-size: 0.9rem;
		text-decoration: none;
		background: #fafafa;
		color: #09090b;
		transition: all 0.2s ease;
		cursor: pointer;
	}

	.btn-primary:hover {
		background: #f59e0b;
		transform: translateY(-1px);
		box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
	}

	.btn-secondary {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.85rem 2rem;
		border-radius: 8px;
		font-weight: 600;
		font-size: 0.9rem;
		text-decoration: none;
		background: transparent;
		color: #a1a1aa;
		border: 1px solid rgba(255, 255, 255, 0.08);
		transition: all 0.2s ease;
		cursor: pointer;
	}

	.btn-secondary:hover {
		color: #fafafa;
		border-color: rgba(255, 255, 255, 0.2);
	}

	.btn-large {
		padding: 1rem 2.5rem;
		font-size: 1rem;
	}

	/* ═══════════════════════════ */
	/* SECTIONS                   */
	/* ═══════════════════════════ */
	.section {
		padding: 5rem 1.5rem;
		border-top: 1px solid rgba(255, 255, 255, 0.03);
	}

	.section-dark {
		background: rgba(255, 255, 255, 0.01);
	}

	.section-emphasis {
		background: linear-gradient(180deg, rgba(245, 158, 11, 0.02) 0%, transparent 100%);
		border-top: 1px solid rgba(245, 158, 11, 0.08);
	}

	.section-inner {
		max-width: 960px;
		margin: 0 auto;
	}

	.section-header-row {
		display: flex;
		gap: 1.25rem;
		align-items: flex-start;
		margin-bottom: 2.5rem;
	}

	.section-number {
		font-size: 0.8rem;
		font-weight: 800;
		color: #f59e0b;
		font-family: 'JetBrains Mono', monospace;
		min-width: 30px;
		padding-top: 0.15rem;
		opacity: 0.7;
	}

	.section-title {
		font-size: clamp(1.4rem, 3.5vw, 2rem);
		font-weight: 800;
		color: #fafafa;
		margin: 0 0 0.4rem 0;
		letter-spacing: -0.03em;
	}

	.section-desc {
		color: #71717a;
		font-size: 0.95rem;
		line-height: 1.6;
		margin: 0;
		max-width: 600px;
	}

	/* ═══════════════════════════ */
	/* STATS                      */
	/* ═══════════════════════════ */
	.stats-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 0.75rem;
		margin-bottom: 2.5rem;
	}

	.stat-card {
		padding: 1.5rem;
		border-radius: 10px;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		border: 1px solid rgba(255, 255, 255, 0.04);
		background: rgba(255, 255, 255, 0.02);
	}

	.stat-danger {
		border-color: rgba(239, 68, 68, 0.1);
	}

	.stat-warning {
		border-color: rgba(245, 158, 11, 0.1);
	}

	.stat-number {
		font-size: 1.8rem;
		font-weight: 800;
		font-family: 'JetBrains Mono', monospace;
		letter-spacing: -0.02em;
	}

	.stat-danger .stat-number { color: #ef4444; }
	.stat-warning .stat-number { color: #f59e0b; }

	.stat-label {
		font-size: 0.78rem;
		color: #52525b;
		line-height: 1.4;
	}

	/* ═══════════════════════════ */
	/* SITUATION                  */
	/* ═══════════════════════════ */
	.situation-block {
		max-width: 700px;
		margin-bottom: 2rem;
	}

	.situation-block p {
		color: #a1a1aa;
		font-size: 1rem;
		line-height: 1.8;
		margin: 0 0 1rem 0;
	}

	.situation-block strong {
		color: #fafafa;
		font-weight: 600;
	}

	.situation-block em {
		color: #ef4444;
		font-style: italic;
	}

	.situation-punchline {
		font-size: 1.15rem !important;
		font-weight: 700 !important;
		color: #fafafa !important;
		margin-top: 1.5rem !important;
	}

	/* ═══════════════════════════ */
	/* THE PLAN STATEMENT         */
	/* ═══════════════════════════ */
	.plan-statement {
		max-width: 700px;
	}

	.plan-headline {
		font-size: clamp(1.5rem, 4vw, 2.2rem);
		font-weight: 900;
		color: #fafafa;
		margin: 0 0 1rem 0;
		letter-spacing: -0.03em;
		line-height: 1.2;
	}

	.plan-sub {
		font-size: 1.05rem;
		color: #71717a;
		line-height: 1.75;
		margin: 0;
	}

	.plan-sub em {
		color: #f59e0b;
		font-style: italic;
		font-weight: 600;
	}

	/* ═══════════════════════════ */
	/* 4 STEPS                    */
	/* ═══════════════════════════ */
	.steps-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
		margin-bottom: 3rem;
	}

	.step-card {
		padding: 2rem;
		background: rgba(255, 255, 255, 0.02);
		border: 1px solid rgba(255, 255, 255, 0.04);
		border-radius: 12px;
		transition: all 0.25s ease;
	}

	.step-card:hover {
		border-color: rgba(245, 158, 11, 0.15);
		background: rgba(255, 255, 255, 0.03);
	}

	.step-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 1rem;
	}

	.step-num {
		font-size: 2rem;
		font-weight: 900;
		color: #27272a;
		font-family: 'JetBrains Mono', monospace;
		line-height: 1;
	}

	.step-card:hover .step-num {
		color: rgba(245, 158, 11, 0.2);
	}

	.step-cost {
		text-align: right;
	}

	.cost-label {
		display: block;
		font-size: 0.6rem;
		color: #52525b;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		font-weight: 600;
	}

	.cost-value {
		display: block;
		font-size: 0.9rem;
		font-weight: 700;
		color: #10b981;
		font-family: 'JetBrains Mono', monospace;
	}

	.step-title {
		font-size: 1.15rem;
		font-weight: 700;
		color: #fafafa;
		margin: 0 0 0.75rem 0;
		letter-spacing: -0.01em;
	}

	.step-body {
		font-size: 0.88rem;
		color: #71717a;
		line-height: 1.7;
		margin: 0 0 1rem 0;
	}

	.step-body strong {
		color: #d4d4d8;
		font-weight: 600;
	}

	.step-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
		margin-bottom: 1rem;
	}

	.step-tag {
		font-size: 0.65rem;
		font-weight: 600;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		background: rgba(245, 158, 11, 0.06);
		color: #a1a1aa;
		border: 1px solid rgba(245, 158, 11, 0.08);
		font-family: 'JetBrains Mono', monospace;
	}

	.step-link {
		font-size: 0.82rem;
		font-weight: 600;
		color: #f59e0b;
		text-decoration: none;
		transition: opacity 0.2s;
	}

	.step-link:hover {
		opacity: 0.8;
	}

	/* Steps total */
	.steps-total {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.total-line {
		flex: 1;
		height: 1px;
		background: rgba(255, 255, 255, 0.06);
	}

	.total-content {
		text-align: center;
		flex-shrink: 0;
	}

	.total-label {
		display: block;
		font-size: 0.6rem;
		color: #52525b;
		text-transform: uppercase;
		letter-spacing: 0.12em;
		font-weight: 600;
		margin-bottom: 0.3rem;
	}

	.total-range {
		display: block;
		font-size: 1.8rem;
		font-weight: 900;
		color: #10b981;
		font-family: 'JetBrains Mono', monospace;
		letter-spacing: -0.03em;
	}

	.total-compare {
		display: block;
		font-size: 0.72rem;
		color: #52525b;
		margin-top: 0.2rem;
	}

	/* ═══════════════════════════ */
	/* CHAPTERS LIST              */
	/* ═══════════════════════════ */
	.chapters-progress {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.cp-bar-bg {
		flex: 1;
		max-width: 200px;
		height: 3px;
		background: rgba(255, 255, 255, 0.06);
		border-radius: 2px;
		overflow: hidden;
	}

	.cp-bar-fill {
		height: 100%;
		background: linear-gradient(90deg, #f59e0b, #10b981);
		border-radius: 2px;
		transition: width 0.8s ease;
	}

	.cp-text {
		font-size: 0.72rem;
		color: #52525b;
		font-family: 'JetBrains Mono', monospace;
	}

	.chapters-list {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}

	.chapter-row {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem 1.25rem;
		border: 1px solid rgba(255, 255, 255, 0.03);
		border-radius: 10px;
		text-decoration: none;
		transition: all 0.2s ease;
		background: transparent;
	}

	.chapter-row:hover {
		border-color: rgba(245, 158, 11, 0.12);
		background: rgba(255, 255, 255, 0.015);
	}

	.chapter-done {
		border-color: rgba(16, 185, 129, 0.1);
	}

	.chapter-num-box {
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 8px;
		background: rgba(255, 255, 255, 0.03);
		border: 1px solid rgba(255, 255, 255, 0.05);
		font-size: 0.72rem;
		font-weight: 700;
		color: #52525b;
		font-family: 'JetBrains Mono', monospace;
		flex-shrink: 0;
	}

	.chapter-num-done {
		background: rgba(16, 185, 129, 0.08);
		border-color: rgba(16, 185, 129, 0.15);
		color: #10b981;
	}

	.chapter-info {
		flex: 1;
		min-width: 0;
	}

	.chapter-title {
		font-size: 0.95rem;
		font-weight: 600;
		color: #d4d4d8;
		margin: 0 0 0.15rem 0;
	}

	.chapter-desc {
		font-size: 0.78rem;
		color: #52525b;
		margin: 0;
		line-height: 1.3;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.chapter-arrow {
		color: #27272a;
		flex-shrink: 0;
		transition: all 0.2s;
	}

	.chapter-row:hover .chapter-arrow {
		color: #f59e0b;
		transform: translateX(3px);
	}

	/* ═══════════════════════════ */
	/* CTA                        */
	/* ═══════════════════════════ */
	.section-cta {
		padding: 6rem 1.5rem;
		border-top: 1px solid rgba(239, 68, 68, 0.08);
	}

	.cta-inner {
		text-align: center;
		max-width: 700px;
		position: relative;
	}

	.cta-border {
		width: 40px;
		height: 2px;
		background: #ef4444;
		margin: 0 auto 1.5rem;
	}

	.cta-eyebrow {
		font-size: 0.65rem;
		font-weight: 700;
		color: #ef4444;
		text-transform: uppercase;
		letter-spacing: 0.15em;
		font-family: 'JetBrains Mono', monospace;
		margin: 0 0 1.5rem 0;
	}

	.cta-title {
		font-size: clamp(1.3rem, 3vw, 1.8rem);
		font-weight: 700;
		color: #d4d4d8;
		margin: 0 0 1.5rem 0;
		letter-spacing: -0.02em;
		line-height: 1.5;
	}

	.cta-body {
		color: #52525b;
		font-size: 0.95rem;
		line-height: 1.7;
		margin: 0 0 2.5rem 0;
	}

	.cta-actions {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
	}

	.cta-newsletter {
		margin-top: 3rem;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.cta-newsletter-label {
		font-size: 0.8rem;
		color: #52525b;
		margin: 0 0 0.75rem 0;
	}

	/* ═══════════════════════════ */
	/* RESPONSIVE                 */
	/* ═══════════════════════════ */
	@media (max-width: 768px) {
		.hero {
			min-height: auto;
			padding: 4rem 1.25rem 3rem;
		}

		.hero-actions,
		.cta-actions {
			flex-direction: column;
			align-items: stretch;
		}

		.btn-primary, .btn-secondary {
			justify-content: center;
		}

		.section {
			padding: 3.5rem 1rem;
		}

		.section-header-row {
			flex-direction: column;
			gap: 0;
		}

		.section-number {
			margin-bottom: 0.5rem;
		}

		.steps-grid {
			grid-template-columns: 1fr;
		}

		.step-card {
			padding: 1.5rem;
		}
	}

	@media (max-width: 480px) {
		.hero {
			padding: 3rem 1rem 2.5rem;
		}

		.stats-grid {
			grid-template-columns: repeat(2, 1fr);
		}

		.section {
			padding: 3rem 0.75rem;
		}

		.steps-total {
			flex-direction: column;
			gap: 0.75rem;
		}

		.total-line {
			width: 60px;
			height: 1px;
		}
	}
</style>
