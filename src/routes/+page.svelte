<script>
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { sections } from '$lib/data/blueprint.js';
	import { blueprintProgress } from '$lib/stores/progress.js';
	import { jsonLd } from '$lib/utils/jsonld.js';
	import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
	import BookStatusBanner from '$lib/components/BookStatusBanner.svelte';
	import FloatingNav from '$lib/components/FloatingNav.svelte';
	import LiveDashboard from '$lib/components/LiveDashboard.svelte';
	import InteractiveStackTable from '$lib/components/InteractiveStackTable.svelte';
	import AGICountdown from '$lib/components/AGICountdown.svelte';
	import PillarsLoopDiagram from '$lib/components/PillarsLoopDiagram.svelte';
	import DivergenceDiagram from '$lib/components/DivergenceDiagram.svelte';
	import WindowSim from '$lib/components/WindowSim.svelte';

	export let data;

	const homeSections = [
		{ id: 'brief', label: 'Brief' },
		{ id: 'blurb', label: 'The Book' },
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
	{@html `<script type="application/ld+json">${jsonLd({
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
					that no longer exists.
					<span class="hero-subtitle-break">AI is rewriting every industry. Costs are out of control.
					But inside that disruption is an opportunity most people haven't seen yet.</span>
				</p>

				<p class="hero-question">
					What might <em>a new way of getting our needs met</em> look like at a <mark>fraction</mark> of the traditional cost?
				</p>

				<div class="hero-answer">
					<div class="answer-bar"></div>
					<div class="answer-content">
						<p class="answer-tagline"><em>Live like your ancestors, empowered by the tools and tech of our time.</em></p>
						<ul class="answer-list">
							<li>Gain back your autonomy</li>
							<li>Build better systems</li>
							<li>Grow your own food</li>
							<li>Make robots labor for <em>you</em> — not some giant corporation</li>
						</ul>
						<p class="answer-cost">
							There is a new way of life emerging...are you ready?
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

				<p class="hero-site-disclaimer">
					For informational and educational purposes only. Not legal, financial, or professional advice. <a href="/disclaimer">Full disclaimer</a>.
				</p>


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

	<!-- BACK COVER COPY -->
	<section class="section section-blurb" id="blurb" use:observe>
		<div class="section-inner">
			<div class="blurb-card">
				<p class="blurb-eyebrow">Surviving the Singularity</p>

					<p class="blurb-hook">The robots have taken over. Congratulations! You've lost.</p>

					<p class="blurb-body">
						But losing the old world is the exact tactical opening you need to become aware of the one
						that's already here. For millennia, humanity has been the smartest critter on the block.
						That is about to change forever.
					</p>

					<p class="blurb-body">
						The corporate state bureaucrats want to fence this moment behind a digital moat, metering
						your survival while trapping you in a system of debt and surveillance. They think they can
						put a legal collar on a machine god.
					</p>

					<p class="blurb-body blurb-body--em">They are dead wrong.</p>

					<p class="blurb-body">
						If you're looking for a collection of soothing essays or a guide on where to build your
						prepper fortress, this ain't it. This book is an active blueprint for society to change
						its ways before it's too late.
					</p>

					<p class="blurb-body">
						This moment presents our first real opportunity to stop hiding behind fear and insecurity.
						We already possess the technology to solve the problems that have plagued our species since
						the very beginning, yet the powers that be choose doubt at every turn.
					</p>

					<blockquote class="blurb-pullquote">Will the machines make the same choice?</blockquote>

					<p class="blurb-body">
						This book maps a three-stage transition to ensure everyone has what they need to not only
						survive, but thrive at this critical moment.
					</p>

					<p class="blurb-body">
						The endgame isn't making enough money to buy a bunker until this all blows over. We can
						build new systems that secure physical survival on the local level and guarantee our
						children the future they deserve.
					</p>

					<div class="blurb-close">
						<p class="blurb-tools">The tools are on the table.</p>
						<p class="blurb-question-final">Will you continue to hide?</p>
						<p class="blurb-answer-final">
							Or will you face the music, and realize we are finally free to dance again?
						</p>
					</div>

					<div class="blurb-cta">
					<a href="/book" class="btn-primary">
						Read the Book
						<svg class="shimmer-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
					</a>
				</div>
			</div>
		</div>
	</section>

	<!-- EMAIL SIGNUP -->
	<section class="section section-signup" use:observe>
		<div class="section-inner">
			<div class="signup-band">
				<div class="signup-text">
					<img src="/Surviving-the-Singularity-Cover.png" alt="Surviving the Singularity" class="signup-cover" aria-hidden="true" loading="lazy" />
					<div class="signup-text-body">
						<p class="signup-lead">Be first when the book launches.</p>
						<p class="signup-sub">Get the field notes published along the way.</p>
					</div>
				</div>
				<div class="signup-form">
					<NewsletterSignup source="hero" label="" placeholder="your@email.com" buttonText="Get Early Access" />
					{#if data?.signupCount}
						<p class="signup-social-proof">Join <strong>{data.signupCount.toLocaleString()}</strong> readers getting ready.</p>
					{/if}
					<a href="/checklist" class="hero-magnet-link">Or get the free Readiness Checklist →</a>
				</div>
			</div>
		</div>
	</section>

	<!-- THREE PILLARS -->
	<section class="section" id="pillars" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
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

			<PillarsLoopDiagram />
		</div>
	</section>

	<!-- SITUATION REPORT -->
	<section class="section" id="situation" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<div>
					<h2 class="section-title">The Reality Check</h2>
					<p class="section-desc">The numbers that explain why the old path doesn't work, and why a new one is possible.</p>
				</div>
			</div>

			<div class="stats-section" use:stagger>
				<div class="stats-row-label stats-row-label--danger">
					<span class="row-label-line"></span>
					<span class="row-label-text">The Problem</span>
					<span class="row-label-line"></span>
				</div>
				<div class="stats-row stats-row--danger">
					<div class="stat-card stat-danger">
						<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
						<span class="stat-number" use:countUp={{ target: '23', suffix: '%' }}>0%</span>
						<span class="stat-label">Cumulative U.S. CPI inflation, Jan 2020–Apr 2026 (approx.)</span>
						<a class="stat-source" href="https://www.bls.gov/cpi/" target="_blank" rel="noopener noreferrer">Source: BLS CPI</a>
					</div>
					<div class="stat-card stat-danger">
						<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
						<span class="stat-number" use:countUp={{ target: '420', prefix: '$', suffix: 'K' }}>$0K</span>
						<span class="stat-label">Median U.S. home sale price, recent quarters (approx., varies)</span>
						<a class="stat-source" href="https://fred.stlouisfed.org/series/MSPUS" target="_blank" rel="noopener noreferrer">Source: FRED MSPUS</a>
					</div>
					<div class="stat-card stat-danger">
						<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
						<span class="stat-number" use:countUp={{ target: '30', suffix: ' yrs' }}>0 yrs</span>
						<span class="stat-label">Standard U.S. fixed-rate mortgage term (typical)</span>
						<a class="stat-source" href="https://www.consumerfinance.gov/owning-a-home/loan-options/" target="_blank" rel="noopener noreferrer">Source: CFPB</a>
					</div>
				</div>

				<div class="stats-row-label stats-row-label--success">
					<span class="row-label-line"></span>
					<span class="row-label-text">The Opportunity</span>
					<span class="row-label-line"></span>
				</div>
				<div class="stats-row stats-row--success">
					<div class="stat-card stat-success">
						<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
						<span class="stat-number">~85%</span>
						<span class="stat-label">Drop in U.S. utility-scale solar installed cost, 2010–2023</span>
						<a class="stat-source" href="https://emp.lbl.gov/utility-scale-solar" target="_blank" rel="noopener noreferrer">Source: LBNL / NREL</a>
					</div>
					<div class="stat-card stat-success">
						<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
						<span class="stat-number">16M+</span>
						<span class="stat-label">U.S. self-employed workers (incorporated + unincorporated, recent BLS)</span>
						<a class="stat-source" href="https://www.bls.gov/opub/ted/2023/number-of-self-employed-workers-up-from-2020-to-2022.htm" target="_blank" rel="noopener noreferrer">Source: BLS</a>
					</div>
					<div class="stat-card stat-success">
						<svg class="card-corner" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M0 12 L0 1 L12 1" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
						<span class="stat-number">~$3.6K</span>
						<span class="stat-label">Median U.S. farmland value per acre, 2023 (varies widely by region)</span>
						<a class="stat-source" href="https://www.nass.usda.gov/Publications/Todays_Reports/reports/land0823.pdf" target="_blank" rel="noopener noreferrer">Source: USDA NASS</a>
					</div>
				</div>
			</div>

			<DivergenceDiagram />

			<div class="situation-block">
				<p>
					A standard 30-year mortgage compounds total payments well above the sticker price; exact figures depend on rate, taxes, insurance, and PMI. Dollar purchasing power has eroded materially since 2020 by most reasonable measures. <strong>None of these statements should be relied on without checking current data.</strong>
				</p>
				<p>At the same time, some inputs for a different kind of life have gotten dramatically cheaper or more accessible:</p>
				<ul class="answer-list situation-list">
					<li>Utility-scale solar</li>
					<li>Consumer GPUs that run local AI</li>
					<li>Open-source automation projects</li>
					<li>Free creator platforms</li>
				</ul>
				</div>

			<LiveDashboard />
		</div>
	</section>

	<!-- LEAD MAGNET BAND -->
	<section class="section" use:observe>
		<div class="section-inner">
			<a href="/checklist" class="magnet-band">
				<div class="magnet-text">
					<p class="magnet-eyebrow">Free · Start today</p>
					<h2 class="magnet-title">The Singularity Readiness Checklist</h2>
					<p class="magnet-sub">Twelve concrete moves to build independence before AGI reprices everything. See the first three free.</p>
				</div>
				<span class="magnet-cta">
					Get the Checklist
					<svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
				</span>
			</a>
		</div>
	</section>

	<!-- THE PLAN -->
	<section class="section section-emphasis" id="plan" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<div>
					<h2 class="section-title">The Plan</h2>
					<p class="section-desc">Four steps the author has been thinking about.</p>
				</div>
			</div>

			<div class="plan-statement">
				<p class="plan-headline">Adaptability matters more, the faster things change.</p>
				<p class="plan-sub">An author's working hypothesis: that the ability to <em>build</em>, <em>learn</em>, and <em>teach</em> may matter more under accelerating change.</p>
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
						One possible economic channel: film what you learn, build, and figure out. The <strong>One-Hour Rule</strong> — if it took you more than an hour to learn, it could be a video.
					</p>
					<p class="step-caveat">Be responsible: don't share location, family, financial, or safety-sensitive details publicly.</p>
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
						Land prices vary enormously by region and parcel. Owner-builder, reclaimed, refurbished, and adaptive-reuse pathways exist in many places.
					</p>
					<p class="step-caveat">Each carries very different legal and code regimes. Work with licensed local professionals before any purchase or build.</p>
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
						Not a house. A <strong>shouse</strong> — shop first, shelter second. Steel kit prices swing with commodity markets.
					</p>
					<p class="step-caveat">Habitability conversions face local codes and inspections that vary by county. Consult a licensed contractor and your permitting authority first.</p>
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
						Use the space. Document what you build. Open-source projects worth knowing: <a href="https://farm.bot/" target="_blank" rel="noopener noreferrer">FarmBot</a> (CNC food-growing), <a href="https://www.llama.com/" target="_blank" rel="noopener noreferrer">Llama</a> and other open-weight models.
					</p>
					<p class="step-caveat">Not an endorsement — evaluate fit, safety, and legality for your situation.</p>
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

			<WindowSim />
		</div>
	</section>

	<!-- ALTERNATIVES TO CONSIDER -->
	<section class="section" id="stack" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
				<div>
					<h2 class="section-title">Alternatives to Consider</h2>
					<p class="section-desc">Some systems worth thinking about differently.</p>
				</div>
			</div>

			<InteractiveStackTable />
		</div>
	</section>

	<!-- THE FULL BLUEPRINT -->
	<section class="section" id="chapters" use:observe>
		<div class="section-inner">
			<div class="section-header-row">
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
				<p class="cta-newsletter-label">Get notified when the book drops. No spam, no noise.</p>
				<NewsletterSignup source="footer-cta" label="" buttonText="Get Early Access" />
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

	/* ── MARK EMPHASIS ── */
	/* Light amber emphasis — no box, no underline (both read as link/button). */
	mark {
		background: none;
		color: #fbbf24;
		font-weight: 700;
		text-decoration: none;
	}

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
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding: 1.25rem 1rem 1.5rem;
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

	.hero-subtitle-break {
		display: block;
		margin-top: 0.6rem;
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

	.answer-list {
		list-style: none;
		padding: 0;
		margin: 0 0 0.9rem;
		display: flex;
		flex-direction: column;
		gap: 0.55rem;
	}
	.answer-list li {
		position: relative;
		padding-left: 1.35rem;
		font-size: 0.95rem;
		color: #e2e8f0;
		line-height: 1.45;
	}
	.answer-list li::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0.55em;
		width: 6px;
		height: 6px;
		border-radius: 1px;
		background: #f59e0b;
		transform: rotate(45deg);
	}
	.answer-list li :global(em) {
		color: #fbbf24;
		font-style: normal;
		font-weight: 700;
	}

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

	.hero-signup {
		margin-top: 1.75rem;
		width: 100%;
		max-width: 460px;
		padding-top: 1.5rem;
		border-top: 1px solid rgba(148, 163, 184, 0.1);
	}

	.hero-signup-lead {
		font-size: 0.92rem;
		font-weight: 600;
		color: #cbd5e1;
		margin: 0 0 0.85rem;
		line-height: 1.45;
	}

	.hero-social-proof {
		font-size: 0.84rem;
		color: #94a3b8;
		margin: 0.75rem 0 0;
	}
	.hero-social-proof strong { color: #f59e0b; font-weight: 700; }

	.hero-magnet-link {
		display: inline-block;
		margin-top: 0.85rem;
		font-size: 0.86rem;
		font-weight: 600;
		color: #f59e0b;
		text-decoration: none;
		transition: opacity 0.15s ease;
	}
	.hero-magnet-link:hover { opacity: 0.8; text-decoration: underline; text-underline-offset: 3px; }

	/* ── EMAIL SIGNUP BAND ── */
	.section-signup {
		padding-top: 0;
		border-top: none;
	}

	.signup-band {
		max-width: 720px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
		padding: 1.75rem 1.25rem;
		background: rgba(245, 158, 11, 0.04);
		border: 1px solid rgba(245, 158, 11, 0.12);
		border-top: none;
		border-radius: 0 0 18px 18px;
	}

	.signup-text {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 0.85rem;
	}

	.signup-cover {
		width: 56px;
		flex-shrink: 0;
		height: auto;
		border-radius: 4px;
		box-shadow: 0 4px 12px rgba(0,0,0,0.5), 2px 2px 0 rgba(245,158,11,0.1);
	}

	.signup-text-body { display: flex; flex-direction: column; gap: 0.2rem; }

	.signup-lead {
		font-size: 1rem;
		font-weight: 700;
		color: #f1f5f9;
		margin: 0;
	}

	.signup-sub {
		font-size: 0.9rem;
		color: #94a3b8;
		margin: 0;
	}

	.signup-form { display: flex; flex-direction: column; gap: 0.5rem; }

	.signup-social-proof {
		font-size: 0.84rem;
		color: #94a3b8;
		margin: 0.25rem 0 0;
	}
	.signup-social-proof strong { color: #f59e0b; font-weight: 700; }

	@media (min-width: 640px) {
		.signup-band {
			flex-direction: row;
			align-items: flex-start;
			padding: 1.75rem 2.5rem;
		}
		.signup-text { flex: 1; }
		.signup-form { flex: 1.2; }
	}

	/* ── LEAD MAGNET BAND ── */
	.magnet-band {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1.5rem;
		flex-wrap: wrap;
		padding: 1.75rem 2rem;
		background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(249, 115, 22, 0.05));
		border: 1px solid rgba(245, 158, 11, 0.3);
		border-radius: 16px;
		text-decoration: none;
		transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
	}
	.magnet-band:hover {
		border-color: rgba(245, 158, 11, 0.55);
		transform: translateY(-2px);
		box-shadow: 0 12px 40px rgba(245, 158, 11, 0.12);
	}

	.magnet-text { flex: 1 1 320px; }

	.magnet-eyebrow {
		font-family: var(--font-primary, 'JetBrains Mono', monospace);
		font-size: 0.74rem;
		font-weight: 700;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: #f59e0b;
		margin: 0 0 0.5rem;
	}

	.magnet-title {
		font-size: clamp(1.25rem, 3vw, 1.6rem);
		font-weight: 800;
		color: #f1f5f9;
		letter-spacing: -0.02em;
		margin: 0 0 0.5rem;
		line-height: 1.2;
	}

	.magnet-sub {
		font-size: 0.94rem;
		color: #94a3b8;
		line-height: 1.5;
		margin: 0;
	}

	.magnet-cta {
		flex-shrink: 0;
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.8rem 1.5rem;
		background: linear-gradient(135deg, #f59e0b, #f97316);
		color: #0f172a;
		font-weight: 800;
		font-size: 0.92rem;
		border-radius: 10px;
		white-space: nowrap;
		transition: transform 0.2s ease;
	}
	.magnet-band:hover .magnet-cta { transform: translateX(3px); }

	.hero-site-disclaimer {
		margin: 1.25rem 0 0;
		font-size: 0.8rem;
		color: #64748b;
		line-height: 1.5;
	}
	.hero-site-disclaimer a {
		color: #94a3b8;
		text-decoration: underline;
		text-underline-offset: 2px;
	}
	.hero-site-disclaimer a:hover { color: #f59e0b; }

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
		padding: 2.5rem 1.25rem;
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

	.section-countdown {
		padding-top: 1rem;
		padding-bottom: 1rem;
	}

	.section-inner {
		max-width: 960px;
		margin: 0 auto;
		width: 100%;
	}

	.section-header-row {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 2.5rem;
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

	/* ── BACK COVER BLURB ── */
	.section-blurb {
		background: linear-gradient(180deg, rgba(245, 158, 11, 0.03) 0%, transparent 100%);
		border-top: 1px solid rgba(245, 158, 11, 0.12);
	}

	.blurb-card {
		max-width: 720px;
		margin: 0 auto;
		padding: 1.75rem 1.25rem 1.75rem;
		background: linear-gradient(160deg, rgba(30, 41, 59, 0.55) 0%, rgba(15, 23, 42, 0.35) 100%);
		border: 1px solid rgba(245, 158, 11, 0.18);
		border-radius: 18px;
		box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.06), 0 24px 64px rgba(0, 0, 0, 0.4);
	}

	.blurb-eyebrow {
		font-family: var(--font-primary);
		font-size: 0.76rem;
		font-weight: 700;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: #f59e0b;
		margin: 0 0 1.25rem;
	}

	.blurb-hook {
		font-size: clamp(1.35rem, 4vw, 2rem);
		font-weight: 900;
		color: #fafafa;
		line-height: 1.15;
		letter-spacing: -0.03em;
		margin: 0 0 1.5rem;
		text-wrap: balance;
	}

	.blurb-body {
		font-size: 0.97rem;
		color: #e2e8f0;
		line-height: 1.8;
		margin: 0 0 1rem;
	}

	.blurb-body--em {
		font-size: 1.1rem;
		font-weight: 900;
		color: #fbbf24;
		letter-spacing: -0.01em;
	}

	.blurb-pullquote {
		margin: 1.5rem 0;
		padding: 1rem 1.25rem;
		border-left: 3px solid #f59e0b;
		background: rgba(245, 158, 11, 0.06);
		border-radius: 0 8px 8px 0;
		font-size: clamp(1rem, 2.5vw, 1.2rem);
		font-weight: 700;
		font-style: italic;
		color: #f1f5f9;
		line-height: 1.4;
	}

	.blurb-close {
		border-top: 1px solid rgba(245, 158, 11, 0.12);
		margin-top: 1.5rem;
		padding-top: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.blurb-tools {
		font-size: 1rem;
		font-weight: 700;
		color: #fafafa;
		margin: 0;
		letter-spacing: -0.01em;
	}

	.blurb-question-final {
		font-size: 1.05rem;
		font-weight: 700;
		color: #f1f5f9;
		margin: 0;
	}

	.blurb-answer-final {
		font-size: clamp(1rem, 3vw, 1.3rem);
		font-weight: 900;
		color: #f59e0b;
		line-height: 1.3;
		margin: 0.25rem 0 0;
		letter-spacing: -0.02em;
		text-wrap: balance;
	}

	.blurb-cta {
		margin-top: 2rem;
		display: flex;
	}

	@media (min-width: 640px) {
		.blurb-card {
			padding: 2.5rem 2.5rem 2rem;
		}
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
	.stats-section {
		margin-bottom: 2rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.stats-row {
		display: grid;
		grid-template-columns: 1fr;
		gap: 0.6rem;
	}

	.stats-row-label {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-top: 0.5rem;
	}

	.row-label-line {
		flex: 1;
		height: 1px;
	}

	.row-label-text {
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		white-space: nowrap;
	}

	.stats-row-label--danger .row-label-line { background: rgba(251, 146, 60, 0.25); }
	.stats-row-label--danger .row-label-text { color: #fb923c; }
	.stats-row-label--success .row-label-line { background: rgba(16, 185, 129, 0.25); }
	.stats-row-label--success .row-label-text { color: #10b981; }

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
		margin: 0 0 0.6rem;
	}
	.step-body strong { color: #d4d4d8; font-weight: 600; }

	.step-caveat {
		font-size: 0.74rem;
		color: #8a96a6;
		line-height: 1.55;
		margin: 0 0 0.85rem;
		padding-left: 0.65rem;
		border-left: 2px solid rgba(148, 163, 184, 0.18);
	}
	.step-caveat :global(a) { color: inherit; text-decoration: underline; }

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
		.hero { padding: 3rem 1.25rem 2rem; }
		.section { padding: 2.5rem 1.25rem; }
		.section-cta { padding: 3rem 1.25rem; }

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
		.hero { padding: 4rem 1.5rem 3rem; }
		.section { padding: 3rem 1.5rem; }
		.section-cta { padding: 4rem 1.5rem; }

		.section-header-row {
			flex-direction: row;
			align-items: flex-start;
			gap: 1.25rem;
		}


		.hero-actions { flex-direction: row; flex-wrap: wrap; }
		.btn-primary, .btn-secondary { flex: 0 1 auto; }

		.pillars-grid { grid-template-columns: 1fr; }

		.stats-row { grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }

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
		.hero { padding: 5rem 2rem 4rem; }
		.hero-grid { background-size: 80px 80px; }
		.hero-glow { width: 800px; height: 800px; top: -300px; right: -200px; }

		.section { padding: 4rem 2rem; }
		.section-countdown { padding: 2rem 2rem 1rem; }
		.section-cta { padding: 5rem 2rem; }

		.section-inner { max-width: 1100px; }

		.pillars-grid { grid-template-columns: repeat(3, 1fr); }

		.stats-row { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }

		.steps-grid { grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }

		.chapter-desc { white-space: nowrap; }
	}

	@media (min-width: 1280px) {
		.hero { padding: 6rem 3rem 5rem; }
		.section { padding: 5rem 3rem; }
		.section-countdown { padding: 2.5rem 3rem 1rem; }
		.section-cta { padding: 6rem 3rem; }
		.section-inner { max-width: 1200px; }
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

		.pillars-grid, .steps-grid, .stats-row { gap: 0.6rem; }
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
