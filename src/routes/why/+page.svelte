<script>
	import { onMount } from 'svelte';
	import { fade, fly } from 'svelte/transition';

	let visible = false;

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

	const timeline = [
		{ year: '2017', event: 'Transformer architecture invented at Google', impact: 'The architecture behind every modern AI', source: 'Attention Is All You Need — Vaswani et al.' },
		{ year: '2020', event: 'GPT-3 demonstrates emergent reasoning', impact: '175B parameters. Few-shot learning surprises researchers.', source: 'OpenAI' },
		{ year: '2022', event: 'ChatGPT reaches 100M users in 2 months', impact: 'Fastest-growing consumer application in history', source: 'Reuters' },
		{ year: '2023', event: 'GPT-4 passes bar exam, medical boards, CPA exam', impact: 'AI outperforms 90th percentile of human professionals', source: 'OpenAI Technical Report' },
		{ year: '2024', event: 'Claude, Gemini, and open-source models reach near-expert level', impact: 'AI coding, writing, and analysis becomes routine', source: 'Multiple benchmarks' },
		{ year: '2025', event: 'AI agents begin automating multi-step workflows', impact: 'AI doesn\'t just answer — it acts', source: 'Anthropic, OpenAI, Google' },
		{ year: '2027', event: 'Projected: AI matches median human performance broadly', impact: 'Leopold Aschenbrenner\'s "Situational Awareness" timeline', source: 'situational-awareness.ai' },
		{ year: '2030', event: 'Projected: Artificial General Intelligence', impact: 'Multiple credible researchers predict AGI by this date', source: 'Metaculus, Kurzweil, Hinton' },
	];

	const voices = [
		{
			name: 'Leopold Aschenbrenner',
			role: 'Former OpenAI researcher',
			quote: 'We are on the cusp of the most significant technological transformation in human history. By 2027, AI systems will likely be able to do the work of an AI researcher — and then the intelligence explosion begins.',
			source: 'Situational Awareness (2024)',
			url: 'https://situational-awareness.ai/',
			key: true
		},
		{
			name: 'Geoffrey Hinton',
			role: 'Turing Award winner, "Godfather of AI"',
			quote: 'These things will be more intelligent than us. We need to think about how to deal with that.',
			source: 'Interview after leaving Google (2023)',
			url: 'https://www.bbc.com/news/world-us-canada-65452940',
			key: true
		},
		{
			name: 'Ray Kurzweil',
			role: 'Inventor, futurist, Google Director of Engineering',
			quote: 'By 2029, computers will have human-level intelligence... The singularity — the moment when AI surpasses human intelligence — will happen by 2045.',
			source: 'The Singularity Is Nearer (2024)',
			url: 'https://en.wikipedia.org/wiki/The_Singularity_Is_Nearer',
			key: false
		},
		{
			name: 'Dario Amodei',
			role: 'CEO of Anthropic',
			quote: 'I think it is quite likely that we\'ll have systems that are broadly as capable as humans at intellectual work within 2-3 years.',
			source: 'Public statements (2024)',
			url: 'https://www.anthropic.com',
			key: false
		},
		{
			name: 'Sam Altman',
			role: 'CEO of OpenAI',
			quote: 'The intelligence age will be the most transformative and potentially dangerous era in human history. It will also be the most wonderful.',
			source: 'Blog post (2024)',
			url: 'https://blog.samaltman.com/',
			key: false
		},
		{
			name: 'Ilya Sutskever',
			role: 'Co-founder of OpenAI, founder of Safe Superintelligence Inc.',
			quote: 'The things we are building are going to be incredibly powerful. We need to take the issue of safety seriously.',
			source: 'NeurIPS keynote',
			url: 'https://www.ssi.inc',
			key: false
		}
	];

	const capabilities = [
		{ task: 'Legal bar exam', human: '68%', ai: '90%', winner: 'ai', year: '2023' },
		{ task: 'Medical diagnosis (radiology)', human: '87%', ai: '94%', winner: 'ai', year: '2024' },
		{ task: 'Code generation (HumanEval)', human: '~100%', ai: '97%', winner: 'tie', year: '2024' },
		{ task: 'Scientific reasoning (GPQA)', human: '65%', ai: '59%', winner: 'human', year: '2024' },
		{ task: 'Creative writing (blind test)', human: '46%', ai: '54%', winner: 'ai', year: '2024' },
		{ task: 'Mathematical reasoning (MATH)', human: '90%', ai: '96%', winner: 'ai', year: '2025' },
	];

	onMount(() => { visible = true; });
</script>

<svelte:head>
	<title>Why This Matters — The Singularity, Explained | Surviving the Singularity</title>
	<meta name="description" content="The evidence for artificial superintelligence is overwhelming. Here's what the top researchers are saying — and what you can do about it." />
	<meta property="og:title" content="Why This Matters — The Singularity, Explained" />
	<meta property="og:description" content="The evidence for artificial superintelligence is overwhelming. Here's what you can do about it." />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
