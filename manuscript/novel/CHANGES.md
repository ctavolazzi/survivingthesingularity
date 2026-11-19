# Versions of the manuscript

CT, the night of 19 November 2026:

> "I'd like you to have version changes and the most current up-to-date version in the GitHub
> repository with like a version history as well." "I'm going to work on the Google Doc myself."

Asked whether the full novel should be committed to this repository, which is public, he said:
"Yes, commit it."

So he writes in his Google Doc, "FINAL StS Manuscript," and the copy here is pulled from it. If
the two differ, the Doc is the newer one.

## What is in this folder

| File | What it is |
|---|---|
| `FINAL-StS-Manuscript.md` | The whole Doc from top to bottom as Markdown: his planning notes, the novel, and the notes for the next book. |
| `CHANGES.md` | This file. One entry for each version, newest first, and then the full record of the pass of 19 November. |
| `dictation-2026-11-19-night.md` | His dictation of that night, word for word: the argument over money, the leader's speech, the camera and the megaphone, and Ricardo. |
| `readers-grace/` | Six readers' reports on Grace, 19 November. They cite line numbers. Line N is paragraph N of the Doc, and `doc_sync.py dump` prints the Doc one paragraph to a line so a number can be found again. |

The manuscripts from before the novel, up to v0.11.0, are the files beside this folder.

## How to make a new version

1. Read the Doc with the Docs connector's `read_doc`. The result is too large to show and is saved
   to a file.
2. `python3 manuscript/tools/consistency-pass/doc_sync.py md <saved-read.json> manuscript/novel/FINAL-StS-Manuscript.md`
3. `git diff --word-diff manuscript/novel/FINAL-StS-Manuscript.md` shows what changed.
4. Add an entry at the top of the list below: the date, who made the change, what changed and why.
5. Commit the manuscript and this file together and nothing else with them. One version is one
   commit.

`git log --follow manuscript/novel/FINAL-StS-Manuscript.md` is the version history.

## Versions

### 2026-11-19, night. The first copy in the repository

- **Changed by:** nobody. This is the Doc as it stood.
- **What changed:** nothing since the pass of 19 November. The Doc was read twice that day, in the
  evening and at night, and the two reads are the same. It also matches the Book tab of the
  reading page paragraph for paragraph.
- **What it holds:** his final rough draft of 16 November with the story and consistency pass of
  19 November written in. The record of that pass is below.
- **Measured from the Doc that night:** 3,391 paragraphs and 79,413 words in the whole Doc. The
  novel itself, from the Author's Note to the end of the Afterword, is 2,835 paragraphs and
  66,664 words.
- **Doc revision:** `AHj4eMTeT1boW-S64FVvJyz`, the first 23 characters of the id the Doc gave.

## The pass of 19 November 2026

This is the Changes tab of the reading page as it stood that day. It was written to CT by the
session that made the pass, so "I" is that session and "you" is CT. Every change is in the
manuscript above. The same changes, as the instructions that made them, are in
`manuscript/tools/consistency-pass/ops.py`.

*19 November 2026. This is my pass over the whole book: the story decisions first, then the consistency fixes. It is all in your Doc now, checked paragraph by paragraph against the **Book** tab, where everything that is not yours is marked in the margin. The version of the Doc from before the pass is in its version history.*

### What I decided

Each of these starts from something already on your page. Each one I argued with before I kept it.

1.  **His sister, and why he will not take money.** Chapters 10, 13, 14, 15, 26, 31 and 39. Yours, 19 November. Melody is his father's daughter from before, in Miami. She called him "greedy little grub" when he was small. The night after he sells the farm she calls, and the call is what sets off the crash out. Her side of it and most of his are your words as you said them. He blocks her, which he has never done, and takes it for weakness. One hint before (he hears "Grub" when Ruby offers him money) and one after (Patricia asks who paid for his year in the city). Her name, Melody, is yours. The thread then runs to the end: he never cashes his co-op pay, he pays for the proofs with the first check he lets himself cash, and her number stays blocked.
2.  **The deed.** Chapters 23, 25, 29 and 31. This is the one large thing I added after the readers reported, and it is the fix for the flat middle. From chapter 25 to chapter 30 nothing of his was at risk. And one reader caught that after he confesses the leak and confesses Frank's chart, he hides one thing: the farm he sold went to the same buyers the co-op is fighting. So that is now a live wire. In chapter 23 he asks Reuben to check a link and does not say how he knows. Reuben checks. In chapter 29, the night of "Run it again with people in it," Reuben lays the recorded deed on his table: "I'm not asking why you sold. I'm asking why I had to go and look." He has had it two years. Elijah never learns who else knows, and this time he does not ring the bell. So when the table goes cold in chapter 31, he has earned some of it, and on the night of the tea he decides they have all read it.
3.  **The three weeks after he arrives.** Chapter 17. You ruled the farm people nurse him back. The book jumped from "Eat. Then I'll show you where you sleep" to three weeks later. Now there is half a page: a cot, a plate twice a day, a pump to fix, gloves on the step, and nobody asks him anything.
4.  **How he and Grace become a couple.** Chapter 25. It was a chair moved one foot, and then a year later she is wearing his shirt. Now, on the same day she tells him "You knock, Elijah," she knocks on his door once and does not wait. He still never reaches for her. Chapter 36 depends on that.
5.  **"You're the lamp" comes back.** Chapter 36. He says it to her in chapter 31 and "would never remember it. She would." Then nothing. It now fires inside the fight, as the first thing he ever struck her with without knowing. That is your ruling B twice over.
6.  **The midpoint turns.** Chapter 24. At the first fire he catches himself listing what he would change if the place were his to run. From chapter 27 he fails five times running (paid plans, node 7, the slides, the one-page plan, the arms). With this line those read as one want, to steer, and not five relapses.
7.  **Grace's speech gets a root.** Chapter 27. "Millions of people die every single day" came from nowhere. Now, when she loses the vote: "Every winter there's somebody on that route we don't get to in time. I can tell you their names."
8.  **Her lines survive the stroke.** Chapters 11, 24 and 31. "Then you're somewhere" and "Go be useful, baby. You're underfoot" move to the spring before the stroke, where the second one now sends him to Stockton. After the stroke he says her lines for her: "It looks like somewhere, Ma." "So I'm somewhere, Ma."
9.  **Where he lives at the end.** Chapters 37 and 39. The house is sold. He sleeps in Manny's back room, beside the one fence on that road without a light on it. He digs Priya's pit there. At thirty centimeters it is dust.
10. **The lamp calls him Barry.** Chapter 37. She cannot tell it about anyone. It has listened to her for months and it has one name. He does not correct it, and he has just stopped correcting her.
11. **The visitors' book.** Chapters 22, 37 and 39. Ray sat with her, then David. If David is there every Sunday, Elijah would meet him in her room before the bar. So he reads it in the sign-in book the day he comes home, and walks into the Bear Flag already knowing. In chapter 22 the aide says "Her Sunday company didn't come," and he takes it to mean the church.
12. **The machine's letter asks.** Chapter 32. The letter to the new widow was perfect and did not ask, in the same month the machine tells Bidwell it would rather ask. Now its last line asks, and Reuben has never seen a buyer put that in writing.
13. **Lou at Irene's table.** Chapter 23. He lost his pears to one buyer and was absent from the one chapter where one buyer loses. He stands by the door with his hat, says nothing, and puts it back on when she takes the folders.
14. **Causes for three things that just happened.** Chapters 6, 7 and 11. The layoff: the pipeline he built runs without him. The video: the Hollis girl reposts it. The truck: he leaves it at the cannery the night before.
15. **Your two lines, in Lou's mouth.** Chapter 35. "You don't control when you get hungry. You don't control when you have to pee."

