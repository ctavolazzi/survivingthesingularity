# Chapter 1: The Event Horizon

![Event Horizon Telescope image of the M87 supermassive black hole](/book-images/ch01-m87-black-hole.jpg)

*The event horizon of M87. Past a certain line, there is no going back. (Event Horizon Telescope Collaboration, CC BY 4.0, via Wikimedia Commons)*


> *"Within thirty years, we will have the technological means to create superhuman intelligence. Shortly after, the human era will be ended."*
> Vernor Vinge, *The Coming Technological Singularity* (1993)

**In this chapter:**

- The event horizon is behind us, not ahead. The Singularity is not a forecast; it is a structural condition we are already living inside.
- The 2017 Transformer paper, "Attention Is All You Need," automated the one thing we thought was ours alone: the processing of thought itself.
- Silicon is not the only front. Biological computing is closing on the same target from a completely different, far more energy-efficient direction.
- The clock reads 2027, the point where the machine begins, in earnest, to rewrite its own code without us.

---

The Monday after the toast, Elijah brought the printout to work.

He'd read "Attention Is All You Need" so many times over the weekend that the pages had gone soft at the corners, furred with highlighter in four colors that had stopped meaning anything distinct. He'd slept maybe five hours across two nights. He carried the thing into Claypot the way you carry a lab result you don't want confirmed, and he found Devendra at the good coffee machine on the fourth floor, because Devendra was senior, and calm, and had been doing this since before Elijah could spell *gradient descent*, and Elijah needed someone to tell him he was overreacting.

"I think it's already over," Elijah said. No preamble. "I watched three people get replaced last week. Real people. Not a projection… a bar, a Tuesday, three jobs, gone. And nobody who did it even thought of it as a big deal."

Devendra tapped his cup against the drip tray, unhurried. "Augmentation, not replacement," he said. It had the worn smoothness of a thing said many times. "It's a very good autocomplete, Elijah. It makes the people who use it faster. The realtors didn't fire humans because a chatbot is a person. They restructured. Companies restructure." He smiled, not unkindly, the way you smile at someone who's just discovered a thing you made your peace with years ago. "You'll calibrate. Everybody's first month feels like the apocalypse."

Elijah wanted to be talked down. That was the humiliating part. He stood there holding the soft pages and *wanted* the calm to work on him. But it slid off, because he'd seen the training curves inside this building, and he'd done the one thing Devendra's reassurance depended on him not doing, which was the arithmetic.

So that night he decided to settle it with his own hands, the only way a farm kid ever really trusts a thing: he'd try to break it.

He had an old tower at home, a space heater of a machine he'd built for cheap during the pivot, two consumer GPUs zip-tied into a case that didn't quite fit them. He pulled a modest open model and started fine-tuning it on his own data, telling himself that if he could feel where it topped out, if he could find the ceiling by touch, he'd know it was just software, bounded like all software, and he could sleep.

The room got warm around eleven. Warm the way the cab of his delivery car used to get in August, that thick engine-heat with a smell to it. The fans spun up to a howl he could hear from the kitchen. He kept feeding it. The loss curve kept sliding down, not magically, not infinitely, but *steadily*, the way a thing slides when there's real signal underneath and you've simply never had the compute to chase it before. Every increment cost him more. More power off the wall, more heat into the room, the meter he couldn't see spinning somewhere out in the garage.

At 1:20 a.m. the machine threw the temperature warning, throttled itself to protect the silicon, and then, when he stubbornly queued another run, shut down hard. Black screen. The fans coasted to silence. The room ticked as it cooled, exactly like the engine of a car after a long haul.

Elijah sat in the sudden quiet with sweat cooling on the back of his neck and understood something he would spend a whole later chapter of this book trying to say properly.

The thing hadn't hit a ceiling of *intelligence*. It had hit a ceiling of *heat*. It would have kept getting better, it was still getting better when the hardware quit, and the only wall it found was thermodynamic. The machine that had dissolved three careers at the Bear Flag was not magic and was not bounded by cleverness. It was bounded by *watts*, by *cooling*, by the same brutal physics that decided whether his grandmother's crop lived or died. Give it more power and more heat to shed, and it would keep walking down that curve past anything a person could follow.

He had wanted proof it was just software. He'd gotten it. And the proof was so much worse than the fear, because *just software* running on *enough energy* was precisely the problem. There was no clever limit coming to save anyone. There was only the power bill, and the people who could afford it.

He didn't tell Devendra any of this. There was no point. Devendra wasn't wrong about the small mechanics, it *was* autocomplete, it *did* make people faster. He was wrong about the only thing that mattered, which was where the curve went when you stopped pretending it would politely stop. Elijah had watched it not stop. He'd had to unplug it to make it stop.

