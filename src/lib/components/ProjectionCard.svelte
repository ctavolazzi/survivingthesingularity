<script>
    export let title;
    export let description;
    export let publicationDate;
    export let organization;
    export let link;
    export let imageUrl = '';
    export let customIcon = ''; // For custom icon or emoji

    function formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    }

    function getFaviconUrl(url) {
        try {
            const domain = new URL(url).hostname;
            return `https://www.google.com/s2/favicons?domain=${domain}&sz=128`;
        } catch {
            return '/img-missing.webp';
        }
    }

    $: faviconUrl = getFaviconUrl(link);
</script>

<div class="card rounded-xl shadow-md overflow-hidden bg-white dark:bg-gray-800">
    <div class="p-4">
        <div class="flex items-start mb-2">
            <div class="w-12 h-12 rounded-lg overflow-hidden bg-gray-200 dark:bg-gray-700 flex items-center justify-center mr-3 flex-shrink-0">
                {#if customIcon}
                    <span class="text-2xl">{customIcon}</span>
                {:else if imageUrl}
                    <img src={imageUrl} alt={title} class="w-full h-full object-cover"  loading="lazy" \/\>
                {:else}
                    <img src={faviconUrl} alt={organization} class="w-8 h-8"  loading="lazy" \/\>
                {/if}
            </div>
            <div>
                <h3 class="text-lg font-bold text-gray-800 dark:text-white">{title}</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">{organization}</p>
            </div>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-300 mb-2">{description}</p>
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-4">{formatDate(publicationDate)}</p>
        <a
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center justify-center w-full py-2 px-4 rounded-full bg-blue-400 hover:bg-orange-500 text-white text-center text-sm font-semibold transition-colors duration-300"
        >
            Read Full Report
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
        </a>
    </div>
</div>

<style>
    .card {
        background-color: var(--card-bg, white);
        color: var(--card-text, black);
    }

    :global(.dark) .card {
        --card-bg: #1e293b;
        --card-text: white;
    }
</style>