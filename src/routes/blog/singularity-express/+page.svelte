<!-- src/routes/blog/singularity-express/+page.svelte -->
<script>
  import Spacer from '$lib/components/Spacer.svelte';
  import { onMount } from 'svelte';

  let navbarHeight = 0;

  onMount(() => {
    navbarHeight = document.querySelector('nav').offsetHeight;
  });

  function handleBackBook() {
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
  }

  function handleJoinSkool() {
    alert("The Skool Community is launching next Friday 8/9 - please stay tuned.");
  }

  function handleGetGuide() {
    window.open('https://tavolazzi.gumroad.com/l/singularitychecklist', '_blank');
  }

  function handleReadSample() {
    window.location.href = 'https://survivingthesingularity.com/sample';
  }

  const post = {
    title: "The Singularity Express Arrives at the Station",
    date: "2024-08-08",
    author: "Christopher Tavolazzi",
    content: `<h1>Choo Choo, Motherfuckers.</h1>

<p>The Singularity Express just pulled into the station, and we're in for one hell of a ride.</p>

<p>Some Twitter rando named <a href="https://x.com/iruletheworldmo" target="_blank" rel="noopener noreferrer">@iruletheworldmo</a> just lit up the internet claiming we've hit "Level 2" AI. No, that's not a new Call of Duty achievement. We're talking about the kind of AI that makes ChatGPT look like a speak-and-spell toy from the '80s. And why should you care? Because this isn't just another tech hype train – it's the fucking Singularity Express, and we're all on board whether we like it or not.</p>

<p>Let's break this down for those of you who haven't been obsessively charting the "robots take over the world" timeline:</p>

<p><ul>
  <li><strong>Levels to AGI</strong></li>
  <li>Level 1: Conversational AI (ChatGPT and its chatty cousins)</li>
  <li>Level 2: Reasoning AI (where shit just got real)</li>
  <li>Level 3: Autonomous AI (I, Robot, but probably less Will Smith)</li>
  <li>Level 4: Innovative AI (when machines start filing patents and we're all unemployed)</li>
  <li>Level 5: Organizational AI (Skynet, but with better PR)</li>
</ul></p>

<h3>Why This Matters:</h3>

<p>Each level is a quantum leap in AI capability, and we just jumped from "cute party trick" to "oh shit, it can think."</p>

<p>We've been chilling at Level 1 for a minute, with AI that can talk your ear off but has the reasoning skills of a pet rock. Ask it something truly novel, and you'll get either a digital shrug or a story so creative it belongs in a Tolkien novel.</p>

<p>But Level 2? That's where things get spicy. We're talking about AI that can reason, that can look at a problem it's never seen before and go, "Hold my silicon, I got this."</p>

<p><span class="bold-before-colon">Real-World Impact</span>: Google's AlphaProof and AlphaGeometry just crashed the International Mathematical Olympiad and snagged a silver medal. That's not just impressive; it's the kind of thing that makes human mathematicians consider a career in interpretive dance.</p>

<p><span class="survival-tip">Survival Tip #1</span>: Start learning interpretive dance. It might be the only job left.</p>

<p>Why should you give a flying flip? Because math isn't just about torturing high school students. It's the language the universe speaks when it's not drunk. An AI that can do math like this can potentially revolutionize every single field of science faster than you can say "technological unemployment."</p>

<p><span class="bold-before-colon">From Lab to Life</span>: Imagine cancer researchers using AI to crunch through millions of potential drug combinations overnight. Or climate scientists modeling centuries of weather patterns in minutes. We're not just accelerating progress; we're strapping a rocket to it and aiming for the stars.</p>

<p>But wait, there's more! Picture having a genius researcher working 24/7, never needing a Red Bull, never making the same mistake twice, and constantly leveling up like it's in some cosmic RPG. Now imagine that researcher can instantly share its "Eureka!" moments with every other AI on the planet. Yeah, it's that bonkers.</p>

<p><span class="survival-tip">Survival Tip #2</span>: Invest in companies making comfy chairs. We're all going to need a place to sit and watch the AI do... well, everything.</p>

<p>The economics of this are wild enough to make even crypto bros dizzy. Instead of spending years and millions on human researchers (who, let's face it, spend half their time arguing over whose turn it is to clean the lab microwave), we could have AI churning out Nobel-worthy insights faster than you can say "Would you like fries with that?"</p>

<h3>What's Next?</h3
<p>Hold onto your butts, because the jump from Level 2 to Level 3 - autonomous AI agents - could happen faster than you can update your LinkedIn profile to "AI Overlord Appeasement Specialist." Once these silicon savants can reason and have novel insights, letting them loose to act on those insights is just a small step for AI, one giant "Oh shit" moment for mankind.</p>

<p>We're entering a world where one AI's lightbulb moment instantly becomes every AI's new party trick. It's like if every scientist in history could instantaneously know and build upon each other's work, but without the messy business of peer review or reproducibility.</p>

<p><span class="survival-tip">Survival Tip #3</span>: Start a journal. Future AI historians will want to know what it was like to live through the last days of human intellectual superiority.</p>

<p>Are we anywhere near the limits of what's possible? Not even close, baby. But we're about to find out, and the ride's going to be wilder than your uncle's dance moves at a wedding after he's had too much of the open bar.</p>

<p>The singularity - that sci-fi wet dream where AI surpasses human intelligence and we all become pets or paperclips - has been the boogeyman of tech philosophers for decades. But with these developments, we're not just approaching the singularity - we're strapped to the front of the rocket sled headed straight for it, and someone just lit the fuse.</p>

<p>But let's get real for a second. What does this actually mean for you, me, and the guy who still can't figure out how to unmute himself on Zoom calls?</p>

<h3>Level 3: Autonomous AI - The "I Can't Believe It's Not Human" Stage</h3>

<p><strong>Picture this:</strong> You wake up, and your AI assistant has already rescheduled your dentist appointment because it noticed a conflict with an important meeting. It's also ordered your groceries based on your health goals and what's actually in your fridge (yes, it knows you ate that last slice of pizza at 2 AM).</p>

<p>Your car drives you to work, automatically rerouting to avoid an accident it knew about before the traffic apps did. At the office, an AI has already drafted reports, scheduled meetings, and even started negotiations with clients in different time zones.</p>

<p><span class="survival-tip">Survival Tip #4</span>: Learn to code, or at least learn to speak 'AI'. Your new boss might not understand human laziness.</p>

<h3>Level 4: Innovative AI - The "Well, We Had a Good Run" Stage</h3>

<p>You're a scientist working on climate change. You go to sleep, and overnight, the AI has not only processed all the climate data from the past century but has also designed and run millions of simulations. By morning, it's proposing a new carbon capture technology that no human had thought of before.</p>

<p>Or you're a novelist with writer's block. The AI doesn't just suggest plot points; it creates entire new genres of literature, complete with fully realized worlds and characters so compelling they make George R.R. Martin look like he's writing shopping lists.</p>

<p><span class="survival-tip">Survival Tip #5</span>: Creativity is no longer just for humans. Find the intersection of AI innovation and human intuition, and set up shop there.</p>

<h3>Level 5: Organizational AI - The "Is This The Matrix?" Stage</h3>

<p>Imagine a city where traffic lights, public transport, energy grids, and emergency services are all controlled by a single AI. It predicts and prevents crimes before they happen, optimizes energy use down to the individual lightbulb, and can evacuate an entire region in the face of a natural disaster with zero casualties.</p>

<p>Now scale that up to a global level. An AI managing world resources, predicting and preventing conflicts, solving global warming, and maybe even figuring out how to make pineapple on pizza universally acceptable (okay, maybe that's too far-fetched).</p>

<p><span class="survival-tip">Survival Tip #6</span>: Become the bridge between AI systems and human needs. We'll need translators who can speak both silicon and soul.</p>

<p>Here's the kicker: the jump between these levels? It might happen so fast it'll make your head spin. We're not talking decades. We might be talking years. Maybe months. Hell, by the time you finish reading this, we might have jumped another level.</p>

<p>This isn't sci-fi anymore, folks. This is the world we're careening towards at breakneck speed. The Singularity Express isn't just pulling into the station; it's barreling down the tracks with no brakes.</p>

<p>So, what's a mere mortal to do? Start by upgrading your survival kit from canned goods and bottled water to a crash course in AI ethics and a comfortable chair to watch the show from. Because ready or not, the future's coming, and it's coming in hot.</p>

<p><span class="survival-tip">Final Survival Tip</span>: Embrace the chaos. Learn. Adapt. And maybe, just maybe, we can evolve alongside our new silicon overlords.</p>

<p>Welcome to the singularity, folks. The express train is here, and it waits for no one. All aboard, and maybe bring a change of pants. It's going to be one hell of a ride.</p>

<p><strong>Remember:</strong> In the race between human and artificial intelligence, if you can't beat 'em... well, let's hope we can join 'em. Or at least convince them to keep us around as vintage collectibles.</p>

<p>Now, if you'll excuse me, I need to patent my idea for "AI Overlord Appeasement" before some silicon smartass beats me to it.</p>`
  };
