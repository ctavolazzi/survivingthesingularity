# Edits to the novel: the running list

Running list, started 2026-11-25. These are CT's edits to the v5 manuscript (Google Doc "StS v5 draft (Nov 23)").

**Where the edits stand (27 Nov, end of the eleventh logging chat):** edits 1 to 223 are in the book, the Google Doc "StS
v8 draft (Nov 26)", made on CT's word from `manuscript/tools/edits-v6/make_v6.py`'s build (the v5 Doc with its
suggestions accepted, then every row of `ops.py`). Each of those entries still says where it stood when it was logged
("Logged only; not in the v6 Doc yet."); that is its history. Edits 224 to 233 (tenth and eleventh chats) are logged only,
until CT clears them for the Doc. The next edit is 234.

**So nothing gets dropped:** every edit has a check row in `manuscript/tools/edits-v5/checks.py`. Run
`python3 manuscript/tools/edits-v5/verify.py READ.json --table manuscript/novel/EDITS-status.md` on a fresh read of the
v8 Doc; `EDITS-status.md` is the one table of where each edit stands (all 223 "accepted" on 26 Nov). A copy of this list
lives in Google Drive as "StS edit list, edits 1 to N (mirror of GitHub)"; the link to the newest one is in
`EDIT-LOGGING-PROCEDURE.md`, step 10. It is refreshed once, at the end of a session.

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

## Direction from CT, 26 Nov: Chapter 20 to the end (context, not for the page)

Given while reading Chapter 20, after the first readers' passes. Nothing below is an edit yet.

- CT: "this is the part where there's the payoff for all of that suffering that Elijah went through. So, like, are we
  doing what we should be doing here? ... Does Priya have a good arc? Does Curtis have a good arc? Does Lou guide
  everyone and help shape these people in his way where he's kind of silly, but also kind of serious? Is there a
  moment where we get to see different sides of the characters? ... Does the dialogue feel like natural? ... Do we
  have satisfying conclusions to the stuff that we put out there, or is it just like a series of events?"
- CT: "dialogue should be where a lot of the character traits, backstory, ideas, decisions, things that are
  discussed, dialogue should be where it is. And right now I feel like a lot of what I'm reading is just sort of a
  series of events that transpire without chutzpah ... Not always. There's quite a lot of special sauce in there.
  There's some memorable stuff. But I feel like we could chop, cut, remove a lot of the like filler and chaff, and we
  can replace it with ... this is the reduction process ... We're making a risotto, and we can use metaphor, simile,
  idioms. We can use the beauty and the color of language to make it more than just interesting events. We can make
  it impactful. We can make it relatable, topical, relevant, timeless, archetypal."
- CT: "Marta wanting to set Grace and Elijah up, and then having that actually pay off should take several chapters.
  There should be little bits where the reader is like, yeah, but I'm interested in this other thing that was going
  on over here ... The pond is where they should have like their first kiss, because obviously, right? Like
  obviously. I don't even know in the story where they have their first kiss right now."
- CT: "one of the strongest ways that we can flesh things out is to have the characters ask each other questions and
  then answer to the best of their ability, and have other characters interject to correct things that are wrong, but
  be wrong about things as well. These characters are not infallible, and they're not just pawns in a plot to deliver
  a sermon. I'm trying to figure out how to make them fully realized and have their story arcs really impart something
  memorable. I don't feel like the text currently does that, and I feel like chapter 20 is where I personally am
  starting to lose interest and where things are starting to get a little repetitive. We need to add some conflict.
  We need to add some drama. We need to add obstacles for the characters to overcome. Like, we've just seen that they
  can work together really well. They shipped 40 units. Things are going great. We need setbacks. We need problems.
  We need challenges for them to face."
- CT: "I love the way the book ends. It made me cry ... The end of the book is really good. I think we close out a lot
  of threads ... The argument between Grace and Elijah is pivotal, but the events leading up to the fire, all of the
  things that they've been through together, all of the challenges that they've overcome, the setbacks that they
  face, losses. There needs to be, like, stakes. Somebody needs to leave the farm. And it hurts. They leave for greener
  pastures. They give up. They decide that it's not worth it. Like, they give up on the vision too soon. That's a
  normal thing that would happen." So: Chapter 37 to the Epilogue stay; the work is Chapters 20 to 36.
- CT, on Elijah and Grace: "One of the big things I think we are overlooking is the will they, won't they push and
  pull between Elijah and Grace. We don't want the kiss to be sudden. We want it to be obviously foreshadowed and set
  up. Like, they like each other. They had that little moment where they were laying on the ground. Maybe there could
  be a line somewhere after that happens where they, like, shoot glances at each other. But something external
  prevents them from taking it further, and something internal inside Elijah prevents him from taking it further,
  where he is like, yes, I want to, but, like, also, I don't know. He thinks back on his pain from his prior
  relationships. And we don't need to get into the details there ... he's gotten involved with a coworker before, and
  this kind of feels the same. He learned a long time ago not to date where you eat, but there was just something so
  alluring about Grace. And then we can list some of her character traits. Like, Elijah loves that she's intelligent.
  He loves that that she's assertive. He loves that she cares so much. But in order to have him love those things,
  you know, she's strong-willed, but she can be silly. We need to show those parts of her. We can't just list them. I
  feel like a lot of this book, as I'm reading it right now, is kind of a lot of lists. And I want it to feel a
  little bit more vivid without being heavy-handed and without going over the line."
- CT, on the kiss, the year after it, Ma, and the letter scene: "I like it better if it's the fall, but it's to prevent
  him from leaving. The kiss is to prevent him from leaving. There needs to be another few months of like a will they,
  won't they. Maybe a full year goes by before he really like decides to go for it. He does something romantic that's
  meaningful to her personally. There needs to be backstory there that informs it, that's written somewhere in the
  book that foreshadows what he's going to do. He remembers. It's really sweet. We don't just drop his mom off the face
  of the earth either, right? There needs to be another conflict that maybe happens with his mom, like he has a scare.
  And he's like, maybe I need to go home right now. Like he goes home a couple of times to visit her on holidays and
  stuff, and he's writing her letters ... we can write a scene right now where he is writing a letter and Grace comes
  in to talk to him and sits on his desk, and it reveals some sort of like personal conflict that foreshadows the
  blowout fight that causes him to leave. They have their first little tiff, and she's like, why are you acting this
  way? And he goes, because I just, and he scratches his head and he breathes to try and calm himself down ... He
  grabs his hair up on the top of his head and he's like, I've lost a lot of people who were important to me, okay?
  I've been through a lot. Finishing this book is really important to me. You are really important to me. This farm is
  really important to me. These people are really important to me. And she's like, so then why can't you just whatever
  ... I don't know what she wants, but whatever it is that she wants, she's confronting him about it ... And he's
  like, because it's just, it's not fair. And she'll be like confused and like take a step back and cross her arms.
  Fair to who? And he's like, I don't know. Don't worry about it. And she's like, you're almost 40 and these are your
  conflict resolution skills? And he looks at her and ... he almost gets mad. And then he decides to just let it go,
  realizing, you know, it's not worth it to fight over something like this. He's like, Grace. He takes her hands. He's
  like, look, I'm sorry, okay? I'm sorry. Do you want to go into town and get ice cream? And she lights up ... but
  she's still a little mad. You can see it in her eyes ... She squints to show him that she's mad, but grins just a
  little bit. And she's like, I want frozen yogurt. And that makes them go to the store where Tyler is, where they
  have whatever pivotal conversation they have with Tyler."