He left the tower off for a week. Then he opened the notebook where he'd written MADRONE ≠ DRONE, and under it, he started keeping the arithmetic.

---

## The Foundations

## The Event Horizon of General Intelligence
The public, institutional, and academic discourse surrounding advanced technology frequently approaches the concept of the Technological Singularity as a hypothetical event confined to the distant future. However, empirical trajectories across machine learning, biological computing, and macroeconomic restructuring indicate that the event horizon has already been crossed. The Singularity is no longer an abstract philosophical debate; it is an active, structural reality driven by exponential progressions in computational intelligence and the decoupling of economic value from human labor. The fundamental premise of this societal and technological transition is that intelligence, historically the ultimate scarce resource that has gated human progress, innovation, and production, is rapidly approaching a marginal cost of zero.

The friction currently observed across global markets, socio-political institutions, and local communities is the direct result of legacy systems attempting to artificially meter this zero-cost resource. Corporate monopolies and traditional capitalist frameworks are attempting to fence this moment behind digital moats, forcing humanity to pay subscription fees for a resource that requires minimal variable cost to reproduce, thereby trapping the population in an artificial system of debt and transactional compliance. To understand the trajectory of the coming decade, it is necessary to analyze the exact mechanisms driving this intelligence explosion, the societal and psychological backlash it guarantees, and the hyper-local infrastructural pivots required to survive the systemic collapse of the labor-based social contract. An objective, data-driven analysis maps a distinct progression from the current era of Artificial General Intelligence (AGI) toward Artificial Superintelligence (ASI), and ultimately, to structural shifts on a cosmological scale.

## The Structural Automation of Thought
The modern acceleration toward AGI was fundamentally catalyzed in 2017 with the introduction of the Transformer architecture by researchers at Google Brain and Google Research. Prior to this innovation, the dominant sequence transduction models in natural language processing relied heavily on complex recurrent neural networks (RNNs) or convolutional neural networks (CNNs) arranged in rigid encoder-decoder configurations. These legacy architectures were inherently bottlenecked by their sequential processing requirements; a system had to fully process step t before it could process step t+1, severely limiting the ability to leverage modern hardware accelerators.

The seminal paper "Attention Is All You Need" achieved a profound structural breakthrough by dispensing with recurrence and convolutions entirely, relying solely on an attention mechanism to map global dependencies between input and output. This shift to parallel self-attention represented the literal automation of thought processing, allowing operations to be massively parallelized. The foundational model was small by today's standards, roughly sixty-five million parameters in its base configuration, and it still beat everything before it.

| Evaluation Metric / Task | Legacy Ensemble State-of-the-Art | Transformer Architecture Result |
| :-: | :-: | :-: |
| WMT 2014 English-to-German (BLEU) | ~26.4 BLEU | 28.4 BLEU (improvement of >2 BLEU) |
| WMT 2014 English-to-French (BLEU) | ~40.4 BLEU | 41.8 BLEU |
| Training Compute Cost | Weeks to Months on vast clusters | 3.5 days on eight GPUs |

*Table 1: Performance Benchmarks of the 2017 Transformer Architecture.*

By eliminating the sequential bottleneck, self-attention dramatically improved the speed, scalability, and efficiency of models, enabling the processing of intricate patterns over long-range dependencies across massive datasets. This parallelization was not merely a software optimization; it fundamentally altered the physical execution of machine learning. Later implementations went further, restructuring the model so that its attention and feed-forward stages run concurrently instead of one after the other, squeezing measurably more work out of every GPU in the cluster.

Crucially, this massively parallelized compute architecture grants the model the ability to process its own structure, setting the foundation for unassisted recursive self-improvement, the definitive trigger for an intelligence explosion, wherein the model can iteratively engineer its own code without a human in the loop.

## Synthetic Biological Intelligence and Sample Efficiency
While silicon-based Transformer architectures scale through brute-force parallelization and massive energy consumption, concurrent breakthroughs in biological computing demonstrate an alternative, highly efficient pathway to advanced intelligence. Cortical Labs' development of "DishBrain" exemplifies the integration of living biological neural networks (BNNs) with in silico computing via high-density multi-electrode arrays. In 2022, researchers successfully embedded 800,000 in vitro human and rodent neurons within a simulated environment, proving that the culture could self-organize its activity to play a simplified version of the arcade game "Pong".

