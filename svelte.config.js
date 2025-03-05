import adapter from '@sveltejs/adapter-cloudflare';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// Use Cloudflare adapter explicitly instead of adapter-auto
		adapter: adapter({
			// Cloudflare adapter options
			routes: {
				include: ['/*'],
				exclude: []
			},
			// Enable Node.js compatibility
			nodeCompat: true
		}),
		// Disable prerendering for routes that use dynamic data loading
		prerender: {
			handleHttpError: ({ path, referrer, message }) => {
				// Ignore 404s for specific paths that need dynamic loading
				if (path.startsWith('/newsletter') || path.includes('blog')) {
					return;
				}
				// Otherwise fail the build
				throw new Error(message);
			},
			handleMissingId: 'ignore'
		},
		// Add aliases for Node.js built-ins
		alias: {
			fs: '$lib/utils/cloudflare-polyfills/fs-empty.js',
			path: '$lib/utils/cloudflare-polyfills/path-empty.js',
			url: '$lib/utils/cloudflare-polyfills/url-empty.js'
		},
		// Ensure proper environment variables are available
		env: {
			publicPrefix: 'PUBLIC_',
			privatePrefix: 'PRIVATE_'
		}
	},
	preprocess: vitePreprocess()
};

export default config;
