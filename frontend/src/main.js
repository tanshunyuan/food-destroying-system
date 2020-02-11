import Root from './Root.svelte';

const app = new Root({
	target: document.body,
});

window.app = app;

export default app;
