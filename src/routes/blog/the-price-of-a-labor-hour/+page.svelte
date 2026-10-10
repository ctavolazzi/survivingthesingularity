<script>
  import SocialShare from '$lib/components/SocialShare.svelte';
  import Spacer from '$lib/components/Spacer.svelte';
  import NewsletterSignup from '$lib/components/NewsletterSignup.svelte';

  const post = {
    title: 'The Price of a Labor-Hour: Blue Jeans, Jevons, and the Conquistadors of Work',
    date: '2026-09-25',
    author: 'Christopher Tavolazzi',
    readingTime: '14 min read',
    description: "There is a number that tells you how close a machine is to taking your job. Here's what it is, what it did to spinners, weavers, farmers and horses, why there are more T-shirts on Earth than ever, and why the arrival of AI looks less like a factory upgrade and more like 1519.",
    image: '/images/surviving_the_singularity_cover_1200.png'
  };
</script>

<svelte:head>
  <title>{post.title} | Surviving the Singularity</title>
  <meta name="description" content={post.description} />
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content={post.description} />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
</svelte:head>

<div class="blog-post">
  <article class="post-inner">
    <header class="post-header">
      <a href="/blog" class="back-link">
        <span aria-hidden="true">←</span> Back to Blog
      </a>
      <h1 class="post-title">{post.title}</h1>
      <div class="post-meta">
        <span>{post.date}</span>
        <span class="sep" aria-hidden="true">·</span>
        <span>{post.readingTime}</span>
        <span class="sep" aria-hidden="true">·</span>
        <span>By {post.author}</span>
      </div>
      <SocialShare title={post.title} description={post.description} image={post.image} />
    </header>

    <div class="content">

      <p class="lead">
        Every job on Earth has a price tag attached to one hour of it. The moment a machine can do that hour for less, the clock starts ticking. That's not a prediction. It's the most reliable pattern in economic history, and it's worth knowing the name of the number that runs it.
      </p>

      <nav class="toc" aria-label="In this post">
        <p class="toc-label">In this post</p>
        <ol>
          <li><a href="#definition">The term: Cost per Labor-Hour Equivalent</a></li>
          <li><a href="#history">What that number did to every worker it touched</a></li>
          <li><a href="#fabric">Reality check: Jevons Paradox and your blue jeans</a></li>
          <li><a href="#conquest">1519: the conquistador scenario</a></li>
          <li><a href="#paths">Three paths, and a secret fourth</a></li>
          <li><a href="#next">Two futures, one certainty</a></li>
        </ol>
      </nav>

      <!-- ─────────────────────────────── 1 ─────────────────────────────── -->

      <h2 id="definition">1. The Term: Cost per Labor-Hour Equivalent</h2>

      <p>
        Economists already have the building blocks. A <strong>labor-hour</strong> (also called a man-hour or person-hour) is the standard unit of labor: one person working for one hour. The <strong>wage rate</strong> is the price of that unit. In <em>The General Theory</em> (1936), John Maynard Keynes formalized this as the <strong>wage-unit</strong>: the money wage of one hour of ordinary labor. He used it as a ruler to measure an economy in real terms, stripped of inflation.
      </p>

      <p>
        The statistic governments actually track is <strong>Unit Labor Cost (ULC)</strong>, published by the U.S. Bureau of Labor Statistics and the OECD:
      </p>

      <div class="formula">
        <p class="formula-line"><span class="formula-name">Unit Labor Cost</span> = total labor compensation ÷ units of output</p>
        <p class="formula-line formula-sub">= (compensation per hour) ÷ (output per hour)</p>
      </div>

      <p>
        ULC connects what you're paid to how much you produce. If wages rise 5% and productivity rises 5%, ULC doesn't move. If productivity doubles and wages don't, the labor inside every product just got half as expensive.
      </p>

      <p>
        None of these measures were built for a world where the worker might not be a person. So here is the term this site will use:
      </p>

      <div class="definition">
        <p class="definition-term">Cost per Labor-Hour Equivalent <span class="definition-abbr">(CLHE)</span></p>
        <p class="definition-body">
          The all-in cost of getting one human-hour's worth of useful output from any source: a person, a machine, an AI model, or a mix. For a person, it's the fully loaded wage (pay plus taxes, benefits and overhead) divided by output per hour. For a machine, it's hardware amortized over its working life, plus energy, maintenance, software and the human time spent supervising it, divided by the same output.
        </p>
        <p class="definition-rule">
          When a machine's CLHE falls below a human's for a given task, that task begins to move. Not overnight, and not completely. But it moves.
        </p>
      </div>

      <p>
        CLHE is useful because it puts a weaver and a power loom, a farmhand and a combine, a paralegal and a language model on the same scale. You don't need to believe any story about "the robots are coming." You just need to watch one number per task.
      </p>

      <!-- ─────────────────────────────── 2 ─────────────────────────────── -->

      <h2 id="history">2. What That Number Did to Every Worker It Touched</h2>

      <p>
        We have good historical data on how many human-hours it took to produce the same output before and after a technology arrived. Read these as CLHE collapses.
      </p>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th scope="col">Task</th>
              <th scope="col">Before</th>
              <th scope="col">After</th>
              <th scope="col">What happened to the workers</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Spinning 100 lb of cotton into yarn</td>
              <td>~50,000 hours by hand (18th-century Indian spinners)</td>
              <td>~300 hours on power-assisted mules by 1795; ~135 by 1825</td>
              <td>Home spinning, mostly done by women, vanished as paid work within a generation</td>
            </tr>
            <tr>
              <td>Weaving cloth in Britain</td>
              <td>Handloom weavers numbered roughly a quarter million in the 1820s</td>
              <td>Power looms spread through the 1830s and 1840s</td>
              <td>Handloom wages collapsed; the trade was a remnant by mid-century</td>
            </tr>
            <tr>
              <td>Growing 100 bushels of U.S. wheat</td>
              <td>250 to 300 hours (1830, walking plow, hand sowing, sickle)</td>
              <td>40 to 50 hours by 1890; about 3 by the late 1980s</td>
              <td>Farm share of U.S. workers fell from over half to under 2%</td>
            </tr>
            <tr>
              <td>Moving goods and people</td>
              <td>Horses and mules: about 26 million on U.S. farms at the 1915 peak</td>
              <td>Trucks, tractors and cars</td>
              <td>Down to about 3 million by 1960. Horses didn't retrain.</td>
            </tr>
            <tr>
              <td>Connecting a phone call</td>
              <td>A human operator for every call</td>
              <td>Mechanical, then electronic, switching</td>
              <td>AT&amp;T automated over half its network from 1920 to 1940; where a city switched to dial, jobs for young women as operators fell 50 to 80%</td>
            </tr>
            <tr>
              <td>Doing arithmetic</td>
              <td>"Computer" was a job title held by people, often rooms full of them</td>
              <td>Electronic computers</td>
              <td>The job title was transferred to the machine</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="table-note">
        Sources: spinning hours from Catling's operative-hours estimates; wheat hours from the USDA's <em>Growing a Nation</em> farm technology timeline; operator figures from Feigenbaum and Gross (NBER Working Paper 28061); horse counts from USDA census data. Figures are rounded.
      </p>

      <p>Three patterns repeat in every row.</p>

      <ul>
        <li><strong>The drop is not 20% or 50%. It's 90% to 99%.</strong> Once a machine gets a foothold on a task, its CLHE keeps falling for decades while human CLHE stays roughly flat, because a human hour is a human hour.</li>
        <li><strong>The people displaced are rarely the people who benefit.</strong> The handloom weavers of the 1830s did not become factory owners. Many of them, and their children, lived through decades of real poverty before the gains reached ordinary households.</li>
        <li><strong>Total employment recovered anyway.</strong> Britain, the U.S. and every industrialized country ended up with more jobs, not fewer. The work went somewhere new. That "somewhere new" is the entire subject of the next section.</li>
      </ul>

      <p>
        What's different now is the width of the front. Every row above is one task, or one industry. AI and general-purpose robots are attacking CLHE on thousands of tasks simultaneously: writing, coding, drawing, diagnosing, driving, sorting, picking and packing. The historical pattern is the same. The blast radius is not.
      </p>

      <!-- ─────────────────────────────── 3 ─────────────────────────────── -->

      <h2 id="fabric">3. Reality Check: Jevons Paradox and Your Blue Jeans</h2>

      <p>
        Time to get slapped out of it, in both directions.
      </p>

      <p>
        In 1865, the economist William Stanley Jevons published <em>The Coal Question</em>. Britain was worried about running out of coal, and the popular assumption was that more efficient steam engines would save it. Jevons argued the opposite: making coal more efficient to use would make it cheaper per unit of work, which would open up new uses, which would increase total coal consumption. He was right. This is now called <strong>Jevons Paradox</strong>: when something gets dramatically cheaper to use, we tend to use dramatically more of it.
      </p>

      <p>
        Now look down at what you're wearing.
      </p>

      <p>
        Fabric is the oldest and cleanest example of automation we have, and we take it so much for granted we forget it was ever expensive. Before the Industrial Revolution, cloth was a serious store of wealth. People repaired clothing until it fell apart, passed garments down in wills, and in many households a large share of every woman's waking life went to spinning. Remember that table: 50,000 hours of spinning for 100 pounds of cotton.
      </p>

      <p>
        Then CLHE on spinning and weaving fell by roughly 99%. Here's what happened next.
      </p>

      <ul>
        <li><strong>We didn't make the same amount of cloth with fewer people. We made incomparably more cloth.</strong> Global fiber production is now well over 100 million tonnes a year. Clothing production roughly doubled in just the first fifteen years of this century.</li>
        <li><strong>Clothing went from a major expense to a minor one.</strong> In 1901, the average American household spent 14% of its budget on apparel. In 2024 it spent 2.5%.</li>
        <li><strong>The demand exploded into forms nobody in 1780 could have imagined:</strong> fast fashion, athletic wear, technical fabrics, band T-shirts, merch drops, cosplay, a pair of jeans for every mood. Cheap fabric didn't just satisfy the old demand. It invented new demand.</li>
        <li><strong>And humans are still sewing.</strong> This is the part that should stop you cold. After 250 years of textile automation, the step where a person guides fabric through a sewing machine is still overwhelmingly done by human hands, because fabric is floppy and stretchy and robots are still bad at it. Tens of millions of people work in textiles, clothing and footwear worldwide, many in Bangladesh, Vietnam, India and China. (Even that step is starting to move: robotics labs now sew whole garments by temporarily stiffening the cloth with a water-soluble polymer, then rinsing it soft.)</li>
      </ul>

      <blockquote>
        More automation than ever. More T-shirts and blue jeans than ever. And there are still human beings at the sewing machines.
      </blockquote>

      <p>
        That's the optimistic slap: <strong>automation doesn't end labor, it moves it.</strong> When the cost of one step collapses, demand for the whole product can grow so much that the steps that weren't automated need more people than before. Generation after generation, people have found the next thing to do. Spinners' grandchildren became clerks. Farmers' grandchildren became engineers, nurses and YouTubers.
      </p>

      <p>
        Now the other slap, which is just as real:
      </p>

      <ul>
        <li><strong>"Still requires human labor" does not mean "still pays well."</strong> The steps that resisted automation in clothing are some of the lowest-paid, most dangerous jobs on Earth. The Rana Plaza factory collapse in Bangladesh in 2013 killed more than 1,100 garment workers. The humans who remain in a heavily automated supply chain are often the ones with the least bargaining power.</li>
        <li><strong>Jevons protects demand for the output, not for any particular input.</strong> Demand for transportation exploded after the engine, exactly as Jevons would predict. Demand for horses didn't come back. The horse was the input that got replaced, and the extra demand flowed to the machine.</li>
        <li><strong>Humans have survived every previous round because there was always something the machines couldn't do yet.</strong> Hands when machines had muscle. Minds when machines had hands. AI is the first technology aimed directly at the mind. The rebound may still come, and history says bet on it. But it's a bet, not a law of physics.</li>
      </ul>

      <p>
        So the honest version is: the cycle will very likely continue, and humans will very likely adapt again. But "humanity adapts" is a statement about the species over decades. It says nothing about whether <em>you</em> land on the weaver's side of the table or the mill owner's side in the next ten years.
      </p>

      <!-- ─────────────────────────────── 4 ─────────────────────────────── -->

      <h2 id="conquest">4. 1519: The Conquistador Scenario</h2>

      <p>
        Fabric is the gentle analogy. Here's the severe one.
      </p>

      <p>
        In 1519, Hernán Cortés landed on the coast of Mexico with a few hundred men. Two years later, Tenochtitlan, one of the largest cities in the world at the time, had fallen. The Spanish brought steel, gunpowder, horses and ships the Mexica had never seen. Smallpox came with them and tore through the city in 1520. Over the next eighty years, waves of epidemic disease (smallpox first, then the cocoliztli fevers of 1545 and 1576, whose origin historians still debate) cut the Indigenous population of central Mexico by roughly 90%, from something like 20 million to under 2 million.
      </p>

      <p>
        Map it onto now:
      </p>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th scope="col">1519</th>
              <th scope="col">Now</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>The Spanish, arriving with technology the locals can't match</td><td>AI and robotics</td></tr>
            <tr><td>The indigenous population</td><td>Human workers</td></tr>
            <tr><td>Gold and silver: the thing everyone suddenly wants</td><td>Human labor, and control over whatever replaces it</td></tr>
            <tr><td>Smallpox: the damage no one planned</td><td>Second-order effects: collapsing wages, stranded skills, institutions that can't adapt fast enough</td></tr>
          </tbody>
        </table>
      </div>

      <p>
        Now follow the gold, because the actual gold tells you exactly where this goes.
      </p>

      <p>
        Cortés and his men melted down Mexica treasure into bars. Then the Spanish found the silver mines of Zacatecas and Potosí, and precious metal poured into Europe for the next century. The result was the <strong>Price Revolution</strong>: over roughly a century and a half, prices across Europe rose severalfold, in some cases sixfold. Spain was flooded with the most valuable substance in the world, and the value of that substance fell because there was so much of it. Philip II's crown suspended payments to its bankers four times (1557, 1560, 1575, 1596) while the silver passed through Spanish hands to the bankers of Genoa.
      </p>

      <blockquote>
        When a new world opens up and floods the market with the thing everyone used to fight over, that thing gets cheap. And the fight moves.
      </blockquote>

      <p>
        That's what's about to happen to labor. Human labor has always been scarce: there were only so many hands and so many hours. If a vast artificial labor force comes online, labor stops being scarce. Its price, the CLHE, falls toward the cost of electricity and hardware. Humans competing with machines for the same tasks will watch the value of their hours drop the way gold dropped in 16th-century Seville.
      </p>

      <p>
        Machines will keep gaining ground on every task that's economically valuable. And then, just like every time before, we will invent something new to compete over. Commodities will appear that nobody can currently foresee, that people want, and that are scarce. In 1519, nobody in Seville could have predicted that tobacco, sugar, chocolate and potatoes from the Americas would reshape the world economy. The treasure they came for wasn't the one that lasted.
      </p>

      <p>
        And there's one thing about this cycle that has never changed: <strong>as humanity expands its technology, it also expands its ability to control other humans with it.</strong> If a labor force of billions of machine-workers comes online, the most valuable resource on Earth stops being labor. It becomes <strong>control over labor</strong>: who owns the models, the robots, the data centers, the energy and the land they sit on.
      </p>

      <p>
        That's the uncomfortable twist in the analogy. The machines are not the conquistadors. Machines don't want gold. The conquistadors are whoever ends up controlling the machines.
      </p>

      <!-- ─────────────────────────────── 5 ─────────────────────────────── -->

      <h2 id="paths">5. Three Paths, and a Secret Fourth</h2>

      <p>
        Every civilization that has met a technologically superior force has gone down some mix of three roads. History has examples of each.
      </p>

      <div class="paths">
        <div class="path">
          <p class="path-num">Path 1</p>
          <p class="path-title">Steamrolled</p>
          <p class="path-body">
            The advanced side takes the resources and gives nothing back. The encomienda system handed conquistadors the forced labor of entire indigenous communities. In AI terms: the gains from machine labor flow almost entirely to whoever owns the machines, and everyone else is left competing for the shrinking set of tasks that are still cheaper to do by hand.
          </p>
        </div>
        <div class="path">
          <p class="path-num">Path 2</p>
          <p class="path-title">Merged</p>
          <p class="path-body">
            The two sides blend into something new. Modern Mexico is exactly this: a mestizo nation whose language, food, religion, art and people are a fusion of both worlds. Cortés himself only won because tens of thousands of Tlaxcalan and other indigenous allies fought beside him for their own reasons. In AI terms: humans and machines integrate, through tools, augmentation, and eventually maybe the body itself, until "human work" and "machine work" stop being separate categories.
          </p>
        </div>
        <div class="path">
          <p class="path-num">Path 3</p>
          <p class="path-title">Mastered</p>
          <p class="path-body">
            The less advanced side adopts the technology fast enough to control it. Meiji Japan, facing Western gunboats in the 1850s, industrialized in about a generation and was never colonized. Ethiopia bought modern rifles and defeated an invading Italian army at Adwa in 1896. In AI terms: individuals, communities and nations that own their own models, their own robots and their own energy, instead of renting them. The fine print: Japan didn't stop at mastering the machine. Within a generation it was taking colonies of its own, Taiwan in 1895 and Korea in 1910. Mastery isn't the same thing as decency.
          </p>
        </div>
      </div>

      <p>
        My honest guess is that we get all three at once. Some people and some countries get steamrolled. Some blend. Some take control. The mix depends on choices being made right now about who owns this technology.
      </p>

      <div class="path path-secret">
        <p class="path-num">The secret fourth path</p>
        <p class="path-title">Breakaway</p>
        <p class="path-body">
          A breakaway civilization leaves Earth. This has a historical echo too: every wave of settlers that crossed an ocean eventually stopped being the people who left. But this time the divergence could be biological, not just cultural. We already know that bodies change in space: bone density drops, muscle wastes, fluid shifts, vision changes. Children who grow up in low gravity, under different radiation, in engineered environments, and possibly with engineered biology, could over generations become something measurably different from Earth humans. A subspecies, not by choice of flag but by the physics of where they were raised. It's speculative. It's also the one path none of the Mexica, Spanish, Japanese or Ethiopians ever had.
        </p>
      </div>

      <!-- ─────────────────────────────── 6 ─────────────────────────────── -->

      <h2 id="next">6. Two Futures, One Certainty</h2>

      <p>
        Collapse all of that down and you get two broad futures, and both of them have already happened to someone:
      </p>

      <ul>
        <li><strong>A. We get outcompeted, and we suffer.</strong> This is 1521 Tenochtitlan. It's the handloom weavers of the 1830s. It's the horse.</li>
        <li><strong>B. We keep control of the technology, and the economy evolves to value new kinds of scarcity.</strong> This is the long arc of the textile story: cheap cloth, and people moving on to work nobody in 1780 could have described.</li>
      </ul>

      <p>
        Here's the part that doesn't depend on which one we get. Whether cheap, abundant labor arrives through private companies or through governments nationalizing these space-age technologies, the economic result is the same:
      </p>

      <ol class="chain">
        <li>The supply of labor increases exponentially.</li>
        <li>The price of a labor-hour, its CLHE, collapses toward the cost of energy and hardware.</li>
        <li>Jevons Paradox kicks in: cheap labor gets used for far more things than expensive labor ever was. Use cases nobody bothered with, because they weren't worth paying a person for, suddenly make sense.</li>
        <li>Value migrates away from labor itself and toward whatever is still scarce.</li>
        <li>The economy reorganizes around new forms of scarcity that we mostly can't name yet.</li>
      </ol>

      <p>
        We don't know what those scarcities will be. We can be confident some of what drives them hasn't been invented yet. But we can make educated guesses by reading the past: attention, trust, provenance (proof a real person made something), land, energy, ownership of compute, physical presence, taste, and authority over the machines themselves. Every one of those is already getting more valuable as labor gets cheaper.
      </p>

      <p>
        That's the practical takeaway, and it's the same one this whole site is built on. <strong>Don't compete with the machine on price per hour. You will lose that race the way the spinners lost it.</strong> Instead, own a piece of the machine: your own local AI, your own robot, your own food production, your own energy, your own small-scale supply chain. Be on the side of the table that controls the labor, even if it's just a little bit of it.
      </p>

      <p>
        The conquistadors are coming either way. The question is whether you're the one holding the map.
      </p>

      <div class="cta-block">
        <p class="cta-label">Stay in the Loop</p>
        <p class="cta-body">
          More on the economics of machine labor, and how to own a piece of it instead of competing with it, goes out to the list first.
        </p>
        <div class="cta-signup" id="signup">
          <NewsletterSignup source="blog-labor-hour" label="" buttonText="Get Updates" bookUrl="/book" />
        </div>
        <a href="/book" class="cta-link">Read the book for the full blueprint →</a>
      </div>

    </div>
  </article>

  <div class="post-footer">
    <a href="/blog" class="back-link">
      <span aria-hidden="true">←</span> Back to Blog
    </a>
    <SocialShare title={post.title} description={post.description} image={post.image} />
  </div>

  <Spacer height="4rem" />
