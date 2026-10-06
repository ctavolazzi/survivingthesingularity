import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { imagetools } from 'vite-imagetools';

export default defineConfig({
	// Isolated cache (worktree shares node_modules with the main repo via symlink).
	cacheDir: '.vite-game',
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
			// node_modules is symlinked to the main repo, whose real path sits
			// outside this worktree. Allow both roots so Vite can serve the
			// SvelteKit client runtime (otherwise it 403s the symlinked deps).
			allow: [
				'.',
				'/Users/ctavolazzi/Code/active/survivingthesingularity'
			]
		}
	}
});
