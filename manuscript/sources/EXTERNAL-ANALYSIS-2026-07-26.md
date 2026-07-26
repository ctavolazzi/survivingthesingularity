# External analytical evaluation of Surviving the Singularity

**Received 2026-07-26 from CT.** Title: "Socio-Technical Metamorphosis and Agentic
Resilience: An Analytical Evaluation of *Surviving the Singularity*." Third-party
synthesis of the manuscript, machine-assisted, 15 pages, 8 works cited.

---

## READ THIS FIRST: what this document is and is not

**It is a cross-reference.** Someone outside the project read the book and restated its
architecture in analytical register: the nine stages, the precedent ledger, the
technical claims, the case studies. That makes it a useful mirror. Where it matches the
book, the book communicated. Where it drifts, either the book is ambiguous or the
analyst inferred.

**It is NOT a source, and nothing in it may be cited.** Its own works-cited list runs to
eight entries, several of them Medium posts and one of them the book's own Medium
article, so a number appearing here has not been independently verified. Its numbers
are almost entirely *restatements of the book's own claims*, which means using it to
verify the book would be circular.

> **The failure mode to avoid: laundering.** The book has real citation debt.
> Precedents P-07 through P-22 are unverified and Appendix B sources 166-178 are
> unchecked. A document like this one, which confidently restates those exact claims in
> authoritative prose, is the single easiest way to convince yourself they are now
> verified. They are not. Treat every figure below as a **verification worklist item**,
> not as a receipt.

Chapter agents: use this to check whether your chapter's argument survived contact with
an outside reader. Do not add a single citation from it to Appendix B.

---

## 1. Subtitle discrepancy (found on intake, needs a CT ruling)

The analysis calls the book *"Surviving the Singularity: Staying agentic while AI
rewrites work, money, medicine, and meaning."* That is a fourth variant. The repo
currently carries three:

| Location | Subtitle | What it drives |
|---|---|---|
| `src/lib/data/book/book.json` | The 9 Stages of the Singularity and the Future of Earth | EPUB and PDF metadata, the shipped artifact |
| `src/app.html` | A field manual for staying agentic as AI rewrites work, money, medicine, and meaning. | Social cards, search results |
| `src/lib/components/BookCoverModal.svelte` | A field manual for staying agentic as AI rewrites the world. | What a preorder buyer actually sees |

Three subtitles, six weeks from publication, with a preorder campaign starting in
August. The cover a buyer sees and the metadata inside the file they download do not
agree. This needs one ruling and one sweep.

---

## 2. Where the analysis confirms the book landed

These read back accurately, which is evidence the writing is doing its job:

- The nine stages, their three-era grouping, and Stage 4 as the hinge.
- The thesis that the event horizon is already crossed and 2027 is the tipping point.
- Hyper-local mesh topology as the answer, explicitly *not* political reform and
  explicitly *not* Luddite resistance.
- The Precedent Ledger as case law rather than anecdote, with the story to mechanism to
  rule structure intact.
- The co-op case studies: the Crucible, Priya's soil trials, Denny, Irene Calder.

Notably it also absorbed the v0.7.1 reframe: it lands on "liberation from compulsory
toil" and "optional production models" rather than on collapse. The wake-up-call turn
survived an outside reading. That is worth knowing.

---

## 3. Claims restated, each needing independent verification

Numbers as the analysis states them. **Every one is a worklist item.** The Verified
column is for whoever does the checking.

### Transformer and AGI timeline

| Claim | Verified? |
|---|---|
| WMT 2014 EN-DE: ~26.4 BLEU legacy to 28.4 BLEU Transformer | |
| WMT 2014 EN-FR: ~40.4 to 41.8 BLEU | |
| Training cost: weeks/months on clusters to 3.5 days on eight GPUs | |
| Expert survey 50% HLMI estimate moved 2060 to 2047 in one iteration | |
| Subset of researchers place human-level AGI as early as 2027 | |

Primary source for the first three is Vaswani et al., "Attention Is All You Need"
(2017). The survey claim is Grace et al.; `AUDITOR-BRIEF` says Grace numbers were
already checked at v0.5.0, so reconcile rather than redo.

### DishBrain / synthetic biological intelligence

| Claim | Verified? |
|---|---|
| 800,000 in vitro human and rodent neurons on high-density MEAs | |
| Self-organized to learn gameplay within five minutes | |
| Sample efficiency far above DQN, A2C, PPO | |
| Draws a fraction of a watt | |
| AU$600,000 grant from Australian Office of National Intelligence | |

`AUDITOR-BRIEF` records DishBrain (AU$) as already fact-checked. Confirm scope: the
currency was checked, but the neuron count and the five-minute figure may not have been.

### Jahoda latent deprivation

