# v5 edits waiting for CT's go

Running list, started 2026-11-25. These are CT's edits to the v5 manuscript (Google Doc "StS v5 draft (Nov 23)").
**Nothing on this list has been applied to the Doc yet.** CT will say when to make the changes and rebuild the
publication files (`publication/novel/build/build.sh`).

Wording in quotes is CT's unless marked "mine". Items marked OPEN need a decision from CT. Items marked CALLED were settled by Claude under CT's 2026-11-25 instruction
("I'm trusting you to keep track of where stuff goes and the details of how to keep the composition rolling"); see
"Claude's calls" below. CT can overrule any of them.
When an edit is made, move it to "Applied" with the date. To change the Doc, use the bridge:
`node scripts/sts-bridge.mjs edit READ.json --find "old words" --replace "new words"`.

## Waiting

### Author's Note
1. Delete the line "You can doubt my forecast."
2. Keep "You can rise to meet it." as the close, then add a new line after it: "Let's begin to imagine how."

### Chapter 0: Three Glasses Up
3. After "The band was called Crop Dust." add "Har har." and end the paragraph there. The next paragraph starts at
   "Nate played bass and Wes played drums..."
4. Clarify whose grandmother it is in "David had called him Mad since they were eight. His grandmother used to walk
   him..." Proposed (mine): "Elijah's grandmother".
5. OPEN. Change the word "bridge" in "He thought of himself as a bridge." and "Until he saw what was on the other
   side of that bridge." Word not yet decided.
6. Before "PorusAI built the bomb." add (Option A): "If Google was Einstein, PorusAI was Oppenheimer."
7. Replace "David gave him the look too, and then gave him a beer." with "But at least David's looks came with a
   side of beer."
13. Say that Elijah's Claypot office is a satellite office. Proposed (mine), placed before "But Claypot moved like a
    big company moves...": "Elijah worked out of a satellite office, a long way from where anything got decided."
    The manuscript never says where Claypot's main office is, so no location was added.

### Chapter 1: A Bet for Lamb
8. Add a line about Devendra's coffee where he is first introduced (the paragraph ending "He found him at the good
   coffee machine on the fourth floor."): "Devendra liked his coffee the same way every day and got very annoyed if
   it wasn't right." Placement is mine.
9. At the coffee machine, replace his quote with: "You'll calibrate. Everyone's first month here feels like the
   apocalypse." He picked up his cup. "I got a mortgage and three kids. I gave up identity crises a long time ago."
   ("Three" spelled out to match the manuscript; "in grade school" dropped.)
10. Replace "Three jobs in one bar is an anecdote," Devendra said. "You build models for a living. What's your n?"
    with: "...You build models for a living. Relax." Then replace "Elijah didn't have one." with (mine): "Elijah
    didn't relax. He still looked stressed." Then: "Fine." Devendra was enjoying himself now. "You want to play
    Forecaster? Be my guest. Give me a date."
11. Devendra's reply to "Five years. Thanksgiving, 2027. A machine that can do any job in this building." becomes:
    "Five years," Devendra said. "That's one of the more aggressive ones I've heard yet. Okay, fine. And if it's just
    another Tuesday?" ("Devendra said" and "Okay" are mine.) CALLED: Thanksgiving 2027 is a Thursday (the Appendix
    says so). Keep "Tuesday" or go back to "Thursday"?
12. "Loser cooks" becomes "Loser cooks dinner." CALLED: it appears five times (Ch 1 Elijah's reply; Ch 1 sticky note;
    Ch 2 note in the corner; Ch 6 "I bet a guy dinner on it. Loser cooks."; Appendix). Add "dinner" in all five or
    only in Chapter 1? Chapter 6 would repeat the word "dinner".
14. The exchange at the bar. Replace Elijah's "Sure. They'll land somewhere..." with:
    "You sleeping?" / "Sure. A little. I can't stop thinking about the people the realtors fired." /
    "They'll land somewhere," David said. "There's always a job." / "I'm not so sure about that." David's next line,
    "What's a job for?", follows as it is. CALLED: Elijah's old speech ("People land where they put themselves. Retrain,
    learn the new thing. Nobody owes you a job.") is gone in this version. Keep any of it?
15. "Devendra wanted an n. He'd get one. He'd try to break a model himself." becomes: "Devendra wanted a prediction.
    He'd give it one. And he'd do it by cracking one of these things open himself." CALLED: Elijah already gave a date
    at the coffee machine, so "He'd give it one" can read as repeating himself.