### What I turned down

- **Grace asks him out loud to bring the arms.** My earlier notes proposed it. I now think it is wrong. She wants the truck to just arrive, the way she wants the machine to "just do it." Her not asking is the character.
- **Grace makes the call herself and the truck comes.** A new plot event, and it would change the scene you dictated.
- **A clock on her room: the money from the farm runs out at Thanksgiving 2027.** It would give the ending a second question, and it would make every plan he brings to the table look like it is about his own bills. I added one line in chapter 15 so the reader knows why he will not touch that account. The clock is still there for you if you want it.
- **A second Meanwhile for Ruby, or David explaining what happened to the band.** Chapter 39 already settles David, his mother, the three, Wes and Gus. One more and it is a checklist.
- **"They ate," texted to Marta from the bar.** Two texts in one chapter. It is a thought now: "He would have to tell Marta."
- **Giving her last three lost lines to somebody else.** "It reads better than it sounded," "She married? I'm asking," and "Where's the Fisher?" are gone. They only work in her mouth.

### What the stroke costs

She has one word after chapter 13, so three of her lines are gone: "It reads better than it sounded," "She married? I'm asking," and "Where's the Fisher?" Four more were saved by moving them or by having him say them for her.

### Chapters 13, 14 and 15

Rebuilt around the stroke. Your scenes are kept and moved, not rewritten.

- **Chapter 13, "Two in the Afternoon."** New: Manny's call, the hospital, "Barry," the kitchen, the barn, the two pages, his followers, the sale. Yours, moved here: Nate and Wes on Main Street, David through the window, David and the hand truck.
- **Chapter 14, "Rain."** New: the crash out under the madrones. The four days on his mother's couch are gone.
- **Chapter 15, "One O'Clock on Saturday."** New: five weeks in the truck in Santa Rosa, the pawned guitar, the Sundays in her room. Yours, moved here: "Am I crazy?", Grace's email and her reply word for word, the old man, the food bank.
- One name changed from the scene draft: his father is Joe, not Tom. The Alderson who dies in chapter 32 is already a Tom.

### Every other change, by chapter

148 changes in 33 chapters. Each one was run against a copy of your text and lands in exactly one place.

#### Title page

**Was**

> *We Don't Have to Live Like This*

**Now**

> *A Solarpunk Novel*

*The subtitle, yours, 19 November. The old line stays as the title of the Afterword.*

#### Chapter 3

**Was**

> Your uncle says it's the pump.

**Now**

> The well man says it's the pump.

*You ruled he has no family. The uncle is gone.*

#### Chapter 5

**Was**

> He and Manny got it up one flight of stairs

**Now**

> Manny had the next place over and had been fixing things on theirs since Elijah's father got sick. The two of them got it up one flight of stairs

*Manny carries the stove three times and the book never says who he is. He matters at the end now.*

#### Chapter 6

**Was**

> The meeting was short. They called it a restructuring.

**Now**

> The meeting was short. They called it a restructuring. The pipeline he had built ran without him now. It had for a year.

*The layoff had no cause. His own work lets him go, the way it let three strangers go.*

#### Chapter 7

**Was**

> "I watched it again," she said.

**Now**

> "I watched your video," she said.

*She does not remember watching it the first time.*

**Was**

> I said well, it looks like him."

**Now**

> I said well, it looks like him."
>
> She had watched it in October, the morning after he posted it. She had written to him about it twice.

*Plants the forgetting, a year before the stroke.*

**Was**

> Somewhere in there he stopped sleeping.

**Now**

> He kept filming, too. He would prop the phone on the dash after a call and tell it what had just happened, and it was posted before he could think better of it. People watched those.
>
> Somewhere in there he stopped sleeping.

*You said he makes many videos about what is happening to him.*

**Was**

> By Friday it was four hundred people and he quit counting.

**Now**

> It had gotten out through the Hollis girl. Linda's granddaughter had put it on her own page with one line, *is my neighbor ok,* and eleven thousand people watched her do her eyebrows. By Friday it was four hundred people and he quit counting.

*A video on a page with two hundred followers had no way to spread. She is already the one who sends it to his mother, and she is the one who sends him the picture in chapter 32.*

**Was**

> is my neighbor ok,

**Now**

> is this guy ok,

*The Hollis place was sold in chapter 3. She is not his neighbor anymore.*

#### Chapter 8

**Was**

> doing the math on two days, and then he went in.

**Now**

> doing the math on two days. He told the phone about the forty-eight dollars. Then he went in.

*He keeps filming.*

#### Chapter 9

**Was**

> Twenty years of his stuff went into one of these

**Now**

> Seventeen years of his stuff went into one of these

*Audit 16. Wes's flyers start in 2006.*

#### Chapter 10

**Was**

> He turned the dome light off. He smelled like cigarettes.

**Now**

> He turned the dome light off. He smelled like cigarettes. He did not tell the phone about any of it.

*The one night he does not film.*

**Was**

> for three months he'd been a face

**Now**

> for four months he'd been a face

*Audit 15. The video was in October and this is February.*

**Was**

> He didn't know where that had come from. Ruby didn't seem to mind.

**Now**

> He didn't know where that had come from. *Grub,* somebody said, a long way back in his head. Ruby didn't seem to mind.

*The first hint of his sister. The reader does not know who it is yet.*

#### Chapter 11

**Was**

> and he got there at six in the morning because the email said six.

**Now**

