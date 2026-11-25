# v5 edits: the running list

Running list, started 2026-11-25. These are CT's edits to the v5 manuscript (Google Doc "StS v5 draft (Nov 23)").

**Edits 1 to 86 are done: all of them are in the Doc as suggestions, waiting for CT to accept them.** Checked
2026-11-25 against a fresh read of the Doc; the edit-by-edit record is `EDITS-v5-applied.md`. New edits start at
87 and go in "New edits" below. The publication files (`publication/novel/build/build.sh`) have not been rebuilt.

**So nothing gets dropped:** every edit has a check row in `manuscript/tools/edits-v5/checks.py`. Run
`python3 manuscript/tools/edits-v5/verify.py READ.json --table manuscript/novel/EDITS-v5-status.md` on a fresh
read of the Doc after every step; `EDITS-v5-status.md` is the one table of where each edit stands. The build
refuses to run unless every edit passes. A copy of this list lives in Google Drive as "StS v5 edit list (mirror of
GitHub)" (https://docs.google.com/document/d/1YIxK_1g68UoFJs00cCAbdsGOMaEMvDM9ojj5XnNs7tM); refresh it when this
file changes. Each new edit gets a check row when it is logged.

## Character notes from CT (context, not for the page)

- Elijah, 2026-11-25: "It makes sense that people think he's just some punk-ass rich kid with a bone to pick with
  the world. And from a certain perspective, he kind of is. But from his perspective, he's just trying to
  demonstrate that he cares in all the ways he was told that he didn't." Also: "somebody who was falsely accused of
  being a piece of shit and spent his whole life trying to prove otherwise."
- Gus expected Elijah to say no to the show, which is why he lets the loneliness slip (edit 65).

## Direction from CT, 25 Nov: stakes and personality conflict (context, not for the page)

