# Part III and Conclusion: v0.10.0 finalization review

Reviewed 27 September 2026 by Codex in `active/sts-v0.10.0`, from the v0.9.2 manuscript. Canonical prose lives only in `src/lib/data/book/`; figures live in `static/book-images/`. No commits, releases, deployments, or deletions were performed by this review task.

## Coverage

All eleven assigned sections were read in full, including opening scenes, Foundations, practical assignments, precedents, epigraphs, captions, and cross-references:

| Section | Review outcome |
| --- | --- |
| Chapter 10, Create Over Consume | Qualified the model-collapse schematic and removed a false guaranteed mean/timetable. Removed an unsourced per-page energy quantity and the claim that an offline digital manual uses no energy. Kept algorithmic judo as an approach to test, rather than a guarantee that truthful stories go viral. |
| Chapter 11, Robotic Court | Kept the privacy breach, notification, human review, and food-service argument. Marked the memory buffer as illustrative, separated 16-bit storage from the misleading phrase “full precision,” and required model/workload checks. Distinguished heat-flow arithmetic from a usable pump or radiator specification. |
| Chapter 12, Land Strategy | Retained the trust negotiation, consent, separate adviser, payment obligations, New Communities history, and door-to-door food example. No body edits. Root replaced the opening image separately. |
| Chapter 13, Shouse Protocol | Distinguished 640 square feet of outside footprint from usable interior floor space. Replaced absolute condensation protection with assembly-level air/moisture control. Removed unsupported temperature/power guarantees in its thermal diagram. Preserved CT's sourced shouse passage and Marta's structural-welding scene. |
| Chapter 14, Long Tail | Corrected France's 2016 law from a universal donation command to its actual food-safety and donation-agreement provisions. Removed the claim that all waste is edible food. Mesh routing now requires another usable radio path. Retained Frank's move, worker transition, and the two closing precedents. |
| Chapter 15, Soil | Removed unsupported household caloric-net-loss and two-day-garden-work guarantees. Corrected the land-trust diagram's foreclosure immunity, automatic tax shelter, and perpetual-safety implications. Kept Priya's limitations on her field trial and contaminated-ground boundary. Root replaced the opening image separately. |
| Chapter 16, Media Autonomy | Retained the earned success, conditional income, rights checks, consent, separate copies, and IPFS availability limits. No edits. Its “year after the first fire” is consistent with the latest three-year narrative, not the older two-year protocol summary. |
| Chapter 17, Tools | Corrected radio band versus firmware selection, public default channel keys, group-message identity limits, routing tests, and power-cycle checks. Replaced the physically implausible regional-firmware/RAM explanation in the fictional outage with a missed cold-start test after an update. Removed lossless DC and fixed percentage-loss claims; voltage matching remains explicit. Matched alt text to the separate LoRa figure redesign. |
| Chapter 18, Roadmap | Retained the open welding-capacity gap, funded-through-June versus proposed continuation, worker support, and accountable service test. Verified the initially suspicious 2004 SSA independent-testing claim against GAO's recommendation follow-up; it is supported, despite the report itself dating from 2000. No edits. |
| Chapter 19, Ladder | Distinguished partial historical precedents from full implementation of all seven proposals. Corrected French law, NYC counsel eligibility, New Communities' replacement property, and UCL proposal provenance. Clarified that monthly local measurements need coverage work and public totals, not personal records. Kept money optional and CT's recorded first-person mission unchanged. Corrected the NHS account to include legislation, financing, and negotiation. |
| Conclusion | Changed the remaining route-funding deadline from June to December to honor Chapter 19's vote. Removed a guarantee of monotonic technical improvement. Kept the author’s forecast, moral mandate, three-year narrative, and Bear Flag bookend. |

## Editorial authority and decisions

Read `CLAUDE.md`, the main README single-source rules, the book README, `VOICE-GUIDE.md`, `ELIJAH-PROTOCOL.md`, and the v0.9.2 plan and edition notes. The argument, narrative, and field-manual registers remain distinct. No new first-person motive or mission was supplied for CT. The documented anger, food-first priorities, money-optional position, and legal route through institutions remain.

The current manuscript deliberately uses a three-year Bear Flag-to-Bear Flag arc: Chapter 16 occurs a year after the first fire, Chapter 18 has the shouse's second winter and Frank's full year, and the Conclusion explicitly says three years. The older protocol described two years and contained other superseded scene details. The guide now follows the current three-year manuscript and its December funding decision.

Two closing lessons were synchronized with Appendix D through root:

- P-23: “When someone says we can't afford to make a need free, ask how it became free somewhere else: who decided, who paid, and who kept the service running.”
- P-24 mechanism: the present version does not settle a technology's future, and neither improvement nor failure is guaranteed. The existing rule still requires actual results to change the optimistic plan.

## Sources opened for the corrections

