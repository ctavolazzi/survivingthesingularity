<script>
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { sections } from '$lib/data/blueprint.js';
	import { blueprintProgress } from '$lib/stores/progress.js';
	import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
	import BookStatusBanner from '$lib/components/BookStatusBanner.svelte';
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
		{ id: 'stack', label: 'Alternatives' },
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
		<title>Surviving the Singularity</title>
		<meta name="description" content="A field manual for staying agentic as AI rewrites work, money, medicine, and meaning. Open-draft book, full blueprint, and dispatches from the curve." />
		<meta property="og:type" content="website" />
		<meta property="og:title" content="Surviving the Singularity" />
		<meta property="og:description" content="A field manual for staying agentic as AI rewrites work, money, medicine, and meaning." />
		<meta property="og:image" content="/Surviving-the-Singularity-Cover.png" />
		<meta name="twitter:card" content="summary_large_image" />
		<meta name="twitter:image" content="/Surviving-the-Singularity-Cover.png" />
		{@html `<script type="application/ld+json">${JSON.stringify({
			"@context": "https://schema.org",
			"@type": "WebSite",
			"name": "Surviving the Singularity",
			"url": "https://survivingthesingularity.com",
			"description": "A field manual for staying agentic as AI rewrites the way we get our needs met."
		})}</script>`}
	</svelte:head>