16. "The limit he found was heat." becomes: "He had found his first limit. The limit he found was heat, specifically
    overheating."
17. The first two sentences of the next paragraph, "The machine that had dissolved three careers at the Bear Flag
    needed watts. It needed cooling.", become: "The machine that had ended three careers at the Bear Flag needed
    watts, of course, but it also needed cooling."
18. Near the end of Chapter 1: "One tower in one apartment was an n of one." becomes "One tower in one apartment
    wasn't much of a prediction engine." (The sentence before it, "He didn't tell Devendra any of this.", stays.)

19. End of Chapter 1: "He left the tower off for a week. Then he opened the notebook where he'd written MADRONE IS NOT A
    DRONE, turned to a clean page, wrote the date at the top, and started keeping track." becomes: "...Then he opened
    the notebook where he'd written MADRONE IS NOT A DRONE, turned to a clean page, and started writing." Only "wrote
    the date at the top" is cut, and "started keeping track" becomes "started writing".
    Also "where he'd written MADRONE IS NOT A DRONE" changes "written" to "scrawled" (CT chose it). Full sentence:
    "Then he opened the notebook where he'd scrawled MADRONE IS NOT A DRONE, turned to a clean page, and started
    writing."
20. Chapter 1, when the tower shuts off. Elijah says "Shit." Placement (mine): after "The fans coasted to silence.",
    so the paragraph ends: Black screen. The fans coasted to silence. "Shit." The room ticked as it cooled.

### Chapter 2: The Coin Slot
21. At the all-hands, "He was done being surprised. He would write things down before they happened." becomes:
    "He was done being blindsided. He would try to pay closer attention."
    CALLED: later in Chapter 2 the promise is called back: "That night Elijah sat at the kitchen table with the
    notebook and did what he'd promised. He wrote it down before it happened." That no longer matches the promise.
    Change it too?
22. After Elijah texts Wes "Let me look into it, he sent." the next line, "He never did.", becomes: "He meant to do it,
    but he never got the chance." (The later callbacks in Chapters 6 and 13 quote only the texts, so they still fit.)
23. Lena. He does not follow her to her car; he goes over to her in the room as everyone is leaving. Replace the
    paragraphs from "Afterward he went looking for the woman from illustration tools." through "She got in and
    slammed the door. He stood there while she backed out." with this draft (CT's beats and lines; the connecting
    narration is mine):

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

    The next paragraph, "He went back up and found Devendra at the good coffee machine, watching the drip like it
    owed him money.", becomes: "Feeling weird, he went looking for a familiar face, a friendlier one, and found
    Devendra at the good coffee machine, watching the drip like it owed him money."
24. The Devendra exchange that follows. Devendra notices Elijah is rattled, asks like a concerned supervisor, and
    shows his thick skin. After "The sticky note was still on the side of it.", replace the exchange from "Good
    quarter," Devendra said... through "He rinsed his cup and went back to his desk." with (CT's lines and beats;
    the tags and the sentence about the room thinning are mine):

    > Devendra looked at him. "You doing okay? You look a little rattled."
    >
    > "Well, I just had a weird exchange with that woman who spoke."
    >
    > "Don't mind people like that," Devendra said. "People like that have always existed. Luddites. They'll come
    > around. They always do. And if they don't, then, well, maybe she should start looking for another job."
    >
    > "Yeah, but don't we have a responsibility to caretake the rollout? Mitigate some of these effects?"
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

    CALLED: this cuts the enclosure lines (the commons, the hedges, "That's the hedge. I helped plant it.") and "And you
    took the bonus." entirely. Keep any of them?

