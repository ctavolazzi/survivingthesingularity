# Chapter 0: The Demonstration

![Peeling red bark of a Pacific madrone (Arbutus menziesii)](/book-images/ch00-madrone-bark.jpg)

*Pacific madrone, mid-shed. It burns to the ground and comes back from the root. (Photo by and (c)2007 Jina Lee, CC BY-SA 3.0, via Wikimedia Commons)*



> *"The future is already here — it's just not evenly distributed."*
> — attributed to William Gibson, *The Economist* (2003)

The night Elijah Madrone ended three careers, he was drinking a four-dollar beer and trying to teach himself CSS.

He didn't know it that night. That's the part that still gets him. There was no black hood, no signature on a layoff memo, no severance packet sliding across a desk. There was a sticky bar top at the Bear Flag, a laptop running on 40 percent battery, and a machine on the other side of the screen that was writing code faster than he could read it.

His full name was Elijah Galen Madrone, and he'd heard every joke about it by the time he was nine. His grandmother used to walk him through the hills behind her place in Sonoma County and put his hand flat against the trunks of the madrone trees, the ones with the smooth red bark that peels back every summer like the tree is shrugging off its own skin. *That's your tree,* she told him. *It burns to the ground and comes back from the root. Remember that.* He was a kid; he didn't remember it. It took about thirty years and the end of the world as he understood it before the lesson came back around.

The other meaning of his name he'd figured out on his own, at Claypot, in his second year there, sitting in a planning meeting where a vice president explained the team's new charter using the phrase *execution surface*. Elijah had written in his notebook, in block letters, pressing hard enough to emboss the next three pages:

**MADRONE ≠ DRONE.**

He'd underlined it twice. Then he'd gone back to nodding.

---

You should know how he got there, because how he got there is how most of us got where we are: sideways, on the way to something else.

He'd grown up on a working farm, the one his grandmother's hills backed onto — dirt under the nails before he could write his name, diesel and weather and the particular grief of a season going wrong. He knew how to fix a thing with his hands. He knew what it felt like to do everything right and lose the crop anyway. That, it would turn out, was the most useful thing school ever taught him, and it wasn't school.

Before the pandemic, Elijah's life ran on three engines. He played music — bars, weddings, farmers markets, anywhere with a power outlet and a tip jar. He drew, in the hours nobody paid for. And he paid rent by driving deliveries, food and packages and once, memorably, a single helium balloon across two towns, because the machine that routed his jobs did not care what was in the bag. He had no degree that mattered and a settled belief that this was just what a life looked like now: three gigs stapled together into the shape of one income.

Then COVID hit, the stages went dark, the tip jars vanished, and delivery driving went from side hustle to frontline work in a month. And in the dead hours between routes — parked in a lot with the engine ticking, phone propped on the wheel — he started teaching himself data science. Free courses. Kaggle notebooks. Stack Overflow at two in the morning. He had a farm kid's tolerance for grinding at a thing that wasn't working yet, and by the back half of 2020 he could write a Python pipeline that did something real. Somewhere in that long blur of masked handoffs and empty highways, a recruiter found the résumé he'd rebuilt around two words: *machine learning*. Claypot was hiring, junior data roles, no degree required if you could show the work. Claypot — the company whose software he'd been using since he was a teenager pirating it to make show flyers. The company that built the tools every designer, photographer, illustrator, and video editor he'd ever shared a stage or a studio with used to make their living.

He took the job with his whole heart. That's the thing people miss when they tell this story back to him like an accusation. He went in believing it. He was a farm kid and a musician who'd taught himself to speak a little math. He thought he was going to spend his career building tools that made his friends more powerful — take the drudgery out, leave the art in. He thought he was a bridge.

And then he saw what was on the other side of the bridge.

Inside Claypot, behind badge readers and NDAs, the models were already doing things Elijah had been taught were decades away. He watched an internal demo where a system filled in the missing half of a photograph so cleanly that the researcher presenting it had to keep toggling the overlay to prove which half was real. He watched a model sketch, in seconds, in any style you asked for, including styles he recognized — styles with names attached, people attached, rent payments attached. Nobody in the room said the quiet part. The quiet part was in the training data.

He'd sit in those demos with his heart rate climbing and look around at faces that registered nothing but pleasant professional interest, and he'd think: *Am I crazy? Is nobody else seeing this?* That feeling — the vertigo of watching the impossible get a Jira ticket — became the weather of his life. It never really cleared again.

But Claypot moved like a big company moves: carefully, quarterly, with lawyers walking three steps ahead of everything. Whatever was in the labs stayed in the labs.

PorusAI had no such patience.

---

PorusAI was the other kind of company — a research lab with a messiah complex and a burn rate, the kind of outfit that published its breakthroughs like mixtapes. Everyone in Elijah's field knew the lineage by heart: in 2017, researchers at Google had published a paper with the almost taunting title "Attention Is All You Need," and quietly replaced the engine of machine intelligence. Before that paper, machines read the way you read — one word at a time, in order, forgetting the beginning of a long sentence by the time they reached the end. The Transformer architecture let a machine attend to *everything, everywhere, at once* — every word weighing every other word simultaneously — and, crucially, it let the whole process run in parallel across the biggest computers on Earth. Google wrote the physics. Then they largely sat on it.

