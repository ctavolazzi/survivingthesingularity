import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit()
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
			// These are Node.js built-ins that need to be ignored in Cloudflare
			fs: 'undefined',
			path: 'undefined',
			url: 'undefined'
		}
	},
	// Optimization settings
	optimizeDeps: {
		include: ['marked', 'gray-matter'],
		exclude: ['fs', 'path', 'url']
	}
});
