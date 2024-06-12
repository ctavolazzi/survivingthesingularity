// import { sveltekit } from '@sveltejs/kit/vite';
// import { defineConfig } from 'vite';

// export default defineConfig({
// 	plugins: [sveltekit()],
// 	build: {
// 		rollupOptions: {
// 			external: ['stripe']
// 		}
// 	}
// });


import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  envPrefix: 'VITE_',
  build: {
    rollupOptions: {
      external: ['stripe']
    }
  }
});