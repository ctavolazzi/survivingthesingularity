import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { mdsvex } from 'mdsvex';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
		// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter(),
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
		}
	},
	extensions: ['.svelte', '.md', '.svx'],
	preprocess: [
		vitePreprocess(),
		mdsvex({
			extensions: ['.md', '.svx'],
			smartypants: {
				dashes: 'oldschool'
			},
			remarkPlugins: [],
			rehypePlugins: []
		})
	]
};

export default config;
