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

<div class="main-content">
	<div class="countdown-container">
		<Countdown {targetDate} />
	</div>

	<!-- <HeroSection /> -->

  <!-- <section class="book-sample-section">
		<div class="book-sample-container">
			<BookSample />
		</div>
	</section> -->

	<Timeline />
	<!-- Removing KnowledgeMeter component -->
	<div class="book-callout-wrapper">
		<BookCallout
			title="Navigate the Path to Singularity"
			description="Get the insights and strategies you need to prepare for the technological changes that will reshape our world."
			buttonText="Explore the Book"
			buttonLink="/sample"
		/>
	</div>

	<FuturePredictions />

  <FAQ />

	<div class="book-container">
		<a
			href="/sample"
			class="image-button"
			aria-label="View book sample"
		>
			<img
				src={welcomeImage}
				alt="Surviving the Singularity welcome"
				class="welcome-image"
			/>
		</a>
	</div>

	<div class="newsletter-container">
		<NewsletterSignup />
		<DiscordButton />
	</div>

	<div class="recent-posts">
		<LatestNews {latestPost} />
	</div>
</div>

<style>
	.main-content {
		max-width: 100%;
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 1.2rem;
		padding-top: 1rem;
	}

	.countdown-container {
		width: 100%;
		max-width: 100%;
		overflow-x: hidden;
		padding: 0 1rem;
	}

	.book-container {
		display: flex;
		justify-content: center;
		align-items: center;
		margin: 2rem 0;
		width: 100%;
		max-width: 300px;
		margin: 0 auto;
	}

	.welcome-image {
		max-width: 100%;
		height: auto;
		border-radius: 0.5rem;
		box-shadow: 0 4px 6px -1px rgba(255, 255, 255, 0.1), 0 2px 4px -1px rgba(255, 255, 255, 0.06);
		transition: transform 0.3s ease, box-shadow 0.3s ease;
	}

	.welcome-image:hover {
		transform: translateY(-5px);
		box-shadow: 0 10px 15px -3px rgba(255, 255, 255, 0.1), 0 4px 6px -2px rgba(255, 255, 255, 0.05);
	}

	.image-button {
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		max-width: 100%;
		transition: filter 0.3s ease;
		width: 100%;
		display: block;
	}

	.image-button:focus {
		outline: 2px solid #4299e1;
		border-radius: 0.5rem;
		outline-offset: 4px;
	}

	.image-button img {
		width: 100%;
		height: auto;
		border-radius: 8px;
		box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
		transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
	}

	.image-button:hover img {
		transform: scale(1.05);
		box-shadow: 0 6px 12px rgba(255, 255, 255, 0.15);
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
		}
	}

	@media (min-width: 640px) {
	}

	/* Improved styling for the BookCallout component */
	:global(.book-callout-wrapper) {
		margin-top: 1rem;
		margin-bottom: 2rem;
		position: relative;
		z-index: 1;
		transform: scale(1.03);
	}

	/* Add a more dramatic glow effect behind the BookCallout */
	:global(.book-callout-wrapper::before) {
		content: "";
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 100%;
		height: 100%;
		background: radial-gradient(ellipse, rgba(59, 130, 246, 0.2) 0%, rgba(17, 24, 39, 0) 70%);
		filter: blur(60px);
		z-index: -1;
		animation: pulse-glow 8s ease-in-out infinite alternate;
	}

	@keyframes pulse-glow {
		0% {
			opacity: 0.5;
			transform: translate(-50%, -50%) scale(0.9);
		}
		100% {
			opacity: 0.8;
			transform: translate(-50%, -50%) scale(1.1);
		}
	}

	/* Add a subtle divider before and after the BookCallout */
	:global(.book-callout-wrapper::after) {
		content: "";
		position: absolute;
		bottom: -1.5rem;
		left: 50%;
		transform: translateX(-50%);
		width: 60%;
		height: 1px;
		background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
		z-index: -1;
	}

	:global(.timeline-container + .book-callout-wrapper::before) {
		content: "";
		position: absolute;
		top: -1.5rem;
		left: 50%;
		transform: translateX(-50%);
		width: 60%;
		height: 1px;
		background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
		z-index: -1;
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

