# The cast

A folder for each character, and a branch for each: `character/<folder name>`.

In each folder:

- `README.md` says who they are in a line. It is written by hand and kept.
- `gathered.md` is everything the notes say about them, each piece with the file it came from.
- `appearances.md` is where they are in the book, by chapter and paragraph.
- `readers/`, where there is one, holds readers' reports about them.

`gathered.md` and `appearances.md` are built by code and rebuilt each time:

```bash
python3 manuscript/tools/book.py cast
```

To add a character, add them to `cast.json` and run that. What a character's story is, what is
missing and what CT has ruled goes in a file of its own in their folder, written by hand.

Ricardo and the leader of the farm are not in the book yet. They come from CT's dictation of the
morning of 19 November.

<!-- cast -->

| Folder | Who | First seen | Last seen | Paragraphs that name them |
|---|---|---|---|---|
| [`elijah/`](elijah/) | Elijah Galen Madrone | Author's Note | Chapter 39: Back to Bear Flag | 387 |
| [`grace/`](grace/) | Grace | Chapter 15: One O'Clock on Saturday | Chapter 39: Back to Bear Flag | 95 |
| [`his-mother/`](his-mother/) | His mother | Chapter 0: The Demonstration | Chapter 39: Back to Bear Flag | 76 |
| [`melody/`](melody/) | Melody | Chapter 13: Two in the Afternoon | Chapter 14: Rain | 5 |
| [`david/`](david/) | David McGrath | Chapter 0: The Demonstration | Chapter 39: Back to Bear Flag | 83 |
| [`ray/`](ray/) | Ray McGrath | Chapter 0: The Demonstration | Chapter 22: The Crucible | 7 |
| [`his-grandmother/`](his-grandmother/) | His grandmother | Chapter 0: The Demonstration | Chapter 39: Back to Bear Flag | 13 |
| [`his-father-and-manny/`](his-father-and-manny/) | His father, Manny and the uncle | Chapter 3: 9:40 on Sunday | Chapter 39: Back to Bear Flag | 24 |
| [`nate-and-wes/`](nate-and-wes/) | Nate and Wes | Chapter 0: The Demonstration | Chapter 39: Back to Bear Flag | 26 |
| [`devendra/`](devendra/) | Devendra | Chapter 1: You'll Calibrate | Chapter 39: Back to Bear Flag | 34 |
| [`the-realtors-and-the-three/`](the-realtors-and-the-three/) | The realtors, and Kelsey, Carol and Mateo | Chapter 0: The Demonstration | Chapter 39: Back to Bear Flag | 24 |
| [`lindas-granddaughter/`](lindas-granddaughter/) | Linda's granddaughter | Chapter 7: Out of Hand | Chapter 32: Hush | 3 |
| [`ruby/`](ruby/) | Ruby Roth-Jones | Chapter 7: Out of Hand | Chapter 16: Swarf | 34 |
| [`the-architect/`](the-architect/) | The Architect | Chapter 3: 9:40 on Sunday | Chapter 33: Normal | 6 |
| [`gus/`](gus/) | Gus | Chapter 11: Two Million Dollars of Robot Arms | Chapter 12: Not on the List | 16 |
| [`bidwell/`](bidwell/) | Aaron Bidwell | Chapter 2: Terms of Service | Meanwhile (after Chapter 31) | 17 |
| [`bidwells-reader/`](bidwells-reader/) | Bidwell's reader | Meanwhile (after Chapter 2) | Meanwhile (after Chapter 31) | 11 |
| [`the-old-man-on-the-curb/`](the-old-man-on-the-curb/) | The old man on the curb | Chapter 15: One O'Clock on Saturday | Chapter 39: Back to Bear Flag | 23 |
| [`the-others-on-the-road/`](the-others-on-the-road/) | The others on the road | Chapter 7: Out of Hand | Chapter 13: Two in the Afternoon | 18 |
| [`the-machine/`](the-machine/) | The machine | Author's Note | Afterword: We Don't Have to Live Like This | 57 |
| [`marta/`](marta/) | Marta Okonkwo | Chapter 16: Swarf | Chapter 39: Back to Bear Flag | 77 |
| [`lou/`](lou/) | Lou | Chapter 17: Pass the Beans | Chapter 38: Thanksgiving | 50 |
| [`denny/`](denny/) | Denny Osei | Chapter 17: Pass the Beans | Chapter 38: Thanksgiving | 56 |
| [`curtis/`](curtis/) | Curtis | Chapter 17: Pass the Beans | Chapter 38: Thanksgiving | 64 |
| [`tyler/`](tyler/) | Tyler | Chapter 19: Ugly Is a Maintenance Feature | Chapter 38: Thanksgiving | 46 |
| [`priya/`](priya/) | Priya | Chapter 17: Pass the Beans | Chapter 39: Back to Bear Flag | 38 |
| [`reuben/`](reuben/) | Reuben Vance | Chapter 19: Ugly Is a Maintenance Feature | Chapter 39: Back to Bear Flag | 50 |
| [`frank/`](frank/) | Frank Kowalski | Chapter 19: Ugly Is a Maintenance Feature | Chapter 38: Thanksgiving | 42 |
| [`wren/`](wren/) | Wren | Chapter 20: What a Tomato Costs | Chapter 38: Thanksgiving | 21 |
| [`patricia/`](patricia/) | Patricia | Chapter 19: Ugly Is a Maintenance Feature | Chapter 38: Thanksgiving | 21 |
| [`rosa/`](rosa/) | Rosa | Chapter 13: Two in the Afternoon | Chapter 39: Back to Bear Flag | 17 |
| [`irene/`](irene/) | Irene Calder | Chapter 23: Forty Acres | Chapter 38: Thanksgiving | 21 |
| [`the-girl-and-the-mother-from-redding/`](the-girl-and-the-mother-from-redding/) | The girl with the laptop, and the mother from Redding | Chapter 36: The Fire | Chapter 39: Back to Bear Flag | 3 |
| [`ricardo/`](ricardo/) | Ricardo |  |  |  |
| [`the-leader/`](the-leader/) | The leader of the farm |  |  |  |
