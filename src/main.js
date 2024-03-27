import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		name: 'Surviving the Singularity'
	}
});

export default app;