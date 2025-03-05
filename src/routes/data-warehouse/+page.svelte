<script>
    import { dataResources } from '$lib/data/dataResources.js';
    import { Card, Button, Badge, Tooltip, Tabs, TabItem, Pagination } from 'flowbite-svelte';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    function handleViewDataset(link) {
        goto(link);
    }

    // Pagination state
    let booksCurrentPage = 1;
    let articlesCurrentPage = 1;
    let otherCurrentPage = 1;
    let videosCurrentPage = 1;
    let dataWarehouseCurrentPage = 1;

    const itemsPerPage = 3;

    // Helper function to paginate array
    function paginateArray(array, currentPage, itemsPerPage) {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        return array.slice(startIndex, endIndex);
    }

    // Recommended reading - Books
    const recommendedBooks = [
        {
            title: "Superintelligence: Paths, Dangers, Strategies",
            author: "Nick Bostrom",
            description: "A comprehensive analysis of the potential future of machine intelligence and its implications.",
            link: "https://www.amazon.com/Superintelligence-Dangers-Strategies-Nick-Bostrom/dp/0198739834"
        },
        {
            title: "Life 3.0: Being Human in the Age of Artificial Intelligence",
            author: "Max Tegmark",
            description: "Explores how AI might affect crime, war, justice, jobs, society and our sense of being human.",
            link: "https://www.amazon.com/Life-3-0-Being-Artificial-Intelligence/dp/1101946598"
        },
        {
            title: "Human Compatible: Artificial Intelligence and the Problem of Control",
            author: "Stuart Russell",
            description: "A leading AI researcher examines how we can ensure that increasingly powerful AI systems remain aligned with human values.",
            link: "https://www.amazon.com/Human-Compatible-Artificial-Intelligence-Problem/dp/0525558632"
        },
        {
            title: "The Alignment Problem",
            author: "Brian Christian",
            description: "How can we ensure that AI systems do what we want them to do?",
            link: "https://www.amazon.com/Alignment-Problem-Machine-Learning-Values/dp/0393635821"
        },
        {
            title: "AI 2041: Ten Visions for Our Future",
            author: "Kai-Fu Lee & Chen Qiufan",
            description: "A blend of fiction and analysis exploring how AI might transform society over the next 20 years.",
            link: "https://www.amazon.com/AI-2041-Ten-Visions-Future/dp/059323829X"
        }
    ];

    // Recommended reading - Articles/Blog Posts
    const recommendedArticles = [
        {
            title: "Artificial Intelligence: A Modern Approach",
            author: "Stuart Russell and Peter Norvig",
            description: "The standard text in AI, used in universities worldwide.",
            link: "https://aima.cs.berkeley.edu/"
        },
        {
            title: "Alignment Research Center: Progress Report",
            author: "Paul Christiano",
            description: "Updates on AI alignment research and progress toward safe AI systems.",
            link: "https://www.alignmentresearch.org/"
        },
        {
            title: "AI Alignment: Why It's Hard, and Where to Start",
            author: "Eliezer Yudkowsky",
            description: "An introduction to the challenges of aligning advanced AI systems with human values.",
            link: "https://intelligence.org/2016/12/28/ai-alignment-why-its-hard-and-where-to-start/"
        },
        {
            title: "The Bitter Lesson",
            author: "Rich Sutton",
            description: "A reflection on the history of AI research and the power of computation.",
            link: "http://www.incompleteideas.net/IncIdeas/BitterLesson.html"
        },
        {
            title: "Concrete Problems in AI Safety",
            author: "Dario Amodei et al.",
            description: "A research paper outlining practical safety challenges in modern AI systems.",
            link: "https://arxiv.org/abs/1606.06565"
        }
    ];

    // Recommended reading - Other resources
    const recommendedOther = [
        {
            title: "AI Safety Resources",
            author: "Effective Altruism Forum",
            description: "A comprehensive collection of resources on AI safety and alignment.",
            link: "https://forum.effectivealtruism.org/posts/bsE5t6qhGC65fEpzN/ai-safety-resources"
        },
        {
            title: "Machine Learning for Humans",
            author: "Vishal Maini & Samer Sabri",
            description: "A series that explains machine learning concepts in simple terms.",
            link: "https://medium.com/machine-learning-for-humans/why-machine-learning-matters-6164faf1df12"
        },
        {
            title: "AI Alignment Podcast",
            author: "Lucas Perry",
            description: "Conversations with researchers working on AI alignment and safety.",
            link: "https://futureoflife.org/ai-alignment-podcast/"
        },
        {
            title: "Stampy's Wiki",
            author: "AI Safety Community",
            description: "A collaboratively edited knowledge base for AI safety concepts.",
            link: "https://stampy.ai/"
        }
    ];

    // Video categories
    const videoCategories = {
        "AI Safety": [
            {
                title: "The Alignment Problem: Machine Learning and Human Values",
                creator: "Robert Miles",
                description: "An in-depth exploration of AI alignment challenges and potential solutions.",
                youtubeId: "EUjc1WuyPT8"
            },
            {
                title: "AI Safety: Challenges and Strategies",
                creator: "Future of Life Institute",
                description: "Overview of key AI safety concerns and research directions.",
                youtubeId: "3TYT1QfdfsM"
            },
            {
                title: "The Case for Taking AI Seriously as a Threat",
                creator: "Sam Harris",
                description: "A philosophical perspective on AI risk and why we should be concerned.",
                youtubeId: "BXRLoKQHu-k"
            }
        ],
        "Future of Intelligence": [
            {
                title: "The Singularity, Skynet, and the Future of Humanity",
                creator: "Lex Fridman Podcast",
                description: "Discussion with Max Tegmark about AI, consciousness, and the future of intelligence.",
                youtubeId: "PqbB07n_uQ4"
            },
            {
                title: "Artificial General Intelligence: Humanity's Last Invention",
                creator: "Two Minute Papers",
                description: "A concise explanation of AGI and its potential implications.",
                youtubeId: "Yd1XTQ2Y0Ks"
            }
        ],
        "Technical Concepts": [
            {
                title: "How Neural Networks Learn",
                creator: "3Blue1Brown",
                description: "Visual explanation of how neural networks are trained and function.",
                youtubeId: "IHZwWFHWa-w"
            },
            {
                title: "The Mathematics of Neural Networks",
                creator: "Siraj Raval",
                description: "Mathematical foundations behind modern AI systems.",
                youtubeId: "ov_RkIJptwE"
            }
        ]
    };

    // Flatten videos for pagination
    let selectedVideoCategory = Object.keys(videoCategories)[0];
    $: currentVideos = videoCategories[selectedVideoCategory] || [];
    $: paginatedVideos = paginateArray(currentVideos, videosCurrentPage, itemsPerPage);
    $: videoPageCount = Math.ceil(currentVideos.length / itemsPerPage);

    // Group data resources by category
    const dataCategories = {
        "Research & Analysis": dataResources.filter(r => r.tags.some(t => ["Research", "AI", "Singularity"].includes(t))),
        "Industry & Companies": dataResources.filter(r => r.tags.some(t => ["Industry", "Robotics", "Companies"].includes(t))),
        "Media & Resources": dataResources.filter(r => r.tags.some(t => ["Videos", "PDFs", "Links"].includes(t)))
    };

    let selectedDataCategory = Object.keys(dataCategories)[0];
    $: currentDataResources = dataCategories[selectedDataCategory] || [];
    $: paginatedDataResources = paginateArray(currentDataResources, dataWarehouseCurrentPage, itemsPerPage);
    $: dataPageCount = Math.ceil(currentDataResources.length / itemsPerPage);

    // Paginated reading resources
    $: paginatedBooks = paginateArray(recommendedBooks, booksCurrentPage, itemsPerPage);
    $: booksPageCount = Math.ceil(recommendedBooks.length / itemsPerPage);

    $: paginatedArticles = paginateArray(recommendedArticles, articlesCurrentPage, itemsPerPage);
    $: articlesPageCount = Math.ceil(recommendedArticles.length / itemsPerPage);

    $: paginatedOther = paginateArray(recommendedOther, otherCurrentPage, itemsPerPage);
    $: otherPageCount = Math.ceil(recommendedOther.length / itemsPerPage);
