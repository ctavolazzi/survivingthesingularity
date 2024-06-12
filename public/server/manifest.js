const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([".DS_Store","about.txt","android-chrome-192x192.png","android-chrome-512x512.png","apple-touch-icon.png","favicon-16x16.png","favicon-32x32.png","favicon.ico","favicon.png","site.webmanifest","sts-logo-image-black.png","sts-logo-image-white.png"]),
	mimeTypes: {".txt":"text/plain",".png":"image/png",".webmanifest":"application/manifest+json"},
	_: {
		client: {"start":"_app/immutable/entry/start.Dam9E6zA.js","app":"_app/immutable/entry/app.DOsf-1UT.js","imports":["_app/immutable/entry/start.Dam9E6zA.js","_app/immutable/chunks/entry.Bwi3LjvX.js","_app/immutable/chunks/scheduler.DB5l2x1O.js","_app/immutable/chunks/index.igSbMWXI.js","_app/immutable/entry/app.DOsf-1UT.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js","_app/immutable/chunks/scheduler.DB5l2x1O.js","_app/immutable/chunks/index.BzcHPuj_.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-C-rUhsDB.js')),
			__memo(() => import('./chunks/1-giVkgT0J.js')),
			__memo(() => import('./chunks/2-C3-oWJOT.js')),
			__memo(() => import('./chunks/3-CmflVW65.js')),
			__memo(() => import('./chunks/4-LZrZSTzn.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/about",
				pattern: /^\/about\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			},
			{
				id: "/contact",
				pattern: /^\/contact\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