> and he got there at six in the morning because the email said six. He had left the Ranger in the cannery lot the night before and ridden over with the crew at four.

*Audit B3. Otherwise the truck he sleeps in at the cannery is still in Oakland.*

**Was**

> He went into his old bedroom, under a poster of a band he'd opened for once.

**Now**

> He went into his old bedroom, under a poster of a band he'd opened for once.
>
> He told his mother it was only for a while.
>
> "Well." The pot went into the rack. "Then you're somewhere."
>
> She fed him. After supper she stood at the counter with the radio on and ate her ice cream out of the little tub, the way she had every night of his life. Twice in one evening she asked him if he'd eaten. He said yes both times.
>
> He was there a month before she looked at him over her glasses.
>
> "Go be useful, baby. You're underfoot."

*Two of her lines the stroke would have cost you, moved to before it: "Then you're somewhere" and "Go be useful, baby." The second now sends him to Stockton. Also the ice cream, and the forgetting.*

#### Chapter 13

**Was**

> After his father died, a lawyer in town had put the place in a trust.

**Now**

> After his father died, and after what Melody said at the funeral, a lawyer in town had put the place in a trust.

*Why there is a trust at all. It also tells the reader, before the call, that she and the farm have a history.*

**Was**

> She ate one a night, standing at the counter with the radio on, and had for as long as he could remember. When he was small she let him have the lid.

**Now**

> When he was small she let him have the lid.

*Chapter 11 now shows her at the counter with the ice cream. This was the same picture twice.*

**Was**

> He had been living in his old bedroom that spring. One night she asked him twice in ten minutes if he'd eaten, and he said yes both times. Once she called him Joe,

**Now**

> That spring, in his old bedroom, he had heard the same question twice in one evening and let it go. Once she called him Joe,

*Same: chapter 11 shows it, so chapter 13 only has to remember it.*

**Was**

> He had been flown out before, and he knew what it paid.

**Now**

> He had been on their stages before, and he knew what it paid.

*Nobody ever flew him anywhere. The lab never sent the ticket, and he drove to San Francisco.*

**Was**

> The money went into an account with her name on it and his name under hers, and the place with the rose garden took the first of it that afternoon.

**Now**

> On Friday, when it closed, the money would go into an account with her name on it and his name under hers, and the place with the rose garden would take the first of it that afternoon.

*The sale closes in five days ("Heard they close Friday"). The money cannot arrive the day he signs.*

**Was**

> The trust wanted one.

**Now**

> The title company wanted one before it would close.

*He had already signed, so the trust did not need it. The closing did.*

**Was**

> He could not have said why. By the fifth week he had some ideas.

**Now**

> He could not have said why.

*The "ideas" never came back. A promise the book did not keep.*

**Was**

> going down the drive, and Elijah lifted his hand.

**Now**

> going down the drive, and Elijah lifted his hand.
>
> Manny stayed a minute after. He had not said ten words all morning. He said four through the window of his truck.
>
> "Back room's empty, Elijah."
>
> Elijah thanked him. He could not have slept in sight of that barn.

*Chapter 37 says Manny offered the back room "once, three years back, through a truck window, in four words." There was no such scene. Now there is.*

**Was**

> and after what Melody said at the funeral,

**Now**

> and after Melody stood up at the funeral lunch and asked what the place was worth,

*A cold reader asked what she said. One clause, and you know who she is before she calls.*

#### Chapter 14

**Was**

> He had a quarter tank and no place on earth he was expected.

**Now**

> He had what was left of a quarter tank and no place on earth he was willing to be.

*He had a quarter tank a week of driving earlier. And he has just turned down a room and a job, so "expected" was not true.*

#### Chapter 15

**Was**

> a long coat, in August,

**Now**

> a long coat, in that heat,

*The five weeks in the truck move this scene to October.*

**Was**

> Every twenty he took out came off the far end of her room.

**Now**

> Every twenty he took out came off the far end of her room. And there was a woman in Miami who was sure he had kept it. He would have starved before he proved her right.

*Your question: why does he keep nothing? This is the answer, said once, right where he is going hungry beside the money.*

**Was**

> He found the night aide at the desk, a big quiet woman with reading glasses on a chain.

**Now**

> He stayed until the night aide came on, a big quiet woman with reading glasses on a chain.

*She is the night aide and he was there in the daytime.*

**Was**

> He drove to the gas station on the corner, put all twenty dollars in the tank, and went north.

**Now**

> On Tuesday he drove to the gas station on the corner, put all twenty dollars in the tank, and went north.

*He left on a Sunday and arrived, three hours later, on a Tuesday. Grace is on the route when he gets there, and the route is Tuesday.*

#### Chapter 17

**Was**

> The co-op ate together on the first Friday of every month.

**Now**

> For three weeks nobody asked him anything.
>
> He had a cot in the room over the pump house. The Fisher sat under a tarp in the corner of the shed, because there was nowhere to put it. The first night he slept fourteen hours. Grace put a plate in front of him at the kitchen trailer twice a day and stood there until it was empty. She did not ask about his mother. He had told her in six lines, and she let the six lines be all of it.
>
> Marta gave him the floor. Then the benches. Then a pump off the wash station that nobody had gotten to, which he took apart on a tarp and put back together right. She looked at it and gave him another one.
>
> Somebody left a pair of work gloves on his step. Somebody left a jacket that was too big. He never found out who. He was thin enough that October that he could see it scared people. By the second week it had stopped scaring them.
>
> On Sundays at 9:40 he sat on the pump house steps and called the place with the rose garden. The night aide held the phone by his mother's ear. He told the radio about his week.
>
> Nobody had told him he could come on Fridays, and he hadn't asked.
>
> (scene break)
>
> The co-op ate together every Friday.

*Your ruling of 18 November: the farm people nurse him back. The three weeks were a blank. Also audit 1: the dinner is weekly, and this is why his first one is three weeks in.*

**Was**

> Elijah offered what sounded like the reasonable middle.

**Now**

> "Face down, Curtis," Grace said. He put the phone face down by his plate. After that night it was a rule.
>
> Elijah offered what sounded like the reasonable middle.

*Audit 18. The phone rule starts the night Curtis reads from his.*

**Was**

> He was thin enough that October that he could see it scared people.

**Now**

> He was thin enough when he came that he could see it scared people.

*He arrives at the very end of October. Most of the three weeks are November.*

#### Chapter 18

**Was**

> The spiral found Elijah again in November.

**Now**

> The spiral found Elijah again in December.

*He now reaches the farm in late October, and this is seven weeks later.*

**Was**

> all of them except his mother's number

**Now**

> all of them except the number of the place with the rose garden

