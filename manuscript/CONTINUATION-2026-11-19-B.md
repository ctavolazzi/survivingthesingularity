# Continuation: Surviving the Singularity, the novel. Written the evening of 2026-11-19.

Read this first. It replaces `CONTINUATION-2026-11-19.md`, which is kept as a record of the
morning and is out of date in several places.

Then read, in this order:

1. `NOVEL-SUBSTRATE-2026-11-19.md`. What CT wants next, and where each major character stands.
2. `NOVEL-METHOD-2026-11-19.md`. How Elijah's arc was strengthened, so the same thing can be
   done for the others.
3. `NOVEL-READERS-DIGEST-2026-11-19.md`. What ten readers found in the whole book: what was
   fixed, and what is still open.

## The job, in CT's words

19 November, evening:

> "I want to make this book really good."

> "I think Elijah's arc is really strong. A lot stronger than it was when we started working on
> this." "I'd like to do the same thing with some of the other major characters, like Grace and
> his mom."

> "I really want to make this something that is worth people's time. And one of the best ways
> to do that is to make the narrative and story arcs of the characters really strong. Make it
> satisfying, make it make sense. Avoid classic tropes. But have some tropes in there because
> you need some just for readability, relatability, marketability."

> "We're making the best quality thing we can with an original story that people haven't
> necessarily seen before, but we're making it relatable and human and tragic. We're putting
> our characters through moments of great loss so that they can rise. We're putting conflicting
> viewpoints up against each other so that they can hash it out."

> "One thing that I don't think we've really explored at all is the AGI concept. Because
> Elijah's whole shtick is that he sees where it's headed. And so do some of these other
> people. But then he continuously gets rejected by people. They continuously project onto him.
> Disrespect his boundaries. Fail to consider his boundaries. Treat him like a means to an end,
> like a tool." "And how many stories do we have like this about creators? None. This is
> potentially one of the quintessential stories of our moment in history. And I feel like we
> are risking being flippant about it."

> "I want to be real intentional about the characters, the way they interact with each other,
> their motivations, their hopes, their goals, their dreams, their personalities, their
> traumas, their complexities, their backstory, all of that. I think we need to build more
> substrate from which to, in essence, congeal the story together."

> "I just want to take it one step further before we consider publishing it."

His schedule in the Doc says new writing done 22 November, read-through 23 and 24, build 25,
publish Thursday 26 November 2026. "Before we consider publishing it" may mean the date can
move. He has not said so. Do not assume either way.

## How CT wants to be worked with

His own instruction files load by themselves. These are the ones this work kept hitting, and
most of them were learned the hard way on 19 November.

- **Do the thinking, then show him the result.** His words: "you just keep fishing for what you
  think I want instead of giving me what I'm telling you I want." He wants a collaborator who
  runs the options past himself, criticises them, and presents the best version. "Like a
  creator does. And then I'll come through and paint the rest of it with my style and change
  things that I don't like."
- **He is the painter. We build the canvas.** He edits for style, voice and what pleases him.
  He does not want to hunt for contradictions. "I want you to find stuff like that and fix it."
- **Answer first, in a line or two. Then stop.**
- **Be cohesive.** When a reply was a list of changes he said "It's just a jumbled mess of
  random stuff." What worked was telling him the story, act by act, in plain sentences, with
  the changes inside it. Tell the story. Do not hand him an inventory.
- **He finds weak joints by asking plain questions.** "What's the video that he posts?" "If he
  sells the farm, why didn't he keep some money for himself?" Answer the question, say honestly
  where the answer is weak, and give one recommendation. His next message is usually the fix.
- **When he dictates a scene, use his words.** Melody's phone call in chapter 14 is his
  dictation nearly word for word. Grace's speech at the fire in chapter 36 is his dictation.
  Do not rewrite either.
- **When he floats two options, say which you would take and why.** Do not ask him to choose
  with no view of your own. When he asks "do you?", it is a question: answer it, and do not
  act until he says.
- **A short message is not always a go.** But asking him to repeat something he already said is
  worse. Read his prompt and the notes before asking anything.
- **No em dashes or en dashes anywhere.**
- **He reads on his phone.** Long work goes on the reading page. Point to the tab.
- **Writing to the Google Doc needs his say-so in so many words.** On 19 November he said
  "write it to the Doc," and the pass went in. A new chat should not take that as standing
  permission. If his prompt does not say it, the first write will be refused, and he will have
  to say it again.
- **Privacy.** The repository is public. The manuscript text is not in it. His personal journal
  material stays out of every file. His social media export and the Drive doc "Trauma and
  Boundary Reflection" are left alone. Drive is read-only apart from the manuscript Doc.
- **He asked for subagents on Sonnet 5.5** to fetch information for the main session to judge.
  That is how the ten readers were run. See the method file.

## Where everything is