| Claim | Verified? |
|---|---|
| Five latent functions: time structure, social contact, collective purpose, status/identity, enforced activity | |
| LAMB scale used across 13 studies, 5,692+ participants | |
| Deprivation accounts for ~70% of the unemployment to mental-health correlation | |

The 70% figure is the one to scrutinize. It is the kind of precise-sounding number that
an acquisitions editor will check, and "accounts for approximately 70% of the
correlation" is a strong claim about mediation.

### Neo-Luddite incidents (Chapter 7 territory)

| Claim | Verified? |
|---|---|
| Waymo Jaguar struck and killed a dog, 21 May 2023, Toland St, San Francisco | |
| SF Fire Chief: nearly 40 instances of AVs disrupting emergency response | |
| Waymo robotaxi destroyed by firework in Chinatown, 10 Feb 2024 | |
| US federal probe into Waymo safety around school buses | |
| Safe Street Rebels target only empty vehicles, avoid intersections | |

`AUDITOR-BRIEF` says Waymo backlash data was already folded into ch7. Reconcile these
specific dates against what is in the chapter.

### Luddites and precedent details

| Claim | Verified? |
|---|---|
| Frame Breaking Act made machine-wrecking a capital crime | |
| Twelve thousand soldiers deployed, exceeding Wellington's Peninsular force | |
| Luddites spared machines of masters who kept fair terms | |
| Paine's *Common Sense*, January 1776, forty-seven pages | |
| Bernays "torches of freedom," Easter Sunday parade, 1929 | |
| Trithemius, *De Laude Scriptorum*, 1492, had it printed | |
| US horse population peaked ~25 million in the 1910s | |

The Wellington comparison is the sort of vivid claim that is often repeated and rarely
sourced. Verify it directly or soften it.

### Thermodynamics and attention

| Claim | Verified? |
|---|---|
| ~20 minutes to return to a demanding task after one interruption | |
| More than three interrupts per hour means baseline focus is never reached | |

The 20-minute figure traces to Gloria Mark, which `AUDITOR-BRIEF` lists as already
verified. The "three per hour" threshold appears to be the book's own derivation from
it. If so, it must be presented as the book's inference, not as a research finding.

### Shouse and infrastructure specs

| Claim | Verified? |
|---|---|
| Closed-cell spray foam 75 mm walls (R-21), 100 mm ceilings (R-28) | |
| Continuous heating/cooling load under 500 W | |
| 8kW solar, 8kVA inverter, 14.36 kWh battery | |
| Brooklyn Microgrid, 2015, LO3 Energy + Siemens + ConsenSys | |
| Sears Modern Homes, 1908-1942, precut numbered lumber by rail | |

The under-500W envelope claim is load-bearing for the whole "$25,000 exit" argument and
depends on climate, area, and delta-T. State the assumptions or soften it.

### Soil refinery chemistry

| Claim | Verified? |
|---|---|
| Haber-Bosch, delta-H = -92.4 kJ/mol, 15-25 MPa, 400-500 C | |
| Haber-Bosch consumes ~2% of global energy | |
| Biological fixation equation via Rhizobium and mycorrhizal fungi | |
| ACT needs >6.0 mg/L dissolved oxygen | |
| C(DO,sat) ~= 468 / (31.6 + T) mg/L; 10.04 at 15 C, 7.02 at 35 C | |
| 12V linear pump at 80 L/min through high-porosity diffusers | |

The DO saturation formula is a standard empirical approximation. Check the arithmetic at
both stated temperatures, and confirm the constant is the one in general use.

---

## 4. The Precedent Ledger restated, P-01 to P-22

Useful as a **cohesion check**: it shows what each precedent's rule reads as to an
outside reader. Compare against `manuscript/HISTORY-CASEBOOK.md` and Appendix D. Where
the analyst's rule differs from the book's, the block is probably ambiguous.