</svelte:head>

<div class="page">

	<!-- HERO: OPENING STATEMENT -->
	<section class="hero">
		<div class="hero-bg">
			<div class="hero-grid"></div>
		</div>
		{#if visible}
			<div class="hero-content" in:fade={{ duration: 600 }}>
				<a href="/" class="back-link">← Back to Blueprint</a>

				<div class="hero-badge">
					<span class="badge-dot"></span>
					UNDERSTANDING THE SINGULARITY
				</div>

				<h1 class="hero-title">
					This isn't science fiction.<br/>
					<span class="hero-accent">It's happening now.</span>
				</h1>

				<p class="hero-sub">
					The world's top AI researchers — the people actually building these systems — agree:
					artificial intelligence will match and then exceed human-level capability across every domain
					within the next 3-10 years. Here's the evidence, in their own words.
				</p>

				<div class="hero-scroll">
					<span>Scroll to explore the evidence</span>
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
						<path d="M8 3V13M8 13L4 9M8 13L12 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
				</div>
			</div>
		{/if}
	</section>

	<!-- SECTION 1: THE TIMELINE -->
	<section class="section" use:observe>
		<div class="section-inner">
			<div class="section-label">01 — THE EVIDENCE</div>
			<h2 class="section-title">The acceleration is measurable.</h2>
			<p class="section-desc">
				Each year, AI capabilities that experts predicted were decades away arrive months later.
				This isn't hype — it's published research with reproducible results.
			</p>

			<div class="timeline" use:stagger={{ delay: 100 }}>
				{#each timeline as item, i}
					<div class="timeline-item stagger-item" class:timeline-future={parseInt(item.year) > 2025}>
						<div class="timeline-year">{item.year}</div>
						<div class="timeline-body">
							<h3 class="timeline-event">{item.event}</h3>
							<p class="timeline-impact">{item.impact}</p>
							<span class="timeline-source">{item.source}</span>
						</div>
						{#if parseInt(item.year) > 2025}
							<span class="projected-badge">PROJECTED</span>
						{/if}
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- SECTION 2: THE VOICES -->
	<section class="section section-dark" use:observe>
		<div class="section-inner">
			<div class="section-label">02 — THE VOICES</div>
			<h2 class="section-title">What the builders themselves are saying.</h2>
			<p class="section-desc">
				These aren't journalists or pundits. These are the people building the most powerful AI systems
				on Earth — and they're all saying the same thing.
			</p>

			<div class="quotes-grid" use:stagger={{ delay: 120 }}>
				{#each voices as person}
					<div class="quote-card stagger-item" class:quote-key={person.key}>
						<blockquote class="quote-text">"{person.quote}"</blockquote>
						<div class="quote-attribution">
							<div class="quote-name">{person.name}</div>
							<div class="quote-role">{person.role}</div>
							<div class="quote-source">
								{person.source}
								<a href={person.url} target="_blank" rel="noopener noreferrer" class="quote-link">Read →</a>
							</div>
						</div>
					</div>
				{/each}
			</div>

			<div class="callout-box" use:observe>
				<div class="callout-icon">
					<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
						<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
					</svg>
				</div>
				<div class="callout-content">
					<h3 class="callout-title">Recommended Reading</h3>
					<p class="callout-text">
						<strong><a href="https://situational-awareness.ai/" target="_blank" rel="noopener noreferrer">Situational Awareness</a></strong>
						by Leopold Aschenbrenner is the single most important document written about AI in 2024.
						A former OpenAI superalignment researcher lays out — with receipts — exactly why AGI is likely
						by 2027, what that means for the world, and why almost nobody is prepared.
					</p>
					<p class="callout-read-time">~2 hour read. Worth every minute.</p>
				</div>
			</div>
		</div>
	</section>

	<!-- SECTION 3: CAPABILITY COMPARISON -->
	<section class="section" use:observe>
		<div class="section-inner">
			<div class="section-label">03 — THE BENCHMARKS</div>
			<h2 class="section-title">AI vs. Human Performance</h2>
			<p class="section-desc">
				In 2020, AI couldn't reliably write a paragraph. Today it passes professional licensing exams.
				Here's where things stand.
			</p>

			<div class="benchmark-table">
				<div class="bench-header">
					<span class="bench-h-task">Task</span>
					<span class="bench-h-score">Human</span>
					<span class="bench-h-score">AI</span>
					<span class="bench-h-year">Year</span>
				</div>
				{#each capabilities as cap}
					<div class="bench-row" class:bench-ai-wins={cap.winner === 'ai'} class:bench-human-wins={cap.winner === 'human'}>
						<span class="bench-task">{cap.task}</span>
						<span class="bench-score" class:bench-winner={cap.winner === 'human'}>{cap.human}</span>
						<span class="bench-score" class:bench-winner={cap.winner === 'ai'}>{cap.ai}</span>
						<span class="bench-year">{cap.year}</span>
					</div>
				{/each}
			</div>

			<p class="bench-note">
				Sources: OpenAI technical reports, Anthropic, Google DeepMind, GPQA benchmark, HumanEval.
				Human scores represent expert-level performance (e.g., licensed professionals for bar/medical exams).
			</p>
		</div>
	</section>

	<!-- SECTION 4: THE KEY QUESTION -->
	<section class="section section-pivot" use:observe>
		<div class="section-inner">
			<div class="section-label">04 — THE QUESTION</div>
			<h2 class="section-title-large">
				So what do you <em>do</em> with this information?
			</h2>
			<p class="pivot-text">
				Most people respond to this with anxiety, denial, or paralysis.
				But there's a third option that almost nobody is talking about.
			</p>
			<p class="pivot-text">
				Instead of competing with AI for jobs, <strong>use AI as a force multiplier</strong>
				to build something real — physical, owned, and independent.
			</p>

			<div class="pivot-insight">
				<span class="pivot-marker">THE INSIGHT</span>
				<p>The same technologies displacing office workers are <em>empowering</em> builders.
				A solo creator with AI tools can now produce what took a team of 20 in 2019.
				Land is still real. Tools still work. YouTube pays for the journey.</p>
			</div>
		</div>
	</section>

	<!-- SECTION 5: THE BOOK FUNNEL BEGINS -->
	<section class="section section-book" use:observe>
		<div class="section-inner">
			<div class="section-label">05 — THE BLUEPRINT</div>
			<h2 class="section-title">We wrote the playbook.</h2>
			<p class="section-desc">
				"Surviving the Singularity" isn't about predictions. It's about <strong>what to do</strong>.
				A step-by-step guide for building material independence before the window closes.
			</p>

			<div class="book-hero" use:observe>
				<div class="book-visual">
					<div class="book-mock">
						<div class="book-spine"></div>
						<div class="book-cover">
							<div class="book-cover-inner">
								<span class="book-pre">THE</span>
								<span class="book-main-title">BLUEPRINT</span>
								<span class="book-sub-title">Surviving the Singularity</span>
								<div class="book-bar"></div>
								<span class="book-tagline">A Practical Guide to<br/>Material Independence</span>
							</div>
						</div>
					</div>
				</div>

				<div class="book-info">
					<h3 class="book-info-title">What's inside:</h3>
					<ul class="book-toc">
						<li class="book-toc-item">
							<span class="toc-num">01</span>
							<span class="toc-text">The economic trap — why the old path is broken (with math)</span>
						</li>
						<li class="book-toc-item">
							<span class="toc-num">02</span>
							<span class="toc-text">The Shouse model — $8K living space vs. $500K mortgage</span>
						</li>
						<li class="book-toc-item">
							<span class="toc-num">03</span>
							<span class="toc-text">The YouTube content engine — how to fund your build</span>
						</li>
						<li class="book-toc-item">
							<span class="toc-num">04</span>
							<span class="toc-text">Digital sovereignty — running your own AI, offline, forever</span>
						</li>
						<li class="book-toc-item">
							<span class="toc-num">05</span>
							<span class="toc-text">The physical exit — land, building codes, and rural strategy</span>
						</li>
						<li class="book-toc-item">
							<span class="toc-num">06</span>
							<span class="toc-text">Open-source robotics — FarmBot, Mobile Aloha, automation</span>
						</li>
						<li class="book-toc-item">
							<span class="toc-num">07</span>
							<span class="toc-text">The cash engine — digital products, passive income, escape velocity</span>
						</li>
						<li class="book-toc-item">
							<span class="toc-num">08</span>
							<span class="toc-text">Execute — immediate action steps, no excuses</span>
						</li>
					</ul>

					<div class="book-cta-group">
						<a href="/book" class="btn-book-primary">
							Get the Book
							<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
						</a>
						<a href="/blueprint" class="btn-book-secondary">
							Read the Free Blueprint
						</a>
					</div>

					<p class="book-free-note">
						The core blueprint is <strong>free to read online</strong>. The book goes deeper
						with case studies, calculators, vendor lists, and a 90-day action plan.
					</p>
				</div>
			</div>
		</div>
	</section>

	<!-- SECTION 6: SOCIAL PROOF / TESTIMONIALS PLACEHOLDER -->
	<section class="section section-dark" use:observe>
		<div class="section-inner">
			<div class="section-label">06 — THE COMMUNITY</div>
			<h2 class="section-title">People are already building.</h2>

			<div class="proof-grid" use:stagger={{ delay: 100 }}>
				<div class="proof-card stagger-item">
					<div class="proof-stat">$0</div>
					<div class="proof-label">Cost to start a YouTube channel</div>
					<div class="proof-detail">Phone + free editing software. That's it.</div>
				</div>
				<div class="proof-card stagger-item">
					<div class="proof-stat">$5K-$30K</div>
					<div class="proof-label">Rural land (1-5 acres)</div>
					<div class="proof-detail">Multiple counties across 30+ states</div>
				</div>
				<div class="proof-card stagger-item">
					<div class="proof-stat">$2K</div>
					<div class="proof-label">GPU for local AI</div>
					<div class="proof-detail">RTX 4090 runs Llama locally, forever</div>
				</div>
				<div class="proof-card stagger-item">
					<div class="proof-stat">114M+</div>
					<div class="proof-label">YouTube channels earning money</div>
					<div class="proof-detail">Sponsorships, ads, products, donations</div>
				</div>
			</div>

			<div class="proof-comparison" use:observe>
				<h3 class="comparison-title">Two paths. Same goal. Very different math.</h3>
				<div class="comparison-cols">
					<div class="comp-col comp-old">
						<div class="comp-header">Traditional Path</div>
						<ul class="comp-list">
							<li>$500K house → $1.1M after interest</li>
							<li>30-year commitment</li>
							<li>Requires steady employment</li>
							<li>Dependent on employer, market, economy</li>
							<li>No productive capacity</li>
						</ul>
						<div class="comp-total">Total: ~$1.1M+ over 30 years</div>
					</div>
					<div class="comp-col comp-new">
						<div class="comp-header">Builder Path</div>
						<ul class="comp-list">
							<li>$5-30K land + $25-100K shop/shouse</li>
							<li>2-5 year build timeline</li>
							<li>YouTube funds the build in real-time</li>
							<li>Own your land, tools, and AI stack</li>
							<li>Productive from day one</li>
						</ul>
						<div class="comp-total">Total: $30K-$150K, own everything</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- SECTION 7: FINAL CTA -->
	<section class="section section-final" use:observe>
		<div class="section-inner">
			<h2 class="final-title">
				The window is open.<br/>
				<span class="final-accent">Start building.</span>
			</h2>

			<p class="final-text">
				You don't need to quit your job tomorrow. You don't need to buy land this week.
				But you do need to <strong>start</strong>. Read the blueprint. Run the numbers.
				See if this path makes sense for you.
			</p>

			<div class="final-ctas">
				<a href="/blueprint" class="btn-final-primary">
					Read the Free Blueprint
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
				</a>
				<a href="/book" class="btn-final-secondary">
					Get the Full Book
				</a>
			</div>

			<p class="final-note">
				The blueprint is free. Always will be. The book is for people who want to go deeper.
			</p>
		</div>
	</section>
</div>

<style>
	.page {
		width: 100%;
	}

	/* ═══ HERO ═══ */
	.hero {
		position: relative;
		min-height: 85vh;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}

	.hero-bg {
		position: absolute;
		inset: 0;
		z-index: 0;
	}

	.hero-grid {
		position: absolute;
		inset: 0;
		background-image:
			linear-gradient(rgba(245, 158, 11, 0.03) 1px, transparent 1px),
			linear-gradient(90deg, rgba(245, 158, 11, 0.03) 1px, transparent 1px);
		background-size: 60px 60px;
	}

	.hero-content {
		position: relative;
		z-index: 1;
		max-width: 800px;
		margin: 0 auto;
		padding: 4rem 2rem;
		text-align: center;
	}

	.back-link {
		display: inline-block;
		margin-bottom: 2rem;
		font-size: 0.8rem;
		color: #64748b;
		text-decoration: none;
		transition: color 0.2s;
	}

	.back-link:hover {
		color: #f59e0b;
	}

	.hero-badge {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.65rem;
		font-weight: 700;
		color: #f59e0b;
		text-transform: uppercase;
		letter-spacing: 0.15em;
		font-family: 'JetBrains Mono', monospace;
		margin-bottom: 1.5rem;
	}

	.badge-dot {
		width: 6px;
		height: 6px;
		border-radius: 50%;
		background: #f59e0b;
		animation: pulse 2s infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 0.4; }
		50% { opacity: 1; }
	}

	.hero-title {
		font-size: clamp(2rem, 5vw, 3.5rem);
		font-weight: 900;
		color: #f1f5f9;
		line-height: 1.15;
		margin-bottom: 1.5rem;
		letter-spacing: -0.03em;
	}

	.hero-accent {
		color: #f59e0b;
	}

	.hero-sub {
		font-size: 1.1rem;
		color: #94a3b8;
		line-height: 1.7;
		max-width: 650px;
		margin: 0 auto 3rem;
	}

	.hero-scroll {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
		color: #475569;
		font-size: 0.75rem;
		animation: bob 2s ease-in-out infinite;
	}

	@keyframes bob {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(6px); }
	}

	/* ═══ SECTIONS ═══ */
	.section {
		padding: 6rem 2rem;
		opacity: 0;
		transform: translateY(20px);
		transition: opacity 0.6s ease, transform 0.6s ease;
	}

	:global(.section.revealed) {
		opacity: 1;
		transform: translateY(0);
	}

	.section-dark {
		background: rgba(15, 23, 42, 0.4);
	}

	.section-inner {
		max-width: 900px;
		margin: 0 auto;
	}

	.section-label {
		font-size: 0.65rem;
		font-weight: 700;
		color: #f59e0b;
		text-transform: uppercase;
		letter-spacing: 0.15em;
		font-family: 'JetBrains Mono', monospace;
		margin-bottom: 1rem;
	}

	.section-title {
		font-size: clamp(1.5rem, 3.5vw, 2.2rem);
		font-weight: 800;
		color: #f1f5f9;
		margin-bottom: 0.75rem;
		letter-spacing: -0.02em;
	}

	.section-desc {
		font-size: 1rem;
		color: #94a3b8;
		line-height: 1.65;
		margin-bottom: 3rem;
		max-width: 700px;
	}

	/* ═══ TIMELINE ═══ */
	.timeline {
		position: relative;
		padding-left: 1rem;
	}

	.timeline::before {
		content: '';
		position: absolute;
		left: 40px;
		top: 0;
		bottom: 0;
		width: 2px;
		background: linear-gradient(180deg, #f59e0b 0%, #475569 60%, rgba(100,116,139,0.2) 100%);
	}

	.timeline-item {
		display: flex;
		gap: 1.5rem;
		padding: 1.25rem 0;
		position: relative;
		opacity: 0;
		transform: translateX(-10px);
		transition: opacity 0.4s ease, transform 0.4s ease;
	}

	:global(.timeline-item.stagger-in) {
		opacity: 1;
		transform: translateX(0);
	}

	.timeline-future {
		opacity: 0.6;
	}

	:global(.timeline-future.stagger-in) {
		opacity: 0.6;
	}

	.timeline-year {
		min-width: 52px;
		font-size: 0.85rem;
		font-weight: 800;
		color: #f59e0b;
		font-family: 'JetBrains Mono', monospace;
		position: relative;
		z-index: 1;
	}

	.timeline-year::after {
		content: '';
		position: absolute;
		right: -21px;
		top: 50%;
		transform: translateY(-50%);
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: #f59e0b;
		border: 2px solid #020617;
	}

	.timeline-future .timeline-year::after {
		background: #475569;
		border-color: #1e293b;
	}

	.timeline-body {
		flex: 1;
		padding-left: 0.5rem;
	}

	.timeline-event {
		font-size: 0.95rem;
		font-weight: 700;
		color: #e2e8f0;
		margin-bottom: 0.25rem;
	}

	.timeline-impact {
		font-size: 0.85rem;
		color: #94a3b8;
		margin-bottom: 0.3rem;
	}

	.timeline-source {
		font-size: 0.7rem;
		color: #475569;
		font-family: 'JetBrains Mono', monospace;
	}

	.projected-badge {
		font-size: 0.55rem;
		font-weight: 700;
		color: #64748b;
		background: rgba(100, 116, 139, 0.1);
		border: 1px solid rgba(100, 116, 139, 0.15);
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		height: fit-content;
		margin-top: 0.3rem;
	}

	/* ═══ QUOTES ═══ */
	.quotes-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 1.25rem;
		margin-bottom: 3rem;
	}

	.quote-card {
		background: rgba(255, 255, 255, 0.02);
		border: 1px solid rgba(148, 163, 184, 0.06);
		border-radius: 12px;
		padding: 1.5rem;
		opacity: 0;
		transform: translateY(10px);
		transition: opacity 0.4s ease, transform 0.4s ease;
	}

	:global(.quote-card.stagger-in) {
		opacity: 1;
		transform: translateY(0);
	}

	.quote-key {
		border-color: rgba(245, 158, 11, 0.15);
		background: rgba(245, 158, 11, 0.02);
	}

	.quote-text {
		font-size: 1rem;
		color: #e2e8f0;
		line-height: 1.65;
		margin: 0 0 1rem;
		font-style: italic;
	}

	.quote-attribution {
		border-top: 1px solid rgba(148, 163, 184, 0.06);
		padding-top: 0.75rem;
	}

	.quote-name {
		font-size: 0.85rem;
		font-weight: 700;
		color: #f1f5f9;
	}

	.quote-role {
		font-size: 0.75rem;
		color: #64748b;
		margin-bottom: 0.3rem;
	}

	.quote-source {
		font-size: 0.7rem;
		color: #475569;
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.quote-link {
		color: #f59e0b;
		text-decoration: none;
		font-weight: 600;
	}

	.quote-link:hover {
		text-decoration: underline;
	}

	/* ═══ CALLOUT ═══ */
	.callout-box {
		display: flex;
		gap: 1.25rem;
		background: rgba(245, 158, 11, 0.03);
		border: 1px solid rgba(245, 158, 11, 0.12);
		border-radius: 12px;
		padding: 1.5rem;
		opacity: 0;
		transform: translateY(10px);
		transition: opacity 0.6s ease, transform 0.6s ease;
	}

	:global(.callout-box.revealed) {
		opacity: 1;
		transform: translateY(0);
	}

	.callout-icon {
		color: #f59e0b;
		flex-shrink: 0;
		margin-top: 0.15rem;
	}

	.callout-title {
		font-size: 0.9rem;
		font-weight: 700;
		color: #f59e0b;
		margin-bottom: 0.5rem;
	}

	.callout-text {
		font-size: 0.9rem;
		color: #94a3b8;
		line-height: 1.65;
		margin-bottom: 0.5rem;
	}

	.callout-text a {
		color: #f59e0b;
		font-weight: 600;
	}

	.callout-read-time {
		font-size: 0.75rem;
		color: #475569;
		font-family: 'JetBrains Mono', monospace;
	}

	/* ═══ BENCHMARKS ═══ */
	.benchmark-table {
		border: 1px solid rgba(148, 163, 184, 0.08);
		border-radius: 12px;
		overflow: hidden;
		margin-bottom: 1.5rem;
	}

	.bench-header {
		display: grid;
		grid-template-columns: 2fr 1fr 1fr 0.5fr;
		gap: 1rem;
		padding: 0.85rem 1.25rem;
		background: rgba(30, 41, 59, 0.6);
		border-bottom: 1px solid rgba(148, 163, 184, 0.06);
	}

	.bench-h-task, .bench-h-score, .bench-h-year {
		font-size: 0.65rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #64748b;
	}

	.bench-row {
		display: grid;
		grid-template-columns: 2fr 1fr 1fr 0.5fr;
		gap: 1rem;
		padding: 0.85rem 1.25rem;
		border-bottom: 1px solid rgba(148, 163, 184, 0.04);
		transition: background 0.15s;
	}

	.bench-row:hover {
		background: rgba(245, 158, 11, 0.02);
	}

	.bench-task {
		font-size: 0.85rem;
		color: #e2e8f0;
		font-weight: 500;
	}

	.bench-score {
		font-size: 0.85rem;
		color: #94a3b8;
		font-family: 'JetBrains Mono', monospace;
	}

	.bench-winner {
		color: #10b981;
		font-weight: 700;
	}

	.bench-year {
		font-size: 0.75rem;
		color: #475569;
		font-family: 'JetBrains Mono', monospace;
	}

	.bench-note {
		font-size: 0.75rem;
		color: #475569;
		line-height: 1.6;
	}

	/* ═══ PIVOT SECTION ═══ */
	.section-pivot {
		text-align: center;
		background: linear-gradient(180deg, rgba(245, 158, 11, 0.02) 0%, transparent 100%);
	}

	.section-title-large {
		font-size: clamp(1.8rem, 4vw, 2.8rem);
		font-weight: 900;
		color: #f1f5f9;
		margin-bottom: 1.5rem;
		letter-spacing: -0.02em;
	}

	.section-title-large em {
		color: #f59e0b;
		font-style: normal;
	}

	.pivot-text {
		font-size: 1.1rem;
		color: #94a3b8;
		line-height: 1.7;
		max-width: 650px;
		margin: 0 auto 1.25rem;
	}

	.pivot-insight {
		max-width: 650px;
		margin: 3rem auto 0;
		background: rgba(245, 158, 11, 0.03);
		border: 1px solid rgba(245, 158, 11, 0.1);
		border-radius: 12px;
		padding: 1.5rem;
		text-align: left;
	}

	.pivot-marker {
		font-size: 0.6rem;
		font-weight: 800;
		color: #f59e0b;
		letter-spacing: 0.15em;
		font-family: 'JetBrains Mono', monospace;
		display: block;
		margin-bottom: 0.75rem;
	}

	.pivot-insight p {
		font-size: 1rem;
		color: #cbd5e1;
		line-height: 1.7;
		margin: 0;
	}

	.pivot-insight em {
		color: #f59e0b;
	}

	/* ═══ BOOK SECTION ═══ */
	.section-book {
		background: linear-gradient(180deg, transparent 0%, rgba(245, 158, 11, 0.02) 50%, transparent 100%);
	}

	.book-hero {
		display: grid;
		grid-template-columns: 280px 1fr;
		gap: 3rem;
		align-items: start;
		margin-top: 2rem;
		opacity: 0;
		transform: translateY(15px);
		transition: opacity 0.6s ease, transform 0.6s ease;
	}

	:global(.book-hero.revealed) {
		opacity: 1;
		transform: translateY(0);
	}

	.book-visual {
		display: flex;
		justify-content: center;
	}

	.book-mock {
		width: 220px;
		height: 300px;
		position: relative;
		perspective: 800px;
		transform: rotateY(-8deg);
	}

	.book-spine {
		position: absolute;
		left: 0;
		top: 2px;
		bottom: 2px;
		width: 20px;
		background: linear-gradient(180deg, #d97706, #92400e);
		border-radius: 3px 0 0 3px;
		transform: translateX(-18px) rotateY(-30deg);
		transform-origin: right center;
	}

	.book-cover {
		width: 100%;
		height: 100%;
		background: linear-gradient(145deg, #1a1a2e, #0f0f23);
		border: 1px solid rgba(245, 158, 11, 0.2);
		border-radius: 2px 8px 8px 2px;
		box-shadow:
			8px 8px 30px rgba(0, 0, 0, 0.5),
			0 0 40px rgba(245, 158, 11, 0.05);
		overflow: hidden;
	}

	.book-cover-inner {
		padding: 2rem 1.5rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		height: 100%;
		justify-content: center;
		gap: 0.3rem;
	}

	.book-pre {
		font-size: 0.6rem;
		color: #64748b;
		letter-spacing: 0.3em;
		font-weight: 700;
		text-transform: uppercase;
	}

	.book-main-title {
		font-size: 1.4rem;
		font-weight: 900;
		color: #f59e0b;
		letter-spacing: 0.08em;
		line-height: 1.1;
	}

	.book-sub-title {
		font-size: 0.65rem;
		color: #94a3b8;
		letter-spacing: 0.05em;
		margin-top: 0.15rem;
	}

	.book-bar {
		width: 40px;
		height: 2px;
		background: #f59e0b;
		margin: 0.75rem 0;
	}

	.book-tagline {
		font-size: 0.55rem;
		color: #475569;
		line-height: 1.5;
		letter-spacing: 0.03em;
	}

	.book-info-title {
		font-size: 1.1rem;
		font-weight: 700;
		color: #f1f5f9;
		margin-bottom: 1.25rem;
	}

	.book-toc {
		list-style: none;
		padding: 0;
		margin: 0 0 2rem;
	}

	.book-toc-item {
		display: flex;
		gap: 0.75rem;
		padding: 0.6rem 0;
		border-bottom: 1px solid rgba(148, 163, 184, 0.04);
	}

	.toc-num {
		font-size: 0.7rem;
		font-weight: 800;
		color: #f59e0b;
		font-family: 'JetBrains Mono', monospace;
		min-width: 24px;
	}

	.toc-text {
		font-size: 0.88rem;
		color: #94a3b8;
		line-height: 1.4;
	}

	.book-cta-group {
		display: flex;
		gap: 1rem;
		margin-bottom: 1.25rem;
	}

	.btn-book-primary {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.85rem 1.75rem;
		background: #f59e0b;
		color: #0f172a;
		font-weight: 700;
		font-size: 0.9rem;
		border-radius: 8px;
		text-decoration: none;
		transition: all 0.2s;
	}

	.btn-book-primary:hover {
		background: #fbbf24;
		transform: translateY(-1px);
		box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
	}

	.btn-book-secondary {
		display: inline-flex;
		align-items: center;
		padding: 0.85rem 1.75rem;
		background: transparent;
		color: #94a3b8;
		font-weight: 600;
		font-size: 0.9rem;
		border: 1px solid rgba(148, 163, 184, 0.15);
		border-radius: 8px;
		text-decoration: none;
		transition: all 0.2s;
	}

	.btn-book-secondary:hover {
		color: #f1f5f9;
		border-color: rgba(148, 163, 184, 0.3);
	}

	.book-free-note {
		font-size: 0.78rem;
		color: #475569;
		line-height: 1.5;
	}

	/* ═══ PROOF SECTION ═══ */
	.proof-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1rem;
		margin-bottom: 3rem;
	}

	.proof-card {
		background: rgba(255, 255, 255, 0.02);
		border: 1px solid rgba(148, 163, 184, 0.06);
		border-radius: 10px;
		padding: 1.25rem;
		text-align: center;
		opacity: 0;
		transform: translateY(10px);
		transition: opacity 0.4s ease, transform 0.4s ease;
	}

	:global(.proof-card.stagger-in) {
		opacity: 1;
		transform: translateY(0);
	}

	.proof-stat {
		font-size: 1.5rem;
		font-weight: 900;
		color: #f59e0b;
		font-family: 'JetBrains Mono', monospace;
		margin-bottom: 0.3rem;
	}

	.proof-label {
		font-size: 0.8rem;
		color: #e2e8f0;
		font-weight: 600;
		margin-bottom: 0.3rem;
	}

	.proof-detail {
		font-size: 0.7rem;
		color: #475569;
	}

	.proof-comparison {
		opacity: 0;
		transform: translateY(10px);
		transition: opacity 0.6s ease, transform 0.6s ease;
	}

	:global(.proof-comparison.revealed) {
		opacity: 1;
		transform: translateY(0);
	}

	.comparison-title {
		font-size: 1.1rem;
		font-weight: 700;
		color: #f1f5f9;
		margin-bottom: 1.5rem;
		text-align: center;
	}

	.comparison-cols {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
	}

	.comp-col {
		background: rgba(255, 255, 255, 0.02);
		border: 1px solid rgba(148, 163, 184, 0.06);
		border-radius: 12px;
		padding: 1.5rem;
	}

	.comp-new {
		border-color: rgba(245, 158, 11, 0.15);
		background: rgba(245, 158, 11, 0.02);
	}

	.comp-header {
		font-size: 0.85rem;
		font-weight: 700;
		color: #e2e8f0;
		margin-bottom: 1rem;
		text-align: center;
		padding-bottom: 0.75rem;
		border-bottom: 1px solid rgba(148, 163, 184, 0.06);
	}

	.comp-new .comp-header {
		color: #f59e0b;
	}

	.comp-list {
		list-style: none;
		padding: 0;
		margin: 0 0 1rem;
	}

	.comp-list li {
		font-size: 0.85rem;
		color: #94a3b8;
		padding: 0.4rem 0;
		border-bottom: 1px solid rgba(148, 163, 184, 0.03);
		line-height: 1.4;
	}

	.comp-total {
		font-size: 0.85rem;
		font-weight: 700;
		color: #e2e8f0;
		text-align: center;
		padding-top: 0.5rem;
	}

	.comp-new .comp-total {
		color: #10b981;
	}

	/* ═══ FINAL CTA ═══ */
	.section-final {
		text-align: center;
		padding: 8rem 2rem;
		background: linear-gradient(180deg, transparent 0%, rgba(245, 158, 11, 0.03) 100%);
	}

	.final-title {
		font-size: clamp(1.8rem, 4vw, 3rem);
		font-weight: 900;
		color: #f1f5f9;
		margin-bottom: 1.5rem;
		letter-spacing: -0.02em;
	}

	.final-accent {
		color: #f59e0b;
	}

	.final-text {
		font-size: 1.1rem;
		color: #94a3b8;
		line-height: 1.7;
		max-width: 550px;
		margin: 0 auto 2.5rem;
	}

	.final-ctas {
		display: flex;
		gap: 1rem;
		justify-content: center;
		margin-bottom: 1.5rem;
	}

	.btn-final-primary {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 1rem 2rem;
		background: #f59e0b;
		color: #0f172a;
		font-weight: 700;
		font-size: 1rem;
		border-radius: 10px;
		text-decoration: none;
		transition: all 0.2s;
	}

	.btn-final-primary:hover {
		background: #fbbf24;
		transform: translateY(-2px);
		box-shadow: 0 6px 30px rgba(245, 158, 11, 0.3);
	}

	.btn-final-secondary {
		display: inline-flex;
		align-items: center;
		padding: 1rem 2rem;
		background: transparent;
		color: #94a3b8;
		font-weight: 600;
		font-size: 1rem;
		border: 1px solid rgba(148, 163, 184, 0.15);
		border-radius: 10px;
		text-decoration: none;
		transition: all 0.2s;
	}

	.btn-final-secondary:hover {
		color: #f1f5f9;
		border-color: rgba(148, 163, 184, 0.3);
	}

	.final-note {
		font-size: 0.78rem;
		color: #475569;
	}

	/* ═══ STAGGER ANIMATIONS ═══ */
	.stagger-item {
		opacity: 0;
		transform: translateY(10px);
		transition: opacity 0.4s ease, transform 0.4s ease;
	}

	:global(.stagger-item.stagger-in) {
		opacity: 1;
		transform: translateY(0);
	}

	/* ═══ RESPONSIVE ═══ */
	@media (max-width: 768px) {
		.section {
			padding: 4rem 1.25rem;
		}

		.hero-content {
			padding: 3rem 1.25rem;
		}

		.timeline::before {
			left: 32px;
		}

		.bench-header, .bench-row {
			grid-template-columns: 2fr 1fr 1fr;
		}

		.bench-year, .bench-h-year {
			display: none;
		}

		.book-hero {
			grid-template-columns: 1fr;
			gap: 2rem;
		}

		.book-mock {
			transform: rotateY(0);
			width: 180px;
			height: 250px;
		}

		.book-visual {
			order: -1;
		}

		.book-cta-group {
			flex-direction: column;
		}

		.proof-grid {
			grid-template-columns: 1fr 1fr;
		}

		.comparison-cols {
			grid-template-columns: 1fr;
		}

		.final-ctas {
			flex-direction: column;
			align-items: center;
		}

		.callout-box {
			flex-direction: column;
			gap: 0.75rem;
		}
	}

	@media (max-width: 480px) {
		.proof-grid {
			grid-template-columns: 1fr;
		}

		.book-spine {
			display: none;
		}
	}
</style>
