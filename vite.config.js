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
		sourcemap: false,
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
		/* Vite rejects requests whose Host header it does not recognise. That is
		   DNS-rebinding protection and worth keeping, so this allowlists exactly
		   one extra name rather than disabling the check.

		   Why it is needed: WebKit cannot be installed on macOS 12, so Safari
		   engine coverage runs in the Linux Playwright container instead (see the
		   comment block in playwright.config.js). From inside that container the
		   host's dev server is reachable only as host.docker.internal, and
		   without this entry vite answers every request with "Blocked request",
		   which surfaces as a page-load assertion failure rather than anything
		   that points at the real cause.

		   Do NOT change this to `allowedHosts: true`. That turns the protection
		   off for every host, which is the exact thing it exists to prevent. */
		allowedHosts: ['host.docker.internal'],
		fs: {
			allow: ['src/lib/data']
		}
	}
});