These are targeted verification, not a claim that every citation in all eleven chapters was independently re-audited.

| Primary source | What was checked |
| --- | --- |
| [Shumailov et al., Nature (2024)](https://www.nature.com/articles/s41586-024-07566-y) | Collapse under specified recursive-training conditions, tail loss, narrowed distributions, and drift. The chapter's equation is explicitly a schematic, not an attributed theorem. |
| [llama.cpp server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) | Context, KV-cache storage, parallel slots, GPU/offload options. A fixed 20 percent overhead cannot establish fit for every workload. |
| [DOE, insulation and air-sealing details](https://www.energy.gov/cmei/buildings/articles/energy-efficient-home-improvement-credit-insulation-and-air-sealing) | Continuity at seams and penetrations matters; insulation alone isn't an automatic whole-assembly air barrier. |
| [France, Law 2016-138, Article 1](https://www.legifrance.gouv.fr/eli/loi/2016/2/11/2016-138/jo/texte) | Original 2016 law, priority hierarchy, prohibition on deliberately spoiling consumable surplus, proposed donation agreements, and food-safety boundary. |
| [Meshtastic, mesh algorithm](https://meshtastic.org/docs/overview/mesh-algo/) | Finite radio paths and hops, managed flooding, acknowledgment/retry behavior. No routing protocol guarantees an alternate physical path. |
| [Meshtastic, LoRa configuration](https://meshtastic.org/docs/configuration/radio/lora/) | Region is a software setting, matching radio parameters, frequency and transmission limits. |
| [Meshtastic, encryption](https://meshtastic.org/docs/overview/encryption/) | Public default shared channel key; group-channel limitations; distinction from direct-message cryptography. |
| [Meshtastic, official web flasher repository](https://github.com/meshtastic/web-flasher) | Official installer, target device selection, and serial diagnostic workflow. |
| [DOE, DC Microgrid Scoping Study](https://www.energy.gov/sites/prod/files/2015/03/f20/DC_Microgrid_Scoping_Study_LosAlamos-Mar2015.pdf) | Both distribution and conversion losses remain; DC/DC and AC/DC conversion efficiencies must be compared under stated assumptions. |
| [NYC Office of Civil Justice, FY2022 annual report](https://www.nyc.gov/assets/hra/downloads/pdf/services/civiljustice/OCJ_UA_Annual_Report_2022.pdf) | Full representation threshold at 200 percent of federal poverty guidelines and brief assistance above it. The 78 percent outcome refers to represented households. |
| [UCL, Future welfare: Universal Basic Services](https://www.ucl.ac.uk/bartlett/ideas/bartlett-review/bartlett-review-2017/future-welfare-universal-basic-services) | £42 billion proposal, specified services, personal allowance funding, and its status as a proposal. Replaces Wikipedia and secondhand follow-up as the passage's evidentiary basis. |
| [UK Government History, founding of the NHS](https://history.blog.gov.uk/2023/07/13/the-founding-of-the-nhs-75-years-on/) | Pre-NHS coverage limits; financing, institutional change, legislation, and negotiation before July 1948. |
| [GAO, SSA Year 2000 readiness](https://www.gao.gov/products/aimd-00-125) | Recommendations' implementation history explicitly records independent validation procedures in April 2004. Retained. |
| [GAO, Y2K lessons learned](https://www.gao.gov/assets/aimd-00-290.pdf) | Original retrospective remains the source for the operational examples in P-22. |

## Figure scope

Seven existing code-native SVGs received bounded text corrections, keeping their composition and palette:

- `ch10-model-collapse.svg`
- `ch10-algorithm-unlock.svg`
- `ch13-thermal-seal.svg`
- `ch14-mesh-comms.svg`
- `ch15-clt-firewall.svg`
- `ch17-dc-native.svg`
- `ch19-conversion-ladder.svg`

Root was notified before print-copy regeneration. A separate agent owns legibility redesigns, including `ch17-lora-node.svg` and `ch11-cooling-loop.svg`. The old rights-unclear opening images in Chapters 10, 12, and 15 were replaced by root, without changing these chapter-body reviews.

## Verification and limits

- Read the modified prose back from disk and inspected its surrounding paragraphs.
- `git diff --check` passed after the corrections.
- All seven modified SVGs parsed as XML.
- Twenty-one checks for the specific retired defects passed. Each detector first or concurrently detected its corresponding deliberately reintroduced defect in an in-memory manuscript copy. No working file was corrupted for this test.
- No em dashes or unfinished TODO/TBD/FIXME markers were found in the eight edited chapters.

Those checks observe the listed stale claims, syntax, and punctuation. They do not validate a building, electrical installation, community program, hardware purchase, or every book assertion. No equipment was built or measured during this editorial pass. Current product availability and every historical anecdote were not re-researched. Root owns the regenerated index, release gates, full publication builds, and visual proofs; this report does not predeclare those results.