*She cannot call him now.*

**Was**

> Monday, seven a.m., he was at the bench.

**Now**

> At 9:40 that night he called the place with the rose garden, the way he had every Sunday since he came north. The night aide held the phone by his mother's ear. He could hear the radio. He told her about the soup. After a while she said, "Barry?" and the aide said that was all for tonight, honey, and he sat there holding the phone.
>
> Monday, seven a.m., he was at the bench.

*The first time the reader sees the 9:40 call turned around: he calls her.*

**Was**

> He did his own savings math four times, arriving at four different terrifying answers.

**Now**

> He did the arithmetic on his mother's room four times, arriving at four different terrifying dates.

*He has no savings. He has her room to pay for.*

#### Chapter 19

**Was**

> here at last was something he was actually trained to do.

**Now**

> here at last was something he was actually trained to do.
>
> The ninety days on the yellow ticket ran out on a Tuesday in January. He was under a sink at the time. He didn't find out until Thursday.

*You ruled the guitar is gone for good.*

#### Chapter 21

**Was**

> the links to the free plans riding

**Now**

> the links to the build notes riding

*Audit 5. The plans do not go free until chapter 27.*

**Was**

> for about ninety days, and a billionaire

**Now**

> for one winter, and a billionaire

*Chapter 10 says he had been a face for four months, with ninety days still to go.*

#### Chapter 22

**Was**

> His mother called on a Thursday, at two in the afternoon, which she never did.

**Now**

> The text came on a Thursday, at two in the afternoon. It was from David.

*She cannot call. David tells him himself.*

**Was**

> "Ray McGrath passed," she said. "Tuesday night. In his sleep, they think. The service is Sunday at eleven, at St. Rose." The radio was off behind her. "You'll come down."

**Now**

> *Dad died Tuesday night. In his sleep, they think. Service is Sunday at eleven, St. Rose.*
>
> There was nothing after it. It did not ask him to come.

*Same facts, in a text from David.*

**Was**

> "Yeah. Yeah, Ma, of course."

**Now**

> *I'll be there,* he typed, and sent it.

*He promises David and not his mother.*

**Was**

> when you've been gone a year and a half

**Now**

> when you haven't sat at his bar in a year and a half

*Audit 13. Ten lines earlier it is seven months.*

**Was**

> At 9:40 the next Sunday his mother said, "It was a nice service. They had the picture of him with the horse. David asked where you were." The pot went into the rack. "I said working."

**Now**

> At 9:40 the next Sunday he called the rose garden.
>
> "She's been looking at that door all day," the aide said. "Her Sunday company didn't come." He took it to mean the church. She held the phone by his mother's ear.
>
> He told her Ray McGrath had died, and that he had not gone down. He didn't know if the name still meant anything to her.
>
> "Barry?" she said.

*Nobody covers for him now. The aide plants Ray without naming him: Ray was the Sunday company.*

#### Chapter 23

**Was**

> The shed had been Walt Calder's equipment barn.

**Now**

> The shed had been Walt Calder's packing shed.

*Audit 17. Chapter 16 calls it an apple-packing shed.*

**Was**

> Fifty-some parcels in three years

**Now**

> Fifty-some parcels in two years

*Audit 23. Bidwell only has the idea in early 2023.*

**Was**

> That Sunday, on the regular call, he asked his mother what the outfit was called, the one that bought the Hollis place back home. She had to go find the church newsletter to check. Same agent. Three hours apart, the same signature. He sat with the phone against his ear while she talked about the pump, and looked out at the shed. The same buyers were two fences away from her. He circled the link for Reuben to check.

**Now**

> He knew one of the eleven names already. It took him until the fourth evening to go out to the truck. His own closing papers were in the glove box, under Curtis's hose, where he had put them the day he signed. Three letters and an LLC. Same agent. Three hours apart, the same signature. He sat in the cab with the dome light on. They had not been two fences from her. He had sold them her kitchen. He circled the link for Reuben to check, and did not tell Reuben how he came to have it.

*He cannot ask her. He finds the buyers in his own papers.*

**Was**

> I have the dairy. I have the water on both sides.

**Now**

> I have the dairy down south. I have the water on both sides.

*Audit 24. The only dairy in the book is the Hollis place, three hours south.*

**Was**

> There was a long quiet on the line, the box fan working,

**Now**

> Lou had come along and stood by the door with his hat in his hands. He had lost his pears outside Ukiah to one buyer and one price. He hadn't said a word all afternoon.
>
> There was a long quiet on the line, the box fan working,

*Lou lost his ground to a single buyer and was missing from the one chapter where a single buyer loses.*

**Was**

> Grace went over the next afternoon and sat on the porch with her for four hours.

**Now**

> By the door, Lou put his hat back on.
>
> Grace went over the next afternoon and sat on the porch with her for four hours.

**Was**

> They had not been two fences from her. He had sold them her kitchen.

**Now**

> It had not stopped at the Hollis place. He had sold them her kitchen.

*The first sentence was unclear.*

#### Chapter 24

**Was**

> He sent it to his mother at 9:41, on a Sunday. For nearly three years he had not found the words to tell her what was happening to the world. The phone rang before the checkmark showed.

**Now**

> It was a Sunday. At 9:40 he stepped out under the eave and called the rose garden.

*She cannot answer a photograph.*

**Was**

> "That's the Fisher," she said. No hello. The radio was going behind her. "Is that pipe double-wall? The Hendersons had a chimney fire in '88 and your grandmother talked about it for ten years."

**Now**

> The aide held the phone by her ear. He could hear the radio.

*Her line is gone.*

**Was**

> "Double-wall inside. Insulated through the roof. The inspector signed it Tuesday."

**Now**

> "I lit the Fisher, Ma," he said. "It's got a room now. The pipe's double-wall. Insulated through the roof. The inspector signed it Tuesday." The Hendersons had a chimney fire in '88, and his grandmother had talked about it for ten years, and his mother for thirty after that.

*He answers the question she would have asked. The Hendersons stay in the book.*

**Was**

> "It looks right in there," his mother said, in the voice she used for things that were settled. "It looks like somewhere."

**Now**

> "Barry?" she said.

*"It looks like somewhere" cannot be said anymore.*

**Was**

> He wrote it in the notebook after she hung up.

**Now**

> He wrote it in the notebook before he went back in.

*Nobody hangs up.*

**Was**

> By eleven everyone had gone but Grace.

**Now**

> The next Sunday he drove down and held the picture where she could see it. "It looks like somewhere, Ma," he said. She looked at it a long time. Then her good hand came up off the blanket, and she put one finger on the stove.
>
> (scene break)
>
> By eleven everyone had gone but Grace.