**Branch.** `claude/sts-continuation-work-na8qhw`, pushed, not merged. Merging to `main`
deploys the live site. No pull request. He does not want one opened or watched.

**The manuscript** is his Google Doc, "FINAL StS Manuscript." His prompt has its id. As of the
evening of 19 November the Doc holds the whole revised book: every change described in these
notes is in it and was checked against it paragraph by paragraph, words and italics. The Doc
as it stood before the pass is in its version history.

The top of the Doc (TO DO, Story plan, Character pages) was written before the current draft
and has not been touched. Its chapter numbers are an older scheme: its "Chapter 6" is the
book's chapter 16. Its Character pages have Want, Flaw and Arc filled in for Elijah, Marta,
Tyler and Patricia and blank for nearly everyone else. Those blanks are the next job.

The only thing changed up there is the subtitle under the title, which is now "A Solarpunk
Novel" (his choice, 19 November). The Afterword is still titled "We Don't Have to Live Like
This."

**The reading page** is a private artifact titled "Singularity Cast Bible." His prompt has the
link. Tabs that matter now:

- **Book**: the whole manuscript as it is in the Doc, with a bar in the margin beside anything
  that is not his own untouched text (new, changed, or moved).
- **Changes**: the story decisions, what was turned down, and every change by chapter with what
  was there before and why.
- **Readers**: the ten readers' full reports.
- The older tabs (People, Map, Drive, Scene, Beats, Shape, Rhymes, Arcs, Fixes, Method) are the
  work of 18 and 19 November morning. They describe the book before the pass. The People and
  Arcs tabs are still useful raw material for the character work.

**A PDF** of the revised manuscript was made for him: the cover art as page one, then text
only, no picture placeholders. It is not in git. `tools/consistency-pass/make_pdf.py` and
`make_pdf.cjs` make it again.

**In this folder, the notes that are current:**

| File | What it is |
|---|---|
| `CONTINUATION-2026-11-19-B.md` | This file. |
| `NOVEL-SUBSTRATE-2026-11-19.md` | The next pass: the character work he asked for, with what is on the page and what is blank for each major character, and the AGI and creator theme. |
| `NOVEL-METHOD-2026-11-19.md` | What was done to Elijah's arc and how, the ten readers and how to run them again, and how to write to the Doc safely. |
| `NOVEL-READERS-DIGEST-2026-11-19.md` | What the ten readers found, sorted into fixed and open. |
| `tools/consistency-pass/ops.py` | Every change made to the book on 19 November, with the reason for each. Also the list of story decisions and the list of ideas turned down. This is the full record. |
| `drafts/draft-elijah-crash-out-arc.md` | The source of the new chapters 13 to 15, including Melody's call. |

**Older notes, kept as record.** They describe the book before the pass and some of their
proposals were taken, some turned down, some replaced: `NOVEL-BEATS`, `NOVEL-STRUCTURE`,
`NOVEL-CHARACTER-ARCS`, `NOVEL-CHARACTER-PROFILES`, `NOVEL-MAP-ELIJAH`, `NOVEL-MAP-EVERYONE`,
`NOVEL-CONSISTENCY-AUDIT`, `NOVEL-DRIVE-FINDINGS`, and `drafts/draft-later-chapters-36-37-39.md`.
`NOVEL-CHARACTER-PROFILES` is the best of them for voice: each person's own lines.

**Not in git, and gone when a session ends:** `drafts/_private/`. It held a plain-text copy of
the Doc, the working copy of the revised book, and the readers' raw reports. A new session has
to read the Doc again and rebuild them. The method file says how. The readers' reports survive
on the reading page.

## The story as it now runs

**Act One, The Bar (chapters 0 to 5).** Elijah Madrone, a self-taught data worker, shows a
chatbot to three realtors, and a week later they toast him for the three people they let go. He
spends a year measuring and writing down what is coming. Nobody can hear it: not Devendra at
work, not David behind the bar, not his mother, who is kind about it and starting to forget
things.

**Act Two, The City (6 to 15).** Laid off, he posts a four-minute video for four people and it
gets out. Powerful people pick him up, agree with him and use him. He tells Ruby no and hears
"Grub" from a long way back. He tells Gus no and does not know why. He works three weeks unpaid
and is sick in a parking lot when his mother's Sunday call comes, and he lets it ring. She has
a stroke. She has one word left, "Barry." He finds her barn full of supplies she bought to be
nice to him. He asks her what to do and she asks for Barry. He asks his followers for help and
they mock him. He sells the farm to pay for her room, to the same outfit that bought the place
next door. His half-sister Melody calls and screams that he kept the money. He blocks her,
breaks down in his truck under the madrones, yells at God, and gets rain. Five weeks in the
truck. A homeless man gives him twenty dollars. He drives north.

