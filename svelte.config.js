import adapter from '@sveltejs/adapter-cloudflare';
import { readdirSync, readFileSync } from 'node:fs';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { mdsvex } from 'mdsvex';

// One rule per static directory keeps Pages below its 100-rule limit.
// Expanding <files> emits hundreds of book-image rules and drops later rules.
const staticRoutes = readdirSync(new URL('./static/', import.meta.url), { withFileTypes: true })
	.filter((entry) => !entry.name.startsWith('.') && !['_headers', '_redirects', '_routes.json'].includes(entry.name))
	.map((entry) => `/${entry.name}${entry.isDirectory() ? '/*' : ''}`);
// Versioned download aliases already fall under /downloads/*. Only add
// redirect sources that are not covered by a static directory/file rule.
const redirectRoutes = readFileSync(new URL('./_redirects', import.meta.url), 'utf8')
	.split('\n').map((line) => line.trim()).filter((line) => line && !line.startsWith('#'))
	.map((line) => line.split(/\s+/)[0])
	.filter((path) => !staticRoutes.some((rule) => rule.endsWith('*') ? path.startsWith(rule.slice(0, -1)) : path === rule));

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			routes: { exclude: ['<build>', '<prerendered>', ...staticRoutes, ...redirectRoutes] }
		}),
		// CSP for SSR routes (Worker). SvelteKit injects a nonce into its own
		// inline scripts and adds it to this policy so 'unsafe-inline' is not
		// needed. Prerendered pages served as static assets get their CSP from
		// _headers instead (Cloudflare Pages CDN, no Worker).
		csp: {
			mode: 'auto',
			directives: {
				'default-src': ["'self'"],
				'script-src': ["'self'", 'https://static.cloudflareinsights.com'],
				'style-src': ["'self'", "'unsafe-inline'", 'https://fonts.googleapis.com'],
				'font-src': ["'self'", 'https://fonts.gstatic.com', 'data:'],
				'img-src': [
					"'self'", 'data:', 'blob:',
					'https://cdn.midjourney.com',
					'https://images.unsplash.com', 'https://plus.unsplash.com',
					'https://farm.bot',
					'https://*.futurism.com', 'https://wordpress-assets.futurism.com',
					'https://i.ytimg.com', 'https://*.ytimg.com',
					'https://www.open-electronics.org',
					'https://i.cbc.ca', 'https://content.api.news',
					'https://newatlas-brightspot.s3.amazonaws.com',
					'https://www.digitaltrends.com',
					'https://futurism.com',
					'https://i.pcmag.com',
					'https://www.testingcatalog.com', 'https://storage.ghost.io',
					'https://corticallabs.com'
				],
				'media-src': ["'self'"],
				// No Supabase origin here: every Supabase call happens server-side
				// in src/lib/server/supabaseAdmin.js, so the browser never opens a
				// connection to *.supabase.co and must not be permitted to.
				'connect-src': [
					"'self'",
					'https://cloudflareinsights.com'
				],
				'frame-src': [
					"'self'",
					'https://www.youtube.com', 'https://www.youtube-nocookie.com',
					'https://open.spotify.com', 'https://*.substack.com',
					'https://luma.com'
				],
				'base-uri': ["'self'"],
				'form-action': ["'self'"],
				'frame-ancestors': ["'self'"]
			}
		},
		// Disable prerendering for routes that use dynamic data loading
		prerender: {
			// Absolute-URL base for $page.url during prerender. Without this,
			// og:image / og:url built from $page.url bake in the default
			// http://sveltekit-prerender origin and social cards break.
			origin: 'https://survivingthesingularity.com',
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
