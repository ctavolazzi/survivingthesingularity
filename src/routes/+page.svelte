<script>
	import { onMount } from 'svelte';
	import Countdown from '$lib/components/Countdown.svelte';
	// import HeroSection from '$lib/components/HeroSection.svelte';
	import Timeline from '$lib/components/Timeline.svelte';
	// Removing KnowledgeMeter import
	import BookCallout from '$lib/components/BookCallout.svelte';
	import FuturePredictions from '$lib/components/FuturePredictions.svelte';
	import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
	import { loadBlogPosts, blogPosts } from '$lib/data/blog-posts/blogPosts.js';
	import FAQ from '$lib/components/FAQ.svelte';
	import LatestNews from '$lib/components/LatestNews.svelte';
	import BookSample from '$lib/components/BookSample.svelte';
	import welcomeImage from '$lib/images/sts-welcome.png';
	import timelineItems from '$lib/data/timelineItems.json';
	import DiscordButton from '$lib/components/DiscordButton.svelte';
	import MysteryBoxAd from '$lib/components/ads/MysteryBoxAd.svelte';
	import NewsTicker from '$lib/components/NewsTicker.svelte';
	import FeaturedPosts from '$lib/components/FeaturedPosts.svelte';

	// Custom news items to bypass the API
	const customNewsItems = [
		{
			date: '2025-03-06',
			text: 'New synthetic biological intelligence breakthrough announced by Cortical Labs',
			tag: 'Breaking',
			link: '/blog/synthetic-biological-intelligence'
		},
		{
			date: '2025-03-04',
			text: 'DARPA seeks proposals for biological space structures - major implications for space industry',
			tag: 'New',
			link: '/blog/darpa-biomechanical-space-structures'
		},
		{
			date: '2025-03-01',
			text: 'Claude 4 Opus released with unprecedented reasoning capabilities',
			tag: 'AI News',
			link: '/blog/claude-projects-weekend-project'
		},
		{
			date: '2024-02-28',
			text: 'New regulatory framework for AGI proposed by international coalition',
			tag: 'Policy',
			link: '/blog/singularity-express'
		},
		{
			date: '2024-02-25',
			text: 'Preview our exclusive book "Surviving the Singularity" - first chapter now available',
			tag: 'Book',
			link: '/sample'
		},
		{
			date: '2024-02-22',
			text: 'Latest FarmBot update adds advanced computer vision capabilities',
			tag: 'Tech',
			link: '/blog/farm-bot-deep-dive'
		},
		{
			date: '2024-02-20',
			text: 'Our newsletter has reached 10,000 subscribers! Thank you for your support.',
			tag: 'Milestone',
			link: '/blog/robot-farm-bot'
		}
	];

	// Direct load for fast loading components
	export const data = {};
	const targetDate = new Date("2027-11-20T23:59:59").getTime();

	// We'll populate this later
	let posts = [];
	let latestPost = null;
	// Create a store for news ticker items
	let newsTickerItems = [];

	// Load the blog posts when the component is created
	onMount(async () => {
		posts = await loadBlogPosts();

		// Format blog posts for the news ticker
		newsTickerItems = posts.map(post => ({
			date: new Date(post.date).toISOString().split('T')[0],
			text: post.title,
			tag: post.category || 'Blog',
			link: `/blog/${post.slug}`
		})).slice(0, 7);

		console.log("Formatted blog posts for news ticker:", newsTickerItems);
	});
</script>

<svelte:head>
	<!-- Preload welcome image to ensure it loads immediately -->
	<link rel="preload" href={welcomeImage} as="image" fetchpriority="high" />
</svelte:head>

