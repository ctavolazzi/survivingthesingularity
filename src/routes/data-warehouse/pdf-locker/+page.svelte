<script>
    import { onMount } from 'svelte';
    import Spacer from '$lib/components/Spacer.svelte';

    let pdfData = [];

    onMount(async () => {
        const response = await fetch('/data/pdf_locker_index.csv');
        const csvText = await response.text();
        console.log("Raw CSV text:", csvText);
        pdfData = parseCsv(csvText);
        console.log("Parsed PDF Data:", pdfData);
    });

    function parseCsv(csvText) {
        const lines = csvText.trim().split('\n');
        const headers = lines[0].split(',');
        console.log("CSV Headers:", headers);
        return lines.slice(1).map((line, index) => {
            const values = line.split(',');
            console.log(`Row ${index + 1}:`, values);
            const entry = headers.reduce((obj, header, i) => {
                obj[header.trim()] = values[i] ? values[i].trim() : undefined;
                return obj;
            }, {});
            console.log(`Parsed entry ${index + 1}:`, entry);
            return entry;
        });
    }

    function openPdfUrl(url) {
        console.log("Opening URL:", url);
        if (url) {
            window.open(url, '_blank', 'noopener,noreferrer');
        } else {
            console.error("URL is undefined for this PDF");
        }
    }
</script>

<Spacer height="2rem" />
<h1 class="text-3xl font-bold mb-4">PDF Locker</h1>
<p class="mb-6 text-gray-600">Access a collection of curated PDFs related to AI, singularity, and future technologies.</p>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {#each pdfData as pdf}
        <div class="max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
            <div class="p-5">
                <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{pdf.Title}</h5>
                <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{pdf.Description}</p>
                <div class="mb-3">
                    <span class="bg-blue-100 text-blue-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-blue-900 dark:text-blue-300">
                        {pdf.Author}
                    </span>
                    <span class="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300">
                        {pdf.PublicationDate}
                    </span>
                    <span class="bg-yellow-100 text-yellow-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300">
                        {pdf.FileSize}
                    </span>
                </div>
                <button 
                    on:click={() => openPdfUrl(pdf.URL)}
                    class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                >
                    View PDF
                    <svg class="w-3.5 h-3.5 ml-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                    </svg>
                </button>
            </div>
        </div>
    {/each}
</div>

<style>
    /* Add any additional styles here */
</style>
