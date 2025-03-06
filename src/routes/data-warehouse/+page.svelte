<script>
    import { dataResources } from '$lib/data/dataResources.js';
    import { Card, Button, Badge, Tooltip, Tabs, TabItem } from 'flowbite-svelte';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { IconData } from '$lib/assets/Icons.svelte';

    function handleViewDataset(link) {
        goto(link);
    }

    // Add state for reading tab selection
    let selectedReadingTab = "Books";

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
        },
        {
            title: "Power and Prediction: The Disruptive Economics of Artificial Intelligence",
            author: "Ajay Agrawal, Joshua Gans & Avi Goldfarb",
            description: "A 2023 exploration of how AI is reshaping decision-making and business models across industries.",
            link: "https://www.amazon.com/Power-Prediction-Disruptive-Economics-Intelligence/dp/1647824389"
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
            link: "https://www.alignment.org/"
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
        },
        {
            title: "Frontier AI Regulation: Managing Emerging Risks to Public Safety",
            author: "Anthropic, Google DeepMind, Microsoft, OpenAI",
            description: "A 2023 joint publication from leading AI labs on the responsible development of frontier AI systems.",
            link: "https://cdn.openai.com/papers/frontier-ai-regulation.pdf"
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
            link: "https://futureoflife.org/project/future-of-life-institute-podcast/"
        },
        {
            title: "Stampy's Wiki",
            author: "AI Safety Community",
            description: "A collaboratively edited knowledge base for AI safety concepts.",
            link: "https://stampy.ai/"
        },
        {
            title: "AI Governance and Risk Course",
            author: "Center for AI Safety",
            description: "A free online course covering AI governance, risk assessment, and safety frameworks.",
            link: "https://www.safe.ai/ai-governance-and-risk"
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
                title: "Can we build AI without losing control over it?",
                creator: "Sam Harris",
                description: "TED talk on the risks of advanced AI and why alignment is crucial for humanity's future.",
                youtubeId: "8nt3edWLgIg"
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
                youtubeId: "eD5GlCIS0sA"
            },
            {
                title: "The Future of Intelligence: Human, Machine, and Extraterrestrial",
                creator: "Oxford University",
                description: "A 2023 lecture by Stuart Russell on the future of intelligence and AI safety considerations.",
                youtubeId: "3TYT1QfdfsM"
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
            },
            {
                title: "Large Language Models and the Future of AI",
                creator: "Andrej Karpathy",
                description: "A 2023 comprehensive explanation of how large language models work and their implications.",
                youtubeId: "zjkBMFhNj_g"
            }
        ]
    };

    // Flatten videos for pagination
    let selectedVideoCategory = Object.keys(videoCategories)[0];
    $: currentVideos = videoCategories[selectedVideoCategory] || [];

    // Add new resources for the data warehouse
    const additionalDataResources = [
        {
            title: "AI Alignment Landscape",
            description: "A 2023 comprehensive map of the AI alignment research landscape, categorizing different approaches and methodologies.",
            lastEdited: "Dec 2023",
            icon: IconData,
            link: "https://alignmentresearchcenter.org/alignment-landscape/",
            entries: 50,
            buttonText: "View Resource",
            tags: ["Research", "Alignment"]
        },
        {
            title: "State of AI Report 2023",
            description: "Annual report covering the most important developments in AI research, industry, politics, and safety.",
            lastEdited: "Oct 2023",
            icon: IconData,
            link: "https://www.stateof.ai/",
            entries: 1,
            buttonText: "View Report",
            tags: ["Industry", "Companies", "Research"]
        },
        {
            title: "AI Safety Fundamentals Course Materials",
            description: "Comprehensive course materials on AI safety, including readings, videos, and exercises.",
            lastEdited: "Jan 2024",
            icon: IconData,
            link: "https://aisafetyfundamentals.com/",
            entries: 25,
            buttonText: "Access Course",
            tags: ["PDFs", "Videos", "Education"]
        }
    ];

    // Combine original and additional resources
    const allDataResources = [...dataResources, ...additionalDataResources];

    // Group data resources by category - fix the overlapping categories
    const dataCategories = {
        "Research & Analysis": allDataResources.filter(resource =>
            (resource.tags?.includes("Research") &&
            !resource.tags?.includes("PDFs") &&
            !resource.tags?.includes("Videos")) ||
            resource.title === "AI Alignment Landscape"
        ),
        "Industry & Applications": allDataResources.filter(resource =>
            resource.tags?.includes("Industry") ||
            resource.tags?.includes("Robotics") ||
            resource.tags?.includes("Companies") ||
            resource.title === "State of AI Report 2023"
        ),
        "Media & Resources": allDataResources.filter(resource =>
            resource.tags?.includes("PDFs") ||
            resource.tags?.includes("Videos") ||
            resource.title === "AI Safety Fundamentals Course Materials"
        )
    };

    let selectedDataCategory = Object.keys(dataCategories)[0];
    $: currentDataResources = dataCategories[selectedDataCategory] || [];
