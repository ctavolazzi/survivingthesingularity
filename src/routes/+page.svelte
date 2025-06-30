<script>
	import { onMount } from 'svelte';
	import { safeGoto } from '$lib/utils/navigation';
	import Countdown from '$lib/components/Countdown.svelte';
	// import HeroSection from '$lib/components/HeroSection.svelte';
	import Timeline from '$lib/components/Timeline.svelte';
	// Removing KnowledgeMeter import
	import BookCallout from '$lib/components/BookCallout.svelte';
	import FuturePredictions from '$lib/components/FuturePredictions.svelte';
	import { loadBlogPosts, blogPosts } from '$lib/data/blog-posts/blogPosts.js';
	import FAQ from '$lib/components/FAQ.svelte';
	import LatestNews from '$lib/components/LatestNews.svelte';
	import BookSample from '$lib/components/BookSample.svelte';
	// Using static image path for better compatibility
const welcomeImage = '/images/optimized/sts_welcome_1200.webp';
	import timelineItems from '$lib/data/timelineItems.json';

	// Removing MysteryBoxAd import
	import NewsTicker from '$lib/components/NewsTicker.svelte';
	import FeaturedPosts from '$lib/components/FeaturedPosts.svelte';

	import AGIRoadmap from '$lib/components/AGIRoadmap.svelte';
	import PathToSingularity from '$lib/components/PathToSingularity.svelte';
	// Import our new UI components
	import { Button } from '$lib/components/ui';

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
			text: 'New insights on preparing for technological transformation',
			tag: 'Analysis',
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

		// Format blog posts for the news ticker with varied, appropriate tags
		newsTickerItems = posts.map(post => {
			// Define tag based on post slug or title to create variety
			let tag = 'Blog';

			// Assign specific tags based on content type
			if (post.slug === 'singularity-express') {
				tag = 'Opinion';
			} else if (post.slug === 'farm-bot-deep-dive') {
				tag = 'Tech';
			} else if (post.slug === 'darpa-biomechanical-space-structures') {
				tag = 'News';
			} else if (post.slug === 'claude-projects-weekend-project') {
				tag = 'AI Update';
			} else if (post.slug === 'robot-farm-bot') {
				tag = 'Review';
			} else if (post.title.toLowerCase().includes('regulatory')) {
				tag = 'Policy';
			} else if (post.title.toLowerCase().includes('breakthrough')) {
				tag = 'Breaking';
			}

			return {
				date: new Date(post.date).toISOString().split('T')[0],
				text: post.title,
				tag: tag,
				link: `/blog/${post.slug}`
			};
		}).slice(0, 7);
	});

	// Replace the safeNavigate function with our imported one
	function safeNavigate(path) {
		safeGoto(path);
	}
</script>

<svelte:head>
	<!-- Preload welcome image to ensure it loads immediately -->
	<link rel="preload" href={welcomeImage} as="image" fetchpriority="high" />
</svelte:head>

<div class="main-content">
	<div class="countdown-container">
		<Countdown {targetDate} />
	</div>

	<!-- Path to Singularity Component -->
	<div class="path-to-singularity-container">
		<PathToSingularity />
	</div>



	<!-- Add News Ticker near the top for high visibility -->
	<div class="news-ticker-container">
		<NewsTicker
			title="Breaking News & Updates 🚨"
			scrollSpeed={2500}
			items={newsTickerItems}
			backgroundColor="rgba(15, 23, 42, 0.7)"
			textColor="white"
			accentColor="#ef4444"
		/>
	</div>

	<!-- Timeline section doesn't need PathToSingularity since we added it separately -->
	<div class="timeline-section">
		<Timeline />
	</div>

	<!-- Rest of the content -->
	<FuturePredictions class="future-predictions-container" />

	<div class="agi-roadmap-container">
		<AGIRoadmap />
	</div>

	<FAQ class="faq-container" />




	<div class="recent-posts">
		<LatestNews />
	</div>

	<div class="book-callout-container">
		<BookCallout />
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

	<!-- Replace Treasure Tavern Promo with enhanced component -->


	<!-- Mystery Box Ad removed -->
</div>

<style>
	.main-content {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		padding-top: 0.5rem;
	}

	.countdown-container {
		padding: 0 1rem;
	}

	.path-to-singularity-container {
		width: 95%;
		margin: 0.75rem auto;
		max-width: 1000px;
	}



	.timeline-section {
		margin: 0 auto;
		max-width: 900px;
		width: 100%;
	}

	.news-ticker-container {
		width: 95%;
		margin: 0.2rem auto 0.25rem;
		padding: 0 1rem;
	}

	.agi-roadmap-container {
		width: 100%;
		max-width: 800px;
		margin: 2rem auto;
		padding: 0 1rem;
	}





	.recent-posts,
	.book-callout-container {
		margin: 1.5rem auto;
		max-width: 800px;
		width: 100%;
	}

	.featured-posts-container {
		max-width: 1200px;
		width: 95%;
		margin: 0.75rem auto 0.5rem;
		padding: 0 1rem;
	}



	/* Responsive styles */
	@media (min-width: 768px) {
		.main-content {
			max-width: 1200px;
			margin: 0 auto;
			gap: 0.6rem;
		}

		.timeline-section {
			margin: 0 auto;
			max-width: 900px;
			width: 100%;
		}
	}

	@media (max-width: 768px) {


		.news-ticker-container {
			width: 92%;
			margin: 0.15rem auto 0.2rem;
		}

		.featured-posts-container {
			width: 92%;
			margin: 0.5rem auto 0.25rem;
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

		.path-to-singularity-container {
			padding: 0 0.5rem;
			margin: 0.5rem auto;
		}



		.news-ticker-container {
			width: 90%;
			margin: 0.1rem auto 0.1rem;
			padding: 0 0.5rem;
		}

		.featured-posts-container {
			width: 90%;
			margin: 0.5rem auto 0.25rem;
			padding: 0 0.5rem;
		}


	}
</style>

