<script>
	import { audience, AUDIENCES } from '$lib/stores/audienceStore.js';

	const modes = Object.values(AUDIENCES);
	let open = false;

	function select(key) {
		audience.set(key);
		open = false;
	}

	function handleKeydown(e) {
		if (e.key === 'Escape') open = false;
	}
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="switcher" class:switcher--open={open}>
	<button
		class="trigger"
		type="button"
		aria-haspopup="listbox"
		aria-expanded={open}
		on:click={() => (open = !open)}
	>
		Who are you?
		<svg class="caret" width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true">
			<path d="M2 3.5L5 6.5L8 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
		</svg>
	</button>

	{#if open}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<div class="backdrop" on:click={() => (open = false)}></div>
		<ul class="dropdown" role="listbox" aria-label="Select your role">
			{#each modes as mode}
				<li
					role="option"
					aria-selected={$audience === mode.key}
					class="option"
					class:option--active={$audience === mode.key}
					on:click={() => select(mode.key)}
					on:keydown={(e) => e.key === 'Enter' && select(mode.key)}
					tabindex="0"
				>
					{mode.label}
					{#if $audience === mode.key}
						<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
							<path d="M2 6L5 9L10 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					{/if}
				</li>
			{/each}
		</ul>
	{/if}
</div>

<style>
	.switcher {
		position: relative;
	}

	.trigger {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		padding: 0.2rem 0.55rem;
		background: transparent;
		border: none;
		border-radius: 5px;
		color: #e2e8f0;
		font-size: 0.72rem;
		font-weight: 500;
		font-family: var(--font-primary, 'Inter', sans-serif);
		cursor: pointer;
		white-space: nowrap;
		transition: background 0.15s, border-color 0.15s;
		line-height: 1.4;
		outline: none;
	}

	.trigger:hover {
		background: rgba(255, 255, 255, 0.07);
	}

	.switcher--open .trigger {
		background: rgba(255, 255, 255, 0.07);
	}

	.caret {
		color: #94a3b8;
		transition: transform 0.15s;
	}

	.switcher--open .caret {
		transform: rotate(180deg);
	}

	.backdrop {
		position: fixed;
		inset: 0;
		z-index: 49;
	}

	.dropdown {
		position: absolute;
		top: calc(100% + 6px);
		right: 0;
		z-index: 50;
		background: #0f172a;
		border: 1px solid rgba(100, 116, 139, 0.3);
		border-radius: 8px;
		padding: 4px;
		min-width: 140px;
		list-style: none;
		margin: 0;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
	}

	.option {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		padding: 0.45rem 0.75rem;
		border-radius: 5px;
		font-size: 0.82rem;
		font-weight: 500;
		font-family: var(--font-primary, 'Inter', sans-serif);
		color: #94a3b8;
		cursor: pointer;
		transition: background 0.1s, color 0.1s;
	}

	.option:hover {
		background: rgba(100, 116, 139, 0.15);
		color: #e2e8f0;
	}

	.option--active {
		color: #f59e0b;
	}

	.option--active:hover {
		background: rgba(245, 158, 11, 0.1);
	}
</style>
