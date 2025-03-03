<script>
	import Countdown from '$lib/components/Countdown.svelte';
	// import HeroSection from '$lib/components/HeroSection.svelte';
	import Timeline from '$lib/components/Timeline.svelte';
	import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';
	import { post } from '$lib/data/blog-posts/singularity-express/index.js';
	import FAQ from '$lib/components/FAQ.svelte';
	import LatestNews from '$lib/components/LatestNews.svelte';
	import BookSample from '$lib/components/BookSample.svelte';
	import welcomeImage from '$lib/images/sts-welcome.png';
	import timelineItems from '$lib/data/timelineItems.json';

	export let data;
	const targetDate = new Date("2027-11-20T23:59:59").getTime();
</script>

<div class="main-content">
	<Countdown {targetDate} />

	<!-- <HeroSection /> -->

  <!-- <section class="book-sample-section">
		<div class="book-sample-container">
			<BookSample />
		</div>
	</section> -->

	<Timeline />

  <FAQ />

	<div class="book-container">
		<button
			class="image-button"
			on:click={() => {
				window.location.href = '/sample';
			}}
			on:keypress={(e) => {
				if (e.key === 'Enter') {
					window.location.href = '/sample';
				}
			}}
			tabindex="0"
			aria-label="View book sample"
		>
			<img
				src={welcomeImage}
				alt="Surviving the Singularity welcome"
			/>
		</button>
	</div>

	<div class="newsletter-container">
		<div class="newsletter-inner">
			<h2 class="newsletter-heading">Join Our Community</h2>
			<p class="newsletter-text">
				Stay updated with the latest information and resources to help you prepare for the technological Singularity.
			</p>
			<NewsletterSignup />
		</div>
	</div>

	<div class="recent-posts">
		<h2 class="recent-posts-heading">Latest Insights</h2>
		<LatestNews {post} />
	</div>
</div>

