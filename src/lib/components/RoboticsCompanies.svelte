<script>
    import { onMount } from 'svelte';
    import Papa from 'papaparse';
    import { darkMode } from '$lib/stores/darkMode';

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
    <p class="loading dark:text-blue-300">Loading...</p>
{:else if error}
    <p class="error dark:text-pink-300">{error}</p>
{:else}
    <div class="companies-grid">
        {#each companies as company}
            <div class="company-card border-pink-300 dark:border-gray-700 dark:bg-gray-800">
                <h2 class="dark:text-blue-300">{company.Name}</h2>
                <p class="dark:text-gray-300"><strong class="dark:text-pink-300">Description:</strong> {company['Short description']}</p>
                <p class="dark:text-gray-300"><strong class="dark:text-pink-300">Industries:</strong> {company['Targeted industries']}</p>
                <p class="dark:text-gray-300"><strong class="dark:text-pink-300">Product Type:</strong> {company['Product type']}</p>
                <p class="dark:text-gray-300"><strong class="dark:text-pink-300">Robot Type:</strong> {company['Robot or automated system type']}</p>
                <div class="links">
                    {#if company.Website}
                        <a href={company.Website} target="_blank" rel="noopener noreferrer" class="dark:border-blue-300 dark:text-blue-300 dark:hover:bg-blue-300 dark:hover:text-gray-800">Website</a>
                    {/if}
                    {#if company.LinkedIn}
                        <a href={company.LinkedIn} target="_blank" rel="noopener noreferrer" class="dark:border-blue-300 dark:text-blue-300 dark:hover:bg-blue-300 dark:hover:text-gray-800">LinkedIn</a>
                    {/if}
                </div>
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
        padding: 20px;
        transition: transform 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
        border-width: 2px;
        border-style: solid;
        border-radius: 10px;
        background-color: white;
    }

    .company-card:hover {
        transform: translateY(-5px);
        border-color: #ff00aa; /* Darker pink on hover */
    }

    h2 {
        margin-top: 0;
        font-size: 1.5rem;
        margin-bottom: 10px;
        color: #00aeff;
    }

    p {
        margin: 8px 0;
        color: #1f1c1c;
    }

    strong {
        color: #ff00aa;
    }

    .links {
        margin-top: 15px;
    }

    a {
        display: inline-block;
        margin-right: 10px;
        color: #00aeff;
        text-decoration: none;
        padding: 5px 10px;
        border: 1px solid #00aeff;
        border-radius: 5px;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    a:hover {
        background-color: #00aeff;
        color: #1a1a1a;
    }

    .loading, .error {
        text-align: center;
        color: #00aeff;
        font-size: 1.2rem;
        margin-top: 20px;
    }

    .error {
        color: #ff00aa;
    }

    :global(.dark) .company-card {
        background-color: #1a202c;
        border-color: #2d3748;
    }

    :global(.dark) .company-card:hover {
        border-color: #4a5568;
    }
</style>