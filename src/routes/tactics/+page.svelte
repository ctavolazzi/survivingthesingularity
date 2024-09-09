<script>
    import { onMount } from 'svelte';
    import { tacticLibrary } from '$lib/stores/tacticLibrary';
    import TacticCard from '$lib/components/TacticCard.svelte';

    let tactics = [];

    onMount(() => {
        tacticLibrary.fetchTactics();
    });

    tacticLibrary.subscribe(value => {
        tactics = value;
    });
</script>

<h1 class="text-3xl font-bold mb-6">Tactics</h1>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each tactics as tactic (tactic.id)}
        <TacticCard {tactic} />
    {/each}
</div>