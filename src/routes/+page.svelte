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

	// Direct load for fast loading components
	export const data = {};
	const targetDate = new Date("2027-11-20T23:59:59").getTime();

	// We'll populate this later
	let posts = [];
	let latestPost = null;

	// Load the blog posts when the component is created
	onMount(async () => {
		posts = await loadBlogPosts();
		// Get the first post for the latest news section
		latestPost = posts.length > 0 ? posts[0] : null;
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

	<!-- Rest of the content -->
	<FuturePredictions />

	<FAQ />

	<div class="newsletter-container">
		<NewsletterSignup />
		<DiscordButton />
	</div>

	<div class="recent-posts">
		<LatestNews {latestPost} />
	</div>
</div>

<style>
	/* Styles removed for components using inline styles for maximum speed */

	.main-content {
		max-width: 100%;
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
		padding-top: 0.75rem;
	}

	.countdown-container {
		width: 100%;
		max-width: 100%;
		overflow-x: hidden;
		padding: 0 1rem;
		margin-bottom: 0.5rem;
	}

	.timeline-section {
		margin: 0 0.75rem;
	}

	.newsletter-container {
		width: 100%;
		max-width: 800px;
		margin: 0 auto;
	}

	h2 {
		color: #e2e8f0;
	}

	/* Responsive styles */
	@media (min-width: 768px) {
		.main-content {
			max-width: 768px;
			margin: 0 auto;
			gap: 1.5rem;
		}

		.timeline-section {
			margin: 0;
		}
	}

	@media (max-width: 480px) {
		.main-content {
			gap: 0.5rem;
			padding-top: 0.5rem;
		}

		.countdown-container {
			padding: 0 0.75rem;
		}
	}

	/* Improved styling for the BookCallout component - ULTRA MINIMAL FOR SPEED */
	:global(.book-callout-wrapper) {
		margin-top: 1rem;
		margin-bottom: 2rem;
	}

	/* Remove all decorative elements that could delay rendering */
	:global(.book-callout-wrapper::before) {
		display: none;
	}

	/* Updated Discord Component Styles */
	.discord-container {
		width: 100%;
		max-width: 800px;
		margin: 2.5rem auto;
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
</style>