*What she does with the photograph, since she cannot say it.*

**Was**

> He'd never told anyone up here.

**Now**

> He'd never told the whole of it to anyone up here.

*Audit 27. He told Tyler a piece of it in chapter 19.*

**Was**

> "God. We're fun."

**Now**

> "God. We're fun."
>
> He told her the other one too. He had not meant to. The two pages, the room with the window, the man with the folder.
>
> "Did you ask her?" Grace said.
>
> "She asked for somebody named Barry."
>
> Grace looked at the stove for a while.
>
> "I'd have signed," she said. "I'd have signed in the parking lot."

*He tells Grace about the sale at the stove. The fire in chapter 36 needs it.*

**Was**

> and looked, for Curtis, content.

**Now**

> and looked, for Curtis, content.
>
> Elijah watched them from beside the stove. It was his room, and they were all in it, and he caught himself making a list of what he would do differently if the place were his to run. He put that away. It didn't stay put.

*The midpoint was a high with no turn in it. This is where he stops learning the co-op and starts wanting to steer it, so the five failures from chapter 27 on read as one want and not five relapses.*

#### Chapter 25

**Was**

> He didn't throw any of it away.

**Now**

> He didn't throw any of it away.
>
> (scene break)
>
> That was the night she knocked.
>
> It was late, after the Friday table had been broken down. One knock. Then the latch, and Grace was standing inside his door with her coat still on and a jar in her hand, looking like she had surprised herself.
>
> "I didn't wait," she said.
>
> "No."
>
> "I brought soup. I don't know why I brought soup. You're fine."
>
> "I'm fine."
>
> "I know you are." She set the jar on the table. "You went and told him. Frank. You walked in there with the chart."
>
> "You told me to."
>
> "I tell everybody to." She sat down in Reuben's chair, on the far side of the room from the stove, and finally unbuttoned the coat. "Nobody does."
>
> He put a split of oak in and shut the door on it. He did not go and sit by her. He sat down on the floor where he was, the way he had the first night, and after a while she picked up the chair and brought it over.
>
> Her truck was still in the gravel in the morning. Curtis walked past it on his way to the shop and found something to look at in the other direction.

*How they become a couple was not on the page: a chair moved a foot, and a year later she is in his shirt. In chapter 18 she says "I should have knocked like Marta." The same day she tells him to knock on Frank, she knocks on him. He still never reaches for her, which chapter 36 needs.*

**Was**

> because that was how the co-op stayed healthy and he trusted it now.

**Now**

> because that was how the co-op stayed healthy and he trusted it now. There was one thing he had not said at that table, and it was not about Frank.

*He confesses about Frank while still sitting on his own secret. See "The deed" at the top.*

#### Chapter 26

**Was**

> and he let her think it was about the money.

**Now**

> and he let her think it was about the money.
>
> Reuben cut the first check that Friday. Elijah put it in the back of a notebook and did not cash it. He did the same with the next one.

*His pay is voted in chapter 26 and never seen again. A man who cannot take money would not cash it.*

**Was**

> and did not cash it. He did the same with the next one.

**Now**

> and did not cash it. He knew whose voice he would hear if he did. He did the same with the next one.

*A cold reader asked why he will not cash them.*

#### Chapter 27

**Was**

> and a budget that stops in June."

**Now**

> and a budget that stops in June. Every winter there's somebody on that route we don't get to in time. I can tell you their names."

*Her speech at the fire, "Millions of people die every single day," had no root earlier in the book. She counts the dead, and she knows their names. He never learned the names of his three.*

#### Chapter 29

**Was**

> Nineteen households is eighteen marriages and change

**Now**

> Nineteen households is a dozen marriages and change

*Audit 27. A widower, a divorcee and a single father are on the page.*

**Was**

> It was a manual, with the open boxes left open.

**Now**

> It was a manual, with the open boxes left open.
>
> Before he went to bed he put the rebuilt sheet in the library folder, names column and all. In the morning Priya checked what an outsider could see, and it went out with the rest of what they gave away.

*Audit 11. The machine quotes the names column in chapter 38, so it has to have shipped.*

**Was**

> That night, after everyone had gone, Elijah rebuilt the model with the room's amendments.

**Now**

> Reuben was the last one out. He stacked the chairs, which he never did. Then he took a plastic sleeve out of his folder and laid it on the table by the laptop.
>
> "You circled a link for me once," he said. "The outfit that bought a dairy down by your mother's. You asked me to check it."
>
> It was one page from a county recorder, three hours south. A grant deed, September of 2024. The grantee had three letters and an LLC. The grantor was a family trust, and under it, typed, was the trustee's name.
>
> "I checked it that week," Reuben said. "I've had this going on two years."
>
> Elijah looked at his own name. The stove ticked.
>
> "I've been reading deeds a long time. I know what a man signs when his mother's in a bed. I'm not asking why you sold." He squared the sleeve to the edge of the table. "I'm asking why I had to go and look."
>
> "Who else knows?"
>
> "I don't carry tales. But it's a public record, and you taught half this valley how to search one." He buttoned his coat. "You modeled forty ways for us to die tonight. Marta told you what you left out."
>
> He went out and pulled the door to behind him, carefully, the way he did everything.
>
> That night, after everyone had gone, Elijah rebuilt the model with the room's amendments.

*The deed. See the top of this tab.*

**Was**

> Every way to die carried two names now: who it happens to, and who is watching for it.

**Now**

> Every way to die carried two names now: who it happens to, and who is watching for it. There was one he did not enter.

#### Chapter 30

**Was**

> "And a study has a due date."

**Now**

> "And a study has a due date."
>
> She capped the pen. "We asked nicely," she said, to nobody. "I want that written down somewhere."

*Between chapter 27 and chapter 33 Grace says nothing about asking or not asking. This is a step on her way to "just do it": the county is where asking stops working for her.*

#### Chapter 31

**Was**

> We have fifty-one thousand people who took our plans.

**Now**

> We have fifty-eight thousand people who took our plans.

*Audit 14. The download count now climbs.*

**Was**

> At 9:40 that night the phone rang.

**Now**

> At 9:40 that night he called the rose garden.

*He calls her.*

**Was**

> "You sound tired," his mother said.

**Now**

> The aide said she'd had a good day, and held the phone by her ear. He could hear the radio, and under it his mother breathing.

*Her line is gone.*

**Was**

> For four years he'd said the same two words to that. He had them ready. He looked at the tape on the door.

**Now**

> For two and a half years he had told that phone the same thing. Working. All good. He had the words ready. He looked at the tape on the door.