</div>

<style>
  .blog-post {
    min-height: 100vh;
    background-color: #020617;
    color: #e2e8f0;
  }

  .post-inner {
    max-width: 720px;
    margin: 0 auto;
    padding: 3rem 1.5rem 2rem;
  }

  .post-header {
    margin-bottom: 3rem;
  }

  .back-link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.85rem;
    color: #64748b;
    text-decoration: none;
    margin-bottom: 2rem;
    transition: color 0.15s ease;
  }
  .back-link:hover { color: #f59e0b; }

  .post-title {
    font-size: clamp(1.6rem, 5vw, 2.4rem);
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1.2;
    letter-spacing: -0.02em;
    margin: 0 0 1rem;
    text-wrap: balance;
  }

  .post-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #64748b;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
  }
  .sep { color: #334155; }

  .content {
    font-size: 1.05rem;
    line-height: 1.8;
    color: #cbd5e1;
  }

  .lead {
    font-size: 1.2rem;
    font-weight: 500;
    color: #e2e8f0;
    line-height: 1.7;
    margin-bottom: 1.5rem;
  }

  .content p { margin: 0 0 1.25rem; }

  .content h2 {
    font-size: 1.35rem;
    font-weight: 700;
    color: #f59e0b;
    margin: 2.5rem 0 0.85rem;
    letter-spacing: -0.01em;
    scroll-margin-top: 5rem;
  }

  .content ul,
  .content ol {
    margin: 0 0 1.25rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }

  .content ul { list-style: disc; }
  .content ol { list-style: decimal; }

  .content li { line-height: 1.7; }

  .content strong { color: #f1f5f9; font-weight: 600; }

  /* Table of contents */
  .toc {
    margin: 0 0 2.5rem;
    padding: 1.25rem 1.5rem;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 12px;
  }
  .toc-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94a3b8;
    margin: 0 0 0.6rem !important;
  }
  .toc ol { margin-bottom: 0; gap: 0.3rem; }
  .toc a {
    color: #cbd5e1;
    text-decoration: none;
    font-size: 0.95rem;
  }
  .toc a:hover { color: #f59e0b; }

  /* Formula + definition */
  .formula {
    margin: 1.5rem 0;
    padding: 1rem 1.25rem;
    background: rgba(59, 130, 246, 0.06);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-radius: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
  }
  .formula-line { margin: 0 !important; color: #e2e8f0; }
  .formula-name { color: #3b82f6; font-weight: 700; }
  .formula-sub { padding-left: 1.5rem; color: #94a3b8; }

  .definition {
    margin: 2rem 0;
    padding: 1.5rem;
    background: rgba(245, 158, 11, 0.06);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 12px;
  }
  .definition-term {
    font-size: 1.2rem;
    font-weight: 800;
    color: #f59e0b;
    margin: 0 0 0.75rem !important;
  }
  .definition-abbr {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    font-size: 0.95rem;
    color: #fbbf24;
  }
  .definition-body { color: #e2e8f0; }
  .definition-rule {
    margin: 0 !important;
    padding-top: 0.9rem;
    border-top: 1px solid rgba(245, 158, 11, 0.2);
    font-weight: 600;
    color: #f1f5f9;
  }

  /* Tables */
  .table-wrap {
    margin: 1.5rem 0 0.5rem;
    overflow-x: auto;
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 10px;
  }
  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    line-height: 1.5;
    min-width: 560px;
  }
  .data-table th {
    text-align: left;
    padding: 0.7rem 0.9rem;
    background: rgba(30, 41, 59, 0.8);
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
  }
  .data-table td {
    padding: 0.7rem 0.9rem;
    border-top: 1px solid rgba(148, 163, 184, 0.1);
    vertical-align: top;
    color: #cbd5e1;
  }
  .data-table tbody tr:nth-child(even) td { background: rgba(30, 41, 59, 0.3); }
  .table-note {
    font-size: 0.78rem !important;
    color: #64748b;
    line-height: 1.55;
    margin-bottom: 1.75rem !important;
  }

  /* Paths */
  .paths {
    display: grid;
    gap: 1rem;
    margin: 1.5rem 0 1.75rem;
  }
  .path {
    padding: 1.25rem 1.4rem;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-left: 3px solid #3b82f6;
    border-radius: 10px;
  }
  .path-secret {
    margin: 1.5rem 0 1.75rem;
    border-left-color: #f59e0b;
    background: rgba(245, 158, 11, 0.05);
  }
  .path-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94a3b8;
    margin: 0 0 0.25rem !important;
  }
  .path-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.5rem !important;
  }
  .path-body {
    margin: 0 !important;
    font-size: 0.98rem;
  }

  .chain li::marker {
    color: #f59e0b;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
  }

  blockquote {
    border-left: 3px solid #f59e0b;
    padding: 0.75rem 1.25rem;
    margin: 2rem 0;
    background: rgba(245, 158, 11, 0.05);
    border-radius: 0 8px 8px 0;
    font-size: 1.1rem;
    font-style: italic;
    color: #e2e8f0;
  }

  .cta-block {
    margin: 3rem 0 0;
    padding: 2rem 1.5rem;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 14px;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .cta-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #f59e0b;
    margin: 0;
  }

  .cta-body {
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.65;
    margin: 0;
  }

  .cta-signup {
    margin-top: 0.25rem;
  }

  .cta-link {
    font-size: 0.85rem;
    color: #64748b;
    text-decoration: underline;
    text-underline-offset: 3px;
    width: fit-content;
  }
  .cta-link:hover { color: #f59e0b; }

  .post-footer {
    max-width: 720px;
    margin: 2.5rem auto 0;
    padding: 1.5rem 1.5rem 0;
    border-top: 1px solid rgba(148, 163, 184, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
  }

  @media (max-width: 640px) {
    .post-inner { padding: 2rem 1.25rem 1.5rem; }
    .post-footer { padding: 1.25rem 1.25rem 0; }
    .definition { padding: 1.25rem; }
  }
</style>
