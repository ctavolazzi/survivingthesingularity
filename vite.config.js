import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { nodePolyfills } from 'vite-plugin-node-polyfills';

export default defineConfig({
	plugins: [
		sveltekit(),
		// Add Node.js polyfills for Cloudflare
		nodePolyfills({
			// Whether to polyfill `node:` protocol imports.
			protocolImports: true,
			// Polyfills for specific Node.js modules
			include: ['fs', 'path', 'url', 'stream']
		})
	],
	assetsInclude: ['**/*.md'],
	build: {
		sourcemap: true,
		rollupOptions: {
			onwarn(warning, warn) {
				// Ignore URL-related warnings that might be causing the build to fail
				if (warning.code === 'INVALID_URL' ||
				    warning.code === 'UNRESOLVED_IMPORT' ||
				    warning.code === 'EMPTY_BUNDLE') {
					return;
				}
				warn(warning);
			}
		}
	},
	server: {
		fs: {
			allow: ['src/lib/data']
		}
	},
	// Add specific configuration for Cloudflare
	ssr: {
		// Avoid using Node.js built-in modules in SSR
		noExternal: ['marked', 'gray-matter', 'papaparse']
	},
	resolve: {
		// Explicitly tell Vite not to try to resolve these Node builtins
		browserField: true,
		conditions: ['browser', 'module', 'jsnext:main', 'jsnext'],
		alias: {
			// Use our polyfills
			fs: '$lib/utils/cloudflare-polyfills/fs-empty.js',
			path: '$lib/utils/cloudflare-polyfills/path-empty.js',
			url: '$lib/utils/cloudflare-polyfills/url-empty.js',
			stream: '$lib/utils/cloudflare-polyfills/stream-empty.js'
		}
	},
	// Optimization settings
	optimizeDeps: {
		include: ['marked', 'gray-matter'],
		exclude: ['fs', 'path', 'url', 'stream']
	}
});