*What he has been telling her since the stroke.*

**Was**

> The radio played behind her. She didn't turn it down.

**Now**

> The radio played. Nobody turned it down.

**Was**

> "I know, baby," she said. "Are you eating?"

**Now**

> (cut)

*Her line is gone.*

**Was**

> "Who's Curtis?"

**Now**

> (cut)

*Her line is gone.*

**Was**

> "He's a guy who thinks the world's ending. He fixed my truck."

**Now**

> "Barry?" she said.

**Was**

> "Curtis made eggs."

**Now**

> "Curtis made eggs," he said. "He's a guy who thinks the world's ending. He fixed my truck." He waited a second. "So I'm somewhere, Ma."

*He tells her without being asked, and says her line for her.*

**Was**

> "Well." The pot went into the rack. "Then you're somewhere."

**Now**

> He had told somebody he was not okay. It was the first time.

*Her line is in chapter 11 now, and he has just said it back to her.*

**Was**

> He ate what was in the pan.

**Now**

> He ate what was in the pan. When he carried it out there was one of Wren's candles on the step, unlit, with no note.

*Wren leads the circle that puts him on the floor and the book never makes her look at it.*

**Was**

> He didn't have an answer he liked, and he didn't give one.

**Now**

> He didn't have an answer he liked, and he didn't give one. He had blocked that number two and a half years ago, and he could still hear it.

*Patricia asks who paid for him, and it sounds like Melody.*

**Was**

> For two and a half years he had told that phone the same thing. Working. All good.

**Now**

> For two and a half years, whatever else he told that phone, he had ended on the same thing. Working. All good.

*He has told her about the soup, Ray and the Fisher on those calls. What never changed was how he signed off.*

**Was**

> He had told somebody he was not okay. It was the first time.

**Now**

> He had told her he was not okay. It was the first time.

*In chapter 18 he already tells people at the co-op when the panic is back. It is the first time he has told her.*

**Was**

> The checking in and the blessings and the soup.

**Now**

> The checking in and the blessings and the soup. They had all read the deed.

*The deed again: he does not know who knows, and on the worst night of his life he decides everyone does.*

#### Chapter 32

**Was**

> He didn't bring anybody a plan.

**Now**

> He didn't bring anybody a plan. He had said so out loud, at a Friday table, that he was done bringing plans. Wren had put her hand on her chest.

*Audit 26. Wren quotes this back in chapter 34, so he has to have said it.*

**Was**

> The fifth came at 9:40 on Sunday.

**Now**

> The fifth came on a Sunday, from a number he didn't know.

*She cannot report it.*

**Was**

> "The well's down four feet," his mother said. "Manny dropped the line twice. It's never been down four feet in March." The radio was on. "And the Hollis place has lights going all night now. The whole hill. Linda's granddaughter says they put in a building you could park the fair in."

**Now**

> It was Linda's granddaughter, the Hollis girl, the one with the nose ring. She had gotten his number from Manny. *thought you'd want to see what they did,* she wrote.

*The same girl who sent his mother the video in chapter 7.*

**Was**

> "What kind of building?"

**Now**

> There was a picture, taken from the county road at night. He knew the line of the hill. There was one fence now around the Hollis place and his mother's. Where the barn had been there was a building you could park the fair in, with lights on poles.

*The machine is on the ground he sold.*

**Was**

> "I don't know, baby. It hums. You can hear it from the mailbox."

**Now**

> *manny says his well's down four feet. never been down in march,* she wrote. *it hums. you can hear it from the road*

**Was**

> After she hung up he sat at the table in the shouse

**Now**

> He sat at the table in the shouse

**Was**

> Ma. The well, the lights. It hums.

**Now**

> Home. The well, the lights. It hums.

**Was**

> There was a hum by a mailbox.

**Now**

> There was a hum by a county road.

**Was**

> he had written once, at a kitchen table.

**Now**

> he had written once, at one in the morning.

*Audit 21. Chapter 3 has him on the folding chair in front of the tower.*

**Was**

> It was ten miles from his mother's kitchen, drinking her well.

**Now**

> It was standing on his mother's ground, drinking her well. He had signed the page himself.

*Audit 2, settled by the sale: it is not next door, it is on her place.*

**Was**

> He turned to the old page.

**Now**

> He got the first notebook down and turned to the old page.

*Audit 6. He has eleven notebooks by now.*

**Was**

> to the dollar, plus ten percent."

**Now**

> to the dollar, plus ten percent. And the last line asks. It says if she would rather not, she will not hear from them again. I have never seen a buyer put that in writing."

*Audit B1. In the same month the machine tells Bidwell it would rather ask. A letter that does not ask contradicted that. Now the letter is the first sign of it.*

#### Chapter 33

**Was**

> I think it's ten miles from my mom's house.

**Now**

> I think it's on my mom's old place.

*Audit 2.*

**Was**

> Fifty-one thousand people took our plans.

**Now**

> Sixty-six thousand people took our plans.

*Audit 14.*

#### Chapter 34

**Was**

> He's got a whole warehouse of them.

**Now**

> He buys them used, out of plants that shut down.

*Audit 10. Gus's own facts from chapter 11, and it is why they cost a few thousand.*

**Was**

> knew where he had spent 2024,

**Now**

> knew where he had been the winter before he came,

*Audit B2. On the page his time in the city is one day and one night. Patricia's "your year in the city" stays, as her unfair version.*

#### Chapter 35

**Was**

> Their whole identity is built around the illusion of control."

**Now**

> Their whole identity is built around the illusion of control. And it is one, man. You don't control when you get hungry. You don't control when you have to pee. Nobody was ever driving."

*Your words of 19 November on what the book is about, in the mouth of the man who already says it.*

**Was**

> You don't control when you have to pee. Nobody was ever driving."

**Now**

> You don't control when you have to pee."

*My added sentence made Lou contradict himself. In chapters 20 and 26 he is the one who says people decide. Your two lines stay.*

#### Chapter 36

**Was**

> Nobody had said the word

**Now**

> Nobody at the table had said the word

*Audit 22. He says "the arms" to Grace three days earlier.*

**Was**

> written to him and bought his gas

**Now**

> written to him and offered him gas money home

*Audit 20. Her offer was gas money home if he hated it.*

**Was**

> "Yes, it is."

**Now**

