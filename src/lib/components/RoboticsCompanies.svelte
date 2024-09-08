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
                <p class="dark:text-gray-300">
                    <svg class="inline-block w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <strong class="dark:text-pink-300">Description:</strong> {company['Short description']}
                </p>
                <p class="dark:text-gray-300">
                    <svg class="inline-block w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                    </svg>
                    <strong class="dark:text-pink-300">Industries:</strong> {company['Targeted industries']}
                </p>
                <p class="dark:text-gray-300">
                    <svg class="inline-block w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                    </svg>
                    <strong class="dark:text-pink-300">Product Type:</strong> {company['Product type']}
                </p>
                <p class="dark:text-gray-300">
                    <svg class="inline-block w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
                    </svg>
                    <strong class="dark:text-pink-300">Robot Type:</strong> {company['Robot or automated system type']}
                </p>
                <div class="links">
                    {#if company.Website}
                        <a href={company.Website} target="_blank" rel="noopener noreferrer" class="dark:border-blue-300 dark:text-blue-300 dark:hover:bg-blue-300 dark:hover:text-gray-800">
                            <svg class="inline-block w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path>
                            </svg>
                            Website
                        </a>
                    {/if}
                    {#if company.LinkedIn}
                        <a href={company.LinkedIn} target="_blank" rel="noopener noreferrer" class="dark:border-blue-300 dark:text-blue-300 dark:hover:bg-blue-300 dark:hover:text-gray-800">
                            <svg class="inline-block w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                            </svg>
                            LinkedIn
                        </a>
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

    svg {
        vertical-align: middle;
    }

    .links a {
        display: inline-flex;
        align-items: center;
    }
</style>