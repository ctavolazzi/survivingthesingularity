<script>
	import { onMount } from 'svelte';
	import { safeGoto } from '$lib/utils/navigation';
	import Countdown from '$lib/components/Countdown.svelte';
	import Timeline from '$lib/components/Timeline.svelte';
	import BookCallout from '$lib/components/BookCallout.svelte';
	import FuturePredictions from '$lib/components/FuturePredictions.svelte';
	import { loadBlogPosts } from '$lib/data/blog-posts/blogPosts.js';
	import FAQ from '$lib/components/FAQ.svelte';
	import LatestNews from '$lib/components/LatestNews.svelte';
	import NewsTicker from '$lib/components/NewsTicker.svelte';
	import FeaturedPosts from '$lib/components/FeaturedPosts.svelte';
	import AGIRoadmap from '$lib/components/AGIRoadmap.svelte';
	import { fade } from 'svelte/transition';

	const targetDate = new Date("2027-11-20T23:59:59").getTime();

	let posts = [];
	let newsTickerItems = [];
	let heroVisible = false;

	onMount(async () => {
		heroVisible = true;
		posts = await loadBlogPosts();

		newsTickerItems = posts.map(post => {
			let tag = 'Blog';
			if (post.slug === 'singularity-express') tag = 'Opinion';
			else if (post.slug === 'farm-bot-deep-dive') tag = 'Tech';
			else if (post.slug === 'darpa-biomechanical-space-structures') tag = 'News';
			else if (post.slug === 'claude-projects-weekend-project') tag = 'AI Update';
			else if (post.slug === 'robot-farm-bot') tag = 'Review';

			return {
				date: new Date(post.date).toISOString().split('T')[0],
				text: post.title,
				tag: tag,
				link: `/blog/${post.slug}`
			};
		}).slice(0, 7);
	});
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
</svelte:head>