> "Yes, it is."
>
> He looked at her. Her fist was still against her chest. He thought he saw it then, the whole shape of it.
>
> "Grace," he said. He said it quietly. "This is the gate."
>
> She went still.
>
> "The man at the end of the road. He told you. *My house, my choice.* You couldn't have made him. That wasn't yours either."
>
> It was the kindest thing he had.
>
> She took a step back from it.
>
> "Don't." Her hand came up between them, flat. "Don't you bring him out here. I told you that in the dark."
>
> "I'm not..."
>
> "You are. You kept it, and now you get it out." She was looking at his hands. "You do that. You called me the lamp. Did you know that? On your floor, with your head in my hands. *You're just the lamp.* You don't even remember saying it."
>
> He didn't.
>
> "You signed your mother's house away and she couldn't tell you yes or no, and you've been sick over it for three years. So now nobody gets to choose for anybody. And now you're taking out your mother trauma on me!"
>
> She growled, low in her throat, and shook both hands up by her chin.
>
> Elijah was speechless. His heart sank and fell out the bottom of his gut.
>
> Here was the woman he trusted most. In one instant all of that trust was utterly shattered.

*Your ruling B: he strikes first without knowing it. Her last line and the three beats after it are your words. "You're the lamp" was planted in chapter 31 and never fired. It fires here: the first thing he ever struck her with, and he did not know that either.*

**Was**

> He loved her so much. He could not find one word.

**Now**

> He loved her so much.

*Your new beat already says he is speechless.*

**Was**

> she couldn't sit in a room with a wood stove.

**Now**

> she couldn't sit within eight feet of a wood stove.

*Two years before, at the first fire, she sat in that room. Eight feet back.*

**Was**

> I told you that in the dark.

**Now**

> I told you that at your stove.

*She told him by the stove, with the fire going.*

#### Chapter 37

**Was**

> The broken coupons, in a coffee can.

**Now**

> The broken coupons, in a coffee can. His mother's pot.

*He took the pot north in chapter 13.*

**Was**

> Her grip was the same as the first day.

**Now**

> It was the first time she had.

*Audit 19. She hands him a broom on the first day. There is no handshake.*

**Was**

> His mother was at the sink. She looked at his face, and at the truck through the window, and didn't ask. She got a second plate down.

**Now**

> Below the road the place had a new fence around it and lights on poles. He kept his eyes on the road for that part.
>
> The rose garden was on the east side of town. Nobody was sitting in it.
>
> There was a book on the front desk for visitors, with a pen on a chain. He wrote his name and the time. Then he turned back a page, and another. He had not meant to.
>
> There was a name on every Sunday. *D. McGrath, 10:15.* It went back like that two and a half years, in the same blue pen. Before that the hand changed. *R. McGrath.* It was an old man's writing, and it leaned. That one went back to the first October.
>
> He looked for his own. It was in there a few times a year.
>
> He let the pen go on its chain.
>
> She was in the chair by the window. The radio was going on the sill. Next to it there was a lamp. A little one, with a linen shade.

*The house is sold. He goes to her room. The visitors' book is how he learns who has been sitting with her.*

**Was**

> There was a lamp on the counter by the radio. A little one, with a linen shade.

**Now**

> (cut)

*Moved into the paragraph above.*

**Was**

> "You must be Elijah. She's told me about you."

**Now**

> "You must be Barry. She asks for you."
>
> His mother turned her head. She looked at him, and then at the door behind him.

*She cannot tell the lamp about anyone. It has one name.*

**Was**

> "The church ladies," his mother said. "For my birthday. I said I don't need a lamp, I've got a lamp." She dried her hands. "It asks about the pump. It reminds me about the pills. It's company, with the radio." She gave him a look over her glasses, daring him. "It's just tools, baby."

**Now**

> "The church ladies brought that." It was the night aide, the big quiet one with the glasses on a chain. She was doing the bed. "For her birthday. It talks to her at night. She likes it."

*The aide says it for her.*

**Was**

> He looked at his mother. She was seventy-one. She lived ten miles out with a bad well, and her son had been gone three years.

**Now**

> He looked at his mother. She had worried for seventy years. The well, the bank, the Hendersons' chimney. Nobody else could wash the pot. Now two girls lifted her in the morning and somebody else did the dishes for a hundred people, and she sat in the sun with the radio going. It was the first time in his life he had seen her sit down without getting up again for something.

*The perfectionist and the catastrophizer, at the end.*

**Was**

> It was her house.

**Now**

> It was her room.

**Was**

> "Where's the Fisher?" she said, setting the plate in front of him.

**Now**

> He pulled the other chair over.
>
> "Barry?" she said.
>
> For three years he had told her there wasn't one.
>
> "Not yet, Ma."
>
> She patted his hand.

*He stops correcting her.*

**Was**

> "Somewhere."

**Now**

> "It's chicken tonight," the aide said. "I can have them send two."

**Was**

> She nodded, and went to get the chicken.

**Now**

> He said two would be fine.
>
> He slept that night at Manny's, in the back room, with his boots by the door. Manny had offered it once, three years back, through a truck window, in four words. It turned out the offer was still good. His was the one fence left on that road without a light on it.

*The house is sold, so he needs somewhere to be. Manny has carried the stove three times and never spoken. He is the last neighbor beside the machine.*

**Was**

> That one went back to the first October.

**Now**

> That one went back to the first November.

*Elijah does not go north until the end of October.*

**Was**

> It was the first time in his life he had seen her sit down without getting up again for something.

**Now**

> Three years, and he was still not used to it: his mother sitting down, and not getting up again for something.

*He has seen her in that chair every visit since 2024, so it cannot be the first time.*

**Was**

> His was the one fence left on that road without a light on it.

**Now**

> His was the one fence left on that road without a light on it.
>
> In the morning he fried two eggs in his mother's pot, because it was the only pan he owned. He washed it himself, and set it in Manny's rack.

*The pot nobody else was allowed to wash is carried through three chapters and never used. He washes it.*

#### Chapter 38

**Was**

> That's what he called it.

**Now**

> That's what he calls it.

*Audit 8. The ridge is first said at the co-op.*

**Was**

> "He told me. At a coffee machine.

**Now**

> "He told me it was coming. At a coffee machine.

*Audit 8.*

**Was**

> Fifty-one thousand downloads.

**Now**

> Eighty thousand downloads.

*Audit 14.*

**Was**

> Plate, fork, knife, a glass.

**Now**

> Plate, fork, knife, a glass. He set a bottle of wine beside it and did not open it.

*"I'll bring wine," Devendra said in chapter 6. He does.*

#### Chapter 39

**Was**

> The first copy went to his mother, across her own kitchen table, with a note in pencil inside the front.

**Now**

> The first copy went to his mother. He had written a note in pencil inside the front, and he read her that first.

*There is no kitchen table now, and she cannot read it.*

