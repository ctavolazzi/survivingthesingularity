<script>
    import { onMount } from 'svelte';
    import Papa from 'papaparse';

    let companies = [];
    let loading = true;
    let error = null;

    onMount(async () => {
        try {
            const response = await fetch('/data/robotics_companies.csv');
            const csvData = await response.text();
            const result = Papa.parse(csvData, { header: true });
            companies = result.data;
            loading = false;
        } catch (e) {
            error = "Failed to load data";
            loading = false;
        }
    });
</script>

{#if loading}
    <p>Loading...</p>
{:else if error}
    <p>{error}</p>
{:else}
    <div class="companies-grid">
        {#each companies as company}
            <div class="company-card">
                <h2>{company.Name}</h2>
                <p><strong>Description:</strong> {company['Short description']}</p>
                <p><strong>Industries:</strong> {company['Targeted industries']}</p>
                <p><strong>Product Type:</strong> {company['Product type']}</p>
                <p><strong>Robot Type:</strong> {company['Robot or automated system type']}</p>
                {#if company.Website}
                    <a href={company.Website} target="_blank" rel="noopener noreferrer">Website</a>
                {/if}
                {#if company.LinkedIn}
                    <a href={company.LinkedIn} target="_blank" rel="noopener noreferrer">LinkedIn</a>
                {/if}
            </div>
        {/each}
    </div>
{/if}

<style>
    .companies-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        padding: 20px;
    }

    .company-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .company-card:hover {
        transform: translateY(-5px);
    }

    h2 {
        margin-top: 0;
        color: #00aeff;
    }

    a {
        display: inline-block;
        margin-top: 10px;
        margin-right: 10px;
        color: #ff00aa;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
</style>