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
        title: "Research Links",
        description: "A collection of user-submitted links to research papers, articles, and other resources on AI, singularity, and future technologies.",
        lastEdited: "Dynamic",
        icon: IconData,
        link: "/data-warehouse/research-links",
        entries: "Dynamic",
        tags: ["AI", "Singularity", "Research", "Links", "User-Submitted"],
        buttonText: "View Links",
        csvUrl: "/data/research_links.csv", // This now points to the saved file
        getCSVSize: () => fetchCSVSize("/data/research_links.csv"),
        csvStructure: [
            { header: "Title", description: "Title of the research resource" },
            { header: "Author", description: "Author(s) of the resource" },
            { header: "PublicationDate", description: "Date the resource was published" },
            { header: "Description", description: "Brief summary of the resource's content" },
            { header: "URL", description: "URL to the resource" }
        ]
    },
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
    },
    {
        title: "Future Projections",
        description: "Explore insights and reports on the future of technology, employment, and societal changes.",
        lastEdited: "9.7.2024",
        icon: IconData,
        link: "/data-warehouse/future-projections",
        entries: "Dynamic", // This will be determined by the CSV content
        tags: ["Future", "Technology", "Society"],
        buttonText: "View Projections",
        csvUrl: "/data/future_projections.csv",
        getCSVSize: () => fetchCSVSize("/data/future_projections.csv"),
        csvStructure: [
            { header: "Title", description: "Title of the future projection resource" },
            { header: "Link", description: "URL to the resource" },
            { header: "Description", description: "Brief summary of the report's content" },
            { header: "PublicationDate", description: "Date the report was published" },
            { header: "Organization", description: "Organization that produced the report" }
        ]
    },
    {
        title: "PDF Locker",
        description: "Access a collection of curated PDFs related to AI, singularity, and future technologies.",
        lastEdited: "9.8.2024",
        icon: IconData,
        link: "/data-warehouse/pdf-locker",
        entries: "Dynamic", // This will be determined by the PDF collection
        tags: ["AI", "Singularity", "Research", "PDFs"],
        buttonText: "Access PDFs",
        csvUrl: "/data/pdf_locker_index.csv",
        getCSVSize: () => fetchCSVSize("/data/pdf_locker_index.csv"),
        csvStructure: [
            { header: "Title", description: "Title of the PDF document" },
            { header: "Author", description: "Author(s) of the document" },
            { header: "PublicationDate", description: "Date the document was published" },
            { header: "Description", description: "Brief summary of the document's content" },
            { header: "FileSize", description: "Size of the PDF file" },
            { header: "FileName", description: "Name of the PDF file for download" },
            { header: "URL", description: "URL to the PDF file" }
        ]
    },
];