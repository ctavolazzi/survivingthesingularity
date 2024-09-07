import { IconData } from '$lib/assets/Icons.svelte';

async function fetchCSVSize(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const blob = await response.blob();
        const sizeInBytes = blob.size;
        
        if (sizeInBytes < 1024) {
            return `${sizeInBytes} B`;
        } else if (sizeInBytes < 1048576) {
            return `${(sizeInBytes / 1024).toFixed(1)} KB`;
        } else {
            return `${(sizeInBytes / 1048576).toFixed(1)} MB`;
        }
    } catch (error) {
        console.error('Error fetching CSV size:', error);
        return 'Size unknown';
    }
}

export const dataResources = [
    {
        title: "Robotics Companies",
        description: "Comprehensive list of robotics companies with detailed information, including websites and industry focus.",
        lastEdited: "9.5.2024",
        icon: IconData,
        link: "/data-warehouse/robotics-companies",
        entries: 393,
        tags: ["Robotics", "Industry"],
        buttonText: "View Companies",
        csvUrl: "/data/robotics_companies.csv",
        getCSVSize: () => fetchCSVSize("/data/robotics_companies.csv")
    },
    // Add more data resources here
    {
        title: "AI and Singularity Videos",
        description: "A curated collection of informative videos about AI, technological singularity, and related topics.",
        lastEdited: "9.6.2024",
        icon: IconData,
        link: "/data-warehouse/youtube-resources",
        entries: "Dynamic", // This will be determined by the CSV content
        tags: ["AI", "Singularity", "Videos"],
        buttonText: "View Videos",
        csvUrl: "/data/ai_singularity_videos.csv",
        getCSVSize: () => fetchCSVSize("/data/ai_singularity_videos.csv")
    }
];