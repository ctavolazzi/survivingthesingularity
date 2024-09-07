<script>
    import { onMount } from 'svelte';
    import Papa from 'papaparse';
    import Spacer from '$lib/components/Spacer.svelte';
    import { Button } from 'flowbite-svelte';

    let companies = [];
    let filteredCompanies = [];
    let loading = true;
    let error = null;
    let searchTerm = '';
    let currentPage = 1;
    const itemsPerPage = 20;

    const csvUrl = "/data/robotics_companies.csv";
    const csvSize = "50 KB"; // Update this with the actual file size

    function handleDownloadCSV() {
        window.open(csvUrl, '_blank');
    }

    onMount(async () => {
        try {
            const response = await fetch('/data/robotics_companies.csv');
            if (!response.ok) throw new Error('Failed to fetch CSV data');
            const csvData = await response.text();
            const result = Papa.parse(csvData, { 
                header: true,
                skipEmptyLines: true,
                delimiter: ',',
            });
            companies = result.data;
            console.log('Parsed data:', companies);
            filteredCompanies = companies;
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    });

    function formatCell(value, header) {
        if (header === 'Website' || header === 'LinkedIn') {
            return value ? `<a href="${value}" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">${value}</a>` : '';
        }
        return value || '';
    }

    $: {
        filteredCompanies = companies.filter(company => 
            Object.values(company).some(value => 
                value.toLowerCase().includes(searchTerm.toLowerCase())
            )
        );
    }

    $: totalPages = Math.ceil(filteredCompanies.length / itemsPerPage);
    $: paginatedCompanies = filteredCompanies.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

    function nextPage() {
        if (currentPage < totalPages) currentPage++;
    }

    function prevPage() {
        if (currentPage > 1) currentPage--;
    }
</script>

<Spacer height="70px" />

<div class="flex items-center justify-between mb-6">
    <h1 class="text-4xl font-bold">Robotics Companies</h1>
    <Button on:click={handleDownloadCSV} class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300">
        <div class="flex flex-col items-center">
            <span>Download CSV</span>
            <span class="text-sm">({csvSize})</span>
        </div>
        <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
        </svg>
    </Button>
</div>

{#if loading}
    <p class="text-center text-gray-600">Loading data...</p>
{:else if error}
    <p class="text-center text-red-500">Error: {error}</p>
{:else}
    <div class="mb-4">
        <input
            type="text"
            bind:value={searchTerm}
            placeholder="Search companies..."
            class="w-full p-2 border border-gray-300 rounded shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
    </div>

    <div class="overflow-x-auto shadow-md rounded-lg">
        <table class="min-w-full bg-white dark:bg-gray-800">
            <thead>
                <tr>
                    {#each Object.keys(companies[0] || {}) as header}
                        <th class="px-6 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-left text-xs leading-4 font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                            {header}
                        </th>
                    {/each}
                </tr>
            </thead>
            <tbody>
                {#each paginatedCompanies as company, i}
                    <tr class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
                        {#each Object.entries(company) as [header, value]}
                            <td class="px-6 py-4 whitespace-nowrap text-sm leading-5 text-gray-500 dark:text-gray-400">
                                {@html formatCell(value, header)}
                            </td>
                        {/each}
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>

    <div class="mt-4 flex justify-between items-center">
        <button
            on:click={prevPage}
            disabled={currentPage === 1}
            class="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-600 transition-colors duration-200"
        >
            Previous
        </button>
        <span class="text-gray-600">Page {currentPage} of {totalPages}</span>
        <button
            on:click={nextPage}
            disabled={currentPage === totalPages}
            class="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-600 transition-colors duration-200"
        >
            Next
        </button>
    </div>
{/if}

<style>
    .overflow-x-auto {
        max-height: 70vh;
        overflow-y: auto;
    }

    table {
        border-collapse: separate;
        border-spacing: 0;
    }

    th {
        position: sticky;
        top: 0;
        z-index: 10;
    }
</style>