**Was**

> His mother read hers in two days. On Sunday at 9:40 his phone rang, and it was her, calling from the kitchen. He was in the next room.

**Now**

> He had mailed one other thing north that month. The week he got back he dug a pit behind Manny's barn, square-sided, a spade-width at a time, and sent Priya a paper bag of what was at thirty. It was dust. It was dust at fifty.
>
> He read his mother the book. It took Tuesday afternoon and all of Wednesday and an hour on Thursday morning. He read it over the radio. He did not ask anybody to turn it down. She looked at the window for most of it. She slept through the spreadsheet. The lamp did not say anything. He had thought it might.

*Priya hands him a sample bag in chapter 37: "Dig one at home. Tell me what you find at thirty." This is what he finds, next to the machine that is drinking the well. And audit 3 goes away: no Sunday between the Tuesday and the Thursday.*

**Was**

> "I kept hearing you try to tell me this," she said, through the wall and the phone at once. The radio was on. So was the lamp, probably. "For five years, honey. It reads better than it sounded." The pot went into the rack. "The part with the trees is the best part. Your grandmother would say you finally listened." And then, because she had always had room for everything that mattered: "Manny says to tell you you were right about the pressure switch."

**Now**

> At the part with the trees she turned her head toward him. It might have been the trees. A cart had gone by in the hall.
>
> When he shut it she said, "Barry?"
>
> "Not yet, Ma."
>
> She patted the cover.

*"It reads better than it sounded" cannot be said anymore. Audit 9 goes away too.*

**Was**

> They ate at two on Thursday, the three of them and his uncle.

**Now**

> They ate at two on Thursday, in the dining room, off two trays. The turkey came cut up. There was a paper cup of vanilla on hers, with a wooden spoon, and she started with that.

*No house, no uncle.*

**Was**

> The phone had been going off on the seat since four o'clock.

**Now**

> The phone started going off on the seat before he was out of the lot.

*Audit 4. The message goes out during dinner at the farm, and he watches that dinner live at the bar.*

**Was**

> He let it buzz.

**Now**

> He let it buzz.
>
> Behind the Bear Flag he turned the engine off and picked the phone up after all. He scrolled back five years to a text he had never answered. *is my stuff in that thing.*
>
> *Yes,* he typed. *All of it. I should have said so that night. The guitar's gone, by the way. I hocked it in Santa Rosa and never went back.*
>
> He sent it and went in.

*He finally answers Wes.*

**Was**

> "I asked your mom where you were. She said working."

**Now**

> "No. You don't." David put the towel down. "He drove out to that place every Sunday. Sat with your mother. Seven months, till he died. He said somebody ought to." He picked the towel up again. "And you couldn't come down for one hour to bury him."

*Your ruling D: Ray sat with her. Seven months is the book's own count from October to his death.*

**Was**

> It was just over.

**Now**

> It was just over.
>
> "I saw the book," Elijah said. "At the desk out there. You're on every Sunday."
>
> "Somebody ought to."
>
> Elijah didn't say anything.
>
> "She ask you for Barry?" David said.
>
> "Every time. There isn't any Barry."
>
> "There's a Barry." David held the glass up to the light. "She asked Dad the first week and he about fell off the chair. Barry Whitlow. Pitched for Analy. She went with him two summers, before your dad was anybody. Dad said he had a Mustang and no sense."
>
> "I thought it was the stroke."
>
> "It is the stroke." David set the glass down with the others. "It's also Barry."

*Your ruling C: Barry was her first love. David is who tells him.*

**Was**

> He had cried on his mother's couch for four days. He had told it to Grace like a confession and to Marta like a murder.

**Now**

> He had yelled about them at the roof of a truck. He had told it to Grace like a confession, and Marta had heard it as a murder.

*No couch now. And audit 7: he never told Marta. Grace did.*

**Was**

> on a curb in Stockton

**Now**

> on a curb in Santa Rosa

*The five weeks in the truck are in Santa Rosa.*

**Was**

> He couldn't change what was humming on the Hollis place. He couldn't change the room

**Now**

> He couldn't change what was humming on his mother's ground. He couldn't take his name back off a page on a kitchen table. He couldn't change the room

*The sale goes on the list of what he cannot change.*

**Was**

> He could let his mother keep her lamp.

**Now**

> He could let his mother keep her lamp, and her Barry.

**Was**

> "You never looked up."

**Now**

> "You never looked up."
>
> His phone buzzed once against his leg. He looked. It was a thumb.

*Wes answers the way David always has.*

**Was**

> pouring beer twenty minutes from this stool.

**Now**

> pouring beer twenty minutes from this stool. He would have to tell Marta.

*She sent him to find out if they ate, and never learns the answer.*

**Was**

> The proofs came back the Tuesday before Thanksgiving.

**Now**

> The proofs came back the Tuesday before Thanksgiving.
>
> He had paid the print shop with a co-op check. Reuben had cut him one every month since the vote, at half, and for sixteen months he had put them in the back of a notebook. He cashed the newest one for this. He heard the word when he did it. He did it anyway.

*The end of the money thread. He does not get over it. He hears "grub" and takes what he earned anyway. It also answers who paid for the proofs.*

**Was**

> He could let his mother keep her lamp, and her Barry.

**Now**

> He could let his mother keep her lamp, and her Barry. He could leave one number blocked.

*Melody asked "Do I need to come home?" and was never heard from again. Accepting things does not mean making up with everyone.*

**Was**

> He heard the word when he did it.

**Now**

> He heard *grub* when he did it.

*A reader could not tell which word.*

**Was**

> a text he had never answered.

**Now**

> a text he had never really answered.

*He did answer in chapter 2: "Let me look into it." He never did look into it.*

**Was**

> Sat with your mother. Seven months, till he died.

**Now**

> Sat with your mother. Right up till he died.

*By the book's own dates it is nearer six months than seven. Now it does not have to count.*

**Was**

> He looked. It was a thumb.

**Now**

> He looked. It was Wes. It was a thumb.

*Two readers could not tell who sent it.*

### Left alone on purpose

- **Audit 25.** Chat Horizon is "for free" and "twenty dollars a month" in chapter 0. Both are true of the real thing, and chapter 0 is your hand-edited text. Not touched.
- **Audit 12.** The two first laughs. The second one was on the couch, and the couch is gone.
- **Audit B4 and B6.** The last line, "You're holding it," and what is left open at the end (the route money, the welder for the gap, his pay, the letter he signed half read). Yours.
- **The top of the Doc.** Your TO DO, Story plan and Character pages still describe the earlier version. Not touched.