PorusAI built the bomb.

They called the model Silvana. Someone at PorusAI with a literary streak had pulled it from the Latin — *of the forest* — which Elijah would appreciate later with something between a laugh and a chill: the machine named for the forest, meeting the man named for a tree. They wrapped Silvana in an interface so plain it was almost insulting, a white page with a text box and a blinking cursor, and they called it Chat Horizon, and one Tuesday they simply turned it on for the public.

Elijah lost most of a week to it.

He'd read the 2017 paper three times by then and understood maybe half of it — but half was enough. Enough to know there was no trick, no mechanical Turk, no sleight of hand. Enough to know that nobody was cheating. That made it worse, not better — because the part of him that hoped to catch the wires had nothing to hold. He fed it the kind of problems that had eaten whole weekends of his self-teaching and watched it dissolve them in seconds, politely, in complete sentences, at two in the morning, for free.

He did what you do when you witness something. He told people.

His housemate. His bandmates. His mother. His group chats. The response was so uniform it started to feel scripted. *A chatbot? Like the thing in my insurance portal? The one that can't find my policy number and just says "I'm sorry, I didn't understand that" until you type AGENT in all caps?*

"No," Elijah kept saying. "No, no. This is different. I'm telling you. This is *different*."

They were polite about it. That was the worst part. They gave him the look you give a friend who's just gotten into cold plunges or day trading, the *good for you, buddy* look, and they changed the subject, and the world went on pretending, and Elijah went back to the Bear Flag with his laptop, because if nobody wanted the news, fine — he'd use the miracle for himself. He was entry-level at everything that wasn't dirt or a guitar; two years of self-taught data science had given him exactly enough to know how much he didn't know. The front end — the layouts, the colors, the part of software you actually *see* — had always sat on the far side of a canyon he'd never had time to cross. So he picked it, of all the canyons, to cross first.

So he sat at the bar, night after night, and had Silvana walk him across. *Explain flexbox to me like I'm a drummer. Why is this div doing that. Fix it. Now make it beautiful.* Code poured down the screen in ribbons and the canyon closed under his feet, and he was so busy being delighted that he never once looked up to check who was watching.

The realtors were watching.

---

There were three of them, at the corner of the bar, in the blazers realtors wear so you know they're realtors. They'd been having some low-grade argument about a listing when one of them — silver-haired, big class ring, the clear alpha of the trio — leaned over toward Elijah's screen with the frank nosiness of a man who has knocked on ten thousand strangers' doors.

"What is that?" he said. "What are you doing there?"

Here's the thing about that question. The man knew what code looked like. Every realtor who'd survived two decades of the internet had, at some point, paid a guy to build a website, and had stood behind that guy at least once while he typed. He had seen code get made the way you see food get made at a hibachi place — theatrically, one line at a time, by a professional you are paying by the hour.

He had never seen it *appear*. Whole functions, blooming out of nothing, faster than anyone could type, while the man in front of the laptop just sat there sipping a beer with his hands nowhere near the keys.

And Elijah — God help him, he'd been waiting a month for a single human being to ask — Elijah went off.

He turned the laptop toward them like he was turning an altarpiece. He told them about the paper from 2017, the one out of Google with the wild title, and what attention meant when a machine did it. He told them about PorusAI and Silvana and the blinking cursor at the edge of Chat Horizon. He showed them, live: asked the machine for a webpage, and there was a webpage; asked for it in Spanish, and there it was in Spanish; asked it to explain a contract clause, draft a listing description, write a polite-but-firm email to a difficult seller, and it *did*, it just *did it*, each time, in seconds, while the ice melted in their drinks.

"This is the most incredible thing I have ever seen in my life," he told them, and his voice was shaking a little, and he didn't care. "It's doing things I spent two years clawing my way toward. Things I taught myself in parking lots between deliveries. Everyone thinks it's a toy. It is not a toy. I'm telling you — this changes everything for people like you."

They asked good questions. That surprised him. Commission-brained people are learning machines in their own right; show them leverage and they will interrogate it like a home inspection. How much does it cost. What's the catch. Can it do contracts. Can it do the MLS.

And then Elijah said the sentence.

He'd replay it later, the way you replay the moment before a car crash, looking for the exact frame where it all went wrong, and it always came down to this — him, lit up with missionary joy, sliding a bar napkin with his email address across the wood:

"If you ever want help figuring out how to use this stuff — for your workflows, whatever — reach out. Seriously. I'm happy to help. I just want people to see what's coming."

*I just want people to see what's coming.*

He thought he was handing them a telescope.

The silver-haired one took the napkin, read it, folded it into his breast pocket, and bought Elijah a beer. "Interesting," he said. "Very interesting." And the three of them went back to their corner, and Elijah went back to his flexbox, feeling, for the first time in a month, a little less alone. Somebody had finally *listened*.

---