Given after edit 136, at the end of Chapter 19. Nothing below is an edit yet. The plan is written ("The plan for
Chapter 19", below the first thinking); on CT's go it was carried out in edits 131 to 137.

CT: "at the beginning here, we have everything sort of centered around perspectives and viewpoints, but we haven't
introduced any sort of like cross-character consequences. The stakes are so low, and we haven't raised them at all
... this big delivery of these products, it's sort of like glossed over. It's just like, oh, and then they did it.
But like it could have been an opportunity to talk about like the struggle of the old way of doing things, and then
Elijah's just like, wait a minute, I can just use AI for this. And so he does. But then he realizes, because of some
kind of foreshadowing, that even though this is a solar punk farm where they are friendly to this type of thing ...
If he tells people that he just used AI to generate it, Priya's going to have a problem. Somebody else is going to
have a problem. Like we haven't done I don't think a very good job of introducing personality conflict into this
manuscript."

**Claude's first thinking (25 Nov, kept for the record; the plan below it replaces it where they differ):**

1. Where the gap is. From Chapter 22 on, things Elijah does cost other people: the leak he has to confess (Ch 22),
   the retreat plan voted down and the tea circle (Ch 31), the arms meeting where Wren cries (Ch 34). Chapters 16 to
   21 are lessons: somebody corrects him with a story, and nothing he does lands on anyone else. CT is in that
   stretch now.
2. Chapter 19 already holds the pieces. Since edits 131 and 132, Elijah used an AI on the board himself, and in the
   Rod Code scene Tyler, nineteen, takes the customer's anger for doing the same thing while Elijah stands there
   with a deburring tool. If Elijah kept the board AI quiet, that silence stops being indecision and becomes a kid
   paying for Elijah's secret, in front of the buyer of more than half of Lou's crop. Grace's "You picked nothing"
   lands harder, because she doesn't know the half of it.
3. Raise the stakes on the order itself. The book says the network buys more than half of what Lou grows only
   after the fight (Grace, at the wash station). Said when the order comes in, the forty boxes are a risk to Lou's
   living, and Curtis's "what happened if they couldn't deliver" (edit 125) has teeth. The first design burns
   time (Marta's eleven weeks); laying out a second board the old way would take weeks he doesn't have. That is
   the struggle, and the reason he reaches for the AI.
4. Who would have the problem. Pushback on Priya as the one who hates it: in Chapter 21 she asks "What did it
   learn from?" and wants help searching her plant-disease references. Her line is provenance and proof, not
   hatred. The people the book already gives a reason: Curtis ("wanted nothing to do with any of it," Ch 21;
   Judgment Day, Ch 17), Denny (the arms took his warehouse), Marta (zero people can fix it), and Wren, who the
   reader meets in Chapter 20. Each minds for a different reason, which is the personality conflict.
5. The secret needs a bill. Options: he tells Tyler on the bumper the night they read the firmware (edit 136);
   Marta or Grace finds out; or it stays buried until Chapter 22, where he takes another quiet shortcut ("just to
   rule it out") and this time rings the bell and confesses. The last makes Chapter 22 the second time, not the
   first, and shows the growth.
6. Conflict between the members, not only with Elijah. The book has frictions that stay polite: Marta and Grace
   on how to treat him (the broom against "Grace will carry you"), Curtis against everyone on machines, Priya
   against Denny on saying a thing before it is measured (edits 90 and 103), Grace and Curtis ("Curtis, not
   now," edit 109). Cheaper to let two or three of those cost something than to invent new ones.
7. What it touches. Edits 131, 132, 133, 135 and 136 would be reworked, not stacked on. CT has said the book is
   long enough, so this should replace telling ("The forty units shipped in June") rather than add pages.

### The plan for Chapter 19 (Claude's, written 25 Nov at CT's request)

**Status:** done. CT: "Go on the plan." Edits 131, 132, 133, 135 and 136 below were reworked in place to it, and
edit 137 is its Chapter 22 line; the contradictions pass then corrected 131, 136 and 137 (noted under each). CT on the outline in chat: "Okay, I think this is stronger," then:
"this is the first real opportunity for conflict among the crew, and I'd like it to be handled carefully with all
of the lessons that we've learned so far ... this is literally the midway point of the book, and it needs to keep
and hold the reader's interest and set things up for the end." Everything in this plan is Claude's unless it is in
quotation marks.

#### 1. What the book already has (25 Nov read of the Doc)

The ending leans on this scene already. Nothing below needs a new page later in the book.

- **Patricia is hiding the same thing.** At Thanksgiving (Ch 38) she says: "I've used it every day for three
  years. Every report. Every grant. I'd have lost the job in 2025." Chapter 19 is spring 2025, so she is using it
  when she goes after Tyler. The plant is in the scene now: "she kept her phone face down on the bench beside her
  the whole time." It is face down again in Ch 31 and Ch 34, and face up in Ch 38.
- **Her confession is Elijah's silence, said out loud.** Ch 38: "I used it and I still think it's wrong. Both of
  those." Ch 19: "Elijah thought they were both right. That was his excuse."
- **Tyler is the one who keeps secrets.** Ch 26, when the models go dark and he works out Patricia's: "He never
  said a word about what he'd figured out. He was twenty. He just put it away." Ch 38, to Patricia: "You could
  just tell them." and "I wasn't going to say anything."
- **Tyler cannot read his own code, and the book saves that for Ch 26.** "I can't read it. I told Patricia I read
  all of it. I read it like you read the terms on an app." Then Elijah pulls a stool over and they read the
  gantry's code line by line for ten days, with two coffees every morning.
- **Patricia's two questions are Marta's numbers.** Marta, on the first design: one supplier, and zero people in
  the valley who can fix it. Patricia, in the shed: "how many companies make Rod Code?" (one) and "how many people
  in this shed can read what it wrote?" That is why "Something had gone out of her face."
- **"Nobody asked" runs through the chapter.** Tyler's cases: "Nobody had asked him to." Reuben: "Nobody asks
  Reuben." Patricia: "Nobody asked them." It ends at the Architect's "It asked." (Ch 33).
- **Who has what riding on the order.** It came "through a friend of a friend of Priya's." The network "buys more
  than half of what Lou grows." Grace walks Patricia down the line, proud of them.
- **The next chapter already shows the bruise.** Ch 20: "the tractor's broke ... and Curtis is in a mood." Curtis
  and Lou trade the Matrix lines. Ch 34: Curtis "told everybody the very first night that laptop people show up
  and bring their friends."
- **The controller's paperwork has two mistakes later.** Ch 21: the repair card "named the wrong terminal." Ch 27:
  "One connector label in the controller drawing was wrong." They read differently once the reader knows who drew
  the board.
- **Chapter 22 is the same sin, bigger.** A quiet shortcut ("just to rule it out"), then: "He thought about
  keeping it to himself. Then he pictured Marta finding out some other way." Priya: "we took his confidence for a
  check."
- **The fights get bigger from here.** Ch 22 (the leak), Ch 31 (the vote), Ch 34 ("It was two arguments, and then
  it was four"), Ch 38 ("three tables now, at one table"). Chapter 19 is the first crack, so it stays the smallest.

#### 2. The idea

Three people in the shed have used an AI. One of them is nineteen and says so. The two adults keep quiet and let
him take it, one from each side of the argument. The reader knows about Elijah now and learns about Patricia at
the end, and the Chapter 19 scene turns over in their memory when they do.

That makes the midpoint a win with a debt inside it. The boxes ship and Elijah fits in for the first time (edit
127). He paid for it with the oldest habit he has: "he learned to read a room and make it like him" (edit 94).
CT's note on him holds: he is not cunning. He is a man who was told he was a piece of shit and has just found a
table that likes him.

#### 3. Narration (CT, 25 Nov)

CT: "whose feelings? Elijah's and his observations of others. BUT ... we have a hybrid narration style going on
here." The book sits on Elijah's shoulder, and above him is a storyteller who knows more than he does ("Although
Elijah was quite unaware of it," edit 106), leaves him (the kitchen trailer in Ch 17, Bidwell, Ch 38), goes into
other heads (Tyler in Ch 26, Grace in Ch 38) and talks to the reader ("Most people never do, at moments like
that," edit 100).

How the rework uses it:

- The fight stays on Elijah's shoulder. His silence is the event, so the reader has to be inside it.
- The others' feelings come through what he sees them do: Marta's crimper not moving, Grace's hands coming down,
  Lou setting something on the bench.
- The storyteller steps in twice, briefly, for things Elijah cannot know: that the network buys more than half of
  Lou's crop (said before the fight, so the reader watches him stand there without knowing it), and that Tyler
  knows about the board and is choosing not to say so.
- No scene leaves Elijah. Grace and Patricia at the car stay seen from the shed door. Going over there would make
  the storyteller either give Patricia away or visibly hold back.
- No new hint about Patricia. The phone is enough (edit 109's lesson: a seed, "not gone into hard").

**Open, for CT:** whether Chapter 19 should leave Elijah for a scene. This plan says no.

#### 4. Edit by edit

**Edit 131, the second design. Book now: "So he designed it again."** Becomes a short scene in four beats:

1. *The clock.* The first design cost him the weeks he had. One sentence from the storyteller gives Lou's stake
   here; Elijah still doesn't know it, so Grace's line at the wash station and "He hadn't known that" stay.
2. *The old way.* He starts the plain board by hand. Continuity: he laid out the four-layer board himself, so the
   trouble is not that he can't. It is time, and that the parts are now from the drawer and the hardware store:
   relays out of a coffee can (edit 124's drawer), measured with calipers, drawn one at a time. He loses a weekend
   and has a third of a board.
3. *CT's beats, in his words:* "a startup out of Iowa," the rabbit hole where he is lost, "came up for air," "Did
   he actually need to know all this?", "remembered his training," the minimum viable product, "got to work." The
   board is done in a night.
4. *The foreshadowing lands.* Marta's three numbers are still on the whiteboard, with the order pinned beside them
   (edit 125). One company makes the thing that drew his board. Zero people in the valley can read why it put a
   trace where it did, and he is one of the zero. A page earlier Marta asked him to "spend a little more time
   making this feel more like us than like Claypot" and told him "You're a good engineer. I mean it." He doesn't
   mention Iowa. Then he blocks out two weeks to write the firmware himself, by hand, to make up for it.

   Then "The second version was a Raspberry Pi..." as before.

**Edits 132 and 133, his silence in the shed.** Same two paragraphs, every fact and name kept (the $2,011.46 bill,
Kelsey, Carol, Mateo, the deburring tool, "both of them noticed"). What changes:

- "They were both right" is still his excuse. The board is the real reason, and the paragraph says so (132).
- "what would have taken him two weeks" now means the two weeks he set aside to do it honestly. A kid did it in a
  night with the same kind of tool and said so cheerfully.
- Patricia's two questions land on him as Marta's two numbers. He ran them on himself already, at the whiteboard.
- Tyler looks down the line at him once. The storyteller tells the reader what Elijah doesn't know: Tyler has seen
  the board's files, with the Iowa company's name at the top. To Tyler it was never a secret, it was a file ("Why
  wouldn't I?"). He sees Elijah's face, understands, and doesn't say it. Nobody asked him to.
- Sentence openings varied, as edit 133 already does.

Edit 134 ("Marta hadn't said a word either, not since Grace walked Patricia down the line") stays as logged.

**Edit 135, the end of the shed scene.** Marta's question, "I'd have to look," "Look," Tyler scrolling, "We'll
see," Patricia leaving and Grace going to the kitchen trailer all stay. Two things change:

- *The first crack in the crew,* after Grace is in the trailer and before Elijah finds Tyler outside. Six to eight
  lines of dialogue, every speaker named. It is not the argument about AI again (CT cut that once, edit 131). It
  is about what to do with forty boxes, and it is between the members:
  - Curtis goes at Tyler: throw the code out, write it by hand.
  - Lou tells Curtis to lay off the kid. It is Lou's buyer and Lou's date. (His pears stay in Ch 20.)
  - Priya, whose friend of a friend sent the order: don't believe it and don't burn it, test it, and write down
    what fails.
  - Somebody turns to Elijah: you're the engineer, is the kid's code good? He can't vouch for it, because he
    hasn't read it. He can't condemn it, because of the board. He gives them Tyler's own words back: it passed the
    bench. It is the second time that morning he picks nothing.
  - Marta ends it with the work, not a verdict. Her "We'll see" is still the only yes anyone gets.
  - Tyler takes his laptop and a crate of units outside. That is now why he is on the trunk of the Corolla.

  Not in it: Wren (the reader meets her in Ch 20), Grace (in the trailer), and any speech.
- *The trunk.* Elijah's half-confession stays ("I showed an AI to some realtors once. In a bar."). Tyler's "Okay"
  stays. Then Tyler says he knows about the board, and one line more: Elijah could have just told them. (Ch 38,
  Tyler to Patricia: "You could just tell them.") Tyler doesn't ask what happened with the realtors. He is
  nineteen and has twenty-six boxes to go.

Grace at the wash station is the book's, unchanged. She says "You had both halves of it in your head." He had
three, and he doesn't tell her either.

**Edit 136, the night, and June.**

- One line after "You picked nothing.": he had picked, and he knew what.
- The night scene stays (yard light, nineteen boxes to go, "Marta's question"), but they answer it **by test, not
  by reading.** They pull the probe's wire on a unit and watch: the valve opens and stays open. "Shit." Tyler asks
  Rod Code for the fix and gets four lines. They test it again: valve shut, light blinking. Neither of them can
  say why the four lines work, and Elijah, of all people, can't object. The card line and Marta's laminator stay.
  Marta's zero is still zero, and the storyteller can say so in a sentence.
- Why: as logged, 136 has them read the firmware "all of it this time, line by line." That is the Chapter 26
  scene, a year early, and it takes the weight off Tyler's "I can't read it." No coffees here either; Ch 26 has
  them.
- June: the paragraph "The forty units shipped in June. An electrician the CSA hired ... two growers ran the first
  boxes for a week" keeps its facts and gets a cause. They are what Patricia asked for at the car, the price of
  keeping the order. "Two probes died in the first month. Both valves failed shut." stays (edit 136, change 2).

#### 5. What each person carries out of the chapter

| Who | What it costs |
|---|---|
| Tyler | Takes the customer's anger alone, then Curtis's. Keeps Elijah's secret without being asked. |
| Lou | His buyer saw a fight in his shed. He crosses Curtis over a kid. |
| Curtis | Loses the argument. "In a mood" by Chapter 20. |
| Priya | Her name brought the order in. She wants a test and gets a "We'll see." |
| Marta | Her rule is broken twice in her own shed, and she knows about one. She has just told him he is a good engineer. |
| Grace | Her warm voice fails in front of her friend. She uses the other one on Elijah, and gets half an answer. |
| Patricia | Nothing yet. Her bill comes at Thanksgiving. |
| Elijah | Owes a nineteen-year-old. Has lied by leaving things out to Marta and Grace. The belonging he just got is resting on it. He has been wondering what Curtis and Grace agreed on (edit 127); now he is the one in the line with a secret. |

#### 6. Later chapters

Pays off with no change: Ch 20 (Curtis's mood; Lou and Curtis), Ch 21 (the wrong terminal), Ch 22 ("That's
Patricia's argument." / "I know. I stood there while she made it."; "we took his confidence for a check"), Ch 26
(Tyler can't read it; "Elijah knew that face"; Tyler puts Patricia's secret away, the second one he has kept),
Ch 27 (the pledge, the wrong connector label), Ch 34 (the leaf), Ch 38 ("You could just tell them"; "Both of
those").

To decide when CT reaches them, nothing made now:

- **Chapter 22, where Elijah tells it.** Recommended: at the bell, in a line or two, with Tyler in the room. If he
  confesses the leak and still hides the board, the book's first honest confession is half of one. The other
  place is Chapter 32, the page of small failures with the rubber band.
- **Edit 125** (the co-op's reactions to the order) and **edit 127** (the build) stand as logged.

#### 7. Lessons from edits 1 to 136 that the rework has to follow

- Take the reader through what is felt, not through the events (edit 100).
- People do the work, not objects (edit 127).
- Always clear who is speaking and who is in the room (edits 102, 109, 111).
- People get drawn out; they don't make speeches (edit 90).
- A seed, not a speech (edit 109).
- Never the same argument twice (edit 131, the cut).
- Marta is hard and kind in the same breath (edit 124). Her disappointment costs more than her anger.
- A chapter ends on something that moves the story (edit 136).
- A short line that would confuse out of context gets a little redundancy (edit 134).
- Vary the sentence openings (edit 133). No "suddenly" (edit 94).
- CT's words first, Claude's marked, his context never on the page.
- Check every later line that points back (the continuity pass).
- Replace telling with scenes. The book is long enough.

#### 8. Length

Claude's estimate: about one page added. The crew's argument and the longer trunk scene add; the June paragraph
turned into cause, and the reading cut from the night scene, give some back.

#### 9. Open for CT

1. Go, or changes.
2. Leave Elijah for a scene, or stay with him (section 3).
3. Tyler's line on the trunk, the one that sets up "You could just tell them." CT's wording if he has one.
4. Who puts the question to Elijah in the crew's argument: Priya, Lou or Curtis.
5. Where the secret comes out: Chapter 22 or Chapter 32 (section 6). Not needed for the rework.

#### 10. On go

Rework 131, 132, 133, 135 and 136 in place, one at a time, each with "Book now" and "Change to," its check row
updated in `manuscript/tools/edits-v5/checks.py`, verify run, commit and push. Then edit 137.

## New edits (from 87)

Not in the Doc yet. Same rules as below: [CT] is his wording, [Claude] is Claude's.

### Chapter 17: Twice Certified

87. The opening line, "For three weeks nobody asked him anything.", becomes:

    > For three days, no one really asked him anything. They let him settle. They fed him. They had discussions
    > about him behind closed doors, and he caught pieces of them through the wall of the kitchen trailer.
    >
    > "He looks thin."
    >
    > "Is he eating?"
    >
    > "Are we really sure this is a good idea?"
    >
    > "Do you actually believe he's just some guy who made a video or two?"

    Then "He had a cot in the room over the pump house..." as before. [CT: three days, they let him settle, they fed
    him, discussions behind closed doors, and the four lines. Claude: "and he caught pieces of them through the wall
    of the kitchen trailer", so the reader hears them from where Elijah is.] Left as is: "three weeks after he
    picked up the broom" at his first Friday dinner, a few paragraphs on; the co-op talked about him for three days,
    and he still waited three weeks for Friday.
88. How the arms get north (CT: how do they know anything about his life; he would have asked permission; they
    wouldn't just show up). What the book already has: Grace saw his public post ("Anybody have a dry corner for two
    robot arms? Can't pay much. Can work.") and offered the shed in her first email ("Your arms can live there for
    free while you figure it out."). Nobody up north knows about the lien sale. So Elijah asks, and tells them.
    "The arms came up that first week, the day before the lien sale. Somebody had a flatbed..." becomes:

    > On the fourth day he asked Grace if the dry end of the shed was still free. She had offered it in her first
    > message, after she saw his post about the arms. He told her the rest of it: two crates in a storage unit off
    > Highway 99, a lien sale at the end of the week, and nothing to pay it with.
    >
    > The arms came up the day before the lien sale. Somebody had a flatbed...

    and the paragraph goes on as before (the table voting to cover the unit as a loan, the crates in the dry end of
    the equipment shed). [Claude's wording, from CT's question. "On the fourth day" follows edit 87's three days.]
    Corrected 25 Nov (third logging chat): "her first email" became "her first message". The shed offer is in
    Grace's message in Chapter 15; her email from April is the one he opens at the food bank (edit 100).
89. The Sunday calls on the pump house steps, and how he meets Lou (CT: the calls are 9:40 on Sunday mornings, as
    changed in edit 30; the farm lets him be; a fan comes up and tries to talk to him, and one of them shoos the
    fan off, and that's how he meets Lou). Edit 30 already changes "The night aide held the phone" to "The aide
    held the phone" here; that is in the Doc as a pending suggestion. The paragraph "On Sundays at 9:40 he sat on
    the pump house steps and called the place with the rose garden. The aide held the phone by his mother's ear.
    He told the radio about his week." gets a new last sentence and is followed by:

    > ...He told the radio about his week. The co-op let him be.
    >
    > The second Sunday a man he didn't know came up the gravel with his phone already out. He had seen the video.
    > He wanted a picture, and he wanted to ask about the list, and he started in before Elijah had hung up.
    >
    > A sunburned man of about sixty set a bucket down by the pump house and walked over. "He's on the phone with
    > his mother," he said. "Go on, now." The man went. The sunburned one picked his bucket back up.
    >
    > "Lou," he said, and went back to the beds.

    Knock-on, at the first Friday dinner: "...without once looking at his hands. That was Lou. Lou ran the growing
    side, which meant the actual food." becomes "...without once looking at his hands. It was Lou, from the pump
    house steps. Lou ran the growing side, which meant the actual food."
    [CT's beats. Claude's wording. Lou's look (about sixty, sunburned) is taken from his description at the dinner.]
90. The first Friday dinner: they have to coax the horse ranch story out of him (CT: after everything about the
    horses, he wouldn't just go off on these people; they goad him: we read your stuff, we like you, we watch your
    videos, there's a reason you're here, just tell us your thoughts; Grace steps in, and Lou and Marta; Priya is
    looking forward to arguing; Denny is really trying to get him to talk; Lou puts a foot down, "only if you're
    comfortable", echoing Grace; Elijah thinks about it; "Well," begrudgingly, "imagine you run a horse ranch";
    Denny: "I like him already"; Elijah is taken aback; "This was the first warm, safe camaraderie he'd felt in a
    long time.").
    The dinner runs as before through Elijah's definitions, Lou's "What's it eat?" and Priya's "What would you
    measure?", up to "Nobody said anything for a second. The dog sneezed." Then "'I've got a story about it,' Elijah
    said. 'It's kind of dumb.' / 'Good,' said Denny. / 'Okay. Say you work on a horse ranch. Every morning your job
    is..." becomes:

    > "I've got a story about it," Elijah said. "It's kind of dumb." He looked at his plate. "I don't know. I'm kind
    > of off telling it."
    >
    > "Come on, man." Denny leaned in. "We read your stuff. We watch your videos. We like what you put out there.
    > There's a reason you're here. Just tell us what you think."
    >
    > Priya took the pencil from behind her ear, like somebody pulling a chair up to a fight she had been looking
    > forward to.
    >
    > "Denny," Grace said. "Only if he's comfortable."
    >
    > "Let him eat first," Marta said.
    >
    > Lou didn't look up from his walnuts. "Only if you're comfortable," he said.
    >
    > Elijah thought about it.
    >
    > "Well," he said, begrudgingly. "Imagine you run a horse ranch."
    >
    > "I like him already," Denny said.
    >
    > Elijah was taken aback. This was the first genuine camaraderie he'd felt in a hot minute. He noticed his
    > shoulders relax a bit.
    >
    > "Every morning your job is to make sure the horses have enough to eat. One day you walk out to the stable..."

    and the story goes on as before. [CT's beats and lines: Denny's push, "Only if you're comfortable", "Well,"
    begrudgingly, "Imagine you run a horse ranch", "I like him already", "This was the first genuine camaraderie he'd
    felt in a hot minute. He noticed his shoulders relax a bit." (CT's final wording).
    Claude: placing it right before the horse story, where the reluctance belongs; Elijah's "I don't know. I'm kind
    of off telling it."; Priya's pencil; Marta's "Let him eat first". This replaces the earlier draft of edit 90,
    which put the coaxing before his definitions; Lou is introduced at "What's it eat?" as in edit 89.]

### Elijah's father, and why he turns down the money (Chapters 0, 8, 10)

CT, 2026-11-25: Elijah turns down the money because of his father. His dad worked hard his whole life, made smart
investments (not prolific, not an early Google investor; a friend helped him play the market well), and retired
from the utility company with a good pension, back when they still gave those, so he was retired for most of
Elijah's life and they had a lot of good time together. He always told Elijah never to take a handout: "You gotta
work hard for every penny"; "The hand that feeds you controls you, remember that. So at least pick someone kind to
work for." Ironic, since he lived on a pension. When the woman says "Trust no one", Elijah remembers his father,
and that is why he says no to Ruby. Foreshadow it where the book first introduces him, and have a friend say "Man,
I sure wish I could get a handout. Every month I feel like I'm barely getting by."
What the book already says about him: he got sick (the star thistle summer), died about ten years before the
story, watched Iron Derby with Elijah, and is Melody's father. Nothing below contradicts that.

91. Chapter 0. After the paragraph "Elijah had grown up on a working farm in Sonoma County... That, it would turn
    out, was the most useful thing he ever learned." and before "Before the pandemic, Elijah's life ran on three
    engines.", add:

    > His father worked his whole life, and he worked his ass off. He had a career at the utility company and a
    > friend who helped him play the market well. He was never rich. He was no early Google investor. But he made
    > smart choices, and when he retired he got a good pension, back when they still gave those. He was retired for
    > most of Elijah's life, so the two of them got a lot of good time together, out on the farm and in front of the
    > TV.
    >
    > He told Elijah the same thing for twenty years. "Never take a handout. You work hard for every penny you get in
    > this life, son. The hand that feeds you controls you. Remember that. So at least pick someone kind to work
    > for." It was a long time before Elijah noticed that this came from a man living on a pension.
    >
    > He said it once to Wes, in the van after a gig, splitting a tip jar three ways. Wes laughed. "Man, I sure wish
    > I could get a handout. Every month I feel like I'm barely getting by."

    [CT's facts and lines. Claude's wording; the friend is Wes, the band's flyer maker, who is barely getting by in
    the book, and the tip jar is the band's. "In front of the TV" points to Iron Derby in Ch 11.]
92. Chapter 8, the whisper at the coffee urn (edit 45). After "Trust no one. Don't take the golden handcuffs." and
    before "She backed up, looked him right in the eyes, and nodded.", add: "For a second it was his father's voice.
    The hand that feeds you controls you." [Claude]
93. Chapter 10, after he turns down the million (edit 63). The paragraph "He didn't know why he listened to her and
    not Ruby. ... He was always someone who had trusted his gut." gets a last sentence: "And there was his father,
    plain as the kitchen table: never take a handout. A million dollars to do nothing was the biggest handout anyone
    had ever offered him." [Claude, from CT's "that's why he decides not to take it".] CT: "Same thing for the next
    opportunity" (Gus, Ch 11) needs no line.

### Chapter 8: Elijah Madrona

96. At the conference (the event Ruby got him into), before the woman at the coffee urn. After "They would not stand
    near each other. ... It was like a wedding where the families had already been to court." and before "A woman
    was next to him at the urn, filling a paper cup.", add:

    > Across the hall two young women were looking at him. One leaned in and whispered something to the other, and
    > they both laughed and looked away, and then looked back.
    >
    > He thought about going over. He was no stranger to that kind of look. His days as a musician had been a lot of
    > fun.
    >
    > But after the last relationship he was in, he had decided that at this point in his life he was looking for
    > forever, not just tonight. Not that tonight couldn't turn into forever. But he didn't feel like getting
    > entangled in a city he barely knew. At least, not today.
    >
    > He went to get a coffee.

    [CT's beats and most of the words, including "His days as a musician had been a lot of fun." and the forever
    lines. Claude: the first paragraph's wording and "He went to get a coffee.", which walks him to the urn. Not a
    womanizer, per CT. The last relationship is the one he remembers in Chapter 13 (edit 69).]

### Chapter 12: The Seventeen-Dollar Shower

97. The seventeen-dollar shower becomes a short scene (CT: he searches online for somewhere to shower and sees in a
    Reddit thread that you can sometimes use truck stops; he asks the PorusAI thing that started all this, "where can
    I take a fucking shower right now?"; it answers in classic AI language, "Oh man, sounds like you need a quick spot
    to get clean. I hear you. And honestly? That's brave."; he hated the way it talked, sometimes, but goddamn was it
    useful; it told him about the truck stop nearby; there was a shower; only problem? it was seventeen goddamn
    dollars; it had been a minute, so he forked over the money to the other machine, not the one in his pocket).
    In the paragraph that starts "'We'll sort you out Friday,' Trent said, the first Friday.", the last two
    sentences, "A shower at the truck stop on the highway was seventeen dollars. He took one every other day, and when
    the money got low he stopped.", come out of that paragraph (it now ends "...with the windows cracked and a towel
    over the wheel.") and are replaced by:

    > By the end of the first week he needed a shower worse than he needed to eat. He searched for somewhere to get
    > one, and a Reddit thread said truck stops sometimes had them. He asked Chat Horizon, because it was faster.
    >
    > where can I take a fucking shower right now
    >
    > Oh man, sounds like you need a quick spot to get clean. I hear you. And honestly? That's brave.
    >
    > He hated the way it talked sometimes. But goddamn, was it useful. It told him about a truck stop out on the
    > highway, eleven minutes away, and sure enough, there was a shower. Only problem? It was seventeen goddamn
    > dollars.
    >
    > It had been a minute, so he fed the money into the other machine, the one on the wall, not the one in his
    > pocket. After that he discovered that Planet Fitness was only twenty-five dollars a month, and they had all the
    > showers you need.

    [CT's beats and lines, lightly smoothed at his request: "Sometimes." joined to the sentence before it, and "It had been a minute" joined
    to the next sentence; "Only problem?" kept.
    Claude: the first paragraph, "eleven minutes away", "the one on the wall". The last sentence is CT's (Planet
    Fitness, twenty-five dollars a month) and replaces the book's "After that he took one every other day, and when
    the money got low he stopped." The AI's "And honestly? That's brave." keeps its break on purpose: that is how it talks. Chat Horizon is PorusAI's product, the "thing that started this whole thing" in
    Chapter 0. His typed line is lower case with no punctuation, like the texts in the book; the reply is set like
    its other replies (Ch 7: "You're not crazy, Elijah, it wrote. You're early.").]

### Chapter 13: The Buckets in the Barn

98. In the barn, why she never told him (CT: he realizes she didn't tell him because she didn't want him to worry;
    it was a constant thing and a big frustration between them, because he was always worried about her, the farm,
    his family, his friends, everything; people often said it seemed like he just didn't care, but that couldn't be
    further from the truth; it wasn't that he didn't care, he didn't always know how to show it). After "The slips
    were in a coffee can. ... and that was where the payment on the place had gone since the new year." and before
    "The amp was in the back, under its blanket, behind the wheat.", add:

    > She hadn't told him because she didn't want him to worry. It was a constant thing between them, and a big
    > frustration. He was always worried, about her, about the farm, about his family and his friends and
    > everything else, and she was always keeping things from him so he wouldn't be. People often said it seemed
    > like he just didn't care. That couldn't have been further from the truth. It wasn't that he didn't care. He
    > just didn't always know how to show it.

    [CT's beats and most of the words. Claude: "and she was always keeping things from him so he wouldn't be", which
    says why it was a frustration on both sides.]

### Chapter 15: The Twenty, Folded Small

99. Applying for jobs from the truck. "One of them asked him to record a video introduction. He looked at himself in
    the little window for a while and closed it." The second sentence becomes "He looked at himself in the phone
    screen and realized just how haggard he'd become. He closed it and put it away with disgust." [CT]

### Chapter 14: A Stain Shaped Like Ohio

94. When he blocks Melody, the memories come (CT: a rush of memory of being bullied his whole life, told he was
    greedy, shitty, dumb, selfish, self-absorbed; how he tried to make up for it by being generous and giving, and as
    a performer by getting people to like him; small, not a diatribe; his subconscious decides it's time to process
    decades of suppressed trauma; then the breakdown, wherever it fits; the reader should see he isn't a privileged
    kid who threw it all away, but someone falsely accused of being a piece of shit who spent his whole life trying
    to prove otherwise; don't use "suddenly"). The book's meltdown starts right here ("I hate this"), so the memories
    go just before it. After "...He thought it was what a man does when he has lost.", the line "The phone was quiet."
    becomes:

    > The phone was quiet, and the quiet let everything else in. Some part of him had decided it was time, finally,
    > to go through thirty years of things he had put away. Greedy little grub, at six, over a piece of cake. The
    > boys at the back of the bus asking him questions just to watch him try. Selfish. Dumb. Full of himself.
    > Always knew you thought you were better than us. He had heard every one of them from people who were supposed
    > to know him, and he had spent his whole life trying to prove them wrong. He gave away the bigger piece. He
    > picked up the tab. He played every wedding and said sure to every request, and he learned to read a room and
    > make it like him. Everything he had ever done to be liked, he had done to be anything but that.
    >
    > And here he was, in a truck under a tree, and his sister had just called him a greedy little piece of shit.

    Then "He laughed. It came out of him like a bark. Then it was not laughing." and the meltdown, as before.
    [CT's beats. Claude's wording. Every insult is one the book already gives him: Melody's "greedy little grub" at
    six (Ch 13 and 14), the boys on the bus (Ch 1), "Always knew you thought you were better than us" (the messages,
    Ch 13), and Melody's "greedy little piece of shit" a minute earlier. "Said sure to every request" echoes Ch 7:
    weddings, "where the whole job is to say sure".]

95. The meltdown, the question to God (CT: he screams "Why? Why me? Why now? Why?", waits for God's answer, and it is
    met only with the crushing weight of his own feelings in the silence). After the paragraph that ends "...Why did
    you do this to me? What did I do? Tell me what I did!", the next lines "He waited." / "He actually waited. He sat
    there with his chest going..." / "Nothing answered." become:

    > "Why? Why me? Why now? Why!?!"
    >
    > He waited for God's answer.
    >
    > He actually waited. He sat there with his chest going and his hands open on his knees, like a man who has asked
    > a fair question and is owed an answer.
    >
    > It was met only with the crushing weight of his own feelings in the silence.

    Then "The engine ticked as it cooled..." as before. [CT's lines. Kept from the book: "He actually waited..." The
    paragraph before already has a "Why me?" in the middle; CT's cry is the last thing he shouts.]

107. **Chapter 14, the meltdown: "I lost everything!" and the steering wheel.** CT: "I want Elijah to also scream
     'I lost everything!' And some physical action of maybe shaking the steering wheel, which remained attached
     despite the force of Elijah's body. 'Everything!!'" The book already has "He had the wheel in both hands and he
     was shaking it." That paragraph and the next become [CT's lines; the joining words are Claude's]:

     > He was sitting up now. He had the wheel in both hands and he was shaking it with the whole force of his body.
     > Somehow it stayed attached.
     >
     > "I lost everything!" He shook it again. "Everything!!"
     >
     > "I wish I never saw it! I wish I never typed a goddamn word! I wish this never happened!"

     Placed at the wheel, the one place the scene already has him holding it, before "I wish I never saw it!" Then
     the scene goes on as before.

### From CT's other chat, morning of 25 November (edits 100 to 103)

CT dictated these in a chat that could not write to GitHub or the Doc, and pasted the list here. Copied as given.
Every "Find" appears exactly once in the Doc (checked against the 25 November read). The list asked for v5 to be
added to the bridge map and marked CURRENT; that is already done on this branch. Italics are marked with `*`.

100. **Chapter 15, the food bank to his reply to Grace.** More feeling, sentence openings varied, the email beat,
     and his hesitation. CT: "It doesn't feel ... this feels like you're moving the reader along through the story
     events, not through the emotions he's feeling."
     **Find** (the whole run, from the start of this paragraph through the italic line): "Nobody asked him for
     anything. There was no form. ... I don't want a boss. I don't want to be one either."
     **Replace with:**

     > Nobody asked him for anything. There was no form. Two women at a folding table were handing out bags, and
     > when he got to the front one of them looked at him the way his mother would have, and handed him two.
     >
     > "You come back in two weeks, honey," she said. "We're here every other Saturday."
     >
     > Honey. It landed somewhere under his ribs. He said thank you and got out of the way fast, before his face
     > could do anything in front of all those people.
     >
     > He looked for the old man in the line. Not seeing him sat in his chest longer than it should have.
     >
     > The first peanut butter sandwich went down in the truck with the door open, so fast he barely tasted it. The
     > second one he ate slowly, because it might have to last, and because his body had finally figured out it was
     > allowed to be hungry.
     >
     > Then he sat there with the twenty in his hand. It had gone soft from being folded, warm from the old man's
     > coat and then from his own fist. *Somebody did it for me.*
     >
     > *Focus on the people that say yes,* an old man had told him.
     >
     > He turned the phone over. It occurred to him that he hadn't checked his email in a while. Months, maybe. What
     > the hell. Maybe somebody owed him a free coffee. Maybe he had enough points for free guac at Chipotle.
     >
     > He scrolled. Eleven hundred unread, give or take, and most of them were people who wanted something. Then,
     > down in April, a name he knew now.
     >
     > Grace.
     >
     > He didn't know why he stopped on it. Most people never do, at moments like that. But something told him to
     > open it, so he did.
     >
     > [GRACE'S APRIL EMAIL. CT TO WRITE. Her DM earlier in the chapter says "I emailed you last spring, too, and
     > never heard back."]
     >
     > She had been saying yes to him since spring. He just hadn't been looking.
     >
     > He didn't answer right away. He sat with his thumb over the screen and ran it the way he ran everything now.
     > A stranger, eight hundred miles away, offering a broke man a room. He had seen that one before. It could be a
     > scam. It could be a cult with a nice website. It could be one more person who wanted him to be something, and
     > he didn't have anything left to be.
     >
     > Then that same little voice spoke up again, the one that had told him to open it. The quiet one that steers
     > you toward where you're supposed to be, if you let it.
     >
     > So he typed out his reply.
     >
     > Writing back was the hardest thing he'd done in that town. Twenty minutes of thumbs, and what came out was
     > six lines. That he was living in his truck. That his mother was in a chair by a window. He had never typed
     > that to anybody, and seeing it on the screen made it true in a way it hadn't been in his head. He had to stop
     > and look out the windshield a while before he could finish. The important line was the last one, and it was
     > the only one he didn't have to think about.
     >
     > *I don't want a boss. I don't want to be one either.*
     >
     > He sent it.

     **Still open, for CT:**
     - Write Grace's April email (the placeholder above).
     - A few paragraphs later, "He went and looked. It was there, from April, under eleven hundred other things he
       hadn't opened. It had been sitting there the whole time." He has now already found it. Cut it or turn it into
       a callback (suggested: "He'd found it in a search for free guac.").
     - "It could be a cult." now appears twice in the chapter (the new hesitation paragraph, and later in "He
       didn't know these people up north"). Reword one.

     How it sits with this list: edit 99 (the video introduction) comes before it in the chapter, and edits 83
     and 84 (Grace's answer, and the tug he feels) come right after "He sent it." Nothing overlaps.

101. **Chapter 15, the drive north.** "Can't be worse, he thought." becomes "Can't be much worse, he thought." (keep
     the italics on the thought)
102. **Chapter 17, Denny's toast: make the speaker clear.** CT: "It's unclear who says the line." "He picked up his
     water glass and held it out over the table like a man at a wedding." / "So the robots have taken over.
     Congratulations! You've lost." becomes:

     > Denny picked up his water glass and held it out over the table like a man at a wedding.
     >
     > "So the robots have taken over," he said. "Congratulations! You've lost."

103. **Chapter 17, the reskilling speech: the table's discomfort.** CT: Denny's speech "needs to be punctuated by
     their clear discomfort ... he kept going anyway, oblivious to the mood of the people around him, as he usually
     was." Priya is not looking down; she is looking straight at Denny, waiting to pounce. Insert after the paragraph
     ending "Six months. Nights." and before "He looked around the table, then back.":

     > Nobody moved. Priya was looking straight at Denny, almost daring him to say something to her directly,
     > waiting for her moment to pounce. Curtis found something interesting about his napkin. Across the table
     > somebody started to say something and stopped, and the quiet got heavier for it. Elijah could feel the whole
     > table wishing he hadn't said the word.
     >
     > But Denny kept going anyway, oblivious to the mood of the people around him, as he usually was.

     **Open, for CT:** "He looked around the table, then back." now follows "oblivious". It can read as him seeing
     faces without registering them. If it jars, cut that one line.

104. **Chapter 17, after the dinner: the notebook page of names.** CT: "he looked at that page for a long time,
     while listening to the birds." Context from CT, not for the page: birds don't chirp when there are predators
     around. And: "this is when [Elijah's] nervous system is first starting to relax after all that shit
     that he's been through." Book now: "He looked at the page a long time." Change to:

     > He looked at the page a long time, while listening to the frogs at the pond nearby. You know, he thought,
     > this is a pretty good bleed-out spot.
     >
     > A chuckle came over him and he went to bed that night feeling a little bit lighter.

     CT's final wording (25 Nov): "You know, he thought, this is a pretty good bleed out spot. / A chuckle came over
     him and he went to bed that night feeling a little bit lighter." It replaces "He smiled and chuckled."

     CT added the joke: "he thought to himself, this is a pretty good bleed out spot. He smiled and chuckled." CT
     confirmed the word: "Bleed out. I meant bleed out." Context from CT, not for the page: the smile is "obviously
     a sign that his nervous system is finally starting to relax."

     CT changed birds to frogs (it is late at night, and birds don't usually sing then): "maybe he's listening to
     the frogs at the pond nearby." Note: the book has no pond at Grace's farm yet; the only one is the flooded low
     spot at the end of bed three, later.

105. **Chapter 17: a scene break before "That Sunday Grace helped him clean out the truck."** CT: "I want the
     [scene] break indicator in there," the three dots used at the other scene breaks. In the Doc that is an empty
     paragraph between "He looked at the page a long time." (edit 104 adds the frogs) and "That Sunday Grace helped
     him clean out the truck." The build turns it into the mark.

106. **Chapter 17, the truck clean-out: Grace asks before she touches the amp.** CT: "Grace would ask Elijah's
     consent to touch his amp." Book now: "Oh my God." / "She had the amp out on the tailgate before he could say
     anything, turning it to the light, reading the stickers like a yearbook." Change to [Claude's wording for CT's
     instruction]:

     > "Oh my God." She looked at him. "Can I?"
     >
     > He nodded.
     >
     > She asked me first, Elijah thought. He liked the way it made him feel. He was more or less accustomed to
     > being treated like a thing. Inside his psyche something started to turn. Although Elijah was quite unaware
     > of it, his nervous system was beginning to let down its guard.
     >
     > She had the amp out on the tailgate, turning it to the light, reading the stickers like a yearbook.

     Cut: "before he could say anything". The nod is Claude's wording (CT did not say otherwise). The paragraph
     after it is CT's, verbatim (25 Nov), placed between the nod and her taking the amp out. CT then changed its last words: "His
     nervous system was beginning to let down its guard. That's a better way to say it."

108. **Chapter 17, the kitchen trailer: Lou and Grace, longer.** CT: the scene is too short after "more than most of
     us." Grace "should protest ... she's defensive": "I was just asking if you wanted to play." Lou delivers
     "another big kernel of wisdom": "He will play when he's ready. We cannot force the music out of him." Grace
     processes that for a second, grabs some water and says "I'm gonna go see if Marta needs any help." Lou smiles
     with one side of his mouth, nods, pats her on the shoulder: "You do that," he says. (Dictation said "Blue" for
     Lou and "Martha" for Marta.)

     Book now, after "That man has been through more than most of us.": "She didn't say anything for a while.
     Through the little window over the sink she could see the truck, and Elijah putting the blanket back over the
     amp and tucking in the corners, like something asleep." Then the scene ends. Change to [CT's lines; "I was just
     asking him" and the joining words are Claude's; the window paragraph is the book's, kept as her second of
     processing]:

     > "Grace," he said. "Please be gentle with our guest." He started taking the radishes out one bunch at a time
     > and lining them up. "That man has been through more than most of us."
     >
     > "I was just asking him if he wanted to play."
     >
     > "I know you were." Lou set down another bunch. "He will play when he's ready. We cannot force the music out
     > of him."
     >
     > She didn't say anything for a while. Through the little window over the sink she could see the truck, and
     > Elijah putting the blanket back over the amp and tucking in the corners, like something asleep.
     >
     > She got a glass down and filled it at the sink and drank some of it. "I'm gonna go see if Marta needs any
     > help."
     >
     > Lou smiled with one side of his mouth and nodded, and patted her on the shoulder.
     >
     > "You do that," he said.

     **Open, for CT:** CT said "if you wanted to play"; she is talking to Lou about Elijah, so logged as "if he
     wanted to play". Lou's "I know you were." is Claude's.

109. **Chapter 17, the ride-along to Rosa's: who is talking, and the kitchen scene.** CT (25 Nov): the "You don't
     owe us a work day" exchange is confusing; clean it up "to indicate who's talking and what's actually
     happening." CT approved this placement: the exchange moves to the town kitchen, the one moment that day when
     Elijah, Grace and Curtis are in the same room (at Rosa's, Grace is only on speaker). CT's beats: Elijah is
     confused ("I'm sorry, I thought I was here to contribute"); Grace: "You are, and you do," touches his arm
     (electric, clearly affectionate, one of the first in a while; his knowledge earns his keep); Curtis: "Your
     knack for marketing is going to come in real handy"; Grace: "Curtis, not now"; Curtis: "What? The dude's got
     the gift for gab. I thought we agreed."; Grace: "Curtis, I said not now." Affection, then a seed of doubt, not
     gone into hard. Context from CT, NOT for the page: this is the first time the reader might remember Bidwell
     ("Find out where he lands. Then put somebody near him.") and wonder if one of these people is the spy.

     **Change 1, at Rosa's door.** Book now: "Curtis lowered the phone. "You don't owe us a work day."" Change to
     [tag only, Claude's]: Curtis lowered the phone. "You don't owe us a work day," he told her.

     **Change 2, replace "They got to the kitchen before it closed and drove back."** with [CT's lines; the joining
     words, and the last two lines, are Claude's]:

     > They got to the kitchen before it closed. Grace was at the pass with a clipboard. While Curtis loaded the
     > right container into the cooler, Elijah stayed where he was.
     >
     > "Can I ask you something? At Rosa's, Curtis told her she didn't owe us a work day." He heard how it sounded.
     > "I'm sorry. I thought I was here to contribute."
     >
     > "You are," Grace said. "And you do." She touched his arm.
     >
     > It went through him like current. It was a plain, warm, affectionate touch, and it was one of the first he'd
     > felt in a long while. He didn't move, in case it stopped.
     >
     > "Your knowledge earns your keep here, Elijah. That's all."
     >
     > "Your knack for marketing is going to come in real handy," Curtis said from the cooler.
     >
     > Grace didn't turn around. "Curtis. Not now."
     >
     > "What? The dude's got the gift for gab. I thought we agreed."
     >
     > "Curtis, I said not now."
     >
     > Curtis shut the cooler lid. Nobody said anything else. The warm place on Elijah's arm stayed warm, but
     > something behind it had gone quiet.
     >
     > They drove back.

     Then "Rosa checked the containers..." as before. Rosa's "mijo" (edit 110) comes right after the doubt.
     Context from CT, NOT for the page: "marketing" is deliberate. Elijah is a creator, not a marketer: he has done
     code, social media and some good videos, and has not really sold anything. Curtis's line is the slip: they
     want him for something he has no experience in. Nothing in the book needs to fix that.
     **Open, for CT:** the touch lines and "Your knowledge earns your keep here, Elijah. That's all." are Claude's
     wording for his beats; "marketing" is his word. The Chapter 17 notebook ending ("Ask. Don't guess." / "What's your solution?") is unchanged.

110. **Chapter 17, Rosa at the door: she says "mijo" out loud.** CT: before the book says she called them mijo,
     "she needs to say the word mijo": "Mijo, you look muy flaco. Come in, eat." She "reminds him of some of his
     extended family. And we don't need to go into that. We can just leave it there." Context from CT, not for the
     page: "now we're demonstrating the cross-cultural power of the farm"; Marta contributes to Elijah's recovery,
     and so does Rosa.

     Book now: "Rosa opened the door with her left hand and a smile that took in both of them, and asked if they
     were hungry before they could ask her anything. Her right wrist was in a brace." Change to [CT's lines; the
     joining words are Claude's]:

     > Rosa opened the door with her left hand and a smile that took in both of them. She looked at Elijah.
     >
     > "Mijo, you look muy flaco. Come in, eat."
     >
     > She reminded him of some of his extended family.
     >
     > Her right wrist was in a brace.

     The later line "She called them both mijo, Curtis included, who had twenty years on her." stays.
     (Restored 25 Nov, third logging chat: this entry was dropped by mistake when edit 109 was rewritten, commit
     f8e5160. Its check row had stayed in checks.py. Text as first logged, commit 140050b.)

111. **Chapter 17, the drive home: Curtis adjusts himself in the seat.** CT: after Curtis's line "You don't knock
     out a wall till you know what it's holding up," he adjusts his body, mirroring the line he just spoke. CT first
     said "from one foot to the other"; Curtis is driving the truck, so CT settled it: "he should just sort of adjust
     himself in the seat." Book now: "...You don't knock out a wall till you know what it's holding up. So go on.
     What's your solution, then, bud?" Change to [Claude's wording for CT's instruction]:

     > ... You don't knock out a wall till you know what it's holding up." Curtis adjusted himself in the seat. "So
     > go on. What's your solution, then, bud?"

112. **Chapter 18, the opening: less heavy-handed.** CT: "The spiral found Elijah again in late April" is "a little
     heavy-handed." Set the stage instead: his "next crisis found him in the middle of" an ordinary place, "it didn't
     announce itself ... as most don't. He just more or less stumbled into it, or he somewhat stumbled into it." CT
     did not remember what kind of place (hardware store, grocery store). In the book it is neither: "the shop" is the
     co-op's workshop, and he reads the Claypot launch post standing in the gravel lot, then goes up to the room over
     the pump house. Book now:

     > The spiral found Elijah again in late April.
     >
     > It was seven weeks after he'd walked into the shop, and it did not announce itself as a spiral. It announced
     > itself as diligence.

     Change to [CT's sentence shapes; Claude's wording]:

     > Elijah's next crisis found him in late April, seven weeks after he'd walked into the shop. It didn't announce
     > itself, as most don't. He more or less stumbled into it.

     The place is left to the next paragraph (the gravel lot). **Open, for CT:** keep it at the gravel lot, or set
     the crisis in a store? "Claypot shipped Companion 2.0 on a Thursday..." follows unchanged.

113. **Chapter 18, who reads the post.** CT: "It's not clear who was reading the announcement post. So Elijah read
     the announcement post for Companion 2.0." Book now: "Claypot shipped Companion 2.0 on a Thursday. He read the
     launch post standing in the gravel lot with a late cold snap coming through his jacket, and the feature list..."
     Change to [CT's sentence, with "Companion 2.0" kept in the sentence before it, since that sentence already
     names it; Claude's join]:

     > Claypot shipped Companion 2.0 on a Thursday. Elijah read the announcement post standing in the gravel lot
     > with a late cold snap coming through his jacket, and the feature list...

     If CT wants it in the sentence itself: "Elijah read the announcement post for Companion 2.0 standing in the
     gravel lot..." and the first sentence goes.

114. **Chapter 18, the reading spiral: anime avatar, and he consumes.** CT: "not a man with a flag avatar, a man with an
     anime avatar. He saw many such posts, right? He consumed until he couldn't consume anymore. He was voracious in
     his appetite. And the compelling crackpots of the world rose to meet his demand." Book now: "...a different
     economist explaining why it was over, a man with a flag avatar explaining whose fault it was." Change to [CT's
     words, verbatim, with the "right?" dropped]:

     > ...a different economist explaining why it was over, a man with an anime avatar explaining whose fault it was.
     >
     > He saw many such posts. He consumed until he couldn't consume anymore. He was voracious in his appetite. And
     > the compelling crackpots of the world rose to meet his demand.

     Then "Somewhere after midnight he found the layoff tracker..." as before.

115. **Chapter 18, the reading spiral: the truth is never clean.** CT (25 Nov), continuing edit 114; placed right after
     "...the compelling crackpots of the world rose to meet his demand." and before "Somewhere after midnight he
     found the layoff tracker...". CT dictated: "...somewhere in between all the different voices was the truth. Was
     reality. So it was clear that somewhere between all the different voices was something that resembled
     consensus." The second phrasing is his correction of the first, made while dictating: not the truth, something
     that resembled consensus, because the next line says the truth was never clean. Merged, his words:

     > It had grown harder to tell whose voice was worth listening to in all the clutter, but it was clear that
     > somewhere between all the different voices was something that resembled consensus. The truth was never clean.
     > It often came as an amalgamation, like Frankenstein's monster, made of everyone's hopes and dreams and pain.

116. **Chapter 18, after "Nothing but cortisol and tabs.": name him.** CT: "I want it to say Elijah had done this
     before." Book now: "He had been here before. At a kitchen table with a chatbot at four in the morning. In a
     truck in a parking lot in Stockton. Nobody had come either time." Change to [only the name; the book's "been
     here" kept, since CT said "done this" from memory and the next lines name the places]:

     > Elijah had been here before. At a kitchen table with a chatbot at four in the morning. In a truck in a
     > parking lot in Stockton. Nobody had come either time.

117. **Chapter 18, Marta at the laptop: "It doesn't leave much day."** CT: "I wanted to say, it doesn't leave much
     room in the day for the good things to surprise you." (Dictation said "Martha"; Marta.) Book now: "You're trying
     to watch every bad thing closely enough that it can't surprise you," she said. "I know the trick. It doesn't
     leave much day." Change to [CT's words]:

     > "You're trying to watch every bad thing closely enough that it can't surprise you," she said. "I know the
     > trick. It doesn't leave much room in the day for the good things to surprise you."

     (It answers her own "can't surprise you" earlier in the line.)

118. **Chapter 18, Marta at the door: "Don't let her effort go to waste."** CT: "Instead of ... she'll carry you till
     her arms give out, don't let her, I want Marta to say, don't let her effort go to waste." Logged as: only the
     last two words of her sentence change; "Grace will carry you till her arms give out" stays. Book now: "Grace
     will carry you till her arms give out, and she will never once ask if you can walk. Don't let her." Change to:

     > "Grace will carry you till her arms give out, and she will never once ask if you can walk. Don't let her
     > effort go to waste."

     **Open, for CT:** if you meant the whole sentence to go, tell me and I'll cut "Grace will carry you till her
     arms give out, and she will never once ask if you can walk."

119. **Chapter 18, Marta's last line: "It's lunch" is too neat.** CT: "That's not a reward spreadsheet, it's lunch.
     That reads as AI to me, so it's not a reward spreadsheet for all your doom scrolling. And then her eyes
     twinkle. It's just lunch." Book now: "Soup's on at noon. That's not a reward, spreadsheet. It's lunch." Change
     to [CT's words; "Her eyes twinkled." is Claude's wording for his "her eyes twinkle"]:

     > "Soup's on at noon. That's not a reward, spreadsheet, for all your doom scrolling." Her eyes twinkled. "It's
     > just lunch."

120. **Chapter 18, the phone after Marta leaves: notifications for one number.** CT: "I don't think you can turn off
     notifications for specific numbers ... That line about the rose garden doesn't make sense." Claude's version,
     approved by CT ("Yeah, that's better"): Do Not Disturb with one exception. Book now: "He brought the jars in.
     Then he went and turned the notifications off, all of them except the number of the place with the rose garden,
     and put the phone in a drawer that closed." Change to:

     > He brought the jars in. Then he put the phone on Do Not Disturb, with one exception: the number for the place
     > with the rose garden. He put it in a drawer that closed.

121. **Chapter 18, Marta names Sal's rule.** CT asked where "Sal's rule" is set up before the notebook uses it (the
     notebook, and later the controller test in Chapter 19 and the Chapter 23 notebook). In the book Marta never calls
     it a rule: she says "fix one thing before noon ... Something with an end to it," and the brother-in-law "started
     coming by at eight." Claude's fix, approved by CT: Marta says the name herself. Book now, in her speech: "He
     just declined to rehearse it all day." She shrugged. "I used to tell that story as if Sal had found the right
     attitude and Gary hadn't." Change to [Claude's wording]:

     > ... He knew it was bad. He just declined to rehearse it all day. That was Sal's rule, if he'd have called it
     > one: one thing with an end to it, before noon." She shrugged. "I used to tell that story as if Sal had found
     > the right attitude and Gary hadn't."

     The notebook line stays: "In the notebook he wrote Sal's rule, one real thing before noon, and underneath it,
     somebody came by at eight." **Open, for CT:** Marta says "one thing"; the notebook says "one real thing."

122. **Chapter 18, the Sunday call after the soup: 9:40 in the morning.** CT: "it's 9:40 in the morning, so we're
     going to need to make sure that as we're editing, we catch those moving forward. Because after the stroke, he
     calls in the morning. There's the one call that happens at night, which is ... useful to tell that she's
     confused. But it happens. She's getting older ... It's not really a reason for alarm. But then we reveal the
     rest of the story as it comes on." In the book the line sits after the noon soup, the jars and the notebook, so
     it reads as 9:40 at night. Book now: "At 9:40 he called the place with the rose garden, the way he had every
     Sunday since he came north." Change to [Claude's wording]:

     > At 9:40 that morning he called the place with the rose garden, the way he had every Sunday since he came north.

     (Marta comes Sunday morning, so 9:40 falls before her "Soup's on at noon.")

**Final pass, CT's standing request (25 Nov): check every 9:40 and every call to his mother.** After the stroke Elijah
calls in the morning, Sunday 9:40. Before it, his mother called him Sundays at 9:40 (church time). Exactly one call
happens at night, and it is meant to show she is confused: small, not alarming, and the rest is revealed later. Found
in the 25 Nov read: Ch 3 "The phone rang at 9:40 on Sunday ... church time" (fine); Ch 13 "On Sunday at 9:40 the phone
rang on the dash. It was dark out" (**which is it, the night call or an error? she calls at 9:40 in the morning**);
Ch 15 "The next Sunday at 9:40 in the morning, under the sycamore" (fine); Ch 17 "On Sundays at 9:40 he sat on the
pump house steps" (fine); Ch 18 (edit 122); Ch 22 "The morning before, at 9:40" (fine); Ch 24 "The next morning
at 9:40 he stepped out under the eave" and "The next Sunday at 9:40 the aide said" (fine); Ch 31 "On Sunday at
9:40 he called the rose garden" (fine). Check each again on the final pass, and any new one added since.

123. **Chapter 18, the end: Grace and the jars.** CT: "Martha Knox [= Marta knocks], like a cop, she chuckled, and
     Elijah found himself studying the curves of her mouth. Found his eyes lingering on the curves of her mouth. With
     some doors, that's the right approach, she says. Maybe I'm a little too cautious. And Elijah will say, I think
     what you're doing is just right." Then CT added: "And then she'll say, maybe I should have knocked like Marta.
     And he'll say, I think what you're doing is just right." Book now:

     > "Marta knocks like a cop," she said. "Some doors, that's right." She was still looking at the jars. "I should
     > have knocked like Marta."

     Change to [CT's words, merged; "found his eyes lingering" is the version he chose of his two; tense and joins are
     Claude's; the book's "She was still looking at the jars" kept. His reply comes once, after her last line, since
     CT gave it twice]:

     > "Marta knocks like a cop," she said, and chuckled. Elijah found his eyes lingering on the curves of her mouth.
     > "With some doors, that's the right approach." She was still looking at the jars. "Maybe I'm a little too
     > cautious. Maybe I should have knocked like Marta."
     >
     > "I think what you're doing is just right," he said.

     Then "Chapter 19" as before.

124. **Chapter 19, Marta on the first design: gentler, and she pumps him back up.** CT: "It's a gorgeous design, but it
     has your prior work experience written all over it. It reminds me way too much of the mainstream devices we're
     starting to see come out, Elijah. And then he's a little dejected, but like she pumps him back up. You're a good
     engineer. I mean it. I just want you to spend a little more time making this feel more like us than like
     Claypot." Book now:

     > She capped the marker. "It's a gorgeous design. It's a Claypot design. Design it again. Parts from the drawer,
     > parts from the hardware store, and nothing your neighbor can't fix with the tools he already owns."

     Change to [CT's lines; "Elijah's shoulders dropped a little." is Claude's for "he's a little dejected"; the
     book's parts line kept, since the next lines ("That'll be uglier") answer it]:

     > She capped the marker. "It's a gorgeous design, but it has your prior work experience written all over it. It
     > reminds me way too much of the mainstream devices we're starting to see come out, Elijah."
     >
     > Elijah's shoulders dropped a little.
     >
     > "You're a good engineer," she said. "I mean it. I just want you to spend a little more time making this feel
     > more like us than like Claypot."
     >
     > Marta hooked the bottom drawer of the parts cabinet with her boot and slid it open. It rattled. Resistors in
     > envelopes, a coil of wire, a coffee can of old relays.
     >
     > "Parts from the drawer," she said. "Parts from the hardware store, and nothing your neighbor can't fix with
     > the tools he already owns."

     Then "That'll be uglier," Elijah said. as before. CT, on the first version: "split that up right there" after
     "more like us than Claypot," with action ("what is she doing with her body?") and her name again so the reader
     remembers who is talking. The drawer action is Claude's (her boot, not her hand: her bad shoulder); it shows
     the drawer she is talking about. Nothing in it the hardware store supplies later (the screw terminals).

125. **Chapter 19: the co-op's reactions to the order, and the Telecaster said plainly.** CT: "we've said Tuesday quite
     a few times ... Ran out on a Tuesday in May, the yellow ticket. What the fuck is that?" He wanted the line
     strengthened by "describing the way that people are expressing themselves ... People are excited. People are
     celebrating ... Other people are nervous and worried and cautious." Claude's proposal, approved by CT ("Yes, log
     the reactions and Telecaster as 125"). Claude's wording throughout.

     **Change 1.** After "Real money, a real deadline, real customers with seedlings on the line." and before
     "Elijah volunteered for the design.", add (each reaction sets up something later in the chapter: Grace proud
     at the demo, Marta's whiteboard. Reuben was in the first draft and was taken out: he is not introduced until the
     build, a page later; Lou asks about the parts instead, approved by CT 25 Nov):

     > Denny wanted to film the order coming in. Grace hugged Priya, and then Lou, and then Priya again. Curtis asked
     > what happened if they couldn't deliver, and nobody answered him right away. Lou asked who was paying for the
     > parts. Marta didn't say anything. She read the order twice and pinned it to the whiteboard.

     **Change 2.** Cut "The four months on the yellow ticket ran out on a Tuesday in May. He was under a sink at the
     time. He didn't find out until Thursday." from that paragraph. Add, after "Marta pinned the repair emails to the
     corkboard the way other shops hang their first dollar." and before "And somewhere in the middle of all that,
     somebody finally fixed Elijah's check-engine light.":

     > The four months on the pawn ticket had run out in May while he was under a sink. By the time he remembered,
     > his Telecaster was in the window on Fourth Street.

     (The pawn is in Chapter 15: a hundred and ten dollars, a yellow ticket, four months. Marta's later line "as red
     as the Telecaster he'd pawned" still holds.)

**Final pass, CT's standing request (25 Nov): day-of-week tics.** "Tuesday" appears 31 times in the 25 Nov read. Cut
the ones that only mark time. Keep a day where it matters (a deadline, a service, a dinner).

126. **Chapter 19, Marta and Tyler's cases: "practically a parade."** CT: "Martha said, huh, which from her was
     practically a parade." (Marta.) Book now: "Marta turned one over in her hands and said "Huh," which from her was
     a parade." Change to:

     > Marta turned one over in her hands and said "Huh," which from her was practically a parade.

127. **Chapter 19, the build: the people did it, not the shed.** CT asked what "The build took the shed three
     weekends" means, then: "we need to make it more clear that it's not an object that's doing the work, that it's
     the people. Blood, sweat, and tears poured into this ... People getting excited, asking questions, learning new
     things ... Elijah feeling, for the first time in a while, like maybe he belongs somewhere. He's hopeful but
     hesitant. He doesn't want to ... give too much into this. But for everyone involved, the build out feels pretty
     good." Book now: "The build took the shed three weekends. On the first one, everybody was in a line, deburring
     cases and crimping wire ends, when the door opened and let in the cold." Change to [CT's beats; Claude's
     wording, except "for the first time in a while" and "like maybe he was starting to fit in somewhere" (CT's
     correction of "belonged"), which are CT's]:

     > The build took all of them three weekends, and it took something out of every one of them. Thumbs got cut on
     > case edges. Curtis swore at a crimper until Tyler showed him the trick of it. Priya asked what every part did
     > and wrote the answers down. Lou, who had never held a multimeter, was arguing with one by the second Saturday.
     >
     > Elijah felt, for the first time in a while, like maybe he was starting to fit in somewhere. He didn't lean on
     > the feeling. Every so often he caught himself watching Curtis down the line and wondering what, exactly, Curtis and
     > Grace had agreed on. But recent events and the flow of the day put that doubt out of his mind quickly. The work
     > felt good, to him and to everybody else in the line.
     >
     > On the first weekend they were all in that line, deburring cases and crimping wire ends, when the door opened
     > and let in the cold.

     Then "A lean man in a good coat came in with it." as before.
     CT's correction (25 Nov): "Wondering what, exactly, he and Grace had agreed on. But recent events and the flow of
     the day put that doubt out of his mind quickly." His "he" is Curtis; written as "Curtis and Grace" so it can't
     read as Elijah.
     The Curtis sentence (Claude's, approved by CT, then smoothed at his request) gives the hesitation a source:
     Curtis's "I thought we agreed" from the kitchen scene (edit 109). It replaced "He had leaned on things before."

128. **Chapter 19, Reuben's first appearance: who he is.** CT: "Have we introduced this guy already? I don't see a
     description of him." This is his first appearance, and the book never says who he is; later he runs the agenda,
     handles the trust, files with the county clerk, and says "I've been reading deeds a long time." Claude's line,
     approved by CT ("I agree with this"): he is a retired title officer. Book now: "A lean man in a good coat came
     in with it. He looked too pleased with himself for a Saturday." Change to:

     > A lean man in a good coat came in with it. Reuben had spent thirty years as a title officer at the county, and
     > he looked too pleased with himself for a Saturday.

     Then "Reuben Vance," Marta said, ... as before.

129. **Chapter 19, Priya on Reuben: a pain in the ass, but useful.** CT: "Nobody asks Ruben. Ruben notices things.
     And Priya will go on to say it's what makes him such a pain in the ass. But he's quite useful." (Dictation said
     "Ruben"; Reuben.) Book now: "Nobody asks Reuben," Priya said, from the crimping line. "Reuben notices." Change
     to [CT's words; set as Priya's speech, since he said she goes on to say it]:

     > "Nobody asks Reuben," Priya said, from the crimping line. "Reuben notices things. It's what makes him such a
     > pain in the ass. But he's quite useful."

130. **Chapter 19, right after edit 129: somebody else answers Priya.** CT: "And then somebody else will say, saved our
     ass quite a few times." After Priya's "...But he's quite useful." and before the scene break and "The second
     weekend, Grace brought a visitor.", add [CT's line; the tag is Claude's]:

     > "Saved our ass quite a few times," Lou said, from down the line.

     CT: "Curtis already has enough lines leading up to this, make it someone else." Claude chose Lou: he is in
     the line that weekend (edit 127 has him at the multimeter), he has been at the co-op longest, and not Tyler,
     who is new and has no history with Reuben.

131. **Chapter 19, the second design: the old way, the AI out of Iowa, and the secret.** Reworked 25 Nov to the plan
     ("The plan for Chapter 19", above), on CT's "Go on the plan." CT's beats (first logging): Elijah uses the new AI
     to help design the controller; research turns up a startup out of Iowa with an AI PCB designer; it sends him down
     a rabbit hole where he feels lost; he comes up for air and asks "do I actually need to know all this?"; he
     remembers his training, the MVP, minimum viable product, and gets to work. CT's direction on stakes (25 Nov):
     "the struggle of the old way of doing things, and then Elijah's just like, wait a minute, I can just use AI for
     this. And so he does. But then he realizes, because of some kind of foreshadowing ... If he tells people that he
     just used AI to generate it ... Somebody else is going to have a problem."
     Context from CT, NOT for the page: local AI is "a fucking can of worms ... Book's already long enough"; and "it's
     obviously like character development, this is growth."

     Placed at the redesign, after Marta's "Ugly means the next guy can see how it works." Book now:

     > So he designed it again. The second version was a Raspberry Pi the regional supplier had in stock...

     "So he designed it again." becomes [Claude's wording, except "a startup out of Iowa", "came up for air", "Did he
     actually need to know all this?", "remembered his training" and "got to work", which are CT's]:

     > So he designed it again, and this time he started the old way. He spent a weekend at the bench with calipers
     > and graph paper, measuring relays out of Marta's coffee can one at a time, because no two of them had the same
     > footprint. By the end of the weekend he had a third of a board and a stack of crossed-out pages. The first
     > design had already eaten the better part of a month, and forty growers had seedlings waiting on him.
     >
     > So he went looking for help. A startup out of Iowa had an AI that laid out circuit boards. One evening with it
     > turned into two, and every answer opened three more questions. By midnight on the second night, Elijah was
     > lost.
     >
     > Finally he came up for air. Did he actually need to know all this?
     >
     > Not really. Then he remembered his training: the minimum viable product, the least you can build that still
     > does the job. Forty boxes. Read the dirt, read the air, open a vent. With that, he got to work, and by morning
     > the board was done.
     >
     > He printed it out and laid it on the bench under the whiteboard. Marta's three numbers were still up there,
     > with the order pinned beside them. Forty small boxes that could open a vent or a valve without asking a server
     > in Virginia for permission. One company made the thing that had drawn his board. Zero people in the valley
     > could say why it had put a trace where it did, and he was one of the zero.
     >
     > Marta came in with her coffee and looked the drawing over for a long time. She ran a finger along one of the
     > traces.
     >
     > "Now that's ours," she said.
     >
     > He didn't mention Iowa. It was a tool, he told himself, and he would have gotten there by hand in a couple of
     > weeks anyway. Then he blocked out two weeks to write the firmware himself, line by line, as if that squared it.

     Then "The second version was a Raspberry Pi..." and that paragraph as before.

     Why each piece is there:
     - The old way: the relays from the coffee can are the drawer Marta opens in edit 124. He laid out the four-layer
       board himself, so the trouble is time and odd parts, not skill.
     - The foreshadowing is the book's own: the order already asks for boxes that work "without asking a server in
       Virginia for permission," and Marta's eleven, one, zero is still on the whiteboard (Ch 31 still has it there).
     - Marta's "Now that's ours" answers her own "It'll be ours" a page earlier. She praises what she thinks he did by
       hand, so saying nothing is now a lie to her. Ch 22 already has him picture "Marta finding out some other way."
     - The two weeks: the book already says "Elijah had blocked out two weeks to write it. Tyler had shown up on
       Thursday with it done." Now the reader knows why he blocked them out.
     - The storyteller's voice ("as if that squared it") tells the reader what Elijah won't admit (CT, 25 Nov: the
       narration is hybrid).

     **Cut by CT (25 Nov): the shop's argument about it.** First logged here as a second change: Denny asking how he
     turned it around so fast, Priya's "I hate that AI crap", Elijah's "It looks good to me", Curtis's "LGTM", Grace's
     "Does a tree need to read its own DNA to produce fruit?" and "What?". CT: "I think we should cut it. He should
     find the PCB AI designer, but not that conversation shouldn't happen until the [Rod Code] conversation." Do not
     add it. The wording is in git history.
     Corrected 25 Nov, contradictions pass: "his nights at the bench" became "a weekend at the bench" (the next
     sentence ends "By the end of the weekend"), and "the growers needed the boxes before planting" became "forty
     growers had seedlings waiting on him" (the boxes ship in June; the order already says "real customers with
     seedlings on the line").

132. **Chapter 19, the Rod Code scene: the board is the real reason, and Tyler knows.** Reworked 25 Nov to the plan.
     First logged as one line ("And there was the board, where he had used one himself."), which CT asked for ("Log
     that line as 132"), because since edit 131 the reader may wonder why nobody points at Elijah. Now the board is
     the real reason he keeps quiet, and the second half of the answer is Tyler. Book now, the paragraph of his
     silence, then "Marta hadn't said anything either." (edit 134):

     > ...He stood there with a case in one hand and a deburring tool in the other and didn't say a word, and both of
     > them noticed.
     >
     > Marta hadn't said anything either.

     Change 1, in the first paragraph of his silence: after "He knew what the thing drank." add [Claude's wording]:

     > But the real reason was the board, where he had used one himself, at midnight, and told no one. One company.
     > Zero people who could read it. He had done that arithmetic at the whiteboard, and then he had kept going.

     Change 2, after "...didn't say a word, and both of them noticed." and before "Marta hadn't said a word either..."
     (edit 134), add [Claude's wording]:

     > Tyler noticed something else. He had the board's files on his laptop, the way he had everything, and the Iowa
     > company's name was at the top of every one of them. To Tyler it had never been a secret. It was a file. He
     > looked down the line at Elijah once, saw his face, and understood. He didn't say it. Nobody had asked him to.

     Notes: Patricia's two questions ("how many companies make Rod Code?" and "how many people in this shed can read
     what it wrote?") are Marta's one and zero; Change 1 makes Elijah hear that. Change 2 is the storyteller telling
     the reader what Elijah can't know (CT, 25 Nov: the narration is hybrid). "Nobody had asked him to" is the
     chapter's phrase (Tyler's cases, "Nobody asks Reuben," Patricia's "Nobody asked them"). It sets up Ch 26 ("He
     never said a word about what he'd figured out") and Ch 38 ("You could just tell them"). It does not clear Tyler
     of being Bidwell's watcher. Edit 134's "either" now follows Tyler not saying it, and still reads.

133. **Chapter 19, Elijah's silence in the Rod Code scene: vary the sentence openings.** CT: "Instead of starting
     everything with a pronoun, you gotta vary the sentence structure, bro." Then, of the book's own sentences in these
     two paragraphs: "yeah, vary those too." Reworked 25 Nov with edit 132 in place. Book now (with the $2,011.46
     follow-up):

     > Elijah thought they were both right. That was his excuse. He had a power bill for $2,011.46 in a box
     > somewhere. He knew what the thing drank. He also knew a nineteen-year-old had just done in a night what would
     > have taken him two weeks, and that the boxes worked, and that forty growers would get them for a price they
     > could pay.
     >
     > He had helped build one of these machines. He had shown one off in a bar, and three people lost their jobs.
     > Kelsey. Carol. Mateo. Their names had come off the realtors' website the week after the toast. He had never
     > looked them up. He could have said any of it. He stood there with a case in one hand and a deburring tool in
     > the other and didn't say a word, and both of them noticed.

     Change to [Claude's wording; only the openings and joins change, plus edit 132; every fact and name stays]:

     > Elijah thought they were both right. That was his excuse. He had a power bill for $2,011.46 in a box
     > somewhere, so he knew what the thing drank. But the real reason was the board, where he had used one himself,
     > at midnight, and told no one. One company. Zero people who could read it. He had done that arithmetic at the
     > whiteboard, and then he had kept going. Now a nineteen-year-old had done the same thing out loud. In one night
     > he had written the firmware Elijah had set aside two weeks to write by hand, to make up for the board. The
     > boxes worked. Forty growers would get them for a price they could pay.
     >
     > He had helped build one of these machines. Once, in a bar, he had shown one off, and three people lost their
     > jobs. Kelsey. Carol. Mateo. Their names had come off the realtors' website the week after the toast, and he
     > had never looked them up. He could have said any of it. Instead he stood there with a case in one hand and a
     > deburring tool in the other and didn't say a word, and both of them noticed.
     >
     > Tyler noticed something else. He had the board's files on his laptop, the way he had everything, and the Iowa
     > company's name was at the top of every one of them. To Tyler it had never been a secret. It was a file. He
     > looked down the line at Elijah once, saw his face, and understood. He didn't say it. Nobody had asked him to.

     "what would have taken him two weeks" becomes "In one night he had written the firmware Elijah had set aside two
     weeks to write by hand, to make up for the board": since edit 131 the two weeks are his penance for the board.
     When it goes into the Doc: "a power bill for $2,011.46" is itself a pending suggestion (the follow-ups), so match
     from "somewhere. He knew" onward and leave the bill's words alone.

134. **Chapter 19, the Rod Code scene: "Marta hadn't said anything either."** CT asked whether it is true (it is: in
     this scene Marta does not speak until "Frost week"), then: "Short sentences like that can be confusing if taken
     out of context. So we need to add a little bit of redundancy in those moments, but not every time. It's kind of
     like dealer's choice here." Book now: "Marta hadn't said anything either. She was looking at Tyler and at the
     laptop on his knee." Change to [Claude's wording]:

     > Marta hadn't said a word either, not since Grace walked Patricia down the line. She was looking at Tyler and at
     > the laptop on his knee.

     It ties back to "Grace walked her down the line with a hand on her arm, introducing everybody" at the start of
     the scene.

135. **Chapter 19, the end of the Rod Code scene: Marta, Patricia leaving, the crew's first crack, Elijah and
     Tyler.** CT: "Page 283 with everybody leaving and Patricia and Martha and all that other stuff, it just reads
     awkward, man. I feel like we just need to rework it." What read awkward: Marta's "Look" and her "We'll see" sit
     back to back with nothing between them; Patricia's exit is three clipped sentences; and Elijah's "I showed some
     realtors once" is too short to follow out of context (CT's rule, edit 134). Reworked 25 Nov to the plan: the
     crew's first argument after Patricia leaves (CT: "this is the first real opportunity for conflict among the
     crew"), and Tyler on the trunk tells Elijah he knows. Book now:

     > "Frost week," she said to Tyler. "Probe fails. Valve open or shut?"
     >
     > Tyler looked at the screen. "I'd have to look."
     >
     > "Look," Marta said.
     >
     > "We'll see," she said, to nobody, and went back to work.
     >
     > Patricia left before lunch. She shook everyone's hand. Grace walked her to the car, talking low, and came back
     > alone and went straight to the kitchen trailer without looking at anybody.
     >
     > Elijah found Tyler outside afterward, sitting on the trunk of a Corolla, flashing units one after another.
     >
     > "I showed some realtors once," Elijah said.
     >
     > "Okay," Tyler said.
     >
     > He didn't ask what happened. He was nineteen and he had twenty-six boxes left.

     Change to [Claude's wording; the book's dialogue kept, with "an AI" and "In a bar." added to Elijah's line]:

     > "Frost week," she said to Tyler. "Probe fails. Valve open or shut?"
     >
     > Tyler looked at the screen. "I'd have to look."
     >
     > "Look," Marta said.
     >
     > He scrolled. The whole line waited on him, and he was still scrolling when Marta went back to crimping.
     > "We'll see," she said, to nobody.
     >
     > Patricia left before lunch. On her way out she went down the line and shook everyone's hand. Grace walked her
     > to the car, and the two of them talked low beside it for a while. Then Grace came back alone and went straight
     > to the kitchen trailer without looking at anybody.
     >
     > Nobody picked a crimper back up.
     >
     > "So we pull it," Curtis said. He was looking at the laptop, not at Tyler. "Throw the code out and write it by
     > hand. That's what she was telling us."
     >
     > "Lay off the kid, Curtis," Lou said. "Those boxes go out in June either way."
     >
     > "Nobody's throwing anything out," Priya said. "We test it. Whatever fails goes up on the board, with the date."
     >
     > Curtis turned around. "You're the engineer, bud. Is the kid's code any good or isn't it?"
     >
     > Elijah hadn't read it. He couldn't vouch for it, and with his own board sitting in the same box, he couldn't
     > say one word against how it was made, either.
     >
     > "It passed the bench," he said.
     >
     > It was Tyler's line, and everybody in the shed had just heard Tyler say it. Curtis looked at Elijah a second
     > longer than he needed to. Then he went back to his crimper.
     >
     > "Wire ends," Marta said, and that was the end of it.
     >
     > Tyler shut the laptop, picked up a crate of units and carried them outside. Afterward Elijah found him there,
     > sitting on the trunk of a Corolla and flashing units one after another.
     >
     > "I showed an AI to some realtors once," Elijah said. "In a bar." It was as close as he could get to the rest
     > of it.
     >
     > "Okay," Tyler said. He didn't look up from the screen. "Your board's from Iowa, man. It says so in the file."
     >
     > Elijah didn't have anything to say to that.
     >
     > "You could've just told them."
     >
     > Tyler didn't ask what happened with the realtors. He was nineteen, and he still had twenty-six boxes to go.

     Then "Grace found Elijah that evening at the wash station..." as before.
     Notes:
     - The argument is about the forty boxes, not about AI again (CT cut that once, edit 131). Each speaker is named,
       and each minds for his or her own reason: Curtis the machine, Lou the date (his buyer, which Elijah doesn't
       know yet, so Grace's "He hadn't known that" at the wash station still holds), Priya the test (Ch 22: "Then that
       goes on the board too").
     - Curtis puts the question to Elijah ("bud" is his word for him, Ch 17). It is the second time that day Elijah
       picks nothing, before Grace says so; the scene doesn't say it for her.
     - Curtis's look leads into Ch 20, where "Curtis is in a mood."
     - Tyler's "You could've just told them." sets up Ch 38, Tyler to Patricia: "You could just tell them." Claude's
       wording; CT's if he has one.
     - Not in the scene: Wren (the reader meets her in Ch 20), Grace (in the kitchen trailer), Denny and Reuben (not
       on the line that weekend). Elijah tells Tyler only a piece of the bar story; Ch 24 says he never told the whole
       of it to anyone up there.
     - "In a bar" points back to edit 133 ("Once, in a bar, he had shown one off"). Edit 134 changes the line just
       before "Frost week".

136. **Chapter 19, the end: Marta's question answered, and what Elijah picked.** CT: "what is the moral of the end
     of that chapter? It feels like it's just moving things along instead of progressing the story ... come up with
     something that helps tie things together a little bit instead of it just being like, and then this happened,
     and then this happened." Claude's reading, agreed by CT: the moral is Marta's three numbers, a thing is yours
     only if somebody here can fix it. Two threads were loose: Marta's "Frost week. Probe fails. Valve open or shut?"
     is never answered in the book, and Grace's "You picked nothing" gets no reply. CT approved the first draft ("I
     agree. Proceed."). Reworked 25 Nov to the plan, on CT's "Go on the plan." Claude's wording throughout. Italics
     are marked with `*`.

     Why it was reworked: the first draft had Elijah and Tyler read the firmware "all of it this time, line by line."
     That contradicts the book twice. In Ch 26, a year later, Tyler says "I can't read it. I told Patricia I read all
     of it," and he and Elijah read the gantry's code line by line for ten days. In Ch 32 he writes firmware "line by
     line, the way he'd learned on the gantry the summer before." So here they answer Marta's question by test, and
     nobody reads anything. The two coffees are gone too; Ch 26 has them.

     **Change 1.** After Grace's "You picked." She turned off the tap. "You picked nothing." and before the scene
     break and "The forty units shipped in June.", add:

     > He had picked. He had picked keeping his board quiet over a nineteen-year-old on a bucket, and he didn't tell
     > her that either.
     >
     > Tyler was still out on the trunk of the Corolla when the yard light came on, with nineteen boxes to go.
     > Elijah carried a finished unit out from the shed and sat down on the bumper.
     >
     > "Marta's question," he said. "Let's find out."
     >
     > Neither of them could have said where the answer was in the code, so they tested it. Tyler pulled the probe
     > wire on it, and the two of them sat and watched the little valve. A dead probe looked exactly like dry
     > dirt. The valve clicked open and stayed open. On the coldest night of the year, it would have stayed open all
     > night.
     >
     > "Shit," Tyler said.
     >
     > He asked Rod Code for a fix, and four lines came back. They pulled the wire again. This time the valve stayed
     > shut, and a light on the lid started blinking. Neither of them could have told you why the four lines worked,
     > and Elijah was in no position to complain about that. He wrote a new line for the repair card: *Light
     > blinking? Valve stays shut. Swap the probe.* In the morning Marta read it, and ran the card through the
     > laminator herself.
     >
     > The last number on her whiteboard was still a zero. Nobody in the valley could read what was inside those
     > boxes, including the two people who had put it there.

     **Change 2.** In June: "Two growers needed new probes in the first month. They changed them by hand, off the
     card, without throwing anything away." becomes:

     > Two probes died in the first month. Both valves failed shut. The growers changed the probes by hand, off the
     > card, without throwing anything away.

     Notes: "nineteen boxes to go" follows edit 135's twenty-six that afternoon. The bench test already showed the
     answer (probe out, valve clicks open). Grace's "You had both halves of it in your head" stays: she thinks he had
     two halves, and the new line says he had a third. The zero on the whiteboard waits for Ch 26, where Tyler admits
     he can't read his code and the two of them learn to. Curtis's hose is left as it is; it returns in Ch 23.
     Corrected 25 Nov, contradictions pass: "a spare unit" became "a finished unit" (the order is for forty; there
     is no spare).

137. **Chapter 22, at the dinner bell: he tells them about the board.** From the plan for Chapter 19 (section 6, and
     "the bare minimum" in chat, 25 Nov): a secret the reader has been shown has to come out once, and if he confesses
     the leak and still hides the board, the book's first honest confession is half of one. CT: "Go on the plan."
     Book now:

     > ...and stood in his funeral shirt in front of everyone it brought, and read them the timestamps.

     After it, in the same paragraph, add [Claude's wording]:

     > Then, because he was already standing there, he told them about the board too. The startup out of Iowa, the
     > two nights it took, and the two weeks of firmware he had blocked out to make it square. At the back of the
     > crowd, Tyler looked at the floor.

     Then the scene break and "Marta did not raise her voice." as before. Nothing after it changes. The replies
     already in the scene now cover both: Curtis's "You brought their machine inside the wire," and Priya's "we took
     his confidence for a check." The line before it, "He thought about keeping it to himself. Then he pictured Marta
     finding out some other way," points back at Marta's "Now that's ours" (edit 131).
     Corrected 25 Nov, contradictions pass: "the one night it took" became "the two nights it took" (edit 131 has
     two evenings and a night).

138. **Chapter 15: two lines edit 100 left behind.** CT, 25 Nov: "Before we do any more work, you MUST resolve
     contradictions that may have been created." Both were open items under edit 100. Claude's fix: cut, add nothing.

     **Change 1.** Book now, after "Don't ask me. Ask Tyler.":

     > He went and looked. It was there, from April, under eleven hundred other things he hadn't opened. It had
     > been sitting there the whole time.

     Cut. Since edit 100 he has already found and opened her April email at the food bank, so this line contradicts
     it. "He asked for the video call." now follows "Ask Tyler."

     **Change 2.** Book now: "...holding a rich man's empty glass. It could be a cult. It could be nothing, an empty
     shed and a woman who talked too much." Change to: "...holding a rich man's empty glass. It could be nothing, an
     empty shed and a woman who talked too much." Edit 100 already has "It could be a cult with a nice website" a
     page earlier.

**Places to look at, no changes made** (from the other chat's scan for runs where most sentences open the same way
and a big moment is told as a list of events; CT asked only to be made aware of these):

1. Chapter 13, leaving the farm: "He took the amp, a bag of clothes, the notebooks ..." through "He left the key to
   the house on its kitchen table." Strongest candidate. (Edit 82 already rewrites its last line.)
2. Chapter 15: "That was a Tuesday. On Wednesday the delivery app ..." through "He ate the crackers."
3. Chapter 23: "He had sold them Ma's kitchen." gets one sentence before "He circled the link for Reuben" and "He
   built a map."
4. Chapter 37, leaving Grace's farm: "He gave it a week. He turned the compost. He fixed a drip line ..." and "It took
   a morning. A bag of clothes ..."
5. Chapter 31, after the breakdown: "He slept. He got up and swept. He ate what was in the pan." Probably deliberate
   numbness.
6. Chapter 39, Thanksgiving with Ma: "They ate at two on Thursday, in the dining room, off two trays ..." Probably
   deliberate.
7. Probably fine: Chapter 13, "He did not do it well. He said his mother had had a stroke. He said what a room cost
   ..."
8. From this session: Chapter 14 (pages 186 to 195 of the large print PDF), where 50 of 193 sentences start with
   "He". Eight proposed changes were given to CT in chat on 25 November and not logged.


## Needs CT (answered)

Settled by CT on 2026-11-25: keep edit 5 ("chasm"), keep edits 14 and 56 (David's line), keep edit 9 ("first month
here"). The satellite office is in the North Bay. The original questions follow, for the record.

1. **Edit 5, "bridge".** Claude's reading of his dictation: the second sentence becomes "Until he saw what was on
   the other side of that chasm." Confirm.
2. **Edits 14 and 56, whose words Elijah eats.** In v5 Elijah tells David "people land where they put themselves",
   and in Chapter 15 he stands in a food bank line remembering he said it. CT's new bar exchange gives the "they'll
   land somewhere" line to David, so the food bank line now remembers David's words (edit 56). It works, and it
   sets up Chapter 39, where David is the one who knows where the three landed. But it changes Elijah from the man
   who said the callous thing to the man who doubted it. Confirm that is wanted.
3. **Edit 13, where the satellite office is.** Elijah walks into the Bear Flag (Sonoma County) after work on a
   Monday, so the office reads as North Bay. But Devendra "stayed in his house in San Jose" (Ch 25), "kept the job
   in San Jose" (Ch 32) and "stays in San Jose" (Appendix), about two hours away. Also, in Ch 2 the CPO speaks "to
   the room" at this office's all-hands. Say where the office is and Claude will line those up.
4. **Edit 9, "first month here".** Devendra says "Everyone's first month here feels like the apocalypse", but
   Elijah has been at Claypot more than a year by then (his pipeline project was fourteen months earlier). Keep
   "here", or drop it?

## Edits 1 to 86, in book order (all in the Doc as suggestions)

### Author's Note

1. Delete the line "You can doubt my forecast." [CT]
2. Keep "You can rise to meet it." as the close, then add a new line after it: "Let's begin to imagine how." [CT]

The end of the note then reads: "...you might not be paying enough attention. / This could be the most pivotal
moment yet in all of human history. / You can rise to meet it. / Let's begin to imagine how."

### Chapter 0: Three Glasses Up

3. After "The band was called Crop Dust." add "Har har." and end the paragraph there. The next paragraph starts at
   "Nate played bass and Wes played drums..." [CT]
4. "David had called him Mad since they were eight. His grandmother used to walk him..." becomes "...Elijah's
   grandmother used to walk him..." so it is clear whose grandmother. [Claude, at CT's request to clarify]
5. "He thought of himself as a bridge." stays. "Until he saw what was on the other side of that bridge." becomes
   "Until he saw what was on the other side of that chasm." [Claude's reading of CT: "He thought of himself as a
   bridge until he saw what was on the other side of that chasm. We need to change the word there." NEEDS CT.]
   (Chapter 3's "tried, for the third Sunday in a row, to build the bridge" stays; it is the same image.)
6. After "Google drew the engine." and before "PorusAI built the bomb." add: "If Google was Einstein, PorusAI was
   Oppenheimer." [CT, Option A]
7. "David gave him the look too, and then gave him a beer." becomes "David gave him the look too, but at least
   David's looks came with a side of beer." [CT. His first pass was "David gave him the look too, but at least he
   gave him beer", then he reworked the second half to "But at least David's looks came with a side of beer."]
13. Elijah's Claypot office is a satellite office. New sentence before "But Claypot moved like a big company
    moves...": "Elijah worked out of a satellite office, a long way from where anything got decided." [Claude's
    wording, CT's fact. NEEDS CT on where it is.]

### Chapter 1: A Bet for Lamb

8. Where Devendra is introduced (the paragraph ending "He found him at the good coffee machine on the fourth
   floor."), add: "Devendra liked his coffee the same way every day and got very annoyed if it wasn't right." [CT;
   placement Claude's]
9. His quote at the coffee machine becomes: "You'll calibrate. Everyone's first month here feels like the
   apocalypse." He picked up his cup. "I got a mortgage and three kids. I gave up identity crises a long time ago."
   [CT. "You'll calibrate." and "He picked up his cup." are kept from the book. NEEDS CT on "here".]
10. "Three jobs in one bar is an anecdote," Devendra said. "You build models for a living. What's your n?" /
    Elijah didn't have one. / "Fine." Devendra was enjoying himself now. "Give me a date." becomes:

    > "Three jobs in one bar is an anecdote," Devendra said. "You build models for a living. Relax."
    >
    > Elijah didn't relax. He still looked stressed.
    >
    > "Fine." Devendra was enjoying himself now. "You want to play forecaster? Be my guest. Give me a date."

    [CT's lines. "Elijah didn't relax. He still looked stressed." is Claude's wording of CT's beat. "forecaster" is
    lower case; it sets up the moderator's "the people's forecaster" in Chapter 8 and "Hey, forecaster!" in
    Chapter 11.]
11. After Elijah's "Five years. Thanksgiving, 2027. A machine that can do any job in this building.", Devendra's
    "And if it's just a Thursday?" becomes: "Five years," Devendra said. "That's one of the more aggressive ones
    I've heard yet. Okay, fine. And if it's just another Thursday?" [CT, who said "just another Tuesday". Claude
    kept Thursday, because Thanksgiving 2027 is a Thursday and the Appendix says so. "Devendra said" and "Okay" are
    Claude's.]
12. "Loser cooks" becomes "Loser cooks dinner" [CT] in: Ch 1, Elijah's reply; Ch 1, the sticky note ("E.M.
    Thanksgiving 2027. Loser cooks dinner."); Ch 2, the note in the corner; the Appendix ("He took the bet:
    Thanksgiving 2027, loser cooks dinner."). [Placement Claude's.] Left alone on purpose: Ch 6, where he says on
    video "I bet a guy dinner on it. Loser cooks." (the word is right before it), and Ch 7, the T-shirt that says
    LOSER COOKS, which quotes that video.
14. The bar. David's "You sleeping?" stays. Elijah's reply, "Sure. They'll land somewhere," Elijah said. "The
    realtors. People land where they put themselves. Retrain, learn the new thing. Nobody owes you a job.", becomes:

    > "Sure. A little. I can't stop thinking about the people the realtors fired."
    >
    > "They'll land somewhere," David said. "There's always a job."
    >
    > "I'm not so sure about that."

    [CT] David's next line, "What's a job for?", follows as it is, and the rest of the exchange is unchanged.
    Elijah's old speech is cut. See edit 56 for the Chapter 15 line that used to quote it. NEEDS CT (item 2).
15. "Devendra wanted an n. He'd get one. He'd try to break a model himself." becomes: "Devendra wanted a
    prediction. He'd give him a better one. And he'd do it by cracking one of these things open himself." [CT, who
    said "He'd give it one". Claude: "him a better one", because Elijah has already given Devendra a date.]
20. When the tower shuts off, Elijah says "Shit." [CT] The paragraph ends: Black screen. The fans coasted to
    silence. "Shit." The room ticked as it cooled. [Placement Claude's]
16. "The limit he found was heat." becomes: "He had found his first limit. The limit he found was heat,
    specifically overheating." [CT]
17. "The machine that had dissolved three careers at the Bear Flag needed watts. It needed cooling." becomes: "The
    machine that had ended three careers at the Bear Flag needed watts, of course, but it also needed cooling."
    [CT] The paragraph goes on as before ("It ran on the same dumb physics...").
18. "He didn't tell Devendra any of this. One tower in one apartment was an n of one." becomes "He didn't tell
    Devendra any of this. One tower in one apartment wasn't much of a prediction engine." [CT]
19. Last line of the chapter becomes: "He left the tower off for a week. Then he opened the notebook where he'd
    scrawled MADRONE IS NOT A DRONE, turned to a clean page, and started writing." [CT. Changes: "written" to
    "scrawled", "wrote the date at the top" cut, "started keeping track" to "started writing".]

### Chapter 2: The Coin Slot

21. At the all-hands, "He was done being surprised. He would write things down before they happened." becomes: "He
    was done being blindsided. He would try to pay closer attention." [CT]
    Knock-on at the end of the chapter: "That night Elijah sat at the kitchen table with the notebook and did what
    he'd promised. He wrote it down before it happened." becomes "...did what he'd promised. He paid closer
    attention, and he wrote down what he saw coming." [Claude] The list of stages still follows it. (Marta's line in
    Ch 18, "You're trying to watch every bad thing closely enough that it can't surprise you", fits the new promise.)
22 and 25. The texts with Wes. After "Let me look into it, he sent.", the line "He never did." is replaced by:

    > A minute later Wes sent a link. It was a hit piece on how much water Companion was going to drink.
    >
    > is this true
    >
    > Elijah didn't answer. He meant to do it, but he never got the chance.

    [CT: the link to a hit piece about water use, "is this true", Elijah never answers, and "He meant to do it,
    but he never got the chance." The first two sentences are Claude's wording. Companion is the book's name for
    the new Claypot product.]
    Callbacks [CT asked for a throwaway mention of the article]:
    - Ch 6: "Above the box, still, was Wes. is my stuff in that thing. Under it, his own. Let me look into it.
      Nobody had written in there since." becomes "...Under it, his own. Let me look into it. Under that, Wes's
      link to the water article. Nobody had written in there since."
    - Ch 13: "...to Wes. is my stuff in that thing. Under it, Let me look into it. He sat with the two of them for a
      while." becomes "...Under it, Let me look into it. Under that, the link to the water article. He sat with them
      for a while." [Claude]
    - Worth knowing: in Ch 27 Elijah finally answers the water claim, to the co-op: "A question doesn't drink a
      bottle. It's the big sites. The cooling." Nothing to change there.
23. Lena. He does not follow her to her car. Replace everything from "Afterward he went looking for the woman from
    illustration tools." through "She got in and slammed the door. He stood there while she backed out." with:

    > In the shuffle afterward, with everybody talking and comparing notes, some people excited and some maybe
    > apprehensive, Elijah saw the woman from illustration tools gathering her things. He wanted to ask her about what
    > she'd said. He went over. Her badge was clipped to her bag. LENA, it said, and under that, ILLUSTRATION.
    >
    > "Hey," he said, gently. "I liked what you said there."
    >
    > She looked up. She looked at his badge. "You're data team."
    >
    > "Yeah. I mean, I worked on some of it."
    >
    > "Then don't." She started putting things back in her bag.
    >
    > "Look, I'm not trying to…"
    >
    > "I said don't." She zipped the bag. "God, you people don't have any concern for what other people want. You just
    > think about you."
    >
    > She left.

    [CT's beats and dialogue; "You're data team." is kept from the book. The narration is Claude's.] Chapter 9 still
    fits: "A woman named Lena from illustration stood up at our all-hands and asked what the artists get, and nobody
    answered her."
    The next paragraph, "He went back up and found Devendra at the good coffee machine, watching the drip like it
    owed him money.", becomes: "Feeling weird, he went looking for a familiar face, a friendlier one, and found
    Devendra at the good coffee machine, watching the drip like it owed him money." [CT's beat]
24. Devendra after the all-hands. After "The sticky note was still on the side of it.", replace the exchange from
    "Good quarter," Devendra said... through "He rinsed his cup and went back to his desk." with:

    > Devendra looked at him. "You doing okay? You look a little rattled."
    >
    > "Well, I just had a weird exchange with that woman who spoke."
    >
    > "Don't mind people like that," Devendra said. "People like that have always existed. Luddites. They'll come
    > around. They always do. And if they don't, then, well, maybe she should start looking for another job."
    >
    > "Yeah, but you know what they called it when the commons got fenced? Enclosure. The land didn't stop
    > producing. It just stopped being theirs. All you have to build is the fence." Elijah nodded at the screen still
    > glowing through the commons doorway. "Don't we have a responsibility to caretake the rollout? Mitigate some of
    > these effects?"
    >
    > "Why?"
    >
    > They looked at each other for a second. Behind them the commons was thinning out, people drifting back toward
    > their desks.
    >
    > "What do you mean, why?"
    >
    > "I'm not their dad. You're not their mom." Devendra slapped him on the shoulder. "Man. You did a good thing
    > contributing to this. I'm really proud of you. We're going to change the world."
    >
    > Then he turned around and walked away.
    >
    > Elijah was left with a pit in his stomach.

    [CT's lines and beats. Claude: the tags, the commons thinning out, and keeping a short form of the book's
    enclosure lines inside Elijah's question.] Why the fence stays: two later lines point back at it. Ch 6, in the
    layoff meeting, he imagines saying "the realtors, the pipeline with his name in the commits, the fence, the
    notebook." Ch 33, to Grace: "And the fence at Claypot. It's all one thing." Both would lose their meaning if
    the enclosure beat were cut from Chapter 2.
    Cut from the book's version: "Good quarter" and the moat line, the hedges and Parliament, "That's the hedge. I
    helped plant it.", and "You did. And you took the bonus." Nothing later depends on them (the bonus comes up
    again on its own in Ch 10; Reuben gives the full enclosure history in Ch 23).

### Meanwhile (the first one, after Chapter 2: Bidwell and his reader)

26. "Corpus. The body of work. Everything anyone ever made with the software." becomes "...Everything anyone ever
    made with their software and stored on their servers." [CT]
27. "Find out what the dirt costs," he said. becomes "Find out what their dirt costs," he said. [CT]

### Chapter 3: A Satellite Over the Star Thistle

28. The Architect's lecture video:

    > "I am often asked if I am afraid of it," she said. "I am not. I am afraid of us. I am afraid of what mankind
    > might do with such a thing."
    >
    > The pit in Elijah's stomach grew deeper.
    >
    > "We do not exactly have a glowing track record with new technology."

    [CT. Claude: "We do not" instead of "We don't", because she never uses a contraction anywhere in the book.]
    Then "Elijah wrote it all down. Then he watched it again." as before. Her Chapter 9 callback ("I said once, in a
    lecture, that I was afraid of us. I was being polite.") still fits.
70. Who Manny is (CT: "It's Manny. Who the fuck is Manny?"). He is introduced only by name in Ch 3 and Ch 7, and the
    book explains him for the first time after his phone call in Ch 13. He matters later: Elijah ends the book
    sleeping in Manny's back room and digging his soil pits behind Manny's barn. [Claude's wording]
    - Ch 3, on the phone with his mother, after "Pump's doing that thing again. Manny says it's the pressure switch.
      The well man says it's the pump." add: "Manny had the next place over. He had been fixing things on theirs
      since Elijah's father got sick." (Then "A pause, the sound of the pot being set in the rack..." as before.)
    - Ch 13, the call: "It's Manny." The radio was on behind him. "I'm at the house, Elijah..." becomes "It's Manny.
      From next door." The radio was on behind him. "I'm at the house, Elijah..."
    - Ch 13, later: "Manny had smelled it from the yard. Manny had the next place over and had been fixing things on
      theirs since Elijah's father got sick. All his life..." becomes "Manny had smelled it from the yard. All his
      life..." (the introduction has moved to Ch 3).

29. "The phone rang at 9:40 on Sunday, because it always rang at 9:40 on Sunday." becomes "The phone rang at 9:40 on
    Sunday because it always rang around 9:40 every Sunday. That was church time." [CT]
30. The Sunday call is in the MORNING everywhere. [CT: "morning, change the other chapters to match". Every line
    below is Claude's, to make that true.]
    - Ch 3: "She called when her day ended, whether she had seen him that week or not." becomes "She called on her
      way out the door, whether she had seen him that week or not." (The radio, the running water and the pot still
      fit: breakfast dishes before church.)
    - Ch 3, after the call, see edit 61: the satellite he watches has to be at night.
    - Ch 5: see edits 38, 39 and 62.
    - Ch 7: see edit 41.
    - Ch 13: see edit 31. This is the one call that comes at night, on purpose.
    - Ch 15, living in the truck: "At 9:40 that night, back under the sycamore, the phone did not ring." becomes "The
      next Sunday at 9:40 in the morning, under the sycamore, the phone did not ring." The rest stays ("He watched it
      not ring. Then he played the voicemail. After that he did it every week.").
    - Ch 15, before he goes north: "Sundays," he said. "Nine-forty at night. I'm going to call. Could you just hold it
      by her ear?" becomes "Sundays," he said. "Nine-forty in the morning. I'm going to call. Could somebody just
      hold it by her ear?" (He still asks the night aide, who returns in Ch 37.)
    - Ch 17: "The night aide held the phone by his mother's ear." becomes "The aide held the phone by his mother's
      ear."
    - Ch 18: "At 9:40 that night he called the place with the rose garden" becomes "At 9:40 he called the place with
      the rose garden" (Marta came by at eight that morning and soup is at noon). "The night aide" becomes "The
      aide", and "that was all for tonight, honey" becomes "that was all for today, honey".
    - Ch 22, the Sunday of Ray's funeral: "The night before, at 9:40, he called the rose garden." becomes "The
      morning before, at 9:40, he called the rose garden." The aide's "She's been looking at that door all day. Her
      Sunday company didn't come." becomes "She keeps looking at that door. She's waiting on her Sunday company." "He
      took it to mean the church." stays. (Her Sunday company was Ray, who signed in on Sunday mornings and is being
      buried that day; at 9:40 he is not late yet, so she is still waiting.)
    - Ch 24, the first fire in the stove room: "It was a Sunday. At 9:40 he stepped out under the eave and called the
      rose garden." becomes "It was a Saturday. The next morning at 9:40 he stepped out under the eave and called the
      rose garden." (That gathering runs past eleven at night.)
    - Ch 31: "At 9:40 that night he called the rose garden." becomes "On Sunday at 9:40 he called the rose garden.";
      "The aide said she'd had a good day" becomes "The aide said she'd had a good night"; and "In the morning it was
      the first of the month, the day for the pit." becomes "The next morning was the first of the month, the day for
      the pit."
    - No change needed: Ch 24 "The next Sunday at 9:40", Ch 25 ("Elijah called him on Sundays, after his mother"),
      Ch 32, Ch 37 (the night aide; the lamp that "talks to her at night"; the visitor book, "D. McGrath, 10:15").
31. One call comes at night, as a sign something is off with his mother: she thinks it is morning. [CT's idea.
    Claude chose the call and the wording.] It is the Chapter 13 call, the Sunday before her stroke, the one he lets
    ring. Her voicemail from it holds the last whole sentences she ever says to him.
    - Ch 13: "On Sunday at 9:40 the phone rang on the dash. He watched it until it stopped. Then he typed Working
      late. All good. Love you, and sent it, and turned the phone off." becomes "On Sunday at 9:40 the phone rang on
      the dash. It was dark out, and he was too sick to wonder why. He watched it until it stopped. Then he typed
      Working. All good. Love you, and sent it, and put the phone down on the seat, and passed out." (The scene that
      follows is edit 69.) [CT, 2026-11-25: reading "at 9:40" he
      pictures morning, so "Working late" is wrong; his option, "it rang at 9:40 p.m. and Elijah was still too sick to
      notice". Claude's wording. "It was dark out" tells the reader it is night; Elijah doesn't register it. "Working.
      All good." also matches how Chapter 31 quotes his texts.]
    - Ch 13: "There was one voicemail, from Sunday, 9:41." becomes "There was one voicemail, from Sunday, 9:41 p.m."
      (This is where the hour first registers, on Tuesday, when he turns the phone back on.)
    - Ch 14, the voicemail: "Hi, baby. I watched your video." becomes "Morning, baby. I watched your video." The rest
      of it is unchanged.
32. In the notebook: "It takes the people who see it coming, out of the world everyone they love still lives in."
    becomes "...out of the world everyone they love still believes in." [CT]
61. Knock-on of the morning call [Claude]. After the call the book has him at the window watching "a satellite
    dragging itself across the dark", which is the chapter's title image and cannot happen at 9:40 in the morning.
    "After she hung up he stood there a long time. Outside, over the parking lot, the sky had that washed orange
    glow..." becomes "After she hung up he stood there a long time. He was back at the same window that night.
    Outside, over the parking lot, the sky had that washed orange glow..." The rest is unchanged.

### Chapter 4: Cell G14

33. "He typed it in scientific notation, 3.8 times ten to the twenty-sixth watts, and sat back, and felt nothing."
    becomes "He typed it in scientific notation, 3.8 times ten to the twenty-sixth watts, and sat back. He felt
    nearly nothing." [CT: "...and sat back. He felt nearly nothing." Claude kept the number in the sentence, because
    the next paragraph refers back to it.]
34. Last line of the chapter: "The electric bill was in the mailbox that Monday." becomes "The new electric bill
    would show up next Monday, and Elijah was dreading it." [CT]

### Chapter 5: The Tenant Who Paid No Rent

35. The bill: "$211.46" becomes "$2,011". [CT] Knock-on [Claude]: "A hundred and seventy dollars of difference
    between a man who thinks about machine intelligence and a man who runs it" becomes "Nearly two thousand dollars
    of difference between...".
    Note for CT (Claude's estimate, not checked against a real bill): the book says the tower draws 600 watts flat
    out. Running all month that is about 430 kWh, roughly $150 to $250 at California residential rates, so $2,011 is
    about ten times what one tower could run up.
62. Knock-ons of edits 34 and 30 [Claude]:
    - He now dreads the bill, so "This one he opened over the kitchen sink out of pure Monday inertia" becomes "This
      one he opened over the kitchen sink, braced for it". ("The envelope was thin, which fooled him." stays.)
    - The amp scene is now a Sunday morning, so "He unplugged the cable box on his way to bed." becomes "That night,
      on his way to bed, he unplugged the cable box."
36. After the paragraph ending "My dad told me, 'You and your mother shouldn't have to pay the interest on my
    sins.'", a new paragraph:

    > David loved him for it. Whatever else his father had gotten wrong, when it counted he had put the two of them
    > first. That was why Ray still had his stool at the end of the bar, club soda and lime, every night. He
    > sometimes still fell asleep on the bar top, even though he didn't drink. Alcohol is not the only vice.

    [The last two sentences are CT's words. The first three are Claude's wording of CT's beat. CT approved the
    paragraph: "Yeah, that's better."]
37. "Horses don't take anybody's job, Ray," he said. becomes:

    > "Horses don't take anybody's job, Ray," he said, deadpan. He didn't realize how heavy that was. Everybody
    > else did.

    [CT's beat and "deadpan"; the two short sentences are Claude's.]
38. "On Sunday he got the amp out of the hall closet, where it had been sitting in its bag since the last gig before
    the pandemic." becomes:

    > Back home in his apartment that weekend, Elijah was waiting for a call from his mother, and decided to kill
    > some time with a jam. He got the amp out of the hall closet, where it had been sitting in its bag since the
    > last gig before the pandemic.

    [CT] Knock-on [Claude]: "He set it in the corner of the living room and didn't plug anything into it, as a
    monument, which was the point." becomes "He never got around to the jam. He set it in the corner of the living
    room and didn't plug anything into it, as a monument, which was the point."
39. The call that doesn't come. New paragraphs after "...as a monument, which was the point." and before "He put his
    hand flat on the grille...":

    > The call never came. He looked at the clock. It was 10:30. That didn't make sense.
    >
    > He called her. It rang until the machine picked up, and there they were, the two of them, from years ago. His
    > own voice first: "Hello, you've reached the Madrones." Then hers: "Please leave a message after the beep."
    >
    > "Hey, Ma. Haven't heard from you. Hope everything's going okay. Don't make me call the local hospitals, all
    > right? You're probably just busy with Joan. Give me a call when you get a chance, all right?"

    [CT's beats, the greeting and the message. Claude: the first paragraph, "the two of them, from years ago", and
    Joan (Joan Hollis, Ma's neighbor, already in the book) instead of a new "Margaret".]

### Chapter 6: Four Minutes and Eleven Seconds

40. After "He posted the video there, with no caption, because he couldn't think of one." add: "He didn't think
    about it much. He'd been posting on that page for years as a musician. He just wanted to put it out there in the
    world." [CT's beat, close to his words]
    (The band chat line in this chapter changes under edits 22 and 25.)

### Chapter 7: You're Early

42. "By Friday it was four hundred replies and he quit counting." becomes "By Friday it was four thousand replies
    and he quit counting." [CT]
60. Knock-ons of edit 42 [Claude], both in the January scene with David: "He had a senator's office and a lab and
    hundreds of strangers." becomes "...thousands of strangers.", and "there's this woman in Tulsa, there's hundreds
    of them" becomes "...there's thousands of them".
41. "His mother called at 9:40 on a Sunday, the way she did." becomes "His mother called at 9:55 that Sunday. A
    little late, but not terribly unusual." [CT] (In this call the book already has her tell him about the video as
    if for the first time, though she watched it in October and wrote to him about it twice.)
43. "I pour beer, Mad. What's it going to do, pour it?" becomes "I pour beer, Mad. What's it gonna do? Yank the tap
    handle?" [CT; "tap" for his dictated "tab"]

### Chapter 8: Elijah Madrona

44. "They wore a lot of gray and they said off-ramp and guardrails." becomes "...they said guardrails and slow
    down."; "...and they said ship." becomes "...and they said ship and accelerate." [CT]
45. The woman at the coffee urn (the cooling founder). The paragraph introducing her ends "She looked at the room,
    and then at him." in place of "She looked at the room and spoke low, not really to him." Then:

    > "You know, you look pretty green."
    >
    > "I've never done anything like this before."
    >
    > "I thought not." She leaned in close. He could smell her perfume, and it was nice, and he felt a rush. She was
    > pretty attractive. Her hair brushed his cheek, and she said it right into his ear.
    >
    > "Trust no one. Don't take the golden handcuffs."
    >
    > She backed up, looked him right in the eyes, and nodded. "Nobody in here has any friends."
    >
    > Elijah looked around the room. They all looked like friends to him.
    >
    > Then somebody called her name, and her whole face came back on, and she went.

    [CT's beats and dialogue. Narration is Claude's; "her whole face came back on" is kept from the book.] Payoffs
    already in the book: in Ch 12 he texts four people from that room for help and she is the only one who answers,
    with a heart; Ch 14 remembers it. Ruby's million (edit 53) is the golden handcuffs.
46. The panel moderator:

    > "Elijah, your video went parabolic," the moderator said. "And your music is fantastic. We all love what you
    > bring to the table. Now, your biggest video, of course we've all seen it. But some of your recent ones seem to
    > be going into a little more of the nuance of what we're all going through. Tell me, do you fancy yourself sort
    > of the people's forecaster?"
    >
    > The room laughed nicely. Elijah didn't really know how to answer. "I, uh. I mean..."
    >
    > "Don't answer that. Don't worry about it. Listen. Everybody keeps saying AGI. I keep hearing it from all my
    > friends. It hasn't quite hit the mainstream yet. For anybody watching, can you define AGI for us?"

    [CT. Claude: the stammer words, and the room's laugh placed after the forecaster question.] "He knew this. He'd
    watched the Architect's old lecture..." follows as before.
47. After the panel, the woman who sat on his left:

    > On his way out, the woman who had sat on his left found him at the coffee urn. She didn't pat him. "Both sides
    > like you," she said. "Don't ruin that. You have no idea how valuable it is to be able to speak your mind and not
    > worry what anyone thinks about it."
    >
    > "What do you think I should do?"
    >
    > "You want my opinion on what you should do?"
    >
    > "Yeah. To be honest with you, I feel a little out of my depth here."
    >
    > She looked at him. "You are." She picked up her cup. "That's your advantage. You have beginner's luck. What you
    > choose to do with it is up to you."
    >
    > She took her coffee back into the hall.

    [CT's dialogue. "She looked at him." and "She picked up her cup." are Claude's.] Gone: "because you never say
    what anyone should do" and "That's not a forecast. It's a mirror."
48. Ruby by the dumpster:

    > "The replies. Under your video. You answered all of them the first day. I read them."
    >
    > "Yeah. Why wouldn't I?"
    >
    > "Nobody does that, man." He had a quick, light voice, like someone who'd never had to wait for a turn. "The
    > forklift lady. The drummer. Some guy named Earl who thinks you're a demon, and you wrote Earl three paragraphs.
    > There's way too many now. You must have given up."
    >
    > "No."
    >
    > "Then you have to stop that."
    >
    > "Why?"
    >
    > "Because there's four thousand of them and one of you. And tomorrow it'll be eight thousand. Who knows what
    > it'll be next week? Do you know how this game goes?"

    [CT: "the first day", "Yeah. Why wouldn't I?", "Nobody does that, man.", "There's way too many now. You must have
    given up.", and the last line. Claude: Elijah's "No." and Ruby's "Then you have to stop that.", to join them.
    Kept from the book: "I read them.", his voice, the Earl lines.] "He stood up and wiped his hand on his jeans and
    held it out. 'Ruby.'" follows. Gone: "All four hundred, and then you kept going", "next month it's forty
    thousand" and "It's arithmetic."

### Chapter 9: The Wrong Verb

49. In the kitchen, after "The singularity," Ruby said, with his mouth full. and before "It is borrowed from
    physics...":

    > "Do you know what it means?"
    >
    > "Of course I know what it means."
    >
    > "I do not believe you."
    >
    > "It's just a single point."
    >
    > "It is so much more than that."
    >
    > "Okay. Well then, enlighten me."

    [CT. Claude: no contractions for her.]
50. "I would like it to remember you. I spend some of my time on that." becomes "I would like it to remember you. I
    spend much of my time working out how to make it care." [CT, his corrected wording]
51. "The trucker cried," Ruby said. "She didn't like that." CT: very confusing. It becomes: "That trucker she talked
    about? He cried on her," Ruby said. "She didn't like that." [Claude. It points back to her line earlier in the
    scene, "One year it was a man who drove trucks", and explains why she left without meeting Elijah.]

### Chapter 10: Frozen Peas

52. "It tasted like the best night of his twenties." becomes "It tasted like the best nights of his twenties." [CT]
53. Ruby raises the offer. From "It's downstairs. They moved it." through "The truck was at the curb with a full
    tank. He hadn't asked for that either.":

    > "It's downstairs. They moved it."
    >
    > Of course they had. Ruby walked him to the elevator in his socks. He stood there with his hands in the hoodie
    > pocket while they waited for it.
    >
    > "How about half a mill?"
    >
    > "Nah. I'm sorry."
    >
    > "The full million?"
    >
    > Elijah froze. He was really standing there. He was being offered a million dollars, on the spot, just to
    > exist.
    >
    > "Ruby, I really appreciate it, but I really should be going."
    >
    > "Suit yourself, man. Hey, if you're ever in the city, give me a call. I'd love to do this again."
    >
    > He took Elijah's phone out of his hand and thumbed the number in himself, fast, and handed it back. He meant it.
    > A man like Ruby had people to do that for him.
    >
    > "Yeah," Elijah said. "No, yeah. For sure."
    >
    > The doors closed on him standing in all that white.
    >
    > Elijah walked out to his truck, having just turned down retirement. It was at the curb with a full tank. He
    > hadn't asked for that either.

    [CT: the offers ("half a mill" as words, never a number), Elijah's answers, "Suit yourself, man", "having just
    turned down retirement". Kept from the book: the elevator, the city line CT likes, the phone, the doors. The
    rest is Claude's.] It fits what Ruby says earlier on the fire escape, "Everybody says no the first time." The
    first offer was triple his $140,000, about $420,000, so half a mill is a casual $80,000 bump.

63. Why he said no. A new paragraph right after "Elijah walked out to his truck, having just turned down retirement.
    It was at the curb with a full tank. He hadn't asked for that either." and before "He sat behind the wheel with
    the dome light on and looked at the phone.":

    > He didn't know why he listened to her and not Ruby. I mean, Ruby had invited him and made the whole thing
    > happen, but this woman was just some face in the crowd. He didn't even remember her name. But there was truth
    > in her eyes. There was sincerity. He was always someone who had trusted his gut.

    [CT's words, as he said them. Placement is Claude's: it answers the reader's "why did he just do that?" at the
    moment he does it, and points back to the whisper in edit 45.]

### Meanwhile (the second one, after Chapter 10)

54. "Half of it believes him. The other half made a song about him." becomes "...The other half is laughing at a song
    about him." [CT]

### The million, remembered (Chapters 11 to 31)

CT: "When things get hard, he can remember that conversation. When stuff goes on with his mom, he can remember that
talk. But then he can also remember the woman's words." Placement and wording are Claude's.

58. Lines in the book that already mention the offer, brought up to date:
    - Ch 11, in the truck with Gus: "He offered me a job," Elijah said. "Ruby. For doing nothing. Triple what I
      made." becomes "...For doing nothing. A million dollars." Gus's answer changes under edit 64.
    - Ch 31: "He had turned down the triple salary and the ads and the room." becomes "He had turned down the
      million dollars and the ads and the room."
55. New lines:
    - Ch 12, sick in the truck outside the launch party, thumb over Ruby's number. After "One more person who wanted
      something." add: "Six months ago that kid had offered him a million dollars at an elevator, and he had said
      no."
    - Ch 14, under the madrones, at the end of the paragraph that ends "...a face was worth exactly a heart from a
      woman with a cooling company. He had bolted two million dollars of robot arms to a floor and he was not on the
      list." add: "He had turned down a million dollars at an elevator. Trust no one, she had said into his ear.
      Don't take the golden handcuffs. He had taken her advice, and here he was."
    - Ch 15, paying for his mother's room, after "Every twenty he took out came off the far end of her room." add:
      "A million dollars would have pushed the far end of that room out past where he could see it. He did that
      division too, once, and then he stopped doing it."

### Chapter 11: It's Always a Strap

64. In the truck with Gus, after "You take it?" / "No.": "Good. The ones for nothing are the expensive ones." becomes
    "Good. The ones they offer you for nothing usually cost the most in the end." [CT]
    With edit 58 the exchange reads: "He offered me a job," Elijah said. "Ruby. For doing nothing. A million
    dollars." / "You take it?" / "No." / "Good. The ones they offer you for nothing usually cost the most in the
    end."

65. Gus's pitch for the show. He plays his cards too soon (CT: "Nobody would do that if they're trying to sell
    somebody on an idea"), so the admission moves to after Elijah says no.
    - Cut from the pitch: He kept his eyes on the road. "Truth is, I've got a shop full of arms nobody wanted and a
      bus with nobody in the other seat. I'm tired of driving it alone." The pitch ends on "I'll fly you out to the
      shop next week. Let's do it." and goes straight to "It was a good idea. Elijah could see it."
    - After Elijah's no and "Elijah braced. He figured the air would change...", Gus's reply "Your choice," Gus
      said. "I can't force you to do it." becomes:

      > "Yeah, I figured," Gus said. "Thought I'd ask, though." He kept his eyes on the road. "Truth is, I got a
      > bunch of arms nobody wants, and I'm just tired of driving alone. If you ever do want to, though, I'll give
      > you my number."

    - Then "Gus reached over and turned the radio up a little..." as before.
    - At the cannery dock. "When the last arm was off the truck, he took a pen out of his jacket and wrote on the
      back of a gas receipt and handed it to Elijah." stays. The next line, "Here's my phone number. Give me a call if
      you ever want to talk about anything.", becomes:

      > Elijah started to tell him he didn't have to.
      >
      > "No, take my number. I meant it. Here." He pushed the receipt at him. "Give me a call if you ever want to talk
      > about anything."

      Then the rest as before: "Okay. Thanks. I mean it, thank you." / "Sure." / the bus to go look at / "Oh, by the
      way. I saw that you're working on a book. Let me know when it comes out." [CT: "No, take my number, I meant
      it. Here." Claude: Elijah starting to wave it off, so Gus's "No" answers something, and "He pushed the receipt
      at him." "Give me a call if you ever want to talk about anything." is kept from the book. Elijah's "I mean it"
      now echoes Gus's "I meant it".]

    [CT's lines; "tired of driving alone" for his dictated "driving along". Claude: "Gus said", "He kept his eyes on
    the road" (moved from the cut paragraph), and "I'll give you my number" as the way he offers it, since he hands
    it over at the dock. Writing context from CT, not for the page: Gus had a feeling Elijah would say no, which is
    why he lets it slip. The chapter already counts him as billionaire number two: "Two billionaires, two phone
    numbers."]

66. Why he is at the cannery: the promise is two of the arms (CT: "the promise is that he's going to get two of the
    arms, that they'll be his. That's where the connection is. And that's where his insurance policy is ... It's
    enough to survive off of. It's his big emergency fund that comes into play later in the book. But right now, it
    just needs to be more clear how this bridges with the rest of the stuff.") In v5 the arms only turn up in
    Chapter 15, as a surprise, "in place of his wages". Now they are the deal from the start. [CT's facts; all
    wording Claude's; no dollar figures added.]
    - Ch 11: after "I can carry stuff," Elijah said. "I drove delivery for six years. I'm good at carrying stuff.",
      the line "So they let him carry stuff." becomes:

      > Trent thought about that. They had six robot arms coming down from Oakland, a launch party in three weeks
      > and nobody to put them in. They also had two spares in crates that they were never going to need. "Tell you
      > what," he said. "Ride down with the arms. Help the crew bolt them in for the launch. Do that, and the two
      > spares are yours."
      >
      > Elijah didn't know what one of those was worth. He knew it was more than he had. It wasn't a salary. It was
      > an insurance policy, something to stand on if the floor went out.
      >
      > So they let him carry stuff.

    - Ch 11, when Gus prices them. After Gus's paragraph that starts "About three-thirty apiece, installed." and
      before Elijah's "They're yours?", add a line: "Elijah did the arithmetic on two of them and kept it to
      himself."
    - Ch 12, first line: "He worked at the cannery for three weeks on a promise." becomes "He worked at the cannery
      for three weeks on Trent's promise."
    - Ch 12, the paid guy at lunch: "'You on the books?' Elijah said they were sorting him out Friday." becomes
      "'You on the books?' Elijah said he was getting paid in arms. Two of them, Friday." The guy's answer stays:
      "He's done this to two guys already. You're working for a picture, man." So does "Elijah said Trent was good
      for it." and Trent's "We'll sort you out Friday."
    - Ch 15: "In the second week Trent's office finally wrote back. There was no money for him, a woman said, and
      she was sorry about that. But two spare arms were still sitting on the cannery dock in their crates, never
      unpacked, and the company would sign them over in place of his wages if he could get them off the property by
      Friday." becomes "In the second week Trent's office finally wrote back. The two spare arms were still sitting
      on the cannery dock in their crates, never unpacked, a woman said, and the company would sign them over, the
      way Trent had promised, if he could get them off the property by Friday." The rest of Chapter 15 stays: the
      storage unit, no bids on eBay, the scrap offer, "there were always the arms. He could sell them." That is the
      insurance policy failing to pay out, which is the point.
    - Nothing changes later: the arms go north in Ch 17, and in Ch 34 to 37 they are the emergency fund that comes
      into play.

### Chapter 12: The Seventeen-Dollar Shower

67. Sick in the truck after the launch party. The jump to "if he died" is too fast (CT: he's not depressed, he's
    overwhelmed and sick from doing too much; he doesn't want to bother anybody, he already feels like enough of a
    bother, so he decides to sleep it off in the truck; the "if he died" line is his humor, and it gets worse from
    there). After "The phone went face down on the dash.", the paragraph "He wasn't angry. He was too sick to be
    angry. He'd spent ten months saying yes to people. If he died in this truck tonight, the party would go until
    one. Somebody would notice the Ranger on Monday. They just didn't have a place to put him." becomes:

    > He wasn't angry. He was too sick to be angry, and too tired. He'd spent ten months saying yes to people on four
    > hours of sleep, and somewhere in there his body had stopped asking his permission. He didn't want to be a
    > bother. He had been underfoot at his mother's, and a lot at the Bear Flag, and one more person who wanted
    > something everywhere else. He'd sleep it off. People slept things off in trucks all the time.
    >
    > He pulled the jacket up to his chin. If he died in this truck tonight, he thought, the party would go until
    > one, and somebody would notice the Ranger on Monday. It was almost funny. They just didn't have a place to put
    > him.

    [CT's beats. Claude's wording; "underfoot" calls back his mother's "You're underfoot" in Chapter 11, and "one
    more person who wanted something" calls back the Ruby text a few paragraphs earlier. "It was almost funny." is
    there so the line reads as his humor. "They just didn't have a place to put him." is kept from the book.]
    Chapter 13 still opens "In the morning the fever was down enough to drive.", which is him having slept it off,
    and things get worse from there.

### Chapter 13: The Buckets in the Barn

68. First lines of the chapter. "In the morning the fever was down enough to drive. He did not go in to get sorted
    out." becomes "In the morning the fever was down enough to drive. He decided not to go to the hospital. He was
    tough. He could tough it out." [CT]
    Note: "go in to get sorted out" probably meant going into the cannery office to get paid, echoing Trent's "We'll
    sort you out Friday". With CT's line that echo is gone; the arms deal (edit 66) is still settled in Chapter 15.
69. The morning after the night call (CT: he passes out, wakes Monday in the truck, the phone is dead, he starts the
    truck to charge it and waits; no direction, just reflecting; choked up but can't cry, still in go mode; a young
    couple sharing a cup of frozen yogurt; he wants that; he thinks about his last relationship a few years ago, how
    it went, and remembers why he isn't dating and doesn't plan to soon). Replaces "He turned it back on Tuesday, to
    look for work." Everything between the night call (edit 31) and "At two in the afternoon the phone rang in his
    hand" becomes:

    > When he woke up it was Monday. He had slept in the truck all night, sitting up, with his jacket over him. The
    > first thing he did was reach for the phone. It was dead.
    >
    > He needed a charge. He started the truck, plugged the phone into the lighter, and sat there with the engine
    > running and the needle on a quarter tank.
    >
    > Downtown Stockton went about its Monday. A man hosed off the sidewalk in front of a check-cashing place. A bus
    > went by with nobody on it. He didn't have anywhere to be. That was new. For ten months there had always been
    > somewhere to be, and now there was a side street, and a truck, and a phone that wouldn't turn on.
    >
    > His throat got tight. He waited for it to turn into something, and it didn't. He was still in go mode. Some
    > part of him was still standing on the cannery dock, waiting for Friday.
    >
    > Across the street was a frozen yogurt place. A couple came out of it, young, sharing one cup with two spoons,
    > bumping shoulders, arguing about something that made them both laugh. He watched them all the way to the
    > corner.
    >
    > He wanted that. He hadn't let himself want it in a while.
    >
    > The last time had been a few years ago. It had gone the way his things went. He'd said yes to everything and
    > been easy to be around, and one day there wasn't enough of him left to be with. She had said that, more or
    > less, on her way out. He'd told her she was right, and he had meant it.
    >
    > That was why. He had nothing to offer anybody right now but a truck and a list, and he knew exactly how he would
    > do it again.
    >
    > The phone came on. There was one voicemail, from Sunday, 9:41 p.m. He would listen to it later. He would listen
    > to it a great many times.

    Then "At two in the afternoon the phone rang in his hand, and it was her number. She never called at two in the
    afternoon." as before; the call from Manny is now on Monday. [CT's beats. Claude's wording. The ex is not named
    and gets no details beyond why it ended; nothing else in the book mentions a past relationship. Why it ended is
    Claude's: his saying yes until there is nothing left, the pattern the book already gives him ("Yeah. No, yeah, of
    course" in Ch 7, Wren's "You were saying yes the way people say it when they mean please" in Ch 31). It sets up
    Grace, where Ch 25 has him asking Marta "Does Grace have... someone?"]

71. After Manny's call: "He didn't remember the drive. He remembered the gauge." becomes "He didn't remember the
    drive." [CT] ("The gauge" was the gas gauge: a quarter tank, no money, two hours to Santa Rosa. Nobody could
    tell.)

72. At his mother's kitchen table, finding there is nobody to call. "...He had not heard her voice since the funeral,
    and he did not want to hear it now. He went down the list twice, to be sure." / "He was the call." becomes:

    > ...He had not heard her voice since the funeral, and he did not want to hear it now.
    >
    > He got up and went down the hall and ran cold water over his face. He went through the list every which way,
    > but the only person to call was staring at him in the bathroom mirror.

    [CT's last sentence. Claude's bridge: "He got up and went down the hall and ran cold water over his face.", so
    the mirror is really there; he was sitting at the kitchen table.]

73. The hospital woman with the lanyard. "Is there anybody else in the family who should be part of this?" / "No." /
    "Then it's you," she said, and she was sorry about it. becomes:

    > "Is there somebody else?"
    >
    > "No. It's just me."
    >
    > She nodded, with a knowing smile, and that was it.

    [CT]

74. The messages after the clip. "He read every one. His mother had raised him to answer a letter. He couldn't answer
    these, and he couldn't stop reading them." becomes "He read every one. His mother had always raised him to be
    someone who wrote back. He couldn't bring himself to answer these, but he also couldn't stop himself from
    reading." [CT]
    Knock-on [Claude]: the same phrase first appears in Ch 7, when the first messages come in: "They had taken the
    trouble to write, and his mother had raised him to answer a letter." becomes "...and his mother had raised him to
    be someone who wrote back." so the Ch 13 line still reads as a callback.

75. The illustrator in Petaluma. "One was from an illustrator in Petaluma he had never met. You built the thing that
    took my clients. Now you want my twenty? He read that one more than the rest." The last sentence becomes "He only
    needed to read that one once. It bounced around inside his head, rent-free, for days after." [CT]
    The message itself stays "Now you want my twenty?" (CT quoted it as "now you want my money"; "twenty" ties to the
    next paragraph, where he sends Tulsa her twenty back.)

76. In the hospital hallway. "...Forty feet away his mother was asking a nurse for Barry. He could not make it fit in
    one head, and the head was his." / "He didn't answer any of it." becomes:

    > ...Forty feet away his mother was asking a nurse for Barry.
    >
    > It was too much.
    >
    > He didn't answer any of it. He put his phone away and went for a walk to go buy cigarettes.

    [CT. Claude kept "He didn't answer any of it." because it closes out the offers in the paragraph before. He
    already smokes by then: Ch 12, "He had started smoking again in February, on a fire escape."]

77. The trust paper. "After his father died, and after Melody stood up at the funeral lunch and asked what the place
    was worth, a lawyer in town had put it in a trust. Elijah had signed a page at twenty-six and never thought about
    it again. He found it in the drawer under the bank's envelopes. It said that if she couldn't, he could." becomes:

    > After his father died, and after Melody stood up at the funeral lunch and asked what the place was worth, a
    > lawyer in town had put the farm in a trust. Elijah had signed a page at twenty-six and forgotten about it,
    > until now, going through his mother's important papers. He found it in the drawer under the bank's envelopes.
    > It named him the successor trustee. In plain words, it said that if she couldn't, he could. The farm was his to
    > sign for, and his to sell.

    [CT's beats: he signed at 26 and forgot, finds it rummaging through her papers, and the paper has to say what it
    is. Claude's wording and the legal term. CT suggested "executor of the will and power of attorney, or something
    like that"; an executor only acts after a death, and she is alive. For a farm held in a trust, the person who
    steps in is the successor trustee, and that is what lets him sell it to the man from Sacramento in the next
    scene. Claude's general knowledge, not checked with a lawyer.]
78. After the trust paper, before the man from Sacramento. Elijah sits with what the paper means and thinks about
    calling Ruby or a few other people, and then a car pulls in (CT: "A very nice yellow Oldsmobile. You don't see
    those anymore."). "The man from Sacramento came Monday, in a clean pickup, with a folder." becomes:

    > He sat at her table with it a long time. If she couldn't, he could. The farm, the barn, the well with the
    > pressure switch, his grandmother's hill. All of it was his to sign for now, and he had never signed for anything
    > bigger than a truck.
    >
    > He got the phone out and scrolled to ruby, lower case. A million dollars, at an elevator. He could call and say
    > he had changed his mind. He scrolled past it to Gus, and to David, and back up to ruby, and sat there with his
    > thumb over the screen.
    >
    > A car pulled into the driveway. It was a very nice yellow Oldsmobile. You don't see those anymore.
    >
    > The man from Sacramento got out with a folder.

    Then the next paragraph opens with a new sentence [CT]: "He was polite and kind, but firm. He was very sorry
    about Elijah's mother..." and goes on as before. ("He" for CT's "The man from Sacramento", since the line before
    already names him.)
    Knock-on: the notary's Camry is gone (edit 79 moves the signing to the bank), so the Oldsmobile is the only car.
    [CT: "we need to keep it consistent".] [CT's beats and the Oldsmobile lines. Claude's
    wording otherwise. The man no longer comes "Monday, in a clean pickup"; he arrives in the middle of this. Ruby's
    number here is the golden handcuffs coming back (edits 45, 53, 55).]

79. He doesn't just sign (CT: he'd tell the man to get bent, snap, yell, all the stress finally comes out; "I'll
    fucking figure it out"; he thinks of the robot arms and how they could be leveraged, everything he could have
    done, the money he turned down; then the dam breaks and he sobs over the kitchen counter where they made
    Christmas dinner, over the sink where his mom washed his hand after he took a digger and the gravel chewed his
    palm up, covered it in Crisco, an old wives' tale that kind of worked, and bandaged it; he looks around the house
    where he spent so much of his life wishing to be anywhere else; he calls David, who doesn't pick up; he cries
    harder, goes to bed crying, wakes up crying; when he gets himself together he thinks of everyone he could call
    for advice and comes up empty). After the man names the outfit ("...They liked the valley, he said."), and
    before "A notary came out and they did it on the kitchen table" (edit 78), insert:

    > Elijah stood up. "Get bent."
    >
    > The man didn't move. "Mr. Madrone..."
    >
    > "No. You don't get to come in here with a folder while she's lying in that bed." He was yelling. He could hear
    > himself, and he couldn't stop, and ten months of it came up at once. "That's my grandmother's hill out there.
    > This is her kitchen. I'll fucking figure it out."
    >
    > The man set the folder on the table, squared it to the edge, and put his card on top. "The offer's good through
    > Friday," he said. "I am sorry about your mother." The Oldsmobile backed down the drive.
    >
    > Elijah sat back down. He would figure it out. He went through it. The two arms Trent owed him, still crated on
    > the cannery dock; he had heard Gus say what one of those cost. The million he had turned down at an elevator.
    > The stages, the podcasts, the rate he didn't have. All the things he could have done, and hadn't.
    >
    > Then the dam broke.
    >
    > He sobbed. He stood over the kitchen counter where they had made every Christmas dinner of his life, and he
    > sobbed over the sink where his mother had washed out his hand the summer he took a digger in the driveway and
    > the gravel chewed his palm up. She had covered it in Crisco, an old wives' tale that kind of worked, and
    > bandaged it. He looked around the house where he had spent so much of his life wishing he was anywhere else.
    >
    > He called David. David didn't pick up.
    >
    > He cried harder. He went to bed that night crying, and he woke up the next morning crying.
    >
    > When he finally got himself together, he sat at the table and thought of everyone he could call for advice. He
    > came up empty.
    >
    > After staring at the card the man had left behind for what felt like an hour, Elijah picked up the phone.
    >
    > Before he signed anything, he took it all to the bank, to make sure what he was doing was legit. He may have
    > been naive, but he wasn't an idiot. The banker went through every page and said the paperwork was in order,
    > and asked if he wanted to use the bank's notary. He did. Elijah signed where the yellow tabs were, and the bank
    > faxed everything over to the man from Sacramento. Going through somebody in the middle made it all feel a
    > little safer.
    >
    > A few days later, on Friday, the wire cleared. The money went into an account that said Linda Madrone across
    > the top, with his name under hers, and the place with the rose garden took the first of it that afternoon.
    > Elijah knew his mother was safe.
    >
    > He did not keep any. He thought about it for the length of time it took the notary to find her stamp.

    This replaces the book's "A notary came out in a Camry and they did it on the kitchen table. Elijah signed where
    the yellow tabs were. On Friday, when it closed, the money would go into an account that said Linda Madrone
    across the top, with his name under hers, and the place with the rose garden would take the first of it that
    afternoon. / He did not keep any. He thought about it for the length of time it took the notary to find her
    stamp." [CT: the card and the phone, the bank first, "He may have been naive, but he wasn't an idiot", the bank's
    notary, the bank faxing it over, the intermediary feeling safer, the wire clearing a few days later, "Elijah knew
    his mother was safe". The DocuSign line from CT's earlier message is dropped, since his newer version runs it
    through the bank. Kept from the book: the yellow tabs, the account in her name, the rose garden, and the notary
    finding her stamp, which now happens at the bank. "On Friday" keeps David's later "Heard they close Friday"
    true.] "The buckets went with the place. He did not bring them up, and neither did the man." stays. [CT's beats and lines ("Get bent", "I'll fucking figure it out", "Then the dam broke" in
    substance, the digger, the Crisco, "came up empty", the card and the phone). Claude's wording otherwise.]
    Claude's calls:
    - The arms. In the book they only become his, and go into storage, in Chapter 15 (edit 66). Here they are still
      "the two arms Trent owed him, still crated on the cannery dock". CT said "the robot arms that he put in
      storage"; moving them into storage this early would need Chapter 15 reworked. CT can say so.
    - David. Later in this chapter: "David showed up Thursday morning with a hand truck in the back of his pickup. /
      Elijah hadn't called him. Nobody had." Now Elijah did call. That line becomes "Elijah had called him once and
      he hadn't picked up. Manny had called him." (CT chose Manny; see edit 81.)

80. Pruitt, outside the Bear Flag. He appears only in this chapter. "There were two men smoking out front. He knew one
    of them. Pruitt, who had the tire shop." becomes "There were two men smoking out front. He recognized one of
    them: Pruitt, from the tire shop, who had put every set of tires on the Ranger since Elijah bought it." [CT: "He
    recognized Pruitt from the tire shop. Or something like that." Claude's wording; the Ranger detail is added so
    the reader knows why Elijah knows him.]

81. David shows up Thursday with the hand truck. After "David showed up Thursday morning with a hand truck in the back
    of his pickup.", the book's "Elijah hadn't called him. Nobody had." becomes "Elijah had called him once and he
    hadn't picked up. Manny had called him." Then add: "He didn't mention the call. Neither did Elijah." Then
    "'Heard they close Friday,' David said." as before. [Claude's lines; CT approved both and chose Manny as the one
    who told David. Manny is at the farm that morning, lives next door, and David already knows him ("Manny's always
    right" in Ch 7).]

82. The last line of the chapter jumps from the rose garden to the farmhouse. "He left the key to the house on its
    kitchen table, on top of the mail." becomes a new paragraph:

    > Friday morning, he said goodbye to his childhood home, and to what he had always assumed would be his
    > inheritance. Everything he'd taken for granted. For some reason, all the tears he'd cried there were unavailable
    > to him now. Elijah simply laid the house key down on the kitchen table and allowed the door to lock behind him.

    [CT. Claude: "Friday morning," as the opening (CT dictated "Friday. Morning."), "now" for "in that moment", and
    "previously" dropped after "cried there". The tears are the ones from edit 79.] Chapter 14 follows as before.

### Chapter 15: The Twenty, Folded Small

83. Grace's invitation asks first (CT: he's been through a lot and won't just trust strangers from the internet; she
    is polite, asks permission and consent, asks what he wants; "We have a farm. We'd like to have you on it";
    "obviously we know who you are, but also that's not the point"; people up here think he'd bring a lot to the
    group; an offer to come stay a little while if he'd like; they don't expect him to take their word for it or to
    just come; a video call or two if he wants; "Up to you"). Her reply after "I don't want a boss. I don't want to be
    one either." / "She answered in an hour." keeps its first paragraph ("Good. We already have a welder who thinks
    she's the boss..."). The next line, "Come see. I'm sending gas money. If you hate it I'll buy your gas home too.",
    becomes:

    > We have a farm, and we'd like to have you on it. Obviously we know who you are, but that's not the point. The
    > point is, people up here think you'd bring a lot to the group, and we'd like to offer you the chance to come
    > stay with us for a little while, if you want to.
    >
    > We don't expect you to take our word for it, and we don't expect you to just come. You can get to know us
    > first. If you want, we could do a video call or two. Up to you.
    >
    > If you do come, I'll send gas money. If you hate it I'll buy your gas home too.

    Then "Blessings, / Grace / P.S. Eat something first..." as before.
    Later, the video call: "Early Sunday she put him on a video call with the kitchen." becomes "He asked for the
    video call. Early Sunday she put him on with the kitchen." The rest of that paragraph stays.
    [CT's beats and most of the words. Claude: the order, "If you do come" for the gas money, and "He asked for the
    video call", so it is his choice. It echoes the Architect in Ch 9: "I work on whether it asks first."]

84. His answer to the way she asks. After Grace's reply ("...Blessings, / Grace / P.S. Eat something first. It's two
    days of driving and you look thin.") and before "He read the last three words again.", add:

    > There was something about the way she asked that reminded Elijah of the truth he had seen in the eyes of the
    > woman from the conference. As burned and cautious as he was, something in him felt a tug.

    [CT] It points back to edit 63 ("there was truth in her eyes") and the whisper at the coffee urn in Ch 8 (edit 45).
    "The woman from the conference" replaces CT's first "the woman at Ruby's party", which could be read as the night
    at Ruby's place in Ch 10; CT approved the change.

56. The food bank line. "He got in it. Once, at the Bear Flag, he'd told David that people land where they put
    themselves. He stood in that line forty minutes, and he couldn't find one person in it who had." becomes "He got
    in it. Once, at the Bear Flag, David had told him people land somewhere. There's always a job. He stood in that
    line forty minutes. This was somewhere." [Claude, forced by edit 14. NEEDS CT (item 2).]

### Chapter 16: The Red Bin

85. Marta at the plasma table. "She jerked her chin toward the sparks. 'That could be worth something. Not an app.'"
    becomes "She gestured with her chin toward the sparks. 'That thing right there is worth something, not some
    app.'" [CT] It now points plainly at the work on the table; "In the quiet the plasma table ticked as it cooled."
    follows as before.
86. Marta hands him the broom. "'Swarf goes in the red bin,' she said. 'We'll see.'" becomes "'We'll see,' she said.
    'Swarf goes in the red bin.'" [CT] Her answer comes first, and the chore lands last; the chapter is named for the
    bin.

### Chapter 25: Long Enough to Laminate

59. Devendra: "I have a mortgage and two kids in a good school" becomes "I have a mortgage and three kids in a good
    school", to match edit 9. [Claude]

## Continuity pass, 2026-11-25

CT asked Claude to sit with all the edits and make sure the repo is fully up to date. Claude read every edit against
the whole v5 text (3,600 paragraphs), searching for every later line that points back at something an edit changes.

Found and fixed in this file:

- **Edit 7** had dropped "David gave him the look too". Restored as CT first said it.
- **Edit 14** cut a line that Chapter 15 quotes back at the food bank. See edit 56 and "Needs CT".
- **Edit 24** would have cut the enclosure exchange that Chapters 6 and 33 point back to ("the fence"). A short form
  is kept inside Elijah's question.
- **Edit 9** (three kids) contradicted Chapter 25 (two kids). Edit 59.
- **Edit 53** (the million) made two existing lines out of date, in Chapters 11 and 31. Edit 58. The Chapter 13
  memory line moved to Chapter 12, where he already has his thumb over Ruby's number.
- **Edit 30** (morning calls) put the Chapter 3 satellite in daylight (edit 61), sent Elijah "to bed" at 10:30 in
  the morning in Chapter 5 (edit 62), and left "she'd had a good day" at 9:40 a.m. in Chapter 31. The Chapter 22
  call is reworked around Ray's funeral, and the Chapter 15 line is simplified.
- **Edit 34** (he dreads the bill) contradicted "out of pure Monday inertia". Edit 62.
- **Edit 42** (four thousand replies) left "hundreds" twice in Chapter 7. Edit 60.
- **Edit 51** no longer invents a "last guy with a notebook"; it points at her own line.
- **Edit 10**: "forecaster" in lower case.
- **Edit 5**: read from CT's own sentence as "chasm". See "Needs CT".

Checked and fine as they are: the LOSER COOKS T-shirt (Ch 7), "Hey, forecaster!" (Ch 11), Marta's "can't surprise
you" (Ch 18), Lena in Chapter 9, the Architect's "I was being polite" (Ch 9), the heart from the cooling founder
(Ch 12 and 14), the visitor book (Ch 37), "Everybody says no the first time" (Ch 10), the Appendix timeline.

Not changed by any edit but worth CT's eye: the back cover says "A few weeks later, they fired their social media
team"; the book says one week, and names a transaction coordinator, a marketing person and the kid who made their
listing videos.

## Applied

- **v6, 25 Nov (third logging chat), on CT's "Make a new google doc for v6 ... Go on the plan ... it's go time."**
  `manuscript/tools/edits-v6/make_v6.py` took the v5 Doc (read 25 Nov, revision unchanged all day) with every
  suggestion accepted, applied edits 87 to 138 from `ops.py`, and checked every row of `checks.py`: all pass. The
  v5 Doc was not touched. The .docx (19 pictures, made 800 pixels wide to fit the Drive connector) became the Google
  Doc "StS v6 draft (Nov 25)", now CURRENT in the bridge map. Then CT: "Before we do any more work, you MUST resolve
  contradictions that may have been created." Seven fixes, made in ops.py and directly in the v6 Doc (edit 138 and
  the corrections noted under 88, 131, 136 and 137). Read back: all 138 edits accepted, and the Doc's text matches
  make_v6.py's output word for word. The large print PDF built from that read (659 pages) is in the Drive folder
  "StS v5 Publication Files" as surviving-the-singularity-v6-large-print-6x9.pdf; the copy from before the fixes is
  titled "OLD (before contradictions pass)". Left out on purpose: the placeholder for Grace's April email (edit
  100), which is CT's to write.
- Author's Note, 2026-11-25: "They may tell you they moved on because I was an asshole, and they might be right."
  and "But I'm not wrong about our trajectory." Entered in the Doc as suggestions. Still pending in the read of
  2026-11-25 (revision AHj4eMResiURoAJEhT0nN-6E), with the rest. The publication files were built as if accepted.
- All edits 1 to 86, 2026-11-25: entered in the Doc as suggestions, through the Appendix, and read back after each
  batch. Nothing accepted yet. CT's rulings above went in as written. Checked again the same day by a separate
  session against a fresh read: every edit present. Record: `EDITS-v5-applied.md`.
- Follow-ups CT asked for on 2026-11-25, also suggestions:
  - The power bill is $2,011.46 in Chapters 5, 19 and 21 (CT: "$2011.46 in all places"; the comma matches the
    book's other amounts).
  - CT chose to keep the bill and explain it: "A rate hike cuz he went over a limit of some kind." Chapter 5, "One
    month. One month of training runs..." becomes "He had gone over some limit the utility set, and once he crossed
    it, the rate jumped. One month. One month of training runs..." [Claude's wording of CT's beat]
  - North Bay office: "in San Jose" cut from Devendra's lines in Chapters 25 and 32; the Appendix's "He stays in San
    Jose." becomes "He stays put." [Claude]
  - Chapter 13: "it took the notary to find her stamp" becomes "it had taken the notary to find her stamp", since the
    stamp now comes at the bank, before the wire. [Claude]
- Checked and left alone: Chapter 7, where Ma talks about the video as new. The book already says, right after,
  that she watched it in October and wrote to him twice; it is her memory going, before the stroke.
- Back cover (`publication/novel/build/book.json`): "A few weeks later, they fired their social media team" becomes
  "A week later, ...", to match Chapter 0 ("One week later, almost to the hour").