</script>

<div class="main-content" style="padding-top: {navbarHeight}px">
  <Spacer height=".5rem">
    <span class="spacer-text">Surviving the Singularity</span>
  </Spacer>

  <article class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-4">{post.title}</h1>
    <p class="text-gray-600 dark:text-gray-400 italic mb-6">{post.date} - {post.author}</p>
    <button on:click={() => window.location.href = '/blog'} class="mb-4 px-4 py-2 bg-white dark:bg-gray-800 text-black dark:text-white rounded hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors duration-300">← Back to Blog List</button>
    <img alt="Default Blog Image" src="https://cdn.midjourney.com/2cfb73bc-4072-40fa-aa86-8cf4f842b428/0_2.png" class="w-full max-w-2xl h-auto mb-6 rounded" />
    <div class="content">
      {@html post.content}
    </div>
  </article>

  <div class="button-container">
    <button class="big-button" on:click={handleBackBook}>Back the Book on Kickstarter</button>
    <button class="big-button" on:click={handleReadSample}>Read a Sample</button>
    <button class="big-button" on:click={handleGetGuide}>Get the FREE Guide</button>
    <button class="big-button" on:click={handleJoinSkool}>Join the Skool Community</button>
  </div>
</div>

<style>
  :global(body) {
    background-color: #ffffff;
    color: #000000;
  }

  :global(body.dark) {
    background-color: #1a202c;
    color: #ffffff;
  }

  .main-content {
    transition: padding-top 0.3s ease-in-out;
  }

  :global(body.dark) .content :global(*) {
    color: #ffffff !important;
  }

  :global(body.dark) .content :global(a) {
    color: #63b3ed !important;
  }

  :global(body.dark) .content :global(.survival-tip) {
    color: #68d391 !important;
  }

  :global(body.dark) .content :global(h1) {
    color: #ffffff !important;
  }

  .spacer-text {
    font-size: 1.5rem;
    font-weight: bold;
    color: #000000;
    background-color: #ffffff;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  :global(body.dark) .spacer-text {
    color: #ffffff;
    background-color: #2d3748;
  }

  .content :global(h1) {
    font-size: 2em;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #333;
  }

  .content :global(p) {
    margin-bottom: 1.5em;
    line-height: 1.6;
    font-size: 1em;
  }

  .content :global(p:last-child) {
    margin-bottom: 0;
  }

  .content :global(ul) {
    margin-top: 1em;
    margin-bottom: 1em;
    padding-left: 2em;
  }

  .content :global(li) {
    margin-bottom: 0.5em;
  }

  .content :global(h2) {
    font-size: 1.5em;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #333;
  }

  .content :global(h3) {
    font-size: 1.25em;
    font-weight: bold;
    margin-top: 1.25em;
    margin-bottom: 0.5em;
    color: #444;
  }

  .content :global(a) {
    color: blue;
    text-decoration: underline;
  }

  .content :global(a:visited) {
    color: purple;
  }

  .content :global(.bold-before-colon) {
    font-weight: bold;
  }

  .content :global(.survival-tip) {
    font-weight: bold;
    font-style: italic;
  }

  .button-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-top: 2rem;
    max-width: 2xl;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .big-button {
    font-weight: bold;
    font-size: 1.25rem;
    background-color: #f8f9fa;
    border: 2px solid #000000;
    border-radius: 4px;
    padding: 1rem 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
    text-align: center;
  }

  .big-button:hover {
    background-color: #000000;
    color: #ffffff;
  }

  :global(body.dark) .big-button {
    background-color: #2d3748;
    border-color: #ffffff;
    color: #ffffff;
  }

  :global(body.dark) .big-button:hover {
    background-color: #ffffff;
    color: #2d3748;
  }

  @media (max-width: 640px) {
    h1 {
      font-size: 1.875rem;
    }

    .button-container {
      grid-template-columns: 1fr;
    }

    .spacer-text {
      font-size: 1.25rem;
    }
  }
</style>
