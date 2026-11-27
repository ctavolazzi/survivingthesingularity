# Edit 237: Miles Renner on the big screen (Chapter 26)

27 November 2026, the smell chat (twelfth). CT dictated the scene in two messages, saw the draft with his words in
bold and Claude's choices listed, and said "yes". His words in full, the draft with the bold marks, and the choices are
in `manuscript/novel/next-version-scenes-2026-11-26.md`, section 4. Logged only; not in the v8 Doc.

## Where

Chapter 26, a new scene. Book now:

> "See, I don't know what's coming in general," Lou said, and picked his coffee back up. "I just know this bed. Get
> your knee out of it, Ivy League."
>
> (scene break)
>
> On June 12 the big models went dark.

Change to: the same, with this scene between them and a scene break on each side.

> Curtis had the big screen on in the packing shed before dinner that Friday, while the plywood was still going down. A man in a gray sweater sat in a chair on a stage with one ankle on his knee. He was telling a room how it felt to be fired by his own board on a Friday and hired back by Tuesday.
>
> "That's Miles Renner," Curtis said, to nobody. "PorusAI. They threw him out and took him back inside of a week."
>
> Priya had stopped with a stack of plates against her hip.
>
> "Do you believe this guy?" Grace said.
>
> "Well, I mean, he is the CEO of one of the most powerful companies in the world," Curtis said.
>
> "Curtis, you can't be serious," Priya said.
>
> "I mean, I don't trust everything he says, but he does have privileged information and access to the models they don't release to the public."
>
> Grace rolled her eyes.
>
> Priya set the plates down. "Anyone who hoards that much wealth and doesn't use it to immediately try and solve problems like homelessness is just leveraging suffering for their own gain. It's sick. It's disgusting."
>
> "I don't know," Tyler said, from the bench. "I feel like they earned that wealth by being smart."
>
> "Nobody earns a billion dollars," Priya snapped. "They steal it."
>
> Wren stood up. "Does anyone want to go look at mushrooms with me outside?" she said. "The rain brought them up along the ditch."
>
> Tyler was on his feet before she finished. Lou went too.
>
> "Man, you sure know how to clear out a room, Priya," Denny said.
>
> "My morals make people want to commune with nature," Priya said. "I call that a win."
>
> She and Curtis were still at it when Grace caught Elijah's eye and nodded at the door.
>
> Outside, the gravel was still dark from the rain. They got as far as the wash station.
>
> "My dad used to argue with the TV like that," Grace said.
>
> She stopped there. She was looking at the beds, and for a little while she wasn't in the yard at all.
>
> "Hey," Elijah said. "We don't have to talk about anything you don't want to talk about."
>
> "No, it's fine." She shook her head. "But man, I remember him giving speeches like that CEO guy on the TV. He had so much charisma."
>
> "You think that guy has charisma?"
>
> Grace looked at him. "You don't?"
>
> "That guy seems like a sleazeball to me."
>
> "Oh, like you know what billionaires are really like."
>
> Elijah didn't say anything. He made a face.
>
> Grace stopped walking. "Elijah, do you personally know a billionaire?"
>
> Up at the shed the dinner bell went, and Marta's voice after it.
>
> "Sorry, Grace, gotta go," he said, grinning at her.
>
> "Elijah! Do you know a billionaire?"
>
> But Elijah had already skipped off up the gravel. He wasn't about to miss dinner.

## Whose words

All the dialogue is CT's except: Curtis's "That's Miles Renner ... inside of a week" and Wren's "The rain brought them
up along the ditch." The narration is Claude's except "But Elijah ... skipped off ... He wasn't about to miss dinner."

## Claude's choices and invented facts (his to change)

See section 4 of `next-version-scenes-2026-11-26.md`: May 2026; who says the open lines; "harder stuff" and Curtis's
indignation left out; the CEO's name; the sweater, the stage, Friday to Tuesday, the plates, the ditch, the wash
station, the dinner bell.

## What it touches

- The book has 138 scenes now. `story_checks.py` (the calendar) and `knowledge.py` (A6: Grace asks, he never answers)
  were updated. The scene sheet and its CSV still have 137 rows.
- Chapter 34: Priya has said nobody earns a billion dollars seventeen months before "I know a guy."
- "Pondwater": "harder stuff" is still said there for the first time.

## Checks

`make_v6.py`: all 237 check rows pass (612 replacements). `verify.py` on the v8 read: 223 accepted, 224 to 237 not in
the Doc, nothing PARTIAL. No dashes. 482 words in, none out; 104,129 words in the chapters.