<div class="main-content">
	<div class="countdown-container">
		<Countdown {targetDate} />
	</div>

	<!-- Add News Ticker near the top for high visibility -->
	<div class="news-ticker-container">
		<NewsTicker
			title="Latest From Our Blog"
			scrollSpeed={3500}
			items={newsTickerItems}
			backgroundColor="rgba(15, 23, 42, 0.7)"
			textColor="white"
			accentColor="#ef4444"
		/>
	</div>

	<div class="timeline-section">
		<Timeline />
	</div>

	<!-- Removing KnowledgeMeter component -->
	<div class="book-callout-wrapper">
		<BookCallout
			title="Navigate the Path to Singularity"
			description="Get the insights and strategies you need to prepare for the technological changes that will reshape our world."
			buttonText="Explore the Book"
			buttonLink="/sample"
		/>
	</div>

	<!-- Add Featured Posts before the predictions section -->
	<div class="featured-posts-container">
		<FeaturedPosts
			title="Editor's Picks"
			subtitle="Essential reading for understanding the AI revolution"
			maxPosts={2}
			showImages={true}
		/>
	</div>

	<!-- Rest of the content -->
	<FuturePredictions class="future-predictions-container" />

	<FAQ class="faq-container" />

	<div class="newsletter-container">
		<NewsletterSignup />
		<DiscordButton />
	</div>

	<div class="recent-posts">
		<LatestNews />
	</div>

	<!-- Treasure Tavern Promo -->
	<div class="treasure-promo">
		<a href="https://treasuretavernhq.myshopify.com/" class="treasure-link">
			<div class="treasure-content">
				<div class="sparkle-container">
					<span class="sparkle sparkle-1">✨</span>
					<span class="sparkle sparkle-2">✨</span>
				</div>
				<h2>Want to see the best treasures anywhere on the internet?</h2>
				<p>Discover handpicked gems that will brighten your day!</p>
			</div>
		</a>
	</div>

	<!-- Mystery Box Ad -->
	<div class="mystery-box-container">
		<MysteryBoxAd
			title="Mood Booster Mystery Box"
			subtitle="Monthly Surprises"
			description="Discover curated indie treasures delivered monthly to your door. Each box contains 5+ handpicked items designed to boost your mood and bring joy to your everyday life."
			price="24.99"
			frequency="month"
			ctaText="Subscribe Now"
			ctaUrl="https://treasuretavernhq.myshopify.com/"
			badgeText="Most Popular"
			itemCount="5+ items"
		/>
	</div>
</div>