25. Wes sends a second text: a link to a hit piece about how much water the new product (Companion) uses, with
    "is this true". Elijah never answers it. Drafts below; wording outside CT's "is this true" is mine.

    Chapter 2, after "Let me look into it, he sent." (CALLED: here, or later in the timeline?):

    > A minute later Wes sent a link. It was a hit piece on how much water Companion was going to drink.
    >
    > is this true
    >
    > Elijah didn't answer.

    CALLED: edit 22 ("He meant to do it, but he never got the chance.") follows here now. Keep it, or let "Elijah
    didn't answer." be the end?

    Chapter 6, where he opens the band chat. "Above the box, still, was Wes. is my stuff in that thing. Under it, his
    own. Let me look into it. Nobody had written in there since." becomes: "Above the box, still, was Wes. is my
    stuff in that thing. Under it, his own. Let me look into it. Under that, Wes again: the link about the water, and
    is this true. He had never answered. Nobody had written in there since."

    CALLED: Chapter 13 has the same callback ("scrolled up, past his own link, to Wes. is my stuff in that thing.
    Under it, Let me look into it."). Change it to end on the unanswered question too?

### Meanwhile (the first one, after Chapter 2: the Bidwell scene)
26. "Corpus. The body of work. Everything anyone ever made with the software." becomes: "Corpus. The body of work.
    Everything anyone ever made with their software and stored on their servers."
27. "Find out what the dirt costs," he said. becomes: "Find out what their dirt costs," he said.

### Chapter 3: A Satellite Over the Star Thistle
28. The Architect's lecture video. After "I am often asked if I am afraid of it," she said. "I am not. I am afraid of
    us." add CT's lines, so it reads:

    > "I am often asked if I am afraid of it," she said. "I am not. I am afraid of us. I am afraid of what mankind
    > might do with such a thing."
    >
    > The pit in Elijah's stomach grew deeper.
    >
    > "We do not exactly have a glowing track record with new technology."

    Then "Elijah wrote it all down. Then he watched it again." as before. CALLED: "We do not" instead of "We don't",
    because she never uses contractions. The pit echoes the end of the Devendra scene (edit 24). Chapter 9's
    callback ("I said once, in a lecture, that I was afraid of us. I was being polite.") still fits.
29. The first Sunday call. "The phone rang at 9:40 on Sunday, because it always rang at 9:40 on Sunday." becomes:
    "The phone rang at 9:40 on Sunday because it always rang around 9:40 every Sunday. That was church time."
    CT decided: the Sunday call is in the MORNING, and the other chapters change to match (edit 30).
30. The Sunday 9:40 call moves to the morning everywhere (CT: "morning, change the other chapters to match"). Every
    change below is CALLED by Claude to make that true; CT's only fixed point is 9:40 Sunday morning, church time.
    - Ch 3: "She called when her day ended, whether she had seen him that week or not." becomes "She called on her
      way out the door, whether she had seen him that week or not." (The radio, the running water and the pot she
      never let anyone else wash still fit: breakfast dishes before church.)
    - Ch 13: see edit 31 (this one call stays at night, on purpose).
    - Ch 15, the habit while he lives in the truck: "At 9:40 that night, back under the sycamore, the phone did not
      ring." becomes "That Sunday at 9:40, before he drove down, the phone did not ring. He sat under the sycamore
      and watched it not ring." The rest stays ("Then he played the voicemail. After that he did it every week.").
    - Ch 15, arranging the calls before he goes north: "Sundays," he said. "Nine-forty at night. I'm going to call.
      Could you just hold it by her ear?" becomes "Nine-forty in the morning. I'm going to call. Could somebody
      just hold it by her ear?" (The night aide is still the one he asks; she reappears in Ch 37, so she stays.)
    - Ch 17: "The night aide held the phone by his mother's ear." becomes "The aide held the phone by his mother's
      ear."
    - Ch 18: "At 9:40 that night he called the place with the rose garden" becomes "At 9:40 he called the place with
      the rose garden" (Marta came by at eight that morning and soup is at noon, so 9:40 sits between them). "The
      night aide held the phone" becomes "The aide held the phone", and "that was all for tonight, honey" becomes
      "that was all for today, honey".
    - Ch 22: "The night before, at 9:40, he called the rose garden." becomes "The day before, at 9:40, he called the
      rose garden." "She's been looking at that door all day" becomes "all morning", and "Her Sunday company didn't
      come." becomes "Her Sunday company didn't come last week." (David signs in at 10:15 on Sundays, after the
      call, so it has to be last week's visit Ray never made.)
    - Ch 24, the first fire in the stove room: "It was a Sunday. At 9:40 he stepped out under the eave and called the
      rose garden." becomes "It was a Saturday. The next morning at 9:40 he stepped out under the eave and called the
      rose garden." (The gathering runs past eleven at night.) "He wrote it in the notebook before he went back in."
      stays.
    - Ch 31: "At 9:40 that night he called the rose garden." becomes "On Sunday at 9:40 he called the rose garden."
      and the paragraph after the call, "In the morning it was the first of the month, the day for the pit.",
      becomes "The next morning was the first of the month, the day for the pit."
    - No change needed: Ch 7 (she's doing dishes; fine in the morning), Ch 13 voicemail "Sunday, 9:41", Ch 24's
      "The next Sunday at 9:40", Ch 25 ("Elijah called him on Sundays, after his mother"), Ch 37 (the night aide
      and the lamp that "talks to her at night").
31. One call comes at night, as the first sign something is off with his mother (CT's idea: she thinks it's morning,
    but it's evening). CALLED by Claude: the call in Chapter 13, the Sunday before her stroke, the one he doesn't
    answer. Her voicemail is the last whole sentences she ever says to him, so the wrong hour lands there.
    - Ch 13: "On Sunday at 9:40 the phone rang on the dash. He watched it until it stopped." becomes "On Sunday the
      phone rang on the dash at 9:40 at night. She always called in the morning. He watched it until it stopped."
      His text stays "Working late. All good. Love you", which fits at night.
    - Ch 13: "There was one voicemail, from Sunday, 9:41." becomes "There was one voicemail, from Sunday, 9:41 p.m."
    - Ch 14, the voicemail: "Hi, baby. I watched your video." becomes "Morning, baby. I watched your video." The rest
      of the voicemail stays as it is.
    - Ch 15 ("That Sunday at 9:40, before he drove down, the phone did not ring.") stays morning: after the stroke
      he waits at her usual time.
32. Ch 3, in the notebook: "It won't take the machines away first. It takes the people who see it coming, out of the
    world everyone they love still lives in." becomes "...out of the world everyone they love still believes in."
    Only "lives in" changes to "believes in".

### Chapter 4: Cell G14
33. End of the Kardashev paragraph: "He typed it in scientific notation, 3.8 times ten to the twenty-sixth watts, and
    sat back, and felt nothing." becomes "He typed it in scientific notation, 3.8 times ten to the twenty-sixth watts,
    and sat back. He felt nearly nothing." CALLED: CT said "He typed the numbers into the Kardashev scale and sat
    back. ... He felt nearly nothing." The number stays in the sentence because the next paragraph refers back to
    it ("ten-to-the-twenty-sixth watts sat in its cell"), and he types it into the spreadsheet cell, not into the
    scale.
34. Last line of Chapter 4: "The electric bill was in the mailbox that Monday." becomes "The new electric bill would
    show up next Monday, and Elijah was dreading it." Chapter 5's opening still fits: "The envelope was thin, which
    fooled him." now reads as false relief after the dread.

## Claude's calls (2026-11-25)

CT: "We should definitely keep whatever's relevant to the story and useful for dialogue purposes ... I'm trusting you
to keep track of where stuff goes and the details of how to keep the composition rolling." Settled on that basis;
CT can overrule any of them.

- 11: "And if it's just another Thursday?" Keeps CT's "just another" and the real day: Thanksgiving 2027 is a
  Thursday, as the Appendix and later chapters say.
- 12: "Loser cooks dinner." in Ch 1 (Elijah's reply and the sticky note), Ch 2 (the note in the corner) and the
  Appendix. Ch 6 stays "Loser cooks." because "I bet a guy dinner on it" is right before it.
- 14: Elijah's old speech is cut. David's "What's a job for?" still lands after "I'm not so sure about that."
- 15: "Devendra wanted a prediction. He'd give him a better one. And he'd do it by cracking one of these things open
  himself." ("him" for "it", and "a better one" because Elijah already gave a date.)
- 21: The callback becomes "That night Elijah sat at the kitchen table with the notebook and did what he'd promised.
  He paid closer attention, and he wrote down what he saw coming." The list of stages still follows it.
- 24: The enclosure lines, "That's the hedge. I helped plant it." and "And you took the bonus." are cut from Ch 2.
  Nothing is lost: Reuben gives the enclosure history in Ch 23, and the bonus comes up in Ch 10 ("With the bonus.").
  "Good quarter" and the moat line are cut with them. Ch 9 still says Lena "stood up at our all-hands and asked what
  the artists get, and nobody answered her", which still fits.
- 25: The link arrives in Ch 2 right after "Let me look into it, he sent." Order: the link, "is this true",
  "Elijah didn't answer.", then edit 22 "He meant to do it, but he never got the chance."
- 25, Ch 13: the callback becomes "...scrolled up, past his own link, to Wes. is my stuff in that thing. Under it,
  Let me look into it. Under that, is this true, with nothing under it. He sat with them for a while." (replacing
  "He sat with the two of them for a while.")

Still CT's to decide: 5 (the word for "bridge").

## Applied

- Author's Note, 2026-11-25: "They may tell you they moved on because I was an asshole, and they might be right."
  and "But I'm not wrong about our trajectory." Entered in the Doc as suggestions; CT said he accepted them, but two
  reads afterwards still showed them pending. The publication files were built as if accepted. Confirm in the Doc.
