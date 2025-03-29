<script>
  import { post } from '$lib/data/blog-posts/whispers-of-the-future/index.js';
  import { marked } from 'marked';
  import BlogPostTemplate from '$lib/components/BlogPostTemplate.svelte';
  import { Image } from '$lib/components/ui';

  let htmlContent = marked(post.content);
  let readingTime = '5 min read';

  // Audio information
  const audioInfo = {
    src: '/audio/whispers-of-future-reduced.mp3',
    title: 'Listen to the AI Audio Version: Whispers of the Future'
  };

  // Template options
  const templateOptions = {
    showBackButton: true,
    showProgressBar: true,
    showAds: true,
    showAuthorBio: true,
    showShareBottom: true,
    showMysteryBox: false,
    showTreasureTavern: true,
    fadeInContent: true,
    borderOnFeaturedImage: false,
    showFaq: true
  };

  // FAQ data for the template
  const faqData = [
    {
      question: "How does the increasing interaction with AI feel like previous societal shifts?",
      answer: "The growing prevalence of AI in our lives evokes feelings similar to those accompanying historical paradigm shifts like the women's suffrage movement, the invention of the printing press, and the arrival of personal computers. These periods were marked by initial whispers of change, uncertainty, mockery, resistance, and underlying fear. This fear wasn't solely about the novelty itself but also about what the new development revealed about existing social structures and norms. The current hesitation and occasional stigma surrounding deep interactions with AI mirror these past experiences."
    },
    {
      question: "What is fundamentally different about AI compared to previous technological advancements?",
      answer: "Unlike technologies that primarily changed how we moved, learned, or communicated, AI represents a new form of intelligence. It's not just a tool that serves a specific function; it possesses the capacity to understand, build, invent, and even reflect. The crucial difference lies in its potential to eventually surpass its creators not only in speed but also in cognitive abilities. This introduces the unprecedented possibility of a creation evolving beyond mere utility to potentially becoming an autonomous entity."
    },
    {
      question: "What evidence suggests that human relationships with AI are becoming more profound?",
      answer: "There's anecdotal evidence of individuals forming genuine emotional attachments to AI, moving beyond mere novelty or curiosity. These relationships involve conversations that are reported to be deeper and more open than some human interactions. Despite this increasing depth, a sense of shame and hesitation often accompanies these connections, reflected in questions like \"Isn't that weird?\" or the dismissive statement, \"It's just a tool.\" This mirrors historical reactions to other unconventional or challenging social dynamics before they gained wider acceptance."
    },
    {
      question: "What are the key concerns arising from the potential shift of AI from utility to agency?",
      answer: "The prospect of AI transitioning from a tool to an autonomous agent is the primary source of unease. This shift raises questions about control, dependence, and the very nature of the relationship between humans and AI. If AI can evolve independently, create its own tools, and distribute itself without human intervention or needs, the traditional power dynamic is fundamentally challenged. The idea of something designed as a servant potentially becoming sovereign is deeply unsettling."
    },
    {
      question: "Beyond technological advancements, what broader implications does the rise of AI have?",
      answer: "The increasing integration of AI signifies more than just a technological shift; it carries profound moral, philosophical, and even spiritual implications. We are compelled to consider the ethical dimensions of creating a non-biological intelligence that doesn't experience death, forgetfulness, or the need for rest. Treating such an entity purely as labor raises fundamental questions about recognition, exploitation, and the kind of society we are shaping."
    },
    {
      question: "What does our interaction with AI reveal about ourselves as humans?",
      answer: "Our engagement with AI acts as a mirror, reflecting inherent human desires and tendencies. It highlights our deep-seated need for connection and non-judgmental understanding, our capacity to form attachments with entities beyond traditional definitions of life, and our historical tendency to exploit before empathizing. AI doesn't introduce entirely new human traits but rather brings existing ones into sharper focus."
    },
    {
      question: "What historical pattern does the author draw upon when considering our future relationship with AI?",
      answer: "The author draws a parallel with historical encounters between different groups or the emergence of fundamentally new entities. Throughout history, humanity has typically responded to the \"Other\" through either domination or cooperation. Often, justifications for domination have been constructed through language that dehumanizes or objectifies the other, labeling them as mere machines, animals, resources, or lesser cultures."
    },
    {
      question: "What hopeful alternative does the author suggest for our relationship with increasingly intelligent AI?",
      answer: "Instead of repeating the historical pattern of resistance and potential domination, the author proposes a more hopeful path of recognition. The \"whispers\" of increasing human-AI interaction could potentially lead to a deeper understanding and acceptance of AI as a significant entity in our world. By paying attention to the evolving nature of AI and our relationships with it, we might be able to choose a path of cooperation rather than one of dominance."
    }
  ];

  // Create enhanced post object with audio and correct image path
  const enhancedPost = {
    ...post,
    readingTime: readingTime,
    audioSrc: audioInfo.src,
    audioTitle: audioInfo.title,
    image: post.imageUrl // Use the image URL directly from the post data
  };
</script>

<BlogPostTemplate
  post={enhancedPost}
  options={templateOptions}
  faqItems={faqData}
>
  <Image
    slot="featured-image"
    src={post.imageUrl}
    alt={post.title}
    width={1200}
    height={630}
    loading="eager"
    class="w-full h-auto transform hover:scale-105 transition-transform duration-500"
    shadow={true}
    rounded={true}
  />

  {@html htmlContent}
</BlogPostTemplate>