<style>
	/* Styles removed for components using inline styles for maximum speed */

	.main-content {
		max-width: 100%;
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		padding-top: 0.3rem;
	}

	.countdown-container {
		width: 100%;
		max-width: 100%;
		overflow-x: hidden;
		padding: 0 1rem;
		margin-bottom: 0;
	}

	.timeline-section {
		margin: 0 0.5rem;
	}

	.newsletter-container {
		width: 100%;
		max-width: 800px;
		margin: -0.25rem auto 0;
	}

	h2 {
		color: #e2e8f0;
	}

	/* Responsive styles */
	@media (min-width: 768px) {
		.main-content {
			max-width: 768px;
			margin: 0 auto;
			gap: 0.6rem;
		}

		.timeline-section {
			margin: 0;
		}

		.mystery-box-container {
			max-width: 768px;
		}
	}

	@media (max-width: 480px) {
		.main-content {
			gap: 0.3rem;
			padding-top: 0.2rem;
		}

		.countdown-container {
			padding: 0 0.5rem;
		}
	}

	/* Improved styling for the BookCallout component - ULTRA MINIMAL FOR SPEED */
	:global(.book-callout-wrapper) {
		margin-top: 0.3rem;
		margin-bottom: 0.75rem;
	}

	/* Remove all decorative elements that could delay rendering */
	:global(.book-callout-wrapper::before) {
		display: none;
	}

	/* Updated Discord Component Styles */
	.discord-container {
		width: 100%;
		max-width: 800px;
		margin: 1rem auto;
		padding: 0 1rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
	}

	.discord-button {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		background-color: #5865F2;
		color: white;
		font-weight: bold;
		padding: 0.75rem 2rem;
		border-radius: 8px;
		text-decoration: none;
		font-size: 1.1rem;
		transition: all 0.2s ease;
		max-width: 400px;
		width: 100%;
		box-shadow: 0 4px 12px rgba(88, 101, 242, 0.3);
		overflow: visible;
	}

	.discord-button:hover {
		background-color: #4752c4;
		transform: translateY(-2px);
		box-shadow: 0 6px 16px rgba(88, 101, 242, 0.4);
	}

	.discord-icon-wrapper {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 12px;
	}

	.discord-icon {
		width: 24px;
		height: 24px;
	}

	.first-100-badge {
		position: absolute;
		top: -10px;
		right: -10px;
		background: #FF1F8E;
		color: white;
		font-size: 0.7rem;
		font-weight: bold;
		padding: 3px 8px;
		border-radius: 12px;
		transform: rotate(5deg);
		box-shadow: 0 2px 6px rgba(255, 31, 142, 0.5);
		z-index: 2;
	}

	.discord-tagline {
		margin-top: 0.75rem;
		color: #adb5bd;
		font-size: 0.9rem;
	}

	/* Styles for Treasure Tavern Promo */
	.treasure-promo {
		width: 100%;
		max-width: 800px;
		margin: 0.5rem auto 0.5rem;
		padding: 0 1.5rem;
		text-align: center;
		position: relative;
		z-index: 3;
	}

	.treasure-link {
		text-decoration: none;
		display: block;
		color: inherit;
		position: relative;
	}

	.treasure-content {
		background: linear-gradient(180deg, rgba(23, 25, 35, 0.6) 0%, rgba(43, 9, 104, 0.3) 100%);
		border-radius: 16px;
		padding: 1.25rem;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.08);
		transition: all 0.3s ease;
		cursor: pointer;
		position: relative;
		overflow: hidden;
	}

	.treasure-content::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(120deg, rgba(168, 240, 211, 0.05) 0%, rgba(65, 193, 234, 0.05) 100%);
		opacity: 0;
		transition: opacity 0.5s ease;
	}

	.treasure-content:hover {
		transform: translateY(-4px);
		box-shadow: 0 12px 30px rgba(65, 193, 234, 0.15);
	}

	.treasure-content:hover::before {
		opacity: 1;
	}

	.sparkle-container {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		pointer-events: none;
		overflow: hidden;
	}

	.sparkle {
		position: absolute;
		font-size: 1.4rem;
		opacity: 0.7;
		z-index: 1;
		filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.5));
		animation: float 3s ease-in-out infinite;
	}

	.sparkle-1 {
		top: 10%;
		left: 15%;
		animation-delay: 0s;
	}

	.sparkle-2 {
		bottom: 15%;
		right: 10%;
		animation-delay: 1.5s;
	}

	@keyframes float {
		0%, 100% {
			transform: translateY(0) rotate(0deg);
		}
		50% {
			transform: translateY(-10px) rotate(5deg);
		}
	}

	.treasure-promo h2 {
		font-size: 1.8rem;
		margin-bottom: 0.3rem;
		background: linear-gradient(90deg, #a8f0d3 0%, #41c1ea 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		text-fill-color: transparent;
		font-weight: bold;
		line-height: 1.2;
		letter-spacing: -0.5px;
		position: relative;
		z-index: 2;
	}

	.treasure-promo p {
		color: #e2e8f0;
		font-size: 1.1rem;
		margin-top: 0.3rem;
		margin-bottom: 0;
		opacity: 0.9;
		line-height: 1.5;
		position: relative;
		z-index: 2;
	}

	.treasure-promo::after {
		content: '';
		position: absolute;
		bottom: -20px;
		left: 50%;
		transform: translateX(-50%);
		width: 40px;
		height: 40px;
		background: linear-gradient(135deg, #41c1ea 0%, #a8f0d3 100%);
		border-radius: 50%;
		opacity: 0.5;
		filter: blur(15px);
		z-index: -1;
		animation: pulse 4s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% {
			opacity: 0.5;
			transform: translateX(-50%) scale(1);
		}
		50% {
			opacity: 0.7;
			transform: translateX(-50%) scale(1.1);
		}
	}

	@media (max-width: 768px) {
		.treasure-promo {
			margin: 0.5rem auto 0.25rem;
		}

		.treasure-content {
			padding: 1rem;
		}

		.treasure-promo h2 {
			font-size: 1.5rem;
		}

		.treasure-promo p {
			font-size: 0.95rem;
		}
	}

	/* Styles for Mystery Box Ad container */
	.mystery-box-container {
		width: 100%;
		max-width: 900px;
		margin: 0.75rem auto 1rem;
		padding: 0 1rem;
		position: relative;
		z-index: 2;
		transition: transform 0.3s ease;
	}

	.mystery-box-container::before {
		content: '';
		position: absolute;
		top: -15px;
		left: 0;
		right: 0;
		height: 30px;
		background: linear-gradient(to top, rgba(65, 193, 234, 0.1), transparent);
		z-index: 1;
	}

	/* Add subtle shimmer effect to connect the sections */
	.mystery-box-container::after {
		content: '';
		position: absolute;
		top: -30px;
		left: 50%;
		transform: translateX(-50%);
		width: 60%;
		height: 2px;
		background: linear-gradient(90deg,
			transparent,
			rgba(168, 240, 211, 0.3),
			rgba(65, 193, 234, 0.5),
			rgba(168, 240, 211, 0.3),
			transparent);
		z-index: 1;
	}

	@media (min-width: 768px) {
		.mystery-box-container {
			max-width: 768px;
		}
	}

	.news-ticker-container {
		max-width: 1200px;
		width: 95%;
		margin: 0.5rem auto 0.25rem;
		padding: 0 1rem;
		border-radius: 12px;
		overflow: hidden;
		box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
	}

	.featured-posts-container {
		max-width: 1200px;
		width: 95%;
		margin: 0.75rem auto 0.5rem;
		padding: 0 1rem;
	}

	.recent-posts {
		margin-top: -1.5rem;
	}

	@media (max-width: 768px) {
		.news-ticker-container {
			width: 92%;
			margin: 0.3rem auto 0.2rem;
		}

		.featured-posts-container {
			width: 92%;
			margin: 0.5rem auto 0.25rem;
		}
	}

	@media (max-width: 480px) {
		.news-ticker-container {
			width: 90%;
			margin: 0.25rem auto 0.1rem;
			padding: 0 0.5rem;
		}

		.featured-posts-container {
			width: 90%;
			margin: 0.5rem auto 0.25rem;
			padding: 0 0.5rem;
		}
	}

	/* Add button styles */
	.secondary-button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 0.85rem 1.5rem;
		background-color: rgba(59, 130, 246, 0.15);
		color: #60a5fa;
		font-size: 1rem;
		font-weight: 600;
		border-radius: 8px;
		border: 1px solid rgba(59, 130, 246, 0.3);
		text-decoration: none;
		transition: all 0.3s ease;
		margin-top: 1rem;
		max-width: 200px;
		margin-left: auto;
		margin-right: auto;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.secondary-button:hover {
		background-color: rgba(59, 130, 246, 0.25);
		transform: translateY(-2px);
		box-shadow: 0 6px 16px rgba(59, 130, 246, 0.2);
	}

	.arrow-icon {
		margin-left: 0.5rem;
		transition: transform 0.2s ease;
	}

	.secondary-button:hover .arrow-icon {
		transform: translateX(3px);
	}

	@media (max-width: 480px) {
		.secondary-button {
			font-size: 0.9rem;
			padding: 0.75rem 1.25rem;
			max-width: 180px;
		}
	}

	/* Added specific styling for FuturePredictions */
	:global(.future-predictions-container) {
		margin-top: 0.25rem;
	}

	/* Added styling for FeaturedPosts component to make it more compact */
	:global(.featured-posts-section) {
		margin: 1rem 0 !important;
	}

	:global(.featured-header) {
		margin-bottom: 1rem !important;
	}

	:global(.stylish-divider) {
		margin: 0.75rem auto !important;
	}

	:global(.featured-grid) {
		gap: 1.25rem !important;
	}

	/* Add consistent negative margins to pull elements closer */
	:global(.faq-container) {
		margin-top: -0.5rem;
	}
</style>

