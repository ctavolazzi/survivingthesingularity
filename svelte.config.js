// import adapter from '@sveltejs/adapter-node';

// /** @type {import('@sveltejs/kit').Config} */
// const config = {
// 	kit: {
// 		adapter: adapter({
// 			// default options are shown
// 			// out: 'build',
// 			out: 'public',
// 			precompress: false,
// 			env: {
// 				host: 'HOST',
// 				port: 'PORT'
// 			}
// 		})
// 	}
// };

// export default config;

import adapter from '@sveltejs/adapter-node';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
        adapter: adapter({
            out: 'build', // Directory where the build output will be generated
            precompress: false,
            env: {
                host: 'HOST',
                port: 'PORT'
            }
        })
    }
};

export default config;