</script>

<svelte:head>
    <title>Data Resources | Surviving the Singularity</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col items-center">

    <h1 class="text-4xl sm:text-5xl font-extrabold mb-4 text-gray-900 dark:text-gray-100 text-center">
        Explore Our <span class="text-blue-600 dark:text-blue-400">Data Resources</span>
    </h1>
    <p class="text-xl mb-12 text-gray-600 dark:text-gray-300 max-w-3xl text-center">
        Dive into our curated collection of AI and robotics datasets. These resources provide valuable insights into the rapidly evolving world of technology.
    </p>

    <!-- Recommended Reading Section -->
    <div class="w-full mb-12">
        <h2 class="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100 border-b pb-2 border-gray-200 dark:border-gray-700">
            Recommended Reading
        </h2>

        <Tabs style="underline">
            <TabItem open title="Books">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                    {#each paginatedBooks as book}
                        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all">
                            <h3 class="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{book.title}</h3>
                            <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">by {book.author}</p>
                            <p class="text-gray-700 dark:text-gray-300 mb-4">{book.description}</p>
                            <a href={book.link} target="_blank" rel="noopener noreferrer"
                               class="inline-flex items-center text-blue-600 dark:text-blue-400 hover:underline">
                                View Book
                                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                                </svg>
                            </a>
                        </div>
                    {/each}
                </div>
                {#if booksPageCount > 1}
                    <div class="flex justify-center mt-6">
                        <Pagination
                            totalItems={recommendedBooks.length}
                            pageSize={itemsPerPage}
                            currentPage={booksCurrentPage}
                            on:page={(e) => booksCurrentPage = e.detail}
                        />
                    </div>
                {/if}
            </TabItem>

            <TabItem title="Articles & Blog Posts">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                    {#each paginatedArticles as article}
                        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all">
                            <h3 class="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{article.title}</h3>
                            <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">by {article.author}</p>
                            <p class="text-gray-700 dark:text-gray-300 mb-4">{article.description}</p>
                            <a href={article.link} target="_blank" rel="noopener noreferrer"
                               class="inline-flex items-center text-blue-600 dark:text-blue-400 hover:underline">
                                Read Article
                                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                                </svg>
                            </a>
                        </div>
                    {/each}
                </div>
                {#if articlesPageCount > 1}
                    <div class="flex justify-center mt-6">
                        <Pagination
                            totalItems={recommendedArticles.length}
                            pageSize={itemsPerPage}
                            currentPage={articlesCurrentPage}
                            on:page={(e) => articlesCurrentPage = e.detail}
                        />
                    </div>
                {/if}
            </TabItem>

            <TabItem title="Other Resources">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                    {#each paginatedOther as resource}
                        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all">
                            <h3 class="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{resource.title}</h3>
                            <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">by {resource.author}</p>
                            <p class="text-gray-700 dark:text-gray-300 mb-4">{resource.description}</p>
                            <a href={resource.link} target="_blank" rel="noopener noreferrer"
                               class="inline-flex items-center text-blue-600 dark:text-blue-400 hover:underline">
                                Explore Resource
                                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                                </svg>
                            </a>
                        </div>
                    {/each}
                </div>
                {#if otherPageCount > 1}
                    <div class="flex justify-center mt-6">
                        <Pagination
                            totalItems={recommendedOther.length}
                            pageSize={itemsPerPage}
                            currentPage={otherCurrentPage}
                            on:page={(e) => otherCurrentPage = e.detail}
                        />
                    </div>
                {/if}
            </TabItem>
        </Tabs>
    </div>

    <!-- Recommended Videos Section -->
    <div class="w-full mb-12">
        <h2 class="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100 border-b pb-2 border-gray-200 dark:border-gray-700">
            Recommended Videos
        </h2>

        <div class="mb-6">
            <Tabs style="underline">
                {#each Object.keys(videoCategories) as category}
                    <TabItem
                        title={category}
                        active={selectedVideoCategory === category}
                        on:click={() => {
                            selectedVideoCategory = category;
                            videosCurrentPage = 1;
                        }}
                    />
                {/each}
            </Tabs>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {#each paginatedVideos as video}
                <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all">
                    <div class="aspect-w-16 aspect-h-9 mb-4">
                        <iframe
                            src={`https://www.youtube.com/embed/${video.youtubeId}`}
                            title={video.title}
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen
                            class="w-full h-full rounded"
                            loading="lazy"
                        ></iframe>
                    </div>
                    <h3 class="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{video.title}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">by {video.creator}</p>
                    <p class="text-gray-700 dark:text-gray-300">{video.description}</p>
                </div>
            {/each}
        </div>

        {#if videoPageCount > 1}
            <div class="flex justify-center mt-6">
                <Pagination
                    totalItems={currentVideos.length}
                    pageSize={itemsPerPage}
                    currentPage={videosCurrentPage}
                    on:page={(e) => videosCurrentPage = e.detail}
                />
            </div>
        {/if}
    </div>

    <!-- Data Warehouse Resources Section -->
    <div class="w-full">
        <h2 class="text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100 border-b pb-2 border-gray-200 dark:border-gray-700">
            Data Warehouse Resources
        </h2>
        <p class="text-lg mb-8 text-gray-600 dark:text-gray-300 max-w-4xl">
            Explore our curated collection of datasets, research materials, and specialized resources. Each card below represents a different category of data that you can browse, analyze, and use for your own research or understanding of AI and singularity topics.
        </p>

        <div class="mb-6">
            <Tabs style="underline">
                {#each Object.keys(dataCategories) as category}
                    <TabItem
                        title={category}
                        active={selectedDataCategory === category}
                        on:click={() => {
                            selectedDataCategory = category;
                            dataWarehouseCurrentPage = 1;
                        }}
                    />
                {/each}
            </Tabs>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 justify-items-center">
            {#each paginatedDataResources as resource}
                <Card class="hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 w-full">
                    <div class="flex flex-col h-full">
                        <div class="flex items-center mb-4">
                            <span class="icon-container mr-4 text-blue-600 dark:text-blue-400 p-3 bg-blue-100 dark:bg-blue-900 rounded-full">
                                {@html resource.icon.svg}
                            </span>
                            <h2 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{resource.title}</h2>
                        </div>
                        <p class="mb-6 text-gray-700 dark:text-gray-300 flex-grow">
                            {resource.description}
                        </p>
                        <div class="flex flex-wrap gap-2 mb-4">
                            {#each resource.tags as tag}
                                <Badge color="blue" class="text-xs font-semibold">{tag}</Badge>
                            {/each}
                        </div>
                        <div class="flex justify-between items-center text-sm text-gray-600 dark:text-gray-400 mb-6">
                            <span>Updated: {resource.lastEdited}</span>
                            <span class="font-medium">{resource.entries.toLocaleString()} entries</span>
                        </div>
                        <div class="mt-4 space-y-2">
                            <Button on:click={() => handleViewDataset(resource.link)} class="w-full bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600">
                                {resource.buttonText}
                                <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                                </svg>
                            </Button>
                        </div>
                    </div>
                </Card>
            {/each}
        </div>

        {#if dataPageCount > 1}
            <div class="flex justify-center mt-6">
                <Pagination
                    totalItems={currentDataResources.length}
                    pageSize={itemsPerPage}
                    currentPage={dataWarehouseCurrentPage}
                    on:page={(e) => dataWarehouseCurrentPage = e.detail}
                />
            </div>
        {/if}
    </div>
</div>

<style>
    .icon-container :global(svg) {
        @apply w-8 h-8;
    }

    /* Add aspect ratio support for YouTube embeds */
    .aspect-w-16 {
        position: relative;
        padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
    }

    .aspect-w-16 iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
</style>