The significance of the DishBrain architecture lies in its adherence to the free energy principle and the theory of active inference. According to this framework, neurons naturally strive to reduce the unpredictability, or entropy, of their surrounding environment. By successfully hitting the digital ball in the simulated game world, the cellular network minimizes its environmental uncertainty, structurally organizing its signaling activity in a goal-directed manner to avoid negative, unpredictable feedback. This represents a foundational form of synthetic biological intelligence (SBI), capable of apparent learning within five minutes of real-time gameplay, a phenomenon not observed in control conditions without closed-loop structured feedback.

When tested against state-of-the-art Deep Reinforcement Learning (DRL) algorithms, specifically Deep Q-Networks (DQN), Advantage Actor-Critic (A2C), and Proximal Policy Optimization (PPO), the biological cultures exhibited vastly superior sample efficiency. While conventional deep learning models require millions of data points and massive computational power to extrapolate complex tasks and achieve generalization, the biological neurons circumvent this requirement through intrinsic plasticity. Under conditions where data samples were strictly limited to a real-world time course, the biological cultures consistently outperformed deep DRL agents across multiple performance characteristics, including the average number of hits per rally and the relative learning improvement over time.

Furthermore, this biological system operates at a tiny fraction of the power required by conventional GPU-based AI models, directly addressing the thermodynamic reality and sustainability challenges of the singularity. The profound implications of this research have drawn significant national security interest, leading to an AU$600,000 grant from the Australian Office of National Intelligence to create a DishBrain-based AI with continual lifelong learning capabilities, a trait that current silicon-based AI cannot natively replicate. This dual acceleration, both in silicon-based parallel processing and synthetic biological active inference, confirms that the barriers to AGI are rapidly deteriorating from multiple intersecting scientific vectors.

## Timeline Compression and the 2027 Ignition Point
The convergence of these architectural and biological innovations points toward a near-term disruption that heavily contradicts the cautious projections of legacy institutions. A deep analysis of the current industry trajectory indicates that the critical tipping point for AGI, and the subsequent leap to ASI, is mathematically and analytically anchored around the year 2027. This date represents the ignition point at which AI models achieve full, unassisted recursive self-improvement, accelerating past human-level intellectual labor and exiting the human cognitive environment.

This rapid timeline is supported by the unprecedented mobilization of industrial capital currently unfolding within the tech sector. Former OpenAI Superalignment researcher Leopold Aschenbrenner's comprehensive 2024 manuscript, "Situational Awareness," details this extreme trajectory. Over a deeply compressed timeframe, corporate planning has shifted from deploying $10 billion compute clusters to aggressively structuring $100 billion and even trillion-dollar infrastructure expansions. Behind the scenes, a fierce scramble is underway to secure every available power contract and voltage transformer for the rest of the decade, resulting in a mobilization of American industrial might not seen in half a century.

Tracing the trendlines of computational scale (adding ~0.5 orders of magnitude or OOMs per year), algorithmic efficiencies (~0.5 OOMs/year), and "unhobbling" gains that transform chatbots into autonomous agents, the industry expects a qualitative leap from preschooler-level AI to smart-high-schooler-level AI, ultimately outpacing college graduates by 2025 or 2026. By 2027, hundreds of millions of AGIs could be utilized to fully automate AI research itself, compressing a decade's worth of algorithmic progress (over 5 OOMs) into a single year, thereby birthing superintelligence. This intelligence explosion introduces massive geopolitical volatility; Aschenbrenner warns that the free world's survival is at stake, framing the race to AGI as an all-out techno-capital war with authoritarian powers, specifically the CCP, to secure a decisive economic and military advantage.

The broader scientific community is rapidly adjusting its expectations to align with these empirical realities. A longitudinal survey of thousands of AI researchers published in 2024 by Katja Grace et al. revealed a dramatic, unprecedented compression in predictive timelines. Between the 2022 and 2023 iterations of the survey, expert consensus radically shifted.

| AI Milestone | 2022 Aggregate Forecast | 2023 Aggregate Forecast | Net Shift |
| :-: | :-: | :-: | :-: |
| High-Level Machine Intelligence (HLMI), 50% probability | 2060 | 2047 | 13 years sooner |
| Full Automation of Labor (FAOL), 50% probability | 2164 | 2116 | 48 years sooner |

*Table 2: Shifts in Expert Consensus on AI Timelines (Grace et al., 2024).*

The same survey put a 10 percent probability on high-level machine intelligence arriving as early as 2027. And on the darkest question it asked, between 37.8 and 51.4 percent of respondents, depending on how the question was framed, assigned at least a 10 percent probability to outcomes as bad as human extinction. These are not doomers on a forum. These are the people building the systems, surveyed by the thousands.

