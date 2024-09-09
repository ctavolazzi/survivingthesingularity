<script>
    import { page } from '$app/stores';
    import { tacticLibrary } from '$lib/stores/tacticLibrary';
    
    $: tactic = $tacticLibrary.find(t => t.slug === $page.params.slug);
</script>

<div class="container">
    {#if tactic}
        <h1>{tactic.title}</h1>
        <p>{tactic.description}</p>
        <!-- Add more detailed content here -->
    {:else}
        <p>Tactic not found</p>
    {/if}
</div>

<style>
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
</style>