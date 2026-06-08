<script>
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { sections } from '$lib/data/blueprint.js';
	import { blueprintProgress } from '$lib/stores/progress.js';
	import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
	import BookStatusBanner from '$lib/components/BookStatusBanner.svelte';
	import FloatingNav from '$lib/components/FloatingNav.svelte';
	import LiveDashboard from '$lib/components/LiveDashboard.svelte';
	import InteractiveStackTable from '$lib/components/InteractiveStackTable.svelte';
	import AGICountdown from '$lib/components/AGICountdown.svelte';

	const homeSections = [
		{ id: 'brief', label: 'Brief' },
		{ id: 'pillars', label: 'Pillars' },
		{ id: 'situation', label: 'Data' },
		{ id: 'plan', label: 'Plan' },
		{ id: 'steps', label: 'Steps' },
		{ id: 'timeline', label: 'Timeline' },
		{ id: 'chapters', label: 'Blueprint' },
		{ id: 'act', label: 'Act' },
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

	const pillars = [
		{
			num: '01',
			label: 'Learn the Tools',
			body: 'Teach yourself to use modern AI. The real leverage is not a subscription. It is understanding these tools well enough to build new ways of getting your needs met.',
			href: '/blueprint/local-ai',
			color: 'amber',
		},
		{
			num: '02',
			label: 'Open-Source Robotics',
			body: 'Automate food production with FarmBot and workshop tasks with open-source robots. Secure your own calories and labor.',
			href: '/blueprint/robotics',
			color: 'blue',
		},
		{
			num: '03',
			label: 'The Physical Exit',
			body: 'Rural land, a shouse workshop, and a digital cash engine. Crush overhead and buy back decades of your life.',
			href: '/blueprint/physical-exit',
			color: 'green',
		},
	];

	const timeline = [
		{ period: '2025–2026', label: 'Learn the Tools', desc: 'Modern AI becomes learnable by anyone. Consumer hardware and open models put real capability within reach of self-taught builders.' },
		{ period: '2026–2027', label: 'Open-Source Robotics', desc: 'Homestead automation becomes accessible. FarmBot, open bimanual arms, and low-cost actuators reach the maker community.' },
		{ period: '2027–2029', label: 'Shouse Economy', desc: 'Housing affordability crisis accelerates the owner-builder and shouse path for families priced out of suburban real estate.' },
		{ period: '2029–2032', label: 'Decentralized Production', desc: 'Networked independent producers coordinate without dependence on fragile global supply chains.' },
	];

	onMount(() => { heroVisible = true; });

	$: progress = $blueprintProgress;
	$: completedCount = Object.values(progress).filter((v) => v.readAt).length;
	$: progressPercent = Math.round((completedCount / chapters.length) * 100);
</script>

<svelte:head>
	<title>Surviving the Singularity</title>
	<meta name="description" content="Practical tools for material independence in the age of AI. Learn the tools, automate with open-source robotics, and build the physical exit: a field manual for what comes next." />
	<meta property="og:type" content="website" />
	<meta property="og:title" content="Surviving the Singularity" />
	<meta property="og:description" content="Practical tools for material independence in the age of AI." />
	<meta property="og:image" content="/Surviving-the-Singularity-Cover.png" />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:image" content="/Surviving-the-Singularity-Cover.png" />
	{@html `<script type="application/ld+json">${JSON.stringify({
		"@context": "https://schema.org",
		"@type": "WebSite",
		"name": "Surviving the Singularity",
		"url": "https://survivingthesingularity.com",
		"description": "Practical tools for material independence in the age of AI."
	})}</script>`}
</svelte:head>

<div class="page">
	<FloatingNav sections={homeSections} />

	<!-- AGI COUNTDOWN -->
	<section class="section section-countdown" use:observe>
		<div class="section-inner">
			<AGICountdown compact />
		</div>
	</section>

	<!-- HERO -->
	<section class="hero" id="brief">
		<div class="hero-bg">
			<div class="hero-grid"></div>
			<div class="hero-glow"></div>
		</div>

		{#if heroVisible}
			<div class="hero-content" in:fade={{ duration: 600, delay: 100 }}>
				<h1 class="hero-title">
					There are better ways to build the future.
				</h1>

				<p class="hero-subtitle">
					The old playbook (mortgage, career ladder, retire at 65) was designed for a world
					that no longer exists. AI is rewriting every industry. Housing costs are out of control.
					But inside that disruption is an opportunity most people haven't seen yet.
				</p>

				<p class="hero-question">
					What might <em>a new way of getting our needs met</em> look like at a fraction of the traditional cost?
				</p>

				<div class="hero-answer">
					<div class="answer-bar"></div>
					<div class="answer-content">
						<p class="answer-tagline"><em>Live like your ancestors, with the tools of the modern world.</em></p>
						<p class="answer-text">
							Secure land. Build a shop. Grow food. Learn everything. Teach your kids to be <strong>curious</strong>, not just employees. This is one author's blueprint, for thinking about, not acting on without professional guidance.
						</p>
						<p class="answer-cost">
							Some scenarios model costs well below a traditional mortgage. <strong>Your real numbers will differ.</strong>
						</p>
					</div>
				</div>

				<div class="hero-actions">
					<a href="/blueprint" class="btn-primary">
						Read the Full Blueprint
						<svg class="shimmer-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
					</a>
					<a href="#pillars" class="btn-secondary">
						See the 3 Pillars
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

	<!-- THREE PILLARS -->
	<section class="section" id="pillars" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">00</span>
				<div>
					<h2 class="section-title">Three Pillars</h2>
					<p class="section-desc">The framework for material independence in the age of AI. Each pillar reinforces the others.</p>
				</div>
			</div>

			<div class="pillars-grid" use:stagger={{ delay: 120 }}>
				{#each pillars as pillar}
					<a href={pillar.href} class="pillar-card stagger-item pillar-{pillar.color}">
						<div class="pillar-num">{pillar.num}</div>
						<h3 class="pillar-label">{pillar.label}</h3>
						<p class="pillar-body">{pillar.body}</p>
						<span class="pillar-link">
							Explore
							<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M3 7H11M11 7L8 4M11 7L8 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
						</span>
					</a>
				{/each}
			</div>
		</div>
	</section>

	<!-- SITUATION REPORT -->
	<section class="section" id="situation" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">01</span>
				<div>
					<h2 class="section-title">The Reality Check</h2>
					<p class="section-desc">The numbers that explain why the old path doesn't work, and why a new one is possible.</p>
				</div>
			</div>

			<div class="stats-grid" use:stagger>
				<div class="stat-card stagger-item stat-danger">
					<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
					<span class="stat-number" use:countUp={{ target: '23', suffix: '%' }}>0%</span>
					<span class="stat-label">Cumulative U.S. CPI inflation, Jan 2020–Apr 2026 (approx.)</span>
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
					<span class="stat-number" use:countUp={{ target: '30', suffix: ' yrs' }}>0 yrs</span>
					<span class="stat-label">Standard U.S. fixed-rate mortgage term (typical)</span>
					<a class="stat-source" href="https://www.consumerfinance.gov/owning-a-home/loan-options/" target="_blank" rel="noopener noreferrer">Source: CFPB</a>
				</div>
				<div class="stat-card stagger-item stat-success">
					<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
					<span class="stat-number">~85%</span>
					<span class="stat-label">Drop in U.S. utility-scale solar installed cost, 2010–2023</span>
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
					A standard 30-year mortgage compounds total payments well above the sticker price; exact figures depend on rate, taxes, insurance, and PMI. Dollar purchasing power has eroded materially since 2020 by most reasonable measures. <strong>None of these statements should be relied on without checking current data.</strong>
				</p>
				<p>
					At the same time, some inputs that matter for a different kind of life have gotten dramatically cheaper or more accessible: utility-scale solar costs, consumer-grade GPUs capable of running local AI models, open-source automation projects, and free creator platforms.
				</p>
				<p class="situation-punchline">
					Before acting on any of this, talk to qualified professionals where you live.
				</p>
			</div>

			<LiveDashboard />
		</div>
	</section>

	<!-- THE PLAN -->
	<section class="section section-emphasis" id="plan" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">02</span>
				<div>
					<h2 class="section-title">The Plan</h2>
					<p class="section-desc">Four steps the author has been thinking about. Not a prescription. Material for your own evaluation with qualified professionals.</p>
				</div>
			</div>

			<div class="plan-preflight">
				<p class="plan-preflight-title">⚠ Before anything else: talk to local professionals.</p>
				<p class="plan-preflight-body">
					Every step below depends on jurisdiction, zoning, building code, financing, tax, and personal situation. Before considering any action, talk to <strong>licensed professionals where you live</strong>: a local real-estate attorney, a licensed contractor, an accountant, a financial advisor. They can tell you what is actually possible, legal, safe, and sensible in your area. Reading this site is not a substitute for any of that.
				</p>
			</div>

			<div class="plan-statement">
				<p class="plan-headline">Adaptability matters more, the faster things change.</p>
				<p class="plan-sub">An author's working hypothesis: that the ability to <em>build</em>, <em>learn</em>, and <em>teach</em> may matter more under accelerating change. Hypothesis, not advice.</p>
			</div>
		</div>
	</section>

	<!-- THE 4 STEPS -->
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
						Public-facing creator work as one possible economic channel. Film what you learn, build, and figure out. The <strong>One-Hour Rule</strong>: anything that took you more than an hour to learn could be worth a video. <strong>Be responsible:</strong> don't share location, family, financial, or safety-sensitive details publicly.
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
							<span class="cost-value">$5K–$30K</span>
						</div>
					</div>
					<h3 class="step-title">Find land or space</h3>
					<p class="step-body">
						Land prices vary enormously by country, region, and parcel. Owner-builder, reclaimed, refurbished, and adaptive-reuse pathways exist in many jurisdictions, each with very different legal and code regimes. Work with <strong>licensed local professionals</strong> before considering any purchase or build.
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
							<span class="cost-value">$25K–$100K</span>
						</div>
					</div>
					<h3 class="step-title">Build a Shop</h3>
					<p class="step-body">
						Not a house. A <strong>shouse</strong>. Shop first, shelter second. Steel building kit prices fluctuate with commodity markets. Habitability conversions are subject to local building codes and inspection regimes that vary by county. Consult a licensed contractor and your local permitting authority first.
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
							<span class="cost-value">$2K–$15K</span>
						</div>
					</div>
					<h3 class="step-title">Build, Film, Automate, Teach</h3>
					<p class="step-body">
						Use the space. Document what you build. Open-source projects worth knowing about include <a href="https://farm.bot/" target="_blank" rel="noopener noreferrer">FarmBot</a> (open-source CNC food-growing), <a href="https://www.llama.com/" target="_blank" rel="noopener noreferrer">Llama</a> and other open-weights language models. None of this is an endorsement; evaluate fit, safety, and legality for your situation.
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
					<span class="total-compare">Your real costs will differ; consult professionals</span>
				</div>
				<div class="total-line"></div>
			</div>
		</div>
	</section>

	<!-- TIMELINE -->
	<section class="section section-timeline" id="timeline" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">03</span>
				<div>
					<h2 class="section-title">The Window</h2>
					<p class="section-desc">One author's hypothesis about how this unfolds. Educated guesses, not forecasts. The window to act is before these become mainstream, not after.</p>
				</div>
			</div>

			<div class="timeline-track" use:stagger={{ delay: 100 }}>
				{#each timeline as item, i}
					<div class="timeline-item stagger-item">
						<div class="timeline-connector">
							<div class="timeline-dot"></div>
							{#if i < timeline.length - 1}
								<div class="timeline-line"></div>
							{/if}
						</div>
						<div class="timeline-body">
							<span class="timeline-period">{item.period}</span>
							<h3 class="timeline-label">{item.label}</h3>
							<p class="timeline-desc">{item.desc}</p>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ALTERNATIVES TO CONSIDER -->
	<section class="section" id="stack" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">04</span>
				<div>
					<h2 class="section-title">Alternatives to Consider</h2>
					<p class="section-desc">Some systems worth thinking about differently. Each item is a starting point for your own research, not a recommendation.</p>
				</div>
			</div>

			<InteractiveStackTable />
		</div>
	</section>

	<!-- THE FULL BLUEPRINT -->
	<section class="section" id="chapters" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<span class="section-number">05</span>
				<div>
					<h2 class="section-title">The Full Blueprint</h2>
					<p class="section-desc">Eight chapters of conjecture and supposition based on one author's research. Not a roadmap. A way of thinking about what <em>might</em> be possible.</p>
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
				<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="6" stroke="#dde4ef" stroke-width="1.2"/><path d="M7 4v3.5M7 9.5v.5" stroke="#dde4ef" stroke-width="1.5" stroke-linecap="round"/></svg>
				<p>Everything in this blueprint is <strong>conjecture and supposition</strong> based on one person's research. No outcome is promised, projected, or guaranteed. Treat it as material for your own independent evaluation.</p>
			</div>

			<div class="chapters-list" use:stagger={{ delay: 60 }}>
				{#each chapters as chapter}
					<a href="/blueprint/{chapter.slug}" class="chapter-row stagger-item" class:chapter-done={progress[chapter.slug]?.readAt}>
						<span class="chapter-num-box" class:chapter-num-done={progress[chapter.slug]?.readAt}>
							{#if progress[chapter.slug]?.readAt}
								<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7L5.5 10.5L12 3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
							{:else}
								{chapter.num}
							{/if}
						</span>
						<div class="chapter-info">
							<h3 class="chapter-title">{chapter.title}</h3>
							<p class="chapter-desc">{chapter.desc}</p>
						</div>
						<svg class="chapter-arrow" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
							<path d="M4 9H14M14 9L10 5M14 9L10 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</a>
				{/each}
			</div>
		</div>
	</section>

	<!-- BOOK STATUS BANNER -->
	<div class="book-banner-wrap">
		<BookStatusBanner />
	</div>

	<!-- CTA -->
	<section class="section section-cta" id="act" use:observe>
		<div class="section-inner cta-inner">
			<div class="cta-border"></div>
			<p class="cta-eyebrow">Closing thought</p>
			<h2 class="cta-title">
				Real security may come from tangible things you understand,<br class="cta-break" /> not from status, debt, or systems you don't.
			</h2>
			<p class="cta-body">
				Material from this site is for thinking with, not acting on. Anything you might attempt (land purchases, construction, career changes, financial moves) should be evaluated with the relevant licensed professionals in your jurisdiction.
			</p>
			<div class="cta-actions">
				<a href="/blueprint" class="btn-primary btn-large">
					Read the Full Blueprint
					<svg class="shimmer-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
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
	/* ═══════════════════════════════════════════════════
	   MOBILE-FIRST: base styles target 320px viewports.
	   Expand up with min-width breakpoints only.
	   Breakpoints: 480px | 640px | 768px | 1024px
	   ═══════════════════════════════════════════════════ */

	/* ── PAGE ── */
	.page { display: flex; flex-direction: column; }

	/* ── REVEAL ANIMATIONS ── */
	.section > .section-inner {
		opacity: 0;
		transform: translateY(24px);
		transition: opacity 0.6s ease, transform 0.6s ease;
	}
	.section:global(.revealed) > .section-inner {
		opacity: 1;
		transform: translateY(0);
	}
	:global(.stagger-item) {
		opacity: 0;
		transform: translateY(12px);
		transition: opacity 0.4s ease, transform 0.4s ease;
	}
	:global(.stagger-in) {
		opacity: 1;
		transform: translateY(0);
	}

	/* ── BOOK BANNER ── */
	.book-banner-wrap {
		padding: 2rem 1rem 0;
		max-width: 960px;
		margin: 0 auto;
		width: 100%;
		box-sizing: border-box;
	}

	/* ── HERO ── */
	.hero {
		position: relative;
		min-height: 80vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 2rem 1rem 1.5rem;
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
		background-size: 60px 60px;
	}

	.hero-glow {
		position: absolute;
		width: 600px;
		height: 600px;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(245, 158, 11, 0.06), transparent 70%);
		top: -200px;
		right: -150px;
		filter: blur(60px);
		animation: hero-glow-breath 9s ease-in-out infinite;
	}

	@keyframes hero-glow-breath {
		0%, 100% { transform: scale(1); opacity: 0.85; }
		50% { transform: scale(1.08); opacity: 1; }
	}

	.hero-content {
		position: relative;
		z-index: 2;
		width: 100%;
		max-width: 860px;
	}

	.hero-classification {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.82rem;
		font-weight: 700;
		color: #fbbf24;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		font-family: var(--font-primary);
		margin-bottom: 1.5rem;
		padding: 0.45rem 0.85rem;
		background: linear-gradient(135deg, rgba(245, 158, 11, 0.14) 0%, rgba(245, 158, 11, 0.04) 100%);
		border: 1px solid rgba(245, 158, 11, 0.3);
		border-radius: 999px;
	}

	.classification-radar { flex-shrink: 0; overflow: visible; }

	.radar-core {
		transform-origin: 7px 7px;
		animation: radar-core-pulse 2s ease-in-out infinite;
	}
	@keyframes radar-core-pulse {
		0%, 100% { opacity: 0.55; }
		50% { opacity: 1; }
	}

	.radar-ring { transform-origin: 7px 7px; opacity: 0; }
	.radar-ring-1 { animation: radar-ping 2.4s ease-out infinite; }
	.radar-ring-2 { animation: radar-ping 2.4s ease-out 1.2s infinite; }
	@keyframes radar-ping {
		0% { transform: scale(1); opacity: 0.7; }
		100% { transform: scale(2.6); opacity: 0; }
	}

	.hero-title {
		font-size: clamp(1.8rem, 7vw, 3.5rem);
		font-weight: 900;
		color: #fafafa;
		line-height: 1.15;
		margin: 0 0 1.25rem;
		text-wrap: balance;
		letter-spacing: -0.04em;
	}

	.hero-subtitle {
		font-size: clamp(0.9rem, 3vw, 1.05rem);
		color: #e9eef5;
		line-height: 1.75;
		margin: 0 0 1.25rem;
		max-width: 700px;
	}

	.hero-question {
		font-size: clamp(1rem, 3.5vw, 1.4rem);
		font-weight: 700;
		color: #fafafa;
		margin: 0 0 1.25rem;
	}
	.hero-question em { color: #f59e0b; font-style: italic; }

	.hero-answer {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		margin-bottom: 2rem;
		padding: 1.25rem;
		background: rgba(245, 158, 11, 0.04);
		border: 1px solid rgba(245, 158, 11, 0.1);
		border-radius: 12px;
	}

	.answer-bar {
		width: 40px;
		height: 3px;
		background: linear-gradient(90deg, #f59e0b, #f97316);
		border-radius: 2px;
		flex-shrink: 0;
	}

	.answer-tagline {
		font-size: 0.95rem;
		font-style: italic;
		color: #fbbf24;
		margin: 0 0 0.75rem;
		line-height: 1.5;
	}

	.answer-text {
		font-size: 0.95rem;
		color: #d4d4d8;
		line-height: 1.7;
		margin: 0 0 0.65rem;
	}
	.answer-text strong { color: #fafafa; font-weight: 700; }

	.answer-cost {
		font-size: 0.85rem;
		color: #e9eef5;
		margin: 0;
		font-family: var(--font-primary);
	}
	.answer-cost strong { color: #10b981; font-weight: 700; }

	.hero-actions {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.hero-progress {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-top: 1.5rem;
	}

	.progress-bar-bg {
		width: 100px;
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
		font-size: 0.8rem;
		color: #dde4ef;
		font-family: var(--font-primary);
	}

	/* ── BUTTONS ── */
	.btn-primary {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		padding: 0.9rem 1.5rem;
		min-height: 48px;
		border-radius: 8px;
		font-weight: 700;
		font-size: 0.9rem;
		text-decoration: none;
		background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
		color: #0a0a0a;
		border: 1px solid #f59e0b;
		box-shadow: 0 4px 16px rgba(245, 158, 11, 0.28);
		transition: filter 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
		cursor: pointer;
	}

	.btn-primary:hover {
		filter: brightness(1.08);
		transform: translateY(-2px);
		box-shadow: 0 10px 30px rgba(245, 158, 11, 0.42);
	}

	.btn-secondary {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		padding: 0.9rem 1.5rem;
		min-height: 48px;
		border-radius: 8px;
		font-weight: 600;
		font-size: 0.9rem;
		text-decoration: none;
		background: transparent;
		color: #e9eef5;
		border: 1px solid rgba(255, 255, 255, 0.08);
		transition: color 0.2s ease, border-color 0.2s ease;
		cursor: pointer;
	}

	.btn-secondary:hover {
		color: #fafafa;
		border-color: rgba(255, 255, 255, 0.2);
	}

	.btn-large { padding: 1rem 2rem; font-size: 1rem; min-height: 52px; }

	/* ── SECTIONS ── */
	.section {
		padding: 1.5rem 1rem;
		border-top: 1px solid rgba(255, 255, 255, 0.03);
	}

	.section-emphasis {
		background: linear-gradient(180deg, rgba(245, 158, 11, 0.02) 0%, transparent 100%);
		border-top: 1px solid rgba(245, 158, 11, 0.08);
	}

	.section-timeline {
		background: linear-gradient(180deg, rgba(59, 130, 246, 0.02) 0%, transparent 100%);
		border-top: 1px solid rgba(59, 130, 246, 0.06);
	}

	.section-cta {
		padding: 2rem 1rem;
		border-top: 1px solid rgba(245, 158, 11, 0.08);
	}

	.section-inner {
		max-width: 960px;
		margin: 0 auto;
		width: 100%;
	}

	.section-header-row {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		margin-bottom: 2rem;
	}

	.section-number {
		font-size: 1.5rem;
		font-weight: 900;
		font-family: var(--font-primary);
		background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
		-webkit-background-clip: text;
		background-clip: text;
		-webkit-text-fill-color: transparent;
		letter-spacing: 0.02em;
		margin-bottom: 0.4rem;
	}

	.section-title {
		font-size: clamp(1.3rem, 4vw, 2rem);
		font-weight: 800;
		color: #fafafa;
		margin: 0 0 0.35rem;
		letter-spacing: -0.03em;
		text-wrap: balance;
	}

	.section-desc {
		color: #e9eef5;
		font-size: 0.9rem;
		line-height: 1.6;
		margin: 0;
		max-width: 600px;
	}

	/* ── THREE PILLARS ── */
	.pillars-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 0.75rem;
	}

	.pillar-card {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
		padding: 1.5rem;
		border-radius: 14px;
		text-decoration: none;
		border: 1px solid rgba(148, 163, 184, 0.14);
		background: linear-gradient(160deg, rgba(30, 41, 59, 0.55) 0%, rgba(15, 23, 42, 0.32) 100%);
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
		transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
		min-height: 44px;
	}

	.pillar-card:hover {
		transform: translateY(-3px);
	}

	.pillar-amber:hover { border-color: rgba(245, 158, 11, 0.5); box-shadow: 0 12px 32px rgba(245, 158, 11, 0.14); }
	.pillar-blue:hover { border-color: rgba(59, 130, 246, 0.5); box-shadow: 0 12px 32px rgba(59, 130, 246, 0.14); }
	.pillar-green:hover { border-color: rgba(16, 185, 129, 0.5); box-shadow: 0 12px 32px rgba(16, 185, 129, 0.14); }

	.pillar-num {
		font-size: 0.9rem;
		font-weight: 800;
		font-family: var(--font-primary);
		letter-spacing: 0.1em;
		opacity: 0.9;
	}

	.pillar-amber .pillar-num { color: #f59e0b; }
	.pillar-blue .pillar-num { color: #3b82f6; }
	.pillar-green .pillar-num { color: #10b981; }

	.pillar-label {
		font-size: 1rem;
		font-weight: 700;
		color: #fafafa;
		margin: 0;
		letter-spacing: -0.01em;
	}

	.pillar-body {
		font-size: 0.88rem;
		color: #e9eef5;
		line-height: 1.65;
		margin: 0;
		flex: 1;
	}

	.pillar-link {
		display: inline-flex;
		align-items: center;
		gap: 0.35rem;
		font-size: 0.86rem;
		font-weight: 600;
		margin-top: 0.25rem;
	}

	.pillar-amber .pillar-link { color: #f59e0b; }
	.pillar-blue .pillar-link { color: #3b82f6; }
	.pillar-green .pillar-link { color: #10b981; }

	/* ── STATS ── */
	.stats-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 0.6rem;
		margin-bottom: 2rem;
	}

	.stat-card {
		position: relative;
		padding: 1.25rem;
		border-radius: 10px;
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
		border: 1px solid rgba(148, 163, 184, 0.12);
		background: linear-gradient(160deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.28) 100%);
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.25);
		transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
	}

	.stat-card:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35); }
	.stat-danger:hover { border-color: rgba(245, 158, 11, 0.4); }
	.stat-success:hover { border-color: rgba(16, 185, 129, 0.4); }

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

	.stat-danger .card-corner { color: #fb923c; }
	.stat-success .card-corner { color: #10b981; }
	.stat-danger { border-color: rgba(245, 158, 11, 0.1); }
	.stat-success { border-color: rgba(16, 185, 129, 0.12); }

	.stat-number {
		font-size: clamp(1.3rem, 4vw, 1.8rem);
		font-weight: 800;
		font-family: var(--font-primary);
		letter-spacing: -0.02em;
	}
	.stat-danger .stat-number { color: #fb923c; }
	.stat-success .stat-number { color: #10b981; }

	.stat-label {
		font-size: 0.82rem;
		color: #dde4ef;
		line-height: 1.4;
	}

	.stat-source {
		display: inline-block;
		margin-top: 0.3rem;
		font-size: 0.82rem;
		color: #dde4ef;
		text-decoration: underline;
		text-underline-offset: 2px;
		font-family: var(--font-primary);
	}

	/* ── SITUATION ── */
	.situation-block { max-width: 700px; margin-bottom: 2rem; }

	.situation-block p {
		color: #e9eef5;
		font-size: 0.95rem;
		line-height: 1.8;
		margin: 0 0 1rem;
	}

	.situation-block strong { color: #fafafa; font-weight: 600; }

	.situation-punchline {
		font-size: 1.05rem;
		font-weight: 700;
		color: #fafafa;
		margin-top: 1.25rem;
	}

	/* ── PLAN STATEMENT ── */
	.plan-preflight {
		max-width: 720px;
		margin: 0 0 1.75rem;
		padding: 1rem;
		background: rgba(120, 53, 15, 0.18);
		border: 1px solid rgba(245, 158, 11, 0.35);
		border-radius: 10px;
	}

	.plan-preflight-title {
		font-family: var(--font-primary);
		font-size: 0.85rem;
		font-weight: 700;
		color: #fde9c8;
		margin: 0 0 0.5rem;
		letter-spacing: 0.04em;
	}

	.plan-preflight-body {
		font-size: 0.88rem;
		color: #fde9c8;
		line-height: 1.7;
		margin: 0;
	}
	.plan-preflight-body strong { color: #fdf6ec; }

	.plan-statement { max-width: 700px; }

	.plan-headline {
		font-size: clamp(1.3rem, 4vw, 2.2rem);
		font-weight: 900;
		color: #fafafa;
		margin: 0 0 0.75rem;
		letter-spacing: -0.03em;
		line-height: 1.2;
	}

	.plan-sub {
		font-size: 1rem;
		color: #e9eef5;
		line-height: 1.75;
		margin: 0;
	}
	.plan-sub em { color: #f59e0b; font-style: italic; font-weight: 600; }

	/* ── 4 STEPS ── */
	.steps-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 0.75rem;
		margin-bottom: 2.5rem;
	}

	.step-card {
		padding: 1.5rem;
		background: linear-gradient(160deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.28) 100%);
		border: 1px solid rgba(148, 163, 184, 0.12);
		border-radius: 14px;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.25);
		transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
	}

	.step-card:hover {
		border-color: rgba(245, 158, 11, 0.4);
		transform: translateY(-3px);
		box-shadow: 0 12px 32px rgba(245, 158, 11, 0.12);
	}

	.step-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 0.85rem;
	}

	.step-num {
		font-size: 1.8rem;
		font-weight: 900;
		color: rgba(245, 158, 11, 0.85);
		font-family: var(--font-primary);
		line-height: 1;
		transition: color 0.2s ease;
	}
	.step-card:hover .step-num { color: #f59e0b; }

	.step-cost { text-align: right; }

	.cost-label {
		display: block;
		font-size: 0.82rem;
		color: #dde4ef;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		font-weight: 600;
	}

	.cost-value {
		display: block;
		font-size: 0.88rem;
		font-weight: 700;
		color: #10b981;
		font-family: var(--font-primary);
	}

	.step-title {
		font-size: 1.05rem;
		font-weight: 700;
		color: #fafafa;
		margin: 0 0 0.65rem;
		letter-spacing: -0.01em;
	}

	.step-body {
		font-size: 0.85rem;
		color: #e9eef5;
		line-height: 1.7;
		margin: 0 0 0.85rem;
	}
	.step-body strong { color: #d4d4d8; font-weight: 600; }

	.step-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem;
		margin-bottom: 0.85rem;
	}

	.step-tag {
		font-size: 0.82rem;
		font-weight: 600;
		padding: 0.2rem 0.45rem;
		border-radius: 4px;
		background: rgba(245, 158, 11, 0.06);
		color: #e9eef5;
		border: 1px solid rgba(245, 158, 11, 0.08);
		font-family: var(--font-primary);
	}

	.step-link {
		font-size: 0.8rem;
		font-weight: 600;
		color: #f59e0b;
		text-decoration: none;
		transition: opacity 0.2s;
	}
	.step-link:hover { opacity: 0.8; }

	.steps-total {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
	}

	.total-line {
		width: 60px;
		height: 1px;
		background: rgba(255, 255, 255, 0.06);
	}

	.total-content { text-align: center; }

	.total-label {
		display: block;
		font-size: 0.82rem;
		color: #dde4ef;
		text-transform: uppercase;
		letter-spacing: 0.12em;
		font-weight: 600;
		margin-bottom: 0.25rem;
	}

	.total-range {
		display: block;
		font-size: 1.5rem;
		font-weight: 900;
		color: #10b981;
		font-family: var(--font-primary);
		letter-spacing: -0.03em;
	}

	.total-compare {
		display: block;
		font-size: 0.8rem;
		color: #dde4ef;
		margin-top: 0.2rem;
	}

	/* ── TIMELINE ── */
	.timeline-track {
		display: flex;
		flex-direction: column;
		gap: 0;
	}

	.timeline-item {
		display: flex;
		gap: 1rem;
	}

	.timeline-connector {
		display: flex;
		flex-direction: column;
		align-items: center;
		flex-shrink: 0;
		padding-top: 0.2rem;
	}

	.timeline-dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
		background: #3b82f6;
		border: 2px solid rgba(59, 130, 246, 0.3);
		flex-shrink: 0;
		box-shadow: 0 0 8px rgba(59, 130, 246, 0.4);
	}

	.timeline-line {
		width: 1px;
		flex: 1;
		background: rgba(59, 130, 246, 0.15);
		margin-top: 4px;
		min-height: 2rem;
	}

	.timeline-body {
		padding-bottom: 2rem;
		flex: 1;
	}

	.timeline-period {
		display: inline-block;
		font-size: 0.76rem;
		font-weight: 700;
		font-family: var(--font-primary);
		color: #3b82f6;
		letter-spacing: 0.06em;
		margin-bottom: 0.35rem;
		padding: 0.15rem 0.5rem;
		background: rgba(59, 130, 246, 0.08);
		border: 1px solid rgba(59, 130, 246, 0.15);
		border-radius: 4px;
	}

	.timeline-label {
		font-size: 1rem;
		font-weight: 700;
		color: #fafafa;
		margin: 0 0 0.4rem;
		letter-spacing: -0.01em;
	}

	.timeline-desc {
		font-size: 0.85rem;
		color: #e9eef5;
		line-height: 1.65;
		margin: 0;
	}

	/* ── BLUEPRINT CONJECTURE ── */
	.blueprint-conjecture-notice {
		display: flex;
		gap: 0.75rem;
		align-items: flex-start;
		padding: 0.85rem 1rem;
		background: rgba(148, 163, 184, 0.04);
		border: 1px solid rgba(148, 163, 184, 0.1);
		border-radius: 8px;
		margin-bottom: 1.25rem;
	}
	.blueprint-conjecture-notice svg { flex-shrink: 0; margin-top: 0.15rem; }
	.blueprint-conjecture-notice p {
		font-size: 0.85rem;
		color: #dde4ef;
		line-height: 1.6;
		margin: 0;
	}
	.blueprint-conjecture-notice strong { color: #dde4ef; font-weight: 600; }

	/* ── CHAPTERS PROGRESS ── */
	.chapters-progress {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1.25rem;
	}

	.cp-bar-bg {
		flex: 1;
		max-width: 160px;
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
		font-size: 0.8rem;
		color: #dde4ef;
		font-family: var(--font-primary);
	}

	/* ── CHAPTERS LIST ── */
	.chapters-list {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}

	.chapter-row {
		display: flex;
		align-items: center;
		gap: 0.85rem;
		padding: 0.85rem 1rem;
		min-height: 52px;
		border: 1px solid rgba(148, 163, 184, 0.1);
		border-radius: 12px;
		text-decoration: none;
		background: linear-gradient(160deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.2) 100%);
		transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease;
	}

	.chapter-row:hover {
		border-color: rgba(245, 158, 11, 0.4);
		transform: translateX(3px);
	}

	.chapter-done { border-color: rgba(16, 185, 129, 0.1); }

	.chapter-num-box {
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 8px;
		background: rgba(255, 255, 255, 0.03);
		border: 1px solid rgba(255, 255, 255, 0.05);
		font-size: 0.8rem;
		font-weight: 700;
		color: #dde4ef;
		font-family: var(--font-primary);
		flex-shrink: 0;
	}

	.chapter-num-done {
		background: rgba(16, 185, 129, 0.08);
		border-color: rgba(16, 185, 129, 0.15);
		color: #10b981;
	}

	.chapter-info { flex: 1; min-width: 0; }

	.chapter-title {
		font-size: 0.9rem;
		font-weight: 600;
		color: #d4d4d8;
		margin: 0 0 0.1rem;
	}

	.chapter-desc {
		font-size: 0.85rem;
		color: #dde4ef;
		margin: 0;
		line-height: 1.3;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.chapter-arrow {
		color: #dde4ef;
		flex-shrink: 0;
		transition: color 0.2s ease, transform 0.2s ease;
	}
	.chapter-row:hover .chapter-arrow { color: #f59e0b; transform: translateX(3px); }

	/* ── CTA ── */
	.cta-inner {
		text-align: center;
		max-width: 700px;
		margin: 0 auto;
		position: relative;
	}

	.cta-border {
		width: 36px;
		height: 2px;
		background: #fb923c;
		margin: 0 auto 1.25rem;
	}

	.cta-eyebrow {
		font-size: 0.82rem;
		font-weight: 700;
		color: #fb923c;
		text-transform: uppercase;
		letter-spacing: 0.15em;
		font-family: var(--font-primary);
		margin: 0 0 1.25rem;
	}

	.cta-title {
		font-size: clamp(1.15rem, 3.5vw, 1.75rem);
		font-weight: 700;
		color: #d4d4d8;
		margin: 0 0 1.25rem;
		letter-spacing: -0.02em;
		line-height: 1.5;
		text-wrap: balance;
	}

	.cta-break { display: none; }

	.cta-body {
		color: #dde4ef;
		font-size: 0.9rem;
		line-height: 1.7;
		margin: 0 0 2rem;
	}

	.cta-actions {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		align-items: stretch;
	}

	.cta-newsletter {
		margin-top: 2.5rem;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.cta-newsletter-label {
		font-size: 0.86rem;
		color: #dde4ef;
		margin: 0 0 0.75rem;
	}

	/* ══════════════════════════════════════════════════════
	   TABLET - 480px+
	   ══════════════════════════════════════════════════════ */
	@media (min-width: 480px) {
		.hero { padding: 4rem 1.25rem 3rem; }
		.section { padding: 3rem 1.25rem; }
		.section-cta { padding: 3.5rem 1.25rem; }

		.hero-answer { flex-direction: row; gap: 1rem; }
		.answer-bar { width: 3px; height: auto; }

		.hero-actions {
			flex-direction: row;
			flex-wrap: wrap;
		}
		.btn-primary, .btn-secondary { flex: 1; min-width: 0; }

		.steps-grid { grid-template-columns: 1fr; }
		.steps-total { flex-direction: row; }
		.total-line { flex: 1; width: auto; }
	}

	/* ══════════════════════════════════════════════════════
	   TABLET - 640px+
	   ══════════════════════════════════════════════════════ */
	@media (min-width: 640px) {
		.hero { padding: 5rem 1.5rem 3.5rem; }
		.section { padding: 3.5rem 1.5rem; }
		.section-cta { padding: 4.5rem 1.5rem; }

		.section-header-row {
			flex-direction: row;
			align-items: flex-start;
			gap: 1.25rem;
		}

		.section-number { padding-top: 0.15rem; min-width: 30px; }

		.hero-actions { flex-direction: row; flex-wrap: wrap; }
		.btn-primary, .btn-secondary { flex: 0 1 auto; }

		.pillars-grid { grid-template-columns: 1fr; }

		.stats-grid { grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }

		.steps-grid { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
		.steps-total { flex-direction: row; }
		.total-line { flex: 1; width: auto; }

		.cta-break { display: inline; }
		.cta-actions { flex-direction: row; justify-content: center; align-items: center; }
		.book-banner-wrap { padding: 2rem 1.5rem 0; }
	}

	/* ══════════════════════════════════════════════════════
	   DESKTOP - 1024px+
	   ══════════════════════════════════════════════════════ */
	@media (min-width: 1024px) {
		.hero { padding: 7rem 2rem 5rem; min-height: 90vh; }
		.hero-grid { background-size: 80px 80px; }
		.hero-glow { width: 800px; height: 800px; top: -300px; right: -200px; }

		.section { padding: 5rem 1.5rem; }
		.section-cta { padding: 6rem 1.5rem; }

		.pillars-grid { grid-template-columns: repeat(3, 1fr); }

		.stats-grid { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }

		.chapter-desc { white-space: nowrap; }
	}

	/* ══════════════════════════════════════════════════════
	   PHONE - tighten vertical rhythm (<480px only; larger
	   screens keep their roomier spacing via min-width blocks)
	   ══════════════════════════════════════════════════════ */
	@media (max-width: 479px) {
		.hero-title { margin: 0 0 0.85rem; }
		.hero-subtitle { margin: 0 0 0.85rem; }
		.hero-question { margin: 0 0 0.85rem; }
		.hero-answer { margin-bottom: 1.25rem; }

		.section-header-row { margin-bottom: 1.1rem; }
		.situation-block { margin-bottom: 1.25rem; }

		.pillars-grid, .steps-grid, .stats-grid { gap: 0.6rem; }
		.pillar-card, .step-card { padding: 1rem; }
		.stat-card { padding: 1rem; }
		.chapter-row { padding: 0.85rem 1rem; }
		.timeline-item { margin-bottom: 1rem; }
	}

	/* ── REDUCED MOTION ── */
	@media (prefers-reduced-motion: reduce) {
		.hero-glow,
		.radar-core,
		.radar-ring-1,
		.radar-ring-2 { animation: none; }
	}
</style>
