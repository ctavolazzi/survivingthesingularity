<script>
import { Card, Badge } from 'flowbite-svelte';
import { onMount } from 'svelte';

export let video;

function getEmbedUrl(videoId) {
    return `https://www.youtube.com/embed/${videoId}`;
}

let isLoading = true;

function handleIframeLoad() {
    isLoading = false;
}

onMount(() => {
    isLoading = true;
});
</script>

<Card class="mb-4 border-b border-gray-200 dark:border-gray-700">
    <h3 class="text-xl font-semibold mb-2">{video.Title}</h3>
    <p class="text-sm opacity-75 mb-2">By {video.Creator}</p>

    <div class="video-container mb-4">
        {#if isLoading}
        <div class="awesome-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
            <div class="spinner-core"></div>
        </div>
        {/if}
        <iframe
        src={getEmbedUrl(video.VideoId)}
        title={video.Title}
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        on:load={handleIframeLoad}
        class:hidden={isLoading}
        ></iframe>
    </div>

    <p class="mb-4">{video.Description}</p>

    <div class="flex flex-wrap gap-2 mb-4">
        {#each video.Tags.split(',') as tag}
        <Badge color="dark" class="bg-transparent border border-current">{tag.trim()}</Badge>
        {/each}
    </div>

    <a href={`https://www.youtube.com/watch?v=${video.VideoId}`} 
       target="_blank" 
       rel="noopener noreferrer" 
       class="youtube-button">
        Watch on YouTube
        <svg class="arrow-icon" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path>
        </svg>
    </a>
</Card>

<style>
    .video-container {
        position: relative;
        padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
        height: 0;
        overflow: hidden;
    }
    .video-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }

    .youtube-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 0.5rem 1rem;
        border: 2px solid #000;
        border-radius: 0.25rem;
        color: #4f46e5;
        font-weight: 500;
        text-decoration: none;
        transition: background-color 0.3s, color 0.3s;
    }

    .youtube-button:hover {
        background-color: #4f46e5;
        color: #fff;
    }

    .arrow-icon {
        width: 1.25rem;
        height: 1.25rem;
        margin-left: 0.5rem;
        fill: currentColor;
        transition: transform 0.3s;
    }

    .youtube-button:hover .arrow-icon {
        transform: translateX(4px);
    }

    :global(.dark) .youtube-button {
        border-color: #6366f1;
        color: #818cf8;
    }

    :global(.dark) .youtube-button:hover {
        background-color: #6366f1;
        color: #fff;
    }

    .awesome-spinner {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100px;
        height: 100px;
        z-index: 10;
    }

    .spinner-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 4px solid transparent;
        border-top-color: #4f46e5;
        animation: spin 1.5s linear infinite;
    }

    .spinner-ring:nth-child(2) {
        width: 80%;
        height: 80%;
        top: 10%;
        left: 10%;
        border-top-color: #818cf8;
        animation-duration: 1.75s;
        animation-direction: reverse;
    }

    .spinner-ring:nth-child(3) {
        width: 60%;
        height: 60%;
        top: 20%;
        left: 20%;
        border-top-color: #c7d2fe;
        animation-duration: 2s;
    }

    .spinner-core {
        position: absolute;
        width: 40%;
        height: 40%;
        top: 30%;
        left: 30%;
        background-color: #4f46e5;
        border-radius: 50%;
        animation: pulse 1s ease-in-out infinite alternate;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    @keyframes pulse {
        from { transform: scale(0.8); opacity: 0.8; }
        to { transform: scale(1.2); opacity: 1; }
    }

    :global(.dark) .spinner-ring {
        border-top-color: #818cf8;
    }

    :global(.dark) .spinner-ring:nth-child(2) {
        border-top-color: #c7d2fe;
    }

    :global(.dark) .spinner-ring:nth-child(3) {
        border-top-color: #e0e7ff;
    }

    :global(.dark) .spinner-core {
        background-color: #818cf8;
    }

    .hidden {
        display: none;
    }
</style>