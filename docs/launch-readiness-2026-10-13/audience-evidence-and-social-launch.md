# Audience, evidence and social launch

Research checked 13 October 2026 against the integrated v0.11.0 candidate, starting at `7ffe1545`. This is a launch working document, not customer research or a claim-by-claim certification of the book. No sales analytics, follower analytics, customer interviews or conversion experiments were available. The audience priorities and composite below are hypotheses to test; source findings are labeled separately. Nothing here has been posted, scheduled or sent.

## What to launch

**Launch digital early access to the current book draft, with a public sample and a concrete invitation to try one useful action.** The product currently sells a $5 digital preorder, current PDF/EPUB and online draft, plus The Precedent File. Future digital editions are included while the project is maintained; preorder buyers do not pay the planned membership. Print is a separate purchase, with the stated half-price benefit for the early cohort. This is the actual offer in [`src/lib/offer.js`](../../src/lib/offer.js), not a finished print-book announcement.

Proposed positioning: **A provocative book about AI, food, and what neighbors can build together. Read the argument, examine the forecasts, and choose a practical place to start.**

That fits the book better than promising a proven survival blueprint, career insurance, or a definitive AGI timetable. The manuscript mixes argument, sourced history, speculative fiction, forecasts, and proposals. Its distinctive commercial idea is practical cooperation around everyday needs; its voice is direct and sometimes abrasive. Do not hide either fact from a buyer.

The launch should show an actual excerpt and a useful exercise before asking someone to accept the entire thesis. The free checklist is an especially good entry for an unfamiliar audience. The public sample establishes the author's voice and includes the reading guide, but it is an introduction, not a free implementation chapter.

## Evidence checked again