**Act Three, The Farm (16 to 31).** A co-op of nineteen households takes him in and asks him
nothing for three weeks. He sweeps, builds, leaks their data, rings the bell on himself,
helps save forty acres, and gets a roof. At his first fire he catches himself listing what he
would change if the place were his. Grace knocks on his door once and does not wait. He hides
one thing from the people who forgave him everything else: the farm he sold went to their
enemy. Reuben has known for two years and lays the deed on his table. He does not own up. He
brings the table a plan to make money and the table goes cold. He takes the tea, comes apart,
and tells Grace "You're just the lamp." He will not remember it. She will.

**Act Four, Home (32 to 39).** The machine wakes in secret on the land he sold. He sees it
before anyone and is believed for one minute, and the co-op still will not do what he wants.
At the bonfire he tells Grace she cannot choose for other people. He thinks he is being kind.
She answers with the lamp and with his mother. "Maybe you should go home." He goes back to a
rented back room at Manny's, beside the one fence on that road without a light on it. In his
mother's room the lamp calls him Barry and he does not correct it. On Thanksgiving the machine
asks the world's permission. At the Bear Flag, David tells him the three people were fine all
along, that David's father sat with his mother every Sunday until he died, and that Barry was
her first love. He says "Congratulations" and means it, and leaves the book on the bar.

## What is settled

**CT's rulings.** His exact words are in `ops.py`, in the scene draft, and in
`CONTINUATION-2026-11-19.md`.

- The stroke, the sale of the farm, "Barry," the barn she filled to humor him, the followers
  turning on him, the crash out, the five weeks in the truck, the guitar gone for good.
- Ray sat with his mother. David tells him who Barry was.
- At the fire Elijah strikes first without knowing it, and Grace says "And now you're taking
  out your mother trauma on me!"
- His sister is **Melody**. She is his father's daughter from before, lives in Miami, called
  him greedy, and her call sets off the crash out. He blocks her. CT turned down "Mallory" as
  too heavy-handed.
- He has a complex about money: "he doesn't want to be perceived as being motivated by money."
- The subtitle is "A Solarpunk Novel."
- The book is about this: "Surviving the singularity involves surviving yourself." It is about
  acceptance and being present, and letting go of the illusion of control.
- Grace's speech at the fire and Melody's phone call are his dictation.

**Mine, in the Doc, shown to him, and not yet ruled on.** Each is one or a few sentences and
can be taken out in a minute. The full list with reasons is `DECIDED` in `ops.py` and the top
of the Changes tab.

- The three weeks after he arrives (chapter 17).
- Grace knocking on his door (chapter 25).
- "You're the lamp" fired inside the fight (chapter 36).
- The midpoint turn at the first fire (chapter 24).
- The root for Grace's speech: "I can tell you their names" (chapter 27).
- His mother's lines moved to before the stroke, and Elijah saying them for her afterwards.
- Manny's back room, the pit that comes up dust, the pot he washes himself.
- The lamp calling him Barry. The visitors' book.
- The machine's letter that asks. Lou at Irene's table.
- The whole money thread after the call: the uncashed cheques, paying for the proofs with the
  first one he cashes, the number that stays blocked.
- **The deed** (chapters 23, 25, 29, 31). This is the largest. He was told to read chapter 29
  and say if it is wrong for Elijah. No answer yet.
- His father's name, Joe. Barry's surname, school and car. Pruitt. The aide.

**Turned down, with reasons.** `REJECTED` in `ops.py`. The main ones: Grace asking out loud for
the arms (her not asking is the character), Grace making the call herself, and a clock on his
mother's money.

## What is open

1. **The character work he has now asked for.** See the substrate file. This is the job.
2. **The AGI idea and the creator's story.** His words above. See the substrate file.
3. **Four things the book sets up and never returns to**, which are his to decide: the letter
   Elijah signs half read in San Francisco; the three crawlers that copied the leaked journal;
   who welds after Marta's shoulder goes; why he says no to Gus.
4. **The picture lines.** He said "No interior images please just text" about the PDF. The 19
   bracketed picture lines and their captions are still in the Doc. He has not said to remove
   them there.
5. **The top of the Doc** still describes the earlier book.
6. **The site.** Nothing on the live site has been touched. The build on 25 November and the
   publication pipeline in `publication/` have not been looked at in this work.

## Prompt to start the next chat

He writes his own. This is here so nothing gets left out of it.

- Fetch the branch `claude/sts-continuation-work-na8qhw` in `ctavolazzi/survivingthesingularity`
  and bring it onto the new branch. Do not merge to main. No pull request.
- Read `manuscript/CONTINUATION-2026-11-19-B.md` first, then the three files it names.
- The manuscript is the Google Doc "FINAL StS Manuscript" (give the id). Say plainly whether
  the new chat may write to it.
- The reading page (give the link). To update it: read it with the Artifact tool, rebuild with
  `manuscript/tools/reading-page`, publish to the same link.
- Say what to work on first. If he does not, the next job is Grace: see the substrate file.