| ID | Event | Mechanism | Rule as read by the analyst |
|---|---|---|---|
| P-01 | The Reading Rage (1790s) | Panic over decentralized media access | "Kids these days" marks power moving to people who no longer need institutional permission |
| P-02 | The Toy at the Fair (1876) | Mismeasurement of disruptive scale | Ask what dies when the capability becomes boring, not how impressive the demo is |
| P-03 | One Million Years (1903) | Flawed expert linear extrapolation | Expert timelines are autopsies of the last failure; frontier progress is a door, opening all at once |
| P-04 | The Red Flag Act (1865) | Incumbent regulatory capture | Safety collars do not stop technology, they decide which region profits |
| P-05 | The Fleet That Sailed Home (1433) | Voluntary surrender of capability | Abandoned capability emigrates to whoever keeps sailing |
| P-06 | The Great Demotion (1543) | Human decentering | Humans survive decentering; monopolies charging rent on the old map do not |
| P-07 | The Horse's Last Ledger (1783-1960) | Cost-per-watt competition | Thermodynamic arithmetic does not negotiate; audit your energy ledger first |
| P-08 | The Grain Trap (c. 9500 BC) | Irreversible adoption ratchet | Adoption is driven by group competition, not individual consent |
| P-09 | The Frame-Breakers (1811-1816) | Physical war on machinery | Resistance aimed at the machine hits the part that cannot hear |
| P-10 | Torches of Freedom (1929) | Extraction disguised as identity | Persuasion does not argue with values, it wears them |
| P-11 | The Year Bronze Stopped (c. 1177 BC) | Failure of specialized trade | Interdependence is contagion; resilience is what works when the ships stop |
| P-12 | The Abbot's Confession (1492) | Unconscious adoption | Critics adopt the machine to publish the criticism; read the workflow, not the essay |
| P-13 | The Quartz Heresy (1969-1983) | Disruption of legacy manufacturing | Use the new machine's profits to fund what you want preserved |
| P-14 | One Hundred Sixty Acres (1862) | Land redistribution in crisis | Transitions reprice land first; the emergency is why the filing office is empty |
| P-15 | The House by Mail (1908-1942) | Bypassing builder monopolies | Find the version that ships as a kit with expertise in the manual |
| P-16 | Graveyard of the Unconvinced (1975-2011) | Refusal to divest legacy assets | Seeing the wave is easy; divesting the beachfront is the hard part |
| P-17 | The Mirror Twin (2000s) | Capability outliving product | Products are mortal, capabilities transfer if identified in time |
| P-18 | Twenty Million Gardens (1943-1944) | Standby infrastructure | The soil by the door has a proven activation record; keep it warm |
| P-19 | Forty-Seven Pages (1776) | Permissionless distribution | Leverage is reach divided by permission |
| P-20 | Access to Tools (1968) | Repairable spatial autonomy | Tools, not credentials, make people capable |
| P-21 | The Apocalypse On Time (1999) | Successful preemption | A premortem that works looks like paranoia that was not needed |
| P-22 | The Passing Fad (1995-2000) | Dismissal of exponential networks | Early iterations are the worst the technology will ever be; dismissal is a lagging indicator |

---

## 5. Case-study details worth checking for continuity

Against `ELIJAH-PROTOCOL.md`. If the analyst got a detail wrong, the book may be
ambiguous there:

- **The Crucible**: three retired enterprise servers from a county surplus auction, two
  scavenged compute cards, 48 GB combined, salvaged Honda Civic radiator on the north
  wall. One config line exposed 19 households of data for 41 hours. Response was a
  public postmortem plus lockout-tagout with a physical signature in a paper log.
- **Priya's soil trials**: 12 raised beds, 6 inoculated with ACT from a 55-gallon drum
  with molasses and kelp, 6 controls. Capacitive sensors at 1 cm depth produced a
  "confident fiction." Manual pits showed control roots turning sideways at four inches
  against hardpan while tea beds ran past 30 cm. Fix was multi-depth PVC probes at 5,
  15, and 30 cm calibrated against physical ground truth.
- **Denny Osei**: warehouse worker, reskilled 2019 into logistics and dispatch routing,
  displaced again 2023. Runs @thecoffeejesus. Scripted "optimal" engagement videos were
  buried as synthetic slop; his plain register worked.
- **Irene Calder**: widow, 40 acres, month-to-month lease. Agent offered 22% over market,
  cash, 14-day close. County records showed 11 LLCs sharing one Sacramento registered
  agent holding fifty-some parcels across three counties. Answer was a Community Land
  Trust with a plain-language covenant.

Note: the co-op is stated as **nineteen households**, and the leak is stated as
exposing **nineteen households** of data. Confirm both against the protocol bible, since
one number may have been inferred from the other.

---

## 6. Its own works cited

Eight entries. Recording them for provenance, not for use:

1. "Surviving the Singularity: Your Essential Guide..." thecoffeejesus.medium.com
2. situational-awareness.ai (Aschenbrenner)
3. philippdubach.com, "Aschenbrenner: Situational Awareness Two Years On"
4. "Playing Brains: ... DishBrain," PMC10602981
5. community.openai.com thread on situational-awareness.ai
6. medium.com/data-science-collective, "Situational Awareness, Two Years Later"
7. forum.effectivealtruism.org, summary of Situational Awareness
8. medium.com/@thecoffeejesus/about

Entry 4 (the PMC DishBrain paper) is the only peer-reviewed item and is worth pulling
directly for the Chapter 2 and 5 neuron claims. Entry 1 and entry 8 are the book's own
author, so any agreement there is self-reference, not corroboration.