</script>

<svelte:head>
    <title>Data Resources | Surviving the Singularity</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold mb-3 sm:mb-4 text-gray-900 dark:text-gray-100 text-center">
        Explore Our <span class="text-blue-600 dark:text-blue-400">Data Resources</span>
    </h1>
    <p class="text-lg sm:text-xl mb-8 sm:mb-12 text-gray-600 dark:text-gray-300 max-w-3xl mx-auto text-center">
        Dive into our curated collection of AI and robotics datasets. These resources provide valuable insights into the rapidly evolving world of technology.
    </p>

    <!-- Recommended Reading Section -->
    <div class="mb-10">
        <h2 class="text-2xl sm:text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100 border-b pb-2 border-gray-200 dark:border-gray-700">
            Recommended Reading
        </h2>

        <!-- Tab navigation -->
        <div class="flex justify-center mb-6 border-b border-gray-200 dark:border-gray-700">
            <button
                class="px-4 py-2 font-medium {selectedReadingTab === 'Books' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}"
                on:click={() => selectedReadingTab = 'Books'}
            >
                Books
            </button>
            <button
                class="px-4 py-2 font-medium {selectedReadingTab === 'Articles' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}"
                on:click={() => selectedReadingTab = 'Articles'}
            >
                Articles & Blog Posts
            </button>
            <button
                class="px-4 py-2 font-medium {selectedReadingTab === 'Other' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}"
                on:click={() => selectedReadingTab = 'Other'}
            >
                Other Resources
            </button>
        </div>

        <!-- Books content -->
        {#if selectedReadingTab === 'Books'}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each recommendedBooks as book}
                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
                    <h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white line-clamp-2">{book.title}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">by {book.author}</p>
                    <p class="text-sm text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">{book.description}</p>
                    <div class="flex justify-center mb-10">
                        <a href={book.link} class="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg text-center">
                            Read a Sample
                        </a>
                    </div>
                </div>
            {/each}
        </div>
        {/if}

        <!-- Articles content -->
        {#if selectedReadingTab === 'Articles'}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each recommendedArticles as article}
                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
                    <h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white line-clamp-2">{article.title}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">by {article.author}</p>
                    <p class="text-sm text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">{article.description}</p>
                    <a href={article.link} target="_blank" rel="noopener noreferrer"
                       class="inline-flex items-center text-blue-600 dark:text-blue-400 hover:underline text-sm">
                        View Article
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                        </svg>
                    </a>
                </div>
            {/each}
        </div>
        {/if}

        <!-- Other resources content -->
        {#if selectedReadingTab === 'Other'}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each recommendedOther as resource}
                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
                    <h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white line-clamp-2">{resource.title}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">by {resource.author}</p>
                    <p class="text-sm text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">{resource.description}</p>
                    <a href={resource.link} target="_blank" rel="noopener noreferrer"
                       class="inline-flex items-center text-blue-600 dark:text-blue-400 hover:underline text-sm">
                        View Resource
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                        </svg>
                    </a>
                </div>
            {/each}
        </div>
        {/if}
    </div>

    <!-- Recommended Videos Section -->
    <div class="mb-10">
        <h2 class="text-2xl sm:text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100 border-b pb-2 border-gray-200 dark:border-gray-700">
            Recommended Videos
        </h2>

        <!-- Tab navigation -->
        <div class="flex justify-center mb-6 border-b border-gray-200 dark:border-gray-700">
            {#each Object.keys(videoCategories) as category, i}
                <button
                    class="px-4 py-2 font-medium {selectedVideoCategory === category ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}"
                    on:click={() => selectedVideoCategory = category}
                >
                    {category}
                </button>
            {/each}
        </div>

        <!-- Video content -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each videoCategories[selectedVideoCategory] as video}
                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
                    <div class="aspect-w-16 aspect-h-9 mb-3">
                        <!-- Link directly to YouTube instead of embedding -->
                        <a
                            href={`https://www.youtube.com/watch?v=${video.youtubeId}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            class="video-thumbnail relative w-full h-full rounded bg-gray-200 dark:bg-gray-700 flex items-center justify-center"
                            aria-label="Watch video on YouTube: {video.title}"
                        >
                            <!-- YouTube thumbnail -->
                            <img
                                src={`https://img.youtube.com/vi/${video.youtubeId}/mqdefault.jpg`}
                                alt={video.title}
                                class="w-full h-full object-cover rounded"
                                loading="lazy"
                            />
                            <!-- Play button overlay -->
                            <div class="absolute inset-0 flex items-center justify-center">
                                <div class="bg-red-600 rounded-full p-3 text-white">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                            </div>
                        </a>
                    </div>
                    <h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white line-clamp-2">{video.title}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">by {video.creator}</p>
                    <p class="text-sm text-gray-700 dark:text-gray-300 line-clamp-3">{video.description}</p>
                </div>
            {/each}
        </div>
    </div>

    <!-- Data Warehouse Resources Section -->
    <div>
        <h2 class="text-2xl sm:text-3xl font-bold mb-4 text-gray-900 dark:text-gray-100 border-b pb-2 border-gray-200 dark:border-gray-700">
            Data Warehouse Resources
        </h2>
        <p class="text-base sm:text-lg mb-6 text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Explore our curated collection of datasets, research materials, and specialized resources. Each card below represents a different category of data that you can browse, analyze, and use for your own research or understanding of AI and singularity topics.
        </p>

        <!-- Tab navigation -->
        <div class="flex justify-center mb-6 border-b border-gray-200 dark:border-gray-700">
            {#each Object.keys(dataCategories) as category, i}
                <button
                    class="px-4 py-2 font-medium {selectedDataCategory === category ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}"
                    on:click={() => selectedDataCategory = category}
                >
                    {category}
                </button>
            {/each}
        </div>

        <!-- Data resources content -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each dataCategories[selectedDataCategory] as resource}
                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
                    <div class="flex items-center mb-3">
                        <span class="icon-container mr-3 text-blue-600 dark:text-blue-400 p-2 bg-blue-100 dark:bg-blue-900 rounded-full">
                            {@html resource.icon.svg}
                        </span>
                        <h3 class="text-xl font-bold tracking-tight text-gray-900 dark:text-white line-clamp-2">{resource.title}</h3>
                    </div>
                    <p class="mb-4 text-sm text-gray-700 dark:text-gray-300 line-clamp-3">
                        {resource.description}
                    </p>
                    <div class="flex flex-wrap gap-1 mb-3">
                        {#each resource.tags as tag}
                            <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-0.5 rounded dark:bg-blue-900 dark:text-blue-300">{tag}</span>
                        {/each}
                    </div>
                    <div class="flex justify-between items-center text-xs text-gray-600 dark:text-gray-400 mb-4">
                        <span>Updated: {resource.lastEdited}</span>
                        <span class="font-medium">{resource.entries.toLocaleString()} entries</span>
                    </div>
                    <button
                        on:click={() => handleViewDataset(resource.link)}
                        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded flex items-center justify-center"
                    >
                        {resource.buttonText}
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                        </svg>
                    </button>
                </div>
            {/each}
        </div>
    </div>
</div>

<style>
    .icon-container :global(svg) {
        @apply w-6 h-6;
    }

    /* Add aspect ratio support for YouTube embeds */
    .aspect-w-16 {
        position: relative;
        padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
    }

    /* This style applies to both iframes and buttons within the aspect container */
    .aspect-w-16 > * {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }

    /* Text truncation for long content */
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .line-clamp-3 {
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
</style>