- CT, on visiting Ma (after Claude's push-back that a visit home would break the visitor book in Ch 37): "I feel like
  that's fine ... he wants to go, he means to go. But it's just, it's too hard. And like, she's not even there anyway.
  And maybe one of the characters can even say that to him on the farm. Like, he's packing up, he's getting ready to
  leave. Because he feels like he just has to. He feels like he should. But then maybe someone, I don't know who, can
  ask him questions like, what are you going for? ... He's like, just to see her, just to show up. Like, I need to go
  see her. It's the right thing to do. And then they're like, I mean, is it? He's like, he just like looks at them
  like stunned. What do you mean? I mean, you said so yourself, like, all she says is Barry. And he's like, yeah, but
  she can still recognize me. Like, she still knows that I'm there. And like, does she? And he's like, I'm going. All
  right. And then he goes. And he gets maybe 100 miles before that check engine light comes back on. And he realizes
  that he really doesn't have enough money to fix it if it breaks on the road. He doesn't have anyone to ask. He can't
  take money from the fund that pays for his mom's care. And the best bet he has to get that money is on the farm
  with these people. He thinks through, like, maybe he could sell, go back to doing music ... Maybe he could make
  some art, sell it on his page ... But as he's thinking through the options, parked at a truck stop, he remembers
  the $17 shower and how desperate that felt and how awful that was. And he realizes he, even though he does have just
  enough to get there and back with gas, food, and everything else, at this point in time, it's just too big of a
  risk. And that just fucking eats him up, just tears him up. He gets emotional. A single tear slips out of his eye.
  He puts the truck in drive and flips a U and heads back towards the farm. Disappointed in himself for a whole bunch
  of reasons. He shows back up in the next part, or maybe the next chapter, and everybody's like, we thought you were
  going home. Not everybody, but like, you know, the people that knew ... Grace is excited, right? She sees him come
  back and she tries to hide her excitement, but she can't really hide it. Marta notices that Grace is excited. Lou
  notices that Grace is excited too. And if we weave it into the right part, then maybe this would be like Lou maybe
  realizing that those two like each other. Or if he's already known ... him like confirming something that he
  already knew. I don't know. You can read enough of the book to figure it out ... Let's finish the fight."
- CT, on the storm, power, the rover and the argument about being replaced: "The county goes dark for 3 days? That's
  ridiculous. That's not believable at all ... We need to change that to overnight. We also need to add power when it
  counts, and the farm needs to get a rover, one of those high tower rovers. And they need to discuss how to use it to
  do labor. And when they are discussing how to use it to do labor, there needs to be a philosophical argument, of
  course, about being replaced. And then Lou says, we're not being replaced, we're expanding our capacity. We're having
  productivity gains. And then Elijah has a flashback to what they said at Claypot. And Curtis isn't so sure because
  he's seen a lot of movies. And Curtis is like, next thing you know, we got government surveillance drones flying all
  over us. And he's like, I need to go build an EMP. And then he walks off and Lou shakes his head. And Marta's like, or
  whoever's there, Patricia maybe, if she's there, she's like, you're not actually going to let him build an EMP, are
  you? That's wildly illegal. And if it's Marta that says it, that's great. If it's Patricia that says it, that's also
  great. Maybe Priya says it, whoever's there in the scene, and it makes the most sense. And Lou's like, I'll go talk
  to him. And then he leaves. But since Elijah's the narrator and he's like the focal point of the story, we don't see
  that conversation. What we see is Elijah's apprehension and guilt. And we don't need to say Elijah was apprehensive
  and guilty. We need to show it."
- CT, on fans, wingnuts and the teacher: "Denny should get excited that they have fans online. There should be a
  conversation somewhere in there where Priya cautions him about crazy people and wingnuts. And he's like, what do you
  mean? And she's like, I ran for office, don't you remember? Like, there are some wild people out there. And then she
  looks over at Elijah and she's like, I mean, you know what I'm talking about, don't you? And Elijah does ... This is
  an opportunity for him to reflect. Like, yeah, he got some cool opportunities. Yeah, there were some wonderful
  things that happened. But also, he remembers some very hateful DMs that he got, and the way that his friends treated
  him, the way that his, community treated him was really hard, was really tough. We need to add a part at the
  beginning when his video first goes viral, talking about like how he's surprised with the backlash. He thought he
  was doing people a favor, but the messages that he gets from people online, like let's say his one of his old school
  teachers throws him a message. Somebody that he admired, somebody he really looked up to, like maybe his Spanish
  teacher. And the message that he gets from that guy is extremely condescending, negative, rude, mean, spirited ...
  And then something in the environment needs to happen so that it calls his attention away from it, and then it
  moves the story forward." (The teacher's lines are in edit 196.)
- What the book has now (corrected 26 Nov; Claude first told CT there was no kiss, which was wrong): one kiss, in
  Chapter 25, in the shouse after a Friday dinner ("she leaned down and kissed him, once, and stayed there with her
  forehead on his"), and her truck still in the gravel the next morning. Earlier in Chapter 25: Marta's scene ("You
  like her." ... "Don't make me sorry."), then the blanket by the amp ("her head came over and rested against the side
  of his, and stayed"), then Marta's nudge to Grace ("somebody ought to bring him something loud"). They become a
  couple off the page: Chapter 26 only says she wears his shirt and "where she slept now". The pond appears three times
  (Ch 17 frogs, Ch 18 and Ch 37 birds) and is never described or used for a scene.

### The plan for Chapter 20 to the end (Claude's draft, 26 Nov; nothing logged, waiting on CT)

**The current map is `PLAN-CHAPTERS-20-TO-36.md`** (same folder), written later the same day. What follows is the
earlier working: the readers' findings, plan v2 and the 59 line flags.

Made from five readers' passes over make_v6.py's v6.txt (setups and payoffs, Elijah's arc, the co-op cast, moments
told instead of shown, relationships), every anchor grep-checked. Their verdict on CT's question: the personal threads
mostly land (David and the bar, "Barry", the amp, the coupon that "became the steel", Curtis's fence, Rosa), and
Chapters 37 to 39 carry weight. It still reads as a series of events because (1) Chapters 20 to 30 are separate lessons,
each solved inside its chapter and ending on a notebook line; (2) the late payoffs are handed to Elijah by someone else
(David, Devendra, Lou); (3) outward threads go quiet (Bidwell's planted "somebody", the bet, the board secret, the
route's January, Marta's welder gap). Cast: Priya has a role, not an arc; Curtis's arc is good but undone in one line in
Ch 34; Lou lands through a job or a joke and turns into a lectern in Ch 33 and 35, is never wrong at a cost, and shapes
only Elijah and Curtis; Wren, Reuben and Denny are flat; dialogue works short and in a trade, is forced as a thesis.

**Plan v2 for Chapters 20 to 36 (Claude's, 26 Nov, after three more readers: timeline and stakes, who could
leave, Grace and Elijah beat by beat; CT keeps Ch 37 to the Epilogue as they are).** What the readers found: in Ch 20
to 36 the group never loses anything lasting (no money, land, member, customer or building; only the leaked data and
"Six CSA households canceled", never mentioned again). The route's money is restated, not escalated. Mrs. Delgado and
her insulin are first named at the fire. Denny's burnout, the county study, the welder gap and Bidwell's "somebody"
are dropped. The first kiss is in Ch 25, in the shouse; they become a couple off the page (Ch 26, "where she slept
now"). The pond is never a place. The ladder, each rung a loss that stays lost:
1. Ch 21, June 2025: the first heat wave. A controller on Patricia's network fails and a grower loses a house of
   starts (heat is Elijah's "first limit", Ch 1). Tyler traces it to the board; Elijah knows it is the AI-made part
   and says nothing. Patricia's Ch 27 pledge ("No generated code") then has a reason.
2. Ch 22, July: the leak and the bell; he confesses both, and people react. The six households that cancel get a
   number on the page, and the hole it leaves is the first money trouble. The hour of Ray's funeral passes on the page.
3. Ch 23: the trust saves the land, but the down payment takes the channel's surplus; Reuben's pages on a missed
   payment are planted.
4. Ch 18, 22, 24, 25: Marta's matchmaking spread across chapters (now all in Ch 25). Ch 25: the kiss moves from the
   shouse to the pond, where in Ch 17 he joked "this is a pretty good bleed-out spot".
5. Ch 26 and 27, 2026: one short beat of them as a couple in place of "where she slept now"; Grace pays for his pay
   vote with Curtis; Mrs. Delgado seen once on the route, through Rosa or Grace.
6. Ch 29 and 30: Denny's burnout named, the tool company's offer real, the welder gap open.
7. Ch 31, February 2027: Denny leaves for the tool company. The goodbye is on the page and it hurts. The channel's
   money stops and the trust payment is at risk; Elijah's $800 visitor plan becomes his panic fix (it already puts
   Denny's bench in it); the table turns it down; the tea circle.
8. Ch 32, March to June: Denny gone, Elijah alone with the signs; the route misses a delivery for the first time.
9. Ch 33, June: Denny comes back, quietly, before the July dinner (his Ch 33 and 34 lines, his porch in Ch 37 and
   the Thanksgiving livestream all stand, and mean more).
10. Ch 34 (optional): the north-house couple ("he'd take a robot over another October") leave for good after the
   arms are tabled, so "eighteen people short" is real and festival week costs what it says.
11. Ch 35: Lou's night sermon cut down. Ch 36: the fire now lands on things the reader saw.
Questions for CT: the heat failure as the spine; Denny leaves and comes back (or someone else, or for good); the kiss
at the pond; the north-house couple.
CT's answers (26 Nov): "Kiss at the pond, yes, but we need a good setup for it. Denny leaves and comes back. Yeah, that
sounds right. That sounds fine. The North House couple leaving permanently, yes. But that doesn't really add serious
stakes because we don't know them. The heat failure as the spine, I need a little more explanation for that."
Claude's idea for the couple (not decided): make them the grower who loses the starts in the Ch 21 heat failure, the
houses node 7 cut off in the Ch 28 storm, and the ones who leave in Ch 34, so the reader knows them and their leaving
is the bill for Elijah's shortcuts. They need names.
CT (26 Nov), yes to the heat failure and to the couple: "That hurts. That's good. Like, this is why we can't blindly
trust the machines. We need to double check everything. Like, we can lean on them for a lot, but for the critical stuff
that cannot fail, we need to do it ourselves to the best of our ability. I mean, of course we need to use the tools,
but there's an old IBM quote, and I think Lou should say it ... a machine cannot be held accountable, therefore a
machine should never make a management decision. And then, like, the starts are lost, yes, and that's a huge blow, but
it's not a break moment. It's not like he ruined everything. Elijah's going to feel terrible and want to leave. He's
going to, try to retreat in shame, but grace should stop him. And then that's what sets up their kiss."
(The IBM line, from a 1979 IBM training slide, reads "A computer can never be held accountable, therefore a computer
must never make a management decision." Lou can say it his way.)

**Spine (Claude's proposal, CT to decide):** one running problem from Ch 20 to about Ch 30 that the co-op gets wrong
before it gets right: the forty controllers go bad in the field. The failing part is the board Elijah made with an AI
(Ch 19); Tyler knew; Patricia is the customer; Marta's "zero people can fix it" is the problem; Curtis, Priya, Denny and
Lou each argue it their own way and are each partly wrong (CT: "characters ask each other questions ... other
characters interject to correct things that are wrong, but be wrong about things as well").

**Threads, each a small set of edits (replace telling with a scene; the book doesn't get longer):**
(The quoted lines below are the readers' placeholders for what each beat says, not prose. Several are the mirrored
contrast shape CT has ruled out; every line gets written fresh, in the characters' own voices, before CT sees it.)
A. The board secret comes due. Ch 22: the one-clause confession becomes a choice ("because Tyler was standing at the
   back") and gets reactions: Curtis "Twice", Tyler "It said so in the file", Grace "And the board. In front of that
   kid." Feeds the spine.
B. Grace and Elijah. Marta's nudge grows across chapters (now one line, end of Ch 24); first kiss at the pond (CT);
   Ch 31: the morning after on the page, Grace choosing "Nothing that mattered", Elijah telling her "I'm not okay";
   Ch 37: the lamp makes him hear "You're the lamp"; Ch 39: Grace on the "could" side (he can knock, and let her slam it).
C. Lou fallible. Cut the Ch 35 night sermon to the walnut, "The man who refuses to launch it" and ALC; Grace to Lou in
   Ch 38, "He got that from you"; on the step in Ch 37, "I told you people change their own. I didn't tell you to quit
   showing up while they did."
D. Members against each other. Ch 38: Grace and Patricia ("I'm the one who asked Tyler"); Ch 34: Curtis, "He's on this
   side of the fence. His friends aren't."; the free-files vote's bill (Ch 27 Grace and Frank; Ch 38 Curtis to Marta,
   "Ship them, you said", and Priya's margin note costs her); Ch 38: Wren, "It had mine too. Nobody thanked me."; Tyler
   and Wren at Thanksgiving; Ch 37: Marta, "I told you not to make me sorry", and she steps out of the door; Ch 26:
   Grace, "He asked it looking at me."
E. Elijah closes his own threads. Ch 33: "I sold it to them" (pays FOUNDER HIDES THINGS; Reuben); Ch 37: the uncashed
   checks endorsed to the route; Epilogue: Marta gets "They ate"; the bet paid with Devendra's lamb photo and the rubber
   band off the first notebook; a copy at the desk for M. Madrone; Ch 39: David's forgiveness after the apology, not
   before; one line to Denny ("I forgot your warehouse").
F. On the page, not summary. Festival week (Elijah picks Lou's squash row; "Guy with arms"); the hour of Ray's
   funeral passing (Ch 22); Tyler's yes to the apprenticeship (Ch 29); the land trust closing with Lou there (Ch 23);
   the morning Tyler loses his job (Ch 25); Devendra's call reaching Ma (Ch 37).
G. Dropped threads. Bidwell's "somebody" folded into Devendra ("They asked me to keep calling you. I'd have called
   anyway."); the Hollis cousins kept or cut; the route's January answered in Lou's picture in the Epilogue; Marta's
   welder gap closed at "It became the steel"; the manuscript seen being written once.
H. Repetition cut. Ch 28 node lesson (repeats Ch 22); the resentment that lands twice (Ch 31 and 34); the Ch 39
   can/can't list and the lines that explain what the actions already show.

**Line flags, Chapter 20 to the end** (59 given to CT in chat on 26 Nov; not logged; the ones inside a thread above
are handled there). Same order as in chat: Ch 20: "She'd eaten his too"; Wren's "call you back". Ch 21: "had been the
internet". Ch 22: Ray's words "A club soda with a lime"; "the first one they'd read". Ch 23: the power bill "said so";
"the kitchen-table meeting". Ch 24: "the place were his to run"; "nothing got built only once"; "where no room had
been". Ch 25: "augmented, not replaced"; paired the phone "so she wouldn't see his hands"; the truck song and the laugh;
"confessed to it". Ch 26: "spread it in all directions"; inches and centimeters; Lou's "man". Ch 27: Walt's card "two
lines under"; "pinned it at the paint"; "I'm just saying"; "did the pipes"; Irene's towels. Ch 29: "one he did not
keep"; Priya's margin note; "Marta or Frank"; "make one finished". Ch 30: "changed more to the rest"; Lou's "man" twice.
Ch 31: Marta's "I've lost one" (maybe deliberate); Melody's number "could still hear it"; "a year in the city". Ch 32:
the date "with his initials"; Reuben's "six years". Ch 33: "wrote well"; Wes's "It went to the TV"; "nobody asked the
three of them"; the empty line under Curtis's name; "Nights at the hospital in Ukiah"; Marta's fence (check her oh-nine
story); Lou's "Here."; the 50-word hinge sentence. Ch 34: the price list. Ch 35: the steam engine; Lou's "man"; "In the
same lane"; "this lady". Ch 36: "cross it". Ch 37: "before theirs did". Ch 38: "race her to the rail"; "looked at
Marta"; "what could be considered a wink". Ch 39: "Marta had heard it as a murder"; "one number blocked"; "a glass went
down"; "Not for good"; "Manny's well, four feet down"; "a hinge and a gatepost"; "donned".

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

**Settled 26 Nov.** CT asked Claude to answer these with its best reasoning, then: "OK." Nothing in the edits changes.
1. Go: done (edits 131 to 137).
2. Chapter 19 stays with Elijah. A scene at the car would make the storyteller give Patricia away or visibly hold back.
3. Tyler's line stays as logged in edit 135: "You could've just told them." It echoes his Ch 38 line to Patricia.
4. Curtis puts the question to Elijah (edit 135). He is the one who distrusts the machines; it leads into his mood in Ch 20.
5. The secret comes out in Chapter 22, at the bell (edit 137), so his first confession is a whole one.

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

     **Settled by CT (26 Nov):** keep the line. "Then back to what?" Edit 180 makes it "then back at Elijah."

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

     **Settled by CT (26 Nov):** "if he wanted to play" stays; she is talking to Lou about Elijah, so it is the clear
     one. CT: "Always clarity." Lou's "I know you were." is Claude's.

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
     **Settled by CT (26 Nov):** the touch lines and "Your knowledge earns your keep here, Elijah. That's all." stay
     (Claude's wording for his beats; "marketing" is his word); the last line is changed by edit 181. The Chapter 17 notebook ending ("Ask. Don't guess." / "What's your solution?") is unchanged.

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
     **Settled by CT (26 Nov):** the co-op's gravel lot. Edit 183.

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

     Settled (CT, 26 Nov): keep "been here before."

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
     Changed 26 Nov by edit 182, item 6: "the board" became "the circuit board" (the whiteboard is "the board" on the
     same page). This part of 137 is in the v6 Doc, so 182 changes it there too when it goes in.

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

139. **Author's Note: "But this is different."** CT (26 Nov, reading v6): "Was a thing that did a thing. The shovel never
     dug its own hole. I want to say in between those two lines, but this is different." Book now:

     > Everything humanity ever built before was a tool that does a thing. The shovel never dug its own hole.

     Change to [CT's words]:

     > Everything humanity ever built before was a tool that does a thing. But this is different. The shovel never
     > dug its own hole.

     Logged only; not in the v6 Doc yet.

140. **Author's Note: what he asks of the reader.** CT (26 Nov): "I am asking them to trust me, so we need to change
     that." He tried "I'm not asking you to take me at my word" and "I'm not asking you to just blindly accept this",
     then: "No, none of those are good. If I can ask anything of anyone, it's that you take a look at this for
     yourself." His last version kept. Book now:

     > I'm not asking you to trust me. I'm asking you to take a look for yourself.

     Change to [CT's words]:

     > If I can ask anything of anyone, it's that you take a look at this for yourself.

     The next lines, "Get your goddamn hands on it." / "Use it yourself." / "Then you'll know.", stay. Logged only;
     not in the v6 Doc yet.

141. **Author's Note: no scene break before "This could be the most pivotal moment".** CT (26 Nov): "I don't really
     understand why there's 3 stars there at the end. Right before this could be the most pivotal moment in human
     history. Let's remove those stars." The stars are the build's scene-break mark, made from an empty paragraph in
     the Doc between "...you might not be paying enough attention." and "This could be the most pivotal moment yet in
     all of human history." Change: delete that empty paragraph, so the two lines follow each other like the rest of
     the note. No words change. Logged only; not in the v6 Doc yet.
     Done 26 Nov, and the cause found: the blank paragraph was made by a bug in make_v6.py (when a suggestion joined
     two paragraphs, it left a blank one behind). Fixed in the tool, and all 12 such blanks (here, Ch 2 before
     Devendra's "You doing okay?", Ch 11, and two in Ch 13) deleted from the v6 Doc on CT's yes.

142. **Chapter 1: "So it had a ceiling."** CT (26 Nov): "So it had a ceiling. The ceiling was a power bill. That's
     confusing because we didn't talk about power before that. We talked about heat. So it had a ceiling. Just leave
     it at that." Book now:

     > So it had a ceiling. The ceiling was a power bill. Whoever could pay for the power and the cooling could have
     > as much of it as they wanted.

     Change to [CT's cut]:

     > So it had a ceiling. Whoever could pay for the power and the cooling could have as much of it as they wanted.

     The rest of the paragraph ("He stood at the window in his boxers...") stays. Logged only; not in the v6 Doc yet.

143. **Chapter 2: Wes's "is this true" in italics.** CT (26 Nov): "The 'is this true' line is not italicized in Wes's
     text. It needs to be." The book sets texts in italics (*is my stuff in that thing*, *Let me look into it,* he
     sent). Book now, after "A minute later Wes sent a link. It was a hit piece on how much water Companion was going
     to drink.": the line "is this true" in roman. Change to: *is this true*, in italics. No words change (edit 22's
     line). Logged only; not in the v6 Doc yet. verify.py reads words, not italics, so make_v6.py checks this one.

144. **Chapter 2, the dated page: "so later he could look back and see if he was right."** CT (26 Nov): "So later he
     couldn't pretend he hadn't seen it coming. That's confusing as well. So later he could look back and see if he
     was right is better." Book now:

     > He dated the page and put his initials next to the date, so that later he couldn't pretend he hadn't seen it
     > coming.

     Change to [CT's words]:

     > He dated the page and put his initials next to the date, so that later he could look back and see if he was
     > right.

     Logged only; not in the v6 Doc yet.

145. **Chapter 5, the amp and the call: he starts to play, and the call he was expecting.** CT (26 Nov): "We got some
     confusing wording here. The call never came. The call he was expecting never came. And also he never got around
     to the jam. That's also confusing. He started playing but didn't continue because he noticed the time." Both
     lines were edits 38 and 39 (the "never got around to the jam" was Claude's knock-on). Book now:

     > He never got around to the jam. He set it in the corner of the living room and didn't plug anything into it,
     > as a monument, which was the point.
     >
     > The call never came. He looked at the clock. It was 10:30. That didn't make sense.

     Change to [CT's beats and "The call he was expecting never came."; the first sentence is Claude's wording of
     "He started playing but didn't continue because he noticed the time", and "again" is Claude's knock-on]:

     > He plugged in and started to play, but a few bars in he noticed the time and stopped. He set the amp in the
     > corner of the living room and didn't plug anything into it again, as a monument, which was the point.
     >
     > The call he was expecting never came. He looked at the clock. It was 10:30. That didn't make sense.

     Why "again": the book says he "didn't plug anything into it"; now he plays first, so it would contradict itself
     without the word. Logged only; not in the v6 Doc yet.

146. **Chapter 6, Nina in the parking structure: "Keep your head down and stay focused for me."** CT (26 Nov): "Head
     down for me is confusing. Let's say she says, keep your head down and stay focused for me. And then the next one
     is, he meant to, he wanted to, but life gets in the way sometimes." Book now:

     > He thanked her. She hugged him, there in the parking structure, which nobody at Claypot did. "Head down," she
     > said. "For me."
     >
     > He didn't put his head down. He didn't know how anymore.

     Change to [CT's words; "she said" placed by Claude]:

     > He thanked her. She hugged him, there in the parking structure, which nobody at Claypot did. "Keep your head
     > down and stay focused for me," she said.
     >
     > He meant to. He wanted to. But life gets in the way sometimes.

     Logged only; not in the v6 Doc yet.

147. **Chapter 6: "For a year he had tried explaining it to each of them one at a time."** CT (26 Nov), confirmed: "Yes,
     that's what I want." Book now:

     > For a year he had explained it to every one of them, one at a time.

     Change to [CT's words]:

     > For a year he had tried explaining it to each of them one at a time.

     The rest of the paragraph ("He'd explained it across the bar and over the gate latch and in the van...") stays.
     Logged only; not in the v6 Doc yet.

148. **Chapter 9, the swinging door: Elijah stays on the other side.** CT (26 Nov): "It needs to be very clear that Elijah
     is on the other side of the swinging door. Like, it swung shut. Ruby walked through the door, it swung shut behind
     him, closing Elijah off from seeing what was going on, but he could still hear." Book now:

     > Ruby shouldered through the swinging door. It swung shut behind him.

     Change to [CT's words; "from the hall" is Claude's, to place him]:

     > Ruby walked through the swinging door, and it swung shut behind him, closing Elijah off from seeing what was
     > going on. But from the hall, he could still hear.

     Then ""I brought you one," Ruby said on the other side." as before. The round window is already "papered over
     from the inside", so he can't see through it. Logged only; not in the v6 Doc yet.

149. **Chapter 10, the text to Ruby: "for the life of him."** CT (26 Nov): "He couldn't write a billionaire without
     wanting something, and for the life of him, he still couldn't figure out what he wanted." Book now:

     > He couldn't figure out how to write to a billionaire without wanting something, and he couldn't figure out what
     > he wanted.

     Change to [CT's words]:

     > He couldn't write a billionaire without wanting something, and for the life of him, he still couldn't figure out
     > what he wanted.

     Logged only; not in the v6 Doc yet.

150. **Chapter 11, Trent's deal: he says it himself.** CT (26 Nov): "Instead of just declaratively stating that they have
     two spares, let's make Trent say it. Trent pondered for a moment and then said, you know what? And then said,
     you know, tell you what. You say you're good at carrying stuff. I got a lot of things that need to be carried,
     and some of them are quite expensive. If you do the work, we got two spare robot arms with your name on em."
     His last version of the opening kept ("tell you what"). Book now (edit 66):

     > Trent thought about that. They had six robot arms coming down from Oakland, a launch party in three weeks and
     > nobody to put them in. They also had two spares in crates that they were never going to need. "Tell you what,"
     > he said. "Ride down with the arms. Help the crew bolt them in for the launch. Do that, and the two spares are
     > yours."

     Change to [CT's words; kept from the book, so the trip to the Oakland warehouse that follows is still set up:
     "They had six robot arms coming down from Oakland, a launch party in three weeks and nobody to put them in." and
     "Ride down with the arms. Help the crew bolt them in for the launch."]:

     > Trent pondered for a moment. They had six robot arms coming down from Oakland, a launch party in three weeks
     > and nobody to put them in. "Tell you what," he said. "You say you're good at carrying stuff. I got a lot of
     > things that need to be carried, and some of them are quite expensive. Ride down with the arms. Help the crew
     > bolt them in for the launch. If you do the work, we got two spare robot arms with your name on 'em."

     Cut: "They also had two spares in crates that they were never going to need." Then "Elijah didn't know what one
     of those was worth..." as before. Logged only; not in the v6 Doc yet.

151. **Chapter 11, Gus's offer: no scene break before "It was a good idea."** CT (26 Nov): "In the scene where he's talking
     to Gus, there's 3 dots above. It was a good idea, Elijah could see it, but the 3 dots have been used more to
     indicate like time passing or a big scene change. This doesn't seem like that." The stars come from an empty
     paragraph in the Doc between Gus's "...I'll fly you out to the shop next week. Let's do it." and "It was a good
     idea. Elijah could see it." Change: delete that empty paragraph. No words change. Logged only; not in the v6 Doc
     yet.
     Done 26 Nov, and the cause found: the blank paragraph was made by a bug in make_v6.py (when a suggestion joined
     two paragraphs, it left a blank one behind). Fixed in the tool, and all 12 such blanks (here, Ch 2 before
     Devendra's "You doing okay?", Ch 11, and two in Ch 13) deleted from the v6 Doc on CT's yes.

152. **Chapter 12, the cannery lot: why he doesn't go stay with his mother.** CT (26 Nov): "We need a line somewhere in here
     that makes sense for why he doesn't just go stay with his mom. Like, why doesn't he just go stay with his mom?"
     Book now, end of the paragraph that starts "'We'll sort you out Friday,' Trent said":

     > ...and at night he slept in the cab of the Ranger at the far end of the cannery lot, with the windows cracked
     > and a towel over the wheel.

     After it, a new paragraph [Claude's wording, from the book's own facts; the last sentence and "Not again. Not
     after what happened last time." are CT's correction, 26 Nov]:

     > The farm was two hours north, and his mother would have left the porch light on for him. But gas there and
     > back every day was more than he had, and she had sent him off to be useful. He wasn't going to walk back
     > through the door with nothing to show for it. Not again. Not after what happened last time.

     The reasons are all in the book: "Home was two hours north" (later in this chapter), no money until Friday, and
     Ma's "Go be useful, baby. You're underfoot." (Ch 11). Then "By the end of the first week he needed a shower..."
     (edit 97) as before. Context from CT, NOT for the page: what happened last time is never explained ("we just
     don't ever need to, like, go into that"). Logged only; not in the v6 Doc yet.

153. **Chapter 13, after Manny's call: "He left immediately."** CT (26 Nov): "In front of he didn't remember the drive, we need
     to say he left immediately. He didn't remember the drive." Book now, after Manny's "...Linda's alive. They took her
     to Santa Rosa.":

     > He didn't remember the drive.

     Change to [CT's words]:

     > He left immediately. He didn't remember the drive.

     (Chapter 0's "He didn't remember the drive home." is a different scene, after the bar; it already has "Elijah
     left without looking up." before it.) Logged only; not in the v6 Doc yet.

154. **Chapter 13, the kitchen: "When he got to the house, he saw what had happened."** CT (26 Nov): "The line, 'the pot was
     on the stove,' needs to be changed to, 'when he got to the house, he saw what had happened. There was a pot on the
     stove,' and then we go into it." Book now, after the scene break that follows the hospital:

     > The pot was on the stove.

     Change to [CT's words]:

     > When he got to the house, he saw what had happened. There was a pot on the stove.

     Then "It was not in the rack. It was on the back burner..." as before. Logged only; not in the v6 Doc yet.

155. **Chapter 7, David and Elijah at the Bear Flag: "People don't care what you know."** CT (26 Nov): "the breakdown
     between him and his friends. Like, he thinks he's trying to help, but it's obvious that he's making people
     uncomfortable. He's not necessarily aware of that." His beats, for "their conversation" before his mother's stroke
     (the January beer in Chapter 7): David asks if he's heard from the guys, "No, I haven't heard from a lot of people,
     actually"; "you're scaring the hoes, man", he laughs it off; "I'm serious, dude, like, you gotta stop"; "as much
     as I'd like to, we're living through historic times. This is an unprecedented moment, and I kind of helped create
     it"; David says "Elijah" to catch his attention, and Elijah is taken aback, because David calls him Mad (dictation
     said "Matt"); "I'm worried about you, man"; "I'm fine. I just, I know things, and I'm trying to figure out how to
     tell people what I know"; "people don't care what you know, they care how you make them feel, man. You should know
     that from all your years playing music with all of us" (his last version of "with"/"for"); "I appreciate that,
     man, but this is just too important"; David makes a face: "All right, well, can I get you anything else?"
     Context from CT, NOT for the page: Elijah thinks he's helping and doesn't see that he makes people uncomfortable.

     The scene already has three of these beats, so they are kept, not repeated: "Hey. You're scaring the hoes." with
     "Elijah laughed. He thought they were back."; "'Elijah,' he said. David had not called him Elijah since they were
     eight years old."; and "I'm worried about you, man." The new lines go in at three places [CT's lines; the joins,
     "Wes isn't really answering me" kept from the book, "Dave", and "David didn't say anything to that" are Claude's]:

     **Change 1.** Book now:

     > "Wes doing okay?"
     >
     > "I don't know. He's not really answering me."

     Change to:

     > "Hey, you heard from the guys?"
     >
     > "No. I haven't heard from a lot of people, actually. Wes isn't really answering me."

     **Change 2.** Book now:

     > "I'm serious, man. Why don't you just stick to music? You were good. People loved you up there. Stay in your
     > lane."
     >
     > "Bro. What do you mean?"
     >
     > David didn't say what he meant. He let his eyes drop to his beer and kept them there.

     Change to:

     > "I'm serious, dude. You gotta stop. Why don't you just stick to music? You were good. People loved you up
     > there. Stay in your lane."
     >
     > "I mean, as much as I'd like to, we're living through historic times, Dave. This is an unprecedented moment,
     > and I kind of helped create it."
     >
     > David didn't say anything to that. He let his eyes drop to his beer and kept them there.

     **Change 3.** After David's speech ("...I'd have just wanted you to go to bed."). Book now:

     > "It's not like that."
     >
     > "Okay."
     >
     > "Dave. It's not."
     >
     > "Okay, Mad."
     >
     > Then they sat there

     Change to:

     > "I'm fine," Elijah said. "I just know things, and I'm trying to figure out how to tell people what I know."
     >
     > "People don't care what you know, man. They care how you make them feel. You should know that from all your
     > years playing music with all of us."
     >
     > Elijah thought about it for a second. "I appreciate that, man. But this is just too important."
     >
     > David made a face. "All right," he said. "Well, can I get you anything else?"
     >
     > Then they sat there

     Cut by this: Elijah's "Bro. What do you mean?" and the "It's not like that." / "Okay." / "Dave. It's not." / "Okay,
     Mad." exchange; CT's new lines take their places. Then "...and finished their beers." as before. Logged only; not
     in the v6 Doc yet.

156. **Chapter 13, after the bandmates drive off: "He got the letter."** CT (26 Nov): "There's a line when his bandmates
     walk past him where he says he got the letter. Maybe we could rephrase that because there's still a lot of
     repetition with he did this, he did that. We could rephrase that sentence structure." The letter is the one from
     her doctor that he drove into town for ("On Wednesday he drove into town for a letter from her doctor."), which the
     short line doesn't say. Book now:

     > He put his hand down.
     >
     > He got the letter. He walked back to the truck the other way, which took him past the Bear Flag.

     Change to [Claude's wording; every fact kept]:

     > Eventually his hand came down. The doctor's letter was still waiting at the office, so he went and picked it
     > up. On the way back to the truck he went around the other way, which took him past the Bear Flag.

     Logged only; not in the v6 Doc yet.

157. **Chapter 13, David leaves the farm: who heaves the hand truck.** CT (26 Nov): "Similarly, he took the hand truck back
     into his pickup. Who are we talking about here?" It is David; the line before is his ("Yeah, I figured."), but it
     opens on "He" and so do the next three sentences. Book now:

     > He heaved the hand truck back into his pickup. He looked at the porch a second. There was nobody on it. He
     > lifted two fingers off the wheel going down the drive, and Elijah lifted his hand.

     Change to [Claude's wording; every fact kept]:

     > David heaved the hand truck back into his pickup and looked at the porch a second. There was nobody on it.
     > Going down the drive, he lifted two fingers off the wheel, and Elijah lifted his hand.

     Logged only; not in the v6 Doc yet.

158. **Chapter 14, the rain on the truck: sentence openings.** CT (26 Nov): "Same story with the part where it says he lay
     back down, he pulled the jacket up, he did this, he did that." Book now:

     > He lay back down.
     >
     > He pulled the jacket up. He cried the way he had yelled, all the way, with his mouth open. Nobody was going to
     > hear it over that. He cried until his ribs hurt, and then for a while after that he just lay there and leaked.

     Change to [Claude's wording; only the openings and joins change, every fact and image stays]:

     > Slowly he lay back down and pulled the jacket up. Then the crying came, the way the yelling had, all the way,
     > with his mouth open. Nobody was going to hear it over that. It went on until his ribs hurt, and for a while
     > after that he just lay there and leaked.

     Logged only; not in the v6 Doc yet.

159. **Chapter 15, Grace's April email (the placeholder in edit 100).** CT (26 Nov) wrote the email and what follows it:
     "Mr. Madron. It has been an absolute pleasure watching you online, period. Everyone here at the farm agrees, you
     get it. ... Looking forward to working with you, Grace Lane / Elijah took a breath and read the email again.
     Three, four, five times he read it, waiting to feel different. / Inside his chest was that same little voice that
     told him to join Crop Dust, to take the job at Claypot, and to do every other hairbrained thing he had never
     regretted. / He started typing his reply." Fixed silently: "Madron" to Madrone (his name in the book), "yoghurt"
     to yogurt, "hairbrained" to harebrained, the comma splice after "agrees" to a colon. Set in italics, like every
     message in the book. "Grace Lane" is the first time the book gives her surname.

     **Change 1.** After "But something told him to open it, so he did." and before "She had been saying yes to him
     since spring." (where edit 100 had the placeholder), add [CT's words]:

     > Mr. Madrone,
     >
     > It has been an absolute pleasure watching you online. Everyone here at the farm agrees: you get it.
     >
     > We've been working on something for a long time now, and we think you'll appreciate it. Are you familiar
     > with solarpunk? Like that stupid Chobani yogurt commercial, "Dear Alice"?
     >
     > Well, we're doing our best to build it in real life.
     >
     > If you're interested, there's a cot here and a private room with your name on it. Your own door, a shared
     > kitchen, and a bunch of land.
     >
     > We would like to extend a formal invitation to host you while you build out your vision of the future with
     > us.
     >
     > If you're interested, please just say the word and the spot is yours.
     >
     > Looking forward to working with you,
     >
     > Grace Lane
     >
     > Elijah took a breath and read the email again. Three, four, five times he read it, waiting to feel
     > different.

     **Change 2.** Edit 100's "Then that same little voice spoke up again, the one that had told him to open it. The
     quiet one that steers you toward where you're supposed to be, if you let it. / So he typed out his reply." is the
     same beat, so CT's new version replaces it instead of repeating it [CT's words]:

     > Inside his chest was that same little voice that told him to join Crop Dust, to take the job at Claypot, and
     > to do every other harebrained thing he had never regretted.
     >
     > He started typing his reply.

     **Change 3, knock-on (Chapter 26, the gantry).** Book now: "Elijah had never heard the word." Since the email
     asks "Are you familiar with solarpunk?", that line contradicts it. Change to [Claude's wording]: "Elijah had seen
     the word once, in Grace's first email, and never thought about it again." His "It's what?" before it stays.

     **Settled by CT (26 Nov):** "Everyone here at the farm agrees" stays as he wrote it, though Grace's later message
     says half the table disagrees. CT: "It's supposed to be the way I wrote it. It's a sales email lol it's meant to
     be overly optimistic ... that contradiction is totally fine." Context from CT, NOT for the page: the April email
     is a sales pitch, overly optimistic on purpose.

     Logged only; not in the v6 Doc yet.

160. **Chapter 16, meeting Marta: sentence openings.** CT (26 Nov), with a screenshot of the page: "Here's another instance
     of that pattern we talked about" (sentences that all open with "He"). Book now, after "And Elijah went off.":

     > He hadn't meant to. He'd meant to say hello. But he had spent a year being told he'd calibrate, and then
     > most of a year being agreed with by people who weren't listening. And here was a stranger who made things
     > and fixed things for her neighbors. He told her what was coming, fast: the models, the list, the end of the
     > deal. And then he started pitching.
     >
     > He heard himself say the shop could scale. He said platform. He said there ought to be an app, a network of
     > co-ops, a marketplace layer. He could build it in a month. This thing could be in fifty towns by Christmas.
     > They could get ahead of the wave. He said *first-mover,* and heard it come out of his mouth in Ruby's voice,
     > quick and light.

     Change to [Claude's wording; only the openings and joins change, every fact and the italics stay]:

     > Going off wasn't the plan. All he'd meant to say was hello. But he had spent a year being told he'd
     > calibrate, and then most of a year being agreed with by people who weren't listening. And here was a
     > stranger who made things and fixed things for her neighbors. So he told her what was coming, fast: the
     > models, the list, the end of the deal. And then he started pitching.
     >
     > The shop could scale, he heard himself say. Platform. There ought to be an app, a network of co-ops, a
     > marketplace layer. He could build it in a month. This thing could be in fifty towns by Christmas. They could
     > get ahead of the wave. *First-mover,* he said, and heard it come out of his mouth in Ruby's voice, quick and
     > light.

     Then "Somewhere in there he ran out of gas..." as before. Logged only; not in the v6 Doc yet.

161. **Chapter 17, the first Friday dinner: Priya and her pencil.** CT (26 Nov), on the page with "That's a picture": "Priya
     said, fidgeting with the pencil behind her ear." Book now:

     > "That's a picture," Priya said. "What would you measure?"

     Change to [CT's words; placed by Claude on this line, her challenge to him, since the page has two "Priya said"]:

     > "That's a picture," Priya said, fidgeting with the pencil behind her ear. "What would you measure?"

     A few lines later (edit 90) she "took the pencil from behind her ear, like somebody pulling a chair up to a
     fight", so the fidgeting leads into it. Logged only; not in the v6 Doc yet.

162. **Physical beats on bare dialogue tags, through the book.** CT (26 Nov): "There's many opportunities to show physical
     action in moments like these. Please find some and add them to the edits. DO NOT OVERDO IT. Simple physical
     actions that make sense and add character, texture, and color to the book is what I'm after." Claude's choice
     and wording: eleven lines (nine since 26 Nov, see 5 and 10), out of about 110 bare "X said." tags, each where nobody in the scene is already
     moving, using what the book already gives each person (Ruby's fire escape, Reuben's glasses, Grace at the stove,
     Curtis's hands in the wash water, Tyler carrying the reel, the serenity prayer frame behind David's bar).
     Left alone: anywhere the paragraph before already has an action, and Lou's walnuts, which belong to Chapter 35.

     1. Ch 10: "Fire escape," Ruby said. "It's the only good room." becomes:
        > "Fire escape," Ruby said, already sliding a window up. "It's the only good room."
     2. Ch 13: "Heard they close Friday," David said. becomes:
        > "Heard they close Friday," David said, looking past him at the house.
     3. Ch 17: "They broke things," Curtis said. becomes:
        > "They broke things," Curtis said, pointing his fork down the table at her.
     4. Ch 23: "Every month," Reuben said. becomes:
        > "Every month," Reuben said, pushing his glasses up onto his forehead.
     5. Ch 24: dropped 26 Nov (was "holding her hands out to the stove"). Grace does it again eleven lines later,
        "Grace held her hands out to the stove and didn't say anything for a while," and that one matters.
     6. Ch 26: starts with lettuce," Curtis said. "Then it's Skynet." becomes:
        > starts with lettuce," Curtis said, shaking the cold water off his hands. "Then it's Skynet."
     7. Ch 27: "Wait, so the plan is chalk," Tyler said. becomes:
        > "Wait, so the plan is chalk," Tyler said, shifting the reel to his other arm.
     8. Ch 33: "I know it," Lou said. becomes:
        > "I know it," Lou said, and set down his fork.
     9. Ch 34: "It's a sensor," Curtis said. "It's two wires." becomes:
        > "It's a sensor," Curtis said, pinching the bridge of his nose. "It's two wires."
     10. Ch 37: dropped 26 Nov (was "looking past him into the shouse"). Four lines later "Lou looked past him,
        through the open door, at the blanket by the stove."
     11. Ch 39: "Thirty years that's been on that wall," David said. becomes:
        > "Thirty years that's been on that wall," David said, following his eyes up to the frame.

     Logged only; not in the v6 Doc yet.

163. **Chapter 17, the first Friday dinner: "turned off on telling it."** CT (26 Nov): "I don't know, I'm kind of turned
     off on telling it." Book now (edit 90): He looked at his plate. "I don't know. I'm kind of off telling it."
     Change to [CT's words]: He looked at his plate. "I don't know, I'm kind of turned off on telling it." Logged only;
     not in the v6 Doc yet.

164. **Chapter 17, the first Friday dinner: his shoulders.** CT (26 Nov): "Without being conscious of it, his shoulders
     relaxed a few inches." Book now (edit 90): "...the first genuine camaraderie he'd felt in a hot minute. He noticed
     his shoulders relax a bit." Change the last sentence to [CT's words]: "Without being conscious of it, his
     shoulders relaxed a few inches." Logged only; not in the v6 Doc yet.

165. **Chapter 17, Marta at the roll-up door: "Musicians."** CT (26 Nov): "'Musicians' the same way you might say
     termites." Book now: ...and then at him, and said one word, "Musician," the way you'd say termites. Change to [CT's words]: ...and then at him, and said one word, "Musicians," the same way you might say termites.
     Logged only; not in the v6 Doc yet.

166. **Chapter 18, the last lines: "Elijah said", and the birds at the pond.** CT (26 Nov): "I think what you're doing is
     just right, he said. It's clear that it's Elijah talking, but since it's a new page, I want to say, I think the way
     you're doing it is just right, Elijah said. And then, if this is nighttime, we should say something about the
     frogs at the pond. If this is daytime, we should say something about the birds at the pond." The scene has no
     clock time, but he returns the jars at the kitchen trailer "that week", when he works the bench from seven to
     noon, so it reads as daytime: birds. Book now (edit 123):

     > "I think what you're doing is just right," he said.

     Change to [CT's words; the bird line is CT's correction of Claude's, 26 Nov]:

     > "I think the way you're doing it is just right," Elijah said.
     >
     > Out by the pond, the birds were chirping magnificently.

     Then "Chapter 19" as before. The pond is the one from edit 104 (the frogs at night). Context from CT, NOT for the
     page (edit 104): birds don't sing when there are predators around; it is his nervous system settling. Logged
     only; not in the v6 Doc yet.

167. **Chapter 19, the first line: cut.** CT (26 Nov): "Remove the sentence about 40 greenhouse controllers at the beginning
     of chapter 19." Cut: "The co-op's first real manufacturing run was forty greenhouse controllers." The chapter now
     opens "In April the order came, through a friend of a friend of Priya's, from the CSA network two valleys over.
     Forty small boxes that could read soil moisture and air temperature..." Logged only; not in the v6 Doc yet.

168. **Chapter 19, Marta on the first design: "made by us and not Claypot."** CT (26 Nov): "I just want you to spend a
     little more time making this feel like it was made by us and not Claypot." Book now (edit 124): "I just want you to
     spend a little more time making this feel more like us than like Claypot." Change to [CT's words]: "I just want you
     to spend a little more time making this feel like it was made by us and not Claypot." Logged only; not in the v6
     Doc yet.

169. **Chapter 19, June: the team fixes it, not Elijah alone.** CT (26 Nov): "And Elijah fixed what they found > and the
     fledgling production team fixed what they found..." Book now: "...two growers ran the first boxes for a week and
     sent back notes in pencil, and Elijah fixed what they found before the rest went out." Change to [CT's words]:
     "...and the fledgling production team fixed what they found before the rest went out." Logged only; not in the v6
     Doc yet.

170. **Chapter 20, the first line.** CT (26 Nov): "Lou put him on a drip tape in may > What Lou did to Elijah in May just
     about killed him." Book now: "Lou put him on drip tape in May, and it just about killed him." Change to [CT's words]: "What Lou did to Elijah in May just about killed him." The drip tape is named
     a little later in the chapter ("a quarter mile of plastic tubing", "This is drip tape"). Logged only; not in the
     v6 Doc yet.

171. **Chapter 20, Lou laughing at the drip tape: "Hey, Ivy League."** CT (26 Nov): "\"Ivy League\" > \"Hey Ivy League\"".
     Book now: "Ivy League," he said, wiping his eyes. "You look like a man trying to put pants on an octopus." Change to [CT's words; the comma after
     "Hey" is Claude's]: "Hey, Ivy League," he said, wiping his eyes. The Appendix's list of Lou's names for him ("Ivy League") stays. Logged only;
     not in the v6 Doc yet.

172. **Chapters 20 to 39: sentence openings.** CT (26 Nov), on the recommendations for the second half ("Prepare these edits for the future the same way we have with the other edits"). Claude counted 42 paragraphs in Chapters 20 to 39 where most sentences open with "He" and changed the openings and joins in the ones that read as a tic, the way edits 133, 156 to 158 and 160 were done. Every fact and line of dialogue stays. Left alone on purpose, because the repetition is the point: the dashboard in Ch 23 ("He built a map. He built, God help him, a dashboard."), the welding beads in Ch 30, the work and the numbness in Ch 31 ("He scribed the lines. He clamped the strip.", "He stood there. He wanted to leave", "He slept. He got up and swept."), "He didn't go help" in Ch 32, Lou and the bracket in Ch 29, Denny going live in Ch 38, and "He couldn't change ... He could" in Ch 39. Claude's wording throughout.

     1. Book now:
     > He had come north to do something about it. He also believed nobody could do anything about it. He had never put those two facts next to each other.

        Change to:
     > He had come north to do something about it, and he also believed nobody could do anything about it. Until now, those two facts had never sat next to each other in his head.

     2. Book now:
     > He stood there with the keys and thought about the logs

        Change to:
     > Instead he stood there with the keys and thought about the logs

     3. Book now:
     > He stayed where he was useful. Useful was easier than David.

        Change to:
     > So he stayed where he was useful. Useful was easier than David.

     4. Book now:
     > He swept the shop twice. He checked his phone for nothing. He thought about a field full of people who could dance

        Change to:
     > He swept the shop twice and checked his phone for nothing. Then he thought about a field full of people who could dance

     5. Book now:
     > He wanted to draw a line through it and extend it. He opened the inbox.

        Change to:
     > He wanted to draw a line through it and extend it. Instead he opened the inbox.

     6. Book now:
     > he had stopped sleeping for a month. He read it standing up, with the coffee going cold.

        Change to:
     > he had stopped sleeping for a month. This time he read it standing up, with the coffee going cold.

     7. Book now:
     > He read it three times. He typed I'm sorry I missed and looked at it

        Change to:
     > He read it three times, then typed I'm sorry I missed and looked at it

     8. Book now:
     > He pocketed the phone to answer later, when he could think, and went to find Grace.

        Change to:
     > Then he pocketed the phone to answer later, when he could think, and went to find Grace.

     9. Book now:
     > He'd come with a better plan. He had it on his phone.

        Change to:
     > He'd come with a better plan, and he had it on his phone.

     10. Book now:
     > every fifteen minutes. He'd already priced it. He showed her.

        Change to:
     > every fifteen minutes. It was already priced. He showed her.

     11. Book now:
     > He didn't sleep. He lay in the shouse with the phone on his chest

        Change to:
     > He didn't sleep. All night he lay in the shouse with the phone on his chest

     12. Book now:
     > The stove ticked as it cooled. He lay there and listened to it until the window went gray.

        Change to:
     > The stove ticked as it cooled, and he listened to it until the window went gray.

     13. Book now:
     > He'd have a fix drafted by March. He had, everyone knew, already started.

        Change to:
     > A fix would be drafted by March. He had, everyone knew, already started.

     14. Book now:
     > Then the red light came on. He watched himself skip to the last slide

        Change to:
     > Then the red light came on. From somewhere outside himself he watched himself skip to the last slide

     15. Book now:
     > into the microphone. He sat down with eight minutes of the talk unsaid.

        Change to:
     > into the microphone. When he sat down, eight minutes of the talk were still unsaid.

     16. Book now:
     > He wanted numbers. He had a notebook of them already.

        Change to:
     > What he wanted was numbers, and he had a notebook of them already.

     17. Book now:
     > He knew what he was doing. He had a name for it in the notebook and a rule against it. He did it for three nights anyway.

        Change to:
     > He knew what he was doing. There was a name for it in the notebook, and a rule against it. For three nights he did it anyway.

     18. Book now:
     > He didn't bring anybody a plan. He had said out loud, at a Friday table, that he was done bringing plans. Wren had put her hand on her chest. He had asked Grace

        Change to:
     > Nobody got a plan from him. At a Friday table he had said out loud that he was done bringing plans, and Wren had put her hand on her chest. Later he had asked Grace

     19. Book now:
     > He looked at the date in the corner, the one with his initials

        Change to:
     > There was the date in the corner, the one with his initials

     20. Book now:
     > He didn't tell anyone. He had nothing he could show them.

        Change to:
     > He didn't tell anyone. There was nothing he could show them.

     21. Book now:
     > He closed the notebook and snapped a rubber band around it.

        Change to:
     > So he closed the notebook and snapped a rubber band around it.

     22. Book now:
     > He wanted to argue. He wanted to run it again, with the fix in, right now, and show everybody it worked. He looked at Irene.

        Change to:
     > He wanted to argue, to run it again with the fix in, right now, and show everybody it worked. Then he looked at Irene.

     23. Book now:
     > He put the hinge down on the post. He was back in a hallway

        Change to:
     > Carefully he put the hinge down on the post, and then he was back in a hallway

     24. Book now:
     > He had gotten it from Nate and Wes, and from his mother, and from David across a bar.

        Change to:
     > Nate and Wes had given it to him, and his mother, and David across a bar.

     25. Book now:
     > Curtis stood up. He didn't say a word. He wiped his mouth

        Change to:
     > Curtis stood up. Without a word, he wiped his mouth

     26. Book now:
     > He had heard no in that room before.

        Change to:
     > That room had told him no before.

     27. Book now:
     > He sat there with the laptop pointed at her shoulder.

        Change to:
     > So he sat there with the laptop pointed at her shoulder.

     28. Book now:
     > He had eleven notebooks about a machine and not one line about that. He never thought about it. He didn't think about it because

        Change to:
     > Eleven notebooks about a machine, and not one line about that. He never thought about it, because

     29. Book now:
     > He heard how it sounded the second it was out. He meant that he wished

        Change to:
     > The second it was out, he heard how it sounded. What he meant was that he wished

     30. Book now:
     > He knew what choosing for people looked like. He'd been paid for it.

        Change to:
     > What choosing for people looked like, he knew. He'd been paid for it.

     31. Book now:
     > He drove past the turn twice on the way to the feed store and didn't take it.

        Change to:
     > Twice, on the way to the feed store, he drove past the turn and didn't take it.

     32. Book now:
     > He tuned it, and it slipped, and he tuned it again.

        Change to:
     > It took him a minute to tune it, and it slipped, and he tuned it again.

     33. Book now:
     > He leaned the guitar back in its corner and put the blanket back on.

        Change to:
     > Afterward he leaned the guitar back in its corner and put the blanket back on.

     34. Book now:
     > He lifted the hose over his head with one hand

        Change to:
     > From down there he lifted the hose over his head with one hand

     35. Book now:
     > He cashed the newest one for this.

        Change to:
     > For this he cashed the newest one.

     36. Book now:
     > He didn't put a note in that one.

        Change to:
     > That one went without a note.

     37. Book now:
     > He knew what it was. He had known since a hinge and a gatepost in July.

        Change to:
     > He knew what it was, and had known since a hinge and a gatepost in July.

     38. Book now:
     > He would have to be careful in here now, more careful than he used to be.

        Change to:
     > From now on he would have to be careful in here, more careful than he used to be.

     39. Book now:
     > He'd built eleven notebooks on it.

        Change to:
     > Eleven notebooks rested on it.

     40. Book now:
     > He meant the part about another time. He put the phone back in his pocket.

        Change to:
     > He meant the part about another time. The phone went back in his pocket.

     41. Book now:
     > He drank half. He tipped like a man who used to get tipped. He took the book out

        Change to:
     > He drank half and tipped like a man who used to get tipped. Then he took the book out

     Logged only; not in the v6 Doc yet.

173. **Chapters 33, 34 and 38: physical beats in the table scenes.** CT (26 Nov), on the recommendations. The three big table arguments carry most of the book's bare "X said." tags (37, 14 and 19). Ten beats, each where nobody in the lines around it is moving, the same rule as edit 162. Claude's choice and wording.

     1. Book now:
     > "Owned by who?" Curtis said.

        Change to:
     > "Owned by who?" Curtis said, not looking up from his plate.

     2. Book now:
     > "Name one," Marta said.

        Change to:
     > "Name one," Marta said, and set her cup down.

     3. Book now:
     > "Easy for you," Curtis said.

        Change to:
     > "Easy for you," Curtis said, sitting back in his chair.

     4. Book now:
     > "Most of them," Denny said.

        Change to:
     > "Most of them," Denny said, raising his glass.

     5. Book now:
     > "Nine days," Curtis said.

        Change to:
     > "Nine days," Curtis said, looking out the windshield.

     6. Book now:
     > "Item four," Reuben said.

        Change to:
     > "Item four," Reuben said, turning a page.

     7. Book now:
     > "Hell, I'll look at it," said Lou.

        Change to:
     > "Hell, I'll look at it," said Lou, and held out his hand for the laptop.

     8. Book now:
     > "That's a thermometer, Curtis," Frank said.

        Change to:
     > "That's a thermometer, Curtis," Frank said, rubbing his eyes.

     9. Book now:
     > "I know," Tyler said.

        Change to:
     > "I know," Tyler said, looking at his plate.

     10. Book now:
     > "Sit down, Curtis," Rosa said.

        Change to:
     > "Sit down, Curtis," Rosa said, and patted the bench beside her.

     Logged only; not in the v6 Doc yet.

174. **"It's not X. It's Y." lines.** CT (26 Nov), on the recommendations; the shape he called AI-sounding in edit 119. Four of about 25 loosened. Kept on purpose: "That's not a principle, Elijah. That's your mother." (Ch 36; Ch 37 quotes it back), "That's not food yet. That's a poem about tide pools." (Ch 33's title), and the ones that are plain argument. Claude's wording.

     1. Book now:
     > "It's not the Terminator, Curtis. It's an arm. It's bolted

        Change to:
     > "Curtis, it's an arm. It's bolted

     2. Book now:
     > "It's not that they can't. It's that they won't."

        Change to:
     > "They can. They just won't."

     3. Book now:
     > This time it wasn't a yes. It was three tables now, at one table.

        Change to:
     > This time nobody said yes. There were three tables now, at one table.

     4. Book now:
     > But it didn't break. It's on purpose.

        Change to:
     > But it didn't break. Somebody did it on purpose.

     Logged only; not in the v6 Doc yet.

175. **Chapter 31: his father's rule, once more.** CT (26 Nov), on the recommendations. "Never take a handout" (edits 91 to 93) is not heard after Chapter 10. One echo, where Elijah remembers turning down the million. Claude's wording, from the father's line in edit 91.

     Book now:

     > He had turned down the million dollars and the ads and the room. And these people

     Change to:

     > He had turned down the million dollars and the ads and the room. That was his father in him: never take a handout. And these people

     Logged only; not in the v6 Doc yet.

176. **Chapter 26: the flooded bed is not the pond.** CT (26 Nov), on the recommendations. Since edits 104 and 166 the farm has a pond nearby; Chapter 26 called the flooded low spot "a pond" three times, which can read as that pond. Claude's wording.

     1. Book now:
     > the low spot at the end of bed three was a pond,

        Change to:
     > the low spot at the end of bed three was under water,

     2. Book now:
     > looked at the pond, and wrote it down.

        Change to:
     > looked at the water, and wrote it down.

     3. Book now:
     > He got down in the pond with his shoulder

        Change to:
     > He got down in the water with his shoulder

     Logged only; not in the v6 Doc yet.

177. **Chapter 37, at the gate: the birds.** CT (26 Nov), on the recommendations. The birds and frogs at the pond (edits 104 and 166) were his nervous system settling, and they never came back. One line, at the gate, when he finds Grace's new tape, before he cries. Claude's wording, after CT's "Out by the pond, the birds were chirping" (edit 166). Context from CT, NOT for the page (edit 104): birds don't sing when there are predators around.

     Book now:

     > Somebody checked.
     >
     > He sat there with the engine running and cried.

     Change to:

     > Somebody checked.
     >
     > Out by the pond, the birds had started up.
     >
     > He sat there with the engine running and cried.

     Logged only; not in the v6 Doc yet.

178. **Chapter 37, packing the truck: through what he feels.** CT (26 Nov), on the recommendations; the same note as edit 100 ("you're moving the reader along through the story events, not through the emotions he's feeling"). Every item stays; "going on three years" is the chapter's own (Marta's shop, a page later). Claude's wording.

     Book now:

     > It took a morning. A bag of clothes. The laptop. A milk crate of notebooks, eleven of them now, and the manuscript, which was three hundred pages and had a title. The broken coupons, in a coffee can. His mother's pot. Everything he owned fit in the bed of the Ranger with room left over, except two robot arms in the back of the equipment shed.

     Change to:

     > It took a morning. A bag of clothes went in, and the laptop. Then a milk crate of notebooks, eleven of them now, and the manuscript, which was three hundred pages and had a title. He stood holding that one a while before he set it down. The broken coupons went in a coffee can. His mother's pot went in beside them. Going on three years, and everything he owned fit in the bed of the Ranger with room left over. It should have felt like traveling light. It felt like he had hardly been here at all. All that was left were two robot arms in the back of the equipment shed.

     Logged only; not in the v6 Doc yet.

179. **Tuesdays that only mark time.** CT's standing request (25 Nov, after edit 125): cut the ones that only mark time, keep a day where it matters. 22 in Chapters 20 to 39; three cut. Kept: the route day, Ray's death, Marta's PT, the empty houses, Emeka, the county stamp at 11:04, the festival meeting, the packing day, the proofs, and every Tuesday in dialogue. Claude's wording.

     1. Book now:
     > The sweep signed off on it Tuesday.

        Change to:
     > The sweep signed off on it.

     2. Book now:
     > The county's power was back Tuesday.

        Change to:
     > The county's power came back three days later.

     3. Book now:
     > He'd filed it with the clerk on Tuesday.

        Change to:
     > He'd already filed it with the clerk.

     Logged only; not in the v6 Doc yet.

180. **Chapter 17, Denny's reskilling speech: "then back at Elijah."** Settles the open question under edit 103. CT
     (26 Nov): "Keep it. Then back to what?" Denny "folded his hands and looked at Elijah" before the speech, and the
     speech is aimed at him; after edit 103's paragraph on the table, the line no longer says where he looks. Book now:

     > He looked around the table, then back.

     Change to [Claude's wording, approved by CT: "Yes."]:

     > He looked around the table, then back at Elijah.

     Logged only; not in the v6 Doc yet.

181. **Chapter 17, the town kitchen: "Agreed on what?"** Settles the open question under edit 109. CT (26 Nov): "Clarity
     and continuity ... Those are the key things." Claude's read: the touch lines and "Your knowledge earns your keep" are
     clear and stay; the last line was too vague to follow. The new one plants the question edit 127 picks up in
     Chapter 19 ("wondering what, exactly, Curtis and Grace had agreed on"). Book now:

     > Curtis shut the cooler lid. Nobody said anything else. The warm place on Elijah's arm stayed warm, but
     > something behind it had gone quiet.

     Change to [Claude's wording, approved by CT: "Yes."]:

     > Curtis shut the cooler lid. Nobody said anything else. The warm place on Elijah's arm stayed warm, but under
     > it was a question he hadn't had a minute ago. Agreed on what?

     Logged only; not in the v6 Doc yet.

182. **Chapters 21 to 39: clarity pass.** CT (26 Nov): "search through the second half of the book for other moments
     where the perspective could be confusing, where we use pronouns and it's not exactly clear who we're talking
     about, where things are repetitive ... so that I can just nip them in the bud in one fell swoop." Four readers
     went through Chapters 20 to 39; Claude checked every finding against the text and kept 48, then on CT's "Which
     ones belong and which should be changed?" dropped 11 that were clear or deliberate (Priya's "Yes. And we let",
     Phoenix twice, Marta's long second, "At Friday dinner", the stove door, "Neither of them said anything" twice,
     Curtis's arms, "There's always crime", "He had promised her", "He had never said it back" (kept unsaid: Ch 36
     "He had not said it to her yet", and the note in the amp in Ch 38), and the quarter turn of the glass). Two more
     were corrections to edit 162 (its beats 5 and 10, dropped). CT: "Proceed." Claude's wording throughout; each
     change only names who or when, or cuts a repeat.

     1. Ch 21 (no man is named in the paragraph). Book now:
        > He watched her do forty in a night.

        Change to:
        > Elijah watched her do forty in a night.

     2. Ch 21 (a new paragraph; it names who is still talking). Book now:
        > He set the next lid down. "You put my face

        Change to:
        > Denny set the next lid down. "You put my face

     3. Ch 22 (Chapter 21 ends in June, so this steps back). Book now:
        > The servers arrived at the end of May, in the back of Denny's truck.

        Change to:
        > The servers had come at the end of May, in the back of Denny's truck.

     4. Ch 22 (the last man named is Reuben). Book now:
        > He started calling the rack the Crucible.

        Change to:
        > Elijah started calling the rack the Crucible.

     5. Ch 22 (who sent it, and three he's in a row). Book now:
        > He had a text that said Saw the video with the warehouse guy. He's good, and he'd put a thumb on it

        Change to:
        > He had a text from David that said Saw the video with the warehouse guy. He's good. Elijah had put a thumb on it

     6. Ch 22 (the whiteboard is "the board" on the same page; this changes edit 137's words, which are in the v6 Doc). Book now:
        > he told them about the board too.

        Change to:
        > he told them about the circuit board too.

     7. Ch 22 (the paragraph before ends "that summer"). Book now:
        > The co-op adopted a rule that Saturday.

        Change to:
        > The co-op adopted a rule that same Saturday.

     8. Ch 22 (same reason). Book now:
        > That night Grace found him on the pump house steps.

        Change to:
        > That Saturday night Grace found him on the pump house steps.

     9. Ch 22 (saves the reader counting back from Monday). Book now:
        > The morning before, at 9:40, he called the rose garden.

        Change to:
        > The morning before, on Sunday at 9:40, he called the rose garden.

     10. Ch 24 ("her" could be the aide). Book now:
        > The aide held the phone by her ear.

        Change to:
        > The aide held the phone by his mother's ear.

     11. Ch 24 (two women in one clause). Book now:
        > the aide said she had shown it to her.

        Change to:
        > the aide said she had shown it to his mother.

     12. Ch 25 (Devendra is the last man named). Book now:
        > Elijah called him on Sundays, after his mother.

        Change to:
        > Elijah called him on Sundays, after he called Ma.

     13. Ch 27 ("It" points at nothing). Book now:
        > It came to the table anyway.

        Change to:
        > The argument came to the table anyway.

     14. Ch 28 (Denny is the last man named). Book now:
        > All of it happened around him, because

        Change to:
        > All of it happened around Elijah, because

     15. Ch 28 (as two paragraphs, the first reads as Elijah's). Book now:
        > "Now I'm holding your rain fly."
        > 
        > "Still want the fence," Curtis said.

        Change to:
        > "Now I'm holding your rain fly. Still want the fence," Curtis said.

     16. Ch 29 (it follows a beat of Elijah's). Book now:
        > "I've been reading deeds a long time. I know what a man signs

        Change to:
        > "I've been reading deeds a long time," Reuben said. "I know what a man signs

     17. Ch 31 (the chapter before ends on Tyler). Book now:
        > He brought the Friday table a plan.

        Change to:
        > Elijah brought the Friday table a plan.

     18. Ch 31 (Melody is named just before). Book now:
        > But nobody told her it wasn't her business, either.

        Change to:
        > But nobody told Patricia it wasn't her business, either.

     19. Ch 31 (Curtis has just left). Book now:
        > He slept. He got up and swept.

        Change to:
        > Elijah slept. He got up and swept.

     20. Ch 31 ("she" could be the aide). Book now:
        > The aide said she'd had a good night

        Change to:
        > The aide said Ma had had a good night

     21. Ch 33 (two men in play). Book now:
        > He means me. He's said so.

        Change to:
        > My dad means me. He's said so.

     22. Ch 33 (it answers Curtis, after a beat of his). Book now:
        > "Us. Like Irene's wire."

        Change to:
        > "Us," Lou said. "Like Irene's wire."

     23. Ch 33 (the same words as his first time standing). Book now:
        > like he was stopping a truck at a gate.
        > 
        > "Listen to me," he said. "Please."

        Change to:
        > like he was stopping a truck at a gate.
        > 
        > "Listen to me," he said again. "Please."

     24. Ch 33 (four lines after "Lou looked down the table."). Book now:
        > He looked down the table. "So tell me this.

        Change to:
        > He looked from face to face. "So tell me this.

     25. Ch 37 (the next "He" is Lou). Book now:
        > Lou was on the step when he came out.

        Change to:
        > Lou was on the step when Elijah came out.

     26. Ch 37 (his third paragraph in a row, and Elijah said nearly the same words). Book now:
        > "I'll keep the stove going." He slid the key

        Change to:
        > "I'll keep the stove going," Lou said. He slid the key

     27. Ch 37 (Tyler is the last man named). Book now:
        > She held it out to him. He took it.

        Change to:
        > She held it out to Elijah. He took it.

     28. Ch 37 ("Elijah" opens the sentence before too). Book now:
        > Elijah had wanted to ask him one more question.

        Change to:
        > He had wanted to ask Lou one more question.

     29. Ch 37 (the last woman named is M. Madrone in the visitor book). Book now:
        > She was in the chair by the window.

        Change to:
        > His mother was in the chair by the window.

     30. Ch 37 (Elijah's or Manny's). Book now:
        > His was the one fence left on that road

        Change to:
        > Manny's was the one fence left on that road

     31. Ch 38 ("away" twice, three "her"s). Book now:
        > scooted her chair six inches away from her.

        Change to:
        > scooted her chair six inches back from Patricia's.

     32. Ch 38 (Lou is the last man named). Book now:
        > just as he had left it.

        Change to:
        > just as Elijah had left it.

     33. Ch 39 (the sender isn't named). Book now:
        > a text he had never really answered.

        Change to:
        > a text from Wes he had never really answered.

     34. Ch 39 (he already set it down a few lines before). Book now:
        > "Mad." David put the glass down. He leaned on the bar

        Change to:
        > "Mad." David leaned on the bar

     35. Ch 39 (the last woman named is the girl with the laptop). Book now:
        > He heard her. Under all the others.

        Change to:
        > He heard Grace. Under all the others.

     36. Epilogue ("He" reads as Wes). Book now:
        > Wes kept texting dates. He hadn't made one yet.

        Change to:
        > Wes kept texting dates. Elijah hadn't made one yet.

     Logged only; not in the v6 Doc yet. Item 6 changes words of edit 137, which is in the v6 Doc.

183. **Chapter 18: the co-op's gravel lot, and when Claypot shipped.** Settles the open question under edit 112. CT
     (26 Nov): "Yes. And they shopped it on a Thursday afternoon, just 15 minutes before the financial markets
     closed." ("shopped" is "shipped".) Book now:

     > Claypot shipped Companion 2.0 on a Thursday. Elijah read the announcement post standing in the gravel lot
     > with a late cold snap coming through his jacket...

     Change to [CT's words; "fifteen" spelled out, like the book's other numbers]:

     > Claypot shipped Companion 2.0 on a Thursday afternoon, just fifteen minutes before the financial markets
     > closed. Elijah read the announcement post standing in the co-op's gravel lot with a late cold snap coming
     > through his jacket...

     Logged only; not in the v6 Doc yet.

184. **"Recognize Your Power" closes the Dedication.** CT (26 Nov): "Yes. I want the v6 that I'm reading in large print
     to be the most current version," of the v7 changes (`V7-CHANGES.md`). Corrected the same day, in place (not in the
     Doc yet): first logged as a first page of its own, above the title. CT: "I don't want the first page to be
     recognize your power. This is a manuscript. So the first page should be the title, and then the like copyright
     information ... and then there's the dedication ... We don't have an introduction ... we just have chapter 0, and
     I kind of just want to start it there ... So the recognize your power bit should be part of the dedication."
     Change: after the Dedication's line (edit 185), a second centered line:

     > For the people I love who looked me in the eye like I'd finally lost it.
     >
     > Recognize Your Power

     [CT's words.] Then Act One and Chapter 0, as before. The book opens: title page, copyright page (the build adds
     it), Contents, Dedication, Act One, Chapter 0. Logged only; not in the v6 Doc yet.

185. **The Author's Note becomes a Dedication.** CT (26 Nov, for v7, now v6 too): "About the author and author's note
     need to be revised to be a dedication instead of an author's note." In Contents, "Author's Note" becomes
     "Dedication", and "Thank You" is added after "Appendix". The heading "Author's Note" and the whole note (from
     "For years, I've been talking about this." to "Let's begin to imagine how.") are replaced by a heading
     "Dedication" and one centered line:

     > For the people I love who looked me in the eye like I'd finally lost it.

     [Claude's draft, made from CT's own sentence in the note: "I've watched people I love look me in the eye like I'd
     finally lost it." CT (26 Nov): "The dedication was good. I liked what you wrote."] Edits 1, 2 and 139 to 141 were in the Author's Note,
     so their check rows now say "replaced by 185". Logged only; not in the v6 Doc yet.

186. **The very end: Thank You, and "Recognize Your Power".** CT (26 Nov, for v7, now v6 too): "the about is a
     gratitude to the reader." Claude's first draft was replaced the same day, in place (not in the Doc yet), by CT's
     own words: "the acknowledgement is a thank you for reading, thank you for your time. Please consider how much of a
     difference each and every one of us can make in this world if we really try. But you don't really need to make
     that big of a difference to everyone. You are someone. And if you touch any heart, please be sure to start with
     your own. Recognize your power." After the Appendix's last line, "Thursday, November 25, 2027. Thanksgiving.", a
     heading "Thank You" and [CT's words; only the sentence breaks are Claude's]:

     > Thank you for reading. Thank you for your time.
     >
     > Please consider how much of a difference each and every one of us can make in this world if we really try. But
     > you don't really need to make that big of a difference to everyone. You are someone. And if you touch any heart,
     > please be sure to start with your own.

     Then the last line of the book, centered: "Recognize Your Power" [CT's words]. The large print PDF no longer adds
     the "About the Author" page after it (`about_author_in_book` in `publication/novel/build/book.json`; the bio stays
     there for the back cover). Logged only; not in the v6 Doc yet.

187. **Chapter 31: the call to Ma moves to the next Sunday.** The same Sunday, Marta knocks at eight and takes him to
     the shop; then Curtis's eggs, he sleeps, sweeps and eats, and Wren comes by. None of that fits before 9:40 that
     morning. CT (26 Nov), after weighing a shift of it all to Saturday (which would put the circle on the night of
     the Friday table): "The next Sunday." Book now:

     > On Sunday at 9:40 he called the rose garden.

     Change to [CT's words]:

     > The next Sunday at 9:40 he called the rose garden.

     Changes words of edit 30, which is in the v6 Doc: check row 30 narrowed to "Sunday at 9:40 he called the rose
     garden." Logged only; not in the v6 Doc yet.

188. **Chapter 15, the last lines before Act Three: the check-engine light.** CT (26 Nov): "I want Elijah to just see
     it. Roll his eyes, and then be overcome with laughter. I want him to turn up the music. I want you to choose a
     fitting song, and I want him to think the words figures. I hope they have a good mechanic." Book now:

     > Somewhere past Cloverdale the check-engine light came on.

     Change to [Claude's wording and Claude's choice of song, from CT's beats; "All his pent-up pain started rolling
     out of his lungs at once." and "Figures. I hope they have a good mechanic." are CT's]:

     > Somewhere past Cloverdale the check-engine light came on.
     >
     > Elijah looked at it and rolled his eyes. Then he snorted, and the snort turned into a laugh, and the laugh got
     > away from him. All his pent-up pain started rolling out of his lungs at once. He wiped his eyes and turned up
     > the radio. Willie Nelson was singing "On the Road Again."
     >
     > Figures, he thought. I hope they have a good mechanic.

     Only the song's title is used, no lyrics. Corrected the same day, in place (not in the Doc yet): the first
     version ("a laugh came up out of him") sat too close to CT's "A chuckle came over him" in Chapter 17 (edit 105
     area); the second read "really dry"; the third (ribs, blurry road, "a broke man in a truck") was "a little too
     much". CT took the middle one and added the pent-up pain line. Logged only; not in the v6 Doc yet.

189. **Chapter 18, Marta at the door: the line about Grace is a warning.** Edit 118 is in the v6 Doc, so this is a new
     edit. CT (26 Nov): "it's supposed to read as a warning, like a, you know, treat my baby girl right or else we'll
     have problems." Book now:

     > Don't let her effort go to waste." She straightened up. "Soup's on at noon.

     Change to [Claude's wording, from CT's direction]:

     > Don't let her effort go to waste." She straightened up and looked him dead in the eye. "You waste it, and you
     > and me are going to have a problem." She let that sit. "Soup's on at noon.

     The next lines are unchanged ("That's not a reward, spreadsheet ... Her eyes twinkled. "It's just lunch.""), so
     the twinkle now lets him off the hook. Logged only; not in the v6 Doc yet.

190. **Chapter 20, Lou's pop quiz: cut the cable box line.** CT (26 Nov): "What does the notebook with the wattage have
     anything to do with what's going on around it?" It points back to Chapter 5 (the cable box, twenty-three watts),
     about 150 pages earlier, and never says the contrast. CT: "It does read like a random fact. We don't really need
     it." Then: "Yeah, let's cut it." Book now:

     > Elijah had no idea. He was a little ashamed of that. He had a notebook with the wattage of his cable box in it.

     Change to:

     > Elijah had no idea. He was a little ashamed of that.

     Logged only; not in the v6 Doc yet.

191. **Chapter 20, Lou on why the farm works: "my man", and "Such as?"** CT (26 Nov): "I don't think Lou would say it
     doesn't work, man, to Elijah. I think he would say it doesn't work, my man. It works because we're lucky, because
     our specific constellation has some unique advantages. And then Elijah would say, such as, and then he would say,
     well, and then explain the rest of it." Book now:

     > "It doesn't work, man. It's never worked. It works because nine people here don't get paid, and Grace is some
     > kind of saint, and my wife taught fourth grade ...

     Change to [CT's words; the sentence break after "lucky" and "Lou said" are Claude's]:

     > "It doesn't work, my man. It works because we're lucky. Our specific constellation has some unique
     > advantages."
     >
     > "Such as?"
     >
     > "Well," Lou said. "Nine people here don't get paid, and Grace is some kind of saint, and my wife taught fourth
     > grade ...

     The rest of his speech is unchanged. "It's never worked" goes, since CT's version leaves it out. Logged only;
     not in the v6 Doc yet.

192. **Chapter 20, after Lou's "Who ate it at your place?": the pot points back to Chapter 13.** CT asked where the pot
     was set up; it is named as hers alone only in Chapter 3, about 200 pages earlier, and burned on the back burner
     in Chapter 13 (how Manny found her). Claude suggested pointing the line at the burned pot. CT (26 Nov): "Her
     sacred pot burned to a crisp on the back burner." Corrected the same day, in place (not in the Doc yet), after a
     reader flagged that the burned pot alone pictures her decline, not her paying for the farm. CT: "Change the
     sacred pot to the sacred pot she never let anyone wash that had been burned to a crisp on the back burner.
     Right? Like, there's some irony there." Book now:

     > Elijah thought about his mother, and the pot she never let anyone else wash.

     Change to [CT's words; "else" kept from the book, as in Chapter 3]:

     > Elijah thought about his mother, and the sacred pot she never let anyone else wash that had been burned to a
     > crisp on the back burner.

     Logged only; not in the v6 Doc yet.

193. **Chapter 20, Lou on robots: "I already lost one orchard."** CT (26 Nov): "Lou says, I already lost one orchard
     to one buyer, and that doesn't make sense. I already lost one orchard is enough." Book now:

     > Not leased. Not a subscription. I already lost one orchard to one buyer."

     Change to [CT's words]:

     > Not leased. Not a subscription. I already lost one orchard."

     Logged only; not in the v6 Doc yet.

194. **Chapter 20, Wren on the machine-written essay.** CT (26 Nov): "I felt like a fraud, and how about she says, I
     felt like a fraud and like a stranger had helped themselves to the inside of my house." Book now:

     > Then I found out a machine wrote it, and I felt like somebody had been in my house."

     Change to [CT's words]:

     > Then I found out a machine wrote it, and I felt like a fraud and like a stranger had helped themselves to the
     > inside of my house."

     Logged only; not in the v6 Doc yet.

195. **Chapter 20, Wren introduced: the run-on split, and "one of the best artists".** CT (26 Nov), on the page: "There's
     a fat run-on sentence here." Claude proposed the split. Then CT: "and the best artist Elijah has ever met. We
     haven't established any sort of artistry. We don't have any frame of reference for that. That's just stating
     something for no reason. And one of the best artists most people had ever met." Book now:

     > That was Wren, who led the Sunday circle and made the candles and had painted every wall of the seed house,
     > inside and out, with things that were half heron and half radio tower. She was twenty-four, and the best
     > artist Elijah had ever met.

     Change to [the split is Claude's wording; "one of the best artists most people had ever met" is CT's]:

     > That was Wren. She led the Sunday circle and made the candles, and she had painted every wall of the seed
     > house, inside and out, with things that were half heron and half radio tower. She was twenty-four, and one of
     > the best artists most people had ever met.

     The rest of the paragraph is unchanged. Logged only; not in the v6 Doc yet.

196. **Chapter 7, the first messages after the video: his old Spanish teacher.** CT (26 Nov): "We need to add a part at
     the beginning when his video first goes viral, talking about like how he's surprised with the backlash ... like
     maybe his Spanish teacher ... extremely condescending, negative, rude, mean, spirited ... And then something in the
     environment needs to happen so that it calls his attention away from it, and then it moves the story forward."
     Full words in "Direction from CT, 26 Nov". On the name: "I don't care what the teacher's name is." Book now:

     > It was supposed to be for Nate and Wes and his mother and David.
     >
     > Then the other kind of message started showing up.

     Change to (inserted between them) [the messages, his thoughts and "He really looked up to this guy. He loved this
     guy. And his old teacher just called him a liar?" are CT's words; the teacher's introduction, the name, "a good
     ear", the phone on the amp and the rattle are Claude's]:

     > Then a name came in that he hadn't seen since high school. Mr. Ostrander had taught him Spanish for three years, and once, after class, had told him he had a good ear and should never let anybody talk him out of using it. Elijah opened it smiling.
     >
     > You don't know what you're talking about. That's never going to happen.
     >
     > Oh, Mr. Ostrander, Elijah wrote back. It's really nice to hear from you. Hope everything's good. Hope you're well.
     >
     > The answer came before he'd set the phone down. Cut the crap, kid. You're out of your league here. You have no idea what you're talking about. This isn't going to happen. This isn't true. And you need to stop spreading fear online.
     >
     > Spreading fear? He scrolled back up through it. I'm not spreading fear, he thought. Am I?
     >
     > Hey, he typed. Maybe something got misconstrued. Maybe there's a miscommunication here. I'm not trying to spread fear. I'm just trying to share what I've personally experienced and let people know what's happening.
     >
     > You're making stuff up and I don't appreciate it. This isn't true. That didn't happen. You're a liar. And you need to stop.
     >
     > Whoa, he thought. What the hell?
     >
     > He set the phone face down on the amp. He really looked up to this guy. He loved this guy. And his old teacher just called him a liar?
     >
     > The phone rattled against the grille.

     The rattle is the senator's office in the next line ("A senator's office wanted fifteen minutes"), which echoes
     the night the video spread (the phone "rattled against the grille"). Earl's line just before ("You're telling
     scared people to be more scared") is echoed on purpose. Corrected the same day, in place: "He read it twice. Then
     he wrote back." cut. CT: "Don't do the pattern." Logged only; not in the v6 Doc yet.

197. **The counting pattern, Chapters 0 to 19 and 37 to 39.** CT (26 Nov), on the list from the sweep (see "The counting
     pattern, swept 26 Nov"): "Great, add these all to the edits to be fixed." The fixes are Claude's. Kept on Claude's
     advice and not changed: CT's own laugh line (edit 188), "David checked the buckle again," "Nobody let go right away.
     Then Grace did." and its mirror on the phone, "Then she reached out and turned it off" and its mirror, "He read it
     again, slower," and the Epilogue's "Then he played something else." Chapters 20 to 36 are fixed in the rewrite.
     Book now, then Change to:

     1. "He'd underlined it twice. Then he'd gone back to nodding."
        > He'd underlined it twice and gone back to nodding.
     2. "David looked at him a second longer than he needed to. Then he went to change a keg."
        > David looked at him a second longer than he needed to, and went to change a keg.
     3. "Curtis looked at Elijah a second longer than he needed to. Then he went back to his crimper."
        > Curtis held Elijah's eye a beat too long and went back to his crimper.
     4. "He left the tower off for a week. Then he opened the notebook where he'd scrawled MADRONE IS NOT A DRONE, turned to a clean page, and started writing."
        > He left the tower off for a week, and when he opened the notebook where he'd scrawled MADRONE IS NOT A DRONE, he turned to a clean page and started writing.
     5. "Elijah wrote it all down. Then he watched it again."
        > Elijah wrote it all down.
     6. "Then he sat very still, because he was dizzy."
        > He sat very still, because he was dizzy.
     7. "Then he needed energy figures, so he found the Kardashev numbers"
        > For energy figures he found the Kardashev numbers
     8. "He poured the pitchers. Then he came back, put on"
        > He poured the pitchers and came back, put on
     9. "Then he opened the band chat to send the link."
        > He opened the band chat to send the link.
     10. "He pasted the link under that anyway. Then he sent it to the other two chats and typed"
        > He pasted the link under that anyway, sent it to the other two chats, and typed
     11. "Then there was a paralegal in Fresno, so he wrote him back too. Then a guy who taught high school shop, and a nurse."
        > There was a paralegal in Fresno, so he wrote him back too, and a guy who taught high school shop, and a nurse.
     12. "Elijah read that one twice. He answered"
        > He answered
     13. "Elijah watched it four times looking for the lie."
        > Elijah watched it looking for the lie.
     14. "He told the phone about the forty-eight dollars. Then he went in."
        > He told the phone about the forty-eight dollars and went in.
     15. "Then he asked about the farm, and what they grew"
        > He asked about the farm, and what they grew
     16. "and looked at it a while. Then he thought about Wes."
        > and looked at it a while, thinking about Wes.
     17. "He watched it until it stopped. Then he typed Working."
        > When it stopped, he typed Working.
     18. "It lasted a second or two. Then David looked back down"
        > It lasted a second or two before David looked back down
     19. "He sat with them for a while. Then he started the truck."
        > He sat with them a while and started the truck.
     20. "local pickup only. Then he watched it. A week went by."
        > local pickup only. A week went by.
     21. "He got as far as the first line. Then he thought about the comments"
        > He got as far as the first line and thought about the comments
     22. "He watched it not ring. Then he played the voicemail."
        > He watched it not ring and played the voicemail.
     23. "He read it twice with the door open"
        > He read it with the door open
     24. "He thought about a chair by a window. Then he put the phone face down"
        > He thought about a chair by a window and put the phone face down
     25. "The old man nodded and put it away. Then he looked at Elijah for a while."
        > The old man nodded, put it away, and looked at Elijah for a while.
     26. "He stood there a second getting his balance. Then he went into the coat one more time"
        > When he had his balance he went into the coat one more time
     27. "Elijah took a breath and read the email again. Three, four, five times he read it, waiting to feel different."
        > Elijah took a breath and read the email again, waiting to feel different.
     28. "He read the last three words again. It was the second time in two days somebody had said them to him."
        > You look thin. It was the second time in two days somebody had said that to him.
     29. "Marta looked at him for another second. Then she picked up a push broom"
        > Marta looked at him another second and picked up a push broom
     30. "She held the amp a second longer. Then she set it down"
        > She held the amp a second longer before she set it down
     31. "the same way you might say termites. Then she went back to her bench."
        > the same way you might say termites, and went back to her bench.
     32. "He brought the jars in. Then he put the phone on Do Not Disturb"
        > He brought the jars in and put the phone on Do Not Disturb
     33. "She read the order twice and pinned it"
        > She read the order and pinned it
     34. "Not really. Then he remembered his training"
        > Not really. But he remembered his training
     35. "Then Grace came back alone and went straight"
        > Grace came back alone and went straight
     36. "and stood there holding it. Then he carried it back"
        > and stood there holding it. He carried it back
     37. "He wrote his name and the time. Then he turned back a page, and another."
        > He wrote his name and the time and turned back a page, and another.
     38. "Then he laid one more place, at the corner"
        > He laid one more place, at the corner
     39. "Then everyone had one in their hand"
        > Soon everyone had one in their hand
     40. "Grace had read hers twice. She laid it down"
        > Grace laid hers down
     41. "She stood over it a second. Then she pulled the blanket off and folded"
        > She stood over it a second before she pulled the blanket off and folded
     42. "without asking. Then he slid the four ones back across with two fingers."
        > without asking, and slid the four ones back across with two fingers.
     43. "He looked at it a while. Then he typed, Can't this time."
        > He looked at it a while before he typed, Can't this time.
     44. "Then he thought of Manny's well, four feet down, and it went back where it came from."
        > The thought of Manny's well, down four feet, sent the smile back where it came from.
     45. "Then a face filled the screen."
        > A face filled the screen.
     46. "Then he took the book out of his jacket"
        > He took the book out of his jacket

     Earlier check rows narrowed or updated to the new words so both pass: 19, 120, 125, 131, 135, 159, 165, 172.
     19, 125, 131 and 135 now show PARTIAL against the v6 Doc, and 197 too (some of its short new lines, such as "He
     answered", are already in the Doc); expected, as for 30, 137 and 182. Logged only; not in the v6 Doc yet.

198. **Chapter 25 rebuilt: the letter, town, the pond, Thanksgiving.** CT's scenes (26 Nov; his words in "Direction from
     CT, 26 Nov" and section 5a of `PLAN-CHAPTERS-20-TO-36.md`), drafted by Claude in
     `manuscript/novel/drafts/chapter-25.md`. CT on draft 1: "You're still overusing pronouns and not varying the
     sentence structure." On draft 2: "I've told you to change this a dozen times and you keep doing it." On draft 3:
     "Yes, this is way better." The draft file is the record of Book now and Change to, with CT's words in bold. In
     the book:
     - New, after "Surely Frank knew.": a scene break, the letter to Ma and the first tiff, and town (frozen yogurt,
       Tyler at Kowalski's, "You knew."). The kitchen-trailer exchange ("You knew since spring and you didn't
       knock?" through "But you knock.") moves into the truck, with her frozen yogurt spoon.
     - Frank letting Tyler go moves after the laminated paper. "Elijah told Grace that night, at the kitchen trailer"
       through "and didn't argue." comes out. "In the morning he made the harder visit" becomes "That week he made the
       harder visit" [Claude's wording].
     - Marta's scene, the festival and the amp night ("That fall, it was Marta who told him about the music." through
       "somebody ought to bring him something loud.") move, unchanged, to the end of Chapter 26.
     - The stove kiss ("The night of that Friday dinner, she knocked." through "in the other direction.") comes out.
       In its place: the pond (CT's kiss) and Thanksgiving (Lou's questions, the truck stop, the U-turn, the return).
     - Chapter 26, one line, to match [Claude's wording]: "She told him on a Saturday morning, in his kitchen, wearing
       his shirt. Nobody at the Friday table had said one word about where she slept now." becomes "She told him on a
       Saturday morning, in his kitchen, over coffee."
     Still owed, so the book reads true (all in the plan): Elijah telling Lou about Barry (Ch 20); the heat failure,
     the empty greenhouse and the forty boards redone (Ch 21, 22); Chapter 26's October night where he makes his move
     (the amp night moved there ends with her head against his, and the kiss is still to be written). Open: whether
     the check-engine light was nothing. Logged only; not in the v6 Doc yet.

199. **Chapter 20: the boxes waiting on summer, Ma and Barry, Wren's comeback.** From the plan; drafted by Claude in
     `manuscript/novel/drafts/chapter-20.md` (Book now and Change to are there). CT's corrections on the boxes
     paragraph: "What the fuck is that, bro?" (draft 1's one long sentence and its joke), then "It hadn't been very hot
     yet. This is foreshadowing, right?" and "we can combine them together ... It was still a cool spring. It hadn't
     been very hot yet." (CT's words), then "do the work." Claude's wording otherwise. Line flags 1 and 2 of the 59 are
     fixed here. Logged only; not in the v6 Doc yet.

200. **Chapter 21: Denny's fans, Priya on wingnuts, the heat.** From the plan and CT's direction of 26 Nov; drafted by
     Claude in `manuscript/novel/drafts/chapter-21.md` (Book now and Change to there, CT's words in bold). CT on draft
     1: Priya "must say, and I still get weird letters ... we don't know what kind of letters they are. It's not
     clear. You need to make things clear." The couple are Hector and Lupe Ochoa (Claude's names). Line flag 3 of the
     59 is fixed here. Logged only; not in the v6 Doc yet.

201. **Chapter 22: the leak, the bell, Lou's IBM line, the pot, the hour of the funeral.** From the plan; written by
     Claude and logged on CT's "just do it" (Book now and Change to in `manuscript/novel/drafts/chapter-22.md`). He
     opens the gate to read the vent logs alone on the drive (shame makes him work alone, and that causes the leak);
     at the bell he chooses to confess the board, with Tyler at the back; Curtis "Twice"; Tyler "It was in the file";
     Lou's IBM line (CT's, 26 Nov: "a machine cannot be held accountable, therefore a machine should never make a
     management decision"), said Lou's way, from his wife's fridge, and the rule that a person opens the vents on hot
     days and signs for it; he packs to leave for good and Grace takes his mother's pot back out of the truck ("You're
     not taking the pot."), with Marta watching from the shop door; six households with a dollar figure ($210 a week,
     Claude's estimate); the Sunday 9:40 call in its place, and the hour of Ray's service passing while he reads
     crawler logs. Line flags 4 and 5 of the 59 fixed; the counting fixes at the old lines 1974, 1976, 2009, 2017 done.
     Rows 137 and 182 narrowed to the words that still hold. Logged only; not in the v6 Doc yet.

202. **Chapter 23: the land or the Ochoas, Grace tells them, where you eat, Lou at the county window.** From the plan;
     written by Claude and logged on CT's "Do it" (Book now and Change to in `manuscript/novel/drafts/chapter-23.md`).
     The down payment takes the channel's whole surplus, the money promised to Hector and Lupe for October; Reuben says
     what three missed payments do; the table argues it (Priya, Curtis, Wren: "So the ones it cost get paid last.") and
     votes for the land; Grace tells the Ochoas herself and sits in her truck after. Elijah's errands past Irene's lead
     to the coworker and CT's line "He learned a long time ago not to date where you eat, but there was just something
     so alluring about Grace." [CT's words]. Lou drives Reuben to the county and keeps his hand on the stamped stack.
     Cut: Reuben's mirrored "data problem" line, the dashboard summary closers, part of Reuben's speech, Lou at the
     kitchen door (a repeat of Ch 22), "Tuesday". Line flags: the power bill "said so", "the kitchen-table meeting".
     Counting fix at the old line 2047. About 405 words in, 231 out. Logged only; not in the v6 Doc yet.

203. **Chapter 24: the containers paid for before the plugs cooked, Hector at the first fire, Marta at the door, the pond.**
     From the plan; written by Claude and logged on CT's "Do it" (Book now and Change to in
     `manuscript/novel/drafts/chapter-24.md`). The containers were bought in April, so the house doesn't come out of
     the Ochoas' money; Hector comes to the first fire for half an hour, Lupe doesn't; Marta leaves last and tells Grace
     in the doorway, "Pick a side of that door. You're heating the whole valley." (her double speak, Claude's wording);
     after the captain, Grace needs air and they walk to the pond for the first time: his bleed-out joke from Chapter
     17, her four-foot rock, nearly a kiss, and the dog from the Friday dinners shakes pond water on both of them; back
     inside, her wet shoes point at the stove. Line flags: "nothing got built only once", "where no room had been", "the
     place were his to run". Counting fix at the old line 2139. About 312 words in, 56 out. Logged only; not in the v6
     Doc yet.

204. **Chapter 26: the rover and the argument about labor, Ma's fall, the pay vote, Mrs. Delgado, the October night at
     the pond.** From the plan and CT's direction of 26 Nov; written by Claude and logged on CT's "Do it" (Book now and
     Change to in `manuscript/novel/drafts/chapter-26.md`, with whose words are whose). The gantry becomes a rover (here
     and in Ch 32 and 33; Ch 38's "the gantry stood parked" waits for CT). CT's lines for Lou ("We're not being
     replaced, we're expanding our capacity. We're having productivity gains."), Curtis (the drones, "I need to go build
     an EMP."), Priya ("wildly illegal") and Lou ("I'll go talk to him.") go into the wash-station argument, with
     Elijah hearing Devendra and the CPO in it. Ma falls on day six of the dark ("Maybe I need to go home right now." is
     CT's); Grace offers to drive; he stays. The pay vote is brought the Friday after Thanksgiving and waits until
     summer; Curtis "asked it looking at me." Mrs. Delgado seen once. October: Grace can't go to her festival; Marta's
     push; he sets the amp on the tailgate at the pond, knocks, they play music until the light goes, he kisses her;
     the morning after, "wearing his shirt and drinking coffee" (CT). Rows 172 and 198 narrowed (the festival jealousy
     and "something loud" are gone; "wearing his shirt" is back). Logged only; not in the v6 Doc yet.

227. **The polish pass at key moments.** CT (26 Nov, tenth chat): "there are some key moments where there's still
     opportunity to buff it out and polish it up. I'd like you to do a pass to tighten everything here and now." Four
     readers, one range each; 50 sentences returned, every quote machine-matched; Claude read each on the page and
     checked whose words it was. 20 places fixed (21 ops rows), all Claude's wording, none of CT's dictated lines:
     Ch 21 (the opening's "Not dramatically. Just constantly."), Ch 22 ("He could not delete what they had copied";
     "the worst available outcome"; "Useful was easier than David."; "which she did not."), Ch 24 ("went to his
     lane"), Ch 25 ("confessed to it"), Pondwater ("He remembered what she had told him ... about her dad and a
     porch." cut), Ch 29 ("one he did not keep"), Ch 31 ("So of course they knew."; "finally saw the whole thing"; "He
     didn't go to the shop"), Ch 32 ("Except there was no demo."), Ch 33 (the hinge inversion from edit 172; "He read
     them out"; "Elijah realized"), Ch 34 ("He didn't have to."; "They could have run that shed"), Ch 35 ("His feet
     had."), Ch 36 ("He told Grace"). 30 left, among them everything in Chapters 0 to 19, the ending and the fire. Five
     lines are put to CT (four mirrored lines in done chapters; "which one of them he'd helped", Ch 36). Each change
     with Book now, Change to and why, and the left list: `manuscript/novel/drafts/polish-2026-11-26.md`. Row 172
     narrowed. 58 words in, 78 out. Logged only; not in the v8 Doc yet.

226. **Chapter 26: why Elijah waits after the pond.** CT (26 Nov, tenth chat), dictated, for "the reason why Elijah
     waits so long in between when Grace kisses him to keep him from leaving the farm and when they actually decide to
     date". Where: Chapter 26, after "By her own rule the answer was his to give, and she didn't knock again.", in
     place of Claude's "His side of it he never said out loud." CT's, word for word (the last version where he
     restated a line): "Elijah didn't quite know why he didn't go for it right away. Maybe it was a combination of his
     prior dating history and his steadfast commitment to not rocking the boat any more than he needed to, but he felt
     like hooking up with Grace would be, at that point in time, a bad call. Even though she'd made it clearer than an
     alpine day that she was into him, he ultimately decided not to jeopardize his room and board by getting
     entangled. It was a decision he truly meant to stand by." / (the pay sentences already there, now opening "The
     pay was part of it too.", Claude's five words) / "But alas, fate has a way of wearing you down. And time had a
     different story to tell. Watching Grace work the land would do that to just about anyone."
     **Held, not logged:** "It took under 6 months for him to change his mind." CT made it conditional ("if there's
     nothing mechanically in the way during that time"). There is: the pond kiss is the second week of November 2025
     (Ch 25) and the amp night is October 2026, eleven months on, and that month is fixed by Grace's festival ("every
     October since she was nineteen"), Marta's "She kissed you at that pond a year ago", the June and July scenes of
     Chapter 26 that are written with the two of them not yet together (Ma's fall, the pay vote), Chapter 27 opening
     in October 2026, and the Appendix timeline. No time jump was made; Chapter 26's year stays. Asked CT whether the
     line should say "under a year".
     Row 204 narrowed ("His side of it he never said out loud." is gone). 128 words in, 7 out. Record: the foot of
     `manuscript/novel/drafts/chapter-26.md`. Logged only; not in the v8 Doc yet.

225. **Chapters 8 to 10: the panel goes further; Elijah says he is overwhelmed; fifty million views; Ruby's pitch.**
     CT (26 Nov, tenth chat), dictated: "do we at any point explain how overwhelmed Elijah is? ... I don't remember
     reading anything about him just saying like how overwhelmed he feels." (He doesn't: the nearest are "I feel a
     little out of my depth here" in Ch 8 and "It was too much." in Ch 13.) "We also never really give a number for
     the video. We say parabolic ... I think it would be reasonable to say like 50 million views on one video." "I
     think the scene with the panel falls flat, but doesn't go as far as it could or needs to." "you can clean up the
     language there based on our editing rules and the writing guide. I trust you to be able to carry this through the
     rest of the way." Seven ops rows; Book now and Change to, with his words in bold, in
     `manuscript/novel/drafts/edit-225-panel-and-ruby.md`.
     Ch 8, the moderator: "your video went parabolic. Fifty million views". Ch 8, the panel, after the woman defines
     AGI: a panelist (a "sneakers one" on Elijah's right, Claude's) asks what stops it destroying everything; the
     alignment problem; "You mean like my car?"; "there isn't really a mechanic for what this thing could do."; the
     experts' ten years; "So what's your prediction?"; he thinks of Devendra's thirty years and says "I said it in the
     video"; "By 2027."; "I mean, yeah. That's what the math says."; the killer robots and "Get to your bunker. Kiss
     your dog and your family goodbye. Elijah Madrone here says it's the end of the world before the end of the
     decade." "The room was kind about it" and "It was worse than if they'd laughed" are gone; "Nobody asked him about
     the math." (Claude's). Ch 8, the dock: Ruby's "Damn, that was brave, bro. That was brave. I admire the hustle." /
     "It's not really a hustle." / "Well, I know, because allegedly you're not selling anything."; and after "You
     hate this. It's okay.", Elijah: "I mean, honestly, I'm quite a bit overwhelmed. There's been a lot of changes
     happening in my life recently, and it's been a bit much." Ruby slaps his back, an arm around his shoulders:
     "Happens to the best of us." "Come on. I want to show you something." Ch 9, the car: "Here, you got a second? I
     want to talk to you about something." Ch 10, the fire escape, before the offer: "Fifty million views on one video
     ... Do you know how much money you should be making, according to your numbers?" / "I don't really think about
     that kind of stuff." / "I know you don't ... You're the artist." / "But if I were in your shoes, and I have been,
     I'd have another paid-off house." / "So listen. Here's the deal." and "Believe me, it's a good list."
     CT's lines are his, with dictation fillers removed ("like", "well", "he's like"; "doing" to "making"). **Invented
     by Claude:** who the panelist is. 617 words in, 25 out. Logged only; not in the v8 Doc yet.

224. **Pondwater: Curtis shows the table a laser weeder run by a brain organoid; Grace tells Elijah about her
     festival outside.** CT (26 Nov, tenth chat): "Do we have a scene in the book where they mention or discuss laser
     weeders? Or any other modern industrial agtech? I feel like the near-future stuff should be in there. Also...maybe
     brain organoids?" The book had neither. He dictated the scene from Priya's "You mean..." to Grace's "Hey so,
     changing the subject," and: "And then you can connect it to the next story elements with what she says after
     that." Context from CT, NOT for the page: "The scene resolves with a brief conversation between Elijah and Grace
     outside after everyone parts ways."
     Where: Pondwater, in place of the one sentence "At dinner one night Grace said she wasn't going to her festival
     this year, and that it was fine, and she left before the pie." (Claude's choice of place: October 2026, the dinner
     the chapter already had; what Grace says next is the festival, which Marta explains the next evening.)
     CT's, word for word: everything from "You mean…" to "Hey so, changing the subject,". Marks changed in his lines:
     "??" to "?", "bonafied" to "bona fide", "round him" to "around him", "beside Curtis" to "besides Curtis", commas
     and periods around the tags ("I'm out, Curtis,"; "I'm going for a walk," said Priya; "Aye aye, captain." Curtis
     made an exaggerated salute.), and the thought set in italics as he asked.
     Claude's: the lead-in (Curtis sets the laptop on the plywood ahead of the pie; "Laser weeder," he said. "Watch.";
     the steel box behind a tractor and the weeds going up in threads of smoke; Tyler's "We've all seen those. The big
     growers run them. They're like a million dollars."; Curtis's "That's last year's ... They call it a brain
     organoid."), and the end ("I'm not going to my festival this year." It was fine, she said. She was gone before he
     could ask what festival, and before anybody had cut the pie.).
     **Invented by Claude:** that a laser weeder with an organoid in it was shown the year before; how Curtis says it
     works (grown in a dish from skin cells, the size of a lentil, taught, fed sugar water); the price Tyler gives.
     Note for CT: the book says nearly the same thing of Denny in Chapter 17 ("oblivious to the mood of the people
     around him, as he usually was", his edit 103); "Ever-oblivious" is now said of Curtis too. Logged as he gave it.
     403 words in, 9 out. Record: `manuscript/novel/drafts/edit-224-organoids.md`. Logged only; not in the v8 Doc yet.

223. **The pass's held items, resolved.** CT (26 Nov): "I want you to resolve as many of these as you can without my
     help." From `drafts/pass-2026-11-26.md`, "Held for CT", and the plan's section 13; Claude's wording throughout.
     Ch 3, his italic note made plain ("It won't start with the machines. First it takes the people who see it coming,
     and pulls them out of the world everyone they love still believes in."). Ch 1, Devendra's "first month with one of
     these". Ch 5, Ma calls back at noon, from Joan's (**invented**: her phone dead in her purse). Ch 13, "my mother's
     kitchen". Ch 18, "looked Elijah right in the eyes" (his line, the pronoun only). Ch 26, Grace waits "for a long
     time", not until dark. Ch 37, "It should have felt like traveling light." cut (plan 13, item 4). Ch 37, "before the
     bank's did". Ch 38, "its version of a wink"; "the way she always had when she needed a yes". Ch 39, "The night of
     the toast, one glass had gone down on this stretch of wood, and three had gone up."; "Melody's number"; "Elijah
     zipped his jacket." Appendix: the Ochoas in the cast; the heat in June, the pond and the U-turn, the amp on the
     tailgate, and Denny gone in the timeline (plan 13, item 6). Left for CT: the gas cap (his scene ends on "Friday,"
     she said.), and "Marta had heard it as a murder" (the plan's change read worse). Rows 9, 178, 204, 218 and 220
     narrowed or moved to the new words. Logged only; not in the v6 Doc yet.

222. **Whole book: the last continuity pass.** CT (26 Nov): "continuity errors, confusing moments, repetition, bad
     sentence structure, anything that might cause problems for the reader," then "Go on the pass." Eight readers read
     the book after edit 221 in eight ranges; 79 findings, every quote machine-checked; Claude judged each on the page.
     50 fixed (51 ops rows), all Claude's wording, among them: the woman who whispered about golden handcuffs named
     (Ch 10, CT's paragraph, the pronoun only), Ruby hands the notebook back (Ch 9), the confession's unseen promise
     (Ch 22), Elijah, not Curtis, mows Praether's fence (Ch 26), the storm lights the co-op, not nineteen houses (Ch 28),
     Marta's shoulder "Worse since the summer" (Ch 29), a hundred visitors a year, not twenty, pay for the route
     (Ch 31), the price list before Elijah shows it (Ch 34), Lupe's INSTALLED BY line (Ch 36), the Appendix's shed.
     10 held for CT (four in the ending, four of his own lines, two others); 19 dropped. Each change, with Book now and
     Change to, and the held list: `manuscript/novel/drafts/pass-2026-11-26.md`. Rows 16, 63, 133, 167, 182, 198, 201,
     202, 210, 211 and 220 updated or narrowed to the new words. Logged only; not in the v6 Doc yet.

221. **Chapter 34: the women weigh the tall rover at Irene's table.** CT (26 Nov): a scene before the meeting where the
     women weigh the taller machine and the yield against pushback from the community and decide for it, with an older
     woman's advice on people who tell you what they think without being asked ("Not ABOUT men, but PEOPLE," read as a
     note for Claude, not a line). Written by Claude, every word (Book now and Change to in
     `manuscript/novel/drafts/chapter-34.md`, section 221). After "DECEMBER.", a new scene: Priya, Marta and Grace take
     Priya's sheet up to Irene's house the afternoon before the October meeting. Priya: twelve beds, not four; "It never
     touches the food" (the pledge covers the field to the box). Marta: the robot welder at her plant ("By spring it had
     given six of us the whole week."). Grace: what the route and Lupe have said, unasked. Irene, the older woman: "it's
     hardly ever about the thing ... They wanted to know if they still had a say on this road" and "Just don't tell
     yourself afterward it was free." Marta and Grace sign; Grace will talk to Lupe. The meeting's "Marta and Grace had
     signed it under her" and Marta's "She's not wrong about the factories" now have their setup. The treasurer stays
     Reuben. 612 words in, none out. Corrected in place, 26 Nov (ninth chat, Claude's own review): Irene's mirrored "They weren't there about the pivot ... They
     wanted to know" became "Every time, honey, what they wanted to know was whether they still had a say on this
     road."; "Just don't tell yourself afterward it was free." became "and you know going in that some of them won't
     stay."; Marta's "It did. By spring it had given six of us the whole week." became "It did, for a while. By spring
     they'd laid off six of us." Logged only; not in the v6 Doc yet.

220. **Chapter 18 opens on Lou: Praether's war, and the ace in the hole.** CT (26 Nov): "Then in the next chapter the
     reveal: Praether is a Gulf War vet, and maybe this is where Lou tells Elijah and Grace to keep the arms to
     themselves?" A short scene before "Elijah's next crisis found him in late April", then a scene break. CT's, word
     for word: "You need to have an ace in the hole, Elijah," Lou said with a knowing gaze, "never reveal all of your
     cards again. I would have thought you'd have learned that by now." / Elijah felt the heat of embarrassment wash
     over him, but it was quickly softened by Grace, who wrapped her arm around him. / "Don't worry, Lou, I won't let
     him do anything stupid!" She smiled and looked him right in the eyes from inches away. / "Right?" / "Right," Elijah
     said, barely containing his enthusiasm to be so close to Grace. / "I won't do anything stupid." Three marks
     changed in his lines: "glaze" to "gaze", a comma after "Don't worry", and "Right." to "Right," before "Elijah
     said". Claude's: the lines before it ("Lou got the two of them alone the week after that dinner. He was weeding
     the end of a bed, and he didn't get up." "Grace says you met Richard." "He yelled at us about the military."
     "Richard went over to the Gulf in ninety-one. He came home with something wrong in him that nobody would put a
     name to, and the government has been writing him letters about it ever since. Most of what he says is true. He
     says it loud, is all." "Grace looked at Elijah. Neither of them brought up the envelope." "Anybody else know
     what's in his barn?" "No."). It answers Elijah's "Why?" in Chapter 17 ("He didn't say. That's Lou. You'll meet
     him."). Logged only; not in the v6 Doc yet.

228. **Lou comes in heavier, on Elijah's first night (Ch 16, 17, 33).** CT (26 Nov, eleventh chat): "maybe an
     introduction to Lou can come in a little heavier. There could be a discussion amongst some of the characters about
     the artist reaction to AI ... And then Lou could interject, like enter the conversation, enter the room, turn a
     corner or whatever, and say, they will adapt, as the Lamplighters did. And then we introduce Lou, and we give him
     a physical description. He's imposing, he's big, he's a big guy. But there's a certain temperance to him that is
     noticeable. He moves gently ... Lou's steps are light as a feather. Elijah should be reminded of his uncle, who
     was a Hopi tribesman ... but that's another story for another time ... Lou could say, like, does everyone please
     welcome our new guest, Elijah. He'll be staying with us for a while. And then I see in my head, like, that next
     chapter is like, nobody asked him any questions for about 3 days." Added at the end of Chapter 16, so Chapter 17
     still opens on his three days. His words: the four lines about the artists, Lou's lamplighters line, the
     description, the uncle, the welcome. Claude's: the people unloading the trailer, Lou's buckets, Grace's "Lou. This
     is him.", the last three sentences. The book's "about sixty, sunburned right up to his hat line" moved here from
     the Friday dinner. Forced by it: "a man named Lou" and "You'll meet him." (Ch 17); the pump house steps, where the
     stranger's one word "Lou," from CT's edit 89 is gone because Elijah has met him; "It was Lou, from the pump house
     steps." (the dinner); and Chapter 33's "Lou wasn't a big man", now "Lou was a big man". Row 89 narrowed. 302 words
     in, 47 out. Held for CT, from the same message: Rosa feeding him in the first three days, Rosa and the ladle
     ("the heart of a helper", the tamales), and "take this to Grace" with the talk about staying for free (Rosa is not
     on the farm before Chapter 38; reasons in the record). Record: `manuscript/novel/drafts/edit-228-lou-comes-in.md`.
     Logged only; not in the v8 Doc yet.

229. **Chapter 27: Curtis and the Riemann hypothesis, at Friday dinner; RSI; Grace's promise.** CT (26 Nov, dictated in
     two messages; the second extends the first, and replaces its last line in place). First: "this is the one that
     will really make it click for anybody who's out of the loop. The Riemann hypothesis ... Curtis can bring it to
     everyone's attention because that's kind of his role ... they're all just chilling. It's a normal day. And this
     doesn't need to be a new section or a new chapter or anything. This can be worked into an appropriate spot ... it
     can go in the proper timeline in the book with real life ... the fact that it shocks Marta makes the others kind
     of snap in. Because Curtis is a wingnut. But there can be a moment where they really lock in because Marta's
     shaken." Second: "And then maybe Marta can explain, and it always will ... Elijah's going to think to himself, so
     it can do everything I did at Claypot and more. And maybe one of the more naive people, like younger, whoever's
     there that's the youngest ... And then Elijah speaks up. It means we're one step, well, more like one giant leap
     closer to RSI ... Elijah's like a little suspicious of their naivety from that point forward ... I feel like this
     is kind of a linchpin scene for what happens later with the ASI sort of like all of a sudden existing." Then the
     talk with Grace, which he chose over giving the Will Smith line to Curtis ("I think it would be better if it was
     that"), through "I promise" and "thank you, I believe you."
     Where: after "He'd never answered David ... he didn't know how to start.", before Thanksgiving 2026. The real
     announcement was Friday, 20 November 2026, so it is that week's Friday dinner. No scene break.
     His words: every line of dialogue except the ones named below; the chorus paragraph; "Curtis was a wingnut";
     "Marta was shaken"; the hand wave; Elijah's two thoughts; the room going silent; the twinkle; people grumbling and
     walking off; "That was how people had been reacting so far ..." to the end of that paragraph; "She got it, but she
     didn't totally get it."; taken aback, the furrowed brow; both bodies tensing; the gesture at the notebooks; the
     hands, the forehead, the hair. "I don't like doing my homework" is left out: he restated it as "I don't like doing
     math problems."
     Claude's choices: who says the lines he left open. Grace ("what does that mean"), Frank ("those of us that don't
     speak math"), Denny ("why are you freaking out", "What is that?"), Tyler (cryptography and bank accounts). The
     youngest at the table is Tyler, so the "who cares" lines, "RSI?", the video game and GTA 6 are his; Chapter 26
     already has him working something out and never saying a word, and Chapter 38 has his "Finally."
     Claude's wording: the opening paragraph; "Curtis hadn't sat back down."; "Curtis went right past him."; "That was
     Marta, from the far end of the table."; Tyler's "Perelman. Russian guy. Twenty ten. He literally said no to a
     million dollars."; "and she stopped there"; "and the table had learned to eat through his headlines"; "Sentences
     didn't get left unfinished when they were hers. The forks stopped."; "There was nobody at that table whose opinion
     she respected more."; "She thought for a second."; "Lou laughed so hard he had to put his cup down. Marta didn't
     laugh."; "He meant recursive self-improvement, a machine that could do the math to build a better machine." (the
     book spells the idea out once, in Chapter 3, and never uses the letters RSI); "Heads shook up and down the table."
     and "somebody said"; "But Tyler went right back to it."; "Grace stayed behind after the rest had gone. She had
     questions."; "these dishes" in Grace's last line (he left the next thing open).
     Facts looked up, 26 Nov (web search; the articles themselves could not be opened from this session): an Anthropic
     mathematician announced on 20 Nov 2026 a proof found with an unreleased model, checked by computer and certified
     the next day; mathematicians have not yet read it through and the prize institute still lists the problem as
     open; the problem dates from 1859; OpenAI announced a Navier-Stokes solution on 8 Sep 2026 (NPR, 22 Sep), used for
     CT's "the Neumann flow or whatever"; Grigori Perelman turned down the million in 2010 (Poincare conjecture); GTA 6
     came out on 19 Nov 2026, the day before. A proof does not break cryptography, which is Marta's "not exactly". The
     book names no real lab, so neither does the scene.
     Forced by it: "Thanksgiving came two weeks after that." becomes "Thanksgiving came the week after." (row 222
     narrowed; row 229 checks the new words). 1,049 words in, 6 out. Record:
     `manuscript/novel/drafts/edit-229-riemann.md`. Logged only; not in the v8 Doc yet.
     Context from CT, NOT for the page (26 Nov): "I know I said already a bunch of times that I don't want to add
     anything new, and I really don't, but this is the one that will really make it click for anybody who's out of the
     loop." On Tyler: "now he suspects that this other person knows too. More than they're letting on. Which will not
     pay off. We don't need to make that necessarily pay off, but we could just like loosely connect it with following
     events". On what comes after: "we may even not need to mention it again after this because it's like really clear
     where it's headed for anybody that gets it. But for people who don't get it, it might be a bit of a jump. But
     that's okay, because it'll feel like a jump in real life." Not used: Curtis saying the Will Smith line (he chose
     Grace and Elijah). Grace's promise is not picked up again anywhere in the book (checked 27 Nov). The source links
     and the rest of that chat's notes: `CHECKPOINT-2026-11-26-riemann-praether.md`, first section.

230. **Chapters 17 and 18: Praether's terms, "I speak wingnut", and Lou at the barn.** CT (26 Nov, dictated): "The
     warning given by Richard Praether when they're out there talking to him ... yeah, I heard from whoever that you
     wanted to store some robot arms out in my old barn. I don't care about that as long as they're unplugged and
     turned off and the military can't access them ... we don't have to say taken aback because we've already had that
     a few times ... The guy says some other stuff. You can help me with that part ... he gets the names wrong. But he
     doesn't care ... as far as I can remember, they're not dating at that point. So Grace stammers ... She wouldn't
     put it back down on the ground. She puts it in the mailbox ... then the next beat should just say, the arms
     arrived on time. Elijah canceled the storage unit. And had someone ... Won't be Grace ... It would make sense if
     it was Lou, actually. Because then Lou can warn Elijah to keep it a secret ... And then he has that exchange that
     we talked about earlier ... they're your people too now. And he looks him in the eyes real serious. He's like,
     don't forget that."
     What changed in the book. Chapter 17: Grace and Elijah now go out to Praether's before the arms come, on foot up
     his drive, and make the deal; the arms come on the Wednesday and Lou, not Grace and not Praether, puts them in
     the barn with Elijah. Replaced: the delivery scene of edit 205 from "The arms came up the day before the lien
     sale." to "Neither of them said anything until the grange." (533 words out, 1,018 in). Chapter 18's opening
     (edit 220) keeps Lou telling the two of them about the Gulf and Grace's lines; the ace in the hole moved to the
     barn.
     His words: Praether's lines from "you want to store some robot arms out in my old barn" to "If something else
     comes up, I'll let you know."; Elijah's and Grace's answers; "Grace went to argue."; the shake; the grimace and
     the smile; "He had the names wrong, and he didn't care."; "What the hell was that?" and "I speak wingnut"; "maybe
     I should", "maybe I shouldn't", "maybe we shouldn't" and the mailbox; "The arms arrived on time. Elijah canceled
     the storage unit"; all of Lou's lines and Elijah's at the barn. Lou's "You need to have an ace in the hole,
     Elijah," Lou said with a knowing gaze, "Never reveal all of your cards again. I would have thought you'd have
     learned that by now." and "Elijah felt the heat of embarrassment wash over him" are his from edit 220, joined to
     the new wording. His "whoever" became Lou ("Lou maybe was the one that connected him with Richard"). His "I like
     Ike, whoever it was" became "Like old Ike said."
     Kept from the book: his description of the yard; Praether's looks and the burn barrel; "I can't pay much" and
     the brush hog, one Saturday a month (Chapter 26 depends on it), as the "other stuff"; one finger up and "Mark my
     words."; the barn's air; the loader and the tie-down that lets go with a bang, with Praether now going down on
     his porch and Lou watching; "Some nights he drove out and looked at the barn from the road."
     Out: "What's in them?" "Arms."; "Beware the military! They never built one thing ... That's how you'll know."
     (the warning is now the military-industrial complex); the gas station movie talk in the truck (replaced by "I
     speak wingnut"); the grin going off Grace's face.
     Claude's wording: "Getting them north was the easy part."; "Lou said he'd have a word with Richard Praether
     first. Then Grace and Elijah drove out the county road in the Ranger to ask the man themselves."; "They left the
     Ranger by the mailbox."; "Grace and Elijah looked at each other, and then at him."; "Praether's face had set into
     a big grimace."; "The grimace went"; "down the drive"; the letter's corner and "gone soft with rain, like it had
     been there a while"; "The door was unlocked, like Praether had said it would be."; "Up at the house, Praether was
     down flat on his porch boards"; "Lou watched him do it and said nothing."; in Chapter 18, "Richard give you the
     speech?", "The military-industrial complex," and "Good. Keep it that way." Tyler at the hardware store still
     names Praether's barn first (Chapter 19 says he sent Elijah out there).
     Corrected in place the same day. CT: "I don't think actually they would bond over just a tinfoil hat comment.
     Richard would push back." His: "You messing with me, son?", the reptilians, the look, "I'm not trying to help no
     lizard people", the laugh, "I like this guy. All right, yeah, we're good. You can keep your arms here. It's going
     to be all right. I'll keep them for as long as you need me to. Unless something else comes up, I'll let you know."
     and "And then he doesn't" (on the page: "He never did."). Out: "The grimace went, and Praether threw him a smile.
     You sure will. I like this one." and "as long as I can". Claude's: "Praether wiped his eye with a knuckle."
     Then CT: "We could use the phrase rattle in his voice for old Richard", on his first line, "Like a can of paint
     being turned over." It is now on "Lou tells me you want to store some robot arms out in my old barn," Praether
     said, "a rattle in his voice like a can of paint being turned over."
     Rows 88, 205, 220 and 222 narrowed. Record: `manuscript/novel/drafts/edit-230-praether-and-lou.md`. Logged only;
     not in the v8 Doc yet.
     Context from CT, NOT for the page (26 Nov): "The arms, stay there for a while ... However we resolved it before."
     They do: offered and refused in Chapter 34, left in the barn in Chapter 37. Praether's "I'll check them myself"
     and the ordnance are not paid off, which is his call (the eleventh checkpoint, "Open with CT"). Since edit 233 the
     secrecy is said once, at the barn. The lien sale needs nothing: Lou covers what is owed before the visit, so the
     sale is off (checked 27 Nov).

231. **Chapter 17: Grace's talk about the bed and staying for free.** CT (26 Nov, eleventh chat), dictated with edit
     228 and held then; placed on his next word, "Send out readers, evaluate what you think is the best course of
     action". His, word for word, fillers out: "How are you liking your bed? Is it comfy enough?" / He raised an eyebrow.
     "Yeah, it's great. It gets a little cold in there at night, but you guys give me plenty of blankets, so I feel
     really good. Thank you. I'm really grateful for this." / "No problem." / "So when do I start paying, or sign, or
     whatever?" / "No, I meant it. You can stay here for free as long as you like. It's just good to have people like
     you around, you know?" / "What do you mean, people like me?" / "You know, people who get it. Every one of these
     families came to us in one way or another, but we're all contributing to the success of the farm." She started
     eating. "I trust you'll do the same." / He thought about it, and lingered a minute. "Is this too good to be true?" /
     "What? You want something?" / He raised his eyebrows and blinked a few times. "No, I'm good." / "Great. Close the
     door on your way out, would you?" After "she let the six lines be all of it.", before "Marta gave him the floor."
     Claude's: "One night, when he had finished, she sat down across from him with a plate of her own." (Rosa can't send him
     in his first days: she lives in town, wrist in a brace, and he meets her on the route weeks later.) "Stay here for
     free" is the room, as her message has it; the pay still goes to the table (Ch 16, 26). 186 words in. Record:
     `manuscript/novel/drafts/edit-231-232-grace-and-rosa.md`. Logged only; not in the v8 Doc yet.

232. **Chapter 27: Rosa makes Thanksgiving 2026; her grace and the ladle.** CT (26 Nov, eleventh chat), held with 231:
     "maybe Rosa can come back in later in the book as like part of the proletariat". First placed as the opening scene
     of Chapter 31; moved on 27 Nov on his word: "And the meal is Thanksgiving, maybe? and they pray", "Rosa's own
     grace, in Spanish, whatever Hispanic Catholics say as she holds a rosary", and "It's her first time making
     Thanksgiving dinner for the farm, but she's got lots of experience" with her line, word for word: "I had a big
     family, but life, it get away from us. The love is still there, deep down, even if the finances maybe get in the way
     sometimes," Rosa explained. "But this last year I volunteer at the church kitchen and we cook a lot of
     food, I cook all day, and now I cook all day here for you!" / "I know someday I cook for my family again. But
     maybe sometimes is ok to give love a little breathing room." / She set a casserole dish on its trivet, and the
     feast began. (His "placeholder"; CT: "The coaster thing".) ("Sorry better Spanglish": "life, it get away from us".) Then, his, from 26 Nov: "I don't really understand all
     this technology stuff," she said. "It goes over my head. In one ear, out the other." / She paused, turned around
     with the ladle ... "I do know good food. In this place, they make a lot of good food. Nourishes the whole
     community." She pointed at him and tapped him on the chest. Then she put her whole palm on his chest and rubbed it
     in circles. "You have the heart of a helper. I can tell." / "I just want everybody to be prepared," / "Prepared is
     sometimes not helpful. Sometimes you can over-prepare. If I over-prepare my tamales, they fall apart. They don't
     taste too good." / Elijah kind of got it. / "Please take this to Grace. It's her turn to eat." The grace is the
     standard Spanish Catholic blessing before meals, in italics: *Bendícenos, Señor, y bendice estos alimentos que por
     tu bondad vamos a recibir. Por Cristo nuestro Señor. Amén.* Claude's: "Rosa made the dinner that year, her first for
     the farm." (his fact), "since before it was light", the brace, Curtis's question, the clapping and the dish towel,
     the rosary in her apron pocket and her good hand, "Before anybody ate", "Elijah carried pots.", the app for the
     holiday route, "and filled a bowl", "She held out the bowl." Between "he said yes before he had thought about it."
     and "After the kitchen trailer fed forty,". Forced by it: Chapter 38's "And Rosa, at her first dinner, in a good
     blouse," is "And Rosa, in a good blouse,". Her lesson now comes before the county meeting (Ch 30); Chapter 31's
     "One page. He had learned that much." is where it lands. "for the last couple years" became "this last year" on his
     word, so Chapter 17's spring 2025, when she can't cook, stays clear. 361 words in, 3 out. Record: `drafts/edit-231-232-grace-and-rosa.md`. Logged only;
     not in the v8 Doc yet.

233. **The finishing pass (Ch 0 to the Appendix).** CT (26 Nov, eleventh chat): "Send out readers ... to finish the
     story arc, to finish the narratives, to finish the characters, to finish everything. After this, if possible, I
     don't really want to change or add anything." Seventeen readers, 69 gaps, 33 verified on the page, a plan judged
     from three and checked by a critic. 30 line fixes, all Claude's wording: Ch 0 "Elijah said it once to Wes" and
     "didn't know him"; Wes's *is this true* back in the Ch 6 and Ch 13 replays; Ch 17 Lou's cover a gift (Grace's line
     out, the secrecy now said once, by Lou at the barn), Priya's pencil back behind her ear; Ch 18 "Grace and Elijah" and
     "Good. Keep it that way." out; Ch 26 "That was in the first notebook" (he heard the Architect's answer in Ch 9) and the July
     coffee "at the kitchen trailer"; Ch 27 "in June" out of the pledge, Tyler's reading covers the boxes, and a scene break between the two
     Fridays; Ch 29
     "delivery time"; Ch 31 "A hundred strangers" twice and Denny's daughter; Ch 32 "a whole file", "six years" out,
     the second "Halve it" out, "till June" out; Ch 33 the Ohio machinist's household and Lou's back seat "before her
     shift"; Ch 34 Marta's welder at the shop after the plant, "What guy?", "found the price list"; Ch 36 Irene's step
     and "Two years before ... eight feet" out; Ch 39 "A while later"; Praether in the Appendix. Rows 197, 205 and 220
     narrowed. Items 1 to 3 of the fix list in `CHECKPOINT-2026-11-26-riemann-praether.md` are done here; that chat's
     edit 230 had already settled three places this pass found in Ch 17. First logged as 229 to 231, renumbered at the
     merge. Left for CT: Ruby's numbers (Ch 8), "Grace printed your cover page" (Ch 17), "signed right under her"
     (Epilogue). Record: `manuscript/novel/drafts/finishing-2026-11-27.md`. Logged only; not in the v8 Doc yet.

234. **Grace doesn't know about the arms until the table finds out (Ch 17, 18, 34, 35, 36).** CT (27 Nov, dictated in
     the Riemann chat): "Wait, if they argue about this at the table at that time, and Grace knew about the arms the
     whole time because she went with Elijah to the old guy's house, then why wouldn't she suggest the fix sooner? She
     can't know about the arms. It has to be a secret he's been keeping from her, or else the breakup doesn't work.
     She has to find out there in that moment and then react so strongly. You've been lying to me this whole time?
     You've kept the arms from me this whole time? How did I not know about this? So Elijah and Lou go together. And
     then Grace and Elijah fight, but Grace and Lou don't necessarily need to talk about the arms. She might confront
     him later at some point and be like, did you know? Lou's like, yeah, I helped him move the arms over there. Maybe
     that happens at the dinner. And now Grace is just pissed."
     Context from CT, NOT for the page: "But she wants a father figure so bad, she doesn't want to lose Lou. She
     doesn't want to lose Elijah either, but she's mad enough at Elijah that she chooses the farm, her home, and Lou
     over Elijah. Misplaced anger. This is classic."
     What was in the way: Grace has known about the arms since her first message (Ch 15: "Your arms can live there for
     free"), she asks about them on the fourth day and passes on Lou's cover (Ch 17), edit 230 took her to Praether's,
     and Chapter 18 opened with Lou swearing her and Elijah to secrecy. His decision of 26 Nov (the plan, 10.5: "a
     secret between Lou, Grace, Elijah, and, eventually, Marta") is replaced by this one.
     His words on the page (Ch 34): "You've been lying to me this whole time?" "You've kept the arms from me this whole
     time? How did I not know about this?" "Did you know?" "Yeah. I helped him move the arms over there." Lou's
     admission is at the dinner (his last word on where). Lou's own line from the plan follows it unchanged ("I told
     our friend Elijah to keep the arms a secret ...").
     What changed, chapter by chapter:
     - Ch 17, the fourth day. Elijah tells Grace the arms are gone, a lien sale, and leaves out that the sale is not
       until the end of the week. She says she is sorry and never asks again. Lou hears it from her, asks him when the
       sale was, gets "This Friday", covers the unit and keeps it between the two of them. Her message in Chapter 15
       stands.
     - Ch 17, Praether's. Lou goes with Elijah in Grace's place: "Lou here tells me", "Elijah and Lou looked at each
       other", Elijah asks about the ordnance, "Look, kid" (was "Look, lady"), "Lou went to argue.", "Don't let him go."
       is said to Lou ("I don't intend to," Lou said.), "What the hell was that?" is Lou's, Elijah picks up the VA
       letter and puts it in the mailbox, and Lou says "Yeah, maybe we shouldn't". Lou tells him about the Gulf in the
       truck (the lines moved from Chapter 18).
     - Ch 17, the barn. After "Keep it close to your chest.": "Grace thinks they went at the sale." "Then let her think
       it," Lou said. "Grace most of all. She'd want to put them to work, and this place isn't ready for that." The
       three in "between the three of us" are now Lou, Elijah and Praether.
     - Ch 18. The opening scene with Lou, Grace and Elijah is cut, with its scene break. The chapter opens on "Elijah's
       next crisis found him in late April".
     - Ch 34. Grace's lines and Lou's answer, after Priya's "this entire time?". Then: "Grace opened her mouth, and
       shut it. She turned back around in her chair." "Grace had not looked at him once." is "again."
     - Ch 35. "What's Grace say about the arms?" / "She hasn't said." is "Grace talking to you yet?" / "No."
     - Ch 36. In the packing shed: "She had hardly spoken to him since the meeting." The fight at the fire is not
       touched.
     Claude's wording and invented facts (all his to change): everything in the fourth-day passage (the lie itself,
     "Grace said she was sorry. She never asked about them again.", Lou's two questions on the pump house steps,
     "Elijah took too long to answer.", "This Friday", "Lou didn't say."); "to ask the man together"; "here" in "Lou
     here tells me"; "kid" for "lady"; "I don't intend to," Lou said.; "in the truck"; both lines about Grace at the
     barn, including Lou's reason for keeping it from her; "She had turned in her chair to face him."; "Grace," he
     said, and that was as far as he got.; "She turned on Lou."; "Grace opened her mouth, and shut it. She turned back
     around in her chair."; "Grace talking to you yet?" / "No."; "She had hardly spoken to him since the meeting."
     His lines that came out, because they only work if Grace knows: from edit 220, "Don't worry, Lou, I won't let him
     do anything stupid!" She smiled and looked Elijah right in the eyes from inches away. / "Right?" / "Right," Elijah
     said, barely containing his enthusiasm to be so close to Grace. / "I won't do anything stupid."; from edit 230,
     "I, uh," Grace said. "I ...", "Grace went to argue." and "Look, lady". They are kept in the record so he can
     place them elsewhere.
     Held for CT (one question): the fight at the fire (Ch 36) never mentions that he hid the arms from her. It
     reads as her wanting them used and him refusing. Should she throw the three years of hiding at him there, in
     his words?
     Also settled by this edit: "Grace telling Marta about the arms" (the plan, 10.5) cannot happen and is off the
     open list. Rows 205, 213, 214, 220, 223, 230 and 233 narrowed. 103,503 words in the chapters (60 more than
     after 233). Record: `manuscript/novel/drafts/edit-234-grace-doesnt-know.md`. Logged only; not in the v8 Doc yet.

Corrected in place, 26 Nov (eighth chat): edit 205, Praether's lines as "an homage to pop culture for moments like
these", with the twist delivered by Grace at the mailbox (CT). Praether puts one finger up: "Mark my words." "Beware
the military!" stays, with "They never built one thing in their lives ... they come around with a check. Somebody
always wants the thing that works." and "Don't say nobody warned you." Out: "I carried what the nice kids built" (it
gave the war away before the letter). New, in the truck: Grace laughs at the end of his drive. "Did he say beware?" "He
said beware." "He's the guy at the gas station. In the movie." She put one finger up. "Don't go up to the lake, kids.
Mark my words." "What happens to the ones who go up to the lake?" "Nothing good, Elijah." Then the envelope: "the grin
went off her face before she put it in the box." All Claude's words except "Beware the military!" No film is named.

219. **Chapters 11, 13, 15 and 19: five continuity fixes.** CT (26 Nov): "Yes pelase did the continuity errors." From
     `STORY-REPORT-2026-11-26.md`, section 6. Words by Claude.
     - Ch 11: "He carried the amp down the stairs himself, and it went into his mother's barn under a moving blanket"
       becomes "He carried the amp down the stairs himself. At his mother's he set it on the back porch, and by the next
       morning she had it out in the barn under a moving blanket". He isn't in the barn in April, so it can be full in
       Chapter 13. **Invented: Ma is the one who carries it out there.**
     - Ch 13: "since Monday night" becomes "since Sunday night" (he calls Sunday and gets no answer).
     - Ch 13, the week of the sale, which ran Friday, Wednesday, Thursday: "On Wednesday he drove into town" becomes
       "Two days before that, on the Wednesday, he had driven into town"; "David showed up Thursday morning" becomes
       "David showed up the next morning".
     - Ch 15: "He had not opened the case since the last gig." becomes "He had hardly opened the case since the last
       gig." (he plays it in Chapter 5).
     - Ch 19: "The cases came from a kid named Tyler. Tyler worked the register at Kowalski's Hardware in town, where
       Elijah had bought the screw terminals" becomes "The cases came from Tyler, the kid at the register who had sent
       him out to Praether's. Elijah had been buying the screw terminals at Kowalski's" (he is met in Chapter 17, edit 205).
     Logged only; not in the v6 Doc yet.

218. **Chapter 39: Devendra's text.** CT (26 Nov): "Devendra could text Elijah after the AGI comes out 'Dinner's on me!'
     And that would be a good closure in the final chapter before Elijah walks out into the night air." After
     "No, I didn't." and before "Elijah donned his jacket.": "His phone buzzed against his leg. It was Devendra.
     *Dinner's on me!*" The text is CT's, italic; the line before it is Claude's. It pays the bet from Chapter 1.
     Bidwell's "somebody" is never named (CT: "we never need to reveal the somebody"). Logged only; not in the v6 Doc yet.

217. **Chapter 37: the arms are at Praether's.** CT (26 Nov): "Resolve the contradiction because the arms should be in
     Praether's barn." "All that was left were two robot arms in the back of the equipment shed." becomes "All that was
     left were two robot arms in Richard Praether's pole barn." Row 178's check was narrowed. Logged only; not in the
     v6 Doc yet.

Corrected in place, 26 Nov (eighth chat), on CT's eight choices (none of it in the Doc):
- Edit 204: the October night is its own chapter, "Pondwater" (CT: "title it 'Pondwater'"), set as a heading with no
  number, like "Meanwhile", so Chapters 27 to 39 keep their numbers; it is in the Contents after Chapter 26. On the
  blanket: "We should start a band" (Claude), "We should call it Pondwater!" (CT's line), they laugh, and it turns
  tender. Then Grace on her father, from CT's words, put in her mouth: "He started drinking when I was in high school.
  Then it was harder stuff than drinking. I made a lot of weird choices back then. I was a little festy girl." and
  "He's still on that porch. Numb. Barely himself anymore. The father who raised me is gone. The one I love, the one I
  grew up admiring. What's there now is a husk, a shell, a container for my father's soul. I grieved him and let go of
  him a long time ago." Then "That was all she said about it." (CT: "That's all she really needs to say about it").
  After Marta's "Don't make me sorry.": "He had dated a few festival girls in the past. That hadn't exactly gone so
  well for him. But Grace seemed like she had it all together." (CT's words). "practically a parade" (used of Marta in
  Chapter 19) becomes "a blessing".
- Edit 204, Praether at his mailbox (CT: "yes gulf war vet"): after "So did ours, the first year." he holds up an
  envelope: "They gave us pills in ninety-one and said take them. Then they blew an ammo dump upwind of us, full of
  nerve gas, and wrote and told me about it six years later. They still write." "Real polite letters." Claude's
  words. Sourced: pyridostigmine bromide pills under an FDA waiver (January 1991); the Khamisiyah demolitions (4 and
  10 March 1991); the Defense Department's letters to veterans (1997, again in 2000). Chapter 17's speech stays as it
  was, so the VA letter is still the reveal.
- Edit 198, the truck stop (CT: "yes. Fix it for nothing thank you."): after "The money for Ma's room was for Ma's
  room.": "Ahead of him were seven hundred miles with nobody on them. Behind him were a hundred, and a man who would
  fix it for nothing." Claude's words. **Invented: seven hundred miles left to go** (the book puts him about a hundred
  miles south, past Yakima).

Corrected in place, 26 Nov (eighth chat), on CT's direction about the two rovers (his words in
`PLAN-CHAPTERS-20-TO-36.md`, section 10.8; none of it in the Doc): edit 204, the rover is a JetAuto Pro, the smaller and
cheaper of two, bought on Lupe's "Could I pick it up?", and Curtis and Elijah program it together (Ch 26; "parked at the
end of bed four" in Ch 33); edit 213, the table votes for the tall one (Lupe: "I can't carry that"; the Trekkie exchange
moves here), then refuses the arms, and the chapter ends on CT's kitchen scene word for word ("the militarization of
the farm"; "The shape of monsters is noticed more in the dark"; catgirls; Priya's pencil); edit 215, Chapter 36 opens on
the Ochoas leaving; edit 216, Ch 38 reads "the new rover stood parked over bed four."

216. **Chapter 38: the last "gantry" is the rover.** CT (26 Nov): "It's meant to be a rover. Not a gantry." Book now:
     "the gantry stood parked over bed four with its arm tucked up"; change to "the rover stood parked over bed four with
     its arm tucked up". His reference for the machine: the Hiwonder JetAuto Pro
     (https://www.hiwonder.com/products/jetauto-pro), a small four-wheel mecanum robot with an arm, lidar and a depth
     camera. Logged only; not in the v6 Doc yet.

215. **Chapter 36: festival week, Lou's squash row; one debt in the fire.** From the plan; written by Claude (Book now and
     Change to in `manuscript/novel/drafts/chapter-36.md`). Twenty people did the work of forty; Elijah picks Lou's row by
     hand; three day names out; "What choosing for people looked like, he knew." back to "He knew what choosing for people
     looked like." (undoing edit 172's inversion; row 172 narrowed). The fire otherwise as written. 2,167 words to 2,208.
     Logged only; not in the v6 Doc yet.

214. **Chapter 35: the night scene cut to the walnuts, the man who refuses, and ALC; Lou lets Grace drop.** From the plan;
     written by Claude (Book now and Change to in `manuscript/novel/drafts/chapter-35.md`). Lou's second speech about
     mothers and "mutually assured survival" come out; "What's Grace say about the arms?" "She hasn't said." and he lets
     it go; "They can. They just won't." out (edit 174's debt); "this lady," "the steam engine," "In the same lane" and a
     bare "man" fixed. Row 174 narrowed. 1,686 words to 1,392. Logged only; not in the v6 Doc yet.

213. **Chapter 34: Curtis's wound, the arms revealed, the war on the phones, Curtis the Trekkie, the Ochoas leave.** CT's
     direction of 26 Nov, with his lines for Priya, Lou, Curtis and Marta word for word (listed in
     `manuscript/novel/drafts/chapter-34.md`, with Book now and Change to). The arms are in Praether's barn "since my first
     week"; Lou's "I told our friend Elijah to keep the arms a secret"; Lupe and the footage from Ukraine; "I'm also a
     Trekkie" and "You want your own Commander Data"; Curtis's granddad's wheat ("I held the gate for them"); the table
     still tables it; the Ochoas leave and Lupe gives Grace the clipboard. 2,320 words to 2,669. Logged only; not in the
     v6 Doc yet.

212. **Chapter 33: Denny comes back; "I sold it to them"; the tomato dinner trimmed.** From the plan (CT: Denny leaves and
     comes back); written by Claude (Book now and Change to in `manuscript/novel/drafts/chapter-33.md`). Denny at the gate
     with a script and a company polo, "Nobody ran me off. That was me."; Elijah tells the table he sold his mother's
     place to them and answers Reuben; the second "Listen to me" comes out. The rest of the planned cut to Lou's dinner
     speeches waits on CT (they may be his). Row 182 narrowed. 4,255 words to 4,363. Logged only; not in the v6 Doc yet.

211. **Chapter 32: the late payment, the missed stop, the April quarrel, the coffee can.** CT's ask of 26 Nov (the missed
     payment echoing his mother; a worse quarrel than the first; he apologizes; frozen yogurt; "it's his fault, or so he
     thinks"), to the plan's section 10.3; written by Claude (Book now and Change to in
     `manuscript/novel/drafts/chapter-32.md`). Grace buys him a week; Mrs. Delgado's box sits at the gate; Irene's "Tell
     Reuben I don't mind waiting"; "A coffee can of order slips, in the barn"; "Don't handle me. Not like she did."; he
     goes after her; "One cup. Two spoons."; the change can on the Friday table. Also Frank's chart, the truck song low,
     Frank for Denny in the juniper scene. 2,068 words to 2,989. Logged only; not in the v6 Doc yet.

210. **Chapter 31: Denny leaves; "Nothing that mattered" on the page; the roster cut.** From the plan (CT: "Denny leaves
     and comes back"); written by Claude (Book now and Change to in `manuscript/novel/drafts/chapter-31.md`). Denny on his
     porch, "Because you said it out loud," gone by the weekend; Grace deciding, in front of us, to say "Nothing that
     mattered" (its summary in Ch 32 comes out); the roster paragraph cut to CT's lines about his father; two line flags.
     Rows 58, 172, 175, 182 and 187 narrowed or updated. Ch 31, 2,996 words to 3,146. Logged only; not in the v6 Doc yet.

209. **Chapter 30: Priya and Grace the night before, Denny's last video, Lou's "my man".** From the plan and CT's ask
     ("Priya and Grace need to talk"); written by Claude (Book now and Change to in `manuscript/novel/drafts/chapter-30.md`).
     Priya on one number and the red light; Grace, "You open with who," and a name on the back of her hand, which turns
     out to be Rosa's; Denny films and hands Tyler the tripod; Lou's "man" twice to "my man"; "changed 'more' to 'the
     rest.'"; two day names out. 2,074 words to 2,307. Logged only; not in the v6 Doc yet.

208. **Chapter 29: the women at the grange hall, Denny argues, Lupe, Tyler's yes, the welder gap.** From the plan and CT's
     ask for scenes with only women; written by Claude (Book now and Change to in `manuscript/novel/drafts/chapter-29.md`).
     Marta, Yvonne, Lupe, Rosa and Irene in the grange hall kitchen; Denny's "I'm not burned out. I'm unpaid." and the
     tool company's number; Lupe's "Somebody quits."; Tyler's "Does it pay?" "No." "Monday."; Marta's "Somebody whose
     coupons bend."; Priya's "Log it." 1,821 words to 2,141. Logged only; not in the v6 Doc yet.

207. **Chapter 28: one night dark, power when it counts, the Ochoas' house off the map.** From the plan and CT's direction
     (overnight; power when it counts; the panels cut costs); written by Claude (Book now and Change to in
     `manuscript/novel/drafts/chapter-28.md`). The battery bank carries the mesh, the freezer and the kitchen trailer;
     Denny films it; Lupe on the radio, "We're just not on your map."; the soup comes up the trail to meet them; the
     county's power is back by morning. The lines re-teaching the two-person rule come out. 1,125 words to 1,194. Row
     179 updated. Logged only; not in the v6 Doc yet.

Corrected in place, 26 Nov (eighth chat), from `STORY-REPORT-2026-11-26.md` (none of it in the Doc): edit 201, the board
confession is played with his words and Marta's "You let me say that. Ours.", and Grace tells Patricia it wasn't Tyler's
code; edit 203, Chapter 24 opens on Elijah carrying the first new board to the Ochoas (Hector: "Took you a month.";
Lupe's clipboard, INSTALLED BY); edit 204, Ma's fall stays open overnight, the year gets his side of it, and Praether
appears once more ("So did ours, the first year."). Rows 137 and 182 updated to the confession's new words.

206. **Chapter 27: what the farm lives on, the knockoff, the pledge and the Ochoas, Thanksgiving 2026.** From the plan,
     the to-do list and the story report; written by Claude on CT's "Do it" (Book now and Change to in
     `manuscript/novel/drafts/chapter-27.md`). The co-op's money named (the farmers market is CT's); Grace, Frank and Marta
     answer the $49 knockoff; the pledge carries the Ochoas' greenhouse and a no-machine clause, the co-op signs, Lupe
     signs and Hector won't ("Nobody was checking. Your leaf don't fix that."); Thanksgiving 2026, a route instead of the
     drive home, dinner in Grace's room in Ardell, a letter to Ma. Line flags, counting and day names fixed. 2,046 words
     to 2,294. Row 172 narrowed. Logged only; not in the v6 Doc yet.

Corrected 26 Nov (eighth chat), after the evaluation in `STORY-REPORT-2026-11-26.md`, as new rows under edits 198 and 199
(the old words are in the v6 Doc): Lou's "Those boxes go out in June either way" is "in May" (Ch 19); Marta's "starting
to see come out, Elijah." is "spreadsheet" (Ch 19; Chapter 37 says "She had never called him that, not once"); "Nine
months" and "the nine visible months" at Frank's counter are eight (Ch 25).

205. **Chapter 17: the arms go to Richard Praether's.** CT, 26 Nov (his words in `PLAN-CHAPTERS-20-TO-36.md`, section
     10.5): Elijah wouldn't trust the farm with the arms in his first week; a lead from Tyler; "a weird old man" whose
     yard is "a dump"; "Beware the military!"; a veteran with PTSD, shown by the VA letter Grace finds by the mailbox;
     a secret between Lou, Grace and Elijah. Written by Claude; Book now and Change to in
     `manuscript/novel/drafts/chapter-17.md`, CT's words in bold. It changes edit 88, which is in the v6 Doc: the arms no
     longer go into the equipment shed and the table doesn't vote on the storage bill (Lou covers it). Check row 88
     narrowed to the words that still hold. Chapters 34 and 37 still say "equipment shed" until they are done.
     Logged only; not in the v6 Doc yet.

Corrected in place, 26 Nov (eighth chat), after three readers audited continuity across edits 198 to 204 (none of it in
the Doc): the boxes ship in May (Chapter 19, one word), not June; the plugs cook in June, not July; Ma's room is back
home and Ray's service is at St. Rose, not in Santa Rosa; the letter scene loses "Sunday nights," "paid through March"
and "without knocking"; Tyler asks for work "that pays"; the last hose clamp; Tyler is nineteen in fall 2025; eight
months, not nine; Marta's scene remembers the kiss ("She kissed you at that pond a year ago, spreadsheet, and you're
asking me."); "Grace had knocked once, at the pond."; Curtis drives the route; the pay vote is in July. The full list is
in `PLAN-CHAPTERS-20-TO-36.md`, section 12.3, and at the foot of each chapter's file in `drafts/`.

Corrected in place, 26 Nov, after an audit of the day's edits against CT's standing rules (none of it in the Doc):
written messages set in italics in edits 196 (Mr. Ostrander's messages and Elijah's replies), 198 (*Dear Ma*) and 200
(*You're a liar. And you need to stop.*; Marta's card, *Power or brain? Halve it.*); two day names that only marked
time taken out ("since Tuesday" in 200 is "in days"; "He had seen it on Tuesday" in 201 is "He had seen it the night
the plugs cooked"). The audit and the rules are in `WRITING-INSTRUCTIONS.md`.

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


## The counting pattern, swept 26 Nov (Chapters 0 to 19 and 37 to 39 logged as edit 197; 20 to 36 in the rewrite)

CT, after edit 196: "Don't do the pattern. He read it twice, then he wrote back." Then: "it's boring and repetitive.
Send out some readers and find other instances of that pattern." A script listed 75 candidates; two readers judged
them and found about 70 more by hand. Line numbers are make_v6.py's v6.txt with edits 1 to 196. "(logged)" means the
line came in through an earlier logged edit, CT's words or Claude's.

Chapters 0 to 19 (36): 72 underlined it twice / Then he'd gone back to nodding; 216 David "a second longer than he
needed to. Then he went to change a keg" (and 1816 Curtis, the same move, logged); 227 left the tower off for a week.
Then (logged); 332 Then he watched it again (logged); 341 Then he sat very still; 370 Then he needed energy figures;
404 Then he came back, put on the drugstore glasses; 467 Then he opened the band chat; 469 Then he sent it to the other
two chats; 485 Elijah read that one twice, and "Then there was a paralegal ... Then a guy"; 487 watched it four times
looking for the lie; 587 forty-eight dollars. Then he went in; 661 Then he asked about the farm; 685 Then he thought
about Wes; 995 Then he typed Working (logged); 1140 Then David looked back down; 1142 Then he started the truck; 1262
Then he watched it; 1265 Then he thought about the comments; 1283 Then he played the voicemail; 1313 He read it twice
with the door open; 1314 Then he put the phone face down (logged); 1329 Then he looked at Elijah for a while; 1406 Then
he went into the coat one more time; 1436 Three, four, five times he read it (logged); 1453 He read the last three
words again (logged); 1472 Then he snorted (edit 188, CT's pick); 1498 Then she picked up a push broom; 1633 Then she
set it down on the tailgate; 1640 Then she went back to her bench (logged); 1725 Then he put the phone on Do Not
Disturb (logged); 1739 She read the order twice (logged); 1755 Then he remembered his training (logged); 1808 Then
Grace came back alone (logged).

Chapters 20 to 36 (37, fixed as part of the rewrite): 1974, 1976, 2009, 2017, 2047, 2139, 2177, 2196, 2237, 2262,
2289, 2326, 2393, 2442, 2443, 2505, 2509, 2516, 2527, 2531, 2542, 2551, 2553, 2592, 2701, 2720, 2740, 2796, 2839, 2846,
3000, 3028, 3056, 3097, 3157, 3187, 3216. Also repeated there: "a split of oak" (2139, 2261, 2701) and "Neither of them
said anything for a while" (2177, 2262, 3187).

Chapter 37 to the Epilogue (16; CT loves the ending, so lightest touch): 3334 Then he carried it back; 3408 Then he
turned back a page; 3437 Then he laid one more place; 3445 Then everyone had one in their hand; 3476 Grace had read
hers twice; 3543 and 3667 "Then Grace did" / "Then one of them did" (a pair; Claude: keep); 3544 Then she pulled the
blanket off; 3550 and 3671 "Then she reached out" (a pair; Claude: keep); 3577 Then he slid the four ones back; 3623
He read it again, slower (Claude: keep); 3632 Then he typed, Can't this time; 3647 Then he thought of Manny's well
(also line flag 57); 3668 Then a face filled the screen; 3678 Then he took the book out of his jacket; 3693 Then he
played something else (Claude: keep).

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
  "StS Publication Files" as surviving-the-singularity-v6-large-print-6x9.pdf; the copy from before the fixes is
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