<div class="main-content">

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- HERO SECTION — The New Era                          -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="hero">
		<div class="hero-bg">
			<div class="hero-grid"></div>
			<div class="hero-glow hero-glow-1"></div>
			<div class="hero-glow hero-glow-2"></div>
			<div class="hero-orb"></div>
		</div>

		{#if heroVisible}
			<div class="hero-content" in:fade={{ duration: 800 }}>
				<p class="hero-eyebrow">The book on AI the world needs right now</p>
				<h1 class="hero-title">
					<span class="hero-title-line">Surviving</span>
					<span class="hero-title-line hero-title-accent">the Singularity</span>
				</h1>
				<p class="hero-subtitle">
					The AI revolution isn't coming — it's here. This is your guide to understanding it, preparing for it, and thriving through it.
				</p>
				<div class="hero-actions">
					<a href="/sample" class="hero-btn hero-btn-primary">
						Read the Free Sample
						<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</a>
					<a href="/start-here" class="hero-btn hero-btn-secondary">
						Start Here
					</a>
				</div>
			</div>
		{/if}
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- COUNTDOWN                                           -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container">
		<Countdown {targetDate} />
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- NEWS TICKER                                         -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container section-narrow">
		<NewsTicker
			title="Latest Updates"
			scrollSpeed={2500}
			items={newsTickerItems}
			backgroundColor="rgba(15, 23, 42, 0.5)"
			textColor="white"
			accentColor="#63b3ed"
		/>
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- WHAT'S COMING — Teaser Section                      -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="whats-coming">
		<div class="whats-coming-inner">
			<h2 class="section-heading">Why This Book Matters Now</h2>
			<p class="section-subheading">AI is reshaping everything. Here's what you'll find inside.</p>
			<div class="roadmap-grid">
				<div class="roadmap-card">
					<div class="roadmap-icon">01</div>
					<h3>Understand the Shift</h3>
					<p>Cut through the hype and fear. Get a clear-eyed look at what AI actually means for your life, career, and future.</p>
					<span class="roadmap-status">12 Chapters</span>
				</div>
				<div class="roadmap-card">
					<div class="roadmap-icon">02</div>
					<h3>Practical Strategies</h3>
					<p>Not just theory — actionable frameworks for thriving when the world changes faster than you can refresh your feed.</p>
					<span class="roadmap-status">Battle-Tested</span>
				</div>
				<div class="roadmap-card">
					<div class="roadmap-icon">03</div>
					<h3>Stay Human</h3>
					<p>The singularity doesn't have to be scary. Learn how to keep what makes us human while embracing what makes us powerful.</p>
					<span class="roadmap-status">Essential Reading</span>
				</div>
			</div>
		</div>
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- TIMELINE                                            -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container">
		<Timeline />
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- FEATURED POSTS                                      -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container section-wide">
		<FeaturedPosts
			title="Editor's Picks"
			subtitle="Essential reading for understanding the AI revolution"
			maxPosts={2}
			showImages={true}
		/>
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- FUTURE PREDICTIONS                                  -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container">
		<FuturePredictions />
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- AGI ROADMAP                                         -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container section-narrow">
		<AGIRoadmap />
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- FAQ                                                 -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container section-narrow">
		<FAQ />
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- LATEST NEWS                                         -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container section-narrow">
		<LatestNews />
	</section>

	<!-- ═══════════════════════════════════════════════════ -->
	<!-- BOOK CALLOUT                                        -->
	<!-- ═══════════════════════════════════════════════════ -->
	<section class="section-container section-narrow">
		<BookCallout />
	</section>

</div>

<style>
	/* ──────────────────────────────────── */
	/* LAYOUT                               */
	/* ──────────────────────────────────── */
	.main-content {
		display: flex;
		flex-direction: column;
		gap: 0;
	}

	.section-container {
		width: 100%;
		max-width: 900px;
		margin: 2rem auto;
		padding: 0 1.5rem;
	}

	.section-narrow {
		max-width: 800px;
	}

	.section-wide {
		max-width: 1100px;
	}

	/* ──────────────────────────────────── */
	/* HERO                                 */
	/* ──────────────────────────────────── */
	.hero {
		position: relative;
		min-height: 85vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 4rem 2rem;
		overflow: hidden;
	}

	.hero-bg {
		position: absolute;
		inset: 0;
		background: linear-gradient(160deg, #020617 0%, #0f172a 40%, #1e1b4b 70%, #0f172a 100%);
	}

	.hero-grid {
		position: absolute;
		inset: 0;
		background-image:
			linear-gradient(rgba(99, 179, 237, 0.04) 1px, transparent 1px),
			linear-gradient(90deg, rgba(99, 179, 237, 0.04) 1px, transparent 1px);
		background-size: 60px 60px;
	}

	.hero-glow {
		position: absolute;
		border-radius: 50%;
		filter: blur(80px);
		opacity: 0.3;
	}

	.hero-glow-1 {
		width: 500px;
		height: 500px;
		background: radial-gradient(circle, #3b82f6, transparent 70%);
		top: -150px;
		right: -100px;
		animation: float-glow 15s ease-in-out infinite;
	}

	.hero-glow-2 {
		width: 400px;
		height: 400px;
		background: radial-gradient(circle, #8b5cf6, transparent 70%);
		bottom: -100px;
		left: -100px;
		animation: float-glow 18s ease-in-out infinite reverse;
	}

	.hero-orb {
		position: absolute;
		width: 300px;
		height: 300px;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		background: radial-gradient(circle, rgba(99, 179, 237, 0.08), transparent 60%);
		border-radius: 50%;
		animation: pulse-orb 6s ease-in-out infinite;
	}

	@keyframes float-glow {
		0%, 100% { transform: translate(0, 0); }
		33% { transform: translate(30px, -20px); }
		66% { transform: translate(-20px, 15px); }
	}

	@keyframes pulse-orb {
		0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
		50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.8; }
	}

	.hero-content {
		position: relative;
		z-index: 2;
		text-align: center;
		max-width: 750px;
	}

	.hero-eyebrow {
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.2em;
		color: #64748b;
		margin-bottom: 1.5rem;
		font-weight: 500;
	}

	.hero-title {
		font-size: clamp(2.5rem, 8vw, 5rem);
		font-weight: 800;
		line-height: 1.05;
		margin: 0 0 1.5rem 0;
		letter-spacing: -0.03em;
	}

	.hero-title-line {
		display: block;
		color: #f1f5f9;
	}

	.hero-title-accent {
		background: linear-gradient(135deg, #63b3ed 0%, #a78bfa 50%, #f472b6 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.hero-subtitle {
		font-size: clamp(1rem, 2.5vw, 1.25rem);
		color: #94a3b8;
		line-height: 1.7;
		margin-bottom: 2.5rem;
		max-width: 600px;
		margin-left: auto;
		margin-right: auto;
	}

	.hero-actions {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
	}

	.hero-btn {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.85rem 2rem;
		border-radius: 10px;
		font-weight: 600;
		font-size: 0.95rem;
		text-decoration: none;
		transition: all 0.3s ease;
		cursor: pointer;
	}

	.hero-btn-primary {
		background: linear-gradient(135deg, #3b82f6, #8b5cf6);
		color: white;
		box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
	}

	.hero-btn-primary:hover {
		transform: translateY(-2px);
		box-shadow: 0 8px 30px rgba(59, 130, 246, 0.4);
	}

	.hero-btn-secondary {
		background: rgba(255, 255, 255, 0.05);
		color: #cbd5e1;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.hero-btn-secondary:hover {
		background: rgba(255, 255, 255, 0.1);
		border-color: rgba(255, 255, 255, 0.2);
		transform: translateY(-2px);
	}

	/* ──────────────────────────────────── */
	/* WHAT'S COMING SECTION                */
	/* ──────────────────────────────────── */
	.whats-coming {
		padding: 4rem 1.5rem;
		background: linear-gradient(180deg, transparent 0%, rgba(15, 23, 42, 0.5) 20%, rgba(15, 23, 42, 0.5) 80%, transparent 100%);
	}

	.whats-coming-inner {
		max-width: 1000px;
		margin: 0 auto;
	}

	.section-heading {
		text-align: center;
		font-size: clamp(1.5rem, 4vw, 2.25rem);
		font-weight: 700;
		color: #f1f5f9;
		margin: 0 0 0.5rem 0;
		letter-spacing: -0.02em;
	}

	.section-subheading {
		text-align: center;
		color: #64748b;
		font-size: 1rem;
		margin: 0 0 3rem 0;
	}

	.roadmap-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
		gap: 1.5rem;
	}

	.roadmap-card {
		background: rgba(30, 41, 59, 0.5);
		border: 1px solid rgba(148, 163, 184, 0.1);
		border-radius: 16px;
		padding: 2rem;
		transition: all 0.3s ease;
	}

	.roadmap-card:hover {
		border-color: rgba(99, 179, 237, 0.3);
		transform: translateY(-4px);
		box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
	}

	.roadmap-icon {
		font-size: 0.8rem;
		font-weight: 700;
		color: #63b3ed;
		letter-spacing: 0.1em;
		margin-bottom: 1rem;
		font-family: 'JetBrains Mono', 'Courier New', monospace;
	}

	.roadmap-card h3 {
		font-size: 1.15rem;
		font-weight: 600;
		color: #e2e8f0;
		margin: 0 0 0.75rem 0;
	}

	.roadmap-card p {
		font-size: 0.9rem;
		color: #94a3b8;
		line-height: 1.6;
		margin: 0 0 1.25rem 0;
	}

	.roadmap-status {
		display: inline-block;
		font-size: 0.7rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		padding: 0.3rem 0.8rem;
		border-radius: 20px;
		background: rgba(99, 179, 237, 0.1);
		color: #63b3ed;
		border: 1px solid rgba(99, 179, 237, 0.2);
	}

	/* ──────────────────────────────────── */
	/* RESPONSIVE                           */
	/* ──────────────────────────────────── */
	@media (min-width: 768px) {
		.main-content {
			max-width: 100%;
			margin: 0 auto;
		}
	}

	@media (max-width: 768px) {
		.hero {
			min-height: 70vh;
			padding: 3rem 1.5rem;
		}

		.hero-actions {
			flex-direction: column;
			align-items: center;
		}

		.hero-btn {
			width: 100%;
			max-width: 280px;
			justify-content: center;
		}

		.section-container {
			padding: 0 1rem;
			margin: 1.5rem auto;
		}

		.whats-coming {
			padding: 3rem 1rem;
		}
	}

	@media (max-width: 480px) {
		.hero {
			min-height: 65vh;
			padding: 2.5rem 1rem;
		}

		.hero-eyebrow {
			font-size: 0.7rem;
		}

		.section-container {
			padding: 0 0.75rem;
			margin: 1rem auto;
		}
	}
</style>