One week later, almost to the hour, he was on the same stool when a hand landed on his shoulder like a gavel.

"There he is! The man himself!" The silver-haired realtor was beaming — the full open-house smile, the one that sells the granite countertops. His colleagues flanked him. One of them was already flagging the bartender. "Whatever he's drinking, and one for us. This guy," he announced, to the bar generally, "this guy right here saved me *so much money*."

Elijah smiled and stood up into the handshake, and some part of him began, quietly, to brace. "Yeah? You got into Chat Horizon?"

"*Got into it.* Brother. We *live* in it." The realtor squeezed his shoulder. "I've got to be honest, when you showed us that thing I thought, okay, neat trick. Then Donna spent a weekend with it." He shook his head, marveling, a man describing a fish he'd caught. "The emails. The listings. The social posts, the flyers, the market updates, the follow-ups. It does *all* of it. Better than — " and here he laughed, actually laughed, " — honestly? Better than the people we were paying to do it."

"Were," Elijah said.

"Hm?"

"You said the people you *were* paying."

"Oh." The realtor waved a hand, easy, unbothered, a man closing a chapter that had already stopped mattering to him. "Yeah, we let three folks go this week. Our transaction coordinator, our marketing gal, and the kid who did our listing videos. Good people, don't get me wrong. But the numbers just don't — I mean, you *saw* what it does. You showed us!" He raised his glass. The other two raised theirs. "To Elijah!"

Three glasses up, catching the neon.

Elijah's arm lifted his own glass because forty years of social training will run the body without any help from the soul. He heard himself say something. The beer was cold and tasted like nothing.

The kid who did their listing videos. Elijah didn't know him. He knew him completely. He'd been him: some twenty-something with a camera and a laptop full of cracked software and a rate he was embarrassed to quote, stringing together realtors and restaurants and the occasional wedding into the shape of one income, telling his parents it was all going to compound into something. That kid had lost his anchor client this week and didn't know yet what Elijah knew, which was that it wasn't a client, it was the tide.

And standing there with the glass at his lips, Elijah ran the numbers he was uniquely, miserably qualified to run. There was nothing special about these three men except that they'd gotten the demonstration early — and he had given it to them. They weren't villains. That was the terrifying part. They were ordinary rational actors doing the ordinary rational thing, one week after first contact. Nobody had needed to train them, sell them, onboard them. The learning curve from *what is that* to *we let three folks go* was seven days, and the only input required had been one enthusiastic idiot with a laptop who wanted people to see what was coming.

He'd gotten one thing right, at least. They saw.

His mind went where it would live from then on: down the list. Every graphic designer he'd ever split a bill with. Every session player, every wedding photographer, every copywriter, every voice actor, every friend who'd ever cobbled a living out of the exact set of tasks he had just watched a text box perform for twenty dollars a month. People for whom the economy was already a rigged carnival game. People with no margin, no cushion, no lobbyist — the first people every wave hits and the last people anyone rebuilds for.

The realtors were not going to hire anyone to manage the machine. Nobody was going to hire anyone to manage the machine. That fantasy died at the Bear Flag between one round and the next. They were going to use the machine to replace everyone it could replace, as fast as it could replace them, and the machine was getting better every quarter, and he knew — he had *seen the roadmaps* — how much better, how much faster, this was going to get.

It was the most significant thing that had ever happened in his lifetime, and it had just happened *to* his own community, *through* his own hands, in a bar, to a toast.

"You okay, chief?" the silver-haired one asked. "You look a little pale."

"I'm fine," Elijah said. "Congratulations on the — yeah. Congratulations."

---

He didn't remember the drive home. He remembered the kitchen table, the laptop open, the hour — 1:40 in the morning — and the cursor blinking on a blank document, patient as the tide.

Years before, a bass player had lent him a paperback about generational cycles — how history moves in long waves, and how every eighty-some years the wave breaks: institutions fail, the old order comes apart, and whatever's standing when it's over builds the next world. The book had a name for that breaking. A turning. Elijah couldn't remember, at 1:40 a.m., whether the crisis was the fourth turning or the fifth, and he was never going to find the paperback in this apartment, but he knew — with the same cold certainty he'd felt watching the demo that filled in the photograph — that he was standing inside one. That the wave had already broken, in a bar, over a beer, to applause, and almost nobody had heard it land.

He didn't have a plan. He wants that on the record. He was not an economist, not a policymaker, not anybody's idea of a prophet. He was a farm kid with a delivery route and two years of self-taught data science who'd wandered into the engine room of the new world and watched, in real time, what one week of it did to three ordinary jobs in one ordinary town.

But he'd spent his whole life making things when he didn't know what else to do. So he did the only thing he knew how to do at 1:40 in the morning with shaking hands.

He started to write.

At the top of the blank document he typed a title, a working title, the kind you put down just so the page isn't empty anymore:

**LIVING THROUGH THE FOURTH TURNING**

It would take another name, eventually.

You're holding it.

---

*The rest of this book is the manual Elijah wished someone had handed him that night at the Bear Flag — what's actually happening, in what order, and what people like us can build while it does.*