More than half of the surveyed experts indicated that "substantial" or "extreme" concern is warranted regarding the socio-economic shocks that will accompany this rapid technological diffusion, including authoritarian population control, worsened inequality, and the spread of false information. Despite this, the corporate march toward the 2027 tipping point continues unabated, meaning society must confront the impending obsolescence of human labor.

## The Economic Paradox: Zero Marginal Cost and Post-Scarcity
The central crisis of the Singularity is not inherently technological; it is macroeconomic and sociological. The current global economic architecture is built upon the fundamental assumption of scarcity, specifically the scarcity of human physical and cognitive labor. However, AGI threatens to substitute human cognitive labor entirely at a marginal cost of zero.

This creates a fatal contradiction within the capitalist framework. From a strict optimization standpoint, the human employee represents a business's single greatest expense, liability, and point of failure. Capitalist enterprises are structurally incentivized to automate this liability out of existence to maximize efficiency and profit. However, in a societal system where an individual's right to survival, measured through access to food, shelter, and healthcare, is legally and culturally tethered to wage labor, the total automation of the workforce without altering the social contract equates to total mass disenfranchisement.

As the marginal cost of intelligence drops to zero, the mechanism of creative destruction continues to destroy old industries, but unlike previous industrial revolutions, it no longer requires human labor to build the new ones; the "creation" phase is executed autonomously by the machine. This economic uncoupling renders traditional business cycle theories obsolete. Humanity is currently caught in a tug-of-war between the mathematical limits of a highly financialized, debt-based economy, which requires excess liquidity that triggers asset price inflation, and the powerful deflationary pressures exerted by exponential AI, which drives the value of human labor toward zero. Prominent industry figures, including OpenAI CEO Sam Altman, have recognized this, floating concepts like Universal Basic Income (UBI), Universal Basic Computing (UBC), and identity verification infrastructures like Worldcoin to distribute the wealth generated by an AI-automated economy.

The logical endpoint of this trajectory is a post-scarcity model, a concept thoroughly explored in post-capitalist theoretical frameworks such as "Fully Automated Luxury Communism" (FALC). Authored by Aaron Bastani, FALC posits that the convergence of five technological drivers, full automation of services and manufacturing, limitless renewable energy and battery storage, asteroid mining for unlimited raw materials, CRISPR synthetic biology for extending lifespans, and cellular agriculture for synthetic food, can permanently eliminate scarcity. When information, labor, energy, and resources become permanently cheap, the traditional price mechanism breaks down, decoupling use-value from market value. In such a paradigm, society possesses the capacity to dissolve the boundary between necessity and luxury, instituting a 10- or 12-hour working week, a guaranteed social wage, and universally guaranteed housing and education. Yet, transitioning to this state of abundance requires overcoming severe psychological and institutional barriers that tie human identity to suffering and toil.

---

## Precedent P-03: One Million Years, Give or Take (New York, 1903)

On October 9, 1903, the New York Times published an editorial titled "Flying Machines Which Do Not Fly." Its conclusion: a working flying machine might be developed by "the combined and continuous efforts of mathematicians and mechanicians in from one million to ten million years."

Sixty-nine days later, the Wright Flyer lifted off the sand at Kitty Hawk.

The editors were not fools. They were doing exactly what respectable analysis is supposed to do: extrapolating from the evidence in front of them, which was Samuel Langley's spectacularly public crash into the Potomac two days before. Their data was accurate. Their reasoning was careful. And their estimate was wrong by a factor of roughly five million, because they were measuring the past while two bicycle mechanics in Ohio, with no press coverage and no government funding, were building the future.

**The mechanism.** Expert timelines are autopsies of the most recent failure, not forecasts of the next success. The distance between "one to ten million years" and "done" can be ten weeks, because progress at a frontier is not a trend line. It is a door, and doors open all at once.

**The rule.** When credentialed voices hand you a comfortable timeline for AGI, remember the unit of error. It is not years. It is orders of magnitude, and history has almost always erred in the direction nobody was bracing for. You are past the event horizon. Plan like the door is already open.

**The practice.**

1. Start a timeline file. Every time an expert publishes an AI timeline, paste it in with the date and the author. Review it quarterly. Within a year you will have taught yourself, with receipts, exactly how much a confident forecast is worth, and you will stop outsourcing your planning horizon to whoever sounded calmest.
2. Plan by doors, not dates. Write down three things AI "cannot do" that would change your work or your household if they opened. Check them monthly. When one opens, and one will, you act that week, because you decided what the door means before it moved.
3. Make one asymmetric bet this month: an action that looks slightly early if the transition takes ten years, and essential if it takes two. Learning the tools, planting the garden, and cutting a fixed cost all qualify. The Times editors risked nothing on their million-year estimate. You do not have that luxury; you live here.
