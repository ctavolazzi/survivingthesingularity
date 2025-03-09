import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { imagetools } from 'vite-imagetools';

export default defineConfig({
	plugins: [
		sveltekit(),
		imagetools({
			defaultDirectives: () => {
				return new URLSearchParams([
					['format', 'webp'],
					['quality', '80'],
					['as', 'picture']
				]);
			},
			include: '**/*.{jpeg,jpg,png,webp}',
			exclude: ['**/node_modules/**']
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
	}
});