<style>
	.main-content {
		max-width: 100%;
		padding: 0 1rem 1rem 1rem;
		box-sizing: border-box;
	}

	h1 {
		font-size: 2rem;
		margin-bottom: 0.5rem;
		color: #333;
	}

	.tagline {
		font-size: 1.2rem;
		margin-bottom: 1rem;
		color: #666;
	}

	.hero-section {
		padding: 1.5rem;
		background-color: #f0f4f8;
		color: #333333;
		border-radius: 8px;
		max-width: 600px;
		margin: 0 auto;
	}

	h1 {
		font-size: 2rem;
		margin-bottom: 0.5rem;
		text-align: center;
	}

	.tagline {
		font-size: 1.2rem;
		text-align: center;
		margin-bottom: 1.5rem;
		color: #a0aec0;
	}

	.content-box {
		background-color: #e2e8f0;
		padding: 1.5rem;
		border-radius: 8px;
		margin-bottom: 1.5rem;
	}

	.welcome {
		font-size: 1.1rem;
		margin-bottom: 1rem;
	}

	.mission {
		font-weight: bold;
		margin-bottom: 0.5rem;
	}

	.benefits {
		list-style-type: none;
		padding-left: 0;
	}

	.benefits li {
		margin-bottom: 0.5rem;
		padding-left: 1.5rem;
		position: relative;
	}

	.benefits li::before {
		content: "•";
		position: absolute;
		left: 0;
		color: #4299e1;
	}

	.cta-container {
		text-align: center;
	}

	.cta-button {
		display: block;
		width: 100%;
		padding: 1rem;
		background-color: #4a4a4a;
		color: white;
		border: none;
		border-radius: 4px;
		font-size: 1.1rem;
		font-weight: bold;
		cursor: pointer;
		transition: background-color 0.3s ease;
		margin-bottom: 0.5rem;
	}

	.cta-button:hover {
		background-color: #333333;
	}

	.cta-info {
		font-size: 1rem;
		font-weight: bold;
		color: #805ad5;
		margin-bottom: 0.5rem;
	}

	.cta-subtext {
		font-size: 0.9rem;
		color: #a0aec0;
	}

	.stylish-divider {
		height: 1px;
		background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
		margin: 2rem 0;
	}

	.book-container {
		max-width: 300px;
		margin: 0 auto;
	}

	.clickable-image {
		width: 100%;
		height: auto;
		border-radius: 8px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		cursor: pointer;
		transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
	}

	.image-button {
		background: none;
		border: none;
		padding: 0;
		width: 100%;
		cursor: pointer;
		display: block;
	}

	.image-button:focus {
		outline: 2px solid #3498db;
		outline-offset: 4px;
	}

	.image-button img {
		width: 100%;
		height: auto;
		border-radius: 8px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
	}

	.image-button:hover img {
		transform: scale(1.05);
		box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
	}

	/* Dark mode styles */
	:global(.dark) body {
		background-color: #1a202c;
		color: #e2e8f0;
	}

	:global(.dark) .hero-section {
		background-color: #2d3748;
		color: #e2e8f0;
	}

	:global(.dark) .content-box {
		background-color: #4a5568;
	}

	:global(.dark) .cta-button {
		background-color: #a0aec0;
	}

	:global(.dark) .cta-button:hover {
		background-color: #718096;
	}

	:global(.dark) .cta-info {
		color: #fbd38d;
	}

	:global(.dark) .singularity-path-container {
		background-color: #2d3748;
	}

	:global(.dark) .path {
		color: #b0b0b0;
	}

	:global(.dark) .singularity {
		color: #f0f0f0;
	}

	:global(.dark) .singularity::after {
		background: linear-gradient(90deg, transparent, #f0f0f0, transparent);
	}

	:global(.dark) h1, :global(.dark) h2 {
		color: #e2e8f0;
	}

	:global(.dark) .tagline {
		color: #a0aec0;
	}

	:global(.dark) .stylish-divider {
		background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
	}

	/* Responsive styles */
	@media (min-width: 768px) {
		.main-content {
			max-width: 768px;
			margin: 0 auto;
		}

		h1 {
			font-size: 2.5rem;
		}

		.tagline {
			font-size: 1.5rem;
		}

		.cta-button {
			font-size: 1.2rem;
		}
	}

	@media (min-width: 640px) {
		.hero-section {
			padding: 2rem;
		}

		h1 {
			font-size: 2.5rem;
		}

		.tagline {
			font-size: 1.4rem;
		}

		.path {
			font-size: 2rem;
		}

		.singularity {
			font-size: 4rem;
		}
	}

	.singularity-path-container {
		background-color: #e2e8f0;
		padding: 2rem 1rem;
		text-align: center;
	}

	.singularity-path-title {
		font-family: 'Arial', sans-serif;
		font-weight: bold;
		line-height: 1.2;
		margin: 0 0 2rem 0;
		padding: 0;
		text-align: center;
	}

	.path {
		display: block;
		font-size: 1.8rem;
		color: #4a4a4a;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		margin-bottom: 0.5rem;
	}

	.singularity {
		display: block;
		font-size: 3.5rem;
		color: #1a1a1a;
		position: relative;
		overflow: hidden;
	}

	.singularity::after {
		content: '';
		position: absolute;
		left: 0;
		bottom: 0;
		width: 100%;
		height: 2px;
		background: linear-gradient(90deg, transparent, #1a1a1a, transparent);
		animation: underline 2s ease-in-out infinite;
	}

	@keyframes underline {
		0% { transform: translateX(-100%); }
		50% { transform: translateX(100%); }
		100% { transform: translateX(100%); }
	}

	.timeline-subtitle {
		text-align: center;
		font-size: 1.5rem;
		color: #4a4a4a;
		margin-bottom: 2rem;
	}

	/* Dark mode styles */
	:global(.dark) .timeline-section {
		background-color: #1a1a1a;
	}

	:global(.dark) .path {
		color: #b0b0b0;
	}

	:global(.dark) .singularity {
		color: #f0f0f0;
	}

	:global(.dark) .singularity::after {
		background: linear-gradient(90deg, transparent, #f0f0f0, transparent);
	}

	:global(.dark) .timeline-subtitle {
		color: #b0b0b0;
	}

	/* Responsive styles */
	@media (min-width: 640px) {
		.path {
			font-size: 2.2rem;
		}

		.singularity {
			font-size: 4.5rem;
		}

		.timeline-subtitle {
			font-size: 1.8rem;
		}
	}

	.singularity-path-section {
		background-color: #1a202c;
		padding: 3rem 1rem;
		border-radius: 8px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.singularity-path-title {
		font-family: 'Arial', sans-serif;
		text-align: center;
		margin: 0 0 1rem 0;
		line-height: 1.2;
	}

	.path {
		display: block;
		font-size: 1.5rem;
		color: #a0aec0;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		margin-bottom: 0.5rem;
		font-weight: 300;
	}

	.singularity {
		display: block;
		font-size: 3.5rem;
		color: #f7fafc;
		font-weight: 700;
		letter-spacing: -0.02em;
	}

	.underline {
		width: 100px;
		height: 3px;
		background: linear-gradient(90deg, #4299e1, #667eea);
		margin: 1rem auto 2rem;
		border-radius: 2px;
	}

	/* Dark mode styles */
	:global(.dark) .singularity-path-section {
		background-color: #2d3748;
	}

	/* Responsive styles */
	@media (min-width: 640px) {
		.singularity-path-section {
			padding: 4rem 2rem;
		}

		.path {
			font-size: 1.8rem;
		}

		.singularity {
			font-size: 4.5rem;
		}

		.underline {
			width: 150px;
		}
	}
</style>