<div class="page">
	<FloatingNav sections={homeSections} />
	<UrgencyBanner />

	<!-- ═══════════════════════════════════════════════ -->
	<!-- BOOK STATUS BANNER                              -->
	<!-- ═══════════════════════════════════════════════ -->
	<div class="book-banner-wrap">
		<BookStatusBanner />
	</div>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE BRIEF - This is not a sales page.          -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="hero" id="brief">
		<div class="hero-bg">
			<div class="hero-grid"></div>
			<div class="hero-glow"></div>
		</div>

		{#if heroVisible}
			<div class="hero-content" in:fade={{ duration: 600, delay: 100 }}>
				<div class="hero-classification">
					<svg class="classification-radar" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">
						<circle class="radar-ring radar-ring-1" cx="7" cy="7" r="2" fill="none" stroke="#ef4444" stroke-width="1"/>
						<circle class="radar-ring radar-ring-2" cx="7" cy="7" r="2" fill="none" stroke="#ef4444" stroke-width="1"/>
						<circle class="radar-core" cx="7" cy="7" r="2.2" fill="#ef4444"/>
					</svg>
					A PRACTICAL BLUEPRINT FOR WHAT COMES NEXT
				</div>

				<h1 class="hero-title">
					There are better ways<br/>to build the future.
				</h1>

				<p class="hero-subtitle">
					The old playbook (mortgage, career ladder, retire at 65) was designed for a world that no longer
					exists. AI is rewriting every industry. Housing costs are out of control. But inside that disruption
					is an opportunity most people haven't seen yet.
				</p>

				<p class="hero-question">
					What might <em>a new way of getting our needs met</em> look like at a fraction of the traditional cost?
				</p>

				<div class="hero-answer">
					<div class="answer-bar"></div>
					<div class="answer-content">
						<p class="answer-tagline"><em>Live like your ancestors, with the tools of the modern world.</em></p>
						<p class="answer-text">
							Secure land. Build a shop. Grow food. Learn everything. Teach your kids to be <strong>curious</strong>, not just employees. This is one author's blueprint - for thinking about, not acting on without professional guidance.
						</p>
						<p class="answer-cost">
							Some scenarios in this thought experiment model costs well below a traditional mortgage. <strong>Your real numbers will differ.</strong>
						</p>
					</div>
				</div>

				<div class="hero-actions">
					<a href="/blueprint" class="btn-primary">
						Read the Full Blueprint
						<svg class="shimmer-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
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
	<!-- SITUATION REPORT - The numbers.                -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section" id="situation" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">01</span>
				<div>
					<h2 class="section-title">The Reality Check</h2>
					<p class="section-desc">The numbers that explain why the old path doesn't work - and why a new one is possible.</p>
				</div>
			</div>

			<div class="stats-grid" use:stagger>
				<div class="stat-card stagger-item stat-danger">
					<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
					<span class="stat-number" use:countUp={{ target: '23', suffix: '%' }}>0%</span>
					<span class="stat-label">Cumulative U.S. CPI inflation, Jan 2020-Apr 2026 (approx.)</span>
					<a class="stat-source" href="https://www.bls.gov/cpi/" target="_blank" rel="noopener noreferrer">Source: BLS CPI</a>
				</div>
				<div class="stat-card stagger-item stat-danger">
					<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
					<span class="stat-number" use:countUp={{ target: '420', prefix: '$', suffix: 'K' }}>$0K</span>
					<span class="stat-label">Median U.S. home sale price, recent quarters (approx., varies)</span>
					<a class="stat-source" href="https://fred.stlouisfed.org/series/MSPUS" target="_blank" rel="noopener noreferrer">Source: FRED MSPUS</a>
				</div>
				<div class="stat-card stagger-item stat-danger">
					<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
					<span class="stat-number" use:countUp={{ target: '30', suffix: ' years' }}>0 years</span>
					<span class="stat-label">Standard U.S. fixed-rate mortgage term (typical)</span>
					<a class="stat-source" href="https://www.consumerfinance.gov/owning-a-home/loan-options/" target="_blank" rel="noopener noreferrer">Source: CFPB</a>
				</div>
				<div class="stat-card stagger-item stat-success">
					<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
					<span class="stat-number">~85%</span>
					<span class="stat-label">Drop in U.S. utility-scale solar installed cost, 2010-2023</span>
					<a class="stat-source" href="https://emp.lbl.gov/utility-scale-solar" target="_blank" rel="noopener noreferrer">Source: LBNL / NREL</a>
				</div>
				<div class="stat-card stagger-item stat-success">
					<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
					<span class="stat-number">16M+</span>
					<span class="stat-label">U.S. self-employed workers (incorporated + unincorporated, recent BLS)</span>
					<a class="stat-source" href="https://www.bls.gov/opub/ted/2023/number-of-self-employed-workers-up-from-2020-to-2022.htm" target="_blank" rel="noopener noreferrer">Source: BLS</a>
				</div>
				<div class="stat-card stagger-item stat-success">
					<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
					<span class="stat-number">~$3.6K</span>
					<span class="stat-label">Median U.S. farmland value per acre, 2023 (varies widely by region)</span>
					<a class="stat-source" href="https://www.nass.usda.gov/Publications/Todays_Reports/reports/land0823.pdf" target="_blank" rel="noopener noreferrer">Source: USDA NASS</a>
				</div>
			</div>

			<div class="situation-block">
				<p>
					A standard 30-year mortgage compounds total payments well above the sticker price - exact figures depend on rate, taxes, insurance, and PMI. Dollar purchasing power has eroded materially since 2020 by most reasonable measures. None of these statements should be relied on without checking current data.
				</p>
				<p>
					At the same time, some inputs that matter for a different kind of life have gotten dramatically cheaper or more accessible: utility-scale solar costs, consumer-grade GPUs capable of running local AI models, open-source automation projects, and free creator platforms. Whether any of this is useful for any specific person depends on their situation, and on local laws, codes, and professional advice in their jurisdiction.
				</p>
				<p class="situation-punchline">
					Before acting on any of this, talk to qualified professionals where you live.
				</p>
			</div>

			<LiveDashboard />
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE PLAN - 4 steps. That's it.                 -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section section-emphasis" id="plan" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">02</span>
				<div>
					<h2 class="section-title">The Plan</h2>
					<p class="section-desc">Four steps the author has been thinking about. Not a prescription. Not a recommendation. Material for your own evaluation with qualified professionals.</p>
				</div>
			</div>

			<div class="plan-preflight">
				<p class="plan-preflight-title">⚠ Before anything else: talk to local professionals.</p>
				<p class="plan-preflight-body">
					Every step below depends on jurisdiction, zoning, building code, financing, tax, and personal situation. Before considering any action, talk to <strong>licensed professionals where you live</strong> - a local real-estate attorney, a licensed contractor, an accountant, a financial advisor, and a doctor as relevant. They can tell you what is actually possible, legal, safe, and sensible in your area. Reading this site is not a substitute for any of that. This is informational only.
				</p>
			</div>

			<div class="plan-statement">
				<p class="plan-headline">Adaptability matters more, the faster things change.</p>
					<p class="plan-sub">An author's working hypothesis: that the ability to <em>build</em>, <em>learn</em>, and <em>teach</em> may matter more under accelerating change. Hypothesis, not advice. The plan below is good material for thinking - if and how you apply any of it is a question for you and your professional advisors.</p>
			</div>
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE 4 STEPS - The core of everything.          -->
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
					<h3 class="step-title">Start making content (responsibly)</h3>
					<p class="step-body">
						Public-facing creator work as one possible economic channel. Film what you learn, build, and figure out. The
						<strong>One-Hour Rule</strong>: anything that took you more than an hour to learn could be
						worth a video. <strong>Be responsible:</strong> don't share location, family, financial, or safety-sensitive details you wouldn't want public; mind copyright and platform terms; respect the privacy of others. Most creators earn little or nothing - this is not a business plan.
					</p>
					<p class="step-body">
						Or any platform: <a href="https://substack.com" target="_blank" rel="noopener noreferrer">Substack</a>, Instagram, your own site. Stay cautious. Find your people.
					</p>
					<div class="step-tags">
						<span class="step-tag">Outcomes vary widely</span>
						<span class="step-tag">No income claim</span>
					</div>
					<a href="/blueprint/content-engine" class="step-link">Read more &rarr;</a>
				</div>

				<div class="step-card stagger-item">
					<div class="step-header">
						<span class="step-num">02</span>
						<div class="step-cost">
							<span class="cost-label">Est. cost</span>
							<span class="cost-value">$5K-$30K</span>
						</div>
					</div>
					<h3 class="step-title">Find land or space</h3>
					<p class="step-body">
						Land prices vary enormously by country, region, and parcel. Some rural areas remain affordable; others do not. Owner-builder, reclaimed, refurbished, and adaptive-reuse pathways exist in many jurisdictions worldwide, each with very different legal and code regimes. Before considering any purchase, lease, or build, work with <strong>licensed local professionals</strong> - real-estate attorney, surveyor, contractor, and tax advisor - who actually know your jurisdiction.
					</p>
					<p class="step-body">
						Where possible, consider <strong>reusing or reclaiming existing structures and materials</strong> before new construction. Local builders, salvage yards, and community groups often know what's possible in your area.
					</p>
					<div class="step-tags">
						<span class="step-tag">Local laws vary widely</span>
						<span class="step-tag">Consult licensed professionals</span>
					</div>
					<a href="/blueprint/physical-exit" class="step-link">Read more &rarr;</a>
				</div>

				<div class="step-card stagger-item">
					<div class="step-header">
						<span class="step-num">03</span>
						<div class="step-cost">
							<span class="cost-label">Est. cost</span>
							<span class="cost-value">$25K-$100K</span>
						</div>
					</div>
					<h3 class="step-title">Build a Shop</h3>
					<p class="step-body">
						Not a house - a <strong>shouse</strong>. Shop first, shelter second. Steel building kit prices fluctuate with commodity markets. Habitability conversions are subject to local building codes, occupancy permits, and inspection regimes that vary by county. Consult a licensed contractor and your local permitting authority before estimating any cost.
					</p>
					<div class="step-tags">
						<span class="step-tag">Code varies by county</span>
							<span class="step-tag">Consult a contractor</span>
					</div>
					<a href="/blueprint/the-shouse" class="step-link">Read more &rarr;</a>
				</div>

				<div class="step-card stagger-item">
					<div class="step-header">
						<span class="step-num">04</span>
						<div class="step-cost">
							<span class="cost-label">Est. cost</span>
							<span class="cost-value">$2K-$15K</span>
						</div>
					</div>
					<h3 class="step-title">Build, Film, Automate, Teach</h3>
					<p class="step-body">
						Use the space. Document what you build. Open-source projects worth knowing about include <a href="https://farm.bot/" target="_blank" rel="noopener noreferrer">FarmBot</a> (open-source CNC food-growing), <a href="https://mobile-aloha.github.io/" target="_blank" rel="noopener noreferrer">Mobile Aloha</a> (research bimanual robot), <a href="https://www.llama.com/" target="_blank" rel="noopener noreferrer">Llama</a> and other open-weights language models, and many community automation projects. Consumer GPUs can run capable local models, though specific hardware capability changes constantly. None of this is an endorsement - evaluate fit, safety, and legality for your situation.
					</p>
					<div class="step-tags">
						<span class="step-tag">Open-source projects, varies</span>
						<span class="step-tag">Verify for your context</span>
					</div>
					<a href="/blueprint/robotics" class="step-link">Read more &rarr;</a>
				</div>

			</div>

			<div class="steps-total">
				<div class="total-line"></div>
				<div class="total-content">
					<span class="total-label">Illustrative range</span>
					<span class="total-range">Highly variable</span>
					<span class="total-compare">Your real costs will differ - consult professionals</span>
				</div>
				<div class="total-line"></div>
			</div>
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE STACK - What replaces what.                -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section" id="stack" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">03</span>
				<div>
					<h2 class="section-title">Alternatives to Consider</h2>
					<p class="section-desc">Some systems worth thinking about differently. Each item is a starting point for your own research — not a recommendation. Click any item to read more context.</p>
				</div>
			</div>

			<InteractiveStackTable />
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- TIMELINE - Illustrative scenario explorer.      -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section section-dark" id="timeline" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">04</span>
				<div>
					<h2 class="section-title">Your Timeline</h2>
					<p class="section-desc">Pick your numbers. Rough illustrative arithmetic — not a forecast. For a deeper breakdown with tech products and cost details, explore the full timeline.</p>
				</div>
			</div>
			<IndependenceCountdown />
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════ -->
	<!-- THE FULL BLUEPRINT - 8 chapters.               -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section" id="chapters" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">05</span>
				<div>
					<h2 class="section-title">The Full Blueprint</h2>
					<p class="section-desc">Eight chapters of conjecture and supposition based on one author's research. Not a roadmap. Not a guarantee. A way of thinking about what <em>might</em> be possible — for you to evaluate with qualified professionals in your own situation.</p>
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

			<div class="blueprint-conjecture-notice">
				<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="6" stroke="#94a3b8" stroke-width="1.2"/><path d="M7 4v3.5M7 9.5v.5" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/></svg>
				<p>Everything in this blueprint is <strong>conjecture and supposition</strong> based on one person's research and thinking. It does not represent professional advice of any kind. No outcome is promised, projected, or guaranteed. Treat it as material for your own independent evaluation.</p>
			</div>

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
	<!-- ACT NOW - This is not optional.                -->
	<!-- ═══════════════════════════════════════════════ -->
	<section class="section section-cta" id="act" use:observe>
		<div class="section-inner cta-inner">
			<div class="cta-border"></div>
			<p class="cta-eyebrow">Closing thought</p>
			<h2 class="cta-title">
				A thesis worth considering:<br/>that real security may come from tangible things you understand,<br/>not from status, debt, or systems you don't.
			</h2>
			<p class="cta-body">
				Material from this site is for thinking with, not acting on. Anything you might attempt - land purchases, construction, career changes, financial moves - should be evaluated with the relevant licensed professionals in your jurisdiction.
			</p>
			<div class="cta-actions">
				<a href="/blueprint" class="btn-primary btn-large">
					Read the Full Blueprint
					<svg class="shimmer-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
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
	/* BOOK BANNER WRAPPER        */
	/* ═══════════════════════════ */
	.book-banner-wrap {
		padding: 2rem 1.5rem 0;
		max-width: 960px;
		margin: 0 auto;
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
		animation: hero-glow-breath 9s ease-in-out infinite;
	}

	@keyframes hero-glow-breath {
		0%, 100% { transform: scale(1); opacity: 0.85; }
		50% { transform: scale(1.08); opacity: 1; }
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

	.classification-radar {
		flex-shrink: 0;
		overflow: visible;
	}

	.radar-core {
		transform-origin: 7px 7px;
		animation: radar-core-pulse 2s ease-in-out infinite;
	}

	@keyframes radar-core-pulse {
		0%, 100% { opacity: 0.55; }
		50% { opacity: 1; }
	}

	.radar-ring {
		transform-origin: 7px 7px;
		opacity: 0;
	}

	.radar-ring-1 {
		animation: radar-ping 2.4s ease-out infinite;
	}

	.radar-ring-2 {
		animation: radar-ping 2.4s ease-out 1.2s infinite;
	}

	@keyframes radar-ping {
		0% { transform: scale(1); opacity: 0.7; }
		100% { transform: scale(2.6); opacity: 0; }
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

	.answer-tagline {
		font-size: 1rem;
		font-style: italic;
		color: #fbbf24;
		margin: 0 0 0.85rem 0;
		line-height: 1.5;
		letter-spacing: -0.005em;
	}
	.answer-tagline em { font-style: italic; }

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
		color: #94a3b8;
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
		background: rgba(245, 158, 11, 0.08);
		color: #f59e0b;
		border: 1px solid rgba(245, 158, 11, 0.35);
		transition: all 0.2s ease;
		cursor: pointer;
	}

	.btn-primary:hover {
		background: rgba(245, 158, 11, 0.15);
		border-color: rgba(245, 158, 11, 0.6);
		transform: translateY(-1px);
		box-shadow: 0 4px 20px rgba(245, 158, 11, 0.18);
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
		position: relative;
		padding: 1.5rem;
		border-radius: 10px;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		border: 1px solid rgba(255, 255, 255, 0.04);
		background: rgba(255, 255, 255, 0.02);
	}

	.card-corner {
		position: absolute;
		top: 6px;
		left: 6px;
		opacity: 0;
		transition: opacity 0.5s ease 0.25s;
		color: rgba(255, 255, 255, 0.4);
	}

	.card-corner path {
		stroke-dasharray: 24;
		stroke-dashoffset: 24;
		transition: stroke-dashoffset 0.8s ease 0.4s;
	}

	.stat-card:global(.stagger-in) .card-corner { opacity: 0.7; }
	.stat-card:global(.stagger-in) .card-corner path { stroke-dashoffset: 0; }

	.stat-danger .card-corner { color: #ef4444; }
	.stat-success .card-corner { color: #10b981; }

	.stat-danger {
		border-color: rgba(239, 68, 68, 0.1);
	}

	.stat-success {
		border-color: rgba(16, 185, 129, 0.12);
	}

	.stat-number {
		font-size: 1.8rem;
		font-weight: 800;
		font-family: 'JetBrains Mono', monospace;
		letter-spacing: -0.02em;
	}

	.stat-danger .stat-number { color: #ef4444; }
	.stat-success .stat-number { color: #10b981; }

	.stat-label {
		font-size: 0.78rem;
		color: #94a3b8;
		line-height: 1.4;
	}

	.stat-source {
		display: inline-block;
		margin-top: 0.4rem;
		font-size: 0.62rem;
		color: #94a3b8;
		text-decoration: underline;
		text-underline-offset: 2px;
		font-family: 'JetBrains Mono', monospace;
		letter-spacing: 0.02em;
	}
	.stat-source:hover { color: #94a3b8; }

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
	.plan-preflight {
		max-width: 720px;
		margin: 0 0 2rem 0;
		padding: 1.1rem 1.25rem;
		background: rgba(127, 29, 29, 0.18);
		border: 1px solid rgba(248, 113, 113, 0.35);
		border-radius: 10px;
	}
	.plan-preflight-title {
		font-family: 'JetBrains Mono', monospace;
		font-size: 0.78rem;
		font-weight: 700;
		color: #fecaca;
		margin: 0 0 0.55rem 0;
		letter-spacing: 0.04em;
	}
	.plan-preflight-body {
		font-size: 0.9rem;
		color: #fecaca;
		line-height: 1.7;
		margin: 0;
	}
	.plan-preflight-body strong { color: #fef2f2; }

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
		color: #94a3b8;
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
		color: #94a3b8;
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
		color: #94a3b8;
		margin-top: 0.2rem;
	}

	/* ═══════════════════════════ */
	/* BLUEPRINT CONJECTURE       */
	/* ═══════════════════════════ */
	.blueprint-conjecture-notice {
		display: flex;
		gap: 0.75rem;
		align-items: flex-start;
		padding: 0.9rem 1.1rem;
		background: rgba(148, 163, 184, 0.04);
		border: 1px solid rgba(148, 163, 184, 0.1);
		border-radius: 8px;
		margin-bottom: 1.25rem;
	}
	.blueprint-conjecture-notice svg {
		flex-shrink: 0;
		margin-top: 0.15rem;
	}
	.blueprint-conjecture-notice p {
		font-size: 0.78rem;
		color: #64748b;
		line-height: 1.6;
		margin: 0;
	}
	.blueprint-conjecture-notice strong {
		color: #94a3b8;
		font-weight: 600;
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
		color: #94a3b8;
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
		color: #94a3b8;
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
		color: #94a3b8;
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
		color: #94a3b8;
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
		color: #94a3b8;
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