| Claim or inference | Primary evidence checked | What the launch may responsibly say |
| --- | --- | --- |
| 300 million jobs | [Goldman Sachs, 5 April 2023](https://www.goldmansachs.com/insights/articles/generative-ai-could-raise-global-gdp-by-7-percent) describes potential automation exposure equivalent to 300 million full-time jobs, with most occupations only partially exposed. | Keep the date, conditional exposure, and full-time-equivalent scope. This is not a count of jobs already lost or destined to disappear. Current homepage wording has those distinctions. |
| 99% of executives | [Mercer's early-career article](https://www.mercer.com/en-gb/insights/talent-and-transformation/skill-based-talent-management/ai-and-early-career/) attributes the figure to Global Talent Trends 2026: expectation of AI-related reductions affecting 1–20% of roles over two years. | Describe surveyed executives' expectations. The article supports the attributed number; this pass did not independently inspect respondent-level data or validate the sampling method. Do not turn it into 99% of jobs or a documented layoff plan. |
| Expert AI dates | [Grace et al., arXiv 2401.02843](https://arxiv.org/abs/2401.02843), initially 2024, revised 8 October 2025, reports a survey of 2,778 researchers and aggregate 10%/50% dates of 2027/2047 for the stated capability definition. Full automation of occupations has different dates. | Retain the distinction between a survey forecast, the author's November 2027 forecast, and demonstrated capability. No consensus deadline or guaranteed recursive improvement follows from these numbers. |
| Affordable robotics | [LeRobot's official documentation](https://huggingface.co/docs/lerobot/index) and [SO-101 assembly guide](https://huggingface.co/docs/lerobot/so101) expose software, hardware and assembly work. | Accessible experimentation is supported. Equivalent industrial performance, safe unattended use, a complete price for every task, and household self-sufficiency are not established by an inexpensive arm. |
| Current labor context | [ILO research brief, 1 June 2026](https://www.ilo.org/publications/impact-genai-jobs-productivity-and-work-organization-review-empirical) synthesizes experiments, firm studies, platform studies and surveys; it describes uneven gains and limited broad displacement so far. | Preparing for change is reasonable. A claim that economy-wide replacement has already happened would outrun this evidence. Expectations, technical exposure and observed employment outcomes answer different questions. |
| Why an anxious-but-curious reader is plausible | [Pew, 17 June 2026](https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/) surveyed 5,119 U.S. adults in February 2026: 49% report chatbot use, while views of AI's impact remain skeptical. | Use and skepticism can coexist. This supports an entry that welcomes questions. It does not establish this site's audience, demand for this book, or willingness to pay. |
| Food, shelter and care | Current Chapters 9, 18 and 19 describe proposals, costs, remaining labor, backups and measures of provision. | Present an ambition and a plan to test. A robotic demonstration or local vegetable trial is not proof of complete nutrition, housing provision, medical care, or freedom from outside inputs. |

The useful challenge to the book is not “Can you find a prestigious source saying AI matters?” It is “Does this source support this exact claim, at this scale, and does the practical recommendation still work if the forecast is late?” Use that question in replies as well as on the site.

### Purchase-page gap repaired in this pass

The purchase page still claimed that 2017 parallel self-attention made unassisted recursive self-improvement possible; described a closed loop for food, shelter and medicine; called the author's measure a replacement for GDP; and displayed an unqualified 2027 tipping-point quote. Those statements contradicted the more careful current manuscript and corrected homepage.

The body now distinguishes evidence, increasingly speculative scenarios, historical comparison and proposed practical trials. The old quote is replaced with the author's actual Chapter 1 admission that the forecast may be wrong. The preview no longer implies an available separate “blueprint” page. No canonical book prose or checkout behavior changed. The edited Svelte component compiled without errors and the offer-drift guard passed; rendered checks belong to the integrated release validation.

### Biological-computing articles corrected

Both `/blog/synthetic-biological-intelligence` and `/blog/synthetic-biological-computers` compared GPT-3 training energy in megawatt-hours with an alleged CL1 rack power figure in watts, then implied a computing-efficiency advantage. The numbers describe different quantities and different work. [Patterson et al. (2021), Table 4](https://arxiv.org/pdf/2104.10350) supports the 1,287 MWh training estimate. The [CL1 product page](https://corticallabs.com/cl1) describes a neural platform with life support, but provides no matched language-model benchmark establishing the claimed advantage. The 30-unit/1,000-watt figure could not be verified from that primary page and was removed rather than repeated as a specification.

The articles and the first article's FAQ now require matched tasks, output quality, duration and complete system energy. They also limit the learning comparison: [Kagan et al. (2022), available through UCL](https://discovery.ucl.ac.uk/id/eprint/10158064/) describes DishBrain in a simplified Pong environment; [Khajehnejad et al. (2025), author-university record](https://research.monash.edu/en/publications/dynamic-network-plasticity-and-sample-efficiency-in-biological-ne/) compares sample efficiency with three selected reinforcement-learning approaches in that setting. These results do not demonstrate general AI superiority or equivalent language-model capability. Both pages carry a visible correction date. The older audio is explicitly labeled as predating the correction; its content has not been regenerated or certified. This targeted correction is not a full scientific review of every historical article.

Both edited components compile without errors. Read-only Chromium checks at 390px and 1440px verified both rendered routes return 200, show the correction and source links, contain no old rack-power/general-superiority assertion, and have no horizontal overflow or uncaught page errors. The first article's energy FAQ opens with the corrected units explanation. Neither route emits separate FAQ JSON-LD. The second article's search/share description and blog-index excerpt now match the limited claim. These are local rendered checks; the deployed articles still require the release update.

## Current alternatives competing for attention

These are adjacent reader choices, not proof of the same audience or substitutes with identical scope. Descriptions below come from official author/publisher pages, checked on the review date. Retail discounts and regional prices vary; no price comparison is needed to make the case for this $5 draft.

| Alternative | Observed positioning | Implication for this launch |
| --- | --- | --- |
| [Co-Intelligence, Ethan Mollick](https://www.penguinrandomhouse.com/books/741805/co-intelligence-by-ethan-mollick/) | Practical engagement with AI for work, learning and life; published 2 April 2024. | “Understand AI and use it at work” alone is crowded. Lead with this book's food, local provision, cooperation and author voice. |
| [Co-Existence, Ethan Mollick](https://co-existence.ai/) | Official release date 20 October 2026; a guide to living and working with unevenly capable AI. Its launch page separates the book, preorder benefit and delivery expectations. | This is immediate competing attention, one week after this review. Make this project's different purpose obvious. Do not imply affiliation or use the other launch as fabricated urgency. |
| [The Coming Wave, Mustafa Suleyman with Michael Bhaskar](https://www.penguinrandomhouse.com/books/722674/the-coming-wave-by-mustafa-suleyman-with-michael-bhaskar/) | Technology, power, governance and containment at large scale. | This book can offer a closer-to-home question and exercises, without claiming that a neighborhood solution settles national governance. |
| [The Singularity Is Nearer, Ray Kurzweil](https://www.penguinrandomhouse.com/books/535433/the-singularity-is-nearer-by-ray-kurzweil/) | Broad technological forecasting and a hopeful long-range future. | Readers attracted by the title may expect a forecasting book. Say early that the practical thesis concerns meals, tools, agreements and local provision. |
| [One Useful Thing](https://www.oneusefulthing.org/about) | Ongoing research-based AI commentary and links to free resources. | The competitor is also free material and an overloaded reading queue. Show the book's coherent route and one usable practice; length and a low price alone are weak reasons to read it. |

## Who to reach first

Prioritize behavior and the job a reader wants done over age or an imagined demographic niche. This is an English-language launch, and many practical examples are U.S.-specific; readers elsewhere may need different institutions, regulations and resources. Do not advertise universal implementation instructions.

| Priority segment | Trigger and constraint | Useful promise and first destination | What would validate fit |
| --- | --- | --- | --- |
| Existing followers who like the author's voice | They have watched the work develop and want to know what exists now. Their risk is confusing support with a finished product. | Current draft, visible sample and precise deliverables; `/early-access` for a warm purchase invitation. | They can correctly explain what they bought and open it without help. |
| Working adults who use AI but feel unsettled | A task changes, a client changes expectations, or a colleague demonstrates a tool. They have limited time and ongoing household obligations. | One small useful action before a worldview; `/checklist`, then `/sample`. | They complete an action and can name a next question worth reading about. |
| Makers and practical collaborators | They already repair, grow, organize or build; novelty alone will not persuade them. | An argument they can interrogate, with costs and failure criteria; `/sample` reading guide toward Chapters 9, 13 and 17 after access. | They distinguish a proposal from an achieved pilot and offer a specific improvement. |
| Early-career readers with limited resources | They want a first step and fear that “prepare” means buying land or expensive hardware. | Start with a task, a skill and willing people; free `/checklist`. | The exercise is usable with their existing resources and does not require buying the book. |
| Community organizers, educators and institutions | They need responsible material and clear ownership of outcomes. Procurement and reputation cost more than $5. | Sample and sources first; reading guide toward Chapters 12, 18, 19 and Appendix A. | They can identify a bounded discussion or pilot, named specialists and unanswered questions. Do not treat this as proof of consulting demand. |

### The primary cold-visitor avatar, in operational detail

**Sam is an illustrative composite, not an observed customer.** Imagine a 34-year-old employee or freelancer doing a mix of writing, administration, coordination and judgment. The age, occupation and circumstances are a scenario for design; they are not known demographics. The important traits are income dependence, some direct AI experience, curiosity, skepticism, and little spare attention.

Sam is not starting with “I believe AGI arrives in 2027.” Sam is starting with “Something at work changed, and I want more choices.” They may like their profession and resent being told their concern is wounded status. They may value technology and still care about privacy, consent, skill erosion and who gets the gains. A visitor can be sympathetic to food security while disliking the author's politics or cosmic scenarios.

Their immediate trigger is specific: a client asks for faster turnaround, a manager demonstrates automated work, an entry-level role disappears from a hiring plan, or an acquaintance builds something surprisingly useful. This is the moment to invite a task inventory or one experiment. Do not inflate a single anecdote into an employment forecast.

Their scarce resource is a useful half-hour. Five dollars may be affordable while a 400-page commitment is not. A mobile visit happens between other obligations. The first screen must tell them: book, current draft, topic, price, free way to inspect it. The reading guide matters because it turns a large book into a path; a countdown does not answer the time-cost objection.

Sam may rent, have dependents, live with others, lack a workshop, or have limited physical capacity. The first win should survive those constraints. They can list tasks, record a household dependency, talk to a willing neighbor, compare a tool on one task, or keep a dated forecast record. They should not have to buy land, quit a job, upload private employer material, or treat DIY work as a substitute for qualified trades.

They are buying an organized argument, the author's perspective, a usable reading route and practices to consider. They are not purchasing guaranteed safety or access to an expert on demand. “All digital content” must not imply that individual consulting, a community installation, a course or a robot is included.

Their trust checks are concrete: Does the sample sound worth reading? Is fiction distinguishable from a real case? Is the source actually relevant? Do I get a file, a website login, or both? What happens after payment? Is print included? Can I get a refund? Does signing up enroll me in a newsletter? A direct answer to each removes more friction than another dramatic prediction.

Their likely objections are “I can read AI news free,” “This sounds like prepper marketing,” “I don't have land,” “The date seems made up,” “Was this written with AI?” and “I don't want another subscription.” Answer with the actual sample, bounded proposals, personal-forecast label, candid authorship disclosure and one-time preorder terms. Never invent independent endorsements or tested outcomes to settle the objection.

Their imagined journey is a testable hypothesis: a social post about one ordinary problem → checklist or sample → recognition that the voice and scope fit → offer details → checkout → verified downloads → reading guide → one chosen practice → an honest recommendation. A warm follower can enter at the offer. A hostile reader may stop at the sample; optimizing for universal agreement would erase the author's voice without proving demand.

The success moment is not simply “Sam bought.” It is “Sam opened the right version, understood its status, found their reading path, and received the thing promised.” A later recommendation should come from that experience. The project currently has no evidence that this sequence converts; collect actual feedback before claiming it does.

## Critic and supporter stress test

| Reaction | Strongest fair objection | Prepared response/action |
| --- | --- | --- |
| First-time visitor | “What actually is this?” | A current digital book draft mixing argument, fiction and practical proposals. Show the public sample and the $5 offer; do not send a cold visitor directly to a password gate. |
| Experienced expert | “Exposure isn't displacement; a Transformer isn't proof of recursive improvement.” | Agree with the distinction, point to the scoped primary source and corrected purchase summary, and invite an exact claim/source correction. |
| Hostile critic | “You're monetizing fear and an arbitrary date.” | Show the open sample, personal-forecast boundary, modest reversible exercises and purchase terms. Avoid arguing that disbelief itself proves the book's thesis. |
| Creator opposed to AI | “You're treating consent and labor concerns as aesthetic insecurity.” | Acknowledge those concerns as substantive. The sample's abrasive status rhetoric remains a real taste barrier. Do not market the book as a neutral consensus textbook. |
| Enthusiastic supporter | “These robots can already feed a whole neighborhood!” | Preserve enthusiasm while correcting scope: the manuscript proposes bounded trials with people, costs, inputs and backups. Do not repost an unsupported testimonial as fact. |
| Practical builder | “Where is the working system, bill of materials and measured result?” | Distinguish real technology examples from proposed local systems and fictional scenes. Do not advertise completed deployments or consulting case studies that have not been demonstrated. |
| Buyer | “I paid and the email hasn't arrived.” | Use the verified receipt/access recovery flow. A support response must reflect actual provider state; an accepted email is not proof of inbox arrival. Never tell them to buy again. |

## Ready-to-review launch copy

These drafts are **unsent**. The launch wording below assumes the candidate has been deployed, checkout/delivery verified and public links tested on the actual domain. Until then, use the preparation version. Do not publish an “available now” message on the strength of a local test.

The candidate includes landscape cards at `/images/og/sample.png`, `/images/og/early-access.png`, `/images/og/checklist.png` and `/images/og/factcheck.png`. Use the real final link in each platform's composer and inspect its preview after deployment; crawlers may retain old cards until refreshed. A correct local image does not prove the platform's cached preview is current. In the predeployment check, production `/sample` was still unavailable, so the launch link requires a fresh live-domain check.

### Preparation post, usable before activation

I'm getting *Surviving the Singularity* ready for digital early access.

It's a book about AI, food, and what neighbors can build together: historical cases, speculative stories, and practical proposals you can argue with.

The current draft is v0.11.0. I'm checking the reading experience and delivery before I announce that it's ready to buy. The question at its center is simple: how do we make ordinary life more secure as the tools change?

### Main launch post, after activation

Digital early access to *Surviving the Singularity* is open.

I wrote it around a question I can't leave alone: if machines can do more, how do we make sure ordinary people actually get a better life?

The book moves from AI forecasts and historical cases to food, shared tools, local energy, and the agreements that keep people fed. There are fictional scenes and speculative futures in it, too. You can disagree with my timeline and still have work worth doing with your neighbors.

The current v0.11.0 draft is $5 once: PDF, EPUB, online reading and The Precedent File. Future digital editions are included while I maintain the project. Preorder buyers won't pay the planned membership. Print is separate.

Read the free introduction and reading guide first. No email required:
https://survivingthesingularity.com/sample

### Short social post, after activation

Digital early access is open: *Surviving the Singularity*. AI, food, and what neighbors can build together. Current draft: $5 once. Read the free sample first, no email required: https://survivingthesingularity.com/sample

### Practical follow-up

One thing you can do before buying any book about AI: write down the tasks in your work, then ask someone who knows the work what you missed.

Pick one small task to test a tool on. Keep track of time, quality, mistakes and the human work still needed. Use material you're allowed to use. A flashy demo and a useful result aren't the same thing.

The free *Surviving the Singularity* checklist is here:
https://survivingthesingularity.com/checklist

### Maker/community follow-up

Before proposing a robot, ask the person already doing the work which repeated task wastes their time.

That's where I want the conversation around *Surviving the Singularity* to begin: useful work, real costs, willing people, and a result somebody can check.

The draft explores a food-first approach to local cooperation. The free introduction explains the argument and helps you choose a reading path:
https://survivingthesingularity.com/sample

### Short video outline

Open with the author on camera: “I wrote a book about AI. The part I care most about is dinner.” Show the actual current PDF/EPUB cover and one legible reading-guide excerpt. Explain the food-first question in one ordinary example, name the work as a current draft, and close with the free sample. Caption the speech and provide descriptive alt text for static images. Use real book pages and author-owned imagery; a robot animation should not be presented as a completed field trial.

## First release feedback loop

Begin with the author's existing audience and a useful free entry. Paid advertising is a separate budget decision; no spend or campaign activation is authorized by this document. Do not add tracking or import contacts just to implement this plan.

Before the broad purchase announcement, the operational handoff must show an actual deployed candidate, correct price/mode, successful download and access recovery, and verified email delivery. Then read the first buyer questions as product evidence. Pause the purchase invitation if delivery or duplicate-payment problems appear; a functioning sample can still be shared honestly.

For a small qualitative check, invite willing readers from different segments to explain what the site sells, find the free sample, choose a reading route and describe what they expect after payment. Record exact misunderstandings, not an invented persona score. Five conversations can find defects; they cannot establish conversion rates or represent a market.

Ask three voluntary follow-up questions after a reader has had time to use it: What brought you here? Which page or chapter did you actually use? What did you expect that you did not find? Add “what would make this useful to someone you know?” only after learning what happened. Request permission before publishing any testimonial and preserve its actual scope.

If approved analytics already exist, compare qualified sample visits, offer visits, completed payments and support failures with consistent denominators and a stated time period. Report platform link clicks separately from site visits; social preview crawlers can fetch pages without a human reader. Small first-week counts are directional evidence, not statistically established winners. Without analytics, maintain a simple aggregate launch log and voluntary feedback rather than pretending to know the funnel.

UTM-tagged entry links alone do not establish sales attribution. This candidate has no verified UTM capture or propagation from `/sample` through `/early-access` into payment metadata; an initial query may be lost on navigation. Do not claim channel-to-purchase reporting from tagged links unless that separate behavior is implemented and tested.

Keep the promise, source, date and destination with each future post. The book can be opinionated. The offer and evidence still need to be exact.
