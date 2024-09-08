<script>
    import { onMount } from 'svelte';
    import { Card, Button, Label, Input, Textarea } from 'flowbite-svelte';
    import { parse, isValid, format, parseISO } from 'date-fns';
    import { browser } from '$app/environment';
    let cachedData = {};
    
    let link = {
        url: '',
        title: '',
        author: '',
        description: '',
        tags: '',
        notes: '',
        dateOfPublication: ''
    };

    let dateError = '';

    // Load cached form data on component mount
    onMount(() => {
        if (browser) {
            const cachedData = localStorage.getItem('researchLinkFormData');
            if (cachedData) {
                link = JSON.parse(cachedData);
            }
        }
    });

    // Cache form data whenever it changes
    $: {
        if (browser) {
            localStorage.setItem('researchLinkFormData', JSON.stringify(link));
        }
    }

    function parseDate(dateString) {
        const formats = [
            'yyyy-MM-dd',
            'MMMM yyyy',
            'MMM yyyy',
            'MMMM d yyyy',
            'MMM d yyyy',
            'yyyy'
        ];

        for (let fmt of formats) {
            const date = parse(dateString, fmt, new Date());
            if (isValid(date)) {
                return date;
            }
        }

        // Try parsing as ISO date string (for dates already in yyyy-MM-dd format)
        const isoDate = parseISO(dateString);
        if (isValid(isoDate)) {
            return isoDate;
        }

        return null; // Return null if parsing fails
    }

    function validateDate() {
        const parsedDate = parseDate(link.dateOfPublication);
        if (parsedDate) {
            const currentDate = new Date();
            const year = parsedDate.getFullYear();

            if (parsedDate > currentDate) {
                dateError = 'Warning: This is a future date. Are you sure this is correct?';
            } else if (year < 1000 || year > 9999) {
                dateError = 'Warning: This date is unusually old or far in the future. Please double-check for accuracy.';
            } else {
                link.dateOfPublication = format(parsedDate, 'yyyy-MM-dd');
                dateError = '';
            }
        } else if (link.dateOfPublication) {
            dateError = 'Invalid date format. Please use a format like "August 2002" or "2002-08-15".';
        } else {
            dateError = '';
        }
    }

    async function handleSubmit() {
        validateDate();
        if (dateError) {
            alert(dateError);
            return;
        }

        const formData = {
            ...link,
            tags: link.tags.split(',').map(tag => tag.trim()).filter(tag => tag !== ''),
            date_of_publication: link.dateOfPublication || null
        };

        try {
            const response = await fetch('/data-warehouse/research-links/contribute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                alert('Link added successfully!');
                // Clear form and cached data on successful submission
                link = { url: '', title: '', author: '', description: '', tags: '', notes: '', dateOfPublication: '' };
                localStorage.removeItem('researchLinkFormData');
                dateError = '';
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to add link');
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }
</script>

<svelte:head>
    <title>Add Research Link | Surviving the Singularity</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-4xl sm:text-5xl font-extrabold mb-2 text-gray-900 dark:text-gray-100">
        Add Your Research
    </h1>
    <p class="text-xl mb-6 text-gray-600 dark:text-gray-300 max-w-3xl">
        Add a link to your research here.
    </p>
    <div class="flex space-x-4 mb-8">
        <Button color="light" href="/data-warehouse/research-links" class="flex items-center">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            Back to Research Links
        </Button>    </div>
</div>
<Card class="max-w-2xl mx-auto">
    <form on:submit|preventDefault={handleSubmit}>
        <div class="mb-4">
            <Label for="url" class="mb-2">Research Link (required)</Label>
            <Input type="url" id="url" placeholder="Enter URL" required bind:value={link.url} />
        </div>
        <div class="mb-4">
            <Label for="title" class="mb-2">Title</Label>
            <Input type="text" id="title" placeholder="Enter title" bind:value={link.title} />
        </div>
        <div class="mb-4">
            <Label for="author" class="mb-2">Author(s)</Label>
            <Input type="text" id="author" placeholder="Enter author(s)" bind:value={link.author} />
        </div>
        <div class="mb-4">
            <Label for="description" class="mb-2">Description</Label>
            <Textarea id="description" placeholder="Enter description" bind:value={link.description} />
        </div>
        <div class="mb-4">
            <Label for="tags" class="mb-2">Tags (comma-separated)</Label>
            <Input type="text" id="tags" placeholder="Enter tags" bind:value={link.tags} />
        </div>
        <div class="mb-4">
            <Label for="dateOfPublication" class="mb-2">Date of Publication</Label>
            <Input type="text" id="dateOfPublication" placeholder="e.g. August 2002" 
                   bind:value={link.dateOfPublication} on:blur={validateDate} />
            {#if dateError}
                <p class="text-red-500 text-sm mt-1">{dateError}</p>
            {/if}
        </div>
        <div class="mb-4">
            <Label for="notes" class="mb-2">Notes</Label>
            <Textarea id="notes" placeholder="Enter notes" bind:value={link.notes} />
        </div>
        <Button type="submit" class="w-full">Add Link</Button>
    </form>
</Card>

<div class="max-w-2xl mx-auto mt-8 p-6 bg-gray-100 dark:bg-gray-800 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">What happens next?</h2>
    <ol class="list-decimal list-inside space-y-2 text-gray-700 dark:text-gray-300">
        <li>Your submitted link and associated information will be added to our research database.</li>
        <li>The link will be available for other users to view and reference in their research.</li>
        <li>You can edit or remove your submitted links at any time by logging into your account.</li>
        <li>Our team may review submissions to ensure quality and relevance.</li>
        <li>Your contribution helps build a comprehensive resource for the community.</li>
    </ol>
    <p class="mt-4 text-gray-600 dark:text-gray-400">
        Note: Please ensure all submitted content complies with our community guidelines and respects intellectual property rights.
    </p>
</div>

<style>
    /* don't put global styles here for now */
</style>