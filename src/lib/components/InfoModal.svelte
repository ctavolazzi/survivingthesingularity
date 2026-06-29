<script>
	import { createEventDispatcher } from 'svelte';
	import { fade, fly } from 'svelte/transition';

	export let open = false;
	export let title = '';

	const dispatch = createEventDispatcher();

	function close() {
		dispatch('close');
	}
	function onKeydown(e) {
		if (e.key === 'Escape' && open) close();
	}
</script>

<svelte:window on:keydown={onKeydown} />

{#if open}
	<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
	<div class="backdrop" transition:fade={{ duration: 180 }} on:click={close}>
		<div
			class="modal"
			role="dialog"
			aria-modal="true"
			aria-label={title}
			transition:fly={{ y: 28, duration: 260 }}
			on:click|stopPropagation
		>
			<header>
				<h3>{title}</h3>
				<button class="close-btn" on:click={close} aria-label="Close dialog">
					<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
						<path d="M3 3L13 13M3 13L13 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
					</svg>
				</button>
			</header>
			<div class="body">
				<slot />
			</div>
		</div>
	</div>
{/if}

<style>
	.backdrop {
		position: fixed;
		inset: 0;
		z-index: 200;
		background: rgba(2, 6, 23, 0.88);
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 1.25rem;
	}
	.modal {
		width: 100%;
		max-width: 480px;
		max-height: min(80vh, 640px);
		overflow-y: auto;
		background: #0a0f23;
		border: 1px solid rgba(245, 158, 11, 0.2);
		border-left: 3px solid rgba(245, 158, 11, 0.4);
		border-radius: 0;
		box-shadow: 6px 6px 0 rgba(245, 158, 11, 0.08);
	}
	header {
		position: sticky;
		top: 0;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		padding: 1.1rem 1.35rem 0.9rem;
		background: #0f172a;
		border-bottom: 1px solid rgba(148, 163, 184, 0.15);
	}
	h3 {
		margin: 0;
		font-size: 1.05rem;
		font-weight: 700;
		color: var(--color-text-primary);
		letter-spacing: -0.01em;
	}
	.close-btn {
		flex-shrink: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		background: rgba(30, 41, 59, 0.7);
		border: 1px solid rgba(148, 163, 184, 0.2);
		border-radius: 50%;
		color: #cbd5e1;
		cursor: pointer;
		transition: color 0.2s, border-color 0.2s, transform 0.15s;
	}
	.close-btn:hover {
		color: var(--color-primary);
		border-color: var(--color-primary);
		transform: rotate(90deg);
	}
	.body {
		padding: 1.1rem 1.35rem 1.4rem;
		font-size: 0.95rem;
		line-height: 1.7;
		color: #cbd5e1;
	}
	.body :global(p) {
		margin: 0 0 0.85rem;
	}
	.body :global(p:last-child) {
		margin-bottom: 0;
	}
	.body :global(a) {
		color: var(--color-primary);
		font-weight: 600;
		text-decoration: none;
	}
	.body :global(a:hover) {
		text-decoration: underline;
	}
	.body :global(ul) {
		margin: 0 0 0.85rem;
		padding-left: 1.2rem;
	}
	.body :global(li) {
		margin-bottom: 0.35rem;
	}
	.body :global(.modal-cta) {
		display: inline-flex;
		align-items: center;
		gap: 0.45rem;
		margin-top: 0.4rem;
		padding: 0.65rem 1.1rem;
		background: var(--color-primary);
		color: #020617;
		border-radius: var(--radius-sm);
		font-weight: 700;
		font-size: 0.9rem;
	}
	.body :global(.modal-cta:hover) {
		background: var(--color-primary-light);
		text-decoration: none;
	}
	@media (max-width: 480px) {
		.backdrop {
			align-items: flex-end;
			padding: 0;
		}
		.modal {
			max-width: none;
			max-height: 82vh;
			border-radius: var(--radius-lg) var(--radius-lg) 0 0;
			border-bottom: none;
		}
	}
</style>
