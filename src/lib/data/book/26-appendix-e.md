# APPENDIX E: THE CYBERDECK

*Chapter 17 gave you the workbench. This is the machine that can come off it. A cyberdeck is a personal computer you assemble or adapt around the functions you want to control. Choose hardware and software that can do those jobs without a cloud or a subscription. It's optional. Everything here starts with the device already in your pocket.*

![A homemade cyberdeck: a rugged hard case holding a mechanical keyboard, an amber map-lit screen, and a stub antenna](/book-images/appe-cyberdeck.png)

*A computer you understand all the way down, that answers to nobody's server.*

## The word, and where it came from

The word is older than the hardware. William Gibson coined "cyberspace deck" in 1984, in *Neuromancer*, for the machine his console cowboys jacked into the matrix with. He never described it in much detail, so for almost thirty years a cyberdeck was a hole in a novel, shaped exactly like the machine you wished you owned.

The hole started filling in around 2012, when the Raspberry Pi put a whole Linux computer on a credit-card board for thirty-five dollars. Suddenly the fictional deck had a plausible brain. Hobbyists began building physical versions and posting them, and a scene formed around community sites and Hackaday's cyberdeck contests. For a decade it stayed a maker subculture.

In 2026, it began reaching a wider audience.

## The 2026 return

Newsweek ran an explainer calling cyberdecks Gen Z's new DIY obsession. [Newsweek, What is a cyberdeck](https://www.newsweek.com/what-is-a-cyberdeck-gen-zs-new-custom-computing-obsession-11787017) TechCrunch covered the same wave from a different door: communities that had exploded thanks largely to women on social media, building artistic, hyper-personal machines and documenting every step, including one builder's seashell that hides a small computer and a local AI. [TechCrunch, Cyberdecks are having a moment](https://techcrunch.com/2026/06/02/cyberdeck-tiktok-trend-reject-big-tech/)

The interesting part isn't the look. It's the stated reason. Ask the people building these why, and a lot of them give you the argument this book has been making: they want a device that's theirs, that isn't quietly watching them, that nobody can meter or brick from a server, and that they can fix with parts from a thrift store.

That's the smart-home trap from Chapter 17, understood from the inside and answered with a soldering iron. It's Create Over Consume wearing a case somebody printed at two in the morning. And it's worth an appendix because it's one of the few places in consumer culture where lots of ordinary people are voluntarily walking back out of the walled garden, on their own. That's a signal. Signals like that are why you watch culture and not just earnings calls.

## Why this belongs in a survival book

Strip the aesthetics and a cyberdeck bundles four capabilities that keep working when the network doesn't:

1. **Local knowledge.** An offline copy of the reference material you'd otherwise search for. The open-source Kiwix project packages all of Wikipedia, plus medical libraries, repair guides, and more, into files that live on the device. When the towers drop, as they do in the Chapter 17 storm, the librarian is still in your pack.
2. **Local intelligence.** A small language model running on the device itself, no network required: a pocket version of the Crucible from Chapter 11. Its answers still need checking, like any model's.
3. **Local communication.** A mesh radio, the same LoRa and Meshtastic hardware as the co-op's network, for short messages over a tested radio path. Two nodes may reach directly; terrain can require relays, and some routes won't work.
4. **Spectrum awareness.** A cheap receive-only software-defined radio, to listen to the world that's still broadcasting when the internet isn't: weather, aircraft, emergency nets.

Here's the honest part: a phone can do a surprising amount of this too. Kiwix runs on phones. A Meshtastic radio pairs with one over Bluetooth. Small models run on recent phones. Many phones make repair and component replacement difficult. A well-documented deck can give you more control over those choices, though it still needs supported software and obtainable parts. Neither one is required to take part in anything in this book.

## The anatomy

There's no official parts list, which is the point. But most decks have the same five organs.

- **The brain.** A single-board computer supported by the software you need. Raspberry Pi is one well-documented option. Match the power supply to the exact board and peripherals, then check temperature and runtime under your workload. Cooling needs depend on that workload and the enclosure. Compute Modules need a compatible carrier board. [Raspberry Pi, computer hardware documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- **The body.** An integrated handheld such as the ClockworkPi uConsole or Hackberry Pi can supply the screen, keyboard, and battery mounting. Read the exact kit contents before budgeting: uConsole offers a version without the compute module and excludes battery cells. Assembly, software, and accessories still need work. [ClockworkPi, uConsole](https://www.clockworkpi.com/uconsole); [ZitaoTech, Hackberry Pi](https://github.com/ZitaoTech/Hackberry-Pi_Zero)
- **The eyes and hands.** A small display and a physical keyboard you can read in a field and type on with cold fingers.
- **The loadout.** The four capabilities above, chosen for your life. A caregiver leans toward medical libraries. A ham operator leans toward the radio. Nobody carries everything; the deck is a statement about what you refuse to be without.
- **The shell.** A printed enclosure, a repurposed case, or a waterproof box. That's where the personality lives, and where the weatherproofing lives.

Power ties it together. Most decks run on low-voltage DC, from a packaged battery with its own protection circuit or a small power station, which makes them a natural first load for the DC corner in Chapter 17. Don't build lithium packs from salvaged cells unless you've been properly taught; buy a protected pack.

## The three tiers

Don't start with the seashell that runs a local AI. Build capability in order, and let each tier work before you add the next.

**Tier 0, the phone you have.** Save one non-sensitive reference you're allowed to copy, turn off the network, and confirm you can open it and find what you need. Write down its source and date so you'll know when it's stale. That's the offline habit, for free.

![A phone and an offline retrieval test: save a reference you may copy, record source and date, turn the network off, then open the copy and find an answer.](/book-images/v103-offline-check.svg)

*Tier 0 ends with a test: can you open the reference and find what you need with the network off? Record the source and date so you know which copy you have.*

**Tier 1, the Communicator.** A supported Meshtastic board, flashed with the firmware for that hardware, configured for your region, and paired to your phone. Budget for the antenna, battery, and enclosure as well as the board. Test a short message with a second compatible node before counting on a route. Terrain, placement, power, and settings decide whether the link works. Default channel keys are public; use a randomly generated shared key for a private group and decide whether location sharing belongs on. [Meshtastic, channel configuration](https://meshtastic.org/docs/configuration/radio/channels/)

**Tier 2, the Librarian.** A supported computer, a screen, suitable protected power, and Kiwix loaded with the libraries you'd actually reach for. Check file size and edition before downloading, as Chapter 16 explains. Open the archive with the network off and find a specific answer. Add a small local model only if the hardware supports it; keep its generated answers distinct from the reference text.

**Tier 3, the Field Station.** Start from a compatible handheld and test its power budget with every peripheral connected. Add a receive-only software-defined radio and an antenna suitable for the public broadcasts you intend to receive. Fold in the mesh and library, then configure and test storage encryption and recovery. Integration earns this tier; buying four parts doesn't.

## Owning the stack means securing it, and staying legal

Two warnings, because the cyberdeck world runs right up against lines this book won't cross with you.

First, the honest part. A deck holds your life: notes, keys, maps, your questions. A machine you carry is a machine that can get lost or taken. Use storage encryption supported by your operating system, a strong passphrase, and a separate backup you have tested. Encryption protects stored data while it is locked; it doesn't make an unlocked or compromised computer safe. A local machine still needs updates from sources you've verified, sensible passwords, and a clear idea of what it's connected to. [Cryptsetup FAQ](https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/FAQ.md)

Second, the boundary. The same hardware skills overlap with offensive security work, and a lot of cyberdeck content online is really about getting into other people's networks. This book's use is defensive and personal, never offensive, and there are two hard lines with real penalties behind them:

- **Access.** Get permission before testing someone else's computer or network, and stay inside that permission. Unauthorized access can violate computer-misuse laws, including the US Computer Fraud and Abuse Act. [18 U.S.C. 1030](https://www.law.cornell.edu/uscode/text/18/1030)
- **Spectrum.** Check the rules for your location and the service you intend to use. Some transmissions need an individual license; others are allowed only with compliant equipment and operating conditions. Reception and disclosure have their own restrictions, so an audible signal isn't permission to record or share it. Start with public broadcasts and your own authorized links. [US interception statute, including its exceptions](https://www.law.cornell.edu/uscode/text/18/2511); [US Part 15 operating conditions](https://www.law.cornell.edu/cfr/text/47/15.5).

Build the deck to keep yourself free, not to reach into anyone else's life. The tool doesn't decide that for you. You do.

## The practice

In 1968 Stewart Brand put three words on the cover of the *Whole Earth Catalog*: Access to Tools (P-21). The cyberdeck is that catalog collapsed into one object: not a computer you're allowed to use, but a computer you understand, can repair, and can't be locked out of.

1. **Test the Communicator this month.** Pair a supported node with your phone and exchange a message with another node using compatible settings. Borrow equipment for the trial if you can. Record where the link works and where it fails.
2. **Load a Librarian.** Put Kiwix and one relevant offline collection onto a supported device. Record its edition date, disconnect the network, and confirm you can search it. A stored reference is useful only if you can retrieve it when needed.
3. **Try one model offline, if your device supports it.** Disable Wi-Fi and cellular data and unplug wired networking. Ask a question you can check against the saved library. A returned answer proves the model ran; a checked answer tells you whether it helped.

Start with one weekend and the device you have. Keep the capability that worked, then build the next